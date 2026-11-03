#!/usr/bin/env python3
"""gen_T27.py - render 02-language/INSTRUCTION-SET.md (task T27, rule 9).

Purpose : catalog of the interpreter's Instruction classes (data/instructions.json), grouped by file, with
          kind (abstract base / concrete / nested family member), plus the DLR-style generated families that
          the scanner sees as single names (arity tables), and the interpreter infrastructure types.
Inputs  : data/instructions.json, data/types.json
Outputs : docs-out/02-language/INSTRUCTION-SET.md
Run     : python3 docs-out/tools/gen_T27.py        (from the repo root)
          python3 docs-out/tools/gen_T27.py --count instructions|abstract|files
Label   : APPROX (regex scan of `class X : Instruction`); stack effects are in the narrative (read by hand).
Language: Python 3 (D-002)
"""
import json
import os
import sys
from collections import OrderedDict

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")


def main():
    ins = json.load(open(os.path.join(DATA, "instructions.json")))
    if len(sys.argv) > 2 and sys.argv[1] == "--count":
        k = sys.argv[2]
        print(len(ins) if k == "instructions" else sum(1 for x in ins if "abstract" in x["modifiers"]) if k == "abstract" else len({x["file"] for x in ins}))
        return 0
    groups = OrderedDict()
    for x in sorted(ins, key=lambda z: (z["file"], z["start"])):
        groups.setdefault(x["file"], []).append(x)
    L = []
    w = L.append
    w("""---
id: LANG-INSTR-001
title: Instruction set
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/interpreter/Instruction.cs, src/System.Management.Automation/engine/interpreter/InstructionList.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/interpreter/_folder.md]
generated_from: [data/instructions.json, data/types.json]
---

# Instruction set

> STATIC-ONLY — behavior not run-verified. The class list is `GENERATED` by `docs-out/tools/gen_T27.py` from `data/instructions.json` (`APPROX`: classes whose base chain reaches `Instruction`). Stack effects and semantics: [TIERING-POLICY.md](TIERING-POLICY.md) §6 and [EQUIVALENCE-SPEC.md](EQUIVALENCE-SPEC.md). Interpreter structure: [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §7.
""")
    absn = sum(1 for x in ins if "abstract" in x["modifiers"])
    w("## 1. Purpose and scope [SPEC]\n")
    w(f"""The interpreter (the "light compiler" in `engine/interpreter`) executes a flat array of `Instruction` objects over an object stack. This catalog lists the <!--N:INSTRUCTION_CLASSES-->{len(ins)}<!--/N--> instruction classes the scanner found (<!--N:INSTRUCTION_ABSTRACT-->{absn}<!--/N--> abstract bases) in <!--N:INSTRUCTION_FILES-->{len(groups)}<!--/N--> files. Generic families that are expanded by arity (`DynamicInstruction<…>`, `ActionCallInstruction<…>`, `FuncCallInstruction<…>`) are listed once per file by the scanner and described in section 4.
""")
    w("## 2. Source map\n")
    w("| path | role |\n|---|---|")
    w("| `src/System.Management.Automation/engine/interpreter/Instruction.cs` | abstract `Instruction` base, `IInstructionProvider`, `NotInstruction` |")
    w("| `src/System.Management.Automation/engine/interpreter/InstructionList.cs` | `InstructionList` emitter and `InstructionArray` |")
    w("| `src/System.Management.Automation/engine/interpreter/Interpreter.cs` | `Interpreter.Run` loop |\n")
    w("## 3. Instruction classes by file\n")
    for f, xs in groups.items():
        w(f"### `{f.split('/')[-1]}`\n")
        w("| Class | Kind | Base | Source |\n|---|---|---|---|")
        for x in xs:
            n = x["name"].split("Interpreter.")[-1]
            kind = "abstract" if "abstract" in x["modifiers"] else ("sealed" if "sealed" in x["modifiers"] else "concrete")
            w(f"| `{n}` | {kind} | `{x['chain'][0] if x['chain'] else '—'}` | `{f}@L{x['start']}-L{x['end']}` |")
        w("")
    w("## 4. Generated families (not enumerated by the scanner)\n")
    w("""| Family | Members | Evidence |
|---|---|---|
| `DynamicInstruction<…>` | 16 generic classes, 0..15 call arguments (`DynamicInstruction<TRet>` … `<T0..T14,TRet>`) | `src/System.Management.Automation/engine/interpreter/DynamicInstructions.Generated.cs` (notes W1-W2) |
| `ActionCallInstruction<…>` | 10 classes, 0..9 arguments | `src/System.Management.Automation/engine/interpreter/CallInstruction.Generated.cs` |
| `FuncCallInstruction<…>` | 10 classes, 0..9 arguments | same file |
| `GetArrayItemInstruction<T>`, `SetArrayItemInstruction<T>`, `TypeIsInstruction<T>`, `TypeAsInstruction<T>`, `DefaultValueInstruction<T>`, `NewArrayInstruction<T>`, `NewArrayInitInstruction<T>` | created per element type on demand by `InstructionFactory` (15 pre-seeded types) | `src/System.Management.Automation/engine/interpreter/InstructionFactory.cs` |

Counts for these families come from the generated-file notes (`FACT-SRC`), not from `data/instructions.json`.
""")
    w("Verification: instruction class list reconciles with `data/instructions.json` (count above); abstract/sealed taken from the class modifiers; family sizes from the three generated source files read in full (notes `.work/notes/src_System.Management.Automation_engine_interpreter_*`).\n")
    open(os.path.join(OUT, "02-language", "INSTRUCTION-SET.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("INSTRUCTION-SET: classes", len(ins), "abstract", absn, "files", len(groups))


if __name__ == "__main__":
    sys.exit(main())
