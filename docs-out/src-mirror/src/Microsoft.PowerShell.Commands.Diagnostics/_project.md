# Microsoft.PowerShell.Commands.Diagnostics

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `src/Microsoft.PowerShell.Commands.Diagnostics/Microsoft.PowerShell.Commands.Diagnostics.csproj` | Library (default) | net10.0 | cross-platform (conditional items) | `Microsoft.PowerShell.Commands.Diagnostics` | DefineConstants=$(DefineConstants);CORECLR; DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | C:8 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `Microsoft.PowerShell.Commands.Diagnostics` (8 C# files, 4727 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|
| [resources](resources/_folder.md) | 14 | 4383 |

## Public API surface (APPROX)

33 types, 6 public top-level types.

## References

Project refs: `System.Management.Automation`

Packages: System.Configuration.ConfigurationManager 10.0.14, System.Diagnostics.EventLog 10.0.14, System.Security.Cryptography.ProtectedData 10.0.14, System.Diagnostics.PerformanceCounter 10.0.14

Referenced by: `PowerShell.Windows.x64`, `powershell-perf`, `powershell-win-core`, `xUnit.tests`

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `src/Microsoft.PowerShell.Commands.Diagnostics/GetEventCommand.cs` | 2054 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Diagnostics/PdhHelper.cs` | 1353 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Diagnostics/GetCounterCommand.cs` | 632 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Diagnostics/NewWinEventCommand.cs` | 336 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Diagnostics/CommonUtils.cs` | 100 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Diagnostics/CounterSet.cs` | 96 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Diagnostics/CounterSample.cs` | 94 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Diagnostics/PdhSafeHandle.cs` | 62 | _GENERATED_ |

## Related documents

_none linked yet_
