# interpreter/LightCompiler.cs (2052 lines) - T27 notes
## W1 L1-300: ExceptionHandler(L30), TryCatchFinallyHandler(L109) with GotoHandler(L173: Array.Find handler by Matches(exception.GetType())), RethrowException(L186), DebugInfo(L190; GetMatchingDebugInfo binary search L211), InterpretedFrameInfo(L250), LightCompiler(L271).
- **L273 `internal const int DefaultCompilationThreshold = 32;`** L275 comment "zero: sync compilation" on `_compilationThreshold`. L291 `_forceCompile` flag.
## W2 L301-600
- L297-301 ctor LightCompiler(int compilationThreshold): `_compilationThreshold = compilationThreshold < 0 ? DefaultCompilationThreshold : compilationThreshold`.  => Compiler passes -1 (CompileOnDemand) => 32; int.MaxValue (NeverCompile).
- L303 nested ctor (parent) copies threshold.
- L324-344 CompileTop(LambdaExpression): define params as locals (EmitInitializeParameter), Compile(body), pop if body non-void but lambda returns void, returns new LightDelegateCreator(MakeInterpreter(name), node).
- L364-373 MakeInterpreter: if _forceCompile => null (no interpreter => LightDelegateCreator compiles); else new Interpreter(name, _locals, GetBranchMapping(), instrs, debugInfos, _compilationThreshold).
- L409-447 closure resolution EnsureAvailableForClosure/ResolveLocal; box local when captured; _parent chain.
- L449-525 CompileGetVariable/GetBoxedVariable/SetVariable: emits LoadLocal / LoadLocalBoxed / LoadLocalFromClosure / StoreLocal / AssignLocal... (+Boxed / ToClosure)
- L533-585 Block: defines locals (EmitInitializeLocal), CompileAsVoid for all but last.
## W3 L601-900: Index (EmitCall getter/Set, EmitGetArrayItem/SetArrayItem), member assign (property setter call / EmitStoreField), assign dispatch L727: Index/MemberAccess/Parameter/Extension else InvalidOperationException; binary L751: Method!=null -> call; ArrayIndex, Add/AddChecked/Sub/SubChecked/Mul/MulChecked/Divide -> CompileArithmetic; Equal/NotEqual; < <= > >= (numeric types only); other => NotImplementedException (And, Or, Modulo, Power, shifts, ExclusiveOr).  Convert: numeric convert instruction else no-op ("TODO conversions...").
- L851-855: EmitDiv for Divide only. Note: NO Modulo instruction.
## W4 L901-1200
- Not (bool only else NotImplemented), TypeAs; unary other => NotImplementedException (Negate w/o Method etc).
- AndAlso/OrElse on bool: branch instrs; Nullable bool => NotImplemented.
- Conditional L997. LoopExpression L1032: body fully commented out (no-op!) i.e. ExpressionType.Loop emits nothing - PowerShell does not use Expression.Loop: uses its own EnterLoopExpression/PowerShellLoopExpression extensions with IInstructionProvider (Compiler.cs L6947-7080).
- Switch L1059: only int test values w/o comparison method, constant test values; else NotImplementedException.
- Label/Goto. Label scope infra (LabelScopeKind) L1174+.
## W5 L1201-1500: label helpers; TryPushLabelBlock; throw/rethrow; Try expr L1398: EmitEnterTryFinally / EmitEnterTryCatch; fault emulation for single catch(Exception) no-variable body ending in rethrow (L1437-1466); catch handlers with Filter => NotImplementedException (L1474-1479); node.Fault != null => NotImplementedException (L1516-1519).
## W6 L1501-1800
- L1550 Dynamic: compile args then EmitDynamic(DelegateType, Binder).
- **L1563-1595 Call: `_forceCompile = true` if any parameter IsByRef or (instance method on non-primitive value type)** [fallback: whole lambda compiled instead of interpreted]. L1597-1625 New: forceCompile if ctor has byref param.
- Member: literal field/static readonly => load constant; static => EmitLoadField; property => call getter; else NotImplementedException.
- NewArrayInit/NewArrayBounds. Extension L1709: IInstructionProvider.AddInstructions(this) else CanReduce -> Compile(Reduce()) else NotImplemented.
- DebugInfo L1728 -> DebugInfo records only (no instruction). RuntimeVariables L1743 -> EmitNewRuntimeVariables. Lambda L1757: nested LightCompiler(this), closure vars captured as boxed, EmitCreateDelegate(creator).
- Coalesce: non-nullable w/o Conversion; else NotImplementedException. Invocation: lambda operand => NotImplemented; else Call to Invoke.
## W7 L1801-2052: ListInit/MemberInit/Quote/Reducible => NotImplementedException; Unbox nop; TypeEqual/TypeIs (sealed => TypeEquals)/TypeAs; Compile(expr,asVoid); CompileAsVoid; CompileNoLabelPush giant switch (L1945-2040): maps ExpressionType; `default: throw Assert.Unreachable`; compound assignments => CompileReducibleExpression => NotImplementedException.
## KEY OPEN: where NotImplementedException is caught? No try/catch in Compiler.CompileTree (to verify). Means IR must avoid these node types by construction.
