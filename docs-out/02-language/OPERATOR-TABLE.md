---
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

## 1. Purpose and scope [SPEC]

One table for every operator token kind: spelling, role, precedence level, associativity, whether the compiler may fold it at compile time, and how it is evaluated. The precedence rule is canonical fact CF-OP-001 (stated in §3).

## 2. Source map

| path | role |
|---|---|
| `src/System.Management.Automation/engine/parser/token.cs::TokenFlags@L601-L752` | precedence and operator-class flags |
| `src/System.Management.Automation/engine/parser/Parser.cs::Parser.BinaryExpressionRule@L6798-L6950` | precedence climbing |
| `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder@L2119-L3422` | binary operation semantics |
| `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSUnaryOperationBinder@L3427-L3738` | unary operation semantics |
| `src/System.Management.Automation/engine/lang/parserutils.cs::ParserOps@L232-L1760` | `-like`, `-match`, `-replace`, `-split`, `-join`, range helpers |

## 3. Precedence and associativity (CF-OP-001)

<!--CF:CF-OP-001-->**Operator precedence and associativity.** Binary operators are parsed by precedence climbing and **all are left-associative**; from lowest to highest precedence the levels are: logical (`-and`, `-or`, `-xor`) = 1; bitwise (`-band`, `-bor`, `-bxor`) = 2; comparison group (all `-eq`/`-ne`/`-gt`/`-ge`/`-lt`/`-le`, `-like`, `-match`, `-replace`, `-contains`, `-in` families with their `i`/`c` variants, `-is`, `-isnot`, `-as`, `-split`, `-join`, `-shl`, `-shr`) = 5; null-coalescing `??` = 7; additive (`+`, `-`) = 9; multiplicative (`*`, `/`, `%`) = 10; format `-f` = 12; range `..` = 13. The comma (array-literal) operator binds tighter than every binary operator; the unary operators, casts and `++`/`--` bind tighter than the comma; the ternary `?:` (right-nested) and assignment (`=`, `+=`, `-=`, `*=`, `/=`, `%=`, `??=`, parsed at statement level with a statement on the right) bind looser than all binary operators; `&&` and `||` chain pipelines and are not expression operators. Operators spelled with a leading dash are recognized as operators only when the tokenizer is in expression mode.<!--/CF-->

Evidence: `src/System.Management.Automation/engine/parser/Parser.cs::Parser.BinaryExpressionRule@L6798-L6950` (reduce while new precedence is less than or equal), `src/System.Management.Automation/engine/parser/token.cs::TokenFlags@L601-L752` (level values), `Parser.ArrayLiteralRule@L6975-L7021`, `Parser.UnaryExpressionRule@L7029-L7226`, `Parser.ExpressionRule@L6696-L6790`, `Parser.PipelineChainRule@L5773-L5988`.

## 4. Operator table

Level = `BinaryPrecedence*` value (higher binds tighter); `fold` = the operator may be constant-folded; `restricted` = flagged `DisallowedInRestrictedMode`. Case: `i`-prefixed and plain forms ignore case, `c`-prefixed forms are case-sensitive (token texts of `i` forms are listed without the `i` for most operators, see [TOKEN-CATALOG.md](TOKEN-CATALOG.md) §3).

