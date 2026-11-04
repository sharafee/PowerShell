#!/usr/bin/env python3
"""gen_T3.py - generated regions of the Phase 3 runtime documents (03-runtime/), rule 9.

Purpose : fills two regions in each document listed in tools/annotations/T3-docs.json:
          <!--GEN:tests-->    ... <!--/GEN:tests-->      Pester files and xUnit files that match path keywords (data/tests.json)
          <!--GEN:secseeds--> ... <!--/GEN:secseeds-->   unverified security-seed hits (data/enforcement-points.json) under source prefixes
          Also: --count <doc-key>:<pester_files|pester_its|xunit_files|seed_hits> prints one number for numbers proposals.
Inputs  : data/tests.json, data/enforcement-points.json, tools/annotations/T3-docs.json
Outputs : rewrites the regions in the listed documents (nothing else)
Run     : python3 docs-out/tools/gen_T3.py            (render all)
          python3 docs-out/tools/gen_T3.py --count T31:pester_its
Label   : GENERATED; test matching is by path keyword (APPROX); seed hits are scanner hits, not verified enforcement points
Language: Python 3 (D-002)
"""
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
CFG = json.load(open(os.path.join(OUT, "tools", "annotations", "T3-docs.json")))


def J(n):
    return json.load(open(os.path.join(DATA, n)))


def fill(path, tag, rows):
    t = open(path, encoding="utf-8").read()
    pat = re.compile(r"(<!--GEN:%s-->)\n?.*?\n?(<!--/GEN:%s-->)" % (tag, tag), re.S)
    if not pat.search(t):
        print("region missing", tag, path)
        return
    open(path, "w", encoding="utf-8").write(pat.sub(lambda m: m.group(1) + "\n" + "\n".join(rows) + "\n" + m.group(2), t))


def match(path, keys):
    p = path.lower()
    return any(k.lower() in p for k in keys)


def pester(cfg, tests):
    return sorted([x for x in tests["pester"] if match(x["path"], cfg.get("pester", []))], key=lambda x: x["path"])


def xunit(cfg, tests):
    return sorted([x for x in tests["xunit"] if match(x["path"], cfg.get("xunit", []))], key=lambda x: x["path"])


def seeds(cfg, pts):
    pre = cfg.get("sec_prefix", [])
    return [p for p in pts if any(p["file"].startswith(q) for q in pre)]


def tests_rows(cfg, tests):
    ps, xs = pester(cfg, tests), xunit(cfg, tests)
    rows = []
    if ps:
        rows += ["| Pester file | Describe | Context | It |", "|---|---:|---:|---:|"]
        for x in ps[:60]:
            rows.append("| `%s` | %d | %d | %d |" % (x["path"], x["describe"], x["context"], x["it"]))
        if len(ps) > 60:
            rows.append("| (%d more files not listed) | | | %d |" % (len(ps) - 60, sum(x["it"] for x in ps[60:])))
        rows.append("| **total (%d files)** | %d | %d | %d |" % (len(ps), sum(x["describe"] for x in ps), sum(x["context"] for x in ps), sum(x["it"] for x in ps)))
    else:
        rows.append("No Pester file matched the path keywords.")
    rows.append("")
    if xs:
        rows += ["| xUnit file | Facts | Theories | Classes |", "|---|---:|---:|---|"]
        for x in xs:
            rows.append("| `%s` | %d | %d | %s |" % (x["path"], x["facts"], x["theories"], ", ".join("`%s`" % c for c in x["classes"][:4])))
    else:
        rows.append("No xUnit file matched the path keywords.")
    rows += ["", "Matching is by path keyword (`APPROX`): %s." % (", ".join("`%s`" % k for k in cfg.get("pester", []) + cfg.get("xunit", [])) or "none")]
    return rows


def seed_rows(cfg, pts):
    s = seeds(cfg, pts)
    if not s:
        return ["No scanner seed hit under the prefixes of this subsystem (`UNVERIFIED`: absence of a hit is not proof of absence of a check)."]
    c = Counter(p["category"] for p in s)
    f = Counter(p["file"] for p in s)
    rows = ["| Category | Seed hits |", "|---|---:|"]
    for k, v in c.most_common():
        rows.append("| %s | %d |" % (k, v))
    rows.append("| **total** | %d |" % len(s))
    rows += ["", "Files with most hits:", "", "| File | Hits |", "|---|---:|"]
    for k, v in f.most_common(8):
        rows.append("| `%s` | %d |" % (k, v))
    rows += ["", "These are regex scanner hits (`APPROX`, `verified: false`, no `SEC-ENF` ID yet). Phase 5 verifies them and assigns IDs; none is claimed here as an enforcement point."]
    return rows


def main():
    tests, pts = J("tests.json"), J("enforcement-points.json")
    if len(sys.argv) >= 3 and sys.argv[1] == "--count":
        key, what = sys.argv[2].split(":")
        cfg = CFG[key]
        v = {"pester_files": len(pester(cfg, tests)), "pester_its": sum(x["it"] for x in pester(cfg, tests)),
             "xunit_files": len(xunit(cfg, tests)), "seed_hits": len(seeds(cfg, pts))}[what]
        print(v)
        return
    for key, cfg in CFG.items():
        p = os.path.join(OUT, cfg["doc"])
        if not os.path.exists(p):
            continue
        fill(p, "tests", tests_rows(cfg, tests))
        fill(p, "secseeds", seed_rows(cfg, pts))
        print("rendered", key, cfg["doc"])


if __name__ == "__main__":
    main()
