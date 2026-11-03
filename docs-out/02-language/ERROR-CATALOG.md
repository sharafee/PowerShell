---
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

## 1. Purpose and scope [SPEC]

Catalog of the parse error IDs. An error ID is the resource key of `ParserStrings.resx` (the code passes `nameof(ParserStrings.Key)` as ID and `ParserStrings.Key` as message template; `FACT-SRC`, `src/System.Management.Automation/engine/parser/Parser.cs::Parser.ReportError@L8143-L8166`). `ParserStrings.resx` holds **<!--N:PARSERSTRINGS_KEYS-->412<!--/N-->** keys; <!--N:PARSERSTRINGS_KEYS_PARSER_TOKENIZER-->157<!--/N--> are reported from `Parser.cs` or `tokenizer.cs` (section 3); the others are reported by semantic checks, type/class building or other code (section 4, owned by [02.4-semantic-analysis.md](02.4-semantic-analysis.md), planned T24).

Report kinds: **(E)** `ReportError` — a plain error; **(I)** `ReportIncompleteInput` — the error sets `ParseError.IncompleteInput` when the error position is at the end of the script (so a REPL can ask for another line) (`src/System.Management.Automation/engine/parser/Parser.cs::Parser.ReportIncompleteInput@L8111-L8141`); **(?)** the classifier found neither call nearby (error built through a variable, e.g. `errorId`/`errorMsg`).

Dedup: `SaveError` drops an error when an earlier error has the same ID and the same start/end line and column; there is no cap on the number of errors (`src/System.Management.Automation/engine/parser/Parser.cs::Parser.SaveError@L8026-L8057`).

<!--CF:CF-ERR-002-->**Parse-error limits and recovery rule.** The parser never throws for a syntax error: each error is appended to `Parser.ErrorList` after de-duplication (an error is dropped only if an earlier error has the same ID and the same start and end line and column), there is no limit on the number of errors, and parsing continues by returning partial or error nodes (`ErrorStatementAst`, `ErrorExpressionAst`), by pretending a missing closing token was present, or by skipping tokens to a synchronization token (`SyncOnError`, which tracks nesting of `()`, `{}` and `[]` and never consumes end of input); `ParseError.IncompleteInput` is true only when the error was reported with `ReportIncompleteInput` and the error position is at the end of the script apart from whitespace and comments. The only exceptions are an exhausted execution stack (the whole parse is retried once on a new thread, then `ScriptTooComplicated` is reported) and any other exception during `ParseFile`/`ParseInput`, which is wrapped as a `ParseException` with `UnrecoverableParserError`.<!--/CF-->

## 2. Source map

| path | type | role |
|---|---|---|
| `src/System.Management.Automation/resources/ParserStrings.resx` | resx | error message templates |
| `src/System.Management.Automation/engine/parser/Parser.cs::Parser.ReportError@L8143-L8166` | method | report a plain error |
| `src/System.Management.Automation/engine/parser/Parser.cs::Parser.ReportIncompleteInput@L8111-L8141` | method | report an error that may mean 'more input expected' |
| `src/System.Management.Automation/engine/parser/Parser.cs::ParseError@L8193-L8241` | class | public error object: `Extent`, `ErrorId`, `Message`, `IncompleteInput` |

## 3. Keys reported by Parser.cs or tokenizer.cs

