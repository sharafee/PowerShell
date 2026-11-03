---
id: LANG-IR-001
title: Intermediate representation
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/parser/Compiler.cs, src/System.Management.Automation/engine/interpreter/LightCompiler.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/parser/_folder.md]
generated_from: []
---

# Intermediate representation

> STATIC-ONLY — behavior not run-verified. `FACT-SRC` unless marked. The IR is the shape of the expression trees `Compiler` produces; it is the contract between [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md), the interpreter ([INSTRUCTION-SET.md](INSTRUCTION-SET.md)) and the JIT ([TIERING-POLICY.md](TIERING-POLICY.md)).

## 1. Purpose and scope [SPEC]

PowerShell has no bytecode of its own. Its IR is a `System.Linq.Expressions` tree: one `Expression<Action<FunctionContext>>` per named block, containing ordinary LINQ nodes, DLR `DynamicExpression` call sites for PowerShell operations, and three PowerShell-specific extension nodes. This document specifies the lambda contract, the runtime objects the tree reads and writes, the protocols the tree implements (output, `$?`, error handling, positions), and which LINQ node kinds it uses. Anything labelled "protocol" is behavior a new implementation must reproduce even if it does not use expression trees ([EQUIVALENCE-SPEC.md](EQUIVALENCE-SPEC.md)).

## 2. Source map

| path | type | role |
|---|---|---|
| src/System.Management.Automation/engine/parser/Compiler.cs::FunctionContext@L784-L814 | class | the one parameter of every lambda |
| src/System.Management.Automation/engine/parser/Compiler.cs::Compiler@L816-L6661 | class | builds the trees |
| src/System.Management.Automation/engine/parser/Compiler.cs::PowerShellLoopExpression@L6947-L6989 | class | extension node: a loop that the interpreter can promote to JIT |
| src/System.Management.Automation/engine/parser/Compiler.cs::EnterLoopExpression@L6991-L7023 | class | extension node: loop iteration counter |
| src/System.Management.Automation/engine/parser/Compiler.cs::UpdatePositionExpr@L7025-L7081 | class | extension node: sequence point and breakpoint check |
| src/System.Management.Automation/engine/parser/Compiler.cs::ExpressionCache@L659-L718 | class | shared constant nodes |

## 3. Responsibilities and non-responsibilities

Describes the tree shape, not the AST → tree rules (see [COMPILATION-MAP.md](COMPILATION-MAP.md)) and not binder behavior (T26, planned BINDER-CATALOG).

## 4. Key types and contracts [IMPL]

### 4.1 The lambda

Signature `Action<FunctionContext>`; name = function name plus a clause suffix (`<Begin>`, `<Process>`, `<End>`, `<Clean>`, `<DynamicParam>`, `<trap>`), `<ScriptBlock>` for anonymous blocks. Single-expression lambdas have the signature `Func<FunctionContext, object>`. Built by `CompileSingleLambda` (src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileSingleLambda@L2552-L2626):

1. `context` = `funcContext._executionContext`, `locals` = `(TupleType)funcContext._localsTuple` (declared as the first block variables; the interpreter reads them at fixed frame slots 0 and 1, see src/System.Management.Automation/engine/interpreter/InterpretedFrame.cs::InterpretedFrame@L28-L332).
2. Prolog (`GenerateFunctionProlog`): store the function name into the context, run an entry position update, `context._debugger.EnterScriptFunction(funcContext)`; for class members also redirect the output pipe to a null pipe and bind `$this`; constructors initialize property defaults.
3. Optional (root block only): load `using` directives and define classes (`GenerateTypesAndUsings`).
4. Body: the statement list (`CompileStatementListWithTraps`).
5. A `returnTarget` label, then the epilog (exit position update).
6. Whole body wrapped in `try … finally { context._debugger.ExitScriptFunction() }`; if the block has traps (or contains a `trap` statement), `try … catch (ReturnException) {}` is added around it.

### 4.2 `FunctionContext` (what the IR can read and write)

