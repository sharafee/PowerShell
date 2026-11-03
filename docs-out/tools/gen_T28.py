#!/usr/bin/env python3
"""gen_T28.py - generated documents of task T28 (rule 9).

Purpose : (1) 02-language/OPERATOR-TABLE.md - every operator token kind (binary, unary, assignment, special)
              with text, precedence level, flags and implementation route (hand annotations);
          (2) region <!--GEN:ranks--> of 02-language/CONVERSION-RULES.md - ConversionRank table from data/enums.json.
Inputs  : data/enums.json, data/tables.json (via gen_T21 parsers), tools/annotations/T28-operators.json
Outputs : docs-out/02-language/OPERATOR-TABLE.md, region in CONVERSION-RULES.md
Run     : python3 docs-out/tools/gen_T28.py [--count operators|ranks]
Label   : APPROX (token tables parsed from verbatim source text; precedence from TokenFlags).
Language: Python 3 (D-002)
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
sys.path.insert(0, os.path.join(OUT, "tools"))
import gen_T21 as g  # noqa: E402

TKN = g.TKN
LP = "src/System.Management.Automation/engine/LanguagePrimitives.cs"


def J(n):
    return json.load(open(os.path.join(DATA, n)))


def operators():
    tb = J("tables.json")
    en = {e["full_name"].split(".")[-1]: e for e in J("enums.json") if e["file"] == TKN}
    kinds = en["TokenKind"]["members"]
    sfl = [re.sub(r"\s+", " ", x) for x in g.split_top(g.strip_comments(tb[f"{TKN}::s_staticTokenFlags"]["text"]))]
    txt = [g.unq(x) for x in g.split_top(g.strip_comments(tb[f"{TKN}::s_tokenText"]["text"]))]
    flags = {m["name"]: int(m["value"], 16) for m in en["TokenFlags"]["members"] if m["name"].startswith("BinaryPrecedence") and m["name"] != "BinaryPrecedenceMask"}
    rows = []
    for m in kinds:
        v = int(m["value"])
        f = sfl[v]
        cls = [c for c in ("BinaryOperator", "UnaryOperator", "AssignmentOperator", "SpecialOperator", "PrefixOrPostfixOperator") if c in f]
        if not cls and m["name"] not in ("Comma", "Redirection", "RedirectInStd", "Pipe", "Ampersand"):
            continue
        lvl = [k for k in flags if "TokenFlags." + k in f]
        rows.append({"name": m["name"], "text": txt[v], "classes": cls, "level": flags[lvl[0]] if lvl else None,
                     "levelname": lvl[0].replace("BinaryPrecedence", "") if lvl else "", "fold": "CanConstantFold" in f,
                     "restricted": "DisallowedInRestrictedMode" in f, "line": m["line"]})
    return rows


def main():
    ann = json.load(open(os.path.join(OUT, "tools", "annotations", "T28-operators.json")))
    rows = operators()
    en = {e["full_name"].split(".")[-1]: e for e in J("enums.json") if e["file"] == LP}
    ranks = en["ConversionRank"]["members"]
    if len(sys.argv) > 2 and sys.argv[1] == "--count":
        print(len(rows) if sys.argv[2] == "operators" else len(ranks))
        return 0
    unmapped = [r["name"] for r in rows if r["name"] not in ann["kinds"]]
    L = []
    w = L.append
    w("""---
id: LANG-OPTABLE-001
title: Operator table
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: [CF-OP-001]
sources: [src/System.Management.Automation/engine/parser/token.cs, src/System.Management.Automation/engine/parser/Parser.cs, src/System.Management.Automation/engine/runtime/Binding/Binders.cs, src/System.Management.Automation/engine/lang/parserutils.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/parser/_folder.md]
generated_from: [data/enums.json, data/tables.json]
---

# Operator table

