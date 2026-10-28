# Notes ast.cs (T23)

## W1 L1-300
- Header comment L5-6 claims private/internal methods live in "AstCompile.cs" -> file does not exist in engine/parser/ (stale comment; check Compiler.cs for partial-class pieces).
- L26-28 using aliases: KeyValuePair=Tuple<ExpressionAst,StatementAst> (hashtable pairs), IfClause=Tuple<PipelineBaseAst,StatementBlockAst>, SwitchClause=Tuple<ExpressionAst,StatementBlockAst>.
- L34-53 internal ISupportsAssignment.GetAssignableValue(); IAssignableValue.GetValue(Compiler, exprs, temps)/SetValue(Compiler, rhs) -> compile-time contract on AST nodes (T25).
- L56-85 internal IParameterMetadataProvider: HasAnyScriptBlockAttributes, GetParameterMetadata(automaticPositions, ref usesCmdletBinding), GetScriptBlockAttributes, GetExperimentalAttributes, UsesCmdletBinding, Parameters, Body, GetPowerShell(...), GetWithInputHandlingForInvokeCommand, GetWithInputHandlingForInvokeCommandWithUsingExpression.
- L91 Ast: public abstract; ctor protected Ast(IScriptExtent) throws if extent null (L100-108); Extent get-only; Parent {get; private set} (L118).
- L126 Visit(ICustomAstVisitor) -> Accept (internal abstract L307); L140 Visit(AstVisitor) -> InternalVisit (internal abstract L309, returns AstVisitAction).
- L156 FindAll(pred, searchNestedScriptBlocks) -> AstSearcher.FindAll; L172 Find -> AstSearcher.FindFirst.
- L185 ToString => Extent.Text. L194 abstract Copy().
- L203-232 SafeGetValue(): default skipHashtableSizeCheck false; uses Runspace.DefaultRunspace?.ExecutionContext; calls GetSafeValueVisitor.GetSafeValue(this, context, SafeValueContext.Default|SkipHashtableSizeCheck); ANY exception caught and rethrown as InvalidOperationException(AutomationExceptions.CantConvertWithDynamicExpression, Extent.Text).
- L240-264 CopyElements<T>(ReadOnlyCollection<T>) returns null when null/empty; CopyElement<T> null-safe.
- L267-300 SetParents<T>, SetParents<T1,T2>(tuples), SetParent(child): throws InvalidOperationException(ParserStrings.AstIsReused) if child.Parent != null (L293-296); then Diagnostics.Assert + child.Parent=this. ClearParent L302.
- L311 EmptyPSTypeNameArray. L313-347 IsInWorkflow (walks parents; stops at FunctionDefinitionAst boundary; inlinescript). L349 internal HasSuspiciousContent {get;set}.
- L353-417 ancestor helpers: GetAncestorConfigurationDefinitionAstAndDynamicKeywordStatementAst, GetAncestorHashtableAst, GetAncestorTypeDefinitionAst (stops at FunctionDefinitionAst unless parent FunctionMemberAst), GetAncestorAst<T>.
- L424-451 SequencePointAst : Ast internal; "never produced by parser, only from compiler"; Copy/Accept/InternalVisit all Diagnostics.Assert(false).
- L456-588 ErrorStatementAst : PipelineBaseAst: 3 internal ctors (nestedAsts; kind+nested; kind+flags+conditions+bodies). Props Kind(Token), Flags(Dictionary<string,Tuple<Token,Ast>>), Conditions, Bodies, NestedAst. Copy picks ctor based on which props non-null (L558-588).

## W2 L301-600 (see W1 for 301-451 notes) + W3 L601-900
- L597-645 ErrorStatementAst.InternalVisit canonical pattern: action=visitor.VisitX(this); if SkipChildren -> return visitor.CheckForPostAction(this, Continue); if Continue visit children in order (NestedAst, Flags.Values (Item2 non-null), Conditions, Bodies) breaking on action != Continue; return visitor.CheckForPostAction(this, action).
- L653-707 ErrorExpressionAst : ExpressionAst; ctor(extent, nestedAsts=null); NestedAst; Copy; Accept->VisitErrorExpression.
- L713-770 ScriptRequirements (NOT an Ast): RequiredApplicationId, RequiredPSVersion, RequiredPSEditions, RequiredModules, RequiredAssemblies, IsElevationRequired; internal static empty collections.
- L775 ScriptBlockAst : Ast, IParameterMetadataProvider. Internal state: HadErrors, IsConfiguration {get;private set}, PostParseChecksPerformed (L783-787). Ctor #1 (8 params, no clean) delegates to #2 with cleanBlock null (L804-823); ctor #2 L842: SetUsingStatements; Attributes (empty static list if null); ParamBlock/BeginBlock/ProcessBlock/EndBlock/CleanBlock/DynamicParamBlock each SetParent if non-null (L852-900).

## W4 L901-1200
- ScriptBlockAst has 11 public ctors by overloads (L804,842,917,944,970,995 explicit-named-blocks family; L1022,1041,1061,1082,1103,1125 implicit-block family). Named-block family: (extent,[using],[attrs],paramBlock,begin,process,end,[clean],dynamicParam). Implicit family: (extent,[using],[attrs],paramBlock,StatementBlockAst statements,isFilter,[isConfiguration]).
- Implicit master ctor L1125-1162: statements==null -> ArgumentNull; isFilter => ProcessBlock = new NamedBlockAst(statements.Extent, TokenKind.Process, statements, unnamed:true); else EndBlock = NamedBlockAst(..TokenKind.End, statements, true) and IsConfiguration=isConfiguration (only set on the non-filter path). Begin/DynamicParam/Clean are null in this path.
- SetUsingStatements L1164 (empty static list if null). Attributes never null (L1181); UsingStatements never null (L1188); ParamBlock/BeginBlock null if absent.

