#!/usr/bin/env python3
"""gen_T26.py - generated catalogs of task T26 (rule 9).

Purpose : (1) 02-language/BINDER-CATALOG.md - every binder class (data/binders.json): base class, source range,
              creation sites, hand annotation (tools/annotations/T26-binders.json);
          (2) region <!--GEN:runtimeops--> of 02-language/RUNTIME-OPERATIONS.md - every runtime helper type of
              engine/runtime/Operations/*.cs and engine/lang/parserutils.cs with range and member count.
Inputs  : data/binders.json, data/types.json, data/members-tierA.json, annotation file
Outputs : docs-out/02-language/BINDER-CATALOG.md, region of RUNTIME-OPERATIONS.md
Run     : python3 docs-out/tools/gen_T26.py [--count binders|optypes|created]
Label   : APPROX (scanner data); annotations FACT-SRC where marked 'read', UNVERIFIED detail where 'names'.
Language: Python 3 (D-002)
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")


def J(n):
    return json.load(open(os.path.join(DATA, n)))


def esc(s):
    return s.replace("|", "\\|")


def main():
    b = J("binders.json")
    ann = json.load(open(os.path.join(OUT, "tools", "annotations", "T26-binders.json")))["binders"]
    types = J("types.json")
    mem = {(m["file"], m["full_name"]): m["members"] for m in J("members-tierA.json")}
    ops = [t for t in types if "/runtime/Operations/" in t["file"] or t["file"].endswith("lang/parserutils.cs")]
    created = sum(len(x.get("created_or_obtained_at", [])) for x in b)
    if len(sys.argv) > 2 and sys.argv[1] == "--count":
        print({"binders": len(b), "optypes": len(ops), "created": created, "ps_binders": sum(1 for x in b if "Language." in x["name"])}[sys.argv[2]])
        return 0
    L = []
    w = L.append
    w("""---
id: LANG-BINDERCAT-001
title: Binder catalog
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/runtime/Binding/Binders.cs, src/System.Management.Automation/engine/ComInterop/ComBinder.cs, src/System.Management.Automation/engine/ComInterop/ComInvokeAction.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/runtime/_folder.md]
generated_from: [data/binders.json]
---

# Binder catalog

> STATIC-ONLY — behavior not run-verified. The table is `GENERATED` by `docs-out/tools/gen_T26.py` from `data/binders.json` (`APPROX`) joined with hand annotations (`docs-out/tools/annotations/T26-binders.json`). Annotation level **read** = the binder's bind/fallback body was read (`FACT-SRC`); **names** = only member names and the compiler's use were read, details `UNVERIFIED` (VB-020). Narrative: [02.6-types-and-operators.md](02.6-types-and-operators.md), [RUNTIME-OPERATIONS.md](RUNTIME-OPERATIONS.md), [IR-SPEC.md](IR-SPEC.md) §5.
""")
    w("## 1. Purpose and scope [SPEC]\n")
    w(f"""A *binder* is a DLR object that turns an operation on runtime values into code, and caches the result per call site by operand types. Every non-trivial operation in compiled PowerShell code (operators, casts, member access, indexing, enumeration, output writes) is a dynamic call site with one of these binders. The scanner found <!--N:BINDER_CLASSES-->{len(b)}<!--/N--> binder classes (<!--N:BINDER_CLASSES_PS-->{sum(1 for x in b if 'Language.' in x['name'])}<!--/N--> in `Binders.cs`, the rest COM interop), with <!--N:BINDER_CREATION_SITES-->{created}<!--/N--> creation or lookup sites.
""")
    w("## 2. Source map\n")
    w("| path | role |\n|---|---|\n| `src/System.Management.Automation/engine/runtime/Binding/Binders.cs` | all PowerShell binders (8,015 lines) |\n| `src/System.Management.Automation/engine/ComInterop/ComBinder.cs`, `ComInvokeAction.cs` | COM member and invoke binders (out of scope, listed for completeness) |\n")
    w("## 3. Binder table\n")
    w("| Binder | Base | Operation (annotation) | Level | Used for | Creation sites | Source |")
    w("|---|---|---|---|---|---:|---|")
    miss = []
    for x in sorted(b, key=lambda z: (z["file"], z["start"])):
        short = x["name"].split("Language.")[-1].split("ComInterop.")[-1]
        a = ann.get(short)
        if a is None:
            if "ComInterop" in x["name"]:
                a = ["names", "COM interop binder (out of scope).", "COM objects"]
            else:
                miss.append(short)
                a = ["?", "?", "?"]
        base = ", ".join(f"`{q}`" for q in x["bases"]) or "—"
        w(f"| `{short}` | {base} | {esc(a[1])} | {a[0]} | {esc(a[2])} | {len(x.get('created_or_obtained_at', []))} | `{x['file']}::{short.split('.')[-1]}@L{x['start']}-L{x['end']}` |")
    w(f"\nRows: **{len(b)}** (`GENERATED`). Binders without annotation: {', '.join(miss) or 'none'}.\n")
    w("## 4. Common mechanics [IMPL]\n")
    w("""- **Defer when values are missing**: a binder first checks `target.HasValue`; if an operand is a `PSObject` wrapper with a different base object it defers to a PSObject-aware path (`DeferForPSObject`), except `Add` on enumerables.
