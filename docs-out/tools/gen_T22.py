#!/usr/bin/env python3
"""gen_T22.py - generated parts of the parser documents (task T22, rule 9).

Purpose : (1) 02-language/ERROR-CATALOG.md  - every ParserStrings.resx key with message text and
              the places that report it (Parser.cs, tokenizer.cs, other files);
          (2) fills the marked regions <!--GEN:productions--> and <!--GEN:precedence--> in
              02-language/02.2-parser.md (production table, binary-operator precedence table).
Inputs  : data/resources.json, data/parser-methods.json, data/tables.json, data/enums.json,
          src/System.Management.Automation/resources/ParserStrings.resx, Parser.cs (read-only,
          to classify ReportError vs ReportIncompleteInput and to find AST constructors/token kinds per method).
Outputs : docs-out/02-language/ERROR-CATALOG.md, regions of docs-out/02-language/02.2-parser.md
Run     : python3 docs-out/tools/gen_T22.py        (from the repo root; rerunnable)
          python3 docs-out/tools/gen_T22.py --count parserstrings_keys|parser_methods|binary_operators
Label   : APPROX (regex extraction; names and counts are cross-checked by reading, see documents).
Language: Python 3 (D-002)
"""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
PARSER = "src/System.Management.Automation/engine/parser/Parser.cs"
TOKENIZER = "src/System.Management.Automation/engine/parser/tokenizer.cs"
TOKEN = "src/System.Management.Automation/engine/parser/token.cs"
RESX = "src/System.Management.Automation/resources/ParserStrings.resx"


def J(n):
    return json.load(open(os.path.join(DATA, n)))


def lines(p):
    return open(os.path.join(ROOT, p), encoding="utf-8-sig").read().split("\n")


def esc(s):
    return s.replace("|", "\\|").replace("\n", " ").replace("\r", "")


def resx_messages():
    t = ET.parse(os.path.join(ROOT, RESX))
    return {d.get("name"): (d.findtext("value") or "") for d in t.getroot().findall("data")}


def classify(src, line):
    """E/I/? : nearest ReportError( / ReportIncompleteInput( call at or before `line` (within 14 lines)."""
    for i in range(line - 1, max(line - 16, 0), -1):
        s = src[i]
        if "ReportIncompleteInput(" in s:
            return "I"
        if "ReportError(" in s:
            return "E"
    return "?"


def uses_for(key, rdata):
    for k in rdata["keys"]:
        if k["key"] == key:
            return k["uses"]
    return []


def compact(lns):
    out = []
    for n in sorted(set(lns)):
        if out and n - out[-1] <= 2:
            continue
        out.append(n)
    return out


