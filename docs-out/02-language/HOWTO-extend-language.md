---
id: LANG-HOWTO-001
title: How to extend the language
kind: guide
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/parser/token.cs, src/System.Management.Automation/engine/parser/tokenizer.cs, src/System.Management.Automation/engine/parser/Parser.cs, src/System.Management.Automation/engine/parser/ast.cs, src/System.Management.Automation/engine/parser/Compiler.cs, src/System.Management.Automation/engine/LanguagePrimitives.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/parser/_folder.md]
generated_from: []
---

# How to extend the language

> STATIC-ONLY — behavior not run-verified. Each recipe lists, in order, the places in the PowerShell source that a change touches, derived from the documents of this study (each step links to its evidence), and traces one existing feature end to end. The lists are what PowerShell itself needs; MicroteamShell can drop the DLR, compiler and visitor-version steps. `INFERENCE` marks steps deduced from the code shape (nothing was built or run).

## 1. Purpose and scope [SPEC]

Practical guidance for adding syntax or semantics: (a) a new operator, (b) a new statement keyword, (c) a new AST node, (d) a new literal, (e) a new automatic variable, (f) a new type conversion.

## 2. Source map

The places named below, by stage: tokenizer (`token.cs`, `tokenizer.cs`, `CharTraits.cs`), parser (`Parser.cs`), AST (`ast.cs`, `AstVisitor.cs`, `PreOrderVisitor.cs`), analysis (`SemanticChecks.cs`, `VariableAnalysis.cs`, `SymbolResolver.cs`), constants (`ConstantValues.cs`, `SafeValues.cs`), compiler (`Compiler.cs`), runtime (`Binders.cs`, `MiscOps.cs`, `parserutils.cs`, `LanguagePrimitives.cs`), variables (`SpecialVariables.cs`).

## 3. Responsibilities and non-responsibilities

A guide, not a specification. It does not say whether a change is advisable.

## 4. Key types and contracts [IMPL]

Contracts that every change must keep: tables in `token.cs` stay the same length as `TokenKind` (a `DEBUG` static constructor asserts it); every AST node must be added to both visitor families and to the debug parent checker; `Copy`, `Accept` and `InternalVisit` must agree on children order ([02.3-ast.md](02.3-ast.md) §6).

## 5. Data model

Not applicable (procedural guide).

## 6. Control flow — recipes

### 6.1 (a) A new operator

1. Add a `TokenKind` member with an explicit value (use a reserved slot in 105-118 or append) and rows in `s_staticTokenFlags` and `s_tokenText` (src/System.Management.Automation/engine/parser/token.cs::TokenKind@L18-L595, src/System.Management.Automation/engine/parser/token.cs::TokenTraits@L757-L1211); flags: `BinaryOperator` plus a `BinaryPrecedence*` level (and `CanConstantFold`/`DisallowedInRestrictedMode` as needed). For a dash operator also add the spelling to `_operatorText` and the kind to `s_operatorTokenKind` in the same position (src/System.Management.Automation/engine/parser/tokenizer.cs::Tokenizer@L595-L5082); for a symbol operator add a case in `Tokenizer.NextToken`.
2. Parser: nothing for an existing precedence level (`BinaryExpressionRule` is table-driven); a new level needs a new `BinaryPrecedence*` value (src/System.Management.Automation/engine/parser/Parser.cs::Parser.BinaryExpressionRule@L6798-L6950).
3. AST: nothing (`BinaryExpressionAst` validates the `BinaryOperator` trait); extend `StaticType` if the result type is fixed (src/System.Management.Automation/engine/parser/ast.cs::BinaryExpressionAst@L7502-L7617).
4. Compiler: a case in `VisitBinaryExpression` (dynamic site with an operation id, or a helper call) (src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitBinaryExpression@L5687-L5977).
5. Runtime: a rule in `PSBinaryOperationBinder.FallbackBinaryOperation` and its operation methods, or a `ParserOps` helper (src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder.FallbackBinaryOperation@L2179-L2238).
6. Type inference/completion (`TypeInferenceVisitor.VisitBinaryExpression`) and restricted-language flags (`INFERENCE`: completion is optional).
7. Tests and docs: operator table, token catalog.
*Trace:* `-shl`/`-shr` have kind values 97 and 98, appended after the earlier operators, with `Comparison` precedence and `CanConstantFold`; the compiler maps them to `LeftShift`/`RightShift` dynamic operations and the binder implements `Shift` ([TOKEN-CATALOG.md](TOKEN-CATALOG.md) §3, [COMPILATION-MAP.md](COMPILATION-MAP.md), src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder.Shift@L2872-L2918). `??` (kind 102) followed the same path with its own precedence level 7.

### 6.2 (b) A new statement keyword

