# src/Microsoft.PowerShell.ConsoleHost/host/msh

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| B:20 | Microsoft.PowerShell.ConsoleHost | 20 | 17148 | 75 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `CommandLineParameterParser.cs` | 1715 | `CommandLineParameterParser`, `NullHostUserInterface` |  |  |
| `ConsoleControl.cs` | 3189 | `ConsoleControl` |  |  |
| `ConsoleHost.cs` | 3159 | `ConsoleHost`, `RunspaceCreationEventArgs` |  |  |
| `ConsoleHostRawUserInterface.cs` | 1693 | `ConsoleHostRawUserInterface`, `ConsoleHostRawUserInterface` |  |  |
| `ConsoleHostTranscript.cs` | 130 | `ConsoleHost` |  |  |
| `ConsoleHostUserInterface.cs` | 2268 | `ConsoleHostUserInterface` |  |  |
| `ConsoleHostUserInterfaceProgress.cs` | 214 | `ConsoleHostUserInterface` |  |  |
| `ConsoleHostUserInterfacePrompt.cs` | 560 | `ConsoleHostUserInterface` |  |  |
| `ConsoleHostUserInterfacePromptForChoice.cs` | 467 | `ConsoleHostUserInterface` |  |  |
| `ConsoleHostUserInterfaceSecurity.cs` | 126 | `ConsoleHostUserInterface` |  |  |
| `ConsoleShell.cs` | 81 | `ConsoleShell` |  |  |
| `ConsoleTextWriter.cs` | 92 | `ConsoleTextWriter` |  |  |
| `Executor.cs` | 709 | `Executor` |  |  |
| `ManagedEntrance.cs` | 124 | `UnmanagedPSEntry` |  |  |
| `PendingProgress.cs` | 994 | `PendingProgress` |  |  |
| `ProgressNode.cs` | 611 | `ProgressNode` |  |  |
| `ProgressPane.cs` | 349 | `ProgressPane` |  |  |
| `Serialization.cs` | 272 | `WrappedDeserializer`, `WrappedSerializer`, `Serialization` |  |  |
| `StartTranscriptCmdlet.cs` | 348 | `StartTranscriptCommand` |  |  |
| `StopTranscriptCmdlet.cs` | 47 | `StopTranscriptCommand` |  |  |

## Partial-class and conditional-compilation notes

Partial types spanning files: `ConsoleHostUserInterface`, `ConsoleHost`

`#if` conditions on types here: `!(!UNIX)`, `!UNIX`, `DEBUG || ASSERTIONS_TRACE`

## Related documents

_none linked yet_
