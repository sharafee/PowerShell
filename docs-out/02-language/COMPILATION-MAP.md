---
id: LANG-COMPMAP-001
title: Compilation map
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/parser/Compiler.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/parser/_folder.md]
generated_from: [data/members-tierA.json]
---

# Compilation map

> STATIC-ONLY — behavior not run-verified. Rows are `GENERATED` by `docs-out/tools/gen_T25.py`: method names and line ranges from `data/members-tierA.json` (`APPROX`), the "compiled form" text from the hand-written annotation file `docs-out/tools/annotations/T25-compilation-map.json` (`FACT-SRC`, read in `Compiler.cs`). Narrative: [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md). Intermediate representation: [IR-SPEC.md](IR-SPEC.md).

## 1. Purpose and scope [SPEC]

For every AST node type, how `Compiler` (an `ICustomAstVisitor2`) turns it into a LINQ expression tree. `Compiler` has <!--N:COMPILER_VISIT_METHODS-->63<!--/N--> `Visit*` methods (one per visitor method of `ICustomAstVisitor` plus `ICustomAstVisitor2`, see [AST-CATALOG.md](AST-CATALOG.md) §5) and <!--N:COMPILER_HELPER_METHODS-->99<!--/N--> other methods (section 4).

## 2. Source map

| path | type | role |
|---|---|---|
| `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler@L818-L6658` | class | AST → expression-tree compiler |

## 3. Node → compiled form