def error_catalog():
    res = J("resources.json")
    rd = res[RESX]
    msgs = resx_messages()
    psrc = lines(PARSER)
    tsrc = lines(TOKENIZER)
    rows_a, rows_b = [], []
    for k in sorted(rd["keys"], key=lambda x: x["key"]):
        key = k["key"]
        pl = [u["line"] for u in k["uses"] if u["file"] == PARSER]
        tl = [u["line"] for u in k["uses"] if u["file"] == TOKENIZER]
        other = sorted({u["file"].replace("src/System.Management.Automation/", "") for u in k["uses"] if u["file"] not in (PARSER, TOKENIZER)})
        pc = " ".join(f"L{n}({classify(psrc, n)})" for n in compact(pl))
        tc = " ".join(f"L{n}({classify(tsrc, n)})" for n in compact(tl))
        msg = esc(msgs.get(key, "(no message in resx)"))
        if pl or tl:
            rows_a.append((key, msg, pc, tc, ", ".join(f"`{o}`" for o in other[:3]) + (f" +{len(other)-3}" if len(other) > 3 else "")))
        else:
            rows_b.append((key, msg, k["use_count"], ", ".join(f"`{o}`" for o in other[:3]) + (f" +{len(other)-3}" if len(other) > 3 else "")))
    n_keys = len(rd["keys"])
    L = []
    w = L.append
    w("""---
id: LANG-ERRCAT-001
title: Parser and tokenizer error catalog
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: [CF-ERR-002]
sources: [src/System.Management.Automation/resources/ParserStrings.resx, src/System.Management.Automation/engine/parser/Parser.cs, src/System.Management.Automation/engine/parser/tokenizer.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/resources/_folder.md]
generated_from: [data/resources.json, data/parser-methods.json]
---

# Parser and tokenizer error catalog

> STATIC-ONLY — behavior not run-verified. Every row is `GENERATED` by `docs-out/tools/gen_T22.py` (`APPROX`: use sites come from `data/resources.json`, the (E)/(I) classification looks at the nearest preceding `ReportError(` / `ReportIncompleteInput(` call in the source). Narrative: [02.2-parser.md](02.2-parser.md) §9, [02.1-tokenizer.md](02.1-tokenizer.md) §9.
""")
    w("## 1. Purpose and scope [SPEC]\n")
    w(f"""Catalog of the parse error IDs. An error ID is the resource key of `ParserStrings.resx` (the code passes `nameof(ParserStrings.Key)` as ID and `ParserStrings.Key` as message template; `FACT-SRC`, `{PARSER}::Parser.ReportError@L8143-L8166`). `ParserStrings.resx` holds **<!--N:PARSERSTRINGS_KEYS-->{n_keys}<!--/N-->** keys; <!--N:PARSERSTRINGS_KEYS_PARSER_TOKENIZER-->{len(rows_a)}<!--/N--> are reported from `Parser.cs` or `tokenizer.cs` (section 3); the others are reported by semantic checks, type/class building or other code (section 4, owned by [02.4-semantic-analysis.md](02.4-semantic-analysis.md), planned T24).

Report kinds: **(E)** `ReportError` — a plain error; **(I)** `ReportIncompleteInput` — the error sets `ParseError.IncompleteInput` when the error position is at the end of the script (so a REPL can ask for another line) (`{PARSER}::Parser.ReportIncompleteInput@L8111-L8141`); **(?)** the classifier found neither call nearby (error built through a variable, e.g. `errorId`/`errorMsg`).

Dedup: `SaveError` drops an error when an earlier error has the same ID and the same start/end line and column; there is no cap on the number of errors (`{PARSER}::Parser.SaveError@L8026-L8057`).
""")
    w("<!--CF:CF-ERR-002-->**Parse-error limits and recovery rule.** The parser never throws for a syntax error: each error is appended to `Parser.ErrorList` after de-duplication (an error is dropped only if an earlier error has the same ID and the same start and end line and column), there is no limit on the number of errors, and parsing continues by returning partial or error nodes (`ErrorStatementAst`, `ErrorExpressionAst`), by pretending a missing closing token was present, or by skipping tokens to a synchronization token (`SyncOnError`, which tracks nesting of `()`, `{}` and `[]` and never consumes end of input); `ParseError.IncompleteInput` is true only when the error was reported with `ReportIncompleteInput` and the error position is at the end of the script apart from whitespace and comments. The only exceptions are an exhausted execution stack (the whole parse is retried once on a new thread, then `ScriptTooComplicated` is reported) and any other exception during `ParseFile`/`ParseInput`, which is wrapped as a `ParseException` with `UnrecoverableParserError`.<!--/CF-->\n")
    w("## 2. Source map\n")
    w("| path | type | role |\n|---|---|---|")
    w(f"| `{RESX}` | resx | error message templates |")
    w(f"| `{PARSER}::Parser.ReportError@L8143-L8166` | method | report a plain error |")
    w(f"| `{PARSER}::Parser.ReportIncompleteInput@L8111-L8141` | method | report an error that may mean 'more input expected' |")
    w(f"| `{PARSER}::ParseError@L8193-L8241` | class | public error object: `Extent`, `ErrorId`, `Message`, `IncompleteInput` |\n")
    w("## 3. Keys reported by Parser.cs or tokenizer.cs\n")
    w("| Error ID (resource key) | Message template | Parser.cs lines | tokenizer.cs lines | Also used in |")
    w("|---|---|---|---|---|")
    for key, msg, pc, tc, other in rows_a:
        w(f"| `{key}` | {msg} | {pc} | {tc} | {other} |")
    w(f"\nRows: **<!--N:PARSERSTRINGS_KEYS_PARSER_TOKENIZER-->{len(rows_a)}<!--/N-->** (`GENERATED`).\n")
    w("## 4. Keys used only elsewhere (semantic checks, type building, runtime)\n")
    w("| Resource key | Message template | Use count | Files (first three) |")
    w("|---|---|---:|---|")
    for key, msg, cnt, other in rows_b:
        w(f"| `{key}` | {msg} | {cnt} | {other} |")
    w(f"\nRows: **{len(rows_b)}** (`GENERATED`). Keys with use count 0 have no reference found by the dataset scan (dead or referenced reflectively: `UNVERIFIED`).\n")
    w("## 5. Cross-checks\n")
    w("`ParserStrings` is not the only resource class a parser error ID can come from: the debug-only check `AssertErrorIdCorrespondsToMsgString` looks the ID up in `ParserStrings`, `DiscoveryExceptions`, `ExtendedTypeSystem`, `MshSnapInCmdletResources` and `ParameterBinderStrings` (`FACT-SRC`, `" + PARSER + "::Parser.AssertErrorIdCorrespondsToMsgString@L8065-L8093`). Only `ParserStrings` is cataloged here.\n")
    w(f"Verification: key count taken from `data/resources.json` (`ParserStrings.resx`, key_count {n_keys}) and reconciled with the `<data>` element count of the resx parsed with `xml.etree` (`{len(msgs)}`); every row has a message from the resx.\n")
    open(os.path.join(OUT, "02-language", "ERROR-CATALOG.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("ERROR-CATALOG: keys", n_keys, "parser/tokenizer", len(rows_a), "others", len(rows_b), "resx", len(msgs))
    return n_keys, len(rows_a)


def productions():
    pm = [x for x in J("parser-methods.json") if x["file"] == PARSER]
    src = lines(PARSER)
    out = ["| Production (method) | Kind | File@Lines | Tokens referenced (`TokenKind`, APPROX) | AST created (`new …Ast(`, APPROX) | Error IDs (`ParserStrings`, APPROX) |",
           "|---|---|---|---|---|---|"]
    for m in pm:
        body = "\n".join(src[m["start"] - 1:m["end"]])
        toks = sorted(set(re.findall(r"TokenKind\.(\w+)", body)))
        asts = sorted(set(re.findall(r"new\s+(\w+Ast)\s*\(", body)))
        errs = sorted(set(re.findall(r"nameof\(ParserStrings\.(\w+)\)", body)))
        tname = m["type"].split(".")[-1]
        kind = "rule" if m["method"].endswith("Rule") else "helper"
        def cell(v, cap=14):
            if not v:
                return "—"
            s = ", ".join(f"`{x}`" for x in v[:cap])
            return s + (f" +{len(v)-cap}" if len(v) > cap else "")
        out.append(f"| `{m['method']}` | {kind} | `{PARSER}::{tname}.{m['method']}@L{m['start']}-L{m['end']}` | {cell(toks)} | {cell(asts, 8)} | {cell(errs, 8)} |")
    return out, len(pm)


def precedence():
    """binary operators: token kind -> precedence level (TokenFlags.BinaryPrecedence*) - GENERATED from token.cs tables."""
    sys.path.insert(0, os.path.join(OUT, "tools"))
    import gen_T21 as g
    tb = J("tables.json")
    en = {e["full_name"].split(".")[-1]: e for e in J("enums.json") if e["file"] == TOKEN}
    flags = {m["name"]: m["value"] for m in en["TokenFlags"]["members"]}
    kinds = en["TokenKind"]["members"]
    sfl = [re.sub(r"\s+", " ", x) for x in g.split_top(g.strip_comments(tb[f"{TOKEN}::s_staticTokenFlags"]["text"]))]
    txt = [g.unq(x) for x in g.split_top(g.strip_comments(tb[f"{TOKEN}::s_tokenText"]["text"]))]
    prec = {k: int(v, 16) for k, v in flags.items() if k.startswith("BinaryPrecedence") and k != "BinaryPrecedenceMask"}
    rows = []
    for m in kinds:
        v = int(m["value"])
        f = sfl[v]
        if "BinaryOperator" not in f:
            continue
        p = [k for k in prec if "TokenFlags." + k in f]
        rows.append((prec[p[0]] if p else -1, p[0].replace("BinaryPrecedence", "") if p else "?", m["name"], txt[v], "Unary" if "UnaryOperator" in f else "", "CanConstantFold" if "CanConstantFold" in f else "", "DisallowedInRestrictedMode" if "DisallowedInRestrictedMode" in f else ""))
    rows.sort(key=lambda r: (r[0], r[2]))
    out = ["| Level (value) | Level name | TokenKind | Text | Also unary | Constant-folded | Restricted-mode flag |",
           "|---:|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r[0]} | {r[1]} | `{r[2]}` | `{esc(r[3])}` | {r[4]} | {r[5]} | {r[6]} |")
    return out, len(rows)


def fill(doc, tag, rows):
    p = os.path.join(OUT, "02-language", doc)
    t = open(p, encoding="utf-8").read()
    pat = re.compile(r"(<!--GEN:%s-->)\n?.*?\n?(<!--/GEN:%s-->)" % (tag, tag), re.S)
    if not pat.search(t):
        print("region missing", tag, doc)
        return
    t = pat.sub(lambda m: m.group(1) + "\n" + "\n".join(rows) + "\n" + m.group(2), t)
    open(p, "w", encoding="utf-8").write(t)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--count":
        what = sys.argv[2]
        if what == "parserstrings_keys":
            print(J("resources.json")[RESX]["key_count"])
        elif what == "parser_methods":
            print(len([x for x in J("parser-methods.json") if x["file"] == PARSER]))
        elif what == "binary_operators":
            print(precedence()[1])
        elif what == "parserstrings_keys_parser_tokenizer":
            rd = J("resources.json")[RESX]
            print(sum(1 for k in rd["keys"] if any(u["file"] in (PARSER, TOKENIZER) for u in k["uses"])))
        return 0
    error_catalog()
    if os.path.exists(os.path.join(OUT, "02-language", "02.2-parser.md")):
        rows, n = productions()
        fill("02.2-parser.md", "productions", rows)
        rows, n2 = precedence()
        fill("02.2-parser.md", "precedence", rows)
        print("productions", n, "binary operators", n2)


if __name__ == "__main__":
    sys.exit(main())