| TokenKind | Text | Class | Level | Associativity | fold | restricted | Evaluation | Behavior (FACT-SRC) |
|---|---|---|---:|---|---|---|---|---|
| `And` | `-and` | Binary | 1 | left | yes |  | AndAlso/OrElse over bool conversions (-and, -or); NotEqual over two bools (-xor) | operands converted with PowerShell truthiness (IsTrue); -and/-or short-circuit; -xor evaluates both |
| `Or` | `-or` | Binary | 1 | left | yes |  | AndAlso/OrElse over bool conversions (-and, -or); NotEqual over two bools (-xor) | operands converted with PowerShell truthiness (IsTrue); -and/-or short-circuit; -xor evaluates both |
| `Xor` | `-xor` | Binary | 1 | left | yes |  | AndAlso/OrElse over bool conversions (-and, -or); NotEqual over two bools (-xor) | operands converted with PowerShell truthiness (IsTrue); -and/-or short-circuit; -xor evaluates both |
| `Band` | `-band` | Binary | 2 | left | yes |  | Dynamic site PSBinaryOperationBinder(And/Or/ExclusiveOr) | integer bitwise operation on int, uint, long or ulong chosen from the wider operand |
| `Bor` | `-bor` | Binary | 2 | left | yes |  | Dynamic site PSBinaryOperationBinder(And/Or/ExclusiveOr) | integer bitwise operation on int, uint, long or ulong chosen from the wider operand |
| `Bxor` | `-bxor` | Binary | 2 | left | yes |  | Dynamic site PSBinaryOperationBinder(And/Or/ExclusiveOr) | integer bitwise operation on int, uint, long or ulong chosen from the wider operand |
| `As` | `-as` | Binary | 5 | left |  | yes | TypeOps.AsOperator | converts or returns $null |
| `Ccontains` | `-ccontains` | Binary | 5 | left |  |  | GenerateCallContains: ParserOps.ContainsOperatorCompiled with enumerator site and Equal binary site (scalar compare) | collection membership by PowerShell equality; -in/-notin swap the operands; -notcontains/-notin negate |
| `Ceq` | `-ceq` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(Equal/NotEqual) with ignore-case flag (i-variants and the plain operator ignore case, c-variants do not) | null handling; enumerable left operand filters (returns matching elements) unless scalar compare; string left operand: ordinal-culture string compare with right operand converted to string; char left operand ignoring case; numeric compare; otherwise Equals, then Equals after converting the right operand to the left operand's type (an InvalidCast gives false) |
| `Cge` | `-cge` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(GreaterThan/LessThan/...) with ignore-case flag | same dispatch as equality; non-numeric left operands use LanguagePrimitives.Compare (right operand converted to the left type; left operand must be comparable) |
| `Cgt` | `-cgt` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(GreaterThan/LessThan/...) with ignore-case flag | same dispatch as equality; non-numeric left operands use LanguagePrimitives.Compare (right operand converted to the left type; left operand must be comparable) |
| `Cin` | `-cin` | Binary | 5 | left |  |  | GenerateCallContains: ParserOps.ContainsOperatorCompiled with enumerator site and Equal binary site (scalar compare) | collection membership by PowerShell equality; -in/-notin swap the operands; -notcontains/-notin negate |
| `Cle` | `-cle` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(GreaterThan/LessThan/...) with ignore-case flag | same dispatch as equality; non-numeric left operands use LanguagePrimitives.Compare (right operand converted to the left type; left operand must be comparable) |
| `Clike` | `-clike` | Binary | 5 | left |  |  | ParserOps.LikeOperator(context, position, left, right, operator) | wildcard match; array left operand filters; constant right operand pre-built to a WildcardPattern |
| `Clt` | `-clt` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(GreaterThan/LessThan/...) with ignore-case flag | same dispatch as equality; non-numeric left operands use LanguagePrimitives.Compare (right operand converted to the left type; left operand must be comparable) |
| `Cmatch` | `-cmatch` | Binary | 5 | left |  | yes | ParserOps.MatchOperator(context, position, left, right, notMatch, ignoreCase) | regex match; scalar left operand sets $Matches (hashtable, case-insensitive keys; numeric group names become int keys); array left operand filters elements |
| `Cne` | `-cne` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(Equal/NotEqual) with ignore-case flag (i-variants and the plain operator ignore case, c-variants do not) | null handling; enumerable left operand filters (returns matching elements) unless scalar compare; string left operand: ordinal-culture string compare with right operand converted to string; char left operand ignoring case; numeric compare; otherwise Equals, then Equals after converting the right operand to the left operand's type (an InvalidCast gives false) |
| `Cnotcontains` | `-cnotcontains` | Binary | 5 | left |  |  | GenerateCallContains: ParserOps.ContainsOperatorCompiled with enumerator site and Equal binary site (scalar compare) | collection membership by PowerShell equality; -in/-notin swap the operands; -notcontains/-notin negate |
| `Cnotin` | `-cnotin` | Binary | 5 | left |  |  | GenerateCallContains: ParserOps.ContainsOperatorCompiled with enumerator site and Equal binary site (scalar compare) | collection membership by PowerShell equality; -in/-notin swap the operands; -notcontains/-notin negate |
| `Cnotlike` | `-cnotlike` | Binary | 5 | left |  |  | ParserOps.LikeOperator(context, position, left, right, operator) | wildcard match; array left operand filters; constant right operand pre-built to a WildcardPattern |
| `Cnotmatch` | `-cnotmatch` | Binary | 5 | left |  | yes | ParserOps.MatchOperator(context, position, left, right, notMatch, ignoreCase) | regex match; scalar left operand sets $Matches (hashtable, case-insensitive keys; numeric group names become int keys); array left operand filters elements |
| `Creplace` | `-creplace` | Binary | 5 | left |  | yes | ParserOps.ReplaceOperator(context, position, left, right, ignoreCase) | right operand is an array of 1..2 elements (pattern, replacement); replacement string or script block (MatchEvaluator); more than 2 elements is an error |
| `Csplit` | `-csplit` | Binary/Unary | 5 | left |  | yes | ParserOps.SplitOperator / UnarySplitOperator(context, position, left, right, ignoreCase) | regex split by default (SimpleMatch option for literal); optional limit and options; predicate script block form; unary form splits on whitespace |
| `Icontains` | `-icontains` | Binary | 5 | left |  |  | GenerateCallContains: ParserOps.ContainsOperatorCompiled with enumerator site and Equal binary site (scalar compare) | collection membership by PowerShell equality; -in/-notin swap the operands; -notcontains/-notin negate |
| `Ieq` | `-eq` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(Equal/NotEqual) with ignore-case flag (i-variants and the plain operator ignore case, c-variants do not) | null handling; enumerable left operand filters (returns matching elements) unless scalar compare; string left operand: ordinal-culture string compare with right operand converted to string; char left operand ignoring case; numeric compare; otherwise Equals, then Equals after converting the right operand to the left operand's type (an InvalidCast gives false) |
| `Ige` | `-ge` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(GreaterThan/LessThan/...) with ignore-case flag | same dispatch as equality; non-numeric left operands use LanguagePrimitives.Compare (right operand converted to the left type; left operand must be comparable) |
| `Igt` | `-gt` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(GreaterThan/LessThan/...) with ignore-case flag | same dispatch as equality; non-numeric left operands use LanguagePrimitives.Compare (right operand converted to the left type; left operand must be comparable) |
| `Iin` | `-iin` | Binary | 5 | left |  |  | GenerateCallContains: ParserOps.ContainsOperatorCompiled with enumerator site and Equal binary site (scalar compare) | collection membership by PowerShell equality; -in/-notin swap the operands; -notcontains/-notin negate |
| `Ile` | `-le` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(GreaterThan/LessThan/...) with ignore-case flag | same dispatch as equality; non-numeric left operands use LanguagePrimitives.Compare (right operand converted to the left type; left operand must be comparable) |
| `Ilike` | `-ilike` | Binary | 5 | left |  |  | ParserOps.LikeOperator(context, position, left, right, operator) | wildcard match; array left operand filters; constant right operand pre-built to a WildcardPattern |
| `Ilt` | `-lt` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(GreaterThan/LessThan/...) with ignore-case flag | same dispatch as equality; non-numeric left operands use LanguagePrimitives.Compare (right operand converted to the left type; left operand must be comparable) |
| `Imatch` | `-imatch` | Binary | 5 | left |  | yes | ParserOps.MatchOperator(context, position, left, right, notMatch, ignoreCase) | regex match; scalar left operand sets $Matches (hashtable, case-insensitive keys; numeric group names become int keys); array left operand filters elements |
| `Ine` | `-ne` | Binary | 5 | left |  |  | Dynamic site PSBinaryOperationBinder(Equal/NotEqual) with ignore-case flag (i-variants and the plain operator ignore case, c-variants do not) | null handling; enumerable left operand filters (returns matching elements) unless scalar compare; string left operand: ordinal-culture string compare with right operand converted to string; char left operand ignoring case; numeric compare; otherwise Equals, then Equals after converting the right operand to the left operand's type (an InvalidCast gives false) |
| `Inotcontains` | `-inotcontains` | Binary | 5 | left |  |  | GenerateCallContains: ParserOps.ContainsOperatorCompiled with enumerator site and Equal binary site (scalar compare) | collection membership by PowerShell equality; -in/-notin swap the operands; -notcontains/-notin negate |
| `Inotin` | `-inotin` | Binary | 5 | left |  |  | GenerateCallContains: ParserOps.ContainsOperatorCompiled with enumerator site and Equal binary site (scalar compare) | collection membership by PowerShell equality; -in/-notin swap the operands; -notcontains/-notin negate |
| `Inotlike` | `-inotlike` | Binary | 5 | left |  |  | ParserOps.LikeOperator(context, position, left, right, operator) | wildcard match; array left operand filters; constant right operand pre-built to a WildcardPattern |
| `Inotmatch` | `-inotmatch` | Binary | 5 | left |  | yes | ParserOps.MatchOperator(context, position, left, right, notMatch, ignoreCase) | regex match; scalar left operand sets $Matches (hashtable, case-insensitive keys; numeric group names become int keys); array left operand filters elements |
| `Ireplace` | `-ireplace` | Binary | 5 | left |  | yes | ParserOps.ReplaceOperator(context, position, left, right, ignoreCase) | right operand is an array of 1..2 elements (pattern, replacement); replacement string or script block (MatchEvaluator); more than 2 elements is an error |
| `Is` | `-is` | Binary | 5 | left |  |  | TypeOps.IsInstance / TypeIs on the base object; -isnot negates | right operand is a type; PSObject/PSCustomObject special cases |
| `IsNot` | `-isnot` | Binary | 5 | left |  |  | TypeOps.IsInstance / TypeIs on the base object; -isnot negates | right operand is a type; PSObject/PSCustomObject special cases |
| `Isplit` | `-isplit` | Binary/Unary | 5 | left |  | yes | ParserOps.SplitOperator / UnarySplitOperator(context, position, left, right, ignoreCase) | regex split by default (SimpleMatch option for literal); optional limit and options; predicate script block form; unary form splits on whitespace |
| `Join` | `-join` | Binary/Unary | 5 | left |  | yes | ParserOps.JoinOperator / UnaryJoinOperator(context, position, left, right) | joins elements converted to strings with the separator; unary form joins with an empty separator |
| `Shl` | `-shl` | Binary | 5 | left | yes |  | Dynamic site PSBinaryOperationBinder(LeftShift/RightShift) | integer shift; operand type int, uint, long or ulong chosen from the wider operand |
| `Shr` | `-shr` | Binary | 5 | left | yes |  | Dynamic site PSBinaryOperationBinder(LeftShift/RightShift) | integer shift; operand type int, uint, long or ulong chosen from the wider operand |
| `QuestionQuestion` | `??` | Binary | 7 | left |  |  | Compiler.Coalesce helper | left operand unless it is $null |
| `Minus` | `-` | Binary/Unary | 9 | left | yes |  | Dynamic site PSBinaryOperationBinder(Subtract) | numeric (wider type, overflow to double); string left operand converted to number; otherwise op_Subtraction |
| `Plus` | `+` | Binary/Unary | 9 | left | yes |  | Dynamic site PSBinaryOperationBinder(Add) (double,double: native add) | null + x gives x; numeric + numeric uses the wider type with overflow to double; numeric + string converts the string to a number (Parser.ScanNumber); string + any (and char + any) concatenates using the right operand's string form; array/enumerable + x appends (array concatenation); hashtable + hashtable merges, hashtable + other is an error; otherwise a user-defined op_Addition |
| `Divide` | `/` | Binary | 10 | left | yes |  | Dynamic site PSBinaryOperationBinder(Divide) | null / x treats null as 0; int/int gives an int when the division is exact, otherwise a double; division by zero raises a RuntimeException; string operands converted to numbers; otherwise op_Division |
| `Multiply` | `*` | Binary | 10 | left | yes |  | Dynamic site PSBinaryOperationBinder(Multiply) | null * x is null; numeric; numeric * string converts the string; string * n repeats the string; array/enumerable * n repeats the elements; otherwise op_Multiply |
| `Rem` | `%` | Binary | 10 | left | yes |  | Dynamic site PSBinaryOperationBinder(Modulo) | null % x treats null as 0; integer remainder; remainder by zero raises a RuntimeException; otherwise op_Modulus |
| `Format` | `-f` | Binary | 12 | left |  | yes | StringOps.FormatOperator(format string, argument) | string.Format with the right operand as arguments (array elements spread) |
| `DotDot` | `..` | Binary | 13 | left |  | yes | ParserOps.RangeOperator / range enumerator | integer ranges up and down; single-character operands give a character range |
| `Ampersand` | `&` | Special | — | — |  |  | Parser/tokenizer level | member access, static member access, invocation/call/dot-source; no expression-tree operator |
| `Bnot` | `-bnot` | Unary | — | — | yes |  | Dynamic site PSUnaryOperationBinder(OnesComplement) | integer bitwise complement |
| `Colon` | `:` | Special | — | — |  | yes | Parser/tokenizer level | member access, static member access, invocation/call/dot-source; no expression-tree operator |
| `ColonColon` | `::` | Special | — | — |  | yes | Parser/tokenizer level | member access, static member access, invocation/call/dot-source; no expression-tree operator |
| `Comma` | `,` | Unary | — | — |  |  | Parser/tokenizer level | member access, static member access, invocation/call/dot-source; no expression-tree operator |
| `DivideEquals` | `/=` | Assignment | — | — |  |  | CompileAssignment / ReduceAssignment | = stores; op= applies the dynamic binary operation to the current value then stores; ??= stores only when the current value is $null |
| `Dot` | `.` | Special | — | — |  | yes | Parser/tokenizer level | member access, static member access, invocation/call/dot-source; no expression-tree operator |
| `Equals` | `=` | Assignment | — | — |  |  | CompileAssignment / ReduceAssignment | = stores; op= applies the dynamic binary operation to the current value then stores; ??= stores only when the current value is $null |
| `Exclaim` | `!` | Unary | — | — | yes |  | Dynamic site PSUnaryOperationBinder(Not) | logical negation of truthiness |
| `MinusEquals` | `-=` | Assignment | — | — |  |  | CompileAssignment / ReduceAssignment | = stores; op= applies the dynamic binary operation to the current value then stores; ??= stores only when the current value is $null |
| `MinusMinus` | `--` | Unary/PrefixOrPostfix | — | — |  | yes | Compiler.CompileIncrementOrDecrement via IAssignableValue | prefix returns the new value; postfix returns the old value (null postfix result is 0); needs an assignable operand |
| `MultiplyEquals` | `*=` | Assignment | — | — |  |  | CompileAssignment / ReduceAssignment | = stores; op= applies the dynamic binary operation to the current value then stores; ??= stores only when the current value is $null |
| `Not` | `-not` | Unary | — | — | yes |  | Dynamic site PSUnaryOperationBinder(Not) | logical negation of truthiness |
| `Pipe` | `|` | Special | — | — |  |  | Parser/tokenizer level | member access, static member access, invocation/call/dot-source; no expression-tree operator |
| `PlusEquals` | `+=` | Assignment | — | — |  |  | CompileAssignment / ReduceAssignment | = stores; op= applies the dynamic binary operation to the current value then stores; ??= stores only when the current value is $null |
| `PlusPlus` | `++` | Unary/PrefixOrPostfix | — | — |  | yes | Compiler.CompileIncrementOrDecrement via IAssignableValue | prefix returns the new value; postfix returns the old value (null postfix result is 0); needs an assignable operand |
| `PostfixMinusMinus` | `--` | Unary/PrefixOrPostfix | — | — |  | yes | Compiler.CompileIncrementOrDecrement via IAssignableValue | prefix returns the new value; postfix returns the old value (null postfix result is 0); needs an assignable operand |
| `PostfixPlusPlus` | `++` | Unary/PrefixOrPostfix | — | — |  | yes | Compiler.CompileIncrementOrDecrement via IAssignableValue | prefix returns the new value; postfix returns the old value (null postfix result is 0); needs an assignable operand |
| `QuestionDot` | `?.` | Special | — | — |  | yes | Parser/tokenizer level | member access, static member access, invocation/call/dot-source; no expression-tree operator |
| `QuestionQuestionEquals` | `??=` | Assignment | — | — |  |  | CompileAssignment / ReduceAssignment | = stores; op= applies the dynamic binary operation to the current value then stores; ??= stores only when the current value is $null |
| `RedirectInStd` | `<` | other | — | — |  | yes | Redirection objects (FileRedirection, MergingRedirection) | stream redirection, not an expression operator |
| `Redirection` | `redirection` | other | — | — |  | yes | Redirection objects (FileRedirection, MergingRedirection) | stream redirection, not an expression operator |
| `RemainderEquals` | `%=` | Assignment | — | — |  |  | CompileAssignment / ReduceAssignment | = stores; op= applies the dynamic binary operation to the current value then stores; ??= stores only when the current value is $null |

