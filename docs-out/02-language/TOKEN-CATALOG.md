---
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

Complete list of token kinds, token flags, keywords, dash operators, character classes, number-suffix flags and tokenizer modes of the PowerShell tokenizer (v7.6.9). Counts: `TokenKind` has <!--N:TOKENKIND_MEMBERS-->157<!--/N--> named members spread over the value range 0..170; `TokenFlags` has <!--N:TOKENFLAGS_MEMBERS-->28<!--/N--> members.

## 2. Source map

| path | type | role |
|---|---|---|
| `src/System.Management.Automation/engine/parser/token.cs::TokenKind@L18-L595` | enum | every token kind |
| `src/System.Management.Automation/engine/parser/token.cs::TokenFlags@L601-L752` | `[Flags]` enum | token traits |
| `src/System.Management.Automation/engine/parser/token.cs::TokenTraits.s_staticTokenFlags@L759-L957` | table | static flags per kind |
| `src/System.Management.Automation/engine/parser/token.cs::TokenTraits.s_tokenText@L959-L1211` | table | default text per kind |
| `src/System.Management.Automation/engine/parser/tokenizer.cs::Tokenizer.s_keywordText@L625-L639` | table | keyword spelling |
| `src/System.Management.Automation/engine/parser/tokenizer.cs::Tokenizer._operatorText@L657-L674` | table | dash-operator spelling |
| `src/System.Management.Automation/engine/parser/CharTraits.cs::CharTraits@L28-L89` | `[Flags]` enum | per-character class bits |


## 3. TokenKind (every member) [SPEC]

Value gaps are reserved slots (placeholders `Reserved slot N` in the static tables); they are listed so the value range is complete. `Text` is the entry of `s_tokenText`; `Static flags` is the entry of `s_staticTokenFlags`.

