# Microsoft.PowerShell.GraphicalHost

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `src/Microsoft.Management.UI.Internal/Microsoft.PowerShell.GraphicalHost.csproj` | Library (default) | net10.0 | cross-platform (conditional items) | `Microsoft.PowerShell.GraphicalHost` | DefineConstants=$(DefineConstants);CORECLR; DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | C:165 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `Microsoft.PowerShell.GraphicalHost` (165 C# files, 26235 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|
| [HelpWindow](HelpWindow/_folder.md) | 7 | 2498 |
| [ManagementList](ManagementList/_folder.md) | 132 | 17652 |
| [ShowCommand](ShowCommand/_folder.md) | 22 | 4055 |
| [commandHelpers](commandHelpers/_folder.md) | 3 | 1959 |
| [resources](resources/_folder.md) | 84 | 19531 |

## Public API surface (APPROX)

182 types, 128 public top-level types.

## References

Project refs: `System.Management.Automation`, `Microsoft.PowerShell.Commands.Utility`

Packages: none

Referenced by: `powershell-win-core`

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `src/Microsoft.Management.UI.Internal/commandHelpers/ShowCommandHelper.cs` | 1297 | _GENERATED_ |
| `src/Microsoft.Management.UI.Internal/HelpWindow/HelpParagraphBuilder.cs` | 994 | _GENERATED_ |
| `src/Microsoft.Management.UI.Internal/ManagementList/ManagementList/ManagementList.Generated.cs` | 850 | _GENERATED_ |
| `src/Microsoft.Management.UI.Internal/ManagementList/ManagementList/Innerlist.cs` | 712 | _GENERATED_ |
| `src/Microsoft.Management.UI.Internal/ShowCommand/ViewModel/AllModulesViewModel.cs` | 658 | _GENERATED_ |
| `src/Microsoft.Management.UI.Internal/ShowCommand/ViewModel/CommandViewModel.cs` | 645 | _GENERATED_ |
| `src/Microsoft.Management.UI.Internal/commandHelpers/OutGridView.cs` | 607 | _GENERATED_ |
| `src/Microsoft.Management.UI.Internal/ManagementList/ManagementList/ManagementListStateDescriptor.cs` | 598 | _GENERATED_ |
| `src/Microsoft.Management.UI.Internal/ManagementList/Common/WpfHelp.cs` | 576 | _GENERATED_ |
| `src/Microsoft.Management.UI.Internal/ShowCommand/ViewModel/ModuleViewModel.cs` | 528 | _GENERATED_ |

## Related documents

_none linked yet_