> STATIC-ONLY — behavior not run-verified. Rows are `GENERATED` by `docs-out/tools/gen_T28.py` from the token tables (`APPROX`) joined with hand annotations (`docs-out/tools/annotations/T28-operators.json`, `FACT-SRC`). Narrative: [02.6-types-and-operators.md](02.6-types-and-operators.md); conversions used by operators: [CONVERSION-RULES.md](CONVERSION-RULES.md); parsing: [02.2-parser.md](02.2-parser.md) §7.2.
""")
    w("## 1. Purpose and scope [SPEC]\n")
    w("One table for every operator token kind: spelling, role, precedence level, associativity, whether the compiler may fold it at compile time, and how it is evaluated. The precedence rule is canonical fact CF-OP-001 (stated in §3).\n")
    w("## 2. Source map\n")
    w("| path | role |\n|---|---|")
    w("| `src/System.Management.Automation/engine/parser/token.cs::TokenFlags@L601-L752` | precedence and operator-class flags |")
    w("| `src/System.Management.Automation/engine/parser/Parser.cs::Parser.BinaryExpressionRule@L6798-L6950` | precedence climbing |")
    w("| `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder@L2119-L3422` | binary operation semantics |")
    w("| `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSUnaryOperationBinder@L3427-L3738` | unary operation semantics |")
    w("| `src/System.Management.Automation/engine/lang/parserutils.cs::ParserOps@L232-L1760` | `-like`, `-match`, `-replace`, `-split`, `-join`, range helpers |\n")
    w("## 3. Precedence and associativity (CF-OP-001)\n")
    w("<!--CF:CF-OP-001-->**Operator precedence and associativity.** Binary operators are parsed by precedence climbing and **all are left-associative**; from lowest to highest precedence the levels are: logical (`-and`, `-or`, `-xor`) = 1; bitwise (`-band`, `-bor`, `-bxor`) = 2; comparison group (all `-eq`/`-ne`/`-gt`/`-ge`/`-lt`/`-le`, `-like`, `-match`, `-replace`, `-contains`, `-in` families with their `i`/`c` variants, `-is`, `-isnot`, `-as`, `-split`, `-join`, `-shl`, `-shr`) = 5; null-coalescing `??` = 7; additive (`+`, `-`) = 9; multiplicative (`*`, `/`, `%`) = 10; format `-f` = 12; range `..` = 13. The comma (array-literal) operator binds tighter than every binary operator; the unary operators, casts and `++`/`--` bind tighter than the comma; the ternary `?:` (right-nested) and assignment (`=`, `+=`, `-=`, `*=`, `/=`, `%=`, `??=`, parsed at statement level with a statement on the right) bind looser than all binary operators; `&&` and `||` chain pipelines and are not expression operators. Operators spelled with a leading dash are recognized as operators only when the tokenizer is in expression mode.<!--/CF-->\n")
    w("Evidence: `src/System.Management.Automation/engine/parser/Parser.cs::Parser.BinaryExpressionRule@L6798-L6950` (reduce while new precedence is less than or equal), `src/System.Management.Automation/engine/parser/token.cs::TokenFlags@L601-L752` (level values), `Parser.ArrayLiteralRule@L6975-L7021`, `Parser.UnaryExpressionRule@L7029-L7226`, `Parser.ExpressionRule@L6696-L6790`, `Parser.PipelineChainRule@L5773-L5988`.\n")
    w("## 4. Operator table\n")
    w("Level = `BinaryPrecedence*` value (higher binds tighter); `fold` = the operator may be constant-folded; `restricted` = flagged `DisallowedInRestrictedMode`. Case: `i`-prefixed and plain forms ignore case, `c`-prefixed forms are case-sensitive (token texts of `i` forms are listed without the `i` for most operators, see [TOKEN-CATALOG.md](TOKEN-CATALOG.md) §3).\n")
    w("| TokenKind | Text | Class | Level | Associativity | fold | restricted | Evaluation | Behavior (FACT-SRC) |")
    w("|---|---|---|---:|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: (x["level"] if x["level"] is not None else 99, x["name"])):
        grp = ann["kinds"].get(r["name"])
        ev, beh = ann["groups"][grp] if grp else ("—", "—")
        cls = "/".join(c.replace("Operator", "") for c in r["classes"]) or "other"
        assoc = "left" if "BinaryOperator" in r["classes"] else ("right (nested)" if r["name"] == "QuestionMark" else "—")
        w(f"| `{r['name']}` | `{r['text']}` | {cls} | {r['level'] if r['level'] is not None else '—'} | {assoc} | {'yes' if r['fold'] else ''} | {'yes' if r['restricted'] else ''} | {ev} | {beh} |")
    w(f"\nRows: **<!--N:OPERATOR_KINDS-->{len(rows)}<!--/N-->** (`GENERATED`). Kinds without annotation: {', '.join(unmapped) or 'none'}.\n")
    w("## 5. Notes\n")
    w("""- **Left-operand driven.** For binary operators the left operand's runtime type selects the rule; the right operand is converted to it where needed. `1 + "2"` is 3, `"1" + 2` is `"12"` (string concatenation).