| Value | Name | Source line | Text | Static flags |
|---:|---|---:|---|---|
| 0 | `Unknown` | L27 | `unknown` | None |
| 1 | `Variable` | L33 | `var` | None |
| 2 | `SplattedVariable` | L40 | `@var` | None |
| 3 | `Parameter` | L46 | `param` | None |
| 4 | `Number` | L52 | `number` | None |
| 5 | `Label` | L58 | `label` | None |
| 6 | `Identifier` | L63 | `ident` | None |
| 7 | `Generic` | L72 | `generic` | None |
| 8 | `NewLine` | L75 | `newline` | ParseModeInvariant |
| 9 | `LineContinuation` | L78 | `line continuation` | ParseModeInvariant |
| 10 | `Comment` | L81 | `comment` | ParseModeInvariant |
| 11 | `EndOfInput` | L84 | `eof` | ParseModeInvariant |
| 12 | `StringLiteral` | L94 | `sqstr` | ParseModeInvariant |
| 13 | `StringExpandable` | L101 | `dqstr` | ParseModeInvariant |
| 14 | `HereStringLiteral` | L107 | `sq here string` | ParseModeInvariant |
| 15 | `HereStringExpandable` | L114 | `dq here string` | ParseModeInvariant |
| 16 | `LParen` | L122 | `(` | ParseModeInvariant |
| 17 | `RParen` | L126 | `)` | ParseModeInvariant |
| 18 | `LCurly` | L129 | `{` | ParseModeInvariant |
| 19 | `RCurly` | L132 | `}` | ParseModeInvariant |
| 20 | `LBracket` | L135 | `[` | None |
| 21 | `RBracket` | L138 | `]` | ParseModeInvariant |
| 22 | `AtParen` | L142 | `@(` | ParseModeInvariant |
| 23 | `AtCurly` | L145 | `@{` | ParseModeInvariant |
| 24 | `DollarParen` | L149 | `$(` | ParseModeInvariant |
| 25 | `Semi` | L152 | `;` | ParseModeInvariant |
| 26 | `AndAnd` | L159 | `&&` | ParseModeInvariant |
| 27 | `OrOr` | L162 | `\|\|` | ParseModeInvariant |
| 28 | `Ampersand` | L165 | `&` | SpecialOperator \| ParseModeInvariant |
| 29 | `Pipe` | L168 | `\|` | SpecialOperator \| ParseModeInvariant |
| 30 | `Comma` | L171 | `,` | UnaryOperator \| ParseModeInvariant |
| 31 | `MinusMinus` | L174 | `--` | UnaryOperator \| PrefixOrPostfixOperator \| DisallowedInRestrictedMode |
| 32 | `PlusPlus` | L177 | `++` | UnaryOperator \| PrefixOrPostfixOperator \| DisallowedInRestrictedMode |
| 33 | `DotDot` | L180 | `..` | BinaryOperator \| BinaryPrecedenceRange \| DisallowedInRestrictedMode |
| 34 | `ColonColon` | L183 | `::` | SpecialOperator \| DisallowedInRestrictedMode |
| 35 | `Dot` | L186 | `.` | SpecialOperator \| DisallowedInRestrictedMode |
| 36 | `Exclaim` | L189 | `!` | UnaryOperator \| CanConstantFold |
| 37 | `Multiply` | L192 | `*` | BinaryOperator \| BinaryPrecedenceMultiply \| CanConstantFold |
| 38 | `Divide` | L195 | `/` | BinaryOperator \| BinaryPrecedenceMultiply \| CanConstantFold |
| 39 | `Rem` | L198 | `%` | BinaryOperator \| BinaryPrecedenceMultiply \| CanConstantFold |
| 40 | `Plus` | L201 | `+` | BinaryOperator \| BinaryPrecedenceAdd \| UnaryOperator \| CanConstantFold |
| 41 | `Minus` | L204 | `-` | BinaryOperator \| BinaryPrecedenceAdd \| UnaryOperator \| CanConstantFold |
| 42 | `Equals` | L207 | `=` | AssignmentOperator |
| 43 | `PlusEquals` | L210 | `+=` | AssignmentOperator |
| 44 | `MinusEquals` | L213 | `-=` | AssignmentOperator |
| 45 | `MultiplyEquals` | L216 | `*=` | AssignmentOperator |
| 46 | `DivideEquals` | L219 | `/=` | AssignmentOperator |
| 47 | `RemainderEquals` | L222 | `%=` | AssignmentOperator |
| 48 | `Redirection` | L225 | `redirection` | DisallowedInRestrictedMode |
| 49 | `RedirectInStd` | L228 | `<` | ParseModeInvariant \| DisallowedInRestrictedMode |
| 50 | `Format` | L231 | `-f` | BinaryOperator \| BinaryPrecedenceFormat \| DisallowedInRestrictedMode |
| 51 | `Not` | L234 | `-not` | UnaryOperator \| CanConstantFold |
| 52 | `Bnot` | L238 | `-bnot` | UnaryOperator \| CanConstantFold |
| 53 | `And` | L241 | `-and` | BinaryOperator \| BinaryPrecedenceLogical \| CanConstantFold |
| 54 | `Or` | L244 | `-or` | BinaryOperator \| BinaryPrecedenceLogical \| CanConstantFold |
| 55 | `Xor` | L247 | `-xor` | BinaryOperator \| BinaryPrecedenceLogical \| CanConstantFold |
| 56 | `Band` | L250 | `-band` | BinaryOperator \| BinaryPrecedenceBitwise \| CanConstantFold |
| 57 | `Bor` | L254 | `-bor` | BinaryOperator \| BinaryPrecedenceBitwise \| CanConstantFold |
| 58 | `Bxor` | L258 | `-bxor` | BinaryOperator \| BinaryPrecedenceBitwise \| CanConstantFold |
| 59 | `Join` | L261 | `-join` | BinaryOperator \| UnaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 60 | `Ieq` | L265 | `-eq` | BinaryOperator \| BinaryPrecedenceComparison |
| 61 | `Ine` | L269 | `-ne` | BinaryOperator \| BinaryPrecedenceComparison |
| 62 | `Ige` | L273 | `-ge` | BinaryOperator \| BinaryPrecedenceComparison |
| 63 | `Igt` | L277 | `-gt` | BinaryOperator \| BinaryPrecedenceComparison |
| 64 | `Ilt` | L281 | `-lt` | BinaryOperator \| BinaryPrecedenceComparison |
| 65 | `Ile` | L285 | `-le` | BinaryOperator \| BinaryPrecedenceComparison |
| 66 | `Ilike` | L289 | `-ilike` | BinaryOperator \| BinaryPrecedenceComparison |
| 67 | `Inotlike` | L293 | `-inotlike` | BinaryOperator \| BinaryPrecedenceComparison |
| 68 | `Imatch` | L297 | `-imatch` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 69 | `Inotmatch` | L301 | `-inotmatch` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 70 | `Ireplace` | L305 | `-ireplace` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 71 | `Icontains` | L309 | `-icontains` | BinaryOperator \| BinaryPrecedenceComparison |
| 72 | `Inotcontains` | L313 | `-inotcontains` | BinaryOperator \| BinaryPrecedenceComparison |
| 73 | `Iin` | L317 | `-iin` | BinaryOperator \| BinaryPrecedenceComparison |
| 74 | `Inotin` | L321 | `-inotin` | BinaryOperator \| BinaryPrecedenceComparison |
| 75 | `Isplit` | L325 | `-isplit` | BinaryOperator \| UnaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 76 | `Ceq` | L329 | `-ceq` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 77 | `Cne` | L333 | `-cne` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 78 | `Cge` | L337 | `-cge` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 79 | `Cgt` | L341 | `-cgt` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 80 | `Clt` | L345 | `-clt` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 81 | `Cle` | L348 | `-cle` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 82 | `Clike` | L352 | `-clike` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 83 | `Cnotlike` | L356 | `-cnotlike` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 84 | `Cmatch` | L360 | `-cmatch` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator \| DisallowedInRestrictedMode |
| 85 | `Cnotmatch` | L364 | `-cnotmatch` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator \| DisallowedInRestrictedMode |
| 86 | `Creplace` | L368 | `-creplace` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator \| DisallowedInRestrictedMode |
| 87 | `Ccontains` | L372 | `-ccontains` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 88 | `Cnotcontains` | L376 | `-cnotcontains` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 89 | `Cin` | L380 | `-cin` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 90 | `Cnotin` | L384 | `-cnotin` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 91 | `Csplit` | L388 | `-csplit` | BinaryOperator \| UnaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator \| DisallowedInRestrictedMode |
| 92 | `Is` | L391 | `-is` | BinaryOperator \| BinaryPrecedenceComparison |
| 93 | `IsNot` | L394 | `-isnot` | BinaryOperator \| BinaryPrecedenceComparison |
| 94 | `As` | L397 | `-as` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 95 | `PostfixPlusPlus` | L400 | `++` | UnaryOperator \| PrefixOrPostfixOperator \| DisallowedInRestrictedMode |
| 96 | `PostfixMinusMinus` | L403 | `--` | UnaryOperator \| PrefixOrPostfixOperator \| DisallowedInRestrictedMode |
| 97 | `Shl` | L407 | `-shl` | BinaryOperator \| BinaryPrecedenceComparison \| CanConstantFold |
| 98 | `Shr` | L411 | `-shr` | BinaryOperator \| BinaryPrecedenceComparison \| CanConstantFold |
| 99 | `Colon` | L414 | `:` | SpecialOperator \| DisallowedInRestrictedMode |
| 100 | `QuestionMark` | L417 | `?` | TernaryOperator \| DisallowedInRestrictedMode |
| 101 | `QuestionQuestionEquals` | L420 | `??=` | AssignmentOperator |
| 102 | `QuestionQuestion` | L423 | `??` | BinaryOperator \| BinaryPrecedenceCoalesce |
| 103 | `QuestionDot` | L426 | `?.` | SpecialOperator \| DisallowedInRestrictedMode |
| 104 | `QuestionLBracket` | L429 | `?[` | None |
| 105 | *(unnamed: reserved slot)* | — | `` | None |
| 106 | *(unnamed: reserved slot)* | — | `` | None |
| 107 | *(unnamed: reserved slot)* | — | `` | None |
| 108 | *(unnamed: reserved slot)* | — | `` | None |
| 109 | *(unnamed: reserved slot)* | — | `` | None |
| 110 | *(unnamed: reserved slot)* | — | `` | None |
| 111 | *(unnamed: reserved slot)* | — | `` | None |
| 112 | *(unnamed: reserved slot)* | — | `` | None |
| 113 | *(unnamed: reserved slot)* | — | `` | None |
| 114 | *(unnamed: reserved slot)* | — | `` | None |
| 115 | *(unnamed: reserved slot)* | — | `` | None |
| 116 | *(unnamed: reserved slot)* | — | `` | None |
| 117 | *(unnamed: reserved slot)* | — | `` | None |
| 118 | *(unnamed: reserved slot)* | — | `` | None |
| 119 | `Begin` | L436 | `begin` | Keyword \| ScriptBlockBlockName |
| 120 | `Break` | L439 | `break` | Keyword \| StatementDoesntSupportAttributes |
| 121 | `Catch` | L442 | `catch` | Keyword |
| 122 | `Class` | L445 | `class` | Keyword |
| 123 | `Continue` | L448 | `continue` | Keyword \| StatementDoesntSupportAttributes |
| 124 | `Data` | L451 | `data` | Keyword \| StatementDoesntSupportAttributes |
| 125 | `Define` | L454 | `define` | Keyword \| StatementDoesntSupportAttributes |
| 126 | `Do` | L457 | `do` | Keyword \| StatementDoesntSupportAttributes |
| 127 | `Dynamicparam` | L461 | `dynamicparam` | Keyword \| ScriptBlockBlockName |
| 128 | `Else` | L464 | `else` | Keyword |
| 129 | `ElseIf` | L467 | `elseif` | Keyword |
| 130 | `End` | L470 | `end` | Keyword \| ScriptBlockBlockName |
| 131 | `Exit` | L473 | `exit` | Keyword \| StatementDoesntSupportAttributes |
| 132 | `Filter` | L476 | `filter` | Keyword \| StatementDoesntSupportAttributes |
| 133 | `Finally` | L479 | `finally` | Keyword |
| 134 | `For` | L482 | `for` | Keyword \| StatementDoesntSupportAttributes |
| 135 | `Foreach` | L486 | `foreach` | Keyword \| StatementDoesntSupportAttributes |
| 136 | `From` | L489 | `from` | Keyword \| StatementDoesntSupportAttributes |
| 137 | `Function` | L492 | `function` | Keyword \| StatementDoesntSupportAttributes |
| 138 | `If` | L495 | `if` | Keyword \| StatementDoesntSupportAttributes |
| 139 | `In` | L498 | `in` | Keyword |
| 140 | `Param` | L502 | `param` | Keyword |
| 141 | `Process` | L505 | `process` | Keyword \| ScriptBlockBlockName |
| 142 | `Return` | L508 | `return` | Keyword \| StatementDoesntSupportAttributes |
| 143 | `Switch` | L511 | `switch` | Keyword \| StatementDoesntSupportAttributes |
| 144 | `Throw` | L514 | `throw` | Keyword \| StatementDoesntSupportAttributes |
| 145 | `Trap` | L517 | `trap` | Keyword \| StatementDoesntSupportAttributes |
| 146 | `Try` | L520 | `try` | Keyword \| StatementDoesntSupportAttributes |
| 147 | `Until` | L523 | `until` | Keyword |
| 148 | `Using` | L526 | `using` | Keyword \| StatementDoesntSupportAttributes |
| 149 | `Var` | L529 | `var` | Keyword \| StatementDoesntSupportAttributes |
| 150 | `While` | L532 | `while` | Keyword \| StatementDoesntSupportAttributes |
| 151 | `Workflow` | L535 | `workflow` | Keyword \| StatementDoesntSupportAttributes |
| 152 | `Parallel` | L538 | `parallel` | Keyword \| StatementDoesntSupportAttributes |
| 153 | `Sequence` | L541 | `sequence` | Keyword \| StatementDoesntSupportAttributes |
| 154 | `InlineScript` | L544 | `inlinescript` | Keyword \| StatementDoesntSupportAttributes |
| 155 | `Configuration` | L547 | `configuration` | Keyword |
| 156 | `DynamicKeyword` | L550 | `<dynamic keyword>` | Keyword |
| 157 | `Public` | L553 | `public` | Keyword |
| 158 | `Private` | L556 | `private` | Keyword |
| 159 | `Static` | L559 | `static` | Keyword |
| 160 | `Interface` | L562 | `interface` | Keyword |
| 161 | `Enum` | L565 | `enum` | Keyword |
| 162 | `Namespace` | L568 | `namespace` | Keyword |
| 163 | `Module` | L571 | `module` | Keyword |
| 164 | `Type` | L574 | `type` | Keyword |
| 165 | `Assembly` | L577 | `assembly` | Keyword |
| 166 | `Command` | L580 | `command` | Keyword |
| 167 | `Hidden` | L583 | `hidden` | Keyword |
| 168 | `Base` | L586 | `base` | Keyword |
| 169 | `Default` | L589 | `default` | Keyword |
| 170 | `Clean` | L592 | `clean` | Keyword \| ScriptBlockBlockName |

