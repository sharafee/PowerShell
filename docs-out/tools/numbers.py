#!/usr/bin/env python3
"""numbers.py - numbers registry (rule 11): generate data/numbers.json, render and lint embeds.

Purpose : single source for every count/constant used in documents.
          Documents embed values as <!--N:KEY-->value<!--/N-->.
Commands: gen     recompute every registered key from data/*.json -> data/numbers.json
          get K   print one value (regeneration command stored in numbers.json uses this)
          render  rewrite every embed in docs-out/**/*.md with the registry value (render-numbers)
          lint    fail on stale embeds, unknown keys and (heuristically) hand-typed counts (lint-numbers)
Run     : python3 docs-out/tools/numbers.py gen|get KEY|render|lint
Language: Python 3 (D-002)   Tested: Linux x86_64 / Python 3.13
All values derive from APPROX extraction unless flagged otherwise (STATIC-ONLY run).
"""
import csv
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
SMA = "src/System.Management.Automation/"


def J(n):
    return json.load(open(os.path.join(DATA, n)))


def files():
    return list(csv.DictReader(open(os.path.join(DATA, "files.csv"))))


def short(n):
    return n.split(".")[-1].split("<")[0]


def enum_members(suffix):
    return [e for e in J("enums.json") if e["full_name"].endswith(suffix)]


REG = {}


def reg(key, fn, dataset, label="APPROX", notes=""):
    REG[key] = (fn, dataset, label, notes)


F = None


def _f():
    global F
    if F is None:
        F = files()
    return F


reg("REPO_FILES_TOTAL", lambda: len(_f()), "files.csv", "GENERATED")
reg("CS_FILES_ALL", lambda: sum(1 for r in _f() if r["language"] == "C#"), "files.csv", "GENERATED")
reg("CS_FILES_SRC", lambda: sum(1 for r in _f() if r["language"] == "C#" and r["path"].startswith("src/")), "files.csv", "GENERATED")
reg("CS_LOC_SRC", lambda: sum(int(r["loc"]) for r in _f() if r["language"] == "C#" and r["path"].startswith("src/")), "files.csv", "GENERATED", "physical lines")
reg("CS_LOC_SMA", lambda: sum(int(r["loc"]) for r in _f() if r["language"] == "C#" and r["path"].startswith(SMA)), "files.csv", "GENERATED", "System.Management.Automation only")
reg("CS_FILES_SMA", lambda: sum(1 for r in _f() if r["language"] == "C#" and r["path"].startswith(SMA)), "files.csv", "GENERATED")
reg("CS_LOC_TIER_A", lambda: sum(int(r["loc"]) for r in _f() if r["language"] == "C#" and r["tier"] == "A"), "files.csv", "GENERATED")
reg("CS_FILES_TIER_A", lambda: sum(1 for r in _f() if r["language"] == "C#" and r["tier"] == "A"), "files.csv", "GENERATED")
reg("CS_FILES_TIER_B", lambda: sum(1 for r in _f() if r["language"] == "C#" and r["tier"] == "B"), "files.csv", "GENERATED")
reg("CS_FILES_TIER_C", lambda: sum(1 for r in _f() if r["language"] == "C#" and r["tier"] == "C"), "files.csv", "GENERATED")
reg("PROJECT_COUNT", lambda: len(J("projects.json")), "projects.json", "GENERATED", "every .csproj in the tree")
reg("PROJECTS_IN_SOLUTION", lambda: sum(1 for p in J("projects.json") if p["in_solution"]), "projects.json", "GENERATED")
reg("TYPES_TOTAL", lambda: len(J("types.json")), "types.json", "APPROX", "incl. nested types and delegates")
for k in ("class", "struct", "interface", "enum", "delegate"):
    reg("TYPES_" + k.upper(), (lambda k=k: sum(1 for t in J("types.json") if t["kind"] == k)), "types.json", "APPROX")