## W5 L1201-1500
- ScriptBlockAst props: Begin/Process/End/Clean/DynamicParam NamedBlockAst (get-only, null if absent); ScriptRequirements {get; internal set} only set for top-level (L1226). GetHelpContent L1231 -> HelpCommentsParser.
- GetScriptBlock() L1250-1272: if !PostParseChecksPerformed => new Parser; root=GetRootScriptBlockAst() (climbs via GetAncestorAst<ScriptBlockAst>(root.Parent)); root.PerformPostParseChecks(parser); parser.ErrorList.Count>0 => throw ParseException. Then if HadErrors => PSInvalidOperationException. Returns new ScriptBlock(this, isFilter:false). (the 'flags' = only isFilter:false here; no other flags param)
- Copy L1289-1314: copies all blocks, attrs, using stmts; preserves IsConfiguration and ScriptRequirements (shared reference). HadErrors/PostParseChecksPerformed NOT copied (new default false).
- ToStringForSerialization L1316 strips curlies when Parent != null; overload L1331 rewrites $using variables -> $__using_X by offsets (UsingExpressionAst.UsingPrefix) and injects params into ParamBlock (remoting/invoke-command text).
- PerformPostParseChecks L1416: ETS events; SymbolResolver.ResolveSymbols(parser,this) then SemanticChecks.CheckAst(parser,this); Assert PostParseChecksPerformed set during semantic checks (T24).
- InternalVisit L1441-1495: order: (AstVisitor2 only) UsingStatements, Attributes; then ParamBlock, DynamicParamBlock, BeginBlock, ProcessBlock, EndBlock, CleanBlock (short-circuit && chain).

## W6 L1501-1800
- ScriptBlockAst explicit IParameterMetadataProvider impl L1499-1692: HasAnyScriptBlockAttributes = Attributes.Count>0 || ParamBlock?.Attributes.Count>0 (L1501); GetParameterMetadata -> Compiler.GetParameterMetaData(ParamBlock.Parameters,...) else empty RuntimeDefinedParameterDictionary (L1506); GetScriptBlockAttributes -> Compiler.GetAttribute(attributeAst) for Attributes then ParamBlock.Attributes (L1516); GetExperimentalAttributes with name-match helper (type accelerator or suffix of ExperimentalAttribute FullName; swallow exceptions) L1534-1590; Parameters => ParamBlock?.Parameters else null; Body => this; UsesCmdletBinding => ParamBlock attribute type == CmdletBindingAttribute (GetReflectionAttributeType) or ParamBlockAst.UsesCmdletBinding(params) (L1676-1690).
- GetPowerShell L1601 -> ExecutionContext.CheckStackDepth(); ScriptBlockToPowerShellConverter.Convert(this, null, isTrustedInput, ...). GetWithInputHandlingForInvokeCommandImpl L1628-1672: adds "$input |" prefix only for simple single pipeline not starting with CommandExpressionAst and not using $input (AstSearcher.IsUsingDollarInput).
- GetSimplePipeline L1694-1738: rejects Begin/Process/Clean/DynamicParam present (CanConvertOneClauseOnly), empty End (CantConvertEmptyPipeline), traps (CantConvertScriptBlockWithTrap), non-PipelineAst statements or >1 statements unless allowMultiplePipelines (CanOnlyConvertOnePipeline). Used for ScriptBlockToPowerShell.
- L1745 ParamBlockAst ctor (extent, attrs, params) lists never null.

## W7 L1801-2100
- ParamBlockAst L1745-1858: children Attributes then Parameters (L1813-1839); static UsesCmdletBinding(params) -> any parameter has [Parameter] attribute (L1843-1857) => ParameterAttribute implies cmdlet binding.
- NamedBlockAst L1864-2026: ctor(extent, TokenKind blockName, StatementBlockAst statementBlock, bool unnamed). HasInvalidBlockName L1995: !blockName.HasTrait(TokenFlags.ScriptBlockBlockName) or (unnamed && not Process/End) -> ArgumentException. Takes statementBlock.Statements/Traps, ClearParent() each then SetParents(...) (re-parenting; StatementBlockAst wrapper discarded) L1910-1931. For !unnamed, if Extent is InternalScriptExtent: OpenCurlyExtent/CloseCurlyExtent (internal, "Used by the debugger for command breakpoints") L1933-1940, L2004-2006. Props Unnamed, BlockKind, Statements (never null), Traps (null if none). Copy rebuilds a StatementBlockAst with extent from curlies (L1975-1993). InternalVisit: VisitNamedBlock then StatementBlockAst.InternalVisit(visitor, Traps, Statements, action) static helper (L2015-2023).
- NamedAttributeArgumentAst L2032: ctor throws on null/empty argumentName or null argument; ExpressionOmitted distinguishes [Parameter(Mandatory)] vs =$true.

