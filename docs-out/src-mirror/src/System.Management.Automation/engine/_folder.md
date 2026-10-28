# src/System.Management.Automation/engine

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| A:34, B:111 | System.Management.Automation | 145 | 151818 | 539 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `AliasInfo.cs` | 362 | `AliasInfo` |  |  |
| `ApplicationInfo.cs` | 142 | `ApplicationInfo` |  |  |
| `ArgumentToVersionTransformationAttribute.cs` | 58 | `ArgumentToVersionTransformationAttribute` |  |  |
| `ArgumentTypeConverterAttribute.cs` | 208 | `ArgumentTypeConverterAttribute` |  |  |
| `AsyncByteStreamTransfer.cs` | 83 | `AsyncByteStreamTransfer` |  |  |
| `Attributes.cs` | 2364 | `ValidateRangeAttribute`, `ParameterAttribute`, `ValidateSetAttribute`, `ValidateNotNullOrAttributeBase` (+36) |  |  |
| `AutomationEngine.cs` | 129 | `AutomationEngine` |  |  |
| `AutomationNull.cs` | 33 | `AutomationNull` |  |  |
| `BytePipe.cs` | 113 | `FileBytePipe`, `NativeCommandProcessorBytePipe`, `BytePipe` |  |  |
| `ChildrenCmdletProviderInterfaces.cs` | 786 | `ChildItemCmdletProviderIntrinsics`, `ReturnContainers` |  |  |
| `CmdletFamilyProviderInterfaces.cs` | 109 | `ProviderIntrinsics` |  |  |
| `CmdletInfo.cs` | 558 | `CmdletInfo` |  |  |
| `CmdletParameterBinderController.cs` | 4653 | `CmdletParameterBinderController`, `DefaultParameterDictionary` |  |  |
| `CodeMethods.cs` | 135 | `AdapterCodeMethods`, `ToStringCodeMethods` |  |  |
| `CommandBase.cs` | 604 | `InternalCommand`, `PSCmdlet`, `ActionPreference`, `ConfirmImpact` (+2) |  |  |
| `CommandDiscovery.cs` | 1646 | `CommandDiscovery`, `LookupPathCollection`, `CommandLookupEventArgs`, `CommandDiscoveryEventSource` (+1) |  |  |
| `CommandInfo.cs` | 984 | `CommandInfo`, `PSTypeName`, `PSSyntheticTypeName`, `CommandTypes` (+2) |  |  |
| `CommandMetadata.cs` | 1551 | `CommandMetadata`, `SessionCapabilities` |  |  |
| `CommandParameter.cs` | 230 | `CommandParameterInternal` |  |  |
| `CommandPathSearch.cs` | 596 | `CommandPathSearch` |  |  |
| `CommandProcessor.cs` | 869 | `CommandProcessor` |  |  |
| `CommandProcessorBase.cs` | 1044 | `CommandProcessorBase` |  |  |
| `CommandSearcher.cs` | 1733 | `CommandSearcher`, `SearchResolutionOptions` |  |  |
| `CommonCommandParameters.cs` | 284 | `CommonParameters` |  |  |
| `CompiledCommandParameter.cs` | 683 | `CompiledCommandParameter`, `ParameterCollectionTypeInformation`, `ParameterCollectionType` |  |  |
| `ConfigurationInfo.cs` | 172 | `ConfigurationInfo` |  |  |
| `ContentCmdletProviderInterfaces.cs` | 594 | `ContentCmdletProviderIntrinsics` |  |  |
| `CoreAdapter.cs` | 6259 | `DotNetAdapter`, `Adapter`, `MethodInformation`, `XmlNodeAdapter` (+12) |  |  |
| `Credential.cs` | 404 | `PSCredential`, `PSCredentialUIOptions`, `PSCredentialTypes`, `GetSymmetricEncryptionKey` |  |  |
| `CultureVariable.cs` | 59 | `PSCultureVariable`, `PSUICultureVariable` |  |  |
| `DataStoreAdapter.cs` | 832 | `PSDriveInfo` |  |  |
| `DataStoreAdapterProvider.cs` | 688 | `ProviderInfo` |  |  |
| `DefaultCommandRuntime.cs` | 246 | `DefaultCommandRuntime` |  |  |
| `DriveInterfaces.cs` | 394 | `DriveManagementIntrinsics` |  |  |
| `DriveNames.cs` | 37 | `DriveNames` |  |  |
| `DscResourceInfo.cs` | 163 | `DscResourceInfo`, `DscResourcePropertyInfo`, `ImplementedAsType` |  |  |
| `DscResourceSearcher.cs` | 212 | `DscResourceSearcher` |  |  |
| `EngineIntrinsics.cs` | 113 | `EngineIntrinsics` |  |  |
| `EnumExpressionEvaluator.cs` | 644 | `FlagsExpression<T>` |  |  |
| `EnumMinimumDisambiguation.cs` | 127 | `EnumMinimumDisambiguation` |  |  |
| `ErrorPackage.cs` | 1837 | `ErrorRecord`, `ErrorDetails`, `ErrorCategoryInfo`, `ErrorCategory` (+3) |  |  |
| `EventManager.cs` | 2648 | `PSLocalEventManager`, `PSEventManager`, `PSRemoteEventManager`, `PSEventSubscriber` (+11) |  |  |
| `ExecutionContext.cs` | 1711 | `ExecutionContext`, `EngineState` |  |  |
| `ExtendedTypeSystemException.cs` | 641 | `PSInvalidCastException`, `MethodException`, `MethodInvocationException`, `ExtendedTypeSystemException` (+5) |  |  |
| `ExternalScriptInfo.cs` | 633 | `ExternalScriptInfo`, `PSSnapInSpecification`, `ScriptRequiresSyntaxException` |  |  |
| `ExtraAdapter.cs` | 385 | `DirectoryEntryAdapter` |  |  |
| `FilterInfo.cs` | 140 | `FilterInfo` |  |  |
| `FunctionInfo.cs` | 497 | `FunctionInfo` |  |  |
| `GetCommandCommand.cs` | 1743 | `GetCommandCommand`, `NounArgumentCompleter` |  |  |
| `ICommandRuntime.cs` | 622 | `ICommandRuntime`, `ICommandRuntime2` |  |  |
| `InformationRecord.cs` | 264 | `InformationRecord`, `HostInformationMessage` |  |  |
| `InitialSessionState.cs` | 5674 | `InitialSessionState`, `PSSnapInHelpers`, `InitialSessionStateEntryCollection<T>`, `SessionStateVariableEntry` (+14) |  |  |
| `InternalCommands.cs` | 2752 | `WhereObjectCommand`, `ForEachObjectCommand`, `SetPSDebugCommand`, `SetStrictModeCommand` (+2) |  |  |
| `InvocationInfo.cs` | 537 | `InvocationInfo`, `RemoteCommandInfo` |  |  |
| `ItemCmdletProviderInterfaces.cs` | 2107 | `ItemCmdletProviderIntrinsics`, `CopyContainers` |  |  |
| `LanguagePrimitives.cs` | 5888 | `LanguagePrimitives`, `PSTypeConverter`, `ConvertThroughString`, `ConversionRank` |  |  |
| `ManagementObjectAdapter.cs` | 1264 | `BaseWMIAdapter`, `ManagementClassApdapter`, `ManagementObjectAdapter` |  |  |
| `MergedCommandParameterMetadata.cs` | 717 | `MergedCommandParameterMetadata`, `MergedCompiledCommandParameter`, `ParameterBinderAssociation` |  |  |
| `MinishellParameterBinderController.cs` | 384 | `MinishellParameterBinderController` |  |  |
| `MshCmdlet.cs` | 1030 | `CommandInvocationIntrinsics`, `SwitchParameter`, `PSCmdlet`, `IDynamicParameters` |  |  |
| `MshCommandRuntime.cs` | 3830 | `MshCommandRuntime` |  |  |
| `MshMemberInfo.cs` | 5157 | `PSMemberInfoIntegratingCollection<T>`, `PSCodeProperty`, `PSScriptProperty`, `PSMemberInfoInternalCollection<T>` (+42) |  |  |
| `MshObject.cs` | 2643 | `PSObject`, `ToStringCodeMethods`, `PSCustomObject`, `WriteStreamType` (+1) |  |  |
| `MshObjectTypeDescriptor.cs` | 769 | `PSObjectTypeDescriptor`, `PSObjectPropertyDescriptor`, `PSObjectTypeDescriptionProvider`, `GettingValueExceptionEventArgs` (+1) |  |  |
| `MshReference.cs` | 90 | `PSReference`, `PSReference<T>` |  |  |
| `MshSecurityException.cs` | 111 | `PSSecurityException` |  |  |
| `MshSnapinQualifiedName.cs` | 134 | `PSSnapinQualifiedName` |  |  |
| `NativeCommand.cs` | 36 | `NativeCommand` |  |  |
| `NativeCommandParameterBinder.cs` | 520 | `NativeCommandParameterBinder` |  |  |
| `NativeCommandParameterBinderController.cs` | 106 | `NativeCommandParameterBinderController` |  |  |
| `NativeCommandProcessor.cs` | 2651 | `NativeCommandProcessor`, `ProcessOutputHandler`, `ProcessInputWriter`, `RemoteException` (+6) |  |  |
| `NullString.cs` | 45 | `NullString` |  |  |
| `ObjectEventRegistrationBase.cs` | 232 | `ObjectEventRegistrationBase` |  |  |
| `OrderedHashtable.cs` | 236 | `OrderedHashtable` |  |  |
| `PSClassInfo.cs` | 86 | `PSClassInfo`, `PSClassMemberInfo` |  |  |
| `PSClassSearcher.cs` | 329 | `PSClassSearcher` |  |  |
| `PSConfiguration.cs` | 794 | `PowerShellConfig`, `PowerShellPolicies`, `ConfigScope`, `Transcription` (+7) |  |  |
| `PSVersionInfo.cs` | 1038 | `SemanticVersion`, `PSVersionInfo`, `PSVersionHashTable` |  |  |
| `ParameterBinderBase.cs` | 2067 | `ParameterBinderBase`, `CommandLineParameters`, `ParameterBindingFlags`, `UnboundParameter` (+1) |  |  |
| `ParameterBinderController.cs` | 1326 | `ParameterBinderController` |  |  |
| `ParameterInfo.cs` | 146 | `CommandParameterInfo` |  |  |
| `ParameterSetInfo.cs` | 345 | `CommandParameterSetInfo` |  |  |
| `ParameterSetPromptingData.cs` | 62 | `ParameterSetPromptingData` |  |  |
| `ParameterSetSpecificMetadata.cs` | 214 | `ParameterSetSpecificMetadata` |  |  |
| `PathInterfaces.cs` | 1414 | `PathIntrinsics` |  |  |
| `Pipe.cs` | 622 | `Pipe`, `VariableStreamKind` |  |  |
| `PositionalCommandParameter.cs` | 27 | `PositionalCommandParameter` |  |  |
| `PowerShellStreamType.cs` | 59 | `PowerShellStreamType` |  |  |
| `ProcessCodeMethods.cs` | 72 | `ProcessCodeMethods` |  |  |
| `ProgressRecord.cs` | 562 | `ProgressRecord`, `ProgressRecordType` |  |  |
| `PropertyCmdletProviderInterfaces.cs` | 1832 | `PropertyCmdletProviderIntrinsics` |  |  |
| `ProviderInterfaces.cs` | 167 | `CmdletProviderManagementIntrinsics` |  |  |
| `ProviderNames.cs` | 132 | `SingleShellProviderNames`, `ProviderNames` |  |  |
| `ProxyCommand.cs` | 503 | `ProxyCommand` |  |  |
| `PseudoParameterBinder.cs` | 136 | `RuntimeDefinedParameterBinder` |  |  |
| `PseudoParameters.cs` | 246 | `RuntimeDefinedParameter`, `RuntimeDefinedParameterDictionary` |  |  |
| `QuestionMarkVariable.cs` | 43 | `QuestionMarkVariable` |  |  |
| `ReflectionParameterBinder.cs` | 322 | `ReflectionParameterBinder` |  |  |
| `ScopedItemSearcher.cs` | 487 | `ScopedItemSearcher<T>`, `FunctionScopeItemSearcher`, `VariableScopeItemSearcher`, `AliasScopeItemSearcher` (+1) |  |  |
| `ScriptCommand.cs` | 16 | `ScriptCommand` |  |  |
| `ScriptCommandProcessor.cs` | 662 | `DlrScriptCommandProcessor`, `ScriptCommandProcessorBase` |  |  |
| `ScriptInfo.cs` | 126 | `ScriptInfo` |  |  |
| `SecurityDescriptorCmdletProviderInterfaces.cs` | 247 | `SecurityDescriptorCmdletProviderIntrinsics` |  |  |
| `SecurityManagerBase.cs` | 183 | `AuthorizationManager`, `CommandOrigin` |  |  |
| `SerializationStrings.cs` | 312 | `SerializationStrings` |  |  |
| `SessionState.cs` | 556 | `SessionStateInternal` |  |  |
| `SessionStateAliasAPIs.cs` | 585 | `SessionStateInternal` |  |  |
| `SessionStateCmdletAPIs.cs` | 326 | `SessionStateInternal` |  |  |
| `SessionStateContainer.cs` | 4897 | `SessionStateInternal`, `ProcessMode` |  |  |
| `SessionStateContent.cs` | 1035 | `SessionStateInternal` |  |  |
| `SessionStateDriveAPIs.cs` | 1436 | `SessionStateInternal` |  |  |
| `SessionStateDynamicProperty.cs` | 2176 | `SessionStateInternal` |  |  |
| `SessionStateFunctionAPIs.cs` | 791 | `SessionStateInternal` |  |  |
| `SessionStateItem.cs` | 1377 | `SessionStateInternal` |  |  |
| `SessionStateLocationAPIs.cs` | 1114 | `SessionStateInternal`, `LocationChangedEventArgs` |  |  |
| `SessionStateNavigation.cs` | 1750 | `SessionStateInternal` |  |  |
| `SessionStateProperty.cs` | 1118 | `SessionStateInternal` |  |  |
| `SessionStateProviderAPIs.cs` | 1556 | `SessionStateInternal` |  |  |
| `SessionStatePublic.cs` | 374 | `SessionState`, `PSLanguageMode`, `SessionStateEntryVisibility`, `IHasSessionStateEntryVisibility` |  |  |
| `SessionStateScope.cs` | 2013 | `SessionStateScope` |  |  |
| `SessionStateScopeAPIs.cs` | 326 | `SessionStateInternal` |  |  |
| `SessionStateScopeEnumerator.cs` | 103 | `SessionStateScopeEnumerator` |  |  |
| `SessionStateSecurityDescriptorInterface.cs` | 578 | `SessionStateInternal` |  |  |
| `SessionStateStrings.cs` | 180 | `StringLiterals` |  |  |
| `SessionStateUtils.cs` | 324 | `SessionStateUtilities`, `SessionStateConstants`, `OpenMode` |  |  |
| `SessionStateVariableAPIs.cs` | 1865 | `SessionStateInternal` |  |  |
| `ShellVariable.cs` | 916 | `PSVariable`, `LocalVariable`, `NullVariable`, `ScopedItemOptions` |  |  |
| `SpecialVariables.cs` | 426 | `SpecialVariables`, `AutomaticVariable`, `PreferenceVariable` |  |  |
| `ThirdPartyAdapter.cs` | 365 | `ThirdPartyAdapter`, `PSPropertyAdapter` |  |  |
| `TypeMetadata.cs` | 1567 | `ParameterMetadata`, `InternalParameterMetadata`, `ParameterSetMetadata` |  |  |
| `TypeTable.cs` | 4779 | `TypeTable`, `TypesPs1xmlReader`, `TypeData`, `ConsolidatedString` (+11) |  |  |
| `TypeTable_GetEvent_Types_Ps1Xml.cs` | 201 | `TypeTable` |  |  |
| `TypeTable_TypesV3_Ps1Xml.cs` | 437 | `TypeTable` |  |  |
| `TypeTable_Types_Ps1Xml.cs` | 9139 | `TypeTable` |  |  |
| `UserFeedbackParameters.cs` | 213 | `PagingParameters`, `ShouldProcessParameters`, `TransactionParameters` |  |  |
| `Utils.cs` | 1866 | `Utils`, `InternalTestHooks`, `BoundedStack<T>`, `HistoryStack<T>` (+2) |  |  |
| `VariableAttributeCollection.cs` | 160 | `PSVariableAttributeCollection` |  |  |
| `VariableInterfaces.cs` | 448 | `PSVariableIntrinsics` |  |  |
| `VariablePath.cs` | 322 | `VariablePath`, `VariablePathFlags`, `FunctionLookupPath` |  |  |
| `cmdlet.cs` | 1855 | `Cmdlet`, `ShouldProcessReason` |  |  |
| `pipeline.cs` | 1668 | `PipelineProcessor` |  |  |
| `regex.cs` | 1384 | `WildcardPattern`, `WildcardPatternMatcher`, `WildcardPatternParser`, `WildcardPatternToRegexParser` (+3) |  |  |
| `scriptparameterbinder.cs` | 170 | `ScriptParameterBinder` |  |  |
| `scriptparameterbindercontroller.cs` | 231 | `ScriptParameterBinderController` |  |  |
| `serialization.cs` | 7679 | `InternalSerializer`, `InternalDeserializer`, `DeserializingTypeConverter`, `PSPrimitiveDictionary` (+19) |  |  |