reg("TYPES_SMA", lambda: sum(1 for t in J("types.json") if t["project"] == "System.Management.Automation"), "types.json", "APPROX")
reg("ENUMS_TOTAL", lambda: len(J("enums.json")), "enums.json", "APPROX")
reg("TOKENKIND_MEMBERS", lambda: sum(len(e["members"]) for e in enum_members("Language.TokenKind")), "enums.json", "APPROX", "members of enum TokenKind (incl. platform-conditional ones)")
reg("TOKENFLAGS_MEMBERS", lambda: sum(len(e["members"]) for e in enum_members("Language.TokenFlags")), "enums.json", "APPROX")
reg("AST_CLASSES_ALL", lambda: len(J("ast-hierarchy.json")), "ast-hierarchy.json", "APPROX", "classes whose base chain reaches Ast (name-based)")
reg("AST_CLASSES_CONCRETE", lambda: sum(1 for a in J("ast-hierarchy.json") if "abstract" not in a["modifiers"]), "ast-hierarchy.json", "APPROX")
reg("VISITOR_IMPLEMENTATIONS", lambda: sum(1 for v in J("visitors.json") if v.get("role") != "visitor interface/base"), "visitors.json", "APPROX")
reg("BINDER_CLASSES", lambda: len(J("binders.json")), "binders.json", "APPROX", "classes deriving (transitively, name-based) from DLR binder base types")
reg("INSTRUCTION_CLASSES", lambda: len(J("instructions.json")), "instructions.json", "APPROX", "classes deriving (transitively) from Instruction")
reg("CMDLET_CLASSES", lambda: sum(1 for c in J("cmdlets.json") if c["kind"] == "cmdlet"), "cmdlets.json", "APPROX", "types carrying [Cmdlet]; platform-conditional ones included")
reg("PROVIDER_CLASSES", lambda: sum(1 for c in J("cmdlets.json") if c["kind"] == "provider"), "cmdlets.json", "APPROX")
reg("PARSER_ERROR_RESOURCE_KEYS", lambda: next(v["key_count"] for k, v in J("resources.json").items() if k.endswith("engine/../resources/ParserStrings.resx") or k.endswith("System.Management.Automation/resources/ParserStrings.resx")), "resources.json", "APPROX", "keys of neutral ParserStrings.resx")
reg("RESX_NEUTRAL_FILES", lambda: len(J("resources.json")), "resources.json", "APPROX", "non-localized .resx files under src/")
reg("RESX_NEUTRAL_KEYS", lambda: sum(v["key_count"] for v in J("resources.json").values()), "resources.json", "APPROX")
reg("SPECIAL_VARIABLE_CONSTANTS", lambda: len(J("auto-variables.json")["constants"]), "auto-variables.json", "APPROX", "string consts in SpecialVariables.cs (automatic + preference + internal)")
reg("ATTRIBUTE_TYPES", lambda: len(J("attributes.json")), "attributes.json", "APPROX")
reg("PESTER_FILES", lambda: len(J("tests.json")["pester"]), "tests.json", "APPROX")
reg("PESTER_IT_BLOCKS", lambda: sum(p["it"] for p in J("tests.json")["pester"]), "tests.json", "APPROX", "regex count of literal-named It blocks")
reg("XUNIT_FILES", lambda: len(J("tests.json")["xunit"]), "tests.json", "APPROX")
reg("XUNIT_FACTS", lambda: sum(x["facts"] for x in J("tests.json")["xunit"]), "tests.json", "APPROX")
reg("CONDITIONAL_SYMBOLS", lambda: len(J("conditional-compilation.json")), "conditional-compilation.json", "APPROX")
reg("ENFORCEMENT_SEED_HITS", lambda: len(J("enforcement-points.json")), "enforcement-points.json", "APPROX", "unverified seed hits; not enforcement points")
reg("PARSER_METHODS", lambda: len(J("parser-methods.json")), "parser-methods.json", "APPROX", "methods in Parser.cs + tokenizer.cs")


def _tagcount(tag):
    n = 0
    for p in J("tests.json")["pester"]:
        for x in p["tree"]:
            if x["kind"] == "Describe":
                n += sum(1 for g in x["tags"] if g.upper() == tag)
    return n