## W8 L2101-2400
- NamedAttributeArgumentAst visits Argument only. AttributeBaseAst L2119 abstract: ctor(extent, ITypeName) throws on null typeName; TypeName (ITypeName); internal abstract Attribute GetAttribute() -> Compiler.GetAttribute(this) in both subclasses (L2253, L2313).
- AttributeAst L2151: ctor(extent,typeName,positional,named); children PositionalArguments then NamedArguments. Copy shares TypeName (ITypeName immutable-ish).
- TypeConstraintAst L2262: ctors (extent, ITypeName) and (extent, Type) -> new ReflectionTypeName(type). Leaf: InternalVisit -> VisitTypeConstraint; no children (SkipChildren mapped to Continue) L2305-2309.
- ParameterAst L2323: ctor(extent, VariableExpressionAst name, attrs, defaultValue); Attributes are AttributeBaseAst (AttributeAst or TypeConstraintAst); StaticType L2387: first TypeConstraintAst's TypeName.GetReflectionType() ?? typeof(object).

## W9 L2401-2700
- ParameterAst: GetTooltip (L2413), GetParamTextWithDollarUsingHandling (L2432; $using -> synthetic name for PSv2 remote); InternalVisit order: Attributes, Name, DefaultValue (L2483-2509).
- StatementBlockAst L2522-2624: ctor(extent, statements, traps); Statements never null; Traps null if none/empty (L2550). Static InternalVisit(visitor, traps, statements, action) L2592-2621: traps visited BEFORE statements; shared by NamedBlockAst.
- StatementAst L2629 abstract, trivial. TypeAttributes [Flags] enum {None=0,Class=1,Interface=2,Enum=4} L2648.
- TypeDefinitionAst L2667: ctor(extent,name,attrs,members,typeAttributes,baseTypes); name IsNullOrWhiteSpace -> ArgumentNull.

## W10 L2701-3000
- TypeDefinitionAst props Name, Attributes, BaseTypes (TypeConstraintAst), Members, TypeAttributes, IsEnum/IsClass/IsInterface (flag tests) L2732-2767. internal Type Type {get;set} with 3 stages null -> TypeBuilder -> RuntimeType (Assert L2785) = cached compile-time info (PSType.cs/T25-T210 class definition). Backing field _type L2798.
- TypeDefinitionAst.Accept: `visitor as ICustomAstVisitor2` then visitor2?.VisitTypeDefinition -> RETURNS NULL for a plain ICustomAstVisitor (L2802-2806). InternalVisit: AstVisitor2 gets VisitTypeDefinition; old visitors still traverse children (REVIEW comment L2818-2821); order Attributes, BaseTypes, Members.
- UsingStatementKind enum {Assembly=0, Command=1, Module=2, Namespace=3, Type=4} L2870. UsingStatementAst L2901: ctor1 (extent, kind, name) rejects Command/Type kind; ctor2 (extent, HashtableAst moduleSpec) kind=Module; ctor3 (extent, kind, aliasName, resolvedAlias) rejects Assembly; ctor4 (extent, aliasName, HashtableAst moduleSpec).

## W11 L3001-3300
- UsingStatementAst props: UsingStatementKind, Name (alias name or the item), Alias (mutually exclusive with ModuleSpecification), ModuleSpecification (HashtableAst, using module only), internal PSModuleInfo ModuleInfo {get; private set} (cached; set by DefineImportedModule L3090 which calls moduleInfo.GetExportedTypeDefinitions()). IsUsingModuleOrAssembly L3101.
- OBSERVATION: UsingStatementAst.Copy (L3037-3045) picks ctor by `Alias != null` only; for the ModuleSpecification-hashtable forms (ctor2 L2936 Name==null; ctor4 L2992) the else-branch ctor1 is called with Name (null for ctor2 -> ArgumentNull; ctor4 drops ModuleSpecification). Candidate defect (INFERENCE from reading; not run).
- UsingStatementAst.Accept requires ICustomAstVisitor2 else returns null (L3049-3053). InternalVisit: if AstVisitor2, calls VisitUsingStatement and returns on ANY non-Continue (SkipChildren is passed to CheckForPostAction unchanged, unlike other nodes that map it to Continue) L3055-3081; children Name, ModuleSpecification, Alias.
- MemberAst L3110 abstract: abstract string Name; internal abstract GetTooltip().
- PropertyAttributes [Flags] {None=0,Public=1,Private=2,Static=0x10,Literal=0x20,Hidden=0x40} L3132. PropertyMemberAst L3156: ctor throws if name blank or Public|Private both set (L3173-3182). Props Name, PropertyType (TypeConstraintAst, nullable), Attributes, PropertyAttributes, InitialValue; IsPublic/IsPrivate/IsHidden/IsStatic. Accept requires ICustomAstVisitor2. InternalVisit starts L3282: AstVisitor2 only gets VisitPropertyMember, then PropertyType, Attributes, ... (continues)

## W12 L3301-3600
- PropertyMemberAst.InternalVisit: ALL child traversal (PropertyType, Attributes, InitialValue) happens only when visitor is AstVisitor2 (L3282-3312); a v1 AstVisitor gets nothing but CheckForPostAction.
- MethodAttributes [Flags] {None,Public=1,Private=2,Static=0x10,Hidden=0x40} L3321. FunctionMemberAst L3342 : MemberAst, IParameterMetadataProvider wraps a private readonly FunctionDefinitionAst _functionDefinitionAst (L3350) which is SetParent'ed to the member; Name/Parameters/Body delegate to it. ctor rejects null FunctionDefinitionAst and Public|Private. IsConstructor = Name equals ((TypeDefinitionAst)Parent).Name ignoring case (needs Parent set; L3451-3454). _toolTip cached (L3458) GetTooltip lists overloads (L3472-3524).
- FunctionMemberAst.Accept requires ICustomAstVisitor2. InternalVisit: ONLY AstVisitor2 visits children: Attributes, ReturnType, _functionDefinitionAst (L3534-3563). IParameterMetadataProvider forwards to _functionDefinitionAst (L3567+).