## 4. TokenFlags (every member) [SPEC]

| Name | Value | Source line |
|---|---|---:|
| `None` | `0x00000000` | L606 |
| `BinaryPrecedenceLogical` | `0x1` | L613 |
| `BinaryPrecedenceBitwise` | `0x2` | L618 |
| `BinaryPrecedenceComparison` | `0x5` | L625 |
| `BinaryPrecedenceCoalesce` | `0x7` | L630 |
| `BinaryPrecedenceAdd` | `0x9` | L635 |
| `BinaryPrecedenceMultiply` | `0xa` | L640 |
| `BinaryPrecedenceFormat` | `0xc` | L645 |
| `BinaryPrecedenceRange` | `0xd` | L650 |
| `BinaryPrecedenceMask` | `0x0000000f` | L657 |
| `Keyword` | `0x00000010` | L662 |
| `ScriptBlockBlockName` | `0x00000020` | L667 |
| `BinaryOperator` | `0x00000100` | L672 |
| `UnaryOperator` | `0x00000200` | L677 |
| `CaseSensitiveOperator` | `0x00000400` | L682 |
| `TernaryOperator` | `0x00000800` | L687 |
| `SpecialOperator` | `0x00001000` | L692 |
| `AssignmentOperator` | `0x00002000` | L697 |
| `ParseModeInvariant` | `0x00008000` | L702 |
| `TokenInError` | `0x00010000` | L707 |
| `DisallowedInRestrictedMode` | `0x00020000` | L712 |
| `PrefixOrPostfixOperator` | `0x00040000` | L717 |
| `CommandName` | `0x00080000` | L722 |
| `MemberName` | `0x00100000` | L727 |
| `TypeName` | `0x00200000` | L732 |
| `AttributeName` | `0x00400000` | L737 |
| `CanConstantFold` | `0x00800000` | L746 |
| `StatementDoesntSupportAttributes` | `0x01000000` | L751 |