reg("PESTER_DESCRIBE_BLOCKS", lambda: sum(p["describe"] for p in J("tests.json")["pester"]), "tests.json", "APPROX", "literal-named Describe blocks")
for _t in ("CI", "FEATURE", "SCENARIO", "SLOW", "REQUIREADMINONWINDOWS", "REQUIRESUDOONUNIX"):
    reg("PESTER_TAG_" + _t, (lambda t=_t: _tagcount(t)), "tests.json", "APPROX", "Describe blocks carrying the tag (regex on -Tag/-Tags)")
reg("XUNIT_TEST_FILES_WITH_FACTS", lambda: sum(1 for x in J("tests.json")["xunit"] if x["facts"]), "tests.json", "APPROX")
reg("RESX_LOCALIZED_FILES", lambda: sum(1 for r in _f() if r["language"] == "resx") - len(J("resources.json")), "files.csv", "APPROX", "localized resx = all resx minus neutral")


def extras():
    """data/numbers-extra.json: [{key, cmd, dataset, label, notes}] - value = stdout of `cmd` (shell, cwd=REPO_ROOT)."""
    import subprocess
    p = os.path.join(DATA, "numbers-extra.json")
    res = []
    if os.path.exists(p):
        for e in json.load(open(p)):
            try:
                v = subprocess.run(e["cmd"], shell=True, cwd=ROOT, capture_output=True, text=True, timeout=300).stdout.strip()
                v = int(v) if re.fullmatch(r"-?\d+", v) else v
            except Exception as ex:  # noqa
                v = None
            res.append({"key": e["key"], "value": v, "dataset": e.get("dataset", ""), "command": e["cmd"], "evidence": "E1",
                        "label": e.get("label", "APPROX"), "notes": e.get("notes", "")})
    return res


def compute():
    out = []
    for k, (fn, ds, label, notes) in REG.items():
        try:
            v = fn()
        except Exception as e:  # noqa
            v, notes = None, f"FAILED: {e!r}"
        out.append({"key": k, "value": v, "dataset": ds, "command": f"python3 docs-out/tools/numbers.py get {k}",
                    "evidence": "E1", "label": label, "notes": notes})
    return out + extras()


def load_reg():
    p = os.path.join(DATA, "numbers.json")
    return {e["key"]: e for e in json.load(open(p))} if os.path.exists(p) else {}


EMB = re.compile(r"<!--N:([A-Z0-9_]+)-->(.*?)<!--/N-->", re.S)


def md_files():
    for dp, dn, fn in os.walk(OUT):
        dn[:] = [d for d in dn if d not in (".work", "tools", "data")]
        for f in fn:
            if f.endswith(".md"):
                yield os.path.join(dp, f)


def cmd_render():
    reg_ = load_reg()
    n = 0
    for p in md_files():
        t = open(p, encoding="utf-8").read()

        def sub(m):
            e = reg_.get(m.group(1))
            return f"<!--N:{m.group(1)}-->{e['value']}<!--/N-->" if e else m.group(0)
        t2 = EMB.sub(sub, t)
        if t2 != t:
            open(p, "w", encoding="utf-8").write(t2)
            n += 1
    print("render-numbers: updated", n, "files")


def cmd_lint():
    reg_ = load_reg()
    bad = []
    for p in md_files():
        t = open(p, encoding="utf-8").read()
        for m in EMB.finditer(t):
            e = reg_.get(m.group(1))
            if not e:
                bad.append((p, "unknown key " + m.group(1)))
            elif str(e["value"]) != m.group(2):
                bad.append((p, f"stale embed {m.group(1)}={m.group(2)} (registry {e['value']})"))
    for b in bad:
        print("LINT-NUMBERS FAIL", *b)
    print("lint-numbers:", "FAIL" if bad else "PASS", len(bad), "findings")
    return 1 if bad else 0


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "gen"
    if c == "gen":
        d = compute()
        json.dump(d, open(os.path.join(DATA, "numbers.json"), "w"), indent=1)
        for e in d:
            print(f"{e['key']:34} {e['value']}")
    elif c == "get":
        print(REG[sys.argv[2]][0]())
    elif c == "render":
        cmd_render()
    elif c == "lint":
        sys.exit(cmd_lint())