| AST node (Visit method) | Compiled form | How (FACT-SRC) | Source |
|---|---|---|---|
| `ErrorStatementAst` (`VisitErrorStatement`) | not compiled | returns null; error nodes never reach the compiler because a script with parse errors cannot be turned into a script block | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitErrorStatement@L2438-L2441` |
| `ErrorExpressionAst` (`VisitErrorExpression`) | constant | returns Constant(1); placeholder | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitErrorExpression@L2443-L2446` |
| `ScriptBlockAst` (`VisitScriptBlock`) | five lambdas | builds one Expression<Action<FunctionContext>> per named block (DynamicParam, Begin, Process, End, Clean); function name suffixes `<Begin>` etc.; param block is not compiled (defaults come from parameter metadata); the first compiled block also defines classes/usings when the script block is the root | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitScriptBlock@L2450-L2502` |
| `TypeConstraintAst` (`VisitTypeConstraint`) | not visited | assert false; type constraints are handled by their parents | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitTypeConstraint@L2995-L2999` |
| `AttributeAst` (`VisitAttribute`) | not visited | assert false; attributes are turned into attribute objects by GetAttribute at metadata time | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitAttribute@L3001-L3005` |
| `NamedAttributeArgumentAst` (`VisitNamedAttributeArgument`) | not visited | assert false | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitNamedAttributeArgument@L3007-L3011` |
| `ParameterAst` (`VisitParameter`) | not visited | assert false; parameters become RuntimeDefinedParameter metadata (GetParameterMetaData) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitParameter@L3013-L3017` |
| `ParamBlockAst` (`VisitParamBlock`) | not visited | assert false | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitParamBlock@L3019-L3023` |
| `NamedBlockAst` (`VisitNamedBlock`) | not visited | assert false; CompileNamedBlock is called from VisitScriptBlock | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitNamedBlock@L3025-L3029` |
| `StatementBlockAst` (`VisitStatementBlock`) | statement list | CompileStatementListWithTraps -> Block (Empty if no statements); each statement wrapped for error-action handling | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitStatementBlock@L3031-L3042` |
| `TypeDefinitionAst` (`VisitTypeDefinition`) | empty | Empty; types are defined by GenerateTypesAndUsings for the root block | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitTypeDefinition@L3425-L3428` |
| `PropertyMemberAst` (`VisitPropertyMember`) | not compiled | returns null | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitPropertyMember@L3430-L3433` |
| `FunctionMemberAst` (`VisitFunctionMember`) | not compiled | returns null; member bodies are compiled as separate script blocks with member-function mode | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitFunctionMember@L3435-L3438` |
| `BaseCtorInvokeMemberExpressionAst` (`VisitBaseCtorInvokeMemberExpression`) | call | InvokeBaseCtorMethod: dynamic site with PSInvokeBaseCtorBinder | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitBaseCtorInvokeMemberExpression@L3440-L3446` |
| `UsingStatementAst` (`VisitUsingStatement`) | empty | Empty; usings are loaded by GenerateLoadUsings in the root prolog | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitUsingStatement@L3448-L3451` |
| `ConfigurationDefinitionAst` (`VisitConfigurationDefinition`) | synthesized pipeline | compiles the AST built by GenerateSetItemPipelineAst (set-item function:<name>); DSC, out of scope | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitConfigurationDefinition@L3453-L3456` |
| `DynamicKeywordStatementAst` (`VisitDynamicKeywordStatement`) | synthesized pipeline | meta statements -> Empty; otherwise compiles the AST built by GenerateCommandCallPipelineAst; DSC, out of scope | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitDynamicKeywordStatement@L3458-L3466` |
| `FunctionDefinitionAst` (`VisitFunctionDefinition`) | runtime call | FunctionOps.DefineFunction(context, ast, ScriptBlockExpressionWrapper); the function body is not compiled with the parent, only when the wrapper's script block first runs | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitFunctionDefinition@L3468-L3475` |
| `IfStatementAst` (`VisitIfStatement`) | conditional | nested Expression.IfThenElse from last clause to first; condition = CaptureStatementResults(cond, Condition) converted to bool; position update before each condition | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitIfStatement@L3477-L3514` |
| `TrapAst` (`VisitTrap`) | not visited | assert false; traps are compiled by CompileTrap from statement lists | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitTrap@L3516-L3520` |
| `AssignmentStatementAst` (`VisitAssignmentStatement`) | assignment | CompileAssignment: destructuring (array LHS) uses PSArrayAssignmentRHSBinder; otherwise ReduceAssignment through IAssignableValue (SetValue / dynamic binary op for +=, -=, ...) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitAssignmentStatement@L3522-L3525` |
| `PipelineChainAst` (`VisitPipelineChain`) | dispatch loop | && / \|\| over pipelines: statement-index dispatch with try/catch (like statement lists), `if ($?)` / `if (-not $?)` between elements, background chains call PipelineOps.InvokePipelineInBackground; no trap handlers are pushed | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitPipelineChain@L3565-L3717` |
| `PipelineAst` (`VisitPipeline`) | runtime call | single expression -> compiled expression (with redirections via GetRedirectedExpression); otherwise PipelineOps.InvokePipeline(input, ignoreInput, CommandParameterInternal[][] per command, command asts, redirections, funcContext); background -> InvokePipelineInBackground; position update unless parent is assignment/paren | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitPipeline@L3736-L3866` |
| `MergingRedirectionAst` (`VisitMergingRedirection`) | runtime object | returns a MergingRedirection value (not an Expression) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitMergingRedirection@L4140-L4147` |
| `FileRedirectionAst` (`VisitFileRedirection`) | new object | Expression.New(FileRedirection(stream, append, fileName)); non-constant file names converted with PSToStringBinder | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitFileRedirection@L4149-L4175` |
| `CommandAst` (`VisitCommand`) | array of arguments | NewArrayInit(CommandParameterInternal[]): first element is the command name argument, then parameters/arguments; numeric literals keep their source text (WrappedNumber); strict-mode check for `f (args)` call syntax | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitCommand@L4177-L4237` |
| `CommandExpressionAst` (`VisitCommandExpression`) | expression + output | compile expression; unless pre/post increment or void, write value to funcContext._outputPipe (CallAddPipe) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitCommandExpression@L4268-L4279` |
| `CommandParameterAst` (`VisitCommandParameter`) | argument object | CommandParameterInternal.CreateParameter / CreateParameterWithArgument | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitCommandParameter@L4281-L4305` |
| `SwitchStatementAst` (`VisitSwitchStatement`) | loop | saves/restores `$_`; -file reads lines with StreamReader; otherwise GenerateIteratorStatement with `$switch`; per item every clause is tested (constant script block, regex, wildcard, exact string, or PSSwitchClauseEvalBinder) - all matching clauses run; default clause when none matched | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitSwitchStatement@L4410-L4542` |
| `DataStatementAst` (`VisitDataStatement`) | try/finally | sets context.LanguageMode to RestrictedLanguage around the body, runtime checks for allowed commands, assigns result to the data variable | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitDataStatement@L4649-L4729` |
| `ForEachStatementAst` (`VisitForEachStatement`) | loop | GenerateIteratorStatement with `$foreach`; enumerator via PSEnumerableBinder; body assigns the loop variable then runs the body | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitForEachStatement@L5058-L5088` |
| `DoWhileStatementAst` (`VisitDoWhileStatement`) | loop | GenerateDoLoop: body, then test; jump back while true | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitDoWhileStatement@L5123-L5126` |
| `DoUntilStatementAst` (`VisitDoUntilStatement`) | loop | GenerateDoLoop with the test negated | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitDoUntilStatement@L5128-L5131` |
| `ForStatementAst` (`VisitForStatement`) | loop | initializer; GenerateWhileLoop with condition and iterator as the `continue` action | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitForStatement@L5133-L5161` |
| `WhileStatementAst` (`VisitWhileStatement`) | loop | GenerateWhileLoop | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitWhileStatement@L5163-L5170` |
| `CatchClauseAst` (`VisitCatchClause`) | not visited | assert false; catch bodies are compiled by VisitTryStatement | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitCatchClause@L5172-L5176` |
| `TryStatementAst` (`VisitTryStatement`) | try/catch/finally | ExpressionType.Try; catch-all-only form catches RuntimeException (PipelineStoppedException rethrown), typed catches use ExceptionHandlingOps.FindMatchingHandler + switch; `$_` set to the ErrorRecord; finally wraps SuspendStoppingPipeline/RestoreStoppingPipeline | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitTryStatement@L5247-L5509` |
| `BreakStatementAst` (`VisitBreakStatement`) | goto or throw | GenerateBreakOrContinue: Expression.Break to the matching compiled loop label, else throw BreakException(label) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitBreakStatement@L5553-L5561` |
| `ContinueStatementAst` (`VisitContinueStatement`) | goto or throw | same, with ContinueException | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitContinueStatement@L5563-L5571` |
| `ReturnStatementAst` (`VisitReturnStatement`) | return label | writes the value to the output pipe (or return pipe in class methods) then Expression.Return to the block's return label; inside a trap lambda throws ReturnException | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitReturnStatement@L5573-L5627` |
| `ExitStatementAst` (`VisitExitStatement`) | throw | throws the exception from PipelineOps.GetExitException(code) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitExitStatement@L5629-L5641` |
| `ThrowStatementAst` (`VisitThrowStatement`) | throw | ExceptionHandlingOps.ConvertToException(value, extent, isRethrow); `throw` with no value rethrows the exception being handled | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitThrowStatement@L5643-L5659` |
| `TernaryExpressionAst` (`VisitTernaryExpression`) | conditional | Expression.Condition(cond as bool, ifTrue as object, ifFalse as object) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitTernaryExpression@L5677-L5685` |
| `BinaryExpressionAst` (`VisitBinaryExpression`) | operator call or dynamic site | constant-folded when constant; -and/-or -> AndAlso/OrElse over bool; double,double + - * / native; other arithmetic and comparisons via DynamicExpression with PSBinaryOperationBinder; -like/-match/-replace/-split/-join/-contains/-in/-is/-as/-f/.. -> ParserOps/StringOps/TypeOps helper calls; ?? -> Coalesce | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitBinaryExpression@L5687-L5977` |
| `UnaryExpressionAst` (`VisitUnaryExpression`) | operator call or dynamic site | constant-folded when constant; -not/! PSUnaryOperationBinder; unary +/- as 0+x / 0-x; -bnot OnesComplement; ++/-- CompileIncrementOrDecrement; unary -join/-split helper calls | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitUnaryExpression@L5994-L6051` |
| `ConvertExpressionAst` (`VisitConvertExpression`) | conversion | constant-folded; [ordered]@{} -> OrderedDictionary; [pscustomobject]@{} -> converter; [ref]$x -> VariableOps.GetVariableAsRef; otherwise ConvertValue: Expression.Convert or PSConvertBinder, PSDynamicConvertBinder when the type is unresolved at compile time | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitConvertExpression@L6102-L6164` |
| `ConstantExpressionAst` (`VisitConstantExpression`) | constant | Expression.Constant(value) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitConstantExpression@L6166-L6169` |
| `StringConstantExpressionAst` (`VisitStringConstantExpression`) | constant | Expression.Constant(value) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitStringConstantExpression@L6171-L6174` |
| `SubExpressionAst` (`VisitSubExpression`) | captured block | no statements -> $null; else CaptureAstResults (temporary output pipe collecting results) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitSubExpression@L6176-L6193` |
| `UsingExpressionAst` (`VisitUsingExpression`) | runtime call | VariableOps.GetUsingValue(locals, key, RuntimeUsingIndex, context) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitUsingExpression@L6195-L6203` |
| `VariableExpressionAst` (`VisitVariableExpression`) | slot or runtime lookup | $null/$true/$false constants; automatic variables via tuple slot or VariableOps.GetAutomaticVariableValue; TupleIndex < 0 -> VariableOps.GetVariableValue (by name); else tuple field access | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitVariableExpression@L6205-L6250` |
| `TypeExpressionAst` (`VisitTypeExpression`) | constant or runtime call | reflection Type constant if resolvable at compile time, else TypeOps.ResolveTypeName at run time | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitTypeExpression@L6276-L6279` |
| `MemberExpressionAst` (`VisitMemberExpression`) | field/property or dynamic site | static [T]::Member with a unique public static field/property -> direct access; else PSGetMemberBinder / PSGetDynamicMemberBinder; `?.` wrapped in a null check | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitMemberExpression@L6281-L6346` |
| `InvokeMemberExpressionAst` (`VisitInvokeMemberExpression`) | dynamic site | InvokeMember: PSInvokeMemberBinder, PSCreateInstanceBinder for `[T]::new`, PSInvokeDynamicMemberBinder for non-constant names; argument/target type constraints passed to the binder | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitInvokeMemberExpression@L6447-L6469` |
| `ArrayExpressionAst` (`VisitArrayExpression`) | captured block | @( ) : empty -> object[0]; single pure expression -> that expression wrapped to array; else CaptureAstResults(Enumerable) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitArrayExpression@L6471-L6520` |
| `ArrayLiteralAst` (`VisitArrayLiteral`) | array init | Expression.NewArrayInit(object, elements cast to object) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitArrayLiteral@L6522-L6532` |
| `HashtableAst` (`VisitHashtable`) | block | new Hashtable(count, OrdinalIgnoreCase) then HashtableOps.AddKeyValuePair per pair; each value statement captured with CaptureStatementResults | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitHashtable@L6555-L6562` |
| `ScriptBlockExpressionAst` (`VisitScriptBlockExpression`) | runtime call | ScriptBlockExpressionWrapper.GetScriptBlock(context, false); the block body is compiled lazily on first run | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitScriptBlockExpression@L6564-L6577` |
| `ParenExpressionAst` (`VisitParenExpression`) | captured pipeline | assignment -> CompileAssignment; otherwise CaptureStatementResults of the pipeline | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitParenExpression@L6579-L6598` |
| `ExpandableStringExpressionAst` (`VisitExpandableStringExpression`) | format call | StringOps.FormatOperator(format string, string[] of nested expressions converted with PSToStringBinder) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitExpandableStringExpression@L6600-L6609` |
| `IndexExpressionAst` (`VisitIndexExpression`) | dynamic site | PSGetIndexBinder with 1 or n index arguments; `?[]` wrapped in a null check | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitIndexExpression@L6611-L6640` |
| `AttributedExpressionAst` (`VisitAttributedExpression`) | delegate | child.Accept(this); attributes only matter on assignment targets | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitAttributedExpression@L6650-L6653` |
| `BlockStatementAst` (`VisitBlockStatement`) | not compiled | returns null (workflow remnants) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitBlockStatement@L6655-L6658` |

Rows: **63** (`GENERATED`). "not visited" rows are asserted unreachable in the compiler (their parents handle them).

## 4. Helper methods of Compiler

| Method | Source |
|---|---|
| `Compile` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.Compile@L961-L964` |
| `CompileExpressionOperand` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileExpressionOperand@L966-L975` |
| `CompileInvocationArguments` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileInvocationArguments@L977-L991` |
| `ReduceAssignment` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ReduceAssignment@L993-L1023` |
| `Coalesce` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.Coalesce@L1025-L1051` |
| `GetLocal` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetLocal@L1053-L1062` |
| `CallGetVariable` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CallGetVariable@L1064-L1071` |
| `CallSetVariable` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CallSetVariable@L1073-L1080` |
| `GetAutomaticVariable` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetAutomaticVariable@L1082-L1116` |
| `CallStringEquals` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CallStringEquals@L1118-L1126` |
| `IsStrictMode` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.IsStrictMode@L1128-L1136` |
| `AddSequencePoint` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.AddSequencePoint@L1138-L1149` |
| `UpdatePosition` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.UpdatePosition@L1151-L1163` |
| `NewTemp` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.NewTemp@L1167-L1170` |
| `GetTypeConstraintForMethodResolution` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetTypeConstraintForMethodResolution@L1172-L1192` |
| `CombineTypeConstraintForMethodResolution` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CombineTypeConstraintForMethodResolution@L1194-L1202` |
| `CombineTypeConstraintForMethodResolution` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CombineTypeConstraintForMethodResolution@L1204-L1217` |
| `ConvertValue` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ConvertValue@L1219-L1242` |
| `ConvertValue` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ConvertValue@L1244-L1256` |
| `GetParameterMetaData` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetParameterMetaData@L1262-L1294` |
| `GetAttributeGenerator` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetAttributeGenerator@L1299-L1320` |
| `CheckNoPositionalArgs` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CheckNoPositionalArgs@L1345-L1359` |
| `CheckNoNamedArgs` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CheckNoNamedArgs@L1361-L1376` |
| `static` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.static@L1378-L1386` |
| `NewCmdletBindingAttribute` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.NewCmdletBindingAttribute@L1388-L1444` |
| `NewExperimentalAttribute` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.NewExperimentalAttribute@L1446-L1463` |
| `NewParameterAttribute` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.NewParameterAttribute@L1465-L1548` |
| `NewOutputTypeAttribute` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.NewOutputTypeAttribute@L1550-L1628` |
| `NewAliasAttribute` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.NewAliasAttribute@L1630-L1643` |
| `NewValidateSetAttribute` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.NewValidateSetAttribute@L1645-L1710` |
| `NewDebuggerHiddenAttribute` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.NewDebuggerHiddenAttribute@L1712-L1717` |
| `NewValidateNotNullOrEmptyAttribute` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.NewValidateNotNullOrEmptyAttribute@L1719-L1724` |
| `NewValidateNotNullAttribute` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.NewValidateNotNullAttribute@L1726-L1731` |
| `GetAttribute` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetAttribute@L1733-L1796` |
| `GetAttribute` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetAttribute@L1798-L1817` |
| `GetRuntimeDefinedParameter` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetRuntimeDefinedParameter@L1819-L1907` |
| `TryGetDefaultParameterValue` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.TryGetDefaultParameterValue@L1909-L1943` |
| `Compile` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.Compile@L1974-L2077` |
| `CompileTree` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileTree@L2079-L2097` |
| `GetExpressionValue` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetExpressionValue@L2099-L2102` |
| `GetExpressionValue` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetExpressionValue@L2104-L2110` |
| `GetExpressionValue` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetExpressionValue@L2112-L2202` |
| `CompileSingleExpression` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileSingleExpression@L2204-L2226` |
| `CaptureAstResults` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CaptureAstResults@L2264-L2355` |
| `CaptureStatementResultsHelper` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CaptureStatementResultsHelper@L2357-L2397` |
| `CaptureStatementResults` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CaptureStatementResults@L2399-L2426` |
| `CallAddPipe` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CallAddPipe@L2428-L2436` |
| `CompileNamedBlock` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileNamedBlock@L2504-L2527` |
| `CompileTrap` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileTrap@L2529-L2550` |
| `CompileSingleLambda` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileSingleLambda@L2552-L2626` |
| `GenerateTypesAndUsings` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateTypesAndUsings@L2628-L2675` |
| `GenerateLoadUsings` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateLoadUsings@L2682-L2708` |
| `DefinePowerShellTypes` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.DefinePowerShellTypes@L2717-L2750` |
| `LoadUsingsImpl` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.LoadUsingsImpl@L2752-L2796` |
| `PopulateRuntimeTypes` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.PopulateRuntimeTypes@L2798-L2820` |
| `LoadAssembly` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.LoadAssembly@L2822-L2854` |
| `LoadModule` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.LoadModule@L2861-L2901` |
| `GenerateFunctionProlog` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateFunctionProlog@L2903-L2959` |
| `InitializeMemberProperties` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.InitializeMemberProperties@L2961-L2985` |
| `GenerateFunctionEpilog` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateFunctionEpilog@L2987-L2993` |
| `CompileStatementListWithTraps` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileStatementListWithTraps@L3046-L3268` |
| `CompileTrappableExpression` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileTrappableExpression@L3270-L3279` |
| `ShouldSetExecutionStatusToSuccess` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ShouldSetExecutionStatusToSuccess@L3287-L3299` |
| `ShouldSetExecutionStatusToSuccess` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ShouldSetExecutionStatusToSuccess@L3307-L3319` |
| `GetSingleExpressionFromPipeline` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetSingleExpressionFromPipeline@L3326-L3335` |
| `ShouldSetExecutionStatusToSuccess` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ShouldSetExecutionStatusToSuccess@L3343-L3364` |
| `ShouldSetExecutionStatusToSuccess` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ShouldSetExecutionStatusToSuccess@L3372-L3419` |
| `CompileAssignment` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileAssignment@L3527-L3563` |
| `CompilePipelineChainElement` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompilePipelineChainElement@L3726-L3734` |
| `GetCommandRedirections` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetCommandRedirections@L3868-L3894` |
| `GetRedirectedExpression` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetRedirectedExpression@L3899-L4110` |
| `AddMergeRedirectionExpressions` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.AddMergeRedirectionExpressions@L4112-L4138` |
| `GetCommandArgumentExpression` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetCommandArgumentExpression@L4239-L4266` |
| `ThrowRuntimeError` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ThrowRuntimeError@L4307-L4310` |
| `ThrowRuntimeError` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ThrowRuntimeError@L4312-L4315` |
| `ThrowRuntimeError` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ThrowRuntimeError@L4317-L4335` |
| `ThrowRuntimeErrorWithInnerException` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ThrowRuntimeErrorWithInnerException@L4337-L4344` |
| `ThrowRuntimeErrorWithInnerException` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.ThrowRuntimeErrorWithInnerException@L4346-L4370` |
| `CreateThrow` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CreateThrow@L4372-L4392` |
| `CreateThrow` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CreateThrow@L4394-L4408` |
| `GetSwitchBodyGenerator` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetSwitchBodyGenerator@L4544-L4647` |
| `GenerateLoopBreakContinueCatchBlocks` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateLoopBreakContinueCatchBlocks@L4731-L4758` |
| `GenerateWhileLoop` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateWhileLoop@L4760-L4864` |
| `GenerateDoLoop` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateDoLoop@L4866-L4929` |
| `GenerateIteratorStatement` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateIteratorStatement@L4931-L5056` |
| `GetRangeEnumerator` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetRangeEnumerator@L5090-L5108` |
| `UpdatePositionForInitializerOrCondition` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.UpdatePositionForInitializerOrCondition@L5110-L5121` |
| `GenerateBreakOrContinue` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateBreakOrContinue@L5511-L5551` |
| `GenerateCallContains` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateCallContains@L5665-L5675` |
| `GetLikeRHSOperand` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetLikeRHSOperand@L5979-L5992` |
| `CompileIncrementOrDecrement` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileIncrementOrDecrement@L6053-L6100` |
| `CompileTypeName` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileTypeName@L6252-L6274` |
| `GetInvokeMemberConstraints` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetInvokeMemberConstraints@L6348-L6376` |
| `GetInvokeMemberConstraints` (overload) | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetInvokeMemberConstraints@L6378-L6403` |
| `InvokeMember` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.InvokeMember@L6405-L6423` |
| `InvokeBaseCtorMethod` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.InvokeBaseCtorMethod@L6425-L6430` |
| `InvokeDynamicMember` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.InvokeDynamicMember@L6432-L6445` |
| `BuildHashtable` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.BuildHashtable@L6534-L6553` |
| `GetNullConditionalWrappedExpression` | `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GetNullConditionalWrappedExpression@L6642-L6648` |

Verification: all 63 `Visit*` methods were read (notes W3-W21); the table is joined by name and the generator asserts that every `Visit*` method has an annotation and vice versa; `VisitPipeline`, `VisitTrap`, `VisitHashtable`, `VisitCatchClause`, `VisitDoWhileStatement` were re-read for this catalog.

