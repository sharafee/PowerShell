---
id: LANG-QUIRKS-001
title: Semantic quirks
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/parser/tokenizer.cs, src/System.Management.Automation/engine/parser/Parser.cs, src/System.Management.Automation/engine/runtime/Binding/Binders.cs, src/System.Management.Automation/engine/runtime/Operations/MiscOps.cs, src/System.Management.Automation/engine/LanguagePrimitives.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/parser/_folder.md]
generated_from: []
---

# Semantic quirks

> STATIC-ONLY — behavior not run-verified; there are no golden samples, so every quirk is read from source (`FACT-SRC`) and its confirmation with `pwsh` is a backlog item. Each quirk has a verdict from the shared vocabulary: `REPLICATE` (part of the baseline), `ADAPT` (same behavior, different mechanism), `REDESIGN` / `AVOID` (a deviation *proposal*, exactly one `DEV-*` row, baseline stays until the owner approves). Counts: <!--N:QUIRKS_TOTAL-->32<!--/N--> quirks — <!--N:QUIRKS_REPLICATE-->26<!--/N--> REPLICATE, <!--N:QUIRKS_ADAPT-->3<!--/N--> ADAPT, <!--N:QUIRKS_AVOID-->3<!--/N--> AVOID, <!--N:QUIRKS_REDESIGN-->0<!--/N--> REDESIGN (counted from the table by `tools/gen_coord.py`). The design canvas ([new-language-design-canvas.md](../09-synthesis/new-language-design-canvas.md)) consumes these verdicts.

## 1. Purpose and scope [SPEC]

Surprising behaviors that an implementer would get wrong from intuition: lexical ambiguities, parsing choices, type coercions, collection handling, output rules, scoping and error semantics.

## 2. Source map

Evidence is by link to the owning document section, which cites the source lines.

## 3. Responsibilities and non-responsibilities

Catalog only; rules are specified in the linked sections and in [LANGUAGE-SPEC-DRAFT.md](LANGUAGE-SPEC-DRAFT.md).

## 4. Key types and contracts [IMPL]

Not applicable.

## 5. Data model — the quirks

