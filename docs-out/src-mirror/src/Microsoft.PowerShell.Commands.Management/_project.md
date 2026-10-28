# Microsoft.PowerShell.Commands.Management

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `src/Microsoft.PowerShell.Commands.Management/Microsoft.PowerShell.Commands.Management.csproj` | Library (default) | net10.0 | cross-platform (conditional items) | `Microsoft.PowerShell.Commands.Management` | DefineConstants=$(DefineConstants);CORECLR; DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | C:61 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `Microsoft.PowerShell.Commands.Management` (61 C# files, 33198 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|
| [cimSupport](cimSupport/_folder.md) | 23 | 6348 |
| [commands](commands/_folder.md) | 38 | 26850 |
| [resources](resources/_folder.md) | 182 | 32505 |

## Public API surface (APPROX)

226 types, 127 public top-level types.

## References

Project refs: `Microsoft.PowerShell.Security`

Packages: System.Diagnostics.EventLog 10.0.14, System.ServiceProcess.ServiceController 10.0.14

Referenced by: `Microsoft.PowerShell.SDK`

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `src/Microsoft.PowerShell.Commands.Management/commands/management/GetComputerInfoCommand.cs` | 5158 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Management/commands/management/Navigation.cs` | 4224 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Management/commands/management/Process.cs` | 3018 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Management/commands/management/Service.cs` | 2912 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Management/commands/management/Computer.cs` | 2266 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Management/commands/management/TestConnectionCommand.cs` | 1254 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Management/cimSupport/cmdletization/cim/cimChildJobBase.cs` | 1081 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Management/commands/management/TimeZoneCommands.cs` | 795 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Management/commands/management/ContentCommandBase.cs` | 707 | _GENERATED_ |
| `src/Microsoft.PowerShell.Commands.Management/cimSupport/cmdletization/cim/clientSideQuery.cs` | 704 | _GENERATED_ |

## Related documents

_none linked yet_
