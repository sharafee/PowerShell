# src/System.Management.Automation/security

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| B:9 | System.Management.Automation | 9 | 7641 | 102 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `Authenticode.cs` | 605 | `SignatureHelper`, `SigningOption` |  |  |
| `CatalogHelper.cs` | 841 | `CatalogHelper`, `CatalogInformation`, `CatalogValidationStatus` |  |  |
| `CredentialParameter.cs` | 91 | `CredentialAttribute` |  |  |
| `MshSignature.cs` | 393 | `Signature`, `SignatureStatus`, `SignatureType`, `Win32Errors` |  |  |
| `SecureStringHelper.cs` | 643 | `SecureStringHelper`, `ProtectedData`, `CAPI`, `EncryptionResult` (+1) |  |  |
| `SecurityManager.cs` | 828 | `PSAuthorizationManager` |  |  |
| `SecuritySupport.cs` | 1777 | `SecuritySupport`, `AmsiUtils`, `CmsMessageRecipient`, `CmsUtils` (+6) |  |  |
| `nativeMethods.cs` | 1513 | `NativeMethods`, `NativeMethods`, `NativeConstants`, `NativeMethods` (+8) |  |  |
| `wldpNativeMethods.cs` | 950 | `SystemPolicy`, `SystemScriptFileEnforcement`, `SystemEnforcementMode` |  |  |

## Subfolders

- [Win32Native](Win32Native/_folder.md) (1 files, 440 LOC)

## Partial-class and conditional-compilation notes

Partial types spanning files: `SystemEnforcementMode`, `SystemPolicy`, `SystemScriptFileEnforcement`

`#if` conditions on types here: `!UNIX`

## Related documents

_none linked yet_