## W13 L3601-3900
- FunctionMemberAst: GetPowerShell/GetWithInputHandling* throw NotSupportedException / NotImplementedException (L3599-3615: "I think this isn't reachable"). IsReturnTypeVoid L3620 (null return type => void; TypeName.IsType(typeof(void))). GetReturnType L3628.
- internal enum SpecialMemberFunctionType {None, DefaultConstructor, StaticConstructor} L3635. CompilerGeneratedMemberFunctionAst L3642 (internal; created by compiler/PSType, not parser): ctor(extent, definingType, type) builds Body = new ScriptBlockAst(extent, null, StatementBlockAst(...), false); for DefaultConstructor body statement is CommandExpressionAst(BaseCtorInvokeMemberExpressionAst(extent, extent, empty args)); definingType.SetParent(this) call actually sets this.Parent=definingType (SetParent(child) on definingType). Accept/InternalVisit Assert(false) unreachable; GetParameterMetadata -> empty; Parameters => null; UsesCmdletBinding false.
- FunctionDefinitionAst L3745 : StatementAst, IParameterMetadataProvider: public ctor(extent,isFilter,isWorkflow,name,params,body): name null/empty -> ArgumentNull; body null -> ArgumentNull; isFilter&&isWorkflow -> ArgumentException (L3782). Parameters null if none (L3791). internal ctor with Token functionNameToken: name = Generic token? StringToken.Value : Text; NameExtent = token.Extent (L3801-3815). Props IsFilter, IsWorkflow, Name, Parameters (nullable), Body, NameExtent. GetHelpContent x2 (HelpCommentsParser). Copy keeps NameExtent (L3891-3897).

## W14 L3901-4200
- FunctionDefinitionAst: GetParamTextFromParameterList (L3899) builds "param(...)" text; InternalVisit: Parameters (nullable), then Body (L3947-3969). IParameterMetadataProvider: params from function-name-list first, else Body.ParamBlock; GetPowerShell -> ScriptBlockToPowerShellConverter.Convert(Body, Parameters, ...); UsesCmdletBinding: Parameters!=null -> ParamBlockAst.UsesCmdletBinding(Parameters) else Body.
- IfStatementAst L4059: Clauses ReadOnlyCollection<IfClause = Tuple<PipelineBaseAst,StatementBlockAst>> (non-empty else ArgumentException L4077), ElseClause nullable. SetParents<T1,T2>(tuples). Visit order: for each clause cond then block; then ElseClause.
- DataStatementAst L4162: ctor(extent, variableName, commandsAllowed, body): body required; blank variableName -> null; CommandsAllowed (ExpressionAst); HasNonConstantAllowedCommand = any not StringConstantExpressionAst (L4197) (cached flag).

## W15 L4201-4500
- DataStatementAst.InternalVisit: Body only (CommandsAllowed NOT visited, L4242-4250). Code-generation field: internal int TupleIndex {get;set} = VariableAnalysis.Unanalyzed (L4256) -> compile-time cached slot index (T24/T25).
- LabeledStatementAst L4266 abstract: ctor(extent,label,condition PipelineBaseAst): whitespace label -> null; Condition SetParent'ed. LoopStatementAst L4309 abstract: adds Body StatementBlockAst required. ForEachFlags [Flags] {None=0, Parallel=1} L4344 (comment L4356-4357: any flag impacting evaluation needs binder like SwitchClauseEvalBinder).
- ForEachStatementAst L4363: ctor1 (extent,label,flags,variable,expression,body); ctor2 adds ExpressionAst throttleLimit. Condition == the enumerated pipeline expression. Copy L4446. InternalVisit L4469: Variable, Condition, Body — ThrottleLimit (set+parented) is NOT visited (observation). 

## W16 L4501-4800
- ForStatementAst L4489: Initializer/Condition/Iterator all optional PipelineBaseAst; visit order Initializer, Condition, Iterator, Body.
- DoWhileStatementAst L4576, DoUntilStatementAst L4632, WhileStatementAst L4688: all LoopStatementAst; condition mandatory (ArgumentNull); visit Condition then Body. (do-while/do-until body-before-condition ordering is a compile/execute matter; AST visits Condition first.)
- SwitchFlags [Flags] {None=0,File=1,Regex=2,Wildcard=4,Exact=8,CaseSensitive=0x10,Parallel=0x20} L4746; comment L4783-4785: flag influencing evaluation requires SwitchClauseEvalBinder caching update.
- SwitchStatementAst L4791 : LabeledStatementAst.

## W17 L4801-5100
- SwitchStatementAst L4791: ctor(extent,label,condition,flags,clauses (SwitchClause=Tuple<ExpressionAst,StatementBlockAst>),default): throws if no clauses AND no default (L4821). Clauses may be empty; Default nullable. Visit: Condition, each clause (Item1,Item2), Default. Copy L4859.
- CatchClauseAst L4922: CatchTypes (TypeConstraintAst; empty => IsCatchAll), Body required. InternalVisit L4992: CatchTypes then Body.
- TryStatementAst L5015: Body required; CatchClauses (empty if none) and Finally nullable; throws if neither catch nor finally (L5047). NOTE no AST node for "trap" ordering; TrapStatementAst separate.