## 5. Keywords (`Tokenizer.s_keywordText` / `s_keywordTokenKind`) [SPEC]

Parallel arrays; recognition is case-insensitive (`s_keywordTable` is built with `OrdinalIgnoreCase`, see [02.1-tokenizer.md](02.1-tokenizer.md) §6). `inlinescript` is only a keyword inside a workflow context.

| # | Spelling | TokenKind | Static flags of the kind |
|---:|---|---|---|
| 1 | `elseif` | `ElseIf` | Keyword |
| 2 | `if` | `If` | Keyword \| StatementDoesntSupportAttributes |
| 3 | `else` | `Else` | Keyword |
| 4 | `switch` | `Switch` | Keyword \| StatementDoesntSupportAttributes |
| 5 | `foreach` | `Foreach` | Keyword \| StatementDoesntSupportAttributes |
| 6 | `from` | `From` | Keyword \| StatementDoesntSupportAttributes |
| 7 | `in` | `In` | Keyword |
| 8 | `for` | `For` | Keyword \| StatementDoesntSupportAttributes |
| 9 | `while` | `While` | Keyword \| StatementDoesntSupportAttributes |
| 10 | `until` | `Until` | Keyword |
| 11 | `do` | `Do` | Keyword \| StatementDoesntSupportAttributes |
| 12 | `try` | `Try` | Keyword \| StatementDoesntSupportAttributes |
| 13 | `catch` | `Catch` | Keyword |
| 14 | `finally` | `Finally` | Keyword |
| 15 | `trap` | `Trap` | Keyword \| StatementDoesntSupportAttributes |
| 16 | `data` | `Data` | Keyword \| StatementDoesntSupportAttributes |
| 17 | `return` | `Return` | Keyword \| StatementDoesntSupportAttributes |
| 18 | `continue` | `Continue` | Keyword \| StatementDoesntSupportAttributes |
| 19 | `break` | `Break` | Keyword \| StatementDoesntSupportAttributes |
| 20 | `exit` | `Exit` | Keyword \| StatementDoesntSupportAttributes |
| 21 | `throw` | `Throw` | Keyword \| StatementDoesntSupportAttributes |
| 22 | `begin` | `Begin` | Keyword \| ScriptBlockBlockName |
| 23 | `process` | `Process` | Keyword \| ScriptBlockBlockName |
| 24 | `end` | `End` | Keyword \| ScriptBlockBlockName |
| 25 | `dynamicparam` | `Dynamicparam` | Keyword \| ScriptBlockBlockName |
| 26 | `function` | `Function` | Keyword \| StatementDoesntSupportAttributes |
| 27 | `filter` | `Filter` | Keyword \| StatementDoesntSupportAttributes |
| 28 | `param` | `Param` | Keyword |
| 29 | `class` | `Class` | Keyword |
| 30 | `define` | `Define` | Keyword \| StatementDoesntSupportAttributes |
| 31 | `var` | `Var` | Keyword \| StatementDoesntSupportAttributes |
| 32 | `using` | `Using` | Keyword \| StatementDoesntSupportAttributes |
| 33 | `workflow` | `Workflow` | Keyword \| StatementDoesntSupportAttributes |
| 34 | `parallel` | `Parallel` | Keyword \| StatementDoesntSupportAttributes |
| 35 | `sequence` | `Sequence` | Keyword \| StatementDoesntSupportAttributes |
| 36 | `inlinescript` | `InlineScript` | Keyword \| StatementDoesntSupportAttributes |
| 37 | `configuration` | `Configuration` | Keyword |
| 38 | `public` | `Public` | Keyword |
| 39 | `private` | `Private` | Keyword |
| 40 | `static` | `Static` | Keyword |
| 41 | `interface` | `Interface` | Keyword |
| 42 | `enum` | `Enum` | Keyword |
| 43 | `namespace` | `Namespace` | Keyword |
| 44 | `module` | `Module` | Keyword |
| 45 | `type` | `Type` | Keyword |
| 46 | `assembly` | `Assembly` | Keyword |
| 47 | `command` | `Command` | Keyword |
| 48 | `hidden` | `Hidden` | Keyword |
| 49 | `base` | `Base` | Keyword |
| 50 | `default` | `Default` | Keyword |
| 51 | `clean` | `Clean` | Keyword \| ScriptBlockBlockName |

