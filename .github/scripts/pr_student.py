"""Resolve the SENATI student behind a pull request using GitHub metadata."""

import json
import os
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROBOT = "github-actions[bot]"
ROSTER = frozenset(
    entry["login"]
    for entry in json.loads(
        (Path(__file__).resolve().parents[1] / "coach.json").read_text(encoding="utf-8")
    )["alumnos"]
)
ReadAPI = Callable[[str], Any]


def gh_api(path: str) -> Any:
    result = subprocess.run(
        ["gh", "api", path], capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)


def pr_student(pr: dict[str, Any], repo: str, api: ReadAPI = gh_api) -> str:
    """Return one roster login, or an empty string if the attribution is ambiguous."""
    author = (pr.get("user") or {}).get("login", "")
    if author in ROSTER:
        return author
    if author != ROBOT:
        return ""

    head = pr.get("head") or {}
    base = pr.get("base") or {}
    if (head.get("repo") or {}).get("full_name") != repo or base.get("ref") != "main":
        return ""
    branch = re.fullmatch(
        r"(?:issue|tbd)-([1-9]\d*)(?:-[a-z0-9]+)+", head.get("ref") or ""
    )
    closes = set(
        re.findall(
            r"(?i)\b(?:closes|fixes|resolves)\s+#([1-9]\d*)\b", pr.get("body") or ""
        )
    )
    if not branch or closes != {branch[1]}:
        return ""

    try:
        issue = api(f"repos/{repo}/issues/{branch[1]}")
    except subprocess.CalledProcessError as exc:
        if "HTTP 404" in (exc.stderr or ""):
            return ""
        raise
    if issue.get("pull_request"):
        return ""
    owners = {user.get("login") for user in issue.get("assignees", [])} & ROSTER
    if len(owners) == 1:
        return next(iter(owners))
    if owners:
        return ""

    # GitHub attributes these accounts from the commit metadata. If several
    # students contributed, there is no unique fallback.
    number = int(pr["number"])
    authors: set[str] = set()
    for page in range(1, 4):  # GitHub returns at most 250 commits for a PR.
        commits = api(f"repos/{repo}/pulls/{number}/commits?per_page=100&page={page}")
        authors.update((item.get("author") or {}).get("login", "") for item in commits)
        if len(commits) < 100:
            break
    candidates = authors & ROSTER
    return next(iter(candidates)) if len(candidates) == 1 else ""


def main() -> None:
    repo = os.environ["GH_REPO"]
    if sys.argv[1:] == ["--batch"]:
        pulls = json.load(sys.stdin)
        print(json.dumps({pr["number"]: pr_student(pr, repo) for pr in pulls}))
    elif sys.argv[1:] == ["--event"]:
        event = json.loads(
            Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8")
        )
        print(pr_student(event.get("pull_request") or {}, repo))
    else:
        raise SystemExit("usage: pr_student.py --event | --batch")


if __name__ == "__main__":
    main()