## W18 L5101-5400
- TryStatementAst.InternalVisit: Body, CatchClauses, Finally. TrapStatementAst L5135: TrapType (TypeConstraintAst nullable), Body; visit TrapType, Body. Traps live in StatementBlockAst.Traps/NamedBlockAst.Traps not in Statements.
- BreakStatementAst L5215 / ContinueStatementAst L5272: Label is an ExpressionAst (nullable) -- label is an expression, not a string. Visit Label. ReturnStatementAst L5329: Pipeline (PipelineBaseAst nullable). ExitStatementAst L5386 same shape.

## W19 L5401-5700
- ThrowStatementAst L5443: Pipeline nullable; IsRethrow (L5480-5500): false if Pipeline != null; else true iff any ancestor is CatchClauseAst (walks all parents incl. across function/script block boundaries; "finally" is not a rethrow).
- ChainableAst L5534 abstract : PipelineBaseAst. PipelineChainAst L5549 : ChainableAst (Q13): ctor(extent, ChainableAst lhsChain, PipelineAst rhsPipeline, TokenKind chainOperator, bool background=false); non-null checks; chainOperator must be TokenKind.AndAnd or OrOr else ArgumentException (L5571-5574). Props LhsPipelineChain (ChainableAst), RhsPipeline (PipelineAst, never a chain), Operator, Background. Left-nested: lhs may be another PipelineChainAst; rhs is always a PipelineAst. Accept: (visitor as ICustomAstVisitor2)?.VisitPipelineChain (null for v1); InternalVisit: VisitPipelineChain only if AstVisitor2, children (Lhs, Rhs) visited for all visitor types (L5621-5646).
- PipelineBaseAst L5657 abstract : StatementAst; virtual GetPureExpression() returns null (L5674).
- PipelineAst L5684 : ChainableAst; ctor(extent, IEnumerable<CommandBaseAst>, bool background).

## W20 L5701-6000
- PipelineAst: 4 ctors (elements+bg, elements, single command+bg, single command). Empty/null elements -> ArgumentException. Background {get; internal set} (L5768; settable by parser after creation). GetPureExpression: single CommandExpressionAst with zero redirections -> its Expression else null (L5773-5787). Visit PipelineElements in order.
- CommandElementAst L5830 abstract. CommandParameterAst L5853: ParameterName (no dash/colon), Argument (only for -Name:value form; otherwise null and the following argument is separate command element), ErrorPosition (required). Visit Argument only.
- CommandBaseAst L5949 abstract : StatementAst: Redirections (never null), internal const MaxRedirections = (int)RedirectionStream.Information + 1 (L5954).

## W21 L6001-6300
- CommandAst L5987: ctor(extent, elements, TokenKind invocationOperator, redirections): elements non-empty; invocationOperator must be Dot, Ampersand or Unknown (L6016). GetCommandName(): CommandElements[0] as StringConstantExpressionAst -> .Value else null (L6048). DefiningKeyword {get;set} (DynamicKeyword that created the command) preserved by Copy. Visit: CommandElements then Redirections.
- CommandExpressionAst L6116: Expression required; Redirections; visit Expression then Redirections.
- RedirectionAst L6191 abstract (FromStream). RedirectionStream enum {All=0,Output=1,Error=2,Warning=3,Verbose=4,Debug=5,Information=6} L6214 => MaxRedirections = 7. MergingRedirectionAst L6255: (extent, from, to); ToStream "must always be Output" per doc; no validation in ctor (L6264-6268). Leaf node.

## W22 L6301-6600
- FileRedirectionAst L6302: ctor(extent, stream, ExpressionAst file, append): file mandatory (ArgumentNull); Location, Append; visit Location.
- AssignmentStatementAst L6379 : PipelineBaseAst: ctor(extent, ExpressionAst left, TokenKind operator, StatementAst right, IScriptExtent errorPosition): all non-null; operator must carry TokenFlags.AssignmentOperator (L6401); NORMALIZATION: if right is a non-background PipelineAst with exactly one CommandExpressionAst element, right is replaced by that CommandExpressionAst (ClearParent first) (L6406-6415) — so Right is CommandExpressionAst or PipelineAst(multi/background/command) or other StatementAst (e.g. if/try). GetAssignmentTargets: Left ArrayLiteralAst elements else Left (L6461). Visit Left then Right.
- ConfigurationType {Resource=0, Meta=1} L6500. ConfigurationDefinitionAst L6516: ctor(extent, ScriptBlockExpressionAst body, ConfigurationType, ExpressionAst instanceName); Copy copies LCurlyToken, ConfigurationToken, CustomAttributes (set after construction) L6579-6589. Accept needs ICustomAstVisitor2 -> VisitConfigurationDefinition.