Keyword rows: **<!--N:TOKENIZER_KEYWORD_ROWS-->51<!--/N-->** (`GENERATED`). `TokenKind.DynamicKeyword` has no row; dynamic (DSC) keywords come from `DynamicKeyword.DynamicKeywords`.

## 6. Dash operators (`Tokenizer._operatorText` / `s_operatorTokenKind`) [SPEC]

Spelling is stored **without** the leading dash. Recognition happens only in expression mode (see [02.1-tokenizer.md](02.1-tokenizer.md) §6.4).

| # | Spelling | TokenKind | Static flags of the kind |
|---:|---|---|---|
| 1 | `-bnot` | `Bnot` | UnaryOperator \| CanConstantFold |
| 2 | `-not` | `Not` | UnaryOperator \| CanConstantFold |
| 3 | `-eq` | `Ieq` | BinaryOperator \| BinaryPrecedenceComparison |
| 4 | `-ieq` | `Ieq` | BinaryOperator \| BinaryPrecedenceComparison |
| 5 | `-ceq` | `Ceq` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 6 | `-ne` | `Ine` | BinaryOperator \| BinaryPrecedenceComparison |
| 7 | `-ine` | `Ine` | BinaryOperator \| BinaryPrecedenceComparison |
| 8 | `-cne` | `Cne` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 9 | `-ge` | `Ige` | BinaryOperator \| BinaryPrecedenceComparison |
| 10 | `-ige` | `Ige` | BinaryOperator \| BinaryPrecedenceComparison |
| 11 | `-cge` | `Cge` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 12 | `-gt` | `Igt` | BinaryOperator \| BinaryPrecedenceComparison |
| 13 | `-igt` | `Igt` | BinaryOperator \| BinaryPrecedenceComparison |
| 14 | `-cgt` | `Cgt` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 15 | `-lt` | `Ilt` | BinaryOperator \| BinaryPrecedenceComparison |
| 16 | `-ilt` | `Ilt` | BinaryOperator \| BinaryPrecedenceComparison |
| 17 | `-clt` | `Clt` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 18 | `-le` | `Ile` | BinaryOperator \| BinaryPrecedenceComparison |
| 19 | `-ile` | `Ile` | BinaryOperator \| BinaryPrecedenceComparison |
| 20 | `-cle` | `Cle` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 21 | `-like` | `Ilike` | BinaryOperator \| BinaryPrecedenceComparison |
| 22 | `-ilike` | `Ilike` | BinaryOperator \| BinaryPrecedenceComparison |
| 23 | `-clike` | `Clike` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 24 | `-notlike` | `Inotlike` | BinaryOperator \| BinaryPrecedenceComparison |
| 25 | `-inotlike` | `Inotlike` | BinaryOperator \| BinaryPrecedenceComparison |
| 26 | `-cnotlike` | `Cnotlike` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 27 | `-match` | `Imatch` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 28 | `-imatch` | `Imatch` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 29 | `-cmatch` | `Cmatch` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator \| DisallowedInRestrictedMode |
| 30 | `-notmatch` | `Inotmatch` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 31 | `-inotmatch` | `Inotmatch` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 32 | `-cnotmatch` | `Cnotmatch` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator \| DisallowedInRestrictedMode |
| 33 | `-replace` | `Ireplace` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 34 | `-ireplace` | `Ireplace` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 35 | `-creplace` | `Creplace` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator \| DisallowedInRestrictedMode |
| 36 | `-contains` | `Icontains` | BinaryOperator \| BinaryPrecedenceComparison |
| 37 | `-icontains` | `Icontains` | BinaryOperator \| BinaryPrecedenceComparison |
| 38 | `-ccontains` | `Ccontains` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 39 | `-notcontains` | `Inotcontains` | BinaryOperator \| BinaryPrecedenceComparison |
| 40 | `-inotcontains` | `Inotcontains` | BinaryOperator \| BinaryPrecedenceComparison |
| 41 | `-cnotcontains` | `Cnotcontains` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 42 | `-in` | `Iin` | BinaryOperator \| BinaryPrecedenceComparison |
| 43 | `-iin` | `Iin` | BinaryOperator \| BinaryPrecedenceComparison |
| 44 | `-cin` | `Cin` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 45 | `-notin` | `Inotin` | BinaryOperator \| BinaryPrecedenceComparison |
| 46 | `-inotin` | `Inotin` | BinaryOperator \| BinaryPrecedenceComparison |
| 47 | `-cnotin` | `Cnotin` | BinaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator |
| 48 | `-split` | `Isplit` | BinaryOperator \| UnaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 49 | `-isplit` | `Isplit` | BinaryOperator \| UnaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 50 | `-csplit` | `Csplit` | BinaryOperator \| UnaryOperator \| BinaryPrecedenceComparison \| CaseSensitiveOperator \| DisallowedInRestrictedMode |
| 51 | `-isnot` | `IsNot` | BinaryOperator \| BinaryPrecedenceComparison |
| 52 | `-is` | `Is` | BinaryOperator \| BinaryPrecedenceComparison |
| 53 | `-as` | `As` | BinaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 54 | `-f` | `Format` | BinaryOperator \| BinaryPrecedenceFormat \| DisallowedInRestrictedMode |
| 55 | `-and` | `And` | BinaryOperator \| BinaryPrecedenceLogical \| CanConstantFold |
| 56 | `-band` | `Band` | BinaryOperator \| BinaryPrecedenceBitwise \| CanConstantFold |
| 57 | `-or` | `Or` | BinaryOperator \| BinaryPrecedenceLogical \| CanConstantFold |
| 58 | `-bor` | `Bor` | BinaryOperator \| BinaryPrecedenceBitwise \| CanConstantFold |
| 59 | `-xor` | `Xor` | BinaryOperator \| BinaryPrecedenceLogical \| CanConstantFold |
| 60 | `-bxor` | `Bxor` | BinaryOperator \| BinaryPrecedenceBitwise \| CanConstantFold |
| 61 | `-join` | `Join` | BinaryOperator \| UnaryOperator \| BinaryPrecedenceComparison \| DisallowedInRestrictedMode |
| 62 | `-shl` | `Shl` | BinaryOperator \| BinaryPrecedenceComparison \| CanConstantFold |
| 63 | `-shr` | `Shr` | BinaryOperator \| BinaryPrecedenceComparison \| CanConstantFold |