Fields: `_scriptBlock`, `_file`, `_debuggerHidden`, `_debuggerStepThrough`, `_sequencePoints` (extents), `_executionContext`, `_outputPipe`, `_breakPoints`, `_boundBreakpoints`, `_currentSequencePointIndex`, `_localsTuple`, `_traps` (stack of trap handler tuples), `_functionName`; methods `PushTrapHandlers`, `PopTrapHandlers` (src/System.Management.Automation/engine/parser/Compiler.cs::FunctionContext@L784-L814).

### 4.3 Locals

A `MutableTuple` whose type comes from variable analysis ([02.4-semantic-analysis.md](02.4-semantic-analysis.md) §7.2). Slot access is a chain of property reads over the tuple access path. Variables with `TupleIndex < 0` are accessed by name through `VariableOps.GetVariableValue/SetVariableValue(path, context, ast)`.

## 5. Data model — the protocols

- **Output protocol.** A statement that produces a value writes it to `funcContext._outputPipe` (`CallAddPipe`: non-enumerable static types are added directly, others through `PSPipeWriterBinder`). The expression-tree value of a pure expression is *not* the output. Assignments produce no output. `++`/`--` produce no output. To collect the output of a sub-statement (conditions, assignments, `@()`, `$()`), the tree swaps `_outputPipe` for a new `Pipe` over a `List<object>`, compiles the statement, and restores the old pipe in a `finally` (src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CaptureAstResults@L2264-L2355).
- **`$?` protocol.** After a statement that "succeeds trivially" (`ShouldSetExecutionStatusToSuccess`: pure expressions and assignments of pure expressions, `$()` with no statements, …) the tree sets `context.QuestionMarkVariableValue = true`; commands set it at run time.
- **Error-action protocol.** Every statement is wrapped so that a non-flow-control exception is passed to `ExceptionHandlingOps.CheckActionPreference(funcContext, e)`; if it returns, execution resumes at the next statement; flow-control exceptions (`FlowControlException`) are rethrown untouched. Detail: [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §6.4.
- **Position protocol.** Before each statement/condition the tree stores the sequence-point index into `funcContext._currentSequencePointIndex` and, if the debugger is active (`_debuggingMode > 0`), calls `OnSequencePointHit`. `UpdatePositionExpr` reduces to `DebugInfo` + that store for the JIT, and to `UpdatePositionInstruction` for the interpreter.
- **Flow-control protocol.** `break`/`continue` to a loop in the same lambda are `Goto` labels; otherwise `BreakException(label)`/`ContinueException(label)` are thrown and caught by the enclosing loop's catch blocks; `return` is a `Return` to the lambda's label (or `ReturnException` inside trap lambdas); `exit` throws the exception from `PipelineOps.GetExitException`; `throw` converts via `ExceptionHandlingOps.ConvertToException`.
- **Dynamic operations.** Arithmetic other than double-double, comparisons, conversions, member/index/invoke operations, enumeration, and pipeline writes are `DynamicExpression` sites using the PowerShell binders (`PSBinaryOperationBinder`, `PSConvertBinder`, `PSGetMemberBinder`, …); each emitted site has its own `CallSite` (per-site caches). Binder semantics: BINDER-CATALOG (planned T26).

## 6. Control flow

Not applicable at this level: the tree is straight code with labels and try blocks; loop and statement shapes are shown in [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §6.

## 7. Algorithms

### 7.1 LINQ node kinds used

Usage counts of `Expression.<Factory>(` calls in `Compiler.cs` (`GENERATED`, `APPROX`: calls, not emitted nodes) with the light compiler's support (hand-read from `LightCompiler.cs`; `FACT-SRC`):

<!--GEN:irnodes-->
| LINQ factory | Calls in Compiler.cs | Interpreter (LightCompiler) support |
|---|---:|---|
| `Expression.Constant` | 130 | yes |
| `Expression.Call` | 102 | yes (by-ref or value-type instance call forces full JIT) |
| `Expression.Block` | 89 | yes (defines locals) |
| `Expression.Assign` | 72 | yes (local, parameter, index, member; not compound) |
| `Expression.Dynamic` | 62 | yes (DynamicInstruction<...> per site) |
| `Expression.Label` | 29 | yes |
| `Expression.Variable` | 21 | yes |
| `Expression.NewArrayInit` | 15 | yes |
| `Expression.Catch` | 14 | yes (no filters) |
| `Expression.IfThen` | 14 | yes |
| `Expression.Field` | 13 | yes (literal/static/instance via reflection) |
| `Expression.New` | 12 | yes (by-ref ctor forces JIT) |
| `Expression.Property` | 12 | yes (getter call) |
| `Expression.TryFinally` | 12 | yes |
| `Expression.Goto` | 9 | yes |
| `Expression.Not` | 9 | yes (bool only) |
| `Expression.Convert` | 8 | numeric convert, otherwise no-op |
| `Expression.Parameter` | 8 | yes |
| `Expression.Throw` | 8 | yes |
| `Expression.Rethrow` | 7 | yes |
| `Expression.SwitchCase` | 6 | int constants only |
| `Expression.TryCatch` | 6 | yes |
| `Expression.Condition` | 5 | yes |
| `Expression.NotEqual` | 5 | numeric/reference |
| `Expression.Equal` | 4 | numeric/reference |
| `Expression.TryCatchFinally` | 4 | yes |
| `Expression.IfThenElse` | 3 | yes |
| `Expression.Switch` | 3 | int test values, no comparison method |
| `Expression.AndAlso` | 2 | bool only |
| `Expression.Empty` | 2 | yes |
| `Expression.TypeIs` | 2 | yes |
| `Expression.Add` | 1 | yes |
| `Expression.ArrayAccess` | 1 | yes (indexer) |
| `Expression.Break` | 1 | yes (goto) |
| `Expression.Continue` | 1 | yes (goto) |
| `Expression.DebugInfo` | 1 | recorded only |
| `Expression.Divide` | 1 | yes |
| `Expression.GreaterThan` | 1 | numeric |
| `Expression.Lambda` | 1 | nested lambdas via closure |
| `Expression.Multiply` | 1 | yes |
| `Expression.OrElse` | 1 | bool only |
| `Expression.Return` | 1 | yes (goto) |
| `Expression.Subtract` | 1 | yes |
| `Expression.SymbolDocument` | 1 | n/a (debug info document) |
<!--/GEN:irnodes-->

Extension nodes (`ExpressionType.Extension`, implement `IInstructionProvider` so the interpreter can compile them without reducing): `PowerShellLoopExpression` (a loop; `AddInstructions` emits its body and finishes the loop counter), `EnterLoopExpression` (emits `EnterLoopInstruction` only if the loop statement count is below the limit), `UpdatePositionExpr` (emits `UpdatePositionInstruction`).

### 7.2 What the interpreter cannot handle

`LightCompiler` throws for: binary `And`/`Or`/`Modulo`/`Power`/shifts/`ExclusiveOr` without a method, unary operators other than `Not` on `bool`/`Convert`/`TypeAs`, `Loop` (body commented out), `Switch` with non-int or non-constant tests, `Try` with filters or fault blocks, `ListInit`, `MemberInit`, `Quote`, compound assignments, `Coalesce` with a conversion, and `Invocation` of a lambda operand; it **forces a full JIT compile** for by-ref calls/constructors and instance calls on non-primitive value types ([TIERING-POLICY.md](TIERING-POLICY.md) §7.2). The IR avoids the throwing shapes by construction (`INFERENCE`; PowerShell uses dynamic sites for operators other than double arithmetic and its own loop node instead of `Loop`).

## 8. Observable behavior [SPEC]

The IR is not observable by scripts. Observable consequences are the protocols in §5. No golden sample: STATIC-ONLY.

## 9. Error handling and edge cases

Single-expression lambdas swallow `FlowControlException` and rethrow `TerminateException` (`GetExpressionValue`). A statement list with ≥ 2 statements uses an integer dispatch with `goto`; after a handled error execution resumes at the *following* statement. The JIT is known to be expensive for many `try/catch` regions (comment in `CompileStatementListWithTraps`).

## 10. Concurrency and threading

A tree is built once per (script block, variant); the produced delegate is shared by all invocations and all clones. Per-call state lives in `FunctionContext` and the locals tuple (new per call).

## 11. Extension points and customization hooks

New node type → add a `VisitX` to `Compiler` and an `IInstructionProvider` if a custom node is needed. New operator → either a dynamic site with an existing binder or a `ParserOps`/`StringOps` helper call.

## 12. Dependencies

`System.Linq.Expressions`, `System.Dynamic` (call sites), the PowerShell binders and runtime helper classes listed in `CachedReflectionInfo` (src/System.Management.Automation/engine/parser/Compiler.cs::CachedReflectionInfo@L28-L657, about 250 cached `MethodInfo`/`FieldInfo` entries grouped by helper class).

## 13. Performance notes

Constant caches (`ExpressionCache.Constant(int)` caches -1..100), reflection info cache, native `double` arithmetic only when both static types are `double`, per-site binder caches.

## 14. Security considerations (mandatory)

The IR embeds the AST nodes and extents as constants (error positions, `$using` keys). The `data` statement sets `context.LanguageMode` to restricted around its body and restores it in a `finally`. Constrained-language enforcement is not in the IR but in the binders and runtime helpers (T26, SEC documents).

## 15. Enterprise considerations

Debuggability: `DebugInfo` + sequence points + `EnterScriptFunction/ExitScriptFunction` give step/breakpoint support in both tiers. Missing: no IR dump facility in release builds (`DebugViewWriter.cs` exists for debug view of trees, `UNVERIFIED` use).

## 16. Tests

Not read (VB-014).

## 17. Design decisions and trade-offs

| Decision | Label | Consequence |
|---|---|---|
| IR = LINQ expression trees | `FACT-SRC` | reuse of the DLR call sites and the .NET JIT; no custom backend |
| output via side effect on a pipe object, not via tree values | `FACT-SRC` | statements compose like commands; needs explicit capture for conditions and assignments |
| per-statement exception wrapper with resume | `FACT-SRC` | non-terminating-error semantics inside script code; cost in tree size and JIT time |
| custom extension nodes for loops and positions | `FACT-SRC` | the interpreter can promote a running loop |

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-IR-01** [ADAPT] (area: NLD-RUN) A tree-walker over the AST can replace the IR, provided it implements the protocols in §5 (output pipe, `$?`, error-action resume, positions, flow control). Why: the observable behavior is defined by the protocols, not by expression trees. Evidence: src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileSingleLambda@L2552-L2626.
- **LSN-IR-02** [REPLICATE] (area: NLD-PIP) Statements write to an output pipe; assignments, `++`/`--` and conditions do not; capturing output swaps the current pipe and restores it in a `finally`. Evidence: src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CaptureAstResults@L2264-L2355, src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.VisitCommandExpression@L4268-L4279.
- **LSN-IR-03** [REPLICATE] (area: NLD-ERR) Wrap each statement so that non-flow-control exceptions go to the error-action policy and execution continues with the next statement when the policy says so. Evidence: src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.CompileStatementListWithTraps@L3046-L3268.
- **LSN-IR-04** [ADAPT] (area: NLD-RUN) Represent break/continue/return as control-flow signals inside the evaluator, and as exceptions only when crossing function or script-block boundaries. Why: PowerShell uses labels in-lambda and exceptions across lambdas; a tree-walker has no lambdas but still crosses script-block calls. Evidence: src/System.Management.Automation/engine/parser/Compiler.cs::Compiler.GenerateBreakOrContinue@L5511-L5551.
- **LSN-IR-05** [REPLICATE] (area: NLD-RUN) Keep a per-statement sequence-point index in the call frame so errors and the debugger can report positions. Evidence: src/System.Management.Automation/engine/parser/Compiler.cs::UpdatePositionExpr@L7025-L7081.

## 19. Open questions / UNVERIFIED

- Use of `DebugViewWriter.cs`; whether it is reachable in release builds.
- Whether any `Expression.Switch` shape used by the compiler (catch dispatch) is accepted by the light compiler's int-only switch (3 uses of `Expression.Switch`; read: catch handler and statement dispatch use int tests).

Verification: node-kind counts generated by `tools/gen_T25.py` from `Compiler.cs`; support column cross-read from `LightCompiler.cs` notes W3-W7; prolog/epilog/wrapper re-read from `CompileSingleLambda` (L2552-2626) and `GenerateFunctionProlog` (L2903-2959).
