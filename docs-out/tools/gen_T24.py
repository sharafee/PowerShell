#!/usr/bin/env python3
"""gen_T24.py - generated check table of 02-language/02.4-semantic-analysis.md (task T24, rule 9).

Purpose : table `Check (member) | Where | Error ID | Trigger (message template) | Runs when` for every
          `nameof(ParserStrings.X)` site in SemanticChecks.cs, SymbolResolver.cs and PSType.cs.
Inputs  : data/types.json, data/members-tierA.json, ParserStrings.resx, the three source files (read-only).
Outputs : fills region <!--GEN:checks--> ... <!--/GEN:checks--> in docs-out/02-language/02.4-semantic-analysis.md
Run     : python3 docs-out/tools/gen_T24.py          (from the repo root)
          python3 docs-out/tools/gen_T24.py --count sites|ids
Label   : APPROX (regex over source; the enclosing member is the innermost member whose line range holds the site).
Language: Python 3 (D-002)
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
S = "src/System.Management.Automation/engine/parser/"
RESX = "src/System.Management.Automation/resources/ParserStrings.resx"
FILES = {
    S + "SymbolResolver.cs": "post-parse, symbol resolution (before semantic checks)",
    S + "SemanticChecks.cs": None,
    S + "PSType.cs": "compile of the root script block (class/enum definition)",
}
STAGE = {
    "SemanticChecks": "post-parse semantic checks (`PerformPostParseChecks`)",
    "RestrictedLanguageChecker": "`data` section semantic check; module-manifest / restricted evaluation; runtime check of data sections",
    "DscResourceChecker": "post-parse, only for classes with `[DscResource()]`",
}


def J(n):
    return json.load(open(os.path.join(DATA, n)))


def esc(s):
    return s.replace("|", "\\|").replace("\n", " ").replace("\r", "")


def sites():
    types = J("types.json")
    members = {(m["file"], m["full_name"]): m["members"] for m in J("members-tierA.json")}
    msgs = {d.get("name"): (d.findtext("value") or "") for d in ET.parse(os.path.join(ROOT, RESX)).getroot().findall("data")}
    rows = []
    for f, stage in FILES.items():
        src = open(os.path.join(ROOT, f), encoding="utf-8-sig").read().split("\n")
        ts = [t for t in types if t["file"] == f]
        for i, l in enumerate(src, 1):
            for m in re.finditer(r"nameof\(ParserStrings\.(\w+)\)", l):
                inner = [t for t in ts if t["start"] <= i <= t["end"]]
                inner.sort(key=lambda t: t["end"] - t["start"])
                tn = inner[0]["full_name"].split("Language.")[-1] if inner else "?"
                mem = "(type level)"
                if inner:
                    mm = [x for x in members.get((f, inner[0]["full_name"]), []) if x.get("start") and x["start"] <= i <= x["end"]]
                    mm.sort(key=lambda x: x["end"] - x["start"])
                    if mm:
                        mem = mm[0]["name"]
                short = tn.split(".")[0]
                rows.append((f, tn, mem, i, m.group(1), msgs.get(m.group(1), "(no message)"), stage or STAGE.get(short, "?")))
    return rows


def main():
    rows = sites()
    if len(sys.argv) > 2 and sys.argv[1] == "--count":
        print(len(rows) if sys.argv[2] == "sites" else len({r[4] for r in rows}))
        return 0
    out = ["| Check (member) | Where | Error ID | Trigger (message template) | Runs when |", "|---|---|---|---|---|"]
    for f, tn, mem, i, eid, msg, stage in rows:
        out.append(f"| `{tn}.{mem}` | `{f}@L{i}` | `{eid}` | {esc(msg)} | {stage} |")
    p = os.path.join(OUT, "02-language", "02.4-semantic-analysis.md")
    t = open(p, encoding="utf-8").read()
    pat = re.compile(r"(<!--GEN:checks-->)\n?.*?\n?(<!--/GEN:checks-->)", re.S)
    if not pat.search(t):
        print("region missing")
        return 1
    t = pat.sub(lambda m: m.group(1) + "\n" + "\n".join(out) + "\n" + m.group(2), t)
    open(p, "w", encoding="utf-8").write(t)
    print("semantic check sites", len(rows), "distinct ids", len({r[4] for r in rows}))


if __name__ == "__main__":
    sys.exit(main())
