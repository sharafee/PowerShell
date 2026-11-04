#!/usr/bin/env python3
"""gen_coord.py - generated parts of the coordinator documents of 02-language (rule 9).

Purpose : (1) CALL-GRAPHS.md        - Mermaid call graphs for tokenize, parse, compile, invoke (name-based, APPROX);
          (2) INTERPRETER-DESIGN-SPACE.md - region <!--GEN:scores--> rendered from data/interpreter-scores.json:
              weighted totals, hard gates, two recommendations, sensitivity (never typed by hand);
          (3) REFERENCE-TEST-CORPUS.md   - region <!--GEN:tests--> from data/tests.json (Language tests by folder and file);
          (4) 09-synthesis/new-language-design-canvas.md - skeleton rows with lesson counts from data/lessons.json.
Inputs  : data/members-tierA.json, data/parser-methods.json, data/interpreter-scores.json, data/tests.json,
          data/lessons.json, the source files (read-only, for call extraction).
Outputs : docs-out/02-language/CALL-GRAPHS.md and regions; docs-out/09-synthesis/new-language-design-canvas.md
Run     : python3 docs-out/tools/gen_coord.py [--count callgraph_nodes|test_files|test_its|options]
Label   : APPROX (call edges are matches of a member name followed by '(' inside another member's line range).
Language: Python 3 (D-002)
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
S = "src/System.Management.Automation/engine/"


def J(n):
    return json.load(open(os.path.join(DATA, n)))


def fill(path, tag, rows):
    t = open(path, encoding="utf-8").read()
    pat = re.compile(r"(<!--GEN:%s-->)\n?.*?\n?(<!--/GEN:%s-->)" % (tag, tag), re.S)
    if not pat.search(t):
        print("region missing", tag, path)
        return
    open(path, "w", encoding="utf-8").write(pat.sub(lambda m: m.group(1) + "\n" + "\n".join(rows) + "\n" + m.group(2), t))


# ------------------------------------------------------------------ call graphs
_src = {}
_members = None


def members():
    global _members
    if _members is None:
        _members = {(m["file"], m["full_name"]): m["members"] for m in J("members-tierA.json")}
    return _members


def body(file, start, end):
    if file not in _src:
        _src[file] = open(os.path.join(ROOT, file), encoding="utf-8-sig").read().split("\n")
    return "\n".join(_src[file][start - 1:end])


def graph(file, type_suffix, root, depth, limit, include=None):
    """BFS over members of one type: edges m -> n when n( appears in m's body (n a member method name)."""
    key = [k for k in members() if k[0] == file and k[1].endswith(type_suffix)][0]
    ms = [m for m in members()[key] if m.get("kind") == "method" and m.get("start")]
    names = defaultdict(list)
    for m in ms:
        names[m["name"]].append(m)
    edges, seen, frontier = [], {root}, [root]
    for _ in range(depth):
        nxt = []
        for n in frontier:
            if n not in names:
                continue
            b = "\n".join(body(file, m["start"], m["end"]) for m in names[n])
            for c in names:
                if c == n or (include and not include(c)):
                    continue
                if re.search(r"(?<![\w.])%s\s*[<(]" % re.escape(c), b) or re.search(r"\.%s\s*[<(]" % re.escape(c), b):
                    edges.append((n, c))
                    if c not in seen and len(seen) < limit:
                        seen.add(c)
                        nxt.append(c)
        frontier = nxt
    edges = [e for e in edges if e[0] in seen and e[1] in seen]
    return sorted(set(edges)), seen


def mermaid(edges):
    out = ["```mermaid", "flowchart LR"]
    for a, b in edges:
        out.append(f"  {a} --> {b}")
    out.append("```")
    return out


def callgraphs():
    P = S + "parser/Parser.cs"
    T = S + "parser/tokenizer.cs"
    C = S + "parser/Compiler.cs"
    R = S + "runtime/CompiledScriptBlock.cs"
    gs = {}
    gs["tokenize"] = graph(T, ".Tokenizer", "NextToken", 3, 40)
    gs["parse"] = graph(P, ".Parser", "ParseTask", 3, 45, include=lambda c: c.endswith("Rule") or c in ("ParseTask", "ScriptBlockRule", "SetTokenizerMode", "SyncOnError"))
    gs["rules"] = graph(P, ".Parser", "ScriptBlockRule", 12, 200, include=lambda c: c.endswith("Rule"))
    gs["compile"] = graph(C, ".Compiler", "Compile", 3, 45, include=lambda c: not c.startswith("Visit") and not c.startswith("New") and c not in ("Compile",) or c == "Compile")
    gs["compile_body"] = graph(C, ".Compiler", "VisitScriptBlock", 4, 40, include=lambda c: not c.startswith("Visit") and c not in ("Compile", "NewTemp", "Constant", "GetLocal"))
    gs["invoke"] = graph(R, ".ScriptBlock", "InvokeWithPipeImpl", 2, 30)
    return gs


def write_callgraphs(gs):
    L = []
    w = L.append
    w("""---
id: LANG-CALLG-001
title: Call graphs
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/parser/Parser.cs, src/System.Management.Automation/engine/parser/tokenizer.cs, src/System.Management.Automation/engine/parser/Compiler.cs, src/System.Management.Automation/engine/runtime/CompiledScriptBlock.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/parser/_folder.md]
generated_from: [data/members-tierA.json]
---

# Call graphs

> STATIC-ONLY — behavior not run-verified. Every graph is `GENERATED` by `docs-out/tools/gen_coord.py` from `data/members-tierA.json` and the member line ranges (`APPROX`: an edge A → B means the name `B` followed by `(` or `<` appears in the body of `A`, so overloads and same-named members of other types can create false edges, and calls through delegates or interfaces are missing). Use them as maps, then read the method. Sequence-level narrative: [LIFECYCLE-script-execution.md](LIFECYCLE-script-execution.md); stage data contracts: [STAGE-CONTRACTS.md](STAGE-CONTRACTS.md).
""")
    w("## 1. Purpose and scope [SPEC]\n")
    w("Entry-point call graphs for **tokenize**, **parse**, **check**, **compile** and **invoke**. 'Check' is not generated (the semantic passes are visitors, entered through `PerformPostParseChecks`) and is given as a hand-written chain in §5.\n")
    w("## 2. Source map\n")
    w("| graph | entry | file |\n|---|---|---|")
    w(f"| tokenize | `Tokenizer.NextToken` | `{S}parser/tokenizer.cs` |")
    w(f"| parse | `Parser.ParseTask` → `ScriptBlockRule` | `{S}parser/Parser.cs` |")
    w(f"| compile | `Compiler.Compile` | `{S}parser/Compiler.cs` |")
    w(f"| invoke | `ScriptBlock.InvokeWithPipeImpl` | `{S}runtime/CompiledScriptBlock.cs` |\n")
    def sect(title, key, note):
        e, n = gs[key]
        w(f"## {title}\n")
        w(f"{note} Nodes: {len(n)}, edges: {len(e)}.\n")
        L.extend(mermaid(e))
        w("")

    sect("3. Tokenize", "tokenize", "`NextToken` and its scanners, depth 3 (`Tokenizer`, name-based).")
    sect("4. Parse: entry chain", "parse", "From `ParseTask` through the first rules, depth 3.")
    w("## 5. Check (hand-written chain)\n")
    w("""`Parser.ParseTask` → `ScriptBlockAst.PerformPostParseChecks` → `SymbolResolver.ResolveSymbols` (visitor over the AST) → `SemanticChecks.CheckAst` (visitor; for class methods `VariableAnalysis.AnalyzeMemberFunction`; for `data` statements `RestrictedLanguageChecker`). Compile-time: `Compiler.Compile` → `VariableAnalysis.Analyze` and, for the root block, `Compiler.GenerateTypesAndUsings` → `TypeDefiner.DefineTypes`. Evidence: [02.4-semantic-analysis.md](02.4-semantic-analysis.md) §6.
""")
    sect("6. Compile", "compile", "From `Compiler.Compile` through helpers (the 63 `Visit*` methods are omitted from the graph; see [COMPILATION-MAP.md](COMPILATION-MAP.md)), depth 3.")
    sect("6b. Compile: script block body", "compile_body", "From `Compiler.VisitScriptBlock` (called through `body.Accept(this)` inside `Compile`) through the lambda builders, depth 4.")
    sect("7. Invoke", "invoke", "From `ScriptBlock.InvokeWithPipeImpl`, depth 2.")
    e, n = gs["rules"]
    w("## 8. Parser rule-to-rule edges (complete list, `*Rule` methods reachable from `ScriptBlockRule`)\n")
    w(f"<!--N:PARSER_RULE_NODES-->{len(n)}<!--/N--> rules, {len(e)} edges (`GENERATED`, `APPROX`). Each row lists the callee rules of one rule.\n")
    w("| Rule | Calls (rules) |\n|---|---|")
    adj = defaultdict(list)
    for a, b in e:
        adj[a].append(b)
    for a in sorted(adj):
        w(f"| `{a}` | " + ", ".join(f"`{b}`" for b in sorted(adj[a])) + " |")
    w("\n## 9. Guidance for MicroteamShell [LESSON]\n")
    w("""- **LSN-CALLG-01** [REPLICATE] (area: NLD-TOOL) Keep the five entry points (tokenize, parse, check, compile, invoke) as separate callable stages with narrow signatures so each can be tested alone. Evidence: `src/System.Management.Automation/engine/parser/Parser.cs::Parser.ParseTask@L176-L227`.
- **LSN-CALLG-02** [ADAPT] (area: NLD-TOOL) Generate such graphs in CI from the shell's own sources to catch accidental coupling between stages. Why: the PowerShell graphs show the compiler calling parser-time helpers and the AST calling the compiler. Evidence: `src/System.Management.Automation/engine/parser/ast.cs::VariableExpressionAst@L9404-L9624`.
""")
    w("Verification: graphs are produced by the script from member ranges; `ParseTask`, `ScriptBlockRule`, `NextToken`, `Compiler.Compile` and `InvokeWithPipeImpl` exist in `data/members-tierA.json`; spot-checked edges: `ParseTask → ScriptBlockRule`, `NextToken → ScanVariable`, `Compile → CompileTree`.\n")
    open(os.path.join(OUT, "02-language", "CALL-GRAPHS.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return len(n)


# ------------------------------------------------------------------ scores
CRIT = ["fidelity", "sandbox", "startup", "throughput", "debug", "aot", "determinism", "memory", "observability", "complexity"]
CRIT_NAMES = {"fidelity": "Behavioral fidelity", "sandbox": "Sandboxability", "startup": "Startup latency", "throughput": "Steady-state throughput", "debug": "Debuggability",
              "aot": "AOT-friendliness", "determinism": "Determinism", "memory": "Memory footprint", "observability": "Observability", "complexity": "Implementation simplicity"}


def total(opt, weights):
    return sum(opt["scores"][c] * weights[c] for c in CRIT) / 100.0


def scores_rows():
    d = J("interpreter-scores.json")
    wts = d["weights"]
    assert sum(wts.values()) == 100 and set(wts) == set(CRIT)
    opts = d["options"]
    rows = []
    rows += ["| Option | Name | " + " | ".join(CRIT_NAMES[c] + f" ({wts[c]})" for c in CRIT) + " | Weighted total (max 5) |", "|---|---|" + "---:|" * (len(CRIT) + 1)]
    for o in opts:
        rows.append(f"| {o['id']} | {o['name']} | " + " | ".join(str(o["scores"][c]) for c in CRIT) + f" | **{total(o, wts):.2f}** |")
    rows += ["", "Justifications (one sentence per score, label in brackets):", ""]
    for o in opts:
        rows.append(f"**{o['id']} {o['name']}**")
        for c in CRIT:
            j = o["why"][c]
            rows.append(f"- {CRIT_NAMES[c]} = {o['scores'][c]} [{j[0]}] {j[1]}")
        rows.append("")
    rows += ["Hard gates (H1 reproduces `CORE` observable behavior; H2 feasible under the deployment constraint; H3 policy hooks possible at every boundary of [STAGE-CONTRACTS.md](STAGE-CONTRACTS.md)):", "",
             "| Option | H1 | H2 JIT-allowed | H2 NativeAOT-required | H3 | Gate note |", "|---|---|---|---|---|---|"]
    for o in opts:
        g = o["gates"]
        rows.append(f"| {o['id']} | {'pass' if g['H1'] else 'FAIL'} | {'pass' if g['H2_jit'] else 'FAIL'} | {'pass' if g['H2_aot'] else 'FAIL'} | {'pass' if g['H3'] else 'FAIL'} | {g['note']} |")
    recs = {}
    for mode, key in (("JIT-allowed", "H2_jit"), ("NativeAOT-required", "H2_aot")):
        ok = [o for o in opts if o["gates"]["H1"] and o["gates"][key] and o["gates"]["H3"]]
        ok.sort(key=lambda o: (-round(total(o, wts), 6), -o["scores"]["complexity"]))
        recs[mode] = ok
    rows += ["", "Recommendations (computed; label `INFERENCE`):", ""]
    for mode, ok in recs.items():
        rows.append(f"- **{mode}**: {ok[0]['id']} {ok[0]['name']} ({total(ok[0], wts):.2f}); runner-up {ok[1]['id']} {ok[1]['name']} ({total(ok[1], wts):.2f}); candidates passing all gates: {', '.join(o['id'] for o in ok)}.")
    # sensitivity: raise one weight (others scaled), find smallest weight where winner changes
    rows += ["", "Sensitivity (weight of one criterion raised, other weights scaled to keep the sum at 100; smallest weight at which the JIT-allowed winner changes):", ""]
    base = recs["JIT-allowed"][0]["id"]
    cand = recs["JIT-allowed"]
    for c in CRIT:
        flip = None
        for w in range(wts[c], 71):
            sc = {k: (wts[k] * (100 - w) / (100 - wts[c]) if k != c else w) for k in CRIT}
            best = max(cand, key=lambda o: (round(sum(o["scores"][k] * sc[k] for k in CRIT) / 100, 6), o["scores"]["complexity"]))
            if best["id"] != base:
                flip = (w, best["id"])
                break
        rows.append(f"- {CRIT_NAMES[c]} (weight {wts[c]}): " + (f"winner becomes {flip[1]} at weight {flip[0]}" if flip else "no change up to weight 70"))
    return rows, recs, opts


def tests_rows():
    t = J("tests.json")
    lang = [x for x in t["pester"] if x["path"].startswith("test/powershell/Language/")]
    folder = defaultdict(lambda: [0, 0, 0, 0])
    for x in lang:
        f = "/".join(x["path"].split("/")[:4])
        a = folder[f]
        a[0] += 1
        a[1] += x["describe"]
        a[2] += x["context"]
        a[3] += x["it"]
    rows = ["| Folder | Files | Describe | Context | It |", "|---|---:|---:|---:|---:|"]
    for f, a in sorted(folder.items()):
        rows.append(f"| `{f}` | {a[0]} | {a[1]} | {a[2]} | {a[3]} |")
    tot = [sum(a[i] for a in folder.values()) for i in range(4)]
    rows.append(f"| **total Language** | **{tot[0]}** | **{tot[1]}** | **{tot[2]}** | **{tot[3]}** |")
    rows += ["", "Files (path, Describe/Context/It counts, first Describe names; `APPROX` regex extraction):", "", "| File | D | C | It | First Describe names |", "|---|---:|---:|---:|---|"]
    for x in sorted(lang, key=lambda z: z["path"]):
        names = [n["name"] for n in x.get("tree", []) if n["kind"] == "Describe"][:2]
        rows.append(f"| `{x['path']}` | {x['describe']} | {x['context']} | {x['it']} | " + "; ".join(n.replace("|", "\\|")[:60] for n in names) + " |")
    other = [x for x in t["pester"] if x["path"].startswith("test/powershell/engine/") and any(k in x["path"] for k in ("Api/", "Basic/", "ExecutionContext", "Runspace", "Pipeline", "ScriptBlock", "Variable", "Type", "Debugger"))]
    rows += ["", "Engine tests that also specify language behavior (selected by path keywords, `APPROX`):", "", "| File | It |", "|---|---:|"]
    for x in sorted(other, key=lambda z: z["path"])[:40]:
        rows.append(f"| `{x['path']}` | {x['it']} |")
    xs = [x for x in t["xunit"] if any(k in x["path"] for k in ("Ast", "Binder", "Parser", "Language", "Tokenizer"))]
    rows += ["", "xUnit tests on the language layer:", "", "| File | Facts | Theories | Classes |", "|---|---:|---:|---|"]
    for x in xs:
        rows.append(f"| `{x['path']}` | {x['facts']} | {x['theories']} | {', '.join(x['classes'])} |")
    return rows, len(lang), tot[3]


def canvas():
    lessons = J("lessons.json")
    cnt = defaultdict(Counter)
    for l in lessons:
        cnt[l["area"].replace("NLD-", "")][l["verdict"]] += 1
    areas = ["LEX", "GRM", "OP", "TYP", "SCP", "ERR", "PIP", "MOD", "CMD", "SEC", "TOOL", "RUN"]
    names = {"LEX": "Lexical structure and tokenizer modes", "GRM": "Grammar, AST and semantic checks", "OP": "Operators and precedence", "TYP": "Types, conversions and values",
             "SCP": "Scopes, variables and sessions", "ERR": "Errors, streams and recovery", "PIP": "Pipeline and output", "MOD": "Modules and packaging", "CMD": "Commands and parameter binding",
             "SEC": "Security, sandboxing and language modes", "TOOL": "Tooling, extension and testing", "RUN": "Execution strategy and runtime"}
    L = ["""---
id: SYN-CANVAS-001
title: New-language design canvas (skeleton)
kind: catalog
tier: B
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: []
mirror_cards: []
generated_from: [data/lessons.json]
---

# New-language design canvas (skeleton)

> STATIC-ONLY. Skeleton created in Phase 2 so that forward links resolve; Phase 7 fills the empty cells. Lesson counts per area and verdict are `GENERATED` by `docs-out/tools/gen_coord.py` from `data/lessons.json` (gate 6d compares them with the verdict counts of [SEMANTIC-QUIRKS](../02-language/SEMANTIC-QUIRKS.md) and the guidance sections).

## 1. Canvas rows

| Row | Area | REPLICATE | ADAPT | REDESIGN | AVOID | Baseline decision | Approved deviation | Status |
|---|---|---:|---:|---:|---:|---|---|---|"""]
    for a in areas:
        c = cnt[a]
        L.append(f"| NLD-{a} | {names[a]} | {c['REPLICATE']} | {c['ADAPT']} | {c['REDESIGN']} | {c['AVOID']} | | | open |")
    tot = Counter()
    for a in areas:
        tot.update(cnt[a])
    L.append(f"| **total** | | **{tot['REPLICATE']}** | **{tot['ADAPT']}** | **{tot['REDESIGN']}** | **{tot['AVOID']}** | | | |")
    L.append("\nVerification: counts rendered from `data/lessons.json` (extracted from the guidance sections by `tools/coordinator.py lessons`); the other columns are intentionally empty until Phase 7.\n")
    open(os.path.join(OUT, "09-synthesis", "new-language-design-canvas.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return dict(tot)


def quirk_counts():
    p = os.path.join(OUT, "02-language", "SEMANTIC-QUIRKS.md")
    c = Counter()
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8"):
            m = re.match(r"\| QRK-\d+ \|.*\| (REPLICATE|ADAPT|REDESIGN|AVOID) \| ([^|]*)\|", ln)
            if m:
                c[m.group(1)] += 1
                c["total"] += 1
    return c


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--count":
        k = sys.argv[2]
        if k.startswith("quirks_"):
            q = quirk_counts()
            print(q["total"] if k == "quirks_total" else q[k.split("_")[1].upper()])
            return 0
        if k == "callgraph_nodes":
            print(len(callgraphs()["rules"][1]))
        elif k in ("test_files", "test_its"):
            _, nf, ni = tests_rows()
            print(nf if k == "test_files" else ni)
        elif k == "options":
            print(len(J("interpreter-scores.json")["options"]))
        return 0
    gs = callgraphs()
    write_callgraphs(gs)
    sp = os.path.join(OUT, "02-language", "INTERPRETER-DESIGN-SPACE.md")
    if os.path.exists(sp):
        rows, recs, opts = scores_rows()
        fill(sp, "scores", rows)
    tp = os.path.join(OUT, "02-language", "REFERENCE-TEST-CORPUS.md")
    if os.path.exists(tp):
        rows, nf, ni = tests_rows()
        fill(tp, "tests", rows)
    tot = canvas()
    print("call graph rule nodes", len(gs["rules"][1]), "canvas lessons", tot)


if __name__ == "__main__":
    sys.exit(main())