Rows: **<!--N:OPERATOR_KINDS-->75<!--/N-->** (`GENERATED`). Kinds without annotation: none.

## 5. Notes

- **Left-operand driven.** For binary operators the left operand's runtime type selects the rule; the right operand is converted to it where needed. `1 + "2"` is 3, `"1" + 2` is `"12"` (string concatenation).
- **`-eq`/`-ne` with arrays.** A collection on the left filters (returns matching elements); a `$null` on the left of `-eq` returns `$true` only for `$null`.
- **Constant folding** only for operators with the `CanConstantFold` flag; operators depending on execution context (`-split`, `-join`, `-like`) or culture (`-f`) are not folded (comment on `TokenFlags.CanConstantFold`).
- **`-and`/`-or`** short-circuit; **`-xor`** does not. **`-band`/`-bor`/`-bxor`/`-shl`/`-shr`** operate on integers of the wider operand type.

## 6. Guidance for MicroteamShell [LESSON]

- **LSN-OP-01** [REPLICATE] (area: NLD-OP) Use the precedence levels and left associativity above; keep the comma tighter than binary operators and put ternary and assignment below. Evidence: `src/System.Management.Automation/engine/parser/Parser.cs::Parser.BinaryExpressionRule@L6798-L6950`.
- **LSN-OP-02** [REPLICATE] (area: NLD-OP) Choose the operation by the left operand's type and convert the right operand to it (CONVERSION-RULES); keep the `i`/`c` case variants and the array-filtering behavior of comparison operators. Evidence: `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder@L2119-L3422`.
- **LSN-OP-03** [ADAPT] (area: NLD-OP) Implement operators as ordinary functions with an explicit dispatch table instead of dynamic binding sites. Why: same observable results; no DLR. Evidence: `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder.FallbackBinaryOperation@L2179-L2240`.

Verification: operator rows generated from `s_staticTokenFlags`/`s_tokenText`; precedence levels cross-checked with the parser's reduce loop (`<=`) and with the generated table in [02.2-parser.md](02.2-parser.md) §7.2; evaluation text read from `PSBinaryOperationBinder` (`BinaryAdd`, `BinaryMultiply`, `BinarySubDivOrRem`, `CompareEQ`, `BinaryEqualityComparison`, `BinaryNumericOp`), `NumericOps.cs` (`IntOps`), `Compiler.VisitBinaryExpression` and `ParserOps` notes. `-shl`/`-shr`, bitwise and `-ge/-gt` internals and `PSUnaryOperationBinder` were read only at the dispatch level (`UNVERIFIED` below that).

