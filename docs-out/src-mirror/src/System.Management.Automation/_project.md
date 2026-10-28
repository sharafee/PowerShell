# System.Management.Automation

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `src/System.Management.Automation/System.Management.Automation.csproj` | Library (default) | net10.0 | cross-platform (conditional items) | `System.Management.Automation` | DefineConstants=$(DefineConstants);CORECLR; DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | A:106, B:598 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `System.Management.Automation` (704 C# files, 563707 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|
| [CoreCLR](CoreCLR/_folder.md) | 4 | 3251 |
| [DscSupport](DscSupport/_folder.md) | 1 | 4064 |
| [FormatAndOutput](FormatAndOutput/_folder.md) | 62 | 31911 |
| [SourceGenerators](SourceGenerators/_folder.md) | 1 | 136 |
| [cimSupport](cimSupport/_folder.md) | 11 | 12260 |
| [engine](engine/_folder.md) | 479 | 425987 |
| [help](help/_folder.md) | 43 | 18038 |
| [logging](logging/_folder.md) | 3 | 1699 |
| [namespaces](namespaces/_folder.md) | 29 | 31314 |
| [resources](resources/_folder.md) | 1050 | 261836 |
| [security](security/_folder.md) | 10 | 8081 |
| [singleshell](singleshell/_folder.md) | 3 | 1629 |
| [utils](utils/_folder.md) | 57 | 25449 |

## Public API surface (APPROX)

2857 types, 879 public top-level types.

## References

Project refs: `PSVersionInfoGenerator`, `Microsoft.PowerShell.CoreCLR.Eventing`

Packages: Newtonsoft.Json 13.0.4, Microsoft.ApplicationInsights 2.23.0, Microsoft.Win32.Registry.AccessControl 10.0.14, System.CodeDom 10.0.14, System.Configuration.ConfigurationManager 10.0.14, System.Diagnostics.EventLog 10.0.14, System.DirectoryServices 10.0.14, System.Management 10.0.14, System.Security.Cryptography.Pkcs 10.0.14, System.Security.Cryptography.ProtectedData 10.0.14, System.Security.Permissions 10.0.14, Microsoft.Management.Infrastructure 3.0.0, Microsoft.PowerShell.Native 700.0.2, Microsoft.Security.Extensions 1.4.0, System.Windows.Extensions 10.0.14

Referenced by: `Microsoft.Management.Infrastructure.CimCmdlets`, `Microsoft.PowerShell.Commands.Diagnostics`, `Microsoft.PowerShell.Commands.Utility`, `Microsoft.PowerShell.ConsoleHost`, `Microsoft.PowerShell.GraphicalHost`, `Microsoft.PowerShell.SDK`, `Microsoft.PowerShell.Security`, `Microsoft.WSMan.Management`

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `src/System.Management.Automation/engine/parser/ast.cs` | 10845 | _GENERATED_ |
| `src/System.Management.Automation/namespaces/FileSystemProvider.cs` | 9605 | _GENERATED_ |
| `src/System.Management.Automation/engine/CommandCompletion/CompletionCompleters.cs` | 9251 | _GENERATED_ |
| `src/System.Management.Automation/engine/TypeTable_Types_Ps1Xml.cs` | 9139 | _GENERATED_ |
| `src/System.Management.Automation/engine/parser/Parser.cs` | 8279 | _GENERATED_ |
| `src/System.Management.Automation/engine/runtime/Binding/Binders.cs` | 8015 | _GENERATED_ |
| `src/System.Management.Automation/engine/serialization.cs` | 7679 | _GENERATED_ |
| `src/System.Management.Automation/engine/Modules/ModuleCmdletBase.cs` | 7495 | _GENERATED_ |
| `src/System.Management.Automation/engine/parser/Compiler.cs` | 7082 | _GENERATED_ |
| `src/System.Management.Automation/cimSupport/cmdletization/xml/CoreCLR/cmdlets-over-objects.xmlSerializer.autogen.cs` | 6688 | _GENERATED_ |

## Related documents

_none linked yet_
