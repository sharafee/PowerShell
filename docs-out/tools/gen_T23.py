#!/usr/bin/env python3
"""gen_T23.py - render 02-language/AST-CATALOG.md from data/*.json (task T23, rule 9).

Purpose : node catalog `NodeType | Base | Children | Created by | Consumed by`, visitor method tables,
          inheritance diagram, enums declared in ast.cs. Never hand-typed.
Inputs  : data/ast-hierarchy.json, data/members-tierA.json, data/visitors.json, data/enums.json,
          src/System.Management.Automation/engine/parser/ast.cs (read-only, InternalVisit bodies).
Outputs : docs-out/02-language/AST-CATALOG.md
Run     : python3 docs-out/tools/gen_T23.py            (from the repo root)
          python3 docs-out/tools/gen_T23.py --count ast_classes|abstract|iv1|iv2|children_gaps
Label   : APPROX. "Children" are the receivers of `.InternalVisit(` calls in the node's InternalVisit method,
          in source order (a raw expression such as `ifClause.Item1` is shown as written). "Created by" is
          `new XAst(` in Parser.cs (data/ast-hierarchy.json). "Consumed by" lists visitor classes defining Visit<Node>.
Language: Python 3 (D-002)
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
ASTCS = "src/System.Management.Automation/engine/parser/ast.cs"
DEFAULT_VISITORS = {"AstVisitor", "AstVisitor2", "ICustomAstVisitor", "ICustomAstVisitor2", "DefaultCustomAstVisitor", "DefaultCustomAstVisitor2"}


def J(n):
    return json.load(open(os.path.join(DATA, n)))


def short(n):
    return n.split(".")[-1]


def nodes():
    h = [x for x in J("ast-hierarchy.json") if x["file"] == ASTCS]
    mem = {short(t["full_name"]): t for t in J("members-tierA.json") if t["file"] == ASTCS}
    return h, mem


def children(src, tmem):
    if not tmem:
        return None, False
    iv = [m for m in tmem["members"] if m["name"] in ("InternalVisit", "InternalVisitChildren") and m.get("start")]
    out, v2 = [], False
    for m in iv:
        body = "\n".join(src[m["start"] - 1:m["end"]])
        if "AstVisitor2" in body:
            v2 = True
        ev = []  # (position, kind, a, b)
        for r in re.finditer(r"foreach\s*\(\s*(?:var|[\w<>,\.]+)\s+(\w+)\s+in\s+([\w\.]+)\s*\)", body):
            ev.append((r.start(), "loop", r.group(1), r.group(2) + "[]"))
        for r in re.finditer(r"(?:var|\w+)\s+(\w+)\s*=\s*([\w\.]+)\[\w+\];", body):
            ev.append((r.start(), "loop", r.group(1), r.group(2) + "[]"))
        for r in re.finditer(r"VisitAndShallContinue\((\w+)\)\s*(?:&&|;)", body):
            ev.append((r.start(), "direct", r.group(1), None))
        for r in re.finditer(r"([A-Za-z_][\w\.\[\]]*)\.InternalVisit\(", body):
            ev.append((r.start(), "visit", r.group(1), None))
        for r in re.finditer(r"StatementBlockAst\.InternalVisit\(visitor,\s*(\w+),\s*(\w+)", body):
            ev.append((r.start(), "direct", f"{r.group(1)}, {r.group(2)} (static helper)", None))
        ev.sort()
        lv = {}
        local_fn = "VisitAndShallContinue" in body
        for _, kind, x, y in ev:
            if kind == "loop":
                lv[x] = y
            elif kind == "direct":
                out.append(x)
            else:
                if x in ("visitor", "StatementBlockAst") or (local_fn and x == "ast"):
                    continue
                root = re.split(r"[\.\[]", x, maxsplit=1)
                if root[0] in lv:
                    x = lv[root[0]] + (x[len(root[0]):] if len(root) > 1 else "")
                out.append(x)
    return out, v2


def main():
    h, mem = nodes()
    vis = J("visitors.json")
    en = [e for e in J("enums.json") if e["file"] == ASTCS]
    if len(sys.argv) > 2 and sys.argv[1] == "--count":
        w = sys.argv[2]
        if w == "ast_classes":
            print(len(h))
        elif w == "abstract":
            print(sum(1 for x in h if "abstract" in x["modifiers"]))
        elif w in ("iv1", "iv2"):
            n = "System.Management.Automation.Language." + ("ICustomAstVisitor" if w == "iv1" else "ICustomAstVisitor2")
            print([v for v in vis if v["name"] == n][0]["visit_method_count"])
        return 0
    src = open(os.path.join(ROOT, ASTCS), encoding="utf-8-sig").read().split("\n")
    byname = {short(x["name"]): x for x in h}
    # visitor index: Visit<Node> -> visitor classes (non-default)
    vindex = {}
    for v in vis:
        s = short(v["name"])
        if s in DEFAULT_VISITORS:
            continue
        for m in v["visit_methods"]:
            vindex.setdefault(m, set()).add(s)
    L = []
    w = L.append
    nabs = sum(1 for x in h if "abstract" in x["modifiers"])
    w("""---