- **`-eq`/`-ne` with arrays.** A collection on the left filters (returns matching elements); a `$null` on the left of `-eq` returns `$true` only for `$null`.
- **Constant folding** only for operators with the `CanConstantFold` flag; operators depending on execution context (`-split`, `-join`, `-like`) or culture (`-f`) are not folded (comment on `TokenFlags.CanConstantFold`).
- **`-and`/`-or`** short-circuit; **`-xor`** does not. **`-band`/`-bor`/`-bxor`/`-shl`/`-shr`** operate on integers of the wider operand type.
""")
    w("## 6. Guidance for MicroteamShell [LESSON]\n")
    w("""- **LSN-OP-01** [REPLICATE] (area: NLD-OP) Use the precedence levels and left associativity above; keep the comma tighter than binary operators and put ternary and assignment below. Evidence: `src/System.Management.Automation/engine/parser/Parser.cs::Parser.BinaryExpressionRule@L6798-L6950`.
- **LSN-OP-02** [REPLICATE] (area: NLD-OP) Choose the operation by the left operand's type and convert the right operand to it (CONVERSION-RULES); keep the `i`/`c` case variants and the array-filtering behavior of comparison operators. Evidence: `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder@L2119-L3422`.
- **LSN-OP-03** [ADAPT] (area: NLD-OP) Implement operators as ordinary functions with an explicit dispatch table instead of dynamic binding sites. Why: same observable results; no DLR. Evidence: `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder.FallbackBinaryOperation@L2179-L2240`.
""")
    w("Verification: operator rows generated from `s_staticTokenFlags`/`s_tokenText`; precedence levels cross-checked with the parser's reduce loop (`<=`) and with the generated table in [02.2-parser.md](02.2-parser.md) §7.2; evaluation text read from `PSBinaryOperationBinder` (`BinaryAdd`, `BinaryMultiply`, `BinarySubDivOrRem`, `CompareEQ`, `BinaryEqualityComparison`, `BinaryNumericOp`), `NumericOps.cs` (`IntOps`), `Compiler.VisitBinaryExpression` and `ParserOps` notes. `-shl`/`-shr`, bitwise and `-ge/-gt` internals and `PSUnaryOperationBinder` were read only at the dispatch level (`UNVERIFIED` below that).\n")
    open(os.path.join(OUT, "02-language", "OPERATOR-TABLE.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    # ranks region
    p = os.path.join(OUT, "02-language", "CONVERSION-RULES.md")
    if os.path.exists(p):
        out = ["| Rank name | Value | Source line |", "|---|---|---:|"]
        for m in ranks:
            out.append(f"| `{m['name']}` | `{m['value']}` | L{m['line']} |")
        t = open(p, encoding="utf-8").read()
        pat = re.compile(r"(<!--GEN:ranks-->)\n?.*?\n?(<!--/GEN:ranks-->)", re.S)
        if pat.search(t):
            open(p, "w", encoding="utf-8").write(pat.sub(lambda m: m.group(1) + "\n" + "\n".join(out) + "\n" + m.group(2), t))
    print("OPERATOR-TABLE rows", len(rows), "unmapped", unmapped, "ranks", len(ranks))


if __name__ == "__main__":
    sys.exit(main())
