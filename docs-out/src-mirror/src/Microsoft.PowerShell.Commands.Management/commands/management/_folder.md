# src/Microsoft.PowerShell.Commands.Management/commands/management

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| C:38 | Microsoft.PowerShell.Commands.Management | 38 | 26850 | 183 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `AddContentCommand.cs` | 84 | `AddContentCommand` |  |  |
| `CIMHelper.cs` | 328 | `CIMHelper`, `CIMExtensions` |  |  |
| `ClearContentCommand.cs` | 101 | `ClearContentCommand` |  |  |
| `ClearPropertyCommand.cs` | 172 | `ClearItemPropertyCommand` |  |  |
| `ClearRecycleBinCommand.cs` | 254 | `ClearRecycleBinCommand`, `NativeMethod` |  |  |
| `Clipboard.cs` | 390 | `Clipboard` |  |  |
| `CombinePathCommand.cs` | 229 | `JoinPathCommand` |  |  |
| `Computer.cs` | 2266 | `RestartComputerCommand`, `ComputerWMIHelper`, `RenameComputerCommand`, `StopComputerCommand` (+4) |  |  |
| `ComputerUnix.cs` | 207 | `CommandLineCmdletBase`, `StopComputerCommand`, `RestartComputerCommand` |  |  |
| `ContentCommandBase.cs` | 707 | `ContentCommandBase` |  |  |
| `ConvertPathCommand.cs` | 138 | `ConvertPathCommand` |  |  |
| `CopyPropertyCommand.cs` | 155 | `CopyItemPropertyCommand` |  |  |
| `GetChildrenCommand.cs` | 366 | `GetChildItemCommand` |  |  |
| `GetClipboardCommand.cs` | 116 | `GetClipboardCommand`, `DelimiterCompleter` |  |  |
| `GetComputerInfoCommand.cs` | 5158 | `ComputerInfo`, `GetComputerInfoCommand`, `OSType`, `OperatingSystemSKU` (+52) |  |  |
| `GetContentCommand.cs` | 378 | `GetContentCommand` |  |  |
| `GetPropertyCommand.cs` | 345 | `GetItemPropertyValueCommand`, `GetItemPropertyCommand` |  |  |
| `Hotfix.cs` | 236 | `GetHotFixCommand` |  |  |
| `JobProcessCollection.cs` | 125 | `JobProcessCollection` |  |  |
| `MovePropertyCommand.cs` | 173 | `MoveItemPropertyCommand` |  |  |
| `Navigation.cs` | 4224 | `RemoveItemCommand`, `MoveItemCommand`, `RenameItemCommand`, `GetLocationCommand` (+16) |  |  |
| `NewPropertyCommand.cs` | 295 | `NewItemPropertyCommand`, `PropertyTypeArgumentCompleter` |  |  |
| `ParsePathCommand.cs` | 478 | `SplitPathCommand` |  |  |
| `PassThroughContentCommandBase.cs` | 76 | `PassThroughContentCommandBase` |  |  |
| `PassThroughPropertyCommandBase.cs` | 102 | `PassThroughItemPropertyCommandBase` |  |  |
| `Process.cs` | 3018 | `StartProcessCommand`, `ProcessBaseCommand`, `StopProcessCommand`, `GetProcessCommand` (+6) |  |  |
| `PropertyCommandBase.cs` | 77 | `ItemPropertyCommandBase` |  |  |
| `RemovePropertyCommand.cs` | 180 | `RemoveItemPropertyCommand` |  |  |
| `RenamePropertyCommand.cs` | 147 | `RenameItemPropertyCommand` |  |  |
| `ResolvePathCommand.cs` | 290 | `ResolvePathCommand` |  |  |
| `Service.cs` | 2912 | `SetServiceCommand`, `ServiceOperationBaseCommand`, `MultipleServiceCommandBase`, `NewServiceCommand` (+11) |  |  |
| `SetClipboardCommand.cs` | 163 | `SetClipboardCommand` |  |  |
| `SetContentCommand.cs` | 90 | `SetContentCommand` |  |  |
| `SetPropertyCommand.cs` | 228 | `SetItemPropertyCommand` |  |  |
| `TestConnectionCommand.cs` | 1254 | `TestConnectionCommand` |  |  |
| `TestPathCommand.cs` | 247 | `TestPathCommand`, `TestPathType` |  |  |
| `TimeZoneCommands.cs` | 795 | `SetTimeZoneCommand`, `GetTimeZoneCommand`, `TimeZoneHelper` |  |  |
| `WriteContentCommandBase.cs` | 346 | `WriteContentCommandBase` |  |  |

## Partial-class and conditional-compilation notes

Partial types spanning files: `RestartComputerCommand`, `StopComputerCommand`

`#if` conditions on types here: `!UNIX`, `UNIX`

## Related documents

_none linked yet_
