# src/Microsoft.PowerShell.Security/security

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| B:11 | Microsoft.PowerShell.Security | 11 | 8196 | 41 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `AclCommands.cs` | 1566 | `SetAclCommand`, `SecurityDescriptorCommandsBase`, `GetAclCommand` |  |  |
| `CatalogCommands.cs` | 295 | `CatalogCommandsBase`, `TestFileCatalogCommand`, `NewFileCatalogCommand` |  |  |
| `CertificateCommands.cs` | 218 | `GetPfxCertificateCommand` |  |  |
| `CertificateProvider.cs` | 3567 | `CertificateProvider`, `X509NativeStore`, `SendAsTrustedIssuerProperty`, `DnsNameRepresentation` (+11) |  |  |
| `CmsCommands.cs` | 602 | `UnprotectCmsMessageCommand`, `ProtectCmsMessageCommand`, `GetCmsMessageCommand` |  |  |
| `CredentialCommands.cs` | 121 | `GetCredentialCommand` |  |  |
| `ExecutionPolicyCommands.cs` | 341 | `SetExecutionPolicyCommand`, `GetExecutionPolicyCommand` |  |  |
| `SecureStringCommands.cs` | 390 | `ConvertToSecureStringCommand`, `ConvertFromSecureStringCommand`, `ConvertFromToSecureStringCommandBase`, `SecureStringCommandBase` |  |  |
| `SignatureCommands.cs` | 623 | `SetAuthenticodeSignatureCommand`, `SignatureCommandsBase`, `GetAuthenticodeSignatureCommand` |  |  |
| `Utils.cs` | 169 | `SecurityUtils` |  |  |
| `certificateproviderexceptions.cs` | 304 | `CertificateNotFoundException`, `CertificateStoreNotFoundException`, `CertificateStoreLocationNotFoundException`, `CertificateProviderItemNotFoundException` |  |  |

## Partial-class and conditional-compilation notes

No partial types spanning files (APPROX).

`#if` conditions on types here: `!UNIX`

## Related documents

_none linked yet_