| Error ID (resource key) | Message template | Parser.cs lines | tokenizer.cs lines | Also used in |
|---|---|---|---|---|
| `AllStream` | * stream | L6245(?) |  |  |
| `ArrayHasTooManyDimensions` | The array has too many dimensions: {0}. The number of dimensions for an array must be less than or equal to 32. | L1554(E) |  |  |
| `BackgroundOperatorInPipelineChain` | Background operators can only be used at the end of a pipeline chain. | L5934(E) |  |  |
| `BadNumericConstant` | The numeric constant {0} is not valid. |  | L3912(E) |  |
| `CannotLoadAssemblyFromUncPath` | Cannot use assembly with an UNC path: '{0}'. | L5099(E) |  |  |
| `CannotLoadAssemblyWithUriSchema` | Cannot use assembly with uri schema '{0}'. | L5108(E) |  |  |
| `ClassesNotAllowedInConstrainedLanguage` | Class keyword is not allowed in ConstrainedLanguage mode. | L4231(E) |  |  |
| `ConfigurationBodyEmpty` | The configuration block results were null or empty. Verify that configurations were defined in the block. | L3137(E) |  |  |
| `ConfigurationNotAllowedInConstrainedLanguage` | Configuration keyword is not allowed in constrainedLanguage mode. | L2993(E) |  |  |
| `ConfigurationNotAllowedOnArm64` | Configuration keyword is not supported on ARM64 processors. | L3012(E) |  |  |
| `ConfigurationNotAllowedOnWinPE` | Configuration is not supported on WinPE. | L3022(E) |  |  |
| `DebugStream` | debug stream | L6250(?) |  |  |
| `DuplicateNamedArgument` | Duplicate named arguments '{0}' are not allowed. | L1225(E) |  | `engine/parser/SemanticChecks.cs` |
| `DuplicateQualifier` | Duplicate '{0}' qualifier | L4455(E) L4477(E) L4500(E) |  |  |
| `DuplicateScriptCommandClause` | Script command clause '{0}' has already been defined. | L1836(E) |  |  |
| `DynamicKeywordPostParseException` | Exception occurred when post-parsing dynamic keyword '{0}' with details '{1}'. | L4081(E) |  |  |
| `DynamicKeywordPreParseException` | Exception occurred when pre-parsing dynamic keyword '{0}' with details '{1}'. | L3745(E) |  |  |
| `EmptyPipeElement` | An empty pipe element is not allowed. | L6083(I) L6136(I) |  |  |
| `EmptyPipelineChainElement` | A pipeline chain operator must be followed by a pipeline. | L5888(I) L5902(E) L5982(I) |  |  |
| `EmptyVariableReference` | An empty ${} variable reference was found. A name is required inside the braces. |  | L2968(E) |  |
| `EndSquareBracketExpectedAtEndOfAttribute` | Missing ] at end of attribute or type literal. | L1127(I) L1147(E) L1485(I) |  |  |
| `EndSquareBracketExpectedAtEndOfType` | Missing ] at end of type token. | L1426(I) L7830(I) |  |  |
| `ErrorLoadingAssembly` | Cannot load assembly '{0}'. | L5157(E) |  | `engine/parser/Compiler.cs`, `src/Microsoft.PowerShell.Commands.Utility/commands/utility/AddType.cs` |
| `ErrorStream` | error stream | L6247(?) |  |  |
| `ExpectedExpression` | An expression was expected after '('. | L7594(I) |  |  |
| `ExpectedValueExpression` | You must provide a value expression following the '{0}' operator. | L4857(E) L5831(I) L6739(I) |  |  |
| `ExpressionsMustBeFirstInPipeline` | Expressions are only allowed as the first element of a pipeline. | L6038(E) |  |  |
| `FileReadError` | The file could not be read: {0}. | L89(?) |  | `engine/parser/Compiler.cs` |
| `IfStatementMissingCondition` | Missing condition in if statement after '{0} ('. | L2444(I) |  |  |
| `IncompleteDollarSubexpressionReference` | $(subexpression) is missing the closing ')'. |  | L2416(I) |  |
| `IncompleteDollarVariableReference` | ${{variable}} reference starting is missing the closing '}}'. |  | L2959(I) |  |
| `IncompleteMemberDefinition` | Missing a property name or method definition. | L4632(I) |  |  |
| `IncompletePropertyAssignmentBlock` | There is an incomplete property assignment block in the instance definition. | L7383(?) |  |  |
| `IncompleteString` | Incomplete string token. |  | L4710(I) |  |
| `InformationStream` | information stream | L6251(?) |  |  |
| `InvalidBracedVariableReference` | Variable reference is not valid. The variable name is missing. |  | L3000(E) |  |
| `InvalidConfigurationName` | The configuration name '{0}' is not valid. Standard names may only contain letters (a-z, A-Z), numbers (0-9), period (.), hyphen (-) and underscore (_). The name may not be null or empty, and should start with a letter. | L2960(E) |  | `DscSupport/CimDSCParser.cs` |
| `InvalidForeachFlag` | The parameter {0} is not valid for the foreach statement. | L3411(E) |  |  |
| `InvalidFunctionParameter` | Parameter declarations are a comma-separated list of variable names with optional initializer expressions. | L984(I) |  |  |
| `InvalidParameterForDataSectionStatement` | The "{0}" parameter of the Data section is not valid. The valid Data section parameter is SupportedCommand. | L5704(E) |  |  |
| `InvalidSwitchFlag` | The parameter {0} is not valid for the switch statement. | L2677(E) |  |  |
| `InvalidUnderlyingType` | '{0}' is not a valid underlying type for enums. Expected a builtin integral type (one of byte, sbyte, short, ushort, int, uint, long or ulong) | L4757(E) |  | `engine/parser/PSType.cs` |
| `InvalidUnicodeEscapeSequence` | The Unicode escape sequence is not valid. A valid sequence is `u{ followed by one to six hex digits and a closing '}'. |  | L1506(E) L1527(E) L1542(E) |  |
| `InvalidUnicodeEscapeSequenceValue` | The Unicode escape sequence value is out of range. The maximum value is 0x10FFFF. |  | L1584(E) |  |
| `InvalidValueForUsingItemName` | '{0}' is not a valid value for using name. | L4973(E) L4985(E) L5044(E) |  |  |
| `InvalidVariableReference` | Variable reference is not valid. '$' was not followed by a valid variable name character. Consider using ${} to delimit the name. |  | L3172(?) |  |
| `InvalidVariableReferenceWithDrive` | Variable reference is not valid. ':' was not followed by a valid variable name character. Consider using ${} to delimit the name. |  | L3167(?) |  |
| `MissingArgument` | Missing argument in parameter list. | L6540(E) |  |  |
| `MissingArrayIndexExpression` | Array index expression is missing or not valid. | L7996(I) |  |  |
| `MissingAssemblyNameSpecification` | The type name is missing the assembly name specification. | L1386(E) L1511(E) L1605(E) |  |  |
| `MissingBaseCtorCall` | Missing 'base' after ':' in a base class constructor call. | L5245(I) |  |  |
| `MissingBraceInObjectDefinition` | Missing '{' in object definition. | L3804(I) L3921(I) |  |  |
| `MissingCatchHandlerBlock` | The Catch block is missing its statement block. | L5571(I) |  |  |
| `MissingCatchOrFinally` | The Try statement is missing its Catch or Finally block. | L5659(I) |  |  |
| `MissingColonInTernaryExpression` | Missing ':' in the ternary expression. | L6761(I) |  |  |
| `MissingConfigurationName` | The name for the configuration is missing. Provide the missing name as a simple name, string, or string-valued expression. | L2917(E) L2930(I) L2944(I) |  |  |
| `MissingCurlyBraceInSwitchStatement` | Missing '{' in switch statement. | L2775(I) |  |  |
| `MissingCurlyInConfigurationStatement` | Missing '{' in configuration statement. | L3116(I) |  |  |
| `MissingEndCurlyBrace` | Missing closing '}' in statement block or type definition. | L1645(I) L1886(I) L2874(I) |  |  |
| `MissingEndParenthesisAfterForeach` | Missing closing ')' after expression part of foreach loop. The correct form is: foreach ($a in $b) {...} | L3489(I) |  |  |
| `MissingEndParenthesisAfterStatement` | Missing closing ')' after expression in '{0}' statement. | L2466(I) L3600(I) L3685(I) |  |  |
| `MissingEndParenthesisInExpression` | Missing closing ')' in expression. | L1111(I) L7607(I) |  |  |
| `MissingEndParenthesisInFunctionParameterList` | Missing ')' in function parameter list. | L884(I) L5439(I) |  |  |
| `MissingEndParenthesisInMethodCall` | Missing ')' in method call. | L7954(I) |  |  |
| `MissingEndParenthesisInSubexpression` | Missing closing ')' in subexpression. | L7548(I) |  |  |
| `MissingEndParenthesisInSwitchStatement` | Missing ')' after expression in switch statement. | L2736(I) |  |  |
| `MissingEndSquareBracket` | Missing ']' after array index expression. | L8012(I) |  |  |
| `MissingEqualsInHashLiteral` | Missing '=' operator after key in hash literal. | L7446(?) |  |  |
| `MissingEqualsInPropertyAssignmentBlock` | Missing '=' operator after key in property assignment. | L7441(?) L7472(?) |  |  |
| `MissingEqualsInUsingAlias` | Missing '=' operator | L5070(I) |  |  |
| `MissingExpression` | Missing expression after '{0}' in pipeline element. | L6333(I) L6667(E) |  |  |
| `MissingExpressionAfterKeyword` | Missing expression after '{0}' in loop. | L3663(I) L4166(I) |  |  |
| `MissingExpressionAfterOperator` | Missing expression after unary operator '{0}'. | L7124(I) |  |  |
| `MissingExpressionAfterToken` | Missing expression after '{0}'. | L932(I) L1009(I) L1247(I) |  |  |
| `MissingExpressionInNamedArgument` | Missing statement after '=' in named argument. | L1197(I) |  |  |
| `MissingFileSpecification` | Missing file specification after redirection operator. | L6186(E) |  |  |
| `MissingFilenameOption` | Cannot process the 'switch' statement because of a missing file name argument to the -file option. | L2651(I) |  |  |
| `MissingFinallyStatementBlock` | The Finally block is missing its statement block. | L5647(I) |  |  |
| `MissingForeachExpression` | Missing expression in foreach loop. The correct form is: foreach ($a in $b) {...} | L3475(I) |  |  |
| `MissingForeachStatement` | Missing statement body in foreach loop. The correct form is: foreach ($a in $b) {...} | L3501(I) |  |  |
| `MissingFunctionBody` | Missing function body in function declaration. | L5270(I) L5382(I) |  |  |
| `MissingInInForeach` | Missing 'in' after variable in foreach loop. The correct form is: foreach ($a in $b) {...} | L3462(I) |  |  |
| `MissingLoopStatement` | Missing statement body in {0} loop. | L3612(I) L3700(I) L4123(I) |  |  |
| `MissingMethodParameterList` | Missing '(' in class method parameter list. | L5195(I) L5237(I) |  |  |
| `MissingNameAfterKeyword` | Missing name after {0} keyword. | L4252(I) L4725(I) L5359(I) |  |  |
| `MissingNamedBlocks` | unexpected token '{0}', expected 'begin', 'process', 'end', 'clean', or 'dynamicparam'. | L1769(E) |  |  |
| `MissingNamedStatementBlock` | Missing statement block after '{0}'. | L1800(I) |  |  |
| `MissingNamespaceAlias` | Missing namespace alias | L5015(I) |  |  |
| `MissingOpenParenthesisAfterKeyword` | Missing opening '(' after keyword '{0}'. | L3428(I) L3552(I) L3646(I) |  |  |
| `MissingOpenParenthesisInIfStatement` | Missing '(' after '{0}' in if statement. | L2428(I) |  |  |
| `MissingPropertyName` | Missing property name after reference operator. | L7734(I) |  |  |
| `MissingPropertyTerminator` | Missing ';' or end-of-line in property definition. | L4565(I) L4881(I) |  |  |
| `MissingStatementAfterKeyword` | Missing statement body after keyword '{0}'. | L2352(I) L2389(I) L4023(I) |  |  |
| `MissingStatementBlock` | Missing statement block after {0} ( condition ). | L2482(I) |  |  |
| `MissingStatementBlockAfterElse` | Missing statement block after 'else' keyword. | L2522(I) |  |  |
| `MissingStatementBlockForDataSection` | The Data section is missing its statement block. | L5756(I) |  |  |
| `MissingStatementInHashLiteral` | Missing statement after '=' in hash literal. | L7477(?) |  |  |
| `MissingStatementTerminator` | Missing a newline or semicolon. | L567(I) |  |  |
| `MissingSwitchConditionExpression` | Missing condition in switch statement clause. | L2806(I) |  |  |
| `MissingSwitchStatementClause` | Missing statement block in switch statement clause. | L2829(I) |  |  |
| `MissingTerminatorMultiLineComment` | The terminator '#>' is missing from the multiline comment. |  | L1830(I) |  |
| `MissingThrottleLimit` | The ThrottleLimit parameter of the foreach statement is missing a value. Supply a throttle limit to the parameter. | L3401(I) |  |  |
| `MissingTrapStatement` | The 'trap' statement was incomplete. A trap statement requires a body. | L5475(I) |  |  |
| `MissingTryStatementBlock` | The Try statement is missing its statement block. | L5618(I) |  |  |
| `MissingTypeBody` | Missing '{0}' body in '{0}' declaration. | L4311(I) L4774(I) |  |  |
| `MissingTypeLiteralToken` | Missing type literal. | L5526(I) |  |  |
| `MissingTypename` | Missing type name after '['. | L1077(I) L1371(I) L1411(I) |  |  |
| `MissingUnicodeEscapeSequenceTerminator` | The Unicode escape sequence is missing the closing '}'. |  | L1548(E) |  |
| `MissingUsingItemName` | Missing using name | L4963(I) |  |  |
| `MissingUsingStatementDirective` | Missing using directive | L4946(I) |  |  |
| `MissingValueForSupportedCommandInDataSectionStatement` | The SupportedCommand parameter of the Data section is missing a value. Supply a cmdlet or function name to the parameter. | L5723(I) |  |  |
| `MissingVariableNameAfterForeach` | Missing variable name after foreach. The correct form is: foreach ($a in $b) {...} | L3444(I) |  |  |
| `MissingWhileOrUntilInDoWhile` | Missing while or until keyword in do loop. | L4138(I) |  |  |
| `ModifiersCannotBeCombined` | Modifier '{0}' cannot be combined with '{1}' | L4463(E) L4485(E) |  |  |
| `MultipleSwitchDefaultClauses` | A switch statement can have only one default clause. | L2845(E) |  |  |
| `OpenBraceNeedsToBeBackTickedInVariableName` | Use `{ instead of { in variable names. |  | L2937(E) |  |
| `OutputStream` | output stream | L6246(?) |  |  |
| `ParameterCannotHaveArgument` | Parameter {0} cannot have an argument. |  | L2018(E) |  |
| `ParameterRequiresArgument` | Parameter {0} requires an argument. | L3350(E) L6567(E) | L2029(E) |  |
| `ParserError` | {0} | L3096(E) L3283(E) |  |  |
| `PipelineValueRequired` | A switch statement must have one of the following:  '-file file_name' or '( expression )'. | L2703(E) L2716(I) L2751(I) |  |  |
| `RedirectionNotSupported` | The '{0}' operator is reserved for future use. | L6195(E) L6217(E) L6228(E) |  |  |
| `RequiredNameOrExpressionMissing` | A required name or expression was missing. | L3340(I) L3797(I) L3819(E) |  |  |
| `RequiresArgumentMustBeConstant` | Argument must be constant. |  | L2039(E) | `DscSupport/CimDSCParser.cs`, `engine/parser/SymbolResolver.cs` |
| `RequiresInvalidStringArgument` | The argument for the {0} parameter is not valid. Specify a valid string argument. |  | L2059(E) L2072(E) L2221(E) |  |
| `RequiresModuleInvalid` | The argument for the Module parameter is not valid. {0} |  | L2190(E) L2198(E) | `engine/parser/SymbolResolver.cs` |
| `RequiresPSEditionInvalid` | The argument for the {0} parameter is not valid. Specify a valid PowerShell edition. |  | L2255(E) |  |
| `RequiresPSEditionValueIsAlreadySpecified` | The argument for the {0} parameter contains duplicate values. Do not specify duplicate PowerShell edition values. |  | L2267(E) |  |
| `RequiresVersionInvalid` | The argument for the Version parameter is not valid. Specify a valid PowerShell version, in the format major.minor version. |  | L2129(E) | `DscSupport/CimDSCParser.cs` |
| `ReservedKeywordNotAllowed` | The '{0}' keyword is not supported in this version of the language. | L2090(E) |  |  |
| `ScriptTooComplicated` | Processing was stopped because the script is too complex. | L220(E) |  | `engine/parser/SemanticChecks.cs` |
| `StreamAlreadyRedirected` | The {0} for this command is already redirected. | L6257(E) |  |  |
| `TerminatorExpectedAtEndOfString` | The string is missing the terminator: {0}. |  | L2346(I) L2508(I) L2599(I) |  |
| `TokenAfterEndOfValidScriptText` | Executable script code found in signature block. |  | L1141(E) |  |
| `TooManyDigitsInUnicodeEscapeSequence` | The Unicode escape sequence contains more than the maximum of six hex digits between braces. |  | L1560(E) |  |
| `TooManyTypes` | Only one type may be specified on class members. | L4439(E) |  |  |
| `TypeNameExpected` | Type name expected. | L4283(I) L4747(I) |  |  |
| `TypeNotAllowedBeforeParam` | Unexpected type [{0}] was found in the parameter statement. | L904(E) |  |  |
| `TypeNotAllowedBeforeStatement` | Unexpected type [{0}] was found before statement. | L2016(E) |  |  |
| `UnexpectedAttribute` | Unexpected attribute '{0}'. | L2006(E) L7153(I) |  | `engine/parser/SemanticChecks.cs` |
| `UnexpectedCharactersAfterHereStringHeader` | No characters are allowed after a here-string header but before the end of the line. |  | L2612(E) |  |
| `UnexpectedNameForType` | The '{0}' resource can only be used once per configuration, and therefore cannot have a name. Remove '{1}', and then run the script again. | L3830(E) L3881(E) |  |  |
| `UnexpectedToken` | Unexpected token '{0}' in expression or statement. | L1362(E) L1588(E) L1672(E) |  |  |
| `UnexpectedTokenInDynamicKeyword` | There is no whitespace between the name and the scriptblock in dynamic keyword '{0}' body statement. | L3950(E) |  |  |
| `UnexpectedUnaryOperator` | Internal error - unexpected unary operator {0}. | L5022(E) |  |  |
| `UnrecognizedToken` | Unrecognized token in source text. |  | L4673(E) |  |
| `UnrecoverableParserError` | Unrecoverable error in PowerShell. | L108(?) L157(?) |  |  |
| `UnsupportedReservedKeyword` | The '{0}' keyword is not supported in this version of the language. | L3756(E) |  |  |
| `UnsupportedReservedProperty` | The '{0}' property is not supported in this version of the language. | L3766(E) |  |  |
| `UsingMustBeAtStartOfScript` | A 'using' statement must appear before any other statements in a script. | L2140(E) |  |  |
| `VerboseStream` | verbose stream | L6249(?) |  |  |
| `WDACParserClassKeywordLogMessage` | The Class keyword will not be allowed in Constrained Language mode for untrusted script. | L4241(E) |  |  |
| `WDACParserClassKeywordLogTitle` | Parser Class Keyword | L4240(E) |  |  |
| `WDACParserConfigKeywordLogMessage` | The Configuration keyword will not be allowed in Constrained Language mode for untrusted script. | L3002(E) |  |  |
| `WDACParserConfigKeywordLogTitle` | Parser Configuration Keyword | L3001(E) |  |  |
| `WarningStream` | warning stream | L6248(?) |  |  |
| `WhitespaceBeforeHereStringFooter` | White space is not allowed before the string terminator. |  | L2735(I) L2847(I) |  |

Rows: **<!--N:PARSERSTRINGS_KEYS_PARSER_TOKENIZER-->157<!--/N-->** (`GENERATED`).

## 4. Keys used only elsewhere (semantic checks, type building, runtime)

| Resource key | Message template | Use count | Files (first three) |
|---|---|---:|---|
| `AddHashTableToNonHashTable` | A hash table can only be added to another hash table. | 1 | `engine/runtime/Binding/Binders.cs` |
| `AmbiguousConversion` | There are valid conversions from {0} to {1}. | 1 | `engine/ComInterop/Errors.cs` |
| `AmbiguousPath` | The path cannot be processed because it resolved to more than one file; only one file at a time can be processed. | 4 | `engine/Modules/ModuleCmdletBase.cs`, `engine/Modules/TestModuleManifestCommand.cs`, `engine/remoting/commands/TestPSSessionConfigurationFile.cs` +1 |
| `AmbiguousTypeReference` | Type name '{0}' is ambiguous, it could be '{1}' or '{2}'. | 3 | `engine/parser/SymbolResolver.cs`, `engine/parser/TypeResolver.cs` |
| `ArrayMultiplyToolongInDataSection` | Array multiplication resulting in more than {0} elements is not allowed in restricted language mode or a Data section. | 1 | `engine/runtime/Operations/ArrayOps.cs` |
| `ArrayReferenceNotSupportedInDataSection` | Array references are not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `ArraySliceAssignmentFailed` | Array assignment to [{0}] failed because assignment to slices is not supported. | 1 | `engine/runtime/Binding/Binders.cs` |
| `AsOperatorRequiresType` | The right operand of '-as' must be a type. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `AssignmentStatementNotSupportedInDataSection` | Assignment statements are not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `AssignmentStatementToAutomaticNotSupported` | Cannot assign automatic variable '{0}' with type '{1}' | 2 | `engine/parser/SemanticChecks.cs` |
| `AstIsReused` | An AST cannot be used as the child of more than one AST. To use this AST in another AST, call the Copy() method and use its result. | 1 | `engine/parser/ast.cs` |
| `AttributeNotAllowedOnDeclaration` | Attribute '{0}' is not valid on this declaration. It is valid on '{1}' declarations only. | 2 | `engine/parser/SemanticChecks.cs` |
| `AttributeNotSupportedInDataSection` | Attributes are not allowed in restricted language mode or a Data section. | 4 | `engine/parser/SemanticChecks.cs` |
| `BackupParserMessage` | An error '{0}' occurred while processing this script. Text describing this error could not be loaded. | 1 | `engine/lang/parserutils.cs` |
| `BackupParserMessageWithException` | An error '{0}' occurred while processing this script. Text describing this error could not be loaded due to error '{1}'. | 1 | `engine/lang/parserutils.cs` |
| `BadEnumeration` | An error occurred while enumerating through a collection: {0}. | 5 | `engine/lang/parserutils.cs`, `engine/runtime/Operations/MiscOps.cs` |
| `BadExpression` | The expression after '{0}' in a pipeline element produced an object that was not valid. It must result in a command name, a script block, or a CommandInfo object. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `BadOperatorArgument` | The argument to operator '{0}' is not valid: {1}. | 2 | `engine/InternalCommands.cs`, `engine/lang/parserutils.cs` |
| `BadReplaceArgument` | The {0} operator allows only two elements to follow it, not {1}. | 1 | `engine/lang/parserutils.cs` |
| `BaseClassNoDefaultCtor` | Base class '{0}' does not contain a parameterless constructor. | 2 | `engine/parser/PSType.cs` |
| `BreakHelpMessage` | Do not continue processing, throw the exception instead. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `BreakLabel` | &Break | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `COMException` | An unhandled COM interop exception occurred: {0} | 0 |  |
| `CannotCall` | Cannot perform call. | 1 | `engine/ComInterop/ComInvokeAction.cs` |
| `CannotConvertValue` | Cannot convert the value to type "{0}". | 4 | `engine/parser/PSType.cs` |
| `CannotCreateTypeConstrainedLanguage` | Cannot create type. Only core types are supported in this language mode. | 1 | `engine/runtime/Binding/Binders.cs` |
| `CannotIndex` | Unable to index into an object of type "{0}". | 2 | `engine/runtime/Binding/Binders.cs`, `engine/runtime/Operations/ArrayOps.cs` |
| `CannotIndexWithByRefLikeReturnType` | Unable to index into an object of type "{0}" with the ByRef-like return type "{1}". ByRef-like types are not supported in PowerShell. | 4 | `engine/runtime/Binding/Binders.cs` |
| `CannotInvoke` | The method cannot be invoked. | 1 | `engine/runtime/Binding/Binders.cs` |
| `CannotLoadPowerShellDataFile` | Failed to load the PowerShell data file '{0}' with the following error: {1} | 2 | `utils/PsUtils.cs` |
| `CannotResolvePowerShellDataFilePath` | Cannot resolve the path '{0}' to a single .psd1 file. | 1 | `utils/PsUtils.cs` |
| `CannotRetrieveTypeInformation` | Cannot retrieve type information. | 1 | `engine/ComInterop/Errors.cs` |
| `CantActivateDocumentInPipeline` | Cannot run a document in the middle of a pipeline: {0}. | 1 | `engine/NativeCommandProcessor.cs` |
| `CantActivateDocumentInPowerShellCore` | Cannot run a document in PowerShell: {0}. | 1 | `engine/NativeCommandProcessor.cs` |
| `CantInvokeCallOperatorAcrossLanguageBoundaries` | Cannot use '&' or '.' operators to invoke a module scope command across language boundaries. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `CantInvokeInBinaryModule` | Cannot use '&' to invoke in the context of binary module '{0}'. Specify a non-binary module after the '&' and try the operation again. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `CantInvokeInNonImportedModule` | Cannot use '&' to invoke in the context of module '{0}' because it is not imported. Import the module '{0}' and try the operation again. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `CimDeserializationError` | Cim deserializer threw an error when deserializing file {0}. | 2 | `DscSupport/CimDSCParser.cs` |
| `ClassNameNotSameAsDefiningFile` | The class name '{0}' does not match '{1}', the name of the file in which it is defined. Rename either the file name to match the class name or vice versa | 1 | `DscSupport/CimDSCParser.cs` |
| `CmdletNotInAllowedListForDataSection` | The command '{0}' is not allowed in restricted language mode or a Data section. | 4 | `engine/parser/SemanticChecks.cs` |
| `ConfigurationInvalidPropertyName` | An attribute name for resource '{0}' was found that is not valid. An attribute name must be a simple string, and cannot contain variables or expressions. Replace '{1}' with a simple string. | 2 | `engine/parser/SemanticChecks.cs` |
| `ConfigurationNotSupportedInPowerShellCore` | Configuration keyword is not supported in PowerShell 6+. | 1 | `DscSupport/CimDSCParser.cs` |
| `ConstructorCantHaveReturnType` | A constructor cannot specify a return type. | 2 | `engine/parser/SemanticChecks.cs` |
| `ContinueHelpMessage` | Report the error then continue with the next script statement. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `ContinueLabel` | &Continue | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `ControlLeavingFinally` | Flow of control cannot leave a Finally block. | 2 | `engine/parser/SemanticChecks.cs` |
| `ConvertCimPropertyToObjectPropertyFailed` | Failed to convert the value of CimProperty {0} to the property value of class {1}. | 1 | `DscSupport/CimDSCParser.cs` |
| `CouldNotGetDispId` | Could not get dispatch ID for {0} (error: {1}). | 1 | `engine/ComInterop/Errors.cs` |
| `CustomAttributeTypeNotFound` | Cannot find the type for custom attribute '{0}'. Make sure that the assembly that contains this type is loaded. | 3 | `engine/parser/Compiler.cs`, `engine/parser/SymbolResolver.cs` |
| `CycleInEnumInitializers` | Cannot define enum because of a cycle in the initialization expressions. | 2 | `engine/parser/PSType.cs` |
| `DataSectionAllowedCommandDisallowed` | Cannot define data section. Definition of additional supported commands is not supported in this language mode. | 2 | `engine/parser/SemanticChecks.cs` |
| `DataSectionStatementNotSupportedInDataSection` | The data statement is not allowed in restricted language mode or another Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `DebugModeShouldHaveOneValue` | DebugMode should only have one value. | 1 | `DscSupport/CimDSCParser.cs` |
| `DefaultAllowedVariablesInDataSection` | $PSCulture, $PSUICulture, $true, $false, $null | 2 | `engine/MshCommandRuntime.cs`, `engine/parser/SemanticChecks.cs` |
| `DisabledRefreshModeNotValidForPartialConfig` | PartialConfiguration '{0}' has a Refresh Mode set to Disabled which is not a valid mode for Partial Configurations. Use Pull or Push refresh mode.  | 1 | `DscSupport/CimDSCParser.cs` |
| `DispBadParamCount` | Cannot find an overload for "{0}" and the argument count: "{1}" | 1 | `engine/ComInterop/Errors.cs` |
| `DispMemberNotFound` | Error while invoking {0}. Could not find member. | 1 | `engine/ComInterop/Errors.cs` |
| `DispNoNamedArgs` | Error while invoking {0}. Named arguments are not supported. | 1 | `engine/ComInterop/Errors.cs` |
| `DispOverflow` | Error while invoking {0}. Overflow detected. | 1 | `engine/ComInterop/Errors.cs` |
| `DispParamNotOptional` | Error while invoking {0}. A required parameter was omitted. | 1 | `engine/ComInterop/Errors.cs` |
| `DispTypeMismatch` | Exception setting "{0}": Cannot convert the "{1}" value of type "{2}" to type "{3}". | 1 | `engine/ComInterop/Errors.cs` |
| `DoWhileStatementNotSupportedInDataSection` | The Do and While statements are not allowed in restricted language mode or a Data section. | 4 | `engine/parser/SemanticChecks.cs` |
| `DotSourcingNotSupportedInDataSection` | Dot sourcing is not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `DscResourceInvalidGetMethod` | Invalid Get method. Get method must return [{0}] and accepts no parameters. | 4 | `engine/parser/SemanticChecks.cs` |
| `DscResourceInvalidKeyProperty` | Invalid key property. The key property must be of [string], signed/unsigned integer, or Enum types. | 2 | `engine/parser/SemanticChecks.cs` |
| `DscResourceMissingDefaultConstructor` | The DSC resource '{0}' has no default constructor. | 3 | `DscSupport/CimDSCParser.cs`, `engine/parser/SemanticChecks.cs` |
| `DscResourceMissingGetMethod` | The DSC resource '{0}' is missing a Get method that returns [{0}] and accepts no parameters. | 2 | `engine/parser/SemanticChecks.cs` |
| `DscResourceMissingKeyProperty` | The DSC resource '{0}' must have at least one key property (using the syntax [DscProperty(Key)].) | 2 | `engine/parser/SemanticChecks.cs` |
| `DscResourceMissingSetMethod` | The DSC resource '{0}' is missing a Set method that returns [void] and accepts no parameters. | 2 | `engine/parser/SemanticChecks.cs` |
| `DscResourceMissingTestMethod` | The DSC resource '{0}' is missing a Test method that returns [bool] and accepts no parameters. | 2 | `engine/parser/SemanticChecks.cs` |
| `DscResourcesNotFoundDuringParsing` | Unable to load resource '{0}': Resource not found. | 1 | `DscSupport/CimDSCParser.cs` |
| `DuplicateCimClassDefinition` | A second CIM class definition for '{0}' was found while processing the schema file '{1}'. This class was already defined in the file(s) '{2}'. Remove the redundant definition, and then try again. | 1 | `DscSupport/CimDSCParser.cs` |
| `DuplicateFormalParameter` | Duplicate parameter ${0} in parameter list. | 2 | `engine/parser/SemanticChecks.cs` |
| `DuplicateKeyInHashLiteral` | Duplicate keys '{0}' are not allowed in hash literals. | 3 | `engine/parser/SemanticChecks.cs`, `engine/runtime/Operations/MiscOps.cs` |
| `DuplicateKeywordDefinition` | Resource name '{0}' is already being used by another Resource or Configuration. | 1 | `DscSupport/CimDSCParser.cs` |
| `DuplicatePropertyInInstanceDefinition` | Duplicate property assignments are not allowed in an instance definition. | 2 | `engine/parser/SemanticChecks.cs` |
| `DuplicateResourceIdInNodeStatement` | A duplicate resource identifier '{0}' was found while processing the specification for node '{1}'. Change the name of this resource so that it is unique within the node specification. | 1 | `DscSupport/CimDSCParser.cs` |
| `DynamicKeywordSemanticCheckException` | Exception occurred when performing semantic check for dynamic keyword '{0}' with details '{1}'. | 2 | `engine/parser/SemanticChecks.cs` |
| `EmptyCatchNotLast` | Catch block must be the last catch block. | 2 | `engine/parser/SemanticChecks.cs` |
| `EmptyExpressionRequiresANonDefaultMode` | If the expression passed to the Where() operator is null then you must specify a non-Default value for the selection mode argument. Please change the value of the mode argument to a value other than Default and try running your script again. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `EmptyFunctionNameInFunctionDefinitionDictionary` | The key property for an entry in the dictionary of functions to define cannot be empty because the key property is used as the function name. Specify a non-empty string as the value of the key property, and then try the operation again. | 2 | `engine/lang/scriptblock.cs`, `engine/runtime/CompiledScriptBlock.cs` |
| `EnumeratorValueMustBeConstant` | Enumerator value must be a constant value. | 2 | `engine/parser/PSType.cs` |
| `EnumeratorValueOutOfBounds` | Enumerator value is either too large or too small for {0}. | 4 | `engine/parser/PSType.cs` |
| `ErrorCollection` | Parser errors were detected. | 0 |  |
| `ExceptionActionPromptCaption` | Action to take for this exception: | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `ExceptionParsingMOFFile` | Exception parsing MOF file '{0}':{1}. | 1 | `DscSupport/CimDSCParser.cs` |
| `ExceptionTypeAlreadyCaught` | Exception type {0} is already handled by a previous handler. | 2 | `engine/parser/SemanticChecks.cs` |
| `ExpandableStringNotSupportedInDataSection` | Expandable strings are not allowed in restricted language mode or a Data section. | 1 | `engine/parser/SemanticChecks.cs` |
| `ExpectArrayTypeOfPropertyInPSClass` | Property {0} of PowerShell class {1} is not declared as array type, but defined in its configuration instance as instance array type. | 1 | `DscSupport/CimDSCParser.cs` |
| `FailToParseModuleScriptFile` | Failed to parse module script file '{0}' with error '{1}'. | 1 | `DscSupport/CimDSCParser.cs` |
| `FileNotFound` | No files matching '{0}' were found. | 2 | `DscSupport/CimDSCParser.cs`, `engine/runtime/Operations/MiscOps.cs` |
| `FileOpenError` | The current provider ({0}) cannot open a file. | 4 | `engine/Modules/ModuleCmdletBase.cs`, `engine/Modules/TestModuleManifestCommand.cs`, `engine/remoting/commands/TestPSSessionConfigurationFile.cs` +1 |
| `FlowControlStatementNotSupportedInDataSection` | Flow control statements such as Break, Continue, Return, Exit, and Throw are not allowed in restricted language mode or a Data section. | 10 | `engine/parser/SemanticChecks.cs` |
| `ForEachBadGenericConversionTypeSpecified` | The generic collection type [{0}] passed to ForEach() has too many type arguments. Please change the specified type to be a generic collection with only one type argument then try running your script again. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `ForEachNonexistentMemberReference` | The ForEach() operator could not find a member '{0}' on the target object. Please verify that the named member exists and then try running your script again. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `ForEachNotSupportCleanBlock` | Script block with a 'clean' block is not supported by the 'ForEach' method. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `ForEachTypeConversionFailed` | Unable to convert input to the target type [{0}] passed to the ForEach() operator. Please check the specified type and try running your script again. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `ForWhileStatementNotSupportedInDataSection` | For and While statements are not allowed in restricted language mode or a Data section. | 4 | `engine/parser/SemanticChecks.cs` |
| `ForeachStatementNotSupportedInDataSection` | Foreach statements are not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `FormatError` | Error formatting a string: {0}. | 1 | `engine/runtime/Operations/StringOps.cs` |
| `FunctionDeclarationNotSupportedInDataSection` | Function declarations are not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `GetBadlyFormedExclusiveResourceId` | The format of the resource reference '{0}' in the exclusive list for resource '{1}' is not valid. An exclusive resource name should be in the format '<typename>\<name>', with no spaces. | 1 | `DscSupport/CimDSCParser.cs` |
| `GetBadlyFormedRequiredResourceId` | The format of the resource reference '{0}' in the Requires list for resource '{1}' is not valid. A required resource name should be in the format '[<typename>]<name>', with alphanumeric characters, spaces, '_', '-', '.' and '\'. | 1 | `DscSupport/CimDSCParser.cs` |
| `GetIDsOfNamesInvalid` | IDispatch::GetIDsOfNames behaved unexpectedly for {0}. | 1 | `engine/ComInterop/Errors.cs` |
| `GetPullModeNeedConfigurationSource` | The PartialConfiguration '{0}' is set to pull mode which requires a ConfigurationSource property. | 1 | `DscSupport/CimDSCParser.cs` |
| `GetSteppablePipelineFromWrongThread` | There is no Runspace available to get and run the SteppablePipeline in this thread. You can provide one in the DefaultRunspace property of the System.Management.Automation.Runspaces.Runspace type. The script block you attempted to get SteppablePipeline from was: {0} | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `HashtableToObjectConversionNotSupportedInDataSection` | Cannot convert hashtable to an object of the following type: {0}. Hashtable-to-Object conversion is not supported in restricted language mode or a Data section. | 1 | `engine/LanguagePrimitives.cs` |
| `ImportDscResourceInsideNode` | Import-DscResource cannot be specified inside of Node context | 1 | `DscSupport/CimDSCParser.cs` |
| `ImportDscResourceMultipleModulesNotSupportedWithName` | Import-DscResource dynamic keyword supports only one module when Name parameter is specified. | 1 | `DscSupport/CimDSCParser.cs` |
| `ImportDscResourceNeedParams` | The syntax of the Import-DscResource dynamic keyword is:  Import-DscResource  [-Name <ResourceName(s)>]  [-ModuleName  <ModuleName(s)>] [-ModuleVersion <ModuleVersion>].  Name          : Names of one or more resources to import. ModuleName    : Module names or ModuleSpecification objects of one or more modules to import. ModuleVersion : Version of module to import. If used, ModuleName must represent only one module by name. | 5 | `DscSupport/CimDSCParser.cs` |
| `ImportDscResourcePositionalParamsNotSupported` | Positional parameters are not supported for the Import-DscResource dynamic keyword. The syntax of Import-DscResource dynamic keyword is: "Import-DscResource  [-Name <ResourceName(s)>] [-ModuleName <ModuleName(s)>] [-ModuleVersion <ModuleVersion>] | 1 | `DscSupport/CimDSCParser.cs` |
| `IndexOutOfRange` | Array assignment failed because index '{0}' was out of range. | 0 |  |
| `InstantiatePSClassObjectFailed` | Failed to create an object of PowerShell class {0}. | 1 | `DscSupport/CimDSCParser.cs` |
| `InterfaceNameExpected` | '{0}': Interface name expected. | 2 | `engine/parser/PSType.cs` |
| `InvalidComObjectException` | A COM object was accessed after it was already released: {0} | 1 | `engine/CommandProcessorBase.cs` |
| `InvalidEndOfLine` | The token '{0}' is not a valid statement separator in this version. | 2 | `engine/parser/SemanticChecks.cs` |
| `InvalidFilenameOption` | The file name argument to -file in the switch statement is not valid. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `InvalidHashtable` | The hashtable supplied to the Desired State Configuration resource {0} is not valid. The key or value cannot be null or empty. | 2 | `DscSupport/CimDSCParser.cs` |
| `InvalidInstanceProperty` | The member '{0}' is not valid. Valid members are '{1}'. | 2 | `engine/parser/SemanticChecks.cs` |
| `InvalidLeftHandSide` | The assignment expression is not valid. The input to an assignment operator must be an object that is able to accept assignments, such as a variable or a property. | 2 | `engine/parser/SemanticChecks.cs` |
| `InvalidLocalConfigurationManagerProperty` | '{0}' cannot be specified in LocalConfigurationManager resource. Please switch to Settings instead or use only following values: {1}. | 1 | `DscSupport/CimDSCParser.cs` |
| `InvalidNamespaceValue` | The specified namespace in the 'using' statement contains invalid characters. | 2 | `engine/parser/SemanticChecks.cs` |
| `InvalidNullKey` | A null key is not allowed in a hash literal. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `InvalidParameter` | Parameter '{0}' is not valid | 0 |  |
| `InvalidPassword` | The username supplied to the Desired State Configuration resource {0} is not valid. The username cannot be null or empty. | 2 | `DscSupport/CimDSCParser.cs` |
| `InvalidPowerShellDataFile` | The PowerShell data file '{0}' is invalid since it cannot be evaluated into a Hashtable object. | 3 | `utils/PsUtils.cs` |
| `InvalidRegularExpression` | The regular expression pattern {0} is not valid. | 2 | `engine/lang/parserutils.cs`, `engine/runtime/Operations/MiscOps.cs` |
| `InvalidScriptBlockInDataSection` | A Begin statement block, Process statement block, or parameter statement is not allowed in a Data section. | 2 | `engine/runtime/CompiledScriptBlock.cs` |
| `InvalidSplitOptionCombination` | The combination of options with the -split operator is not valid. | 1 | `engine/lang/parserutils.cs` |
| `InvalidSplitOptionWithPredicate` | Options are not allowed on the -split operator with a predicate. | 1 | `engine/lang/parserutils.cs` |
| `InvalidUserName` | The username supplied to the Desired State Configuration resource {0} is not valid. The username cannot be null or empty. | 2 | `DscSupport/CimDSCParser.cs` |
| `InvalidUsingExpression` | Expression is not allowed in a Using expression. | 2 | `engine/parser/SemanticChecks.cs` |
| `InvalidValueForProperty` | '{0}' is not a valid value for property '{1}' on class '{2}'. Please change the value to one of the following strings: {3}. | 1 | `DscSupport/CimDSCParser.cs` |
| `InvokeMethodConstrainedLanguage` | Cannot invoke method. Method invocation is supported only on core types in this language mode. | 3 | `engine/InternalCommands.cs`, `engine/runtime/Binding/Binders.cs`, `engine/runtime/Operations/MiscOps.cs` |
| `InvokeMethodOnNull` | You cannot call a method on a null-valued expression. | 4 | `engine/InternalCommands.cs`, `engine/lang/parserutils.cs`, `engine/runtime/Binding/Binders.cs` |
| `InvokingCleanBlockNotSupported` | Directly invoking the 'clean' block of a script block is not supported. | 1 | `engine/runtime/CompiledScriptBlock.cs` |
| `IsOperatorRequiresType` | The right operand of '-is' must be a type. | 3 | `engine/lang/parserutils.cs`, `engine/runtime/Operations/MiscOps.cs` |
| `KeywordParameterReservedForFutureUse` | The {0} '-{1}' parameter is reserved for future use. | 6 | `engine/parser/SemanticChecks.cs` |
| `LabelNotFound` | Label '{0}' not found inside the method. | 2 | `engine/parser/SemanticChecks.cs` |
| `MemberAlreadyDefined` | The member '{0}' is already defined. | 10 | `engine/parser/PSType.cs` |
| `MetaConfigurationUsedInRegularConfig` | Meta Configuration resource {0} is not allowed in the regular configuration. Use meta configuration resources in a configuration with [DscLocalConfigurationManager()] attribute. | 2 | `engine/parser/SemanticChecks.cs` |
| `MethodCallNotSupportedInDataSection` | Method calls are not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `MethodHasCodePathNotReturn` | Not all code path returns value within method. | 2 | `engine/parser/SemanticChecks.cs` |
| `MethodNotFound` | Method invocation failed because [{0}] does not contain a method named '{1}'. | 8 | `engine/runtime/Binding/Binders.cs` |
| `MissingThis` | Cannot assign property, use '{0}{1}'. | 2 | `engine/parser/SymbolResolver.cs` |
| `MissingTryStatement` | Incomplete 'try' statement. A try statement requires a body. | 0 |  |
| `MissingTypeInStaticPropertyAssignment` | Cannot assign property, use '{0}{1}'. | 2 | `engine/parser/SymbolResolver.cs` |
| `MissingValueForMandatoryProperty` | Resource '{0}' requires that a value of type '{1}' be provided for property '{2}'. | 2 | `DscSupport/CimDSCParser.cs` |
| `ModuleNotFoundDuringParse` | Could not find the module '{0}'. | 3 | `DscSupport/CimDSCParser.cs`, `engine/parser/SymbolResolver.cs` |
| `MultipleModuleEntriesFoundDuringParse` | Multiple versions of the module '{0}' were found. You can run 'Get-Module -ListAvailable -FullyQualifiedName {0}' to see available versions on the system, and then use the fully qualified name '@{{ModuleName="{0}"; RequiredVersion="Version"}}'. | 1 | `DscSupport/CimDSCParser.cs` |
| `MultipleTypeConstraintsOnMethodParam` | Multiple type constraints are not allowed on a method parameter. | 2 | `engine/parser/SemanticChecks.cs` |
| `NamedBlockNotAllowedInMethod` | A named block is not allowed in a class method. | 2 | `engine/parser/SemanticChecks.cs` |
| `NeedMultidimensionalIndex` | You cannot index into a {0} dimensional array with index [{1}]. | 4 | `engine/runtime/Binding/Binders.cs`, `engine/runtime/Operations/ArrayOps.cs` |
| `NonExistingVariableReference` | [ref] cannot be applied to a variable that does not exist. | 1 | `engine/runtime/Operations/VariableOps.cs` |
| `NonStaticMemberAccessInStaticMember` | Cannot access the non-static member '{0}' in a static method or initializer of a static property. | 2 | `engine/parser/SemanticChecks.cs` |
| `NonVoidMethodMissingReturnValue` | Invalid return statement within non-void method. | 2 | `engine/parser/SemanticChecks.cs` |
| `NotADefinedOperationForType` | The operation '[{0}] {1} [{2}]' is not defined. | 1 | `engine/lang/parserutils.cs` |
| `NullArray` | Cannot index into a null array. | 2 | `engine/runtime/Binding/Binders.cs` |
| `NullArrayIndex` | Index operation failed; the array index evaluated to null. | 2 | `engine/runtime/Binding/Binders.cs` |
| `NullEntryInVariablesDefinitionList` | A null entry was found in the list of variable entries to create in the script block scope. Remove the entry at index {0}, or replace it with a non-null entry, and then try again. | 1 | `engine/runtime/CompiledScriptBlock.cs` |
| `NullFunctionBodyInFunctionDefinitionDictionary` | The script block that defines function '{0}' cannot be null or empty. Provide a non-empty script block in the function definition dictionary, and then try the operation again. | 1 | `engine/runtime/CompiledScriptBlock.cs` |
| `NumberToReturnMustBeGreaterThanZero` | The 'numberToReturn' value provided to the third argument of the Where() operator must be greater than zero. Please correct the argument's value and try running your script again. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `OnlyOneParameterListAllowed` | The param statement cannot be used if arguments were specified in the function declaration. | 2 | `engine/parser/SemanticChecks.cs` |
| `OperatorFailed` | The '{0}' operator failed: {1}. | 1 | `engine/InternalCommands.cs` |
| `OperatorNotSupportedInDataSection` | The '{0}' operator is not allowed in restricted language mode or a Data section. | 6 | `engine/parser/SemanticChecks.cs` |
| `OperatorRequiresNumber` | The '{0}' operator works only on numbers. The operand is a '{1}'. | 1 | `engine/runtime/Binding/Binders.cs` |
| `OperatorRequiresVariableOrProperty` | The '{0}' operator works only on variables or on properties. | 2 | `engine/parser/SemanticChecks.cs` |
| `OrderedAttributeOnlyOnHashLiteralNode` | The {0} attribute can be specified only on a hash literal node. | 4 | `engine/parser/SemanticChecks.cs` |
| `ParallelAndSequenceBlockNotSupportedInDataSection` | Parallel and sequence blocks are not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `ParamBlockNotAllowedInMethod` | A param block is not allowed in a class method. | 2 | `engine/parser/SemanticChecks.cs` |
| `ParameterAttributeArgumentNeedsToBeConstant` | Attribute argument must be a constant. | 2 | `engine/parser/SemanticChecks.cs` |
| `ParameterAttributeArgumentNeedsToBeConstantOrScriptBlock` | Attribute argument must be a constant or a script block. | 2 | `engine/parser/SemanticChecks.cs` |
| `ParameterDeclarationNotSupportedInDataSection` | Parameter declarations are not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `ParameterizedPropertyAssignmentFailed` | Assignment failed because [{0}] does not contain a property '{1}()' that can be set. | 2 | `engine/lang/parserutils.cs` |
| `ProgramFailedToExecute` | Program '{0}' failed to run: {1}{2}. | 2 | `engine/NativeCommandProcessor.cs` |
| `PropertyInGenericType` | '{0}' is defined in a generic type. | 3 | `engine/CoreAdapter.cs` |
| `PropertyIsReadOnly` | '{0}' is a ReadOnly property. | 4 | `engine/CoreAdapter.cs`, `engine/runtime/Binding/Binders.cs` |
| `PropertyNotDeclaredInPSClass` | Property {0} is not declared in PowerShell class {1}, but defined in its configuration instance. | 1 | `DscSupport/CimDSCParser.cs` |
| `PropertyNotFound` | The property '{0}' cannot be found on this object. Verify that the property exists and can be set. | 3 | `engine/runtime/Binding/Binders.cs` |
| `PropertyNotFoundForAttribute` | Property '{0}' cannot be found for attribute '{1}'. Specify one of the following properties: {2}. | 2 | `engine/parser/SemanticChecks.cs` |
| `PropertyNotFoundForType` | Property '{0}' cannot be found for type '{1}'. | 6 | `engine/parser/Compiler.cs`, `engine/runtime/Binding/Binders.cs` |
| `PropertyNotFoundStrict` | The property '{0}' cannot be found on this object. Verify that the property exists. | 5 | `engine/runtime/Binding/Binders.cs`, `engine/runtime/Operations/MiscOps.cs` |
| `PropertyReferenceNotSupportedInDataSection` | Property references are not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `PropertySetConstrainedLanguage` | Cannot set property. Property setting is supported only on core types in this language mode. | 3 | `engine/runtime/Binding/Binders.cs`, `engine/runtime/Operations/MiscOps.cs` |
| `PsDscMissingSchemaStore` | Unable to find DSC schema store at "{0}". Please ensure PSDesiredStateConfiguration v3 module is installed. | 0 |  |
| `PsDscRunAsCredentialMergeErrorForCompositeResources` | Conflict in using PsDscRunAsCredential for Resource {0} because it already specifies PsDscRunAsCredential value. We can only use one PsDscRunAsCredential for the composite resource.  | 1 | `DscSupport/CimDSCParser.cs` |
| `RedirectionFailed` | Redirection to '{0}' failed: {1} | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `RedirectionNotSupportedInDataSection` | Redirection is not allowed in restricted language mode or a Data section. | 4 | `engine/parser/SemanticChecks.cs` |
| `RedirectionStreamCanOnlyMergeToOutputStream` | Redirection only allows another stream to be merged with the output stream. Please correct the redirection operation to merge into the output stream then try running your script again. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `ReferenceNeedsToBeByItselfInTypeConstraint` | Cannot use [ref] with other types in a type constraint. | 2 | `engine/parser/SemanticChecks.cs` |
| `ReferenceNeedsToBeByItselfInTypeSequence` | Cannot have two occurrences of [ref] in a type sequence. | 2 | `engine/parser/SemanticChecks.cs` |
| `ReferenceNeedsToBeLastTypeInTypeConversion` | [ref] can only be the final type in type conversion sequence. | 2 | `engine/parser/SemanticChecks.cs` |
| `RegularResourceUsedInMetaConfig` | Regular DSC resource {0} is not allowed in the meta configuration.  | 2 | `engine/parser/SemanticChecks.cs` |
| `ResourceNotDefined` | Undefined DSC resource '{0}'. Use Import-DSCResource to import the resource. | 2 | `engine/parser/SemanticChecks.cs` |
| `SchemaFileNotFound` | The schema file {0} was not found. Verify that any modules specified in a configuration statement contain a schema.mof file, and then try running the script again. | 2 | `DscSupport/CimDSCParser.cs` |
| `ScriptBlockDelegateInvokedFromWrongThread` | There is no Runspace available to run scripts in this thread. You can provide one in the DefaultRunspace property of the System.Management.Automation.Runspaces.Runspace type. The script block you attempted to invoke was: {0} | 1 | `engine/lang/scriptblock.cs` |
| `ScriptBlockNotSupportedInDataSection` | Script block literals are not allowed in restricted language mode or a Data section. | 4 | `engine/parser/SemanticChecks.cs` |
| `ScriptContainedMaliciousContent` | This script contains malicious content and has been blocked by your antivirus software. | 2 | `engine/runtime/CompiledScriptBlock.cs`, `security/SecuritySupport.cs` |
| `ScriptHasAdminBlockedContent` | This script contains content that has been flagged as suspicious through a policy setting and has been blocked with error code {0}. Contact your administrator for more information. | 1 | `engine/runtime/CompiledScriptBlock.cs` |
| `ScriptsNotAllowed` | The syntax is not supported by this runspace. This can occur if the runspace is in no-language mode. | 1 | `engine/hostifaces/Command.cs` |
| `SealedBaseClass` | Cannot inherit from sealed class '{0}'. | 2 | `engine/parser/PSType.cs` |
| `SetComObjectDataFailed` | Marshal.SetComObjectData failed. | 1 | `engine/ComInterop/Errors.cs` |
| `SilentlyContinueHelpMessage` | Do not report this error, just continue with the next script statement. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `SilentlyContinueLabel` | S&ilently Continue | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `SplattingNotPermitted` | The splatting operator '@' cannot be used to reference variables in an expression. '@{0}' can be used only as an argument to a command. To reference variables in an expression use '${0}'. | 2 | `engine/parser/SemanticChecks.cs` |
| `SplattingNotPermittedInArgumentList` | Splatted variables like '@{0}' cannot be part of a comma-separated list of arguments. | 2 | `engine/parser/SemanticChecks.cs` |
| `StaticConstructorCantHaveParameters` | A static constructor cannot have any parameters. | 2 | `engine/parser/PSType.cs` |
| `StrictModeFunctionCallWithParens` | The function or command was called as if it were a method. Parameters should be separated by spaces. For information about parameters, see the about_Parameters Help topic. | 1 | `engine/parser/Compiler.cs` |
| `StringMultiplyToolongInDataSection` | String multiplication results with more than "{0}" characters are not allowed in restricted language mode or a Data section. | 1 | `engine/runtime/Operations/StringOps.cs` |
| `SubtypeArray` | Invalid base type '{0}'. Base type cannot be an array. | 6 | `engine/parser/PSType.cs` |
| `SubtypeUnclosedGeneric` | Invalid base type '{0}'. Base type cannot be a generic with unspecified parameters. | 2 | `engine/parser/PSType.cs` |
| `SuspendHelpMessage` | Pause the current pipeline and return to the command prompt. Type exit to resume operation when you are done. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `SuspendLabel` | &Suspend | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `SwitchStatementNotSupportedInDataSection` | The switch statement is not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `TextForPositionMessage` | At {0}:{1} char:{2} + {3} | 1 | `engine/parser/Position.cs` |
| `TextForWordLine` | line | 1 | `engine/parser/Position.cs` |
| `ThrottleLimitRequiresParallelFlag` | The ThrottleLimit parameter is only supported on foreach statements that use the Parallel parameter. | 2 | `engine/parser/SemanticChecks.cs` |
| `TooManyErrors` | Not all parse errors were reported.  Correct the reported errors and try again. | 1 | `utils/ParserException.cs` |
| `TraceEnteringFunction` |     ! CALL function '{0}' | 1 | `engine/debugger/debugger.cs` |
| `TraceEnteringFunctionDefinedInFile` |     ! CALL function '{0}'  (defined in file '{1}') | 1 | `engine/debugger/debugger.cs` |
| `TraceMethodCall` |     ! CALL method '{0}' | 1 | `engine/CoreAdapter.cs` |
| `TraceScriptLineMessage` | {0,4}+ {1} | 1 | `engine/parser/Position.cs` |
| `TraceVariableAssignment` |     ! SET ${0} = '{1}'. | 1 | `engine/debugger/debugger.cs` |
| `TrapStatementNotSupportedInDataSection` | The Trap statement is not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `TryStatementNotSupportedInDataSection` | The Try statement is not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `TypeCreationError` | Error during creation of type "{0}". Error message: {1} | 2 | `engine/parser/PSType.cs` |
| `TypeNotAllowedForParameter` | The type '{0}' is not allowed on a parameter. | 2 | `engine/parser/PSType.cs` |
| `TypeNotAllowedForProperty` | The type '{0}' is not allowed on a property. | 2 | `engine/parser/SemanticChecks.cs` |
| `TypeNotAllowedInDataSection` | The type {0} is not allowed in restricted language mode or a Data section. | 2 | `engine/parser/SemanticChecks.cs` |
| `TypeNotFound` | Unable to find type [{0}]. | 14 | `engine/TypeTable.cs`, `engine/parser/PSType.cs` |
| `TypeNotFoundWithMessage` | Unable to find type [{0}]. Details: {1} | 2 | `engine/runtime/Operations/MiscOps.cs` |
| `UnexpectedKeyword` | Unexpected keyword '{0}'. | 2 | `engine/parser/SemanticChecks.cs` |
| `UnexpectedVarEnum` | Unexpected VarEnum {0}. | 1 | `engine/ComInterop/Errors.cs` |
| `UnsupportedHandlerType` | Attempting to pass an event handler of an unsupported type. | 1 | `engine/ComInterop/Errors.cs` |
| `UnsupportedNamedBlockInConfiguration` | Configuration only supports the End block in its body. Begin, Process and DynamicParam blocks are not allowed in a configuration. | 2 | `engine/parser/SemanticChecks.cs` |
| `UnsupportedPropertyTypeOfDSCResourceClass` | The '{0}' property with type '{1}' of DSC resource class '{2}' is not supported. | 2 | `DscSupport/CimDSCParser.cs` |
| `UnsupportedValueForProperty` | At least one of the values '{0}' is not supported or valid for property '{1}' on class '{2}'. Please specify only supported values: {3}. | 1 | `DscSupport/CimDSCParser.cs` |
| `UsingStatementNotSupported` | This syntax of the 'using' statement is not supported. | 2 | `engine/parser/SemanticChecks.cs` |
| `UsingWithoutInvokeCommand` | A Using variable cannot be retrieved. A Using variable can be used only with Invoke-Command, Start-Job, or InlineScript in the script workflow. When it is used with Invoke-Command, the Using variable is valid only if the script block is invoked on a remote computer. | 1 | `engine/runtime/Operations/VariableOps.cs` |
| `ValueNotInRange` | Property '{0}' of Resource '{1}' has value '{2}' which is not between valid range '{3}' and '{4}'. | 1 | `DscSupport/CimDSCParser.cs` |
| `VariableIsUndefined` | The variable '${0}' cannot be retrieved because it has not been set. | 2 | `engine/runtime/Operations/VariableOps.cs` |
| `VariableNotLocal` | Variable is not assigned in the method. | 2 | `engine/parser/SemanticChecks.cs` |
| `VariableReferenceNotSupportedInDataSection` | A variable that cannot be referenced in restricted language mode or a Data section is being referenced. Variables that can be referenced include the following: {0}. | 3 | `engine/MshCommandRuntime.cs`, `engine/parser/SemanticChecks.cs` |
| `VoidMethodHasReturn` | Invalid return statement within void method. | 2 | `engine/parser/SemanticChecks.cs` |
| `VoidTypeConstraintNotAllowed` | [void] cannot be used as a parameter type, or on the left side of an assignment. | 4 | `engine/parser/SemanticChecks.cs` |
| `WDACGetSteppablePipelineLogMessage` | Creating a steppable pipeline from a script block may require evaluating some expressions within the script block. The expression evaluation will silently fail and return 'null' in Constrained Language mode, unless the expression represents a constant value. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `WDACGetSteppablePipelineLogTitle` | Expression Evaluation May Fail | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `WDACParserDSSupportedCommandLogMessage` | The Data Section that includes the SupportedCommand parameter would be disallowed in Constrained Language mode for untrusted script. | 1 | `engine/parser/SemanticChecks.cs` |
| `WDACParserDSSupportedCommandLogTitle` | Parser Data Section SupportedCommand | 1 | `engine/parser/SemanticChecks.cs` |
| `WDACParserForEachOperatorLogMessage` | The ForEach keyword will fail '{0}' iteration item method invocation when run in Constrained Language mode. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `WDACParserForEachOperatorLogTitle` | ForEach Keyword Method Invocation | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `WDACParserModuleScopeCallOperatorLogMessage` | The module scope call operator will be denied in Constrained Language mode. | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `WDACParserModuleScopeCallOperatorLogTitle` | Module Scope Call Operator | 1 | `engine/runtime/Operations/MiscOps.cs` |
| `WildCardModuleNameError` | Wildcard characters are not supported for module names. | 2 | `engine/parser/SymbolResolver.cs` |
| `WorkflowNotSupportedInPowerShellCore` | Workflow is not supported in PowerShell 6+. | 2 | `engine/parser/SemanticChecks.cs` |

Rows: **255** (`GENERATED`). Keys with use count 0 have no reference found by the dataset scan (dead or referenced reflectively: `UNVERIFIED`).

## 5. Cross-checks

`ParserStrings` is not the only resource class a parser error ID can come from: the debug-only check `AssertErrorIdCorrespondsToMsgString` looks the ID up in `ParserStrings`, `DiscoveryExceptions`, `ExtendedTypeSystem`, `MshSnapInCmdletResources` and `ParameterBinderStrings` (`FACT-SRC`, `src/System.Management.Automation/engine/parser/Parser.cs::Parser.AssertErrorIdCorrespondsToMsgString@L8065-L8093`). Only `ParserStrings` is cataloged here.

Verification: key count taken from `data/resources.json` (`ParserStrings.resx`, key_count 412) and reconciled with the `<data>` element count of the resx parsed with `xml.etree` (`412`); every row has a message from the resx.

