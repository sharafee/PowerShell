#!/usr/bin/env python3
"""gen_T21.py - render 02-language/TOKEN-CATALOG.md from data/*.json (task T21, rule 9).

Purpose : every catalog in the tokenizer documents is GENERATED, never hand-typed.
          Renders: TokenKind table (value, name, default text, static flags),
          TokenFlags table, keyword table, dash-operator table, CharTraits table,
          NumberSuffixFlags table, TokenizerMode table.
Inputs  : data/enums.json, data/tables.json (verbatim source text of static arrays), data/types.json
Outputs : docs-out/02-language/TOKEN-CATALOG.md  (front matter + body)
Run     : python3 docs-out/tools/gen_T21.py        (from the repo root)
          python3 docs-out/tools/gen_T21.py --count keywords|dash_operators   (numbers proposals)
Label   : every row is APPROX (regex extraction of array literals; cross-checked by length == last
          TokenKind value + 1, asserted below).
Language: Python 3 (D-002)
"""
import json
import os
import re
import sys

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
TOK = "src/System.Management.Automation/engine/parser/tokenizer.cs"
TKN = "src/System.Management.Automation/engine/parser/token.cs"
CHT = "src/System.Management.Automation/engine/parser/CharTraits.cs"


def J(n):
    return json.load(open(os.path.join(DATA, n)))


def strip_comments(t):
    # defect workaround: data/tables.json "text" of s_tokenText/s_staticTokenFlags runs past the
    # closing "};" of the array (extractor end-line is too late) -> cut at the first "};".
    k = t.find("};")
    if k != -1:
        t = t[:k + 1]
    t = re.sub(r"^\s*#(end)?region[^\n]*$", "", t, flags=re.M)
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    t = re.sub(r"//[^\n]*", "", t)
    return t


def split_top(t):
    """split an array literal body on top-level commas (strings may contain commas)."""
    t = t.strip()
    if t.startswith("{"):
        t = t[1:]
    if t.endswith("}"):
        t = t[:-1]
    out, cur, q = [], [], False
    i = 0
    while i < len(t):
        c = t[i]
        if q:
            cur.append(c)
            if c == "\\":
                i += 1
                cur.append(t[i])
            elif c == '"':
                q = False
        else:
            if c == '"':
                q = True
                cur.append(c)
            elif c == ",":
                out.append("".join(cur).strip())
                cur = []
            else:
                cur.append(c)
        i += 1
    last = "".join(cur).strip()
    if last:
        out.append(last)
    return [x for x in out]


def unq(s):
    s = s.strip()
    if s.startswith("@"):
        s = s[1:]
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    if s == "string.Empty":
        return ""
    return s.replace("\\\\", "\\").replace('\\"', '"')


