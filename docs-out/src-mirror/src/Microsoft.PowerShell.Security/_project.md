# Microsoft.PowerShell.Security

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `src/Microsoft.PowerShell.Security/Microsoft.PowerShell.Security.csproj` | Library (default) | net10.0 | cross-platform (conditional items) | `Microsoft.PowerShell.Security` | DefineConstants=$(DefineConstants);CORECLR; DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | B:11 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `Microsoft.PowerShell.Security` (11 C# files, 8196 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|
| [resources](resources/_folder.md) | 98 | 14084 |
| [security](security/_folder.md) | 11 | 8196 |

## Public API surface (APPROX)

41 types, 31 public top-level types.

## References

Project refs: `System.Management.Automation`

Packages: none

Referenced by: `Microsoft.PowerShell.Commands.Management`, `Microsoft.PowerShell.SDK`

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `src/Microsoft.PowerShell.Security/security/CertificateProvider.cs` | 3567 | _GENERATED_ |
| `src/Microsoft.PowerShell.Security/security/AclCommands.cs` | 1566 | _GENERATED_ |
| `src/Microsoft.PowerShell.Security/security/SignatureCommands.cs` | 623 | _GENERATED_ |
| `src/Microsoft.PowerShell.Security/security/CmsCommands.cs` | 602 | _GENERATED_ |
| `src/Microsoft.PowerShell.Security/security/SecureStringCommands.cs` | 390 | _GENERATED_ |
| `src/Microsoft.PowerShell.Security/security/ExecutionPolicyCommands.cs` | 341 | _GENERATED_ |
| `src/Microsoft.PowerShell.Security/security/certificateproviderexceptions.cs` | 304 | _GENERATED_ |
| `src/Microsoft.PowerShell.Security/security/CatalogCommands.cs` | 295 | _GENERATED_ |
| `src/Microsoft.PowerShell.Security/security/CertificateCommands.cs` | 218 | _GENERATED_ |
| `src/Microsoft.PowerShell.Security/security/Utils.cs` | 169 | _GENERATED_ |

## Related documents

_none linked yet_
