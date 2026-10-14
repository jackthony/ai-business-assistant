#!/usr/bin/env python3
"""List repo-relative paths cited in backticks inside a markdown file and whether they exist.
Usage: check_paths.py ROOT FILE.md  -> JSON {"missing": [...], "existing": [...]}"""

import json
import os
import re
import sys

root, md = sys.argv[1], sys.argv[2]
text = open(md, encoding="utf-8").read()
PREFIX = (
    "src/",
    "tests/",
    "program/",
    "data/",
    "tools/",
    "configs/",
    "docs/",
    ".github/",
    "notas-estudio/",
    "bitacora/",
    "evidencias/",
)
EXT = re.compile(
    r"^[\w./\\-]+\.(py|md|yml|yaml|json|jsonl|toml|sh|ps1|env|txt|example)$"
)
missing, existing = [], []
for tok in re.findall(r"`([^`\n]+)`", text):
    t = tok.strip().rstrip(".,;:)")
    if any(c in t for c in " *<>{}$|") or t.startswith(("http", "-")):
        continue
    t = t.replace("\\", "/")
    if not (t.startswith(PREFIX) or EXT.match(t)):
        continue
    (existing if os.path.exists(os.path.join(root, t)) else missing).append(t)
print(
    json.dumps(
        {"missing": sorted(set(missing)), "existing": sorted(set(existing))},
        ensure_ascii=False,
    )
)
