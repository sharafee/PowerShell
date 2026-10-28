# hosting.tests

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `test/hosting/hosting.tests.csproj` | Library (default) | net10.0 | cross-platform (conditional items) | `powershell-hosting-tests` | DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | C:1 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `hosting.tests` (1 C# files, 224 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|

## Public API surface (APPROX)

1 types, 1 public top-level types.

## References

Project refs: none

Packages: xunit 2.4.1, XunitXml.TestLogger 2.0.0, Microsoft.PowerShell.SDK $(RELEASE_VERSION), Xunit.SkippableFact 1.3.6, xunit.runner.visualstudio 2.4.3, Microsoft.NET.Test.Sdk 16.7.1, System.ServiceModel.Duplex 4.10.3, System.ServiceModel.Http 4.10.3, System.ServiceModel.NetTcp 4.10.3, System.ServiceModel.Primitives 4.10.3, System.ServiceModel.Security 4.10.3, System.Private.ServiceModel 4.10.3

Referenced by: none

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `test/hosting/test_HostingBasic.cs` | 224 | _GENERATED_ |

## Related documents

_none linked yet_