- **Restrictions**: each produced rule is guarded by type restrictions (`PSGetTypeRestriction`) and, for conversions, by a binder *version* and the language mode, so a language-mode change or a type-table change invalidates cached rules (`InvalidateCache`, version counters; `ExecutionContext.LanguageMode` setter).
- **Per-site caches**: each emitted dynamic expression has its own `CallSite`; both execution tiers use them ([EQUIVALENCE-SPEC.md](EQUIVALENCE-SPEC.md) EQ-02).
- **Fallback with error suggestion**: binders pass an `errorSuggestion` so that "operation not supported" throws a PowerShell error instead of a DLR error.
""")
    w("## 5. Guidance for MicroteamShell [LESSON]\n")
    w("""- **LSN-BIND-01** [ADAPT] (area: NLD-RUN) Replace DLR binders by explicit dispatch functions per operation (`Add(left, right)`, `Convert(value, type)`, `GetMember(target, name)`, `Index(target, args)`) with a small per-site cache only if profiling shows a need. Why: the DLR is a mechanism, the observable behavior is the rule set. Evidence: `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder@L2119-L3422`.
- **LSN-BIND-02** [REPLICATE] (area: NLD-TYP) Keep the dedicated helper operations (enumerate, to-object-array, write-to-pipe, array-assignment shaping, pipeline-result-to-bool); they encode language rules. Evidence: `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSEnumerableBinder@L518-L780`, `PSPipeWriterBinder@L841-L926`, `PSArrayAssignmentRHSBinder@L935-L1042`, `PSPipelineResultToBoolBinder@L1119-L1178`.
- **LSN-BIND-03** [AVOID] (area: NLD-RUN) Do not port COM binders and `PSGetMemberBinder`'s COM/ETS-adapter paths in the first versions. Replace with a plain reflection member lookup. Evidence: `src/System.Management.Automation/engine/ComInterop/ComBinder.cs::ComBinder@L1-L378`. DEV: DEV-BIND-050
""")
    w("Verification: binder list reconciles with `data/binders.json` (counts above); `PSEnumerableBinder`, `PSToObjectArrayBinder`, `PSPipeWriterBinder`, `PSArrayAssignmentRHSBinder`, `PSPipelineResultToBoolBinder`, `PSConvertBinder.FallbackConvert`, `PSBinaryOperationBinder` (dispatch, add, multiply, divide/remainder, equality, numeric) bodies were read; the others by member list and compiler use.\n")
    open(os.path.join(OUT, "02-language", "BINDER-CATALOG.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    # runtime ops region
    p = os.path.join(OUT, "02-language", "RUNTIME-OPERATIONS.md")
    if os.path.exists(p):
        rows = ["| Type | File | Lines | Members (scan) |", "|---|---|---|---:|"]
        for t in sorted(ops, key=lambda z: (z["file"], z["start"])):
            n = len(mem.get((t["file"], t["full_name"]), []))
            rows.append(f"| `{t['full_name'].split('Automation.')[-1]}` | `{t['file'].split('/')[-1]}` | L{t['start']}-L{t['end']} | {n} |")
        txt = open(p, encoding="utf-8").read()
        pat = re.compile(r"(<!--GEN:runtimeops-->)\n?.*?\n?(<!--/GEN:runtimeops-->)", re.S)
        if pat.search(txt):
            open(p, "w", encoding="utf-8").write(pat.sub(lambda m: m.group(1) + "\n" + "\n".join(rows) + "\n" + m.group(2), txt))
    print("BINDER-CATALOG rows", len(b), "missing annotation", miss, "optypes", len(ops))


if __name__ == "__main__":
    sys.exit(main())