## Subfolders

- [COM](COM/_folder.md) (7 files, 2039 LOC)
- [ComInterop](ComInterop/_folder.md) (55 files, 8041 LOC)
- [CommandCompletion](CommandCompletion/_folder.md) (8 files, 15464 LOC)
- [ExperimentalFeature](ExperimentalFeature/_folder.md) (3 files, 650 LOC)
- [Interop](Interop/_folder.md) (33 files, 1164 LOC)
- [Modules](Modules/_folder.md) (16 files, 20237 LOC)
- [Subsystem](Subsystem/_folder.md) (9 files, 2034 LOC)
- [WinRT](WinRT/_folder.md) (1 files, 41 LOC)
- [debugger](debugger/_folder.md) (2 files, 6566 LOC)
- [hostifaces](hostifaces/_folder.md) (32 files, 33963 LOC)
- [interpreter](interpreter/_folder.md) (38 files, 13810 LOC)
- [lang](lang/_folder.md) (6 files, 4489 LOC)
- [parser](parser/_folder.md) (18 files, 48688 LOC)
- [remoting](remoting/_folder.md) (96 files, 97104 LOC)
- [runtime](runtime/_folder.md) (10 files, 19879 LOC)

## Partial-class and conditional-compilation notes

Partial types spanning files: `PSCmdlet`, `SessionStateInternal`, `ToStringCodeMethods`, `TypeTable`

`#if` conditions on types here: `!UNIX`

## Related documents

_none linked yet_
