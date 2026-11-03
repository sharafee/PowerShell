#!/usr/bin/env python3
"""gen_T25.py - render 02-language/COMPILATION-MAP.md (task T25, rule 9).

Purpose : table `NodeType -> how it is compiled`: every Compiler.Visit* method with its line range
          (from data/members-tierA.json) joined with hand annotations (tools/annotations/T25-compilation-map.json),
          plus the list of Compiler helper methods with line ranges.
Inputs  : data/members-tierA.json, data/types.json, tools/annotations/T25-compilation-map.json
Outputs : docs-out/02-language/COMPILATION-MAP.md
Run     : python3 docs-out/tools/gen_T25.py        (from the repo root)
          python3 docs-out/tools/gen_T25.py --count visits|helpers
Label   : ranges APPROX (scanner); annotations FACT-SRC (read in Compiler.cs, notes in .work/notes).
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
F = "src/System.Management.Automation/engine/parser/Compiler.cs"


def esc(s):
    return s.replace("|", "\\|")


SUPPORT = {
    "Constant": "yes", "Call": "yes (by-ref or value-type instance call forces full JIT)", "Block": "yes (defines locals)", "Assign": "yes (local, parameter, index, member; not compound)",
    "Dynamic": "yes (DynamicInstruction<...> per site)", "Label": "yes", "Variable": "yes", "NewArrayInit": "yes", "IfThen": "yes", "Catch": "yes (no filters)",
    "Field": "yes (literal/static/instance via reflection)", "TryFinally": "yes", "Property": "yes (getter call)", "New": "yes (by-ref ctor forces JIT)", "Not": "yes (bool only)",
    "Goto": "yes", "Throw": "yes", "Parameter": "yes", "Convert": "numeric convert, otherwise no-op", "Rethrow": "yes", "TryCatch": "yes", "SwitchCase": "int constants only",
    "NotEqual": "numeric/reference", "Condition": "yes", "TryCatchFinally": "yes", "Equal": "numeric/reference", "Switch": "int test values, no comparison method",
    "IfThenElse": "yes", "TypeIs": "yes", "Empty": "yes", "AndAlso": "bool only", "SymbolDocument": "n/a (debug info document)", "Subtract": "yes", "Return": "yes (goto)",
    "OrElse": "bool only", "Multiply": "yes", "Lambda": "nested lambdas via closure", "GreaterThan": "numeric", "Divide": "yes", "DebugInfo": "recorded only", "Continue": "yes (goto)",
    "Break": "yes (goto)", "ArrayAccess": "yes (indexer)", "Add": "yes",
}


def irnodes():
    src = open(os.path.join(ROOT, F), encoding="utf-8-sig").read()
    cnt = Counter(re.findall(r"Expression\.([A-Z][A-Za-z]*)\(", src))
    rows = ["| LINQ factory | Calls in Compiler.cs | Interpreter (LightCompiler) support |", "|---|---:|---|"]
    for k, v in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):
        rows.append(f"| `Expression.{k}` | {v} | {SUPPORT.get(k, '?')} |")
    return rows, len(cnt)


def fill_region(doc, tag, rows):
    p = os.path.join(OUT, "02-language", doc)
    if not os.path.exists(p):
        return
    t = open(p, encoding="utf-8").read()
    pat = re.compile(r"(<!--GEN:%s-->)\n?.*?\n?(<!--/GEN:%s-->)" % (tag, tag), re.S)
    if pat.search(t):
        open(p, "w", encoding="utf-8").write(pat.sub(lambda m: m.group(1) + "\n" + "\n".join(rows) + "\n" + m.group(2), t))


def main():
    mem = json.load(open(os.path.join(DATA, "members-tierA.json")))
    c = [x for x in mem if x["file"] == F and x["full_name"].endswith(".Compiler")][0]
    ann = json.load(open(os.path.join(OUT, "tools", "annotations", "T25-compilation-map.json")))["visits"]
    visits = [m for m in c["members"] if m["name"].startswith("Visit")]
    helpers = [m for m in c["members"] if m.get("kind") == "method" and not m["name"].startswith("Visit") and m.get("start")]
    if len(sys.argv) > 2 and sys.argv[1] == "--count":
        print(len(visits) if sys.argv[2] == "visits" else len(helpers) if sys.argv[2] == "helpers" else irnodes()[1])
        return 0
    missing = [v["name"] for v in visits if v["name"] not in ann]
    extra = [k for k in ann if k not in {v["name"] for v in visits}]
    assert not missing and not extra, (missing, extra)
    L = []
    w = L.append
    w("""---
id: LANG-COMPMAP-001
title: Compilation map
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/parser/Compiler.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/parser/_folder.md]
generated_from: [data/members-tierA.json]
---

# Compilation map

> STATIC-ONLY — behavior not run-verified. Rows are `GENERATED` by `docs-out/tools/gen_T25.py`: method names and line ranges from `data/members-tierA.json` (`APPROX`), the "compiled form" text from the hand-written annotation file `docs-out/tools/annotations/T25-compilation-map.json` (`FACT-SRC`, read in `Compiler.cs`). Narrative: [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md). Intermediate representation: [IR-SPEC.md](IR-SPEC.md).
""")
    w("## 1. Purpose and scope [SPEC]\n")
    w(f"""For every AST node type, how `Compiler` (an `ICustomAstVisitor2`) turns it into a LINQ expression tree. `Compiler` has <!--N:COMPILER_VISIT_METHODS-->{len(visits)}<!--/N--> `Visit*` methods (one per visitor method of `ICustomAstVisitor` plus `ICustomAstVisitor2`, see [AST-CATALOG.md](AST-CATALOG.md) §5) and <!--N:COMPILER_HELPER_METHODS-->{len(helpers)}<!--/N--> other methods (section 4).
""")
    w("## 2. Source map\n")
    w(f"| path | type | role |\n|---|---|---|\n| `{F}::Compiler@L{c['members'][0]['start']}-L{c['members'][-1]['end']}` | class | AST → expression-tree compiler |\n")
    w("## 3. Node → compiled form\n")
    w("| AST node (Visit method) | Compiled form | How (FACT-SRC) | Source |")
    w("|---|---|---|---|")
    for v in visits:
        k, t = ann[v["name"]]
        w(f"| `{v['name'][5:]}Ast` (`{v['name']}`) | {k} | {esc(t)} | `{F}::Compiler.{v['name']}@L{v['start']}-L{v['end']}` |")
    w(f"\nRows: **{len(visits)}** (`GENERATED`). \"not visited\" rows are asserted unreachable in the compiler (their parents handle them).\n")
    w("## 4. Helper methods of Compiler\n")
    w("| Method | Source |\n|---|---|")
    seen = {}
    for h in helpers:
        n = seen.get(h["name"], 0)
        seen[h["name"]] = n + 1
        w(f"| `{h['name']}`{' (overload)' if n else ''} | `{F}::Compiler.{h['name']}@L{h['start']}-L{h['end']}` |")
    w("\nVerification: all 63 `Visit*` methods were read (notes W3-W21); the table is joined by name and the generator asserts that every `Visit*` method has an annotation and vice versa; `VisitPipeline`, `VisitTrap`, `VisitHashtable`, `VisitCatchClause`, `VisitDoWhileStatement` were re-read for this catalog.\n")
    open(os.path.join(OUT, "02-language", "COMPILATION-MAP.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    rows, nk = irnodes()
    fill_region("IR-SPEC.md", "irnodes", rows)
    print("COMPILATION-MAP: visits", len(visits), "helpers", len(helpers), "ir factory kinds", nk)


if __name__ == "__main__":
    sys.exit(main())