id: LANG-ASTCAT-001
title: AST node catalog
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/parser/ast.cs, src/System.Management.Automation/engine/parser/AstVisitor.cs, src/System.Management.Automation/engine/parser/PreOrderVisitor.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/parser/_folder.md]
generated_from: [data/ast-hierarchy.json, data/members-tierA.json, data/visitors.json, data/enums.json]
---

# AST node catalog

> STATIC-ONLY — behavior not run-verified. Every table is `GENERATED` by `docs-out/tools/gen_T23.py` (`APPROX`: regex extraction, see the column notes). Narrative: [02.3-ast.md](02.3-ast.md).
""")
    w("## 1. Purpose and scope [SPEC]\n")
    w(f"""Complete list of the AST classes declared in `ast.cs` (<!--N:AST_CLASSES_ASTCS-->{len(h)}<!--/N--> classes, <!--N:AST_CLASSES_ABSTRACT-->{nabs}<!--/N--> of them abstract), with base class, visit-order children, parser productions that create them, and the visitors that handle them; the two visitor interface method lists; the inheritance diagram; and the enums declared in `ast.cs`. Count source: `data/ast-hierarchy.json` filtered to `ast.cs` (the dataset has one more row from `VariableAnalysis.cs`, a private helper class, which is excluded).
""")
    w("## 2. Source map\n")
    w("| path | type | role |\n|---|---|---|")
    w(f"| `{ASTCS}::Ast@L91-L420` | abstract class | root of all nodes |")
    w("| `src/System.Management.Automation/engine/parser/AstVisitor.cs` | file | `ICustomAstVisitor(2)`, `DefaultCustomAstVisitor(2)`, `AstSearcher`, DEBUG checkers |")
    w("| `src/System.Management.Automation/engine/parser/PreOrderVisitor.cs` | file | `AstVisitAction`, `AstVisitor(2)`, `IAstPostVisitHandler` |\n")
    w("## 3. Node catalog\n")
    w("Column notes: **Base** = direct base class; **Children (visit order)** = receivers of `.InternalVisit(` in the node's `InternalVisit` method, in source order (`—` = leaf or no `InternalVisit`); **v2** = the method mentions `AstVisitor2`, i.e. visiting is gated or extended for second-generation visitors; **Created by** = parser methods containing `new <Node>(` (`—` = not created by `Parser.cs`: abstract, compiler-synthesized or created in other files); **Consumed by** = non-default visitor classes that define `Visit<Node>` (first six, then `+N`).\n")
    w("| Node | Kind | Base | Children (visit order, APPROX) | v2 | Created by (Parser.cs) | Consumed by (APPROX) | Source |")
    w("|---|---|---|---|---|---|---|---|")
    gaps = 0
    for x in sorted(h, key=lambda z: z["start"]):
        n = short(x["name"])
        base = x["base_chain"][0] if x["base_chain"] else "—"
        ch, v2 = children(src, mem.get(n))
        if ch is None or not ch:
            chs = "—"
            if "abstract" not in x["modifiers"]:
                gaps += 1
        else:
            chs = ", ".join(f"`{c}`" for c in ch)
        cb = sorted({m["method"] for m in x["created_by_parser"]})
        cbs = ", ".join(f"`{c}`" for c in cb) if cb else "—"
        vn = "Visit" + n[:-3] if n.endswith("Ast") else ""
        cons = sorted(vindex.get(vn, []))
        cs = ", ".join(f"`{c}`" for c in cons[:6]) + (f" +{len(cons)-6}" if len(cons) > 6 else "") if cons else "—"
        kind = "abstract" if "abstract" in x["modifiers"] else ("internal" if x["accessibility"] != "public" else "concrete")
        cond = f" `#if {'/'.join(x['cond'])}`" if x["cond"] else ""
        w(f"| `{n}` | {kind}{cond} | `{base}` | {chs} | {'yes' if v2 else ''} | {cbs} | {cs} | `{ASTCS}::{n}@L{x['start']}-L{x['end']}` |")
    w(f"\nRows: **{len(h)}** (`GENERATED`). Concrete nodes with no recognized child visit: {gaps} (leaves, or children visited through a different construct).\n")
    w("## 4. Inheritance diagram\n")
    w("```mermaid\nflowchart LR")
    for x in sorted(h, key=lambda z: z["start"]):
        n = short(x["name"])
        if x["base_chain"]:
            w(f"  {x['base_chain'][0]} --> {n}")
    w("```\n")
    w("## 5. Visitor interfaces\n")
    w("Method lists are the `Visit*` methods found in each type (`GENERATED`, `APPROX`). `ICustomAstVisitor` returns `object`; `AstVisitor` returns `AstVisitAction`.\n")
    for want in ("ICustomAstVisitor", "ICustomAstVisitor2", "AstVisitor", "AstVisitor2"):
        v = [q for q in vis if short(q["name"]) == want][0]
        w(f"**{want}** (`{v['file']}::{want}@L{v['start']}-L{v['end']}`, {v['visit_method_count']} visit methods): " + ", ".join(f"`{m}`" for m in v["visit_methods"]) + "\n")
    w("## 6. Visitor implementations in the repository\n")
    w("| Class | Bases | Visit methods defined | File |\n|---|---|---:|---|")
    for q in sorted(vis, key=lambda z: z["name"]):
        w(f"| `{short(q['name'])}` | {', '.join('`'+b+'`' for b in q['bases']) or '—'} | {q['visit_method_count']} | `{q['file']}` |")
    w("")
    w("## 7. Enums declared in ast.cs\n")
    for e in sorted(en, key=lambda z: z["start"]):
        mem_s = ", ".join(f"`{m['name']}`" + (f"={m['value']}" if m["value"] not in (None, "") else "") for m in e["members"])
        w(f"- `{short(e['full_name'])}` (`{ASTCS}::{short(e['full_name'])}@L{e['start']}-L{e['end']}`): {mem_s}")
    w("")
    w("""## 8. Non-AST public types in ast.cs

Type names (`ITypeName` family), `ScriptRequirements` and `CommentHelpInfo` live in `ast.cs` but are not `Ast` nodes (read in notes, `FACT-SRC`): see [02.3-ast.md](02.3-ast.md) §5.

Verification: node rows reconciled with `data/ast-hierarchy.json` (filtered by file); `InternalVisit` ranges come from `data/members-tierA.json`; edges in the diagram are the direct base of each row; visitor lists reconcile with `data/visitors.json`.
""")
    open(os.path.join(OUT, "02-language", "AST-CATALOG.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("AST-CATALOG: nodes", len(h), "abstract", nabs, "gaps", gaps)


if __name__ == "__main__":
    sys.exit(main())