## W23 L6601-6900 (DSC; OUT-OF-SCOPE-DOCUMENTED)
- ConfigurationDefinitionAst.InternalVisit L6599-6620: v2 only VisitConfigurationDefinition; then InstanceName, then Body — OBSERVATION: `Body.InternalVisit(visitor);` at L6616 discards the returned action (not assigned to `action`), so a Stop/SkipChildren from inside Body is not propagated to the post-action.
- internal props LCurlyToken, ConfigurationToken, CustomAttributes, DefinedKeywords (List<DynamicKeyword>) L6626-6637. GenerateSetItemPipelineAst L6645-6785 synthesizes at parse time a `set-item -Path function:\<name> -Value <scriptblock>` PipelineAst whose function body calls PSDesiredStateConfiguration\Configuration with -ArgsToBody -Name -ResourceModuleTuplesToImport -Body -Outputpath -ConfigurationData -InstanceName; parameters from ConfigurationBuildInParameters (string const L6887+). It builds BinaryExpressionAst(Plus) etc. (shows AST synthesized with token Extents). SetParent(returnPipelineAst) is invoked on `this` (sets pipeline's parent = this?? no: this.SetParent(child) sets child.Parent = this).
- IsImportCommand L6796 uses StaticParameterBinder.BindCommand and IsConstantValueVisitor.IsConstant(..., true, true) for Import-DscResource (links to ConstantValues.cs).

## W24 L6901-7200 (DSC)
- Static lazily-built caches in ConfigurationDefinitionAst: s_configurationBuildInParameters (L6927), s_configurationBuildInParameterAttrAsts (L6963), s_configurationExtraParameterStatements (L6995) — built by Parser.ParseInput on fixed text; NOT thread-safe lazily (no lock) [INFERENCE from absence of lock in L6903-6995].
- DynamicKeywordStatementAst L7003 : StatementAst: ctor(extent, commandElements non-empty); CommandElements = keyword name, instance name, body (ScriptBlockExpressionAst for Node, HashtableAst otherwise). Copy copies internals Keyword (value.Copy() in setter L7101), LCurly, FunctionName, InstanceName, OriginalInstanceName, BodyExpression, ElementName. Accept requires ICustomAstVisitor2. Visit CommandElements (all visitors). GenerateCommandCallPipelineAst (L7123) memoizes _commandCallPipelineAst; builds PipelineAst of command call with module-qualified name Keyword.ImplementingModule + '\\' + FunctionName.Text.

## W25 L7201-7500
- GenerateCommandCallPipelineAst DirectCall vs non-direct (L7172-7322): DirectCall maps hashtable entries to CommandParameterAst with SubExpressionAst-wrapped values; invalid hashtable -> fake parameter "InvalidPropertyHashtable" (for tab completion); non-direct adds -KeywordData ([DynamicKeyword]::GetKeyword(name) via InvokeMemberExpressionAst(static:true)), -Name, -Value, -SourceMetadata ("file::line::col::text"). Result CommandAst.DefiningKeyword = Keyword; PipelineAst memoized.
- #endregion Statements at L7337. ExpressionAst L7344 abstract : CommandElementAst: virtual Type StaticType => typeof(object) (L7361); internal virtual ShouldPreserveOutputInCaseOfException (L7372): only meaningful for ParenExpressionAst/SubExpressionAst (note: the guard `PSTraceSource.NewInvalidOperationException()` creates but does not throw, L7374-7377); true when expr is sole element of a pipeline whose parent is StatementBlockAst/NamedBlockAst (or a Paren that qualifies recursively).
- TernaryExpressionAst L7404 (Q4: `?:`): ctor(extent, condition, ifTrue, ifFalse) all required; props Condition, IfTrue, IfFalse; Accept returns null for non-v2 visitor; InternalVisit v2-gated VisitTernaryExpression; children Condition, IfTrue, IfFalse for all visitors.

## W26 L7501-7800
- BinaryExpressionAst L7502: ctor(extent,left,TokenKind op,right,errorPosition); op must have TokenFlags.BinaryOperator (L7524); props Operator, Left, Right, ErrorPosition. StaticType: bool for Xor/And/Or/Is, else object (L7576-7591) [note -isnot/-in/-contains etc. not listed -> object]. Internal static PSTypeName arrays BoolTypeNameArray, StringTypeNameArray, StringArrayTypeNameArray L7593-7595 (type inference). Visit Left, Right.
- UnaryExpressionAst L7622: ctor(extent, TokenKind, child); kind must have TokenFlags.UnaryOperator (L7639); property TokenKind; StaticType bool for Not/Exclaim else object. Visit Child.
- BlockStatementAst L7710 (workflow remnants `parallel {}`/`sequence {}`): kind Token must be TokenKind.Sequence or Parallel; Body StatementBlockAst.
- AttributedExpressionAst L7779 : ExpressionAst, ISupportsAssignment, IAssignableValue: ctor(extent, AttributeBaseAst attribute, ExpressionAst child).

## W27 L7801-8100
- AttributedExpressionAst: props Child, Attribute (AttributeBaseAst); visit Attribute then Child. "Code Generation Details" (L7847-7900): implements ISupportsAssignment.GetAssignableValue (returns this), IAssignableValue.GetValue -> Accept(compiler) (compiler is an ICustomAstVisitor), SetValue: collects attribute chain (GetAttributes reversed), finds innermost ISupportsAssignment child (cast guaranteed by semantic checks), if var -> Compiler.CallSetVariable(Constant(variableExpr.VariablePath), rhs, Constant(attributes.ToArray())) else assignable.SetValue(Compiler.ConvertValue(rhs, attributes)). -> AST nodes hold compile-time assignment logic (AST<->Compiler coupling; T25).
- ConvertExpressionAst L7906 : AttributedExpressionAst: Type => (TypeConstraintAst)Attribute; StaticType = TypeName.GetReflectionType() ?? object (L7944); GetAssignableValue: if Child is VariableExpressionAst with TupleIndex >= 0 return varExpr (type saved in mutable tuple) else this (L7972-7983); IsRef() => TypeName.Name equals "ref" (L7985).
- MemberExpressionAst L7997 : ExpressionAst, ISupportsAssignment: ctor(extent, expression, CommandElementAst member, bool static) + overload with bool nullConditional; Member is a CommandElementAst (StringConstant for name or expression); Static; NullConditional {get; protected set} true for `?.` or `?[]` (doc L8065); Q4 `?.` = MemberExpressionAst.NullConditional / InvokeMemberExpressionAst; `?[]` IndexExpressionAst. visit Expression, Member.

## W28 L8101-8400
- MemberExpressionAst.GetAssignableValue => new MemberAssignableValue{MemberExpression=this} (L8106; class defined in Compiler.cs, T25).
- InvokeMemberExpressionAst L8115: 4 ctors (genericTypes; no generics; nullConditional+generics; nullConditional). Arguments null if none (L8143); GenericTypeArguments ReadOnlyCollection<ITypeName> (not Ast, not parented). Visit: Expression, Member, Arguments (InternalVisitChildren L8286). GetAssignableValue => InvokeMemberAssignableValue.
- BaseCtorInvokeMemberExpressionAst L8315: ctor(baseKeywordExtent, baseCallExtent, args) -> base(baseCallExtent, VariableExpressionAst($this), StringConstant ".ctor" BareWord, args, static:false). Accept requires v2; InternalVisit calls VisitBaseCtorInvokeMemberExpression only for AstVisitor2 but children for all. No Copy override -> inherited InvokeMemberExpressionAst.Copy builds a plain InvokeMemberExpressionAst (INFERENCE: loses the BaseCtor type on Copy, L8253-8267 vs L8315-8363).
- ITypeName interface L8369 (public; #nullable enable): FullName, Name, AssemblyName?, IsArray, IsGeneric, GetReflectionType() ... (continues).

## W29 L8401-8700 (ITypeName family: NOT Ast nodes)
- ITypeName members: FullName, Name, AssemblyName?, IsArray, IsGeneric, GetReflectionType(), GetReflectionAttributeType(), Extent (L8369-8412). internal ISupportsTypeCaching { Type? CachedType {get;set} } L8416.
- TypeName sealed L8425 : ITypeName, ISupportsTypeCaching. Fields _name,_extent,_genericArgumentCount,_type (L8427-8430), internal TypeDefinitionAst _typeDefinitionAst (L8432). Ctors: (extent,name) validates first char not [ ] , and normalizes "``"->"`" (L8445-8465); (extent,name,assembly); internal (extent,name,genericArgumentCount). FullName = name + ","+assembly if assembly (L8510). IsArray/IsGeneric always false. HasDefaultCtor L8537 (pessimistic when unresolved). GetReflectionType L8579-8621: if _type null: _typeDefinitionAst.Type (script class) else TypeResolver.ResolveTypeName(this,out _) [T24/T28]; retries name+"`N" if unresolved and genericArgumentCount>0; touches TypeHandle to detect TypeBuilder (NotSupportedException => returns un-cached TypeBuilder); caches via Interlocked.CompareExchange (thread-safe publish). GetReflectionAttributeType L8631: try as-is if Attribute-assignable else name+"Attribute". SetTypeDefinition L8651 asserts single assignment. Equals/GetHashCode case-insensitive on name+assembly.

## W30 L8701-9000
- TypeName.IsType(Type) L8704: compares Name against type.FullName or its last segment (documented as used for 'Void' only). ISupportsTypeCaching.CachedType explicit impl.
- GenericTypeName sealed L8729: ctor(extent, ITypeName genericTypeName, IEnumerable<ITypeName> args) args non-empty else ArgumentException; FullName "Name[arg1,arg2]" + ",assembly" cached via Interlocked.CompareExchange (L8776-8811); Name (not cached) uses arg Names; IsArray false, IsGeneric true. GetReflectionType L8874: resolves open generic via GetGenericType (retries name + "`N" when no backtick) then MakeGenericType(args); returns null if any arg unresolved; TypeHandle probe: NotSupportedException => returns type uncached (self-referential class definitions, L8896-8908); other exceptions swallowed (L8912-8915). GetReflectionAttributeType L8955 tries 'XAttribute`N'.

## W31 L9001-9300
- GenericTypeName Equals/GetHashCode structural; ArrayTypeName sealed L9040: ctor(extent, elementType, rank>0); FullName/Name "Elem[,]" (rank-1 commas); GetName guarded by RuntimeHelpers.EnsureSufficientExecutionStack; InsufficientExecutionStackException -> ScriptCallDepthException (L9078-9102, 9164-9198) = recursion guard on nested type names; GetReflectionType: MakeArrayType(rank==1 ? () : (rank)), TypeHandle probe, cached via Interlocked.CompareExchange; GetReflectionAttributeType => null; IsArray true.
- ReflectionTypeName sealed L9245: wraps System.Type; FullName/Name via ToStringCodeMethods.Type(_type) (PowerShell syntax), AssemblyName _type.Assembly.FullName, Extent = PositionUtilities.EmptyExtent; used by TypeConstraintAst(extent, Type).

## W32 L9301-9600
- ReflectionTypeName: GetReflectionType/AttributeType return _type; ISupportsTypeCaching.CachedType setter throws InvalidOperationException (L9334-9339).
- TypeExpressionAst L9345: leaf, TypeName (ITypeName not parented, not an Ast child); StaticType => typeof(Type) (L9382). Copy shares TypeName.
- VariableExpressionAst L9404 : ExpressionAst, ISupportsAssignment, IAssignableValue: ctors (extent, name, splatted) -> new VariablePath(name) [name not stripped of $/@ per doc]; internal (VariableToken) Splatted = Kind==SplattedVariable; (extent, VariablePath, splatted). IsConstantVariable(): VariablePath.IsVariable && unqualified path is $true/$false/$null (SpecialVariables.True/False/Null) (L9476-9490). IsSafeVariableReference(validVariables, ref usesParameter) L9500: IsAnyLocal && (in validVariables or 'args' -> ok, usesParameter) else !Splatted && IsConstantVariable.
- Code-generation cached fields: TupleIndex = VariableAnalysis.Unanalyzed, Automatic, Assigned (L9540-9544) set by VariableAnalysis (T24). IAssignableValue.SetValue (L9556+): $null assignment discards (returns rhs); computes targetType via GetVariableType(compiler,out tupleAccessPath,out localInTuple); for object/PSObject lhs and rhs inserts PSVariableAssignmentBinder dynamic site to copy mutable value types (L9567-9586).

## W33 L9601-9900
- VariableExpressionAst.GetVariableType L9604: localInTuple = TupleIndex >= 0 && (compiler.Optimize || TupleIndex < (int)AutomaticVariable.NumberOfAutomaticVariables); tuple access path via MutableTuple.GetAccessPath(compiler.LocalVariablesTupleType, TupleIndex); else target object. => unoptimized compile only keeps automatic variables in tuple (T25 owns).
- ConstantExpressionAst L9631: Value (object; null only for null constant); ctor(extent, value); internal ctor(NumberToken). StaticType = Value?.GetType() ?? object. Leaf.
- StringConstantType enum {SingleQuoted, SingleQuotedHereString, DoubleQuoted, DoubleQuotedHereString, BareWord} L9693 (declared order, no explicit values).
- StringConstantExpressionAst L9732 : ConstantExpressionAst: value non-null; `new string Value`; StaticType string; MapTokenKindToStringConstantKind L9786: StringExpandable->DoubleQuoted, HereStringLiteral->SingleQuotedHereString, HereStringExpandable->DoubleQuotedHereString, StringLiteral->SingleQuoted, Generic->BareWord, else InvalidOperationException.
- ExpandableStringExpressionAst L9825: public ctor(extent, value, type in {DoubleQuoted,DoubleQuotedHereString,BareWord}) calls Language.Parser.ScanString(value) (AST construction re-enters the parser, L9857); if result not expandable => FormatExpression "{0}" with single nested expr; NestedExpressions ClearParent then SetParents (L9873-9878). internal ctor from token with formatString+nested (non-empty asserted).

## W34 L9901-10200
- ExpandableStringExpressionAst: props Value (unexpanded), StringConstantType, NestedExpressions (Variable or SubExpression asts, non-empty), internal FormatExpression (from scanner); StaticType string; Copy preserves FormatExpression via private ctor; visit NestedExpressions.
- ScriptBlockExpressionAst L9979: ScriptBlock required; StaticType typeof(ScriptBlock); visit ScriptBlock.
- ArrayLiteralAst L10048 : ISupportsAssignment: ctor(extent, IList<ExpressionAst> elements non-empty); wraps the IList directly in ReadOnlyCollection (no copy: INFERENCE caller mutation visible, L10069); StaticType object[]; GetAssignableValue => ArrayAssignableValue (Compiler.cs).
- HashtableAst L10128: KeyValuePairs = ReadOnlyCollection<Tuple<ExpressionAst,StatementAst>> (value is a StatementAst); StaticType Hashtable; internal IsSchemaElement {get;set}.

## W35 L10201-10500
- HashtableAst visit: for each pair Item1 (key) then Item2 (value statement).
- ArrayExpressionAst L10224 `@( )`: SubExpression StatementBlockAst; StaticType object[]. ParenExpressionAst L10290: Pipeline (PipelineBaseAst); GetAssignableValue => ((ISupportsAssignment)Pipeline.GetPureExpression()).GetAssignableValue() (unguarded cast; relies on semantic checks). SubExpressionAst L10356 `$( )`: SubExpression StatementBlockAst. [ShouldPreserveOutputInCaseOfException applies to Paren/Sub.]
- UsingExpressionAst L10416 ($using:x): SubExpression (ExpressionAst); internal int RuntimeUsingIndex = -1 at ctor (code-gen slot, set by compiler/ScriptBlockToPowerShell) preserved by Copy; internal const UsingPrefix = "__using_" (L10465) used for text rewriting; public static ExtractUsingVariable(UsingExpressionAst) L10477.

## W36 L10501-10845 (end)
- UsingExpressionAst.ExtractUsingVariableImpl L10489: recursion via Using/Index(Target)/Member(Expression) to the VariableExpressionAst; else Assert(false)+null. Visit SubExpression.
- IndexExpressionAst L10555: Target, Index, NullConditional {get;} (readonly, unlike MemberExpressionAst's protected set); ctor overload with nullConditional; GetAssignableValue => IndexAssignableValue. Visit Target, Index. (Q4: `?[]`.)
- CommentHelpInfo sealed L10655 (not Ast): Synopsis, Description, Notes, Parameters, Links, Examples, Inputs, Outputs, Component, Role, Functionality, ForwardHelpTargetName/Category, RemoteHelpRunspace, MamlHelpFile; GetCommentBlock() renders `<# ... #>` text.
- FILE COMPLETE 1-10845.
- Public non-Ast types in file: ScriptRequirements L713, ITypeName L8369, TypeName L8425, GenericTypeName L8729, ArrayTypeName L9040, ReflectionTypeName L9245, CommentHelpInfo L10655; internal ISupportsAssignment L34, IAssignableValue L39, IParameterMetadataProvider L56, ISupportsTypeCaching L8416, SpecialMemberFunctionType L3635; public enums TypeAttributes L2648, UsingStatementKind L2870, PropertyAttributes L3132, MethodAttributes L3321, ForEachFlags L4344, SwitchFlags L4746, RedirectionStream L6214, ConfigurationType L6500, StringConstantType L9693.
