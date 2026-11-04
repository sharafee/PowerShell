---
id: LANG-SPEC-001
title: Language specification draft
kind: guide
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/parser/tokenizer.cs, src/System.Management.Automation/engine/parser/Parser.cs, src/System.Management.Automation/engine/LanguagePrimitives.cs]
mirror_cards: []
generated_from: []
---

# Language specification draft

> STATIC-ONLY — baseline behavior specification of the target language (= PowerShell 7.6.9's observable behavior, `CORE` scope), assembled from the study documents. Every statement links to the section that holds its evidence; there are no golden samples, so confirmation with `pwsh` is open (VB-001). All sections are `SPEC`. Each major section ends with a `DEVIATIONS:` note listing the proposals (`DEV-*`) that concern it, or "none"; canvas rows are in [new-language-design-canvas.md](../09-synthesis/new-language-design-canvas.md).

## 1. Purpose and scope [SPEC]

What a MicroteamShell implementation must do to be PowerShell-faithful at the language core: lexical structure, grammar summary, types and conversions, expressions, statements, scoping, pipeline semantics, error semantics. Out of scope: cmdlets, providers, modules, remoting, DSC, formatting.

## 2. Source map

Evidence documents: [02.1](02.1-tokenizer.md), [02.2](02.2-parser.md), [GRAMMAR](GRAMMAR.ebnf.md), [02.3](02.3-ast.md), [02.4](02.4-semantic-analysis.md), [02.5](02.5-compiler-and-engine.md), [02.6](02.6-types-and-operators.md), [OPERATOR-TABLE](OPERATOR-TABLE.md), [CONVERSION-RULES](CONVERSION-RULES.md), [SCOPE](SCOPE-AND-VARIABLES.md), [RTOPS](RUNTIME-OPERATIONS.md), [SB](SCRIPT-BLOCKS.md), [QUIRKS](SEMANTIC-QUIRKS.md).

## 3. Lexical structure

1. A script is Unicode text; lines end with `CR`, `LF` or `CRLF` ([02.1 §7.6](02.1-tokenizer.md)). Newline is a token, not whitespace; space, tab, form feed, vertical tab, no-break space and next-line are whitespace.
2. The tokenizer works in four modes — command, expression, type name, signature — chosen by the parser; text is tokenized lazily ([02.1 §6.2](02.1-tokenizer.md), CF-LEX-001).
3. **Comments**: `# …` to end of line; `<# … #>` not nested; `#requires` lines are pragmas ([02.1 §7.4](02.1-tokenizer.md)).
4. **Line continuation**: a backtick before a newline; whitespace after the backtick is skipped; a newline inside `()`, after a binary operator or after `|`, `&&`, `||`, `,` also continues ([02.2 §6.3](02.2-parser.md), CF-GRM-001).
5. **Identifiers and keywords**: keywords (<!--N:TOKENIZER_KEYWORD_ROWS-->51<!--/N--> in the keyword table, [TOKEN-CATALOG §5](TOKEN-CATALOG.md)) are case-insensitive and recognized only in command (and signature) mode; elsewhere they are identifiers or barewords.
6. **Variables**: `$name`, `${any text}`, `$scope:name`, `$drive:name`, `@name` (splatting); `$?`, `$^`, `$$`, `$_` are single-character names ([02.1 §7.3](02.1-tokenizer.md)).
7. **Numbers**: decimal, hex `0x`, binary `0b`, real with exponent; type suffixes `u s l d y n` (and `ul us uy`); multipliers `kb mb gb tb pb` (1024 powers); the suffix comes before the multiplier; a number must end at a token boundary (CF-LEX-002).
8. **Strings**: single-quoted (`''` escapes a quote, no backtick escapes), double-quoted (backtick escapes `` `0 `a `b `e `f `n `r `t `v `u{…} ``, `""` escapes a quote, `$var` / `${…}` / `$(…)` expand), here-strings `@'…'@` / `@"…"@` with the footer at the start of a line; smart quotes and en/em dashes are accepted as quotes and dashes ([02.1 §7.2](02.1-tokenizer.md), [§5](02.1-tokenizer.md)).
9. **Operators and punctuation**: symbol operators and dash operators (`-eq`, `-and`, …) — the latter only in expression mode ([OPERATOR-TABLE](OPERATOR-TABLE.md)); redirection tokens `>`, `>>`, `2>`, `2>&1`, `*>` (streams 1-6 and all) ([02.1 §7.5](02.1-tokenizer.md)).

DEVIATIONS: DEV-LEX-001 (no `#requires`/signature handling in the tokenizer); canvas row NLD-LEX.

## 4. Grammar summary

The normative grammar is [GRAMMAR.ebnf.md](GRAMMAR.ebnf.md). Summary: a script block is `using` statements, an optional `param` block, then either named blocks (`begin process end dynamicparam clean`) or a statement list. Statements are separated by optional newlines and semicolons; no terminator is needed after a block statement (CF-GRM-001). A pipeline is expressions or commands joined by `|`; pipelines chain with `&&`/`||` and can run in the background with `&`. Assignment has a statement on its right. Binary operators are left-associative with the levels of CF-OP-001; the comma binds tighter than binary operators; ternary and assignment bind looser. Hashtable values are statements. Parse errors are collected, never thrown for bad input, and a tree is still produced (CF-ERR-002).

DEVIATIONS: DEV-GRM-010 (parsing without side effects); canvas row NLD-GRM.

## 5. Types and conversions

1. Values are .NET objects; `$null` is null; "no value" (`AutomationNull`) is distinct; wrappers carry extra members ([02.6 §4](02.6-types-and-operators.md)).
2. Conversion follows the ordered search of CF-CNV-001 with ranks; strings convert to numbers with the literal syntax; numbers to strings with invariant formatting; `IsTrue` defines truthiness ([CONVERSION-RULES](CONVERSION-RULES.md)).
3. Arithmetic promotes to the wider type, overflows `int` to `double`, and divides `int/int` exactly or as `double` ([02.6 §7.2](02.6-types-and-operators.md)).
4. Collections are enumerated per CF-PIP-001; arrays are `object[]` unless typed; hashtables are case-insensitive (`Hashtable`/`OrderedDictionary`).

DEVIATIONS: DEV-TYP-070 (no language-mode gate in conversion); canvas row NLD-TYP.

## 6. Expressions

Operators and their per-type behavior: [OPERATOR-TABLE §4](OPERATOR-TABLE.md). Member access `.` and `::`, method calls (no whitespace before `(`), indexing and slicing, casts, array and hashtable literals, sub-expressions `$()`/`@()`, script block literals, ternary and null-coalescing, `-f`, ranges ([GRAMMAR §7](GRAMMAR.ebnf.md), [BINDER-CATALOG](BINDER-CATALOG.md)). Constant expressions are folded only for foldable operators ([02.3 §7.1](02.3-ast.md)).

DEVIATIONS: DEV-BIND-050 (no COM/ETS-adapter member binding); canvas row NLD-OP.

## 7. Statements

`if/elseif/else`, `while`, `do … while|until`, `for`, `foreach`, `switch` (all matching clauses run; flags regex/wildcard/exact/casesensitive/file), `break`/`continue` with labels, `return`, `exit`, `throw`, `try/catch/finally`, `trap`, `function`/`filter` with `param`, `begin/process/end`, `data`, `class`/`enum`/`using` (EXTENDED) ([GRAMMAR §4-5](GRAMMAR.ebnf.md), [02.5 §6.3-6.4](02.5-compiler-and-engine.md)). Semantic rules (duplicate parameters, loop-control placement, assignment targets, constant attribute arguments) are errors at parse time ([02.4 §8](02.4-semantic-analysis.md)).

DEVIATIONS: DEV-FEAT-091 (reject workflow keywords at parse time); canvas row NLD-GRM.

## 8. Scoping and variables

CF-SCP-001: dynamic-scope reads, local writes, qualifiers `global: script: local: private:`, options `ReadOnly Constant Private AllScope`, new scope per function/script block call, dot-sourcing without scope, `$using:` for remote-style blocks, closures by snapshot ([SCOPE](SCOPE-AND-VARIABLES.md), [SB](SCRIPT-BLOCKS.md)). Strict mode by version walks scopes ([execution context](../03-runtime/execution-context-and-session-state.md) §4).

DEVIATIONS: DEV-SCP-080, DEV-CTX-081 (no language-mode trust marking); canvas row NLD-SCP.

## 9. Pipeline semantics

A statement's value is output only for bare expressions and commands; output is written to the current pipe and unrolled one level (CF-PIP-001); `return` writes output then leaves; conditions, assignments, `$()` and `@()` capture output in a temporary pipe; commands run `begin`/`process`/`end` with `$_` and `$input` ([02.5 §6.5](02.5-compiler-and-engine.md), [LIFECYCLE](LIFECYCLE-script-execution.md)). Pipeline chains `&&`/`||` test `$?`.

DEVIATIONS: none (canvas row NLD-PIP).

## 10. Error semantics

Three channels: parse diagnostics (before running), runtime exceptions, error records on the error stream ([STAGE-CONTRACTS §9](STAGE-CONTRACTS.md)). Each statement is guarded: an error is recorded (`$Error`, `$?` false), then `$ErrorActionPreference` and traps decide to continue, stop or ignore; `throw` terminates unless trapped or caught; `try/catch/finally` matches typed handlers in order and sets `$_` to the error record ([RTOPS §6.1](RUNTIME-OPERATIONS.md), [02.5 §6.4](02.5-compiler-and-engine.md)). Flow-control signals pass through all handlers.

DEVIATIONS: none (CF-ERR-001 is documented with the errors document in Phase 3); canvas row NLD-ERR.

## 11. Observable-behavior quirks

See [SEMANTIC-QUIRKS.md](SEMANTIC-QUIRKS.md) (<!--N:QUIRKS_TOTAL-->32<!--/N--> quirks with verdicts).

DEVIATIONS: DEV-LEX-001, DEV-GRM-010, DEV-SEM-030.

## 12. Dependencies

Documents listed in §2.

## 13. Performance notes

Not applicable (behavior only); execution strategy: [INTERPRETER-DESIGN-SPACE.md](INTERPRETER-DESIGN-SPACE.md).

## 14. Security considerations (mandatory)

Language modes, restricted data sections, constrained conversions and parse-time side effects are described in the linked sections; the baseline includes restricted-language checking for `data` sections ([02.4 §14](02.4-semantic-analysis.md)).

## 15. Enterprise considerations

Diagnostics, logging and positions: [STAGE-CONTRACTS.md](STAGE-CONTRACTS.md) §15.

## 16. Tests

[REFERENCE-TEST-CORPUS.md](REFERENCE-TEST-CORPUS.md).

## 17. Design decisions and trade-offs

The specification is behavior-first; mechanisms (DLR, expression trees, binders) are not part of it.

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-SPEC-01** [REPLICATE] (area: NLD-GRM) Treat this specification plus the quirks catalog as the acceptance baseline and add oracle-confirmed tests per statement. Evidence: `src/System.Management.Automation/engine/parser/Parser.cs::Parser@L36-L8191`.
- **LSN-SPEC-02** [ADAPT] (area: NLD-TOOL) Keep the specification in the shell's repository as executable examples (snippet + expected result) rather than prose only. Why: same content, checkable. Evidence: `test/powershell/Language/Parser/` (test style).

## 19. Open questions / UNVERIFIED

All statements are `FACT-SRC` or `INFERENCE` per the linked sections; the oracle (VB-001) is needed to promote them. The command invocation and parameter binding rules (Phase 3) are not part of this draft.

Verification: each paragraph cites the section holding its evidence; counts (keywords, quirks) come from registered numbers.
