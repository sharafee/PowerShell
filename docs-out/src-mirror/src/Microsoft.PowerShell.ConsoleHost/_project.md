# Microsoft.PowerShell.ConsoleHost

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `src/Microsoft.PowerShell.ConsoleHost/Microsoft.PowerShell.ConsoleHost.csproj` | Library (default) | net10.0 | cross-platform (conditional items) | `Microsoft.PowerShell.ConsoleHost` | DefineConstants=$(DefineConstants);CORECLR; DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | B:26 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `Microsoft.PowerShell.ConsoleHost` (26 C# files, 17831 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|
| [WindowsTaskbarJumpList](WindowsTaskbarJumpList/_folder.md) | 5 | 676 |
| [host](host/_folder.md) | 20 | 17148 |
| [resources](resources/_folder.md) | 126 | 26526 |

## Public API surface (APPROX)

90 types, 4 public top-level types.

## References

Project refs: `System.Management.Automation`

Packages: none

Referenced by: `Microsoft.PowerShell.SDK`

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `src/Microsoft.PowerShell.ConsoleHost/host/msh/ConsoleControl.cs` | 3189 | _GENERATED_ |
| `src/Microsoft.PowerShell.ConsoleHost/host/msh/ConsoleHost.cs` | 3159 | _GENERATED_ |
| `src/Microsoft.PowerShell.ConsoleHost/host/msh/ConsoleHostUserInterface.cs` | 2268 | _GENERATED_ |
| `src/Microsoft.PowerShell.ConsoleHost/host/msh/CommandLineParameterParser.cs` | 1715 | _GENERATED_ |
| `src/Microsoft.PowerShell.ConsoleHost/host/msh/ConsoleHostRawUserInterface.cs` | 1693 | _GENERATED_ |
| `src/Microsoft.PowerShell.ConsoleHost/host/msh/PendingProgress.cs` | 994 | _GENERATED_ |
| `src/Microsoft.PowerShell.ConsoleHost/host/msh/Executor.cs` | 709 | _GENERATED_ |
| `src/Microsoft.PowerShell.ConsoleHost/host/msh/ProgressNode.cs` | 611 | _GENERATED_ |
| `src/Microsoft.PowerShell.ConsoleHost/host/msh/ConsoleHostUserInterfacePrompt.cs` | 560 | _GENERATED_ |
| `src/Microsoft.PowerShell.ConsoleHost/host/msh/ConsoleHostUserInterfacePromptForChoice.cs` | 467 | _GENERATED_ |

## Related documents

_none linked yet_
