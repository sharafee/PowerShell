# src/Microsoft.PowerShell.Commands.Utility/commands/utility

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| C:90 | Microsoft.PowerShell.Commands.Utility | 90 | 32612 | 200 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `AddMember.cs` | 603 | `AddMemberCommand` |  |  |
| `AddType.cs` | 1371 | `AddTypeCommand`, `OutputAssemblyType`, `Language` |  |  |
| `Compare-Object.cs` | 489 | `CompareObjectCommand` |  |  |
| `ConsoleColorCmdlet.cs` | 108 | `ConsoleColorCmdlet` |  |  |
| `ConvertFrom-SddlString.cs` | 264 | `ConvertFromSddlStringCommand`, `SecurityDescriptorInfo` |  |  |
| `ConvertFrom-StringData.cs` | 95 | `ConvertFromStringDataCommand` |  |  |
| `ConvertFromMarkdownCommand.cs` | 233 | `ConvertFromMarkdownCommand` |  |  |
| `ConvertTo-Html.cs` | 761 | `ConvertToHtmlCommand` |  |  |
| `Csv.cs` | 111 | `CSVHelper` |  |  |
| `CsvCommands.cs` | 1815 | `ImportCsvHelper`, `ExportCsvCommand`, `ExportCsvHelper`, `ImportCsvCommand` (+4) |  |  |
| `CustomSerialization.cs` | 1133 | `CustomInternalSerializer`, `CustomSerialization` |  |  |
| `CustomSerializationStrings.cs` | 58 | `CustomSerializationStrings` |  |  |
| `DebugRunspaceCommand.cs` | 559 | `DebugRunspaceCommand` |  |  |
| `Disable-PSBreakpoint.cs` | 43 | `DisablePSBreakpointCommand` |  |  |
| `Enable-PSBreakpoint.cs` | 43 | `EnablePSBreakpointCommand` |  |  |
| `EnableDisableRunspaceDebugCommand.cs` | 532 | `CommonRunspaceCommandBase`, `EnableRunspaceDebugCommand`, `PSRunspaceDebug`, `DisableRunspaceDebugCommand` (+2) |  |  |
| `ExportAliasCommand.cs` | 423 | `ExportAliasCommand`, `ExportAliasFormat` |  |  |
| `Get-Error.cs` | 112 | `GetErrorCommand` |  |  |
| `Get-PSBreakpoint.cs` | 245 | `GetPSBreakpointCommand`, `BreakpointType` |  |  |
| `Get-PSCallStack.cs` | 26 | `GetPSCallStackCommand` |  |  |
| `GetAliasCommand.cs` | 202 | `GetAliasCommand` |  |  |
| `GetCultureCommand.cs` | 124 | `GetCultureCommand`, `ValidateCultureNamesGenerator` |  |  |
| `GetDateCommand.cs` | 600 | `GetDateCommand`, `DisplayHintType` |  |  |
| `GetEventCommand.cs` | 138 | `GetEventCommand` |  |  |
| `GetEventSubscriberCommand.cs` | 132 | `GetEventSubscriberCommand` |  |  |
| `GetHash.cs` | 303 | `GetFileHashCommand`, `HashCmdletBase`, `FileHashInfo` |  |  |
| `GetHostCmdlet.cs` | 24 | `GetHostCommand` |  |  |
| `GetMember.cs` | 282 | `GetMemberCommand`, `MemberDefinition` |  |  |
| `GetRandomCommand.cs` | 36 | `GetRandomCommand` |  |  |
| `GetRandomCommandBase.cs` | 719 | `GetRandomCommandBase`, `PolymorphicRandomNumberGenerator` |  |  |
| `GetRunspaceCommand.cs` | 192 | `GetRunspaceCommand`, `GetRunspaceUtils` |  |  |
| `GetSecureRandomCommand.cs` | 18 | `GetSecureRandomCommand` |  |  |
| `GetUICultureCommand.cs` | 23 | `GetUICultureCommand` |  |  |
| `GetUnique.cs` | 120 | `GetUniqueCommand` |  |  |
| `GetUptime.cs` | 69 | `GetUptimeCommand` |  |  |
| `GetVerbCommand.cs` | 47 | `GetVerbCommand` |  |  |
| `Group-Object.cs` | 553 | `GroupObjectCommand`, `PSTuple`, `GroupInfo`, `GroupInfoNoElement` |  |  |
| `ImplicitRemotingCommands.cs` | 3146 | `ImplicitRemotingCommandBase`, `ImplicitRemotingCodeGenerator`, `ImportPSSessionCommand`, `ExportPSSessionCommand` |  |  |
| `Import-LocalizedData.cs` | 407 | `ImportLocalizedData` |  |  |
| `ImportAliasCommand.cs` | 484 | `ImportAliasCommand` |  |  |
| `ImportPowerShellDataFile.cs` | 104 | `ImportPowerShellDataFileCommand` |  |  |
| `InvokeExpressionCommand.cs` | 68 | `InvokeExpressionCommand` |  |  |
| `Join-String.cs` | 274 | `JoinStringCommand`, `SeparatorArgumentCompleter`, `FormatStringArgumentCompleter` |  |  |
| `JsonSchemaReferenceResolutionException.cs` | 27 | `JsonSchemaReferenceResolutionException` |  |  |
| `MarkdownOptionCommands.cs` | 314 | `SetMarkdownOptionCommand`, `PSMarkdownOptionInfoCache`, `GetMarkdownOptionCommand` |  |  |
| `MatchString.cs` | 2105 | `SelectStringCommand`, `MatchInfo`, `MatchInfoContext`, `ValidateMatchStringCultureNamesGenerator` |  |  |
| `Measure-Object.cs` | 995 | `MeasureObjectCommand`, `GenericObjectMeasureInfo`, `GenericMeasureInfo`, `TextMeasureInfo` (+1) |  |  |
| `New-Object.cs` | 551 | `NewObjectCommand`, `NewObjectNativeMethods` |  |  |
| `NewAliasCommand.cs` | 131 | `NewAliasCommand` |  |  |
| `NewEventCommand.cs` | 133 | `NewEventCommand` |  |  |
| `NewGuidCommand.cs` | 58 | `NewGuidCommand` |  |  |
| `NewTemporaryFileCommand.cs` | 49 | `NewTemporaryFileCommand` |  |  |
| `NewTimeSpanCommand.cs` | 140 | `NewTimeSpanCommand` |  |  |
| `ObjectCommandComparer.cs` | 235 | `ObjectCommandPropertyValue`, `ObjectCommandComparer` |  |  |
| `OrderObjectBase.cs` | 730 | `OrderByProperty`, `OrderByPropertyEntryEvaluationHelper`, `OrderByPropertyComparer`, `ObjectCmdletBase` (+7) |  |  |
| `PSBreakpointAccessorCommandBase.cs` | 19 | `PSBreakpointAccessorCommandBase` |  |  |
| `PSBreakpointCommandBase.cs` | 60 | `PSBreakpointCommandBase` |  |  |
| `PSBreakpointUpdaterCommandBase.cs` | 168 | `PSBreakpointUpdaterCommandBase` |  |  |
| `ReadConsoleCmdlet.cs` | 187 | `ReadHostCommand` |  |  |
| `RegisterObjectEventCommand.cs` | 73 | `RegisterObjectEventCommand` |  |  |
| `RegisterPSEventCommand.cs` | 65 | `RegisterEngineEventCommand` |  |  |
| `Remove-PSBreakpoint.cs` | 27 | `RemovePSBreakpointCommand` |  |  |
| `RemoveAliasCommand.cs` | 73 | `RemoveAliasCommand` |  |  |
| `RemoveEventCommand.cs` | 140 | `RemoveEventCommand` |  |  |
| `RunspaceAttribute.cs` | 97 | `RunspaceAttribute` |  |  |
| `Select-Object.cs` | 878 | `SelectObjectCommand`, `PSPropertyExpressionFilter`, `SelectObjectException`, `SelectObjectExpressionParameterDefinition` |  |  |
| `Send-MailMessage.cs` | 403 | `SendMailMessage` |  |  |
| `Set-PSBreakpoint.cs` | 238 | `SetPSBreakpointCommand` |  |  |
| `SetAliasCommand.cs` | 75 | `SetAliasCommand` |  |  |
| `SetDateCommand.cs` | 153 | `SetDateCommand` |  |  |
| `ShowMarkdownCommand.cs` | 230 | `ShowMarkdownCommand` |  |  |
| `Sort-Object.cs` | 274 | `SortObjectCommand` |  |  |
| `StartSleepCommand.cs` | 156 | `StartSleepCommand` |  |  |
| `Tee-Object.cs` | 170 | `TeeObjectCommand` |  |  |
| `TestJsonCommand.cs` | 340 | `TestJsonCommand` |  |  |
| `TimeExpressionCommand.cs` | 75 | `MeasureCommandCommand` |  |  |
| `UnblockFile.cs` | 230 | `UnblockFileCommand` |  |  |
| `UnregisterEventCommand.cs` | 127 | `UnregisterEventCommand` |  |  |
| `Update-Data.cs` | 100 | `UpdateData` |  |  |
| `Update-List.cs` | 189 | `UpdateListCommand` |  |  |
| `Update-TypeData.cs` | 1391 | `UpdateTypeDataCommand`, `RemoveTypeDataCommand`, `UpdateFormatDataCommand`, `GetTypeDataCommand` (+1) |  |  |
| `UtilityCommon.cs` | 376 | `ByteCollection`, `TextEncodingType`, `UtilityResources` |  |  |
| `Var.cs` | 1413 | `SetVariableCommand`, `VariableCommandBase`, `ClearVariableCommand`, `NewVariableCommand` (+2) |  |  |
| `WaitEventCommand.cs` | 163 | `WaitEventCommand` |  |  |
| `Write-Object.cs` | 44 | `WriteOutputCommand` |  |  |
| `Write.cs` | 463 | `WriteOrThrowErrorCommand`, `WriteErrorException`, `WriteInformationCommand`, `WriteDebugCommand` (+3) |  |  |
| `WriteAliasCommandBase.cs` | 88 | `WriteAliasCommandBase` |  |  |
| `WriteConsoleCmdlet.cs` | 128 | `WriteHostCommand` |  |  |
| `WriteProgressCmdlet.cs` | 134 | `WriteProgressCommand` |  |  |
| `XmlCommands.cs` | 1308 | `SelectXmlCommand`, `ExportClixmlCommand`, `ConvertToXmlCommand`, `ImportXmlHelper` (+4) |  |  |

## Subfolders

- [FormatAndOutput](FormatAndOutput/_folder.md) (19 files, 3497 LOC)
- [ShowCommand](ShowCommand/_folder.md) (7 files, 1343 LOC)
- [WebCmdlet](WebCmdlet/_folder.md) (21 files, 5926 LOC)
- [trace](trace/_folder.md) (6 files, 1626 LOC)

## Partial-class and conditional-compilation notes

No partial types spanning files (APPROX).

`#if` conditions on types here: `!UNIX`

## Related documents

_none linked yet_