| ID | Quirk | Evidence | Golden sample | Verdict | DEV | Rationale |
|---|---|---|---|---|---|---|
| QRK-01 | The same text tokenizes differently by mode: `-eq` is a parameter in a command and an operator in an expression; keywords are recognized only in command mode | [02.1 §6.3](02.1-tokenizer.md) | none (STATIC-ONLY) | REPLICATE | | defines the language's command-versus-expression behavior |
| QRK-02 | `$a-b` is `$a` minus `b` in an expression but one word in a command; `-` is not a variable-name character | [02.1 §7.3](02.1-tokenizer.md) | none | REPLICATE | | needed for command arguments like `echo $a-b` |
| QRK-03 | `#requires` is recognized only when the letters follow `#` immediately, without checking the next character; comments similar to a signature header (edit distance < 10) forbid code after them | [02.1 §7.4](02.1-tokenizer.md) | none | AVOID | DEV-LEX-001 | tokenizer should stay a pure function; pragmas and signature trailers move out of the tokenizer |
| QRK-04 | `$(` inside a string is pre-scanned by counting parentheses only, so a `)` in a nested quoted string may end the scan early (`UNVERIFIED`) | [02.1 §7.2](02.1-tokenizer.md) | none | ADAPT | | scan quotes and comments too; valid scripts behave the same |
| QRK-05 | Hashtable values and assignment right sides are statements: `@{a = if ($x) {1} else {2}}`, `$x = if …`, `$x = 1 \| f` | [GRAMMAR §7, §3a](GRAMMAR.ebnf.md) | none | REPLICATE | | grammar-level baseline |
| QRK-06 | No terminator is needed after a block statement: `if ($x) {1} 2` is two statements; `1 2` is an error | [02.2 §6.3](02.2-parser.md) | none | REPLICATE | | CF-GRM-001 |
| QRK-07 | All binary operators are left-associative, comparison operators share one level with `-split`, `-join`, `-shl`; comma binds tighter than every binary operator (`1,2 -eq 3` compares an array) | [OPERATOR-TABLE §3](OPERATOR-TABLE.md) | none | REPLICATE | | CF-OP-001 |
| QRK-08 | A leading sign belongs to a number only at a unary position (`AllowSignedNumbers`); `1 -1` is a subtraction | [02.1 §6.4](02.1-tokenizer.md) | none | REPLICATE | | needed for correct arithmetic parsing |
| QRK-09 | Typing is left-operand-driven: `1 + "2"` is 3, `"1" + 2` is `"12"`; `"a" * 3` repeats; `array + x` appends | [OPERATOR-TABLE §4](OPERATOR-TABLE.md) | none | REPLICATE | | defines operator behavior |
| QRK-10 | `int` overflow becomes `double`; `int / int` is an `int` only when exact, else `double`; division by zero is a runtime error | [02.6 §7.2](02.6-types-and-operators.md) | none | REPLICATE | | numeric baseline |
| QRK-11 | A collection on the left of `-eq`, `-like`, `-match` etc. filters and returns elements instead of a bool; `$null -eq $x` is true only for `$null` | [02.6 §7.3](02.6-types-and-operators.md) | none | REPLICATE | | idiomatic filtering |
| QRK-12 | Truthiness: non-empty string is true (even `"false"`); `@(0)` is false but `@(1,2)` is true; a single-element list is judged by its element | [CONVERSION-RULES §7.3](CONVERSION-RULES.md) | none | REPLICATE | | `IsTrue` |
| QRK-13 | Output unrolls exactly one level; strings, hashtables and `$null` are never enumerated; `AutomationNull` writes nothing | [02.6 §7.1](02.6-types-and-operators.md) | none | REPLICATE | | CF-PIP-001 |
| QRK-14 | `return $x` does not return a value: it writes `$x` to the output pipe, and a function's result is everything written to its pipe | [02.5 §6.5](02.5-compiler-and-engine.md) | none | REPLICATE | | pipeline semantics |
| QRK-15 | A bare expression statement is output; assignments and `++`/`--` are not; `[void]` and `$null =` discard | [IR-SPEC §5](IR-SPEC.md) | none | REPLICATE | | statement output rule |
| QRK-16 | Errors in a statement are reported and the script continues with the next statement (`ErrorActionPreference` default `Continue`); `throw` and `Stop` terminate | [RUNTIME-OPERATIONS §6.1](RUNTIME-OPERATIONS.md) | none | REPLICATE | | shell-style resilience |
| QRK-17 | Reads search parent scopes (dynamic scoping) but writes always go to the current scope; `$x = 1` in a function never changes the caller's `$x` | [SCOPE §7.1](SCOPE-AND-VARIABLES.md) | none | REPLICATE | | CF-SCP-001 |
| QRK-18 | `switch` tests every clause for every item (no implicit break); `default` runs only if none matched | [02.5 §6.3](02.5-compiler-and-engine.md) | none | REPLICATE | | switch semantics |
| QRK-19 | `foreach` over a single non-enumerable value runs once; over `$null` (no enumerator) it does not run | [02.5 §6.3](02.5-compiler-and-engine.md) | none | REPLICATE | | loop semantics (`UNVERIFIED` for `$null`) |
| QRK-20 | Numeric literals used as command arguments keep their source text (`echo 0x10` passes `0x10`); numbers converted to strings use the literal text when they came from a literal | [COMPILATION-MAP](COMPILATION-MAP.md) `VisitCommand`, [CONVERSION-RULES §7.2](CONVERSION-RULES.md) | none | REPLICATE | | argument fidelity |
| QRK-21 | `hashtable + hashtable` builds a new table and throws on a shared key; the literal uses an ordinal comparer but `+` a culture comparer | [RUNTIME-OPERATIONS §6.3](RUNTIME-OPERATIONS.md), CON-011 | none | ADAPT | | keep merge/duplicate behavior, use one comparer |
| QRK-22 | `string * n` and array repetition are capped at 1,024 only in restricted language; a negative count throws `ArgumentOutOfRangeException` | [RUNTIME-OPERATIONS §6.2-6.3](RUNTIME-OPERATIONS.md) | none | ADAPT | | cap in every mode, raise a runtime error |
| QRK-23 | Postfix `++` on `$null` yields `0` as the expression value | [02.5](02.5-compiler-and-engine.md) notes (`CompileIncrementOrDecrement`) | none | REPLICATE | | backward compatibility |
| QRK-24 | `?` is a plain word in command mode (alias `?`), an operator only in expression mode; `??` and `?:` exist only in expression mode | [02.1 §6.1](02.1-tokenizer.md) | none | REPLICATE | | mode rule |
| QRK-25 | Keywords used as command arguments are plain words (`echo if`); in expression mode keywords are identifiers | [02.2 §7.4](02.2-parser.md), [02.1 §6.3](02.1-tokenizer.md) | none | REPLICATE | | mode rule |
| QRK-26 | In expression mode `2>x` tokenizes as the number `2` followed by `>`; stream numbers 1-6 only | [02.1 §7.5](02.1-tokenizer.md) | none | REPLICATE | | redirection tokenizing |
| QRK-27 | `break`/`continue` are exceptions across function boundaries: a `break` inside a function called from a loop ends the caller's loop | [LIFECYCLE §6 step 10](LIFECYCLE-script-execution.md), [02.5 §6.3](02.5-compiler-and-engine.md) | none | REPLICATE | | flow-control baseline (`UNVERIFIED`: caller-side catch not traced) |
| QRK-28 | Parsing has side effects: `using assembly` probes the file system, `configuration` can create a runspace, class and enum errors surface at compile time | [02.2 §14](02.2-parser.md), [02.4 §6](02.4-semantic-analysis.md) | none | AVOID | DEV-GRM-010 | parse should be pure |
| QRK-29 | `using module` is resolved while parsing by running `Get-Module -ListAvailable` | [02.4 §6](02.4-semantic-analysis.md) | none | AVOID | DEV-SEM-030 | module import belongs to a later phase |
| QRK-30 | `GetNewClosure` snapshots only variables of the current scope with no special options, by value | [SCRIPT-BLOCKS §6](SCRIPT-BLOCKS.md) | none | REPLICATE | | closure baseline |
| QRK-31 | `AllScope` variables are the same object in every scope; `$null`, `$true`, `$false` are such variables | [SCOPE §5](SCOPE-AND-VARIABLES.md) | none | REPLICATE | | scope baseline |
| QRK-32 | String-to-number conversion accepts the literal syntax (hex, binary, suffixes, `kb`); empty string converts to 0 | [CONVERSION-RULES §7.2](CONVERSION-RULES.md) | none | REPLICATE | | `Parser.ScanNumber` |