Dash-operator rows: **<!--N:TOKENIZER_DASH_OPERATOR_ROWS-->63<!--/N-->** (`GENERATED`).

## 7. CharTraits (character-class bits) [SPEC]

| Name | Value | Source line |
|---|---|---:|
| `None` | `0x0000` | L33 |
| `IdentifierStart` | `0x0002` | L38 |
| `MultiplierStart` | `0x0004` | L43 |
| `TypeSuffix` | `0x0008` | L48 |
| `Whitespace` | `0x0010` | L53 |
| `Newline` | `0x0020` | L58 |
| `HexDigit` | `0x0040` | L63 |
| `Digit` | `0x0080` | L68 |
| `VarNameFirst` | `0x0100` | L73 |
| `ForceStartNewToken` | `0x0200` | L78 |
| `ForceStartNewAssemblyNameSpecToken` | `0x0400` | L83 |
| `ForceStartNewTokenAfterNumber` | `0x0800` | L88 |

## 8. NumberSuffixFlags and NumberFormat [SPEC]

| Name | Value | Source line |
|---|---|---:|
| `None` | `0x0` | L506 |
| `Unsigned` | `0x1` | L511 |
| `SignedByte` | `0x2` | L516 |
| `UnsignedByte` | `0x3` | L522 |
| `Short` | `0x4` | L527 |
| `UnsignedShort` | `0x5` | L533 |
| `Long` | `0x8` | L538 |
| `UnsignedLong` | `0x9` | L544 |
| `Decimal` | `0x10` | L549 |
| `BigInteger` | `0x20` | L554 |

| NumberFormat | Value | Source line |
|---|---|---:|
| `Decimal` | `0x0` | L565 |
| `Hex` | `0x1` | L570 |
| `Binary` | `0x2` | L575 |

## 9. TokenizerMode [SPEC]

| Name | Source line |
|---|---:|
| `Command` | L491 |
| `Expression` | L492 |
| `TypeName` | L493 |
| `Signature` | L494 |

## 10. Cross-document links

Narrative, mode-transition table and lexical rules: [02.1-tokenizer.md](02.1-tokenizer.md). Parser consumers of each kind: [02.2-parser.md](02.2-parser.md) (planned, T22). Token subclasses: [02.1-tokenizer.md](02.1-tokenizer.md) §4.


Verification: row counts asserted equal to the `TokenKind` value range (171) and to `data/numbers.json` keys `TOKENKIND_MEMBERS`, `TOKENFLAGS_MEMBERS`; keyword and operator arrays asserted pairwise equal length (`gen_T21.py`). Static-flag and text arrays were also read in the source windows recorded in `.work/notes/` (token.cs W3-W4).

