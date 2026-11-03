#!/usr/bin/env python3
"""gen_T29.py - generated tables of 02-language/SCOPE-AND-VARIABLES.md (task T29, rule 9).

Purpose : table of every name constant in SpecialVariables.cs (automatic, preference and engine variables)
          with source line and reference count, from data/auto-variables.json; plus the two fixed-order enums.
Inputs  : data/auto-variables.json, data/enums.json
Outputs : fills <!--GEN:specialvars--> ... <!--/GEN:specialvars--> in docs-out/02-language/SCOPE-AND-VARIABLES.md
Run     : python3 docs-out/tools/gen_T29.py [--count constants]
Label   : APPROX (regex scan of `internal const string` fields; reference counts are textual).
Language: Python 3 (D-002)
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
SV = "src/System.Management.Automation/engine/SpecialVariables.cs"


def main():
    a = json.load(open(os.path.join(DATA, "auto-variables.json")))["constants"]
    if len(sys.argv) > 2 and sys.argv[1] == "--count":
        if sys.argv[2] == "execcontext":
            m = json.load(open(os.path.join(DATA, "members-tierA.json")))
            x = [t for t in m if t["file"].endswith("engine/ExecutionContext.cs") and t["full_name"].endswith(".ExecutionContext")][0]
            print(len(x["members"]))
        else:
            print(len(a))
        return 0
    en = {e["full_name"].split(".")[-1]: e for e in json.load(open(os.path.join(DATA, "enums.json"))) if e["file"] == SV}
    rows = ["| Field | Variable name | Line | References (APPROX) |", "|---|---|---:|---:|"]
    for c in sorted(a, key=lambda x: x["line"]):
        rows.append(f"| `{c['field']}` | `${c['name']}` | L{c['line']} | {c['reference_count']} |")
    rows.append("")
    for n in ("AutomaticVariable", "PreferenceVariable"):
        e = en[n]
        rows.append(f"`{n}` (`{SV}::{n}@L{e['start']}-L{e['end']}`): " + ", ".join(f"`{m['name']}`={m['value'] if m['value'] not in (None, '') else i}" for i, m in enumerate(e["members"])))
        rows.append("")
    p = os.path.join(OUT, "02-language", "SCOPE-AND-VARIABLES.md")
    t = open(p, encoding="utf-8").read()
    pat = re.compile(r"(<!--GEN:specialvars-->)\n?.*?\n?(<!--/GEN:specialvars-->)", re.S)
    if not pat.search(t):
        print("region missing")
        return 1
    open(p, "w", encoding="utf-8").write(pat.sub(lambda m: m.group(1) + "\n" + "\n".join(rows) + "\n" + m.group(2), t))
    print("special variable constants", len(a))


if __name__ == "__main__":
    sys.exit(main())
