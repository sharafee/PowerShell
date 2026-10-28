# Microsoft.WSMan.Management

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `src/Microsoft.WSMan.Management/Microsoft.WSMan.Management.csproj` | Library (default) | net10.0 | cross-platform (conditional items) | `Microsoft.WSMan.Management` | DefineConstants=$(DefineConstants);CORECLR; DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | C:11 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `Microsoft.WSMan.Management` (11 C# files, 13139 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|
| [resources](resources/_folder.md) | 14 | 4621 |

## Public API surface (APPROX)

50 types, 42 public top-level types.

## References

Project refs: `System.Management.Automation`, `Microsoft.WSMan.Runtime`

Packages: System.Diagnostics.EventLog 10.0.14, System.ServiceProcess.ServiceController 10.0.14

Referenced by: `PowerShell.Windows.x64`, `powershell-perf`, `powershell-win-core`, `xUnit.tests`

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `src/Microsoft.WSMan.Management/ConfigProvider.cs` | 6577 | _GENERATED_ |
| `src/Microsoft.WSMan.Management/WSManInstance.cs` | 1638 | _GENERATED_ |
| `src/Microsoft.WSMan.Management/Interop.cs` | 1138 | _GENERATED_ |
| `src/Microsoft.WSMan.Management/WsManHelper.cs` | 1121 | _GENERATED_ |
| `src/Microsoft.WSMan.Management/CredSSP.cs` | 927 | _GENERATED_ |
| `src/Microsoft.WSMan.Management/WSManConnections.cs` | 387 | _GENERATED_ |
| `src/Microsoft.WSMan.Management/InvokeWSManAction.cs` | 340 | _GENERATED_ |
| `src/Microsoft.WSMan.Management/NewWSManSession.cs` | 309 | _GENERATED_ |
| `src/Microsoft.WSMan.Management/Set-QuickConfig.cs` | 294 | _GENERATED_ |
| `src/Microsoft.WSMan.Management/PingWSMan.cs` | 208 | _GENERATED_ |

## Related documents

_none linked yet_