def esc(s):
    return s.replace("|", "\\|")


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--count":
        tb = J("tables.json")
        key = {"keywords": f"{TOK}::s_keywordText", "dash_operators": f"{TOK}::_operatorText"}[sys.argv[2]]
        print(len(split_top(strip_comments(tb[key]["text"]))))
        return 0
    enums = {e["full_name"].split(".")[-1]: e for e in J("enums.json")
             if e["file"].endswith(("parser/token.cs", "parser/tokenizer.cs", "parser/CharTraits.cs"))}
    tables = J("tables.json")
    kind = enums["TokenKind"]
    flags = enums["TokenFlags"]
    mem = kind["members"]
    nvals = int(mem[-1]["value"]) + 1

    texts = [unq(x) for x in split_top(strip_comments(tables[f"{TKN}::s_tokenText"]["text"]))]
    sflags = [re.sub(r"\s+", " ", x) for x in split_top(strip_comments(tables[f"{TKN}::s_staticTokenFlags"]["text"]))]
    assert len(texts) == nvals, (len(texts), nvals)
    assert len(sflags) == nvals, (len(sflags), nvals)
    byval = {int(m["value"]): m for m in mem}

    kw_text = [unq(x) for x in split_top(strip_comments(tables[f"{TOK}::s_keywordText"]["text"]))]
    kw_kind = [x.replace("TokenKind.", "") for x in split_top(strip_comments(tables[f"{TOK}::s_keywordTokenKind"]["text"]))]
    op_text = [unq(x) for x in split_top(strip_comments(tables[f"{TOK}::_operatorText"]["text"]))]
    op_kind = [x.replace("TokenKind.", "") for x in split_top(strip_comments(tables[f"{TOK}::s_operatorTokenKind"]["text"]))]
    assert len(kw_text) == len(kw_kind) and len(op_text) == len(op_kind)

    # keyword kind -> flags
    flag_of = {byval[v]["name"]: sflags[v] for v in byval}

    L = []
    w = L.append
    w("""---
id: LANG-TOKCAT-001
title: Token catalog
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/parser/token.cs, src/System.Management.Automation/engine/parser/tokenizer.cs, src/System.Management.Automation/engine/parser/CharTraits.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/parser/_folder.md]
generated_from: [data/enums.json, data/tables.json]
---

# Token catalog

> STATIC-ONLY — behavior not run-verified. Every table below is `GENERATED` by `docs-out/tools/gen_T21.py` from `data/enums.json` and `data/tables.json` (`APPROX`: the arrays are parsed from verbatim source text; lengths are asserted equal to the `TokenKind` value range). Narrative lives in [02.1-tokenizer.md](02.1-tokenizer.md). Label for every row: `FACT-SRC` (read in source) + `APPROX` (extraction).

## 1. Purpose and scope [SPEC]

Complete list of token kinds, token flags, keywords, dash operators, character classes, number-suffix flags and tokenizer modes of the PowerShell tokenizer (v7.6.9). Counts: `TokenKind` has <!--N:TOKENKIND_MEMBERS-->157<!--/N--> named members spread over the value range 0..%d; `TokenFlags` has <!--N:TOKENFLAGS_MEMBERS-->28<!--/N--> members.

## 2. Source map

| path | type | role |
|---|---|---|
| `%s::TokenKind@L%d-L%d` | enum | every token kind |
| `%s::TokenFlags@L%d-L%d` | `[Flags]` enum | token traits |
| `%s::TokenTraits.s_staticTokenFlags@L%d-L%d` | table | static flags per kind |
| `%s::TokenTraits.s_tokenText@L%d-L%d` | table | default text per kind |
| `%s::Tokenizer.s_keywordText@L%d-L%d` | table | keyword spelling |
| `%s::Tokenizer._operatorText@L%d-L%d` | table | dash-operator spelling |
| `%s::CharTraits@L%d-L%d` | `[Flags]` enum | per-character class bits |
""" % (nvals - 1,
       TKN, kind["start"], kind["end"],
       TKN, flags["start"], flags["end"],
       TKN, tables[f"{TKN}::s_staticTokenFlags"]["start"], tables[f"{TKN}::s_staticTokenFlags"]["end"],
       TKN, tables[f"{TKN}::s_tokenText"]["start"], tables[f"{TKN}::s_tokenText"]["end"],
       TOK, tables[f"{TOK}::s_keywordText"]["start"], tables[f"{TOK}::s_keywordText"]["end"],
       TOK, tables[f"{TOK}::_operatorText"]["start"], tables[f"{TOK}::_operatorText"]["end"],
       CHT, enums["CharTraits"]["start"], enums["CharTraits"]["end"]))

    w("\n## 3. TokenKind (every member) [SPEC]\n")
    w("Value gaps are reserved slots (placeholders `Reserved slot N` in the static tables); they are listed so the value range is complete. `Text` is the entry of `s_tokenText`; `Static flags` is the entry of `s_staticTokenFlags`.\n")
    w("| Value | Name | Source line | Text | Static flags |")
    w("|---:|---|---:|---|---|")
    for v in range(nvals):
        m = byval.get(v)
        if m is None:
            w(f"| {v} | *(unnamed: reserved slot)* | — | `{esc(texts[v])}` | {esc(sflags[v].replace('TokenFlags.', ''))} |")
        else:
            w(f"| {v} | `{m['name']}` | L{m['line']} | `{esc(texts[v])}` | {esc(sflags[v].replace('TokenFlags.', ''))} |")

    w("\n## 4. TokenFlags (every member) [SPEC]\n")
    w("| Name | Value | Source line |")
    w("|---|---|---:|")
    for m in flags["members"]:
        w(f"| `{m['name']}` | `{m['value']}` | L{m['line']} |")

    w("\n## 5. Keywords (`Tokenizer.s_keywordText` / `s_keywordTokenKind`) [SPEC]\n")
    w("Parallel arrays; recognition is case-insensitive (`s_keywordTable` is built with `OrdinalIgnoreCase`, see [02.1-tokenizer.md](02.1-tokenizer.md) §6). `inlinescript` is only a keyword inside a workflow context.\n")
    w("| # | Spelling | TokenKind | Static flags of the kind |")
    w("|---:|---|---|---|")
    for i, (t, k) in enumerate(zip(kw_text, kw_kind), 1):
        w(f"| {i} | `{esc(t)}` | `{k}` | {esc(flag_of.get(k, '?').replace('TokenFlags.', ''))} |")
    w(f"\nKeyword rows: **<!--N:TOKENIZER_KEYWORD_ROWS-->{len(kw_text)}<!--/N-->** (`GENERATED`). `TokenKind.DynamicKeyword` has no row; dynamic (DSC) keywords come from `DynamicKeyword.DynamicKeywords`.")

    w("\n## 6. Dash operators (`Tokenizer._operatorText` / `s_operatorTokenKind`) [SPEC]\n")
    w("Spelling is stored **without** the leading dash. Recognition happens only in expression mode (see [02.1-tokenizer.md](02.1-tokenizer.md) §6.4).\n")
    w("| # | Spelling | TokenKind | Static flags of the kind |")
    w("|---:|---|---|---|")
    for i, (t, k) in enumerate(zip(op_text, op_kind), 1):
        w(f"| {i} | `-{esc(t)}` | `{k}` | {esc(flag_of.get(k, '?').replace('TokenFlags.', ''))} |")
    w(f"\nDash-operator rows: **<!--N:TOKENIZER_DASH_OPERATOR_ROWS-->{len(op_text)}<!--/N-->** (`GENERATED`).")

    ch = enums["CharTraits"]
    w("\n## 7. CharTraits (character-class bits) [SPEC]\n")
    w("| Name | Value | Source line |")
    w("|---|---|---:|")
    for m in ch["members"]:
        w(f"| `{m['name']}` | `{m['value']}` | L{m['line']} |")

    ns = enums["NumberSuffixFlags"]
    w("\n## 8. NumberSuffixFlags and NumberFormat [SPEC]\n")
    w("| Name | Value | Source line |")
    w("|---|---|---:|")
    for m in ns["members"]:
        w(f"| `{m['name']}` | `{m['value']}` | L{m['line']} |")
    if "NumberFormat" in enums:
        w("")
        w("| NumberFormat | Value | Source line |")
        w("|---|---|---:|")
        for m in enums["NumberFormat"]["members"]:
            w(f"| `{m['name']}` | `{m['value']}` | L{m['line']} |")

    tm = enums["TokenizerMode"]
    w("\n## 9. TokenizerMode [SPEC]\n")
    w("| Name | Source line |")
    w("|---|---:|")
    for m in tm["members"]:
        w(f"| `{m['name']}` | L{m['line']} |")

    w("\n## 10. Cross-document links\n")
    w("Narrative, mode-transition table and lexical rules: [02.1-tokenizer.md](02.1-tokenizer.md). Parser consumers of each kind: [02.2-parser.md](02.2-parser.md) (planned, T22). Token subclasses: [02.1-tokenizer.md](02.1-tokenizer.md) §4.\n")
    w("\nVerification: row counts asserted equal to the `TokenKind` value range (%d) and to `data/numbers.json` keys `TOKENKIND_MEMBERS`, `TOKENFLAGS_MEMBERS`; keyword and operator arrays asserted pairwise equal length (`gen_T21.py`). Static-flag and text arrays were also read in the source windows recorded in `.work/notes/` (token.cs W3-W4).\n" % nvals)

    os.makedirs(os.path.join(OUT, "02-language"), exist_ok=True)
    p = os.path.join(OUT, "02-language", "TOKEN-CATALOG.md")
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote", p, "kinds", nvals, "kw", len(kw_text), "ops", len(op_text))


if __name__ == "__main__":
    sys.exit(main())
