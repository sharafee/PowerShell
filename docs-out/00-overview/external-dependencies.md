---
id: OV-EXTDEP-001
title: External dependencies not in this repository
kind: guide
tier: C
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: []
mirror_cards: []
generated_from: [data/projects.json]
---

# External dependencies not in this repository

> STATIC-ONLY — behavior not run-verified. All counts are `APPROX`/`GENERATED` from regex and own-scanner extraction (no .NET SDK on the study host).

Evidence: `PackageReference` items in the listed `.csproj` files (`FACT-SRC`, via `data/projects.json`), `src/Modules/PSGalleryModules.csproj`, `nuget.config`, and the README files cited. Package versions as written in the project files at the pin.

## Runtime-relevant NuGet packages (shipped product)

| Package | Version | Used by | Purpose (`INFERENCE` from package identity and call sites unless noted) |
|---|---|---|---|
| `Microsoft.PowerShell.Native` | 700.0.2 | `System.Management.Automation` | Prebuilt native shim library (`libpsl-native` on Unix, native helpers on Windows). The in-repo folders `src/libpsl-native/` and `src/powershell-native/` only contain a README stating the code was migrated to the separate PowerShell-native repository (`FACT-SRC`: `src/libpsl-native/README.md`). |
| `Microsoft.Management.Infrastructure` | 3.0.0 | `System.Management.Automation` | CIM/WMI client API used by the CIM adapter and CIM cmdlets (`OUT-OF-SCOPE-DOCUMENTED` for the new shell). |
| `Newtonsoft.Json` | 13.0.4 (`Commands.Utility` pins 13.0.3) | `System.Management.Automation`, `Commands.Utility` | JSON handling inside the engine and the `ConvertFrom/To-Json` family. |
| `Microsoft.ApplicationInsights` | 2.23.0 | `System.Management.Automation` | Telemetry client. |
| `Markdig.Signed` / `Microsoft.PowerShell.MarkdownRender` | 0.44.0 / 7.2.1 | `Commands.Utility` | Markdown rendering cmdlets. |
| `JsonSchema.Net` | 7.4.0 | `Commands.Utility` | `Test-Json` schema validation. |
| `Microsoft.CodeAnalysis.CSharp` | 5.0.0 | `Commands.Utility`, `PSVersionInfoGenerator` | Roslyn: `Add-Type` C# compilation; source generator for version info. |
| `System.Management`, `System.DirectoryServices`, `System.Diagnostics.EventLog`, `System.Security.Cryptography.Pkcs`, `System.Security.Cryptography.ProtectedData`, `System.Security.Permissions`, `System.Configuration.ConfigurationManager`, `System.CodeDom`, `System.Windows.Extensions`, `Microsoft.Win32.Registry.AccessControl` | 10.0.14 | `System.Management.Automation` | .NET compatibility/platform packages (Windows-centric APIs). `ProtectedData` is the DPAPI surface relevant to `SecureString` persistence (see Phase 5). |
| `Microsoft.Security.Extensions` | 1.4.0 | `System.Management.Automation` | Signing/trust APIs (the csproj comment says "Signing APIs"). |
| `Microsoft.Windows.Compatibility` and `System.*` compat packages | 10.0.14 | `Microsoft.PowerShell.SDK` | Meta-package bringing Windows APIs into the SDK package. |
| `Microsoft.Extensions.ObjectPool`, `Microsoft.Bcl.AsyncInterfaces` | 10.0.14 | `Microsoft.PowerShell.SDK` | Support libraries surfaced to SDK consumers. |

Full per-project package table: [project-dependency-graph.md](project-dependency-graph.md).

## Bundled PowerShell modules (not in this repo; restored from the PowerShell Gallery)

`src/Modules/PSGalleryModules.csproj` declares `PackageReference` items for `PSReadLine` 2.4.5, `PowerShellGet` 2.2.5, `PackageManagement` 1.4.8.1, `Microsoft.PowerShell.PSResourceGet` 1.2.0, `Microsoft.PowerShell.Archive` 1.2.6 and `Microsoft.PowerShell.ThreadJob` 2.2.0 (`FACT-SRC`). `nuget.config` clears all package sources and registers one feed, the PowerShell Azure Artifacts feed (`FACT-SRC`).

**Line editor integration.** The console host loads the module by name: `src/Microsoft.PowerShell.ConsoleHost/host/msh/ConsoleHost.cs@L1810` calls `DefaultInitialSessionState.ImportPSModule(new[] { "PSReadLine" })` (`FACT-SRC`). The module is therefore an external, replaceable dependency of the interactive REPL, not part of the engine; the host's prompt code assumes PSReadLine for interactive input (comment at `src/Microsoft.PowerShell.ConsoleHost/host/msh/ConsoleHostUserInterface.cs@L1618`).

## Native code

Native code lives outside the repository (PowerShell-native repo, shipped as `Microsoft.PowerShell.Native`). Managed code reaches Windows and POSIX APIs through P/Invoke declarations. `DllImport|LibraryImport` occurrences concentrate in `security/nativeMethods.cs`, `security/Win32Native/WinTrust.cs`, `security/wldpNativeMethods.cs`, `CoreCLR/CorePsPlatform.cs`, `utils/PlatformInvokes.cs` and the per-API files under `engine/Interop/Windows` (`APPROX`, counted with `rg -c`).

## Build and test tooling dependencies (not shipped)

BenchmarkDotNet 0.15.8, Perfolizer and CommandLineParser (perf tools); xunit 2.9.3, `xunit.runner.visualstudio` 3.1.5 and `Microsoft.NET.Test.Sdk` 18.0.1 (xUnit tests); `Microsoft.Signed.Wix` (MSI packaging); `PowerShellStandard.Library` 5.1.1 (isolated-ALC test assemblies). Pester and other PowerShell test modules are installed by `build.psm1` helpers (see Phase 1 and Phase 6 documents).

## .NET runtime and SDK

`global.json` pins SDK `10.0.403`; `PowerShell.Common.props` sets `TargetFramework` `net10.0` (line 147). `DotnetRuntimeMetadata.json` describes the SDK channel used by the build; its `channel` field says `9.0.1xx-preview6` while `sdkImageVersion` says `10.0.403` (`FACT-SRC`, see DECISIONS D-011).

Verification: package list read from `data/projects.json` (XML-parsed); purpose statements are `INFERENCE` unless a file is cited.
