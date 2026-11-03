#!/usr/bin/env python3
"""expand_refs.py - expand short reference tokens in a draft into validated evidence references.

Purpose : authors write [[engine/parser/Compiler.cs::Compiler.VisitIfStatement]] or [[File.cs::Type]]
          (file name alone means engine/parser/); this tool replaces each token with
          `src/System.Management.Automation/<dir>/File.cs::Type.Member@Lstart-Lend` using the line ranges in
          data/types.json and data/members-tierA.json. A token that cannot be resolved is left unchanged and
          reported (exit code 1), so no reference is ever invented.
Inputs  : a draft markdown file (argv[1]), data/types.json, data/members-tierA.json
Outputs : writes the expanded text to argv[2]
Run     : python3 docs-out/tools/expand_refs.py <draft.md> <out.md>
Label   : ranges are APPROX (scanner); `validate-refs` re-checks existence and plausibility.
Language: Python 3 (D-002)
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
DATA = os.path.join(ROOT, "docs-out", "data")
BASE = "src/System.Management.Automation/"
TOKEN = re.compile(r"\[\[([\w/\.\-]+\.cs)::([\w\.]+)\]\]")


def main():
    types = json.load(open(os.path.join(DATA, "types.json")))
    members = {(m["file"], m["full_name"]): m["members"] for m in json.load(open(os.path.join(DATA, "members-tierA.json")))}
    by = {}
    for t in types:
        by.setdefault(t["file"], []).append(t)
    text = open(sys.argv[1], encoding="utf-8").read()
    bad = []

    def sub(m):
        f, ref = m.group(1), m.group(2)
        if "/" not in f:
            f = "engine/parser/" + f
        elif f.split("/")[0] in ("interpreter", "runtime", "lang", "parser"):
            f = "engine/" + f
        path = BASE + f
        tn, _, mn = ref.partition(".")
        cands = [t for t in by.get(path, []) if t["full_name"].split("Language.")[-1].split("Automation.")[-1] == tn or t["full_name"].split(".")[-1] == tn]
        if mn and not cands:
            # nested type form Outer.Inner as type
            cands = [t for t in by.get(path, []) if t["full_name"].endswith("." + ref)]
            if cands:
                mn = ""
        if not cands:
            bad.append(m.group(0))
            return m.group(0)
        t = sorted(cands, key=lambda x: x["end"] - x["start"])[0]
        if not mn:
            return f"{path}::{ref}@L{t['start']}-L{t['end']}"
        mm = [x for x in members.get((path, t["full_name"]), []) if x["name"] == mn and x.get("start")]
        if not mm:
            bad.append(m.group(0))
            return m.group(0)
        x = mm[0]
        return f"{path}::{ref}@L{x['start']}-L{x['end']}"

    out = TOKEN.sub(sub, text)
    open(sys.argv[2], "w", encoding="utf-8").write(out)
    for b in bad:
        print("UNRESOLVED", b)
    print("expanded", len(TOKEN.findall(text)) - len(bad), "unresolved", len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
