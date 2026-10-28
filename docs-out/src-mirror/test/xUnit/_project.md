# xUnit.tests

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `test/xUnit/xUnit.tests.csproj` | Library (default) | net10.0 | cross-platform (conditional items) | `powershell-tests` | DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | C:29 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `xUnit.tests` (29 C# files, 5749 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|
| [Asserts](Asserts/_folder.md) | 2 | 74 |
| [csharp](csharp/_folder.md) | 26 | 5668 |

## Public API surface (APPROX)

38 types, 33 public top-level types.

## References

Project refs: `Microsoft.PowerShell.SDK`, `Microsoft.PowerShell.Commands.Diagnostics`, `Microsoft.WSMan.Management`, `Microsoft.Management.Infrastructure.CimCmdlets`

Packages: xunit 2.9.3, Xunit.SkippableFact 1.5.85, xunit.runner.visualstudio 3.1.5, XunitXml.TestLogger 8.0.0, Microsoft.NET.Test.Sdk 18.0.1

Referenced by: none

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `test/xUnit/csharp/test_CommandLineParser.cs` | 1332 | _GENERATED_ |
| `test/xUnit/csharp/test_PSConfiguration.cs` | 1104 | _GENERATED_ |
| `test/xUnit/csharp/test_RemoteHyperV.cs` | 819 | _GENERATED_ |
| `test/xUnit/csharp/test_Subsystem.cs` | 345 | _GENERATED_ |
| `test/xUnit/csharp/test_Prediction.cs` | 252 | _GENERATED_ |
| `test/xUnit/csharp/test_CorePsPlatform.cs` | 238 | _GENERATED_ |
| `test/xUnit/csharp/test_FileSystemProvider.cs` | 206 | _GENERATED_ |
| `test/xUnit/csharp/test_CompletionHelpers.cs` | 183 | _GENERATED_ |
| `test/xUnit/csharp/test_Utils.cs` | 179 | _GENERATED_ |
| `test/xUnit/csharp/test_Runspace.cs` | 132 | _GENERATED_ |

## Related documents

_none linked yet_
