# src/System.Management.Automation/engine/remoting/common

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| B:17 | System.Management.Automation | 17 | 10689 | 70 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `AsyncObject.cs` | 58 | `AsyncObject<T>` |  |  |
| `DispatchTable.cs` | 191 | `DispatchTable<T>`, `ServerDispatchTable` |  |  |
| `Indexer.cs` | 112 | `Indexer` |  |  |
| `ObjectRef.cs` | 91 | `ObjectRef<T>` |  |  |
| `PSETWTracer.cs` | 281 | `PSEventId`, `PSTask`, `PSOpcode`, `PSKeyword` (+5) |  |  |
| `PSSessionConfigurationTypeOption.cs` | 103 | `PSTransportOption`, `PSSessionTypeOption` |  |  |
| `RemoteSessionHyperVSocket.cs` | 1157 | `RemoteSessionHyperVSocketClient`, `RemoteSessionHyperVSocketServer`, `HyperVSocketEndPoint` |  |  |
| `RemoteSessionNamedPipe.cs` | 1318 | `RemoteSessionNamedPipeServer`, `NamedPipeUtils`, `RemoteSessionNamedPipeClient`, `NamedPipeClientBase` (+3) |  |  |
| `RunspaceConnectionInfo.cs` | 3803 | `WSManConnectionInfo`, `SSHConnectionInfo`, `ContainerProcess`, `RunspaceConnectionInfo` (+7) |  |  |
| `RunspaceInitInfo.cs` | 34 | `RunspacePoolInitInfo` |  |  |
| `RunspacePoolStateInfo.cs` | 41 | `RunspacePoolStateInfo` |  |  |
| `fragmentor.cs` | 1126 | `SerializedDataStream`, `FragmentedRemoteObject`, `Fragmentor` |  |  |
| `misc.cs` | 418 | `RemoteSessionState`, `RemoteSessionStateInfo`, `RemoteSessionEvent`, `RemoteSessionNegotiationEventArgs` (+6) |  |  |
| `psstreamobject.cs` | 508 | `PSStreamObject`, `PSStreamObjectType`, `CmdletMethodInvoker<T>` |  |  |
| `remotesession.cs` | 34 | `RemoteSession` |  |  |
| `remotingexceptions.cs` | 648 | `PSRemotingErrorId`, `PSRemotingTransportException`, `PSRemotingTransportRedirectException`, `PSRemotingDataStructureException` (+2) |  |  |
| `throttlemanager.cs` | 766 | `ThrottleManager`, `IThrottleOperation`, `Operation`, `OperationStateEventArgs` (+1) |  |  |

## Subfolders

- [WireDataFormat](WireDataFormat/_folder.md) (6 files, 4551 LOC)

## Partial-class and conditional-compilation notes

No partial types spanning files (APPROX).

`#if` conditions on types here: `!(UNIX)`, `!CORECLR`, `UNIX`

## Related documents

_none linked yet_
