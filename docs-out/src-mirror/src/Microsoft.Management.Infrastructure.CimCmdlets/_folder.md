# src/Microsoft.Management.Infrastructure.CimCmdlets

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| C:35 | Microsoft.Management.Infrastructure.CimCmdlets | 35 | 15485 | 84 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `AssemblyInfo.cs` | 6 | - |  |  |
| `CimAsyncOperation.cs` | 585 | `CimAsyncOperation` |  |  |
| `CimBaseAction.cs` | 185 | `CimSyncAction`, `CimBaseAction` |  |  |
| `CimCommandBase.cs` | 910 | `CimBaseCommand`, `ParameterBinder`, `ParameterSetEntry`, `ParameterDefinitionEntry` |  |  |
| `CimGetAssociatedInstance.cs` | 137 | `CimGetAssociatedInstance` |  |  |
| `CimGetCimClass.cs` | 208 | `CimGetCimClass`, `CimGetCimClassContext` |  |  |
| `CimGetInstance.cs` | 537 | `CimGetInstance`, `FormatPartialCimInstance` |  |  |
| `CimIndicationWatcher.cs` | 382 | `CimIndicationWatcher`, `CimIndicationEventInstanceEventArgs`, `CimIndicationEventExceptionEventArgs`, `CimIndicationEventArgs` |  |  |
| `CimInvokeCimMethod.cs` | 453 | `CimInvokeCimMethod` |  |  |
| `CimNewCimInstance.cs` | 363 | `CimNewCimInstance`, `CimNewCimInstanceContext` |  |  |
| `CimPromptUser.cs` | 133 | `CimPromptUser` |  |  |
| `CimRegisterCimIndication.cs` | 348 | `CimRegisterCimIndication`, `CimSubscriptionResultEventArgs`, `CimSubscriptionExceptionEventArgs`, `CimSubscriptionEventArgs` |  |  |
| `CimRemoveCimInstance.cs` | 145 | `CimRemoveCimInstance`, `CimRemoveCimInstanceContext` |  |  |
| `CimResultObserver.cs` | 496 | `CimResultObserver<T>`, `CimMethodResultObserver`, `AsyncResultEventArgsBase`, `AsyncResultErrorEventArgs` (+6) |  |  |
| `CimSessionOperations.cs` | 1247 | `CimSessionState`, `CimNewSession`, `CimSessionBase`, `CimSessionWrapper` (+3) |  |  |
| `CimSessionProxy.cs` | 2313 | `CimSessionProxy`, `CimSessionProxyGetCimClass`, `CimSessionProxySetCimInstance`, `CimSessionProxyNewCimInstance` (+6) |  |  |
| `CimSetCimInstance.cs` | 291 | `CimSetCimInstance`, `CimSetCimInstanceContext` |  |  |
| `CimWriteError.cs` | 394 | `ErrorToErrorRecord`, `CimWriteError` |  |  |
| `CimWriteMessage.cs` | 71 | `CimWriteMessage` |  |  |
| `CimWriteProgress.cs` | 124 | `CimWriteProgress` |  |  |
| `CimWriteResultObject.cs` | 45 | `CimWriteResultObject` |  |  |
| `CmdletOperation.cs` | 403 | `CmdletOperationBase`, `CmdletOperationSetCimInstance`, `CmdletOperationInvokeCimMethod`, `CmdletOperationRemoveCimInstance` (+1) |  |  |
| `GetCimAssociatedInstanceCommand.cs` | 325 | `GetCimAssociatedInstanceCommand` |  |  |
| `GetCimClassCommand.cs` | 283 | `GetCimClassCommand` |  |  |
| `GetCimInstanceCommand.cs` | 684 | `GetCimInstanceCommand` |  |  |
| `GetCimSessionCommand.cs` | 224 | `GetCimSessionCommand` |  |  |
| `InvokeCimMethodCommand.cs` | 582 | `InvokeCimMethodCommand` |  |  |
| `NewCimInstanceCommand.cs` | 521 | `NewCimInstanceCommand` |  |  |
| `NewCimSessionCommand.cs` | 340 | `NewCimSessionCommand` |  |  |
| `NewCimSessionOptionCommand.cs` | 861 | `NewCimSessionOptionCommand`, `ProtocolType` |  |  |
| `RegisterCimIndicationCommand.cs` | 365 | `RegisterCimIndicationCommand` |  |  |
| `RemoveCimInstanceCommand.cs` | 386 | `RemoveCimInstanceCommand` |  |  |
| `RemoveCimSessionCommand.cs` | 259 | `RemoveCimSessionCommand` |  |  |
| `SetCimInstanceCommand.cs` | 444 | `SetCimInstanceCommand` |  |  |
| `Utils.cs` | 435 | `DebugHelper`, `ConstValue`, `ValidationHelper` |  |  |

## Subfolders

- [resources](resources/_folder.md) (14 files, 3192 LOC)

## Partial-class and conditional-compilation notes

No partial types spanning files (APPROX).

No conditionally-compiled types (APPROX).

## Related documents

_none linked yet_