## 6. Control flow

Not applicable.

## 7. Algorithms

Not applicable.

## 8. Observable behavior [SPEC]

All rows are observable; none is run-verified.

## 9. Error handling and edge cases

Rows marked `UNVERIFIED` in their rationale are in the backlog (VB-002 to VB-023).

## 10. Concurrency and threading

Not applicable.

## 11. Extension points and customization hooks

Not applicable.

## 12. Dependencies

Documents linked in the evidence column.

## 13. Performance notes

Not applicable.

## 14. Security considerations (mandatory)

QRK-03, QRK-28 and QRK-29 are the security-relevant quirks: fuzzy signature detection, parse-time file and module access, and parse-time runspace creation. QRK-22 matters for denial of service.

## 15. Enterprise considerations

Not applicable.

## 16. Tests

Confirming each quirk is the first use of the oracle protocol ([ORACLE-PROTOCOL.md](ORACLE-PROTOCOL.md)); candidate tests: [REFERENCE-TEST-CORPUS.md](REFERENCE-TEST-CORPUS.md).

## 17. Design decisions and trade-offs

Most quirks are consequences of two decisions: left-operand-driven typing and output-as-side-effect. Replicating them is cheap if the evaluator follows the protocols; changing them breaks scripts.

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-QRK-01** [REPLICATE] (area: NLD-OP) Treat QRK-01 to QRK-27 and QRK-30 to QRK-32 as part of the baseline language and specify them with tests before implementing. Evidence: `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder@L2119-L3422`.
- **LSN-QRK-02** [ADAPT] (area: NLD-OP) Keep the observable behavior of QRK-04, QRK-21 and QRK-22 with safer mechanisms (full scan, single comparer, caps in all modes). Evidence: `src/System.Management.Automation/engine/runtime/Operations/StringOps.cs::StringOps@L15-L107`.
- **LSN-QRK-03** [AVOID] (area: NLD-GRM) Do not reproduce parse-time side effects (QRK-28, QRK-29) or tokenizer-level pragma handling (QRK-03). Evidence: `src/System.Management.Automation/engine/parser/Parser.cs::Parser.ResolveUsingAssembly@L5088-L5168`. DEV: DEV-GRM-010

## 19. Open questions / UNVERIFIED

Every row needs the oracle; QRK-04, QRK-19, QRK-27 are explicitly partial.

Verification: each row was derived from a document section that cites source reads; verdict counts are computed from this table.