1. Tokenizer: `TokenKind` + `s_keywordText`/`s_keywordTokenKind` rows + flag rows (`Keyword`, `StatementDoesntSupportAttributes` if attributes are not allowed, `ScriptBlockBlockName` for block names) (src/System.Management.Automation/engine/parser/token.cs::TokenTraits@L757-L1211, src/System.Management.Automation/engine/parser/tokenizer.cs::Tokenizer@L595-L5082).
2. Parser: a `case` in `StatementRule` and a `*Rule` method building the AST; set tokenizer modes if the body needs them (src/System.Management.Automation/engine/parser/Parser.cs::Parser.StatementRule@L1950-L2159).
3. AST class (recipe c).
4. Semantic: `SemanticChecks` visit (placement rules), `VariableAnalysis` flow-graph visit, `SymbolResolver` if types are involved (src/System.Management.Automation/engine/parser/SemanticChecks.cs::SemanticChecks@L21-L1514, src/System.Management.Automation/engine/parser/VariableAnalysis.cs::VariableAnalysis@L325-L1847).
5. Compiler: `Compiler.Visit…` ([COMPILATION-MAP.md](COMPILATION-MAP.md)).
6. Restricted language: `RestrictedLanguageChecker` visit; completion/type inference visits.
*Trace:* `clean` (kind 170, the last token kind) is a keyword with `ScriptBlockBlockName`; `NamedBlockListRule` parses it, `ScriptBlockAst` gained `CleanBlock`, the compiler emits a `<Clean>` lambda and `InvokeWithPipeImpl` rejects it for plain invocation (src/System.Management.Automation/engine/parser/Parser.cs::Parser.NamedBlockListRule@L1727-L1857, src/System.Management.Automation/engine/parser/ast.cs::NamedBlockAst@L1864-L2026, src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitScriptBlock@L2450-L2502).

### 6.3 (c) A new AST node

1. Class in `ast.cs` with constructor checks, parent links (`SetParent`), `Copy`, `Accept` and `InternalVisit` (pre/post action pattern) (src/System.Management.Automation/engine/parser/ast.cs::Ast@L91-L420, src/System.Management.Automation/engine/parser/ast.cs::IfStatementAst@L4059-L4157 as template).
2. A `VisitX` in `ICustomAstVisitor` (or `ICustomAstVisitor2` for source compatibility), `DefaultCustomAstVisitor`, `AstVisitor` (or `AstVisitor2`), `AstSearcher`, the DEBUG `CheckAllParentsSet` (src/System.Management.Automation/engine/parser/AstVisitor.cs::ICustomAstVisitor2@L207-L235, src/System.Management.Automation/engine/parser/PreOrderVisitor.cs::AstVisitor@L35-L215).
3. Implementations in every visitor class that must handle it: `Compiler`, `VariableAnalysis`, `IsConstantValueVisitor`, `ConstantValueVisitor`, `IsSafeValueVisitor`, `GetSafeValueVisitor`, `RestrictedLanguageChecker`, `TypeInferenceVisitor`, `ScriptBlockToPowerShellChecker`, … (list: [AST-CATALOG.md](AST-CATALOG.md) §6).
4. Parser production that creates it; semantic checks.
*Trace:* `TernaryExpressionAst` (second-generation node): class with three required children; visited by `AstVisitor2`/`ICustomAstVisitor2` only; created by `ExpressionRule`; compiled to `Expression.Condition`; folded by `IsConstantValueVisitor` (src/System.Management.Automation/engine/parser/ast.cs::TernaryExpressionAst@L7404-L7497, src/System.Management.Automation/engine/parser/Parser.cs::Parser.ExpressionRule@L6696-L6790, src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitTernaryExpression@L5677-L5685).

### 6.4 (d) A new literal

1. Tokenizer: a scan routine reached from `NextToken` (or a new branch in `ScanNumberHelper` for numbers), producing a `Token` subclass or an existing kind (src/System.Management.Automation/engine/parser/tokenizer.cs::Tokenizer.NextToken@L4612-L5081).
2. Parser: `PrimaryExpressionRule` case creating a constant AST (src/System.Management.Automation/engine/parser/Parser.cs::Parser.PrimaryExpressionRule@L7228-L7299).
3. AST: `ConstantExpressionAst`/`StringConstantExpressionAst` (new `StringConstantType` if quoting differs).
4. Compiler: constants are handled generically (`VisitConstantExpression`).
5. Conversions: `Parser.ScanNumber` reuses the tokenizer, so string-to-number follows automatically ([CONVERSION-RULES.md](CONVERSION-RULES.md) §7.2).
*Trace:* the `n` BigInteger suffix: `NumberSuffixFlags.BigInteger`, `CharTraits.TypeSuffix` includes `n`, `ScanNumberHelper` accepts it, `TryGetNumberValue` produces `BigInteger` (src/System.Management.Automation/engine/parser/tokenizer.cs::Tokenizer.TryGetNumberValue@L3555-L3882, [02.1-tokenizer.md](02.1-tokenizer.md) §7.1).

### 6.5 (e) A new automatic variable

