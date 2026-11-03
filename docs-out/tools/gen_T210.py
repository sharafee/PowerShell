#!/usr/bin/env python3
"""gen_T210.py - counts for 02-language/02.7-language-features.md (task T210).

Purpose : the feature table of 02.7 is hand-maintained; this tool counts its rows so the number in the text is registered.
Inputs  : docs-out/02-language/02.7-language-features.md
Run     : python3 docs-out/tools/gen_T210.py --count rows
Language: Python 3 (D-002)
"""
import os
import sys

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
p = os.path.join(ROOT, "docs-out", "02-language", "02.7-language-features.md")
t = open(p, encoding="utf-8").read().split("## 5. Data model")[1].split("## 6.")[0]
rows = [l for l in t.split("\n") if l.startswith("| ") and not l.startswith("| Feature") and not l.startswith("|---")]
print(len(rows))
