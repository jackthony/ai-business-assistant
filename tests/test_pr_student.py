"""Check attribution before automated reviews request access to revision-ia."""

import importlib.util
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "pr_student", Path(__file__).resolve().parents[1] / ".github/scripts/pr_student.py"
)
assert _spec is not None and _spec.loader is not None
module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(module)

REPO = "jackthony/ai-business-assistant"


def bot_pr(repo=REPO, body="Closes #54"):
    return {
        "number": 222,
        "user": {"login": "github-actions[bot]"},
        "head": {"repo": {"full_name": repo}, "ref": "issue-54-memoria-persistente"},
        "base": {"ref": "main"},
        "body": body,
    }


def forbidden_api(path):
    pytest.fail(f"Unexpected GitHub API lookup: {path}")


def test_pr_from_a_student_is_attributed_to_its_author():
    assert (
        module.pr_student({"user": {"login": "WhoAllan"}}, REPO, forbidden_api)
        == "WhoAllan"
    )


@pytest.mark.parametrize(
    "pr",
    [
        {"user": {"login": "jackthony"}},
        {"user": {"login": "dependabot[bot]"}},
        bot_pr(repo="another-owner/ai-business-assistant"),
        bot_pr(body="Closes #55"),
        bot_pr(body="Closes #54\nCloses #55"),
    ],
)
def test_untrusted_or_inconsistent_pr_does_not_request_review(pr):
    assert module.pr_student(pr, REPO, forbidden_api) == ""


def test_bot_pr_uses_the_unique_roster_assignee():
    issue_path = f"repos/{REPO}/issues/54"
    responses = {
        issue_path: {"assignees": [{"login": "WhoAllan"}, {"login": "jackthony"}]}
    }
    assert module.pr_student(bot_pr(), REPO, responses.__getitem__) == "WhoAllan"


def test_bot_pr_falls_back_to_a_unique_commit_author():
    responses = {
        f"repos/{REPO}/issues/54": {"assignees": []},
        f"repos/{REPO}/pulls/222/commits?per_page=100&page=1": [
            {"author": {"login": "WhoAllan"}},
            {"author": {"login": "jackthony"}},
            {"author": None},
        ],
    }
    assert module.pr_student(bot_pr(), REPO, responses.__getitem__) == "WhoAllan"
    responses[f"repos/{REPO}/pulls/222/commits?per_page=100&page=1"].append(
        {"author": {"login": "adbon-dm1"}}
    )
    assert module.pr_student(bot_pr(), REPO, responses.__getitem__) == ""
