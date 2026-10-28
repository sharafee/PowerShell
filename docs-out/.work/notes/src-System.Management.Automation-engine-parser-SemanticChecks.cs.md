# Notes SemanticChecks.cs (T24)
## W1 1-300
- L21 `internal sealed partial class SemanticChecks : AstVisitor2, IAstPostVisitHandler`; entry `CheckAst(Parser, ScriptBlockAst)` L39-47 pushes root onto `_scopeStack`, `ast.InternalVisit(checker)`, asserts stacks balanced.
- statics s_isConstantAttributeArgVisitor / ForClassVisitor (IsConstantValueVisitor) L25-34.
- CheckForDuplicateParameters L85-112: DuplicateFormalParameter L95 (ordinal-ignore-case set of UserPath), VoidTypeConstraintNotAllowed L106.
- VisitParamBlock L114, VisitTypeConstraint L121 -> CheckArrayTypeNameDepth.
- VisitAttribute L128-268: target computation (class/enum/interface, property/field, ctor/method, param-of-method), AttributeNotAllowedOnDeclaration L186, PropertyNotFoundForAttribute L202, ReadOnlyProperty (ExtendedTypeSystem) L217/L229, DuplicateNamedArgument L243, non-constant arg errors L253/L263 (id dynamic via GetNonConstantAttributeArgErrorExpr L73: class ctx -> ParameterAttributeArgumentNeedsToBeConstant else ...OrScriptBlock).
## W2 300-600
- VisitParameter L296: OrderedAttributeOnlyOnHashLiteralNode L306 (param constraint [ordered]); MultipleTypeConstraintsOnMethodParam L318 (class method param).
- VisitTypeExpression L332 depth check + MarkAstParentsAsSuspicious when [Type].
- CheckArrayTypeNameDepth L345: limit 200 -> ScriptTooComplicated L354.
- VisitTypeDefinition L371: finds DscResourceAttribute -> DscResourceChecker.CheckType L386.
- VisitFunctionMember L392: pushes _memberScopeStack; ParamBlockNotAllowedInMethod L399; NamedBlockNotAllowedInMethod L410; ConstructorCantHaveReturnType L417; calls VariableAnalysis.AnalyzeMemberFunction L423 (!); MethodHasCodePathNotReturn L426.
- VisitFunctionDefinition L434: OnlyOneParameterListAllowed L439; DuplicateFormal via CheckForDuplicateParameters L445; WorkflowNotSupportedInPowerShellCore L450.
- VisitSwitchStatement L458: KeywordParameterReservedForFutureUse L463 (-parallel).
- VisitDataStatement L483: RestrictedLanguageChecker(_parser, allowedCommands, null, false) over Body L487.
- VisitForEachStatement L493: KeywordParameterReservedForFutureUse L498 (parallel), L508 (throttlelimit), ThrottleLimitRequiresParallelFlag L520.
- VisitTryStatement L529: EmptyCatchNotLast L545, ExceptionTypeAlreadyCaught L572.
## W3 600-900
- CheckLabelExists L591: LabelNotFound L605 only when inside a FunctionMemberAst (class method).
- CheckForFlowOutOfFinally L630: ControlLeavingFinally L658.
- VisitBreak L680/ VisitContinue L689; CheckForReturnStatement L698: VoidMethodHasReturn L709, NonVoidMethodMissingReturnValue L718; VisitReturn L725.
- CheckAssignmentTarget L738: callback reportError; void in convert L800 (VoidTypeConstraintNotAllowed), ReferenceNeedsToBeByItselfInTypeConstraint L811, AssignmentStatementToAutomaticNotSupported L831; null-conditional member/index disallowed as target (errorAst -> InvalidLeftHandSide via callback).
- VisitAssignmentStatement L866 InvalidLeftHandSide L870.
- VisitBinaryExpression L877: &&/|| appearing as BinaryExpressionAst -> InvalidEndOfLine L882.
- VisitUnaryExpression L891: ++/-- -> OperatorRequiresVariableOrProperty L900.
## W4 900-1200
- VisitConvertExpression L910: [ordered] non-hashtable -> OrderedAttributeOnlyOnHashLiteralNode L919; [ref][ref] ReferenceNeedsToBeByItselfInTypeSequence L947; ReferenceNeedsToBeLastTypeInTypeConversion L994; [Type] -> MarkAstParentsAsSuspicious L1007.
- VisitUsingExpression L1013 -> CheckUsingExpression L1031: allowed: variable, member (non-invoke, string-const member) chain, index with constant index; else InvalidUsingExpression L1023.
- VisitVariableExpression L1061: SplattingNotPermittedInArgumentList L1069, SplattingNotPermitted L1076; VariableNotLocal L1092 when TupleIndex==VariableAnalysis.ForceDynamic && !Assigned && !global && !script && !constant && !implicit-class-method var (reads tuple index set by VariableAnalysis); NonStaticMemberAccessInStaticMember L1102 for $this.
- VisitHashtable L1112: DuplicatePropertyInInstanceDefinition L1127 / DuplicateKeyInHashLiteral L1132 -> report L1136.
- VisitAttributedExpression L1144: UnexpectedAttribute L1158.
- VisitBlockStatement L1166: UnexpectedKeyword L1173 unless IsInWorkflow.
- VisitMemberExpression/InvokeMember L1181/1187 CheckMemberAccess L1193 -> MarkAstParentsAsSuspicious when member not constant.
## W5 1200-1500
- MarkAstParentsAsSuspicious L1211: sets Ast.HasSuspiciousContent=true up the parent chain (used for [Type] expr/convert, non-constant member names, static member on non-type expr).
- VisitScriptBlock L1225 push _scopeStack, push null on _memberScopeStack unless script block is a method body. VisitScriptBlockExpression L1238 DSC: ResourceNotDefined L1290 (CommandAst + ScriptBlockExpr inside configuration).
- VisitUsingStatement L1311: supported kinds Namespace/Assembly/Module; else (or alias) UsingStatementNotSupported L1317; InvalidNamespaceValue L1328 via GeneratedRegex NamespacePattern L1354.
- VisitConfigurationDefinition L1357: UnsupportedNamedBlockInConfiguration L1370.
- VisitDynamicKeywordStatement L1382: Keyword.SemanticCheck callback (DynamicKeywordSemanticCheckException L1397; errors passed through L1393); ConfigurationInvalidPropertyName L1417; InvalidInstanceProperty L1428; RegularResourceUsedInMetaConfig L1452; MetaConfigurationUsedInRegularConfig L1459 (ICrossPlatformDsc subsystem or DscClassCache.SystemResourceNames).
- VisitPropertyMember L1470: TypeNotAllowedForProperty L1479 (void / generic type definition); pushes member scope.
- PostVisit L1490: pops member/ scope stacks; sets scriptBlockAst.PostParseChecksPerformed = true L1503; HadErrors |= parser.ErrorList.Count>0 L1507.
## W6 1500-1800 DscResourceChecker L1516-1805
- CheckType L1524: members scan: Set/Get/Test/default ctor/key; LookupRequiredMembers base types L1620; errors: DscResourceMissingSetMethod L1573, MissingGetMethod L1581, MissingTestMethod L1589, MissingDefaultConstructor L1597 (non-default ctor & no default), MissingKeyProperty L1605; DscResourceInvalidGetMethod L1693/1701 (Get with 0 params must return class type or array); CheckTest requires bool return & 0 params L1717; CheckSet 0 params void L1734; CheckKey L1752 DscPropertyAttribute Key=true; DscResourceInvalidKeyProperty L1793 (type must be string/integer/enum).
## W7 1800-2455 RestrictedLanguageChecker L1807-2454
- ctor(parser, allowedCommands, allowedVariables, allowEnvironmentVariables) L1815; single "*" => all variables allowed; default allowed s_defaultAllowedVariables L2304 = PSCulture, PSUICulture, true, false, null.
- Runtime entry points: CheckDataStatementLanguageModeAtRuntime L1850 (CLM: throws DataSectionAllowedCommandDisallowed unless system lockdown policy is Audit, then WDAC audit log); CheckDataStatementAstAtRuntime L1874; EnsureUtilityModuleLoaded L1885.
- Visitor rows: ScriptBlock L1904 ScriptBlockNotSupportedInDataSection; ParamBlock L1913; TypeConstraint/TypeExpression -> CheckTypeName L1927 (TypeCode.Object rejected, unresolved rejected) TypeNotAllowedInDataSection L1939; Attribute L1955; FunctionDefinition L1978; Trap L2001; Switch L2010; DataStatement L2019; ForEach L2028; DoWhile L2037; For L2046; While L2055; Try L2071; Break/Continue/Return/Exit/Throw FlowControl L2080..2116; DoUntil L2125; Assignment L2135; Command: Dot-sourcing DotSourcingNotSupportedInDataSection L2158, command-name not allowed L2172 (&) / L2179 / L2193 CmdletNotInAllowedListForDataSection (if _allowedCommands null any command allowed); Redirection L2217/L2226; Binary op with TokenFlags.DisallowedInRestrictedMode L2245 -> OperatorNotSupportedInDataSection L2247; Unary L2258; Variable L2307 VariableReferenceNotSupportedInDataSection L2346 (env: drive allowed when allowEnvironmentVariables - module manifests L2317); Member L2356, InvokeMember L2365, Index L2421 ArrayReference, AttributedExpression L2431, BlockStatement L2441 ParallelAndSequence, ScriptBlockExpression L2395.
- Allowed: constants, sub-expressions, array literals/expressions, hashtables, paren, expandable strings (REVIEW comment L2411), convert (type checked), using expression, if/pipeline/statement blocks, command expressions.
