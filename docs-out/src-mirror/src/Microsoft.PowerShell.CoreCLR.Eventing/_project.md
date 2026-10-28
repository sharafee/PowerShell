# Microsoft.PowerShell.CoreCLR.Eventing

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `src/Microsoft.PowerShell.CoreCLR.Eventing/Microsoft.PowerShell.CoreCLR.Eventing.csproj` | Library (default) | net10.0 | cross-platform (conditional items) | `Microsoft.PowerShell.CoreCLR.Eventing` | DefineConstants=$(DefineConstants);CORECLR; DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | C:9 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `Microsoft.PowerShell.CoreCLR.Eventing` (9 C# files, 3811 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|
| [DotNetCode](DotNetCode/_folder.md) | 8 | 3805 |
| [resources](resources/_folder.md) | 14 | 1890 |

## Public API surface (APPROX)

34 types, 3 public top-level types.

## References

Project refs: none

Packages: System.Diagnostics.EventLog 10.0.14

Referenced by: `System.Management.Automation`

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `src/Microsoft.PowerShell.CoreCLR.Eventing/DotNetCode/Eventing/Reader/NativeWrapper.cs` | 1473 | _GENERATED_ |
| `src/Microsoft.PowerShell.CoreCLR.Eventing/DotNetCode/Eventing/UnsafeNativeMethods.cs` | 926 | _GENERATED_ |
| `src/Microsoft.PowerShell.CoreCLR.Eventing/DotNetCode/Eventing/EventProvider.cs` | 783 | _GENERATED_ |
| `src/Microsoft.PowerShell.CoreCLR.Eventing/DotNetCode/Eventing/EventProviderTraceListener.cs` | 289 | _GENERATED_ |
| `src/Microsoft.PowerShell.CoreCLR.Eventing/DotNetCode/Eventing/EventDescriptor.cs` | 132 | _GENERATED_ |
| `src/Microsoft.PowerShell.CoreCLR.Eventing/DotNetCode/Eventing/Reader/CoTaskMemUnicodeSafeHandle.cs` | 70 | _GENERATED_ |
| `src/Microsoft.PowerShell.CoreCLR.Eventing/DotNetCode/Eventing/Reader/CoTaskMemSafeHandle.cs` | 67 | _GENERATED_ |
| `src/Microsoft.PowerShell.CoreCLR.Eventing/DotNetCode/Eventing/Reader/EventLogHandle.cs` | 65 | _GENERATED_ |
| `src/Microsoft.PowerShell.CoreCLR.Eventing/AssemblyInfo.cs` | 6 | _GENERATED_ |

## Related documents

_none linked yet_