1. `SpecialVariables`: name constant; for a **slot** variable also an `AutomaticVariable` enum member (order is fixed: slots 0-8 are asserted by `VariableAnalysis`), `AutomaticVariableTypes` and `AutomaticVariables` entries (src/System.Management.Automation/engine/SpecialVariables.cs::SpecialVariables@L22-L399, src/System.Management.Automation/engine/SpecialVariables.cs::AutomaticVariable@L401-L413).
2. Variable analysis seeds all automatic variables in its constructor, so slot variables are picked up from the arrays (src/System.Management.Automation/engine/parser/VariableAnalysis.cs::VariableAnalysis@L325-L1847).
3. Where the value is set: `InvokeWithPipeImpl` (for `$_`, `$input`, `$this`, `$PSScriptRoot`, `$PSCommandPath`) or the command processor for others.
4. Non-slot engine variables are defined in the global scope at session start (not traced).
*Trace:* `$PSCommandPath` is automatic variable 8, typed `string`, set with `$PSScriptRoot` by `SetPSScriptRootAndPSCommandPath` before the clause runs (src/System.Management.Automation/engine/lang/scriptblock.cs::ScriptBlock.SetPSScriptRootAndPSCommandPath@L1072-L1084).

### 6.6 (f) A new type conversion

1. Language-level: a branch in `FigureLanguageConversion` with a converter method and rank, or rely on a static `Parse`/constructor/cast on the type (src/System.Management.Automation/engine/LanguagePrimitives.cs::LanguagePrimitives.FigureLanguageConversion@L4966-L5154).
2. Pre-seeded conversions go in `RebuildConversionCache`.
3. Restricted modes: add the target type to `CoreTypes` only if safe in Constrained Language Mode (src/System.Management.Automation/engine/parser/TypeResolver.cs::CoreTypes@L709-L838).
4. Type accelerator: `TypeAccelerators` table.
*Trace:* conversion of `ScriptBlock` to delegates is a `toType.IsSubclassOf(Delegate)` branch with `ConvertScriptBlockToDelegate` at rank `Language` ([CONVERSION-RULES.md](CONVERSION-RULES.md) §7.1).

## 7. Algorithms

Not applicable.

## 8. Observable behavior [SPEC]

Not applicable (no run).

## 9. Error handling and edge cases

Typical failure modes visible in the code: table length mismatches (`DEBUG` asserts), missing visitor overrides (default returns `null`/`Continue`, silently skipping the node), second-generation nodes invisible to old visitors ([02.3-ast.md](02.3-ast.md) §6.2).

## 10. Concurrency and threading

Not applicable.

## 11. Extension points and customization hooks

Beyond core changes: dynamic keywords (`DynamicKeyword` with `PreParse/PostParse/SemanticCheck`), type accelerators, `ETS` type data, argument transformation/validation attributes.

## 12. Dependencies

Documents: [02.1-tokenizer.md](02.1-tokenizer.md), [02.2-parser.md](02.2-parser.md), [02.3-ast.md](02.3-ast.md), [02.4-semantic-analysis.md](02.4-semantic-analysis.md), [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md).

## 13. Performance notes

Not applicable.

## 14. Security considerations (mandatory)

Every new operator, node or conversion must be classified for restricted modes: token flag `DisallowedInRestrictedMode`, `RestrictedLanguageChecker` visit, `IsSafeValueVisitor` allow-list decision, `CoreTypes` membership. Forgetting one silently allows the construct in data sections or Constrained Language.

## 15. Enterprise considerations

Add corpus snippets and tests for each change (operator tables and catalogs here are generated, so regenerate them).

## 16. Tests

Not applicable.

## 17. Design decisions and trade-offs

PowerShell's extension cost is high because a construct appears in ~10 tables and visitors; a new shell should centralize per-construct metadata.

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-HOWTO-01** [ADAPT] (area: NLD-TOOL) Keep one declaration per operator/keyword (spelling, kind, precedence, flags, evaluator) and generate the tables, instead of parallel arrays kept in sync by assertions. Why: same behavior, less drift. Evidence: src/System.Management.Automation/engine/parser/token.cs::TokenTraits@L757-L1211.
- **LSN-HOWTO-02** [ADAPT] (area: NLD-TOOL) Give every AST node one visitor interface with a default method; add a test that visits all nodes of a corpus with each visitor. Why: PowerShell's two-generation visitor scheme is only for compatibility. Evidence: src/System.Management.Automation/engine/parser/AstVisitor.cs::ICustomAstVisitor2@L207-L235.
- **LSN-HOWTO-03** [REPLICATE] (area: NLD-SEC) Classify each new construct for restricted evaluation at the time it is added. Evidence: src/System.Management.Automation/engine/parser/SemanticChecks.cs::RestrictedLanguageChecker@L1807-L2454.

## 19. Open questions / UNVERIFIED

- Steps marked `INFERENCE` (completion, type inference) were not traced through the completion code (Tier C).
- No build was run to check that the recipes compile.

Verification: every step links to the source or document that supports it; the traces use `TokenKind` values from [TOKEN-CATALOG.md](TOKEN-CATALOG.md), the `Compiler.VisitScriptBlock` clause names, `SetPSScriptRootAndPSCommandPath`, and the `FigureLanguageConversion` delegate branch read in this study.
