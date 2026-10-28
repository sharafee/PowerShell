# CompiledScriptBlock.cs (2553 lines) - T27 notes
## W1 L1-300
- L25-30 enum CompileInterpretChoice {NeverCompile, AlwaysCompile, CompileOnDemand}. L32-39 enum ScriptBlockClauseToInvoke {Begin,Process,End,Clean,ProcessBlockOnly}.
- L41 CompiledScriptBlockData: two ctors (ast,isFilter) / (scriptText,isProductCode) = delay-parse. Id=Guid.NewGuid() each data.
- L57-83 Compile(bool optimized): InitializeMetadata if _attributes==null; if optimized && NameToIndexMap==null -> CompileOptimized() first (needs the name->index map); then optimized = optimized && !VariableAnalysis.AnyVariablesCouldBeAllScope(NameToIndexMap); if !optimized && !_compiledUnoptimized -> CompileUnoptimized; else if optimized && !_compiledOptimized -> CompileOptimized. Returns effective 'optimized'. Quirk: optimized compile done even when result is then discarded (all-scope variable) -> compile both.
- L85-131 InitializeMetadata under lock(this): attributes, CmdletBinding, DebuggerHidden / DebuggerStepThrough/NonUserCode; runtimeDefinedParameterDictionary; fields assigned last.
- L133-161 CompileUnoptimized/CompileOptimized: lock(this), double-check flag, ReallyCompile(bool), set flag after.
- L163-195 ReallyCompile: ETW ParserEventSource CompileStart/Stop; PerformSecurityChecks(); new Compiler().Compile(this, optimize). LEGACYTELEMETRY conditional.
- L197-283 PerformSecurityChecks: only for ScriptBlockAst (top-level); skip for .psd1 containing safe hashtable; AmsiUtils.ScanContent -> DETECTED => ParseException ScriptContainedMaliciousContent; admin-block range => ScriptHasAdminBlockedContent; ScriptBlock.CheckSuspiciousContent -> HasSuspiciousContent.
- L285-311 delay parse: _scriptText, Ast property => DelayParseScriptText under lock; parser.Parse; errors => ParseException; _scriptText=null.
## W2 L301-600
- L313-345 properties: LocalsMutableTupleType, UnoptimizedLocalsMutableTupleType, creators, NameToIndexMap (only set for optimized), per-clause Action<FunctionContext> x5 optimized + x5 Unoptimized (DynamicParam, Begin, Process, End, Clean).
- L347 SequencePoints. L352-355 _compiledOptimized/_compiledUnoptimized/_hasSuspiciousContent/_isProductCode.
- L388-399 HasSuspiciousContent asserts compiled.
- L403-509 GetAttributes, UsesCmdletBinding, RuntimeDefinedParameters, CmdletBindingAttribute, ObsoleteAttribute, ExperimentalAttribute (lock), GetParameterMetadata(scriptBlock) (CommandMetadata lazily).
- L511-539 ToString.
- L542 partial class ScriptBlock: _scriptBlockData readonly; ctor(ast,isFilter); private ctor(data) captures LanguageMode from TLS context (L565-569).
- L580-581 s_cachedScripts ConcurrentDictionary<Tuple<string,string>,ScriptBlock>.
- L583-601 TryGetCachedScriptBlock: InternalTestHooks.IgnoreScriptBlockCache bypass; key=(fileName,fileContents); returns scriptBlock.Clone() (shares data!). Clone() = new ScriptBlock(_scriptBlockData) L673 => compiled delegates shared across clones.
## W3 L601-900
- L609-637 CacheScriptBlock: skip if IgnoreScriptBlockCache; skip when AST contains 'using module/assembly' (IsUsingTypes) or dynamic keyword; if s_cachedScripts.Count > 1024 => Clear() (whole dictionary) then TryAdd.  [CAP 1024]
- L642 ClearScriptBlockCache. L647 EmptyScriptBlock delay-parsed product code.
- L650-671 Create(parser,fileName,contents): cache check -> Parse -> ParseException -> new ScriptBlock -> CacheScriptBlock -> return Clone() (cached copy must not be session-bound).
- L715-782 GetPowerShellImpl, GetSteppablePipelineImpl, GetSimplePipeline (T210 scope; only note).
- L880-919 CheckRestrictedLanguage (public).
## W4 L901-1200 InvokeWithPipeImpl
- L935-959 overload => clause ProcessBlockOnly. L961 main: Clean => PSNotSupportedException; missing clause => return silently; context = GetContextFromTLS; PipelineStopping check.
- **L1006 runOptimized = context._debuggingMode <= 0 && createLocalScope;** L1007 GetCodeToInvoke(ref runOptimized, clause) (may flip false if all-scope var). codeToInvoke==null => return. L1016 locals = MakeLocalsTuple(runOptimized).
- L1018-1033 automatic vars Underbar/Input/This; SetPSScriptRootAndPSCommandPath.
- L1040-1069 language mode switching: if this.LanguageMode set and != context: transition allowed if target != FullLanguage || createLocalScope || module FullLanguage; else (CL -> FL dot-sourcing, untrusted) Audit-mode WDAC log + allow, else NOT switched (stay).
- L1071-1176 scope setup: createLocalScope => NewScope(false), LocalsTuple=locals, inject functions/variables; else dotted: if CurrentScope.LocalsTuple==null set it, else DottedScopes.Push(locals) + backupWhenDotting dict.
- L1184-1191 BindArgumentsForScriptblockInvoke; FunctionContext construction L1195-1205 (fields _executionContext,_outputPipe,_localsTuple,_scriptBlock,_file,_debuggerHidden,_debuggerStepThrough,_sequencePoints). L1207 LogScriptBlockStart; L1211 codeToInvoke(functionContext) in try/finally LogScriptBlockEnd.
- finally L1223-1262 restore language mode, pipes, ScopeOrigin, RemoveScope / DottedScopes.Pop + restore backup variables, restore session state.
## W5 L1201-1500
- L1265-1286 MakeLocalsTuple(bool createLocalScope[param name actually = optimized]): optimized => (LocalsMutableTupleType, NameToIndexMap, LocalsMutableTupleCreator); else (UnoptimizedLocalsMutableTupleType, UsesCmdletBinding ? Compiler.DottedScriptCmdletLocalsNameIndexMap : Compiler.DottedLocalsNameIndexMap, UnoptimizedLocalsMutableTupleCreator).
- L1288-1366 BindArgumentsForScriptblockInvoke.
- L1371-1411 GetCodeToInvoke: ProcessBlockOnly invalid when Begin||Clean||(End&&Process) => InvalidOperationException; optimized = data.Compile(optimized); selects optimized or Unoptimized delegate per clause; default (ProcessBlockOnly): Process if HasProcessBlock else End.
- L1419 ScriptBlock.Compile(bool) pass-through.
- L1421-1478 LogScriptBlockCreation: HasLogged short-circuit unless InternalTestHooks.ForceScriptBlockLogging; policy; IsProductCode => SkipLogging; text split when Length >= 20000: segmentSize = 10000 + Random.Shared.Next(10000).
## W6 L1501-1800 logging, encryption recipients, FormatLogString (UNIX: replace NUL, LF, CR), CheckSuspiciousContent L1775.
## W7 L1801-2100 SuspiciousContentChecker: LCG=31 rolling hash, 29-char max pattern, LookupHash switch with ~100 hashed patterns (no plaintext). Match(). Security surface (SEC): drives HasSuspiciousContent -> forced logging.
## W8 L2101-2400
- L2101-2137 LogScriptBlockStart/End. L2139-2176 property forwards, HasBegin/Process/End/CleanBlock.
- L2179 PSScriptCmdlet: fields; ctor L2196-2217: `_runOptimized = _scriptBlock.Compile(optimized: context._debuggingMode <= 0 && useNewScope)`; _localsTuple = MakeLocalsTuple(_runOptimized); FunctionContext.
- L2219-2311 Begin/Process/End/Clean/DynamicParam clause selection via _runOptimized ? X : UnoptimizedX. Clean only if _anyClauseExecuted.
- L2323-2407 RunClause: language mode switch (no FL-restriction here), clause(_functionContext), ExitException handling for script files => $LASTEXITCODE.
## W9 L2401-2553: GetDynamicParameters, SetLocalsTupleForNewScope, PushDottedScope/PopDottedScope, PrepareForBinding, SetPreferenceVariables, StopProcessing, Dispose.
## KEY
- NO execution counter / loop counter in this file. Tier decision lives in Compiler.cs L2050-2097 (stmt count 300, threshold -1 / int.MaxValue) and LightCompiler/LightDelegateCreator.
- AlwaysCompile enum member: referenced only in Compiler.CompileTree L2086 (no caller passes it) -> verify by rg.
