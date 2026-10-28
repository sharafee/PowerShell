# src/System.Management.Automation/engine/hostifaces

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| B:32 | System.Management.Automation | 32 | 33963 | 114 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `AsyncResult.cs` | 253 | `AsyncResult` |  |  |
| `ChoiceDescription.cs` | 136 | `ChoiceDescription` |  |  |
| `Command.cs` | 902 | `Command`, `CommandCollection`, `PipelineResultTypes` |  |  |
| `Connection.cs` | 1895 | `Runspace`, `SessionStateProxy`, `InvalidRunspaceStateException`, `RunspaceStateInfo` (+6) |  |  |
| `ConnectionBase.cs` | 1611 | `RunspaceBase` |  |  |
| `ConnectionFactory.cs` | 628 | `RunspaceFactory` |  |  |
| `DefaultHost.cs` | 135 | `DefaultHost` |  |  |
| `FieldDescription.cs` | 416 | `FieldDescription` |  |  |
| `History.cs` | 1902 | `History`, `ClearHistoryCommand`, `InvokeHistoryCommand`, `AddHistoryCommand` (+2) |  |  |
| `HostUtilities.cs` | 605 | `HostUtilities` |  |  |
| `InformationalRecord.cs` | 267 | `InformationalRecord`, `WarningRecord`, `DebugRecord`, `VerboseRecord` |  |  |
| `InternalHost.cs` | 581 | `InternalHost` |  |  |
| `InternalHostRawUserInterface.cs` | 615 | `InternalHostRawUserInterface` |  |  |
| `InternalHostUserInterface.cs` | 1033 | `InternalHostUserInterface` |  |  |
| `ListModifier.cs` | 300 | `PSListModifier`, `PSListModifier<T>` |  |  |
| `LocalConnection.cs` | 1569 | `LocalRunspace`, `CloseOrDisconnectRunspaceOperationHelper`, `RunspaceOpenModuleLoadException`, `StopJobOperationHelper` |  |  |
| `LocalPipeline.cs` | 1400 | `LocalPipeline`, `PipelineStopper`, `PipelineThread` |  |  |
| `MshHost.cs` | 328 | `PSHost`, `IHostSupportsInteractiveSession` |  |  |
| `MshHostRawUserInterface.cs` | 1915 | `PSHostRawUserInterface`, `Rectangle`, `KeyInfo`, `BufferCell` (+5) |  |  |
| `MshHostUserInterface.cs` | 1480 | `PSHostUserInterface`, `TranscriptionOption`, `HostUIHelperMethods`, `IHostUISupportsMultipleChoiceSelection` (+1) |  |  |
| `PSCommand.cs` | 517 | `PSCommand` |  |  |
| `PSDataCollection.cs` | 2121 | `PSDataCollection<T>`, `PSDataCollectionEnumerator<T>`, `PSInformationalBuffers`, `DataAddedEventArgs` (+2) |  |  |
| `PSTask.cs` | 1593 | `PSTaskPool`, `PSTaskChildDebugger`, `PSTaskJob`, `PSTaskBase` (+4) |  |  |
| `Parameter.cs` | 288 | `CommandParameter`, `CommandParameterCollection` |  |  |
| `Pipeline.cs` | 740 | `Pipeline`, `InvalidPipelineStateException`, `PipelineStateInfo`, `PipelineState` (+1) |  |  |
| `PowerShell.cs` | 6209 | `PowerShell`, `PSDataStreams`, `PSInvocationSettings`, `InvalidPowerShellStateException` (+8) |  |  |
| `PowerShellProcessInstance.cs` | 293 | `PowerShellProcessInstance` |  |  |
| `RunspaceInit.cs` | 28 | `LocalRunspace` |  |  |
| `RunspacePool.cs` | 1388 | `RunspacePool`, `InvalidRunspacePoolStateException`, `GetRunspaceAsyncResult`, `RunspacePoolAsyncResult` (+5) |  |  |
| `RunspacePoolInternal.cs` | 1669 | `RunspacePoolInternal` |  |  |
| `internalHostuserInterfacesecurity.cs` | 74 | `InternalHostUserInterface` |  |  |
| `pipelinebase.cs` | 1072 | `PipelineBase` |  |  |

## Partial-class and conditional-compilation notes

Partial types spanning files: `InternalHostUserInterface`, `LocalRunspace`

No conditionally-compiled types (APPROX).

## Related documents

_none linked yet_
