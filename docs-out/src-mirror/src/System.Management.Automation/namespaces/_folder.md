# src/System.Management.Automation/namespaces

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| B:29 | System.Management.Automation | 29 | 31314 | 68 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `AliasProvider.cs` | 355 | `AliasProvider`, `AliasProviderDynamicParameters` |  |  |
| `ContainerProviderBase.cs` | 1086 | `ContainerCmdletProvider` |  |  |
| `CoreCommandContext.cs` | 1148 | `CmdletProviderContext` |  |  |
| `DriveProviderBase.cs` | 238 | `DriveCmdletProvider` |  |  |
| `EnvironmentProvider.cs` | 247 | `EnvironmentProvider` |  |  |
| `FileSystemContentStream.cs` | 1503 | `FileSystemContentReaderWriter`, `FileStreamBackReader`, `BackReaderEncodingNotSupportedException` |  |  |
| `FileSystemProvider.cs` | 9605 | `CopyFileRemoteUtils`, `FileSystemProvider`, `InternalSymbolicLinkLinkCodeMethods`, `AlternateDataStreamUtilities` (+13) |  |  |
| `FileSystemSecurity.cs` | 344 | `FileSystemProvider` |  |  |
| `FunctionProvider.cs` | 389 | `FunctionProvider`, `FunctionProviderDynamicParameters` |  |  |
| `IContentProvider.cs` | 149 | `IContentCmdletProvider` |  |  |
| `IContentReader.cs` | 68 | `IContentReader` |  |  |
| `IContentWriter.cs` | 69 | `IContentWriter` |  |  |
| `IDynamicPropertyProvider.cs` | 339 | `IDynamicPropertyCmdletProvider` |  |  |
| `IPermissionProvider.cs` | 110 | `ISecurityDescriptorCmdletProvider` |  |  |
| `IPropertiesProvider.cs` | 201 | `IPropertyCmdletProvider` |  |  |
| `ItemProviderBase.cs` | 690 | `ItemCmdletProvider` |  |  |
| `LocationGlobber.cs` | 4732 | `LocationGlobber` |  |  |
| `NavigationProviderBase.cs` | 1091 | `NavigationCmdletProvider` |  |  |
| `PathInfo.cs` | 165 | `PathInfo` |  |  |
| `ProviderBase.cs` | 1986 | `CmdletProvider`, `ICmdletProviderSupportsHelp` |  |  |
| `ProviderBaseSecurity.cs` | 99 | `CmdletProvider` |  |  |
| `ProviderDeclarationAttribute.cs` | 162 | `ProviderCapabilities`, `CmdletProviderAttribute` |  |  |
| `RegistryProvider.cs` | 4180 | `RegistryProvider`, `RegistryProviderSetItemDynamicParameter` |  |  |
| `RegistrySecurity.cs` | 213 | `RegistryProvider` |  |  |
| `RegistryWrapper.cs` | 449 | `TransactedRegistryWrapper`, `RegistryWrapper`, `RegistryWrapperUtils`, `IRegistryWrapper` |  |  |
| `SessionStateProviderBase.cs` | 1223 | `SessionStateProviderBase`, `SessionStateProviderBaseContentReaderWriter` |  |  |
| `StackInfo.cs` | 61 | `PathInfoStack` |  |  |
| `VariableProvider.cs` | 238 | `VariableProvider` |  |  |
| `Win32Native.cs` | 174 | `Win32Native` |  |  |

## Partial-class and conditional-compilation notes

Partial types spanning files: `CmdletProvider`, `FileSystemProvider`, `RegistryProvider`

`#if` conditions on types here: `!UNIX`

## Related documents

_none linked yet_
