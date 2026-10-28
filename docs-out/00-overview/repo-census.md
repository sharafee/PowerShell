---
id: OV-CENSUS-001
title: Repository census
kind: catalog
tier: C
status: partial
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: []
mirror_cards: []
generated_from: [data/files.csv, data/projects.json, data/numbers.json]
---

# Repository census

> STATIC-ONLY — behavior not run-verified. All counts are `APPROX`/`GENERATED` from regex and own-scanner extraction (no .NET SDK on the study host).

Pinned at **v7.6.9** (commit `523031e`). Total files: <!--N:REPO_FILES_TOTAL-->4546<!--/N-->; C# files: <!--N:CS_FILES_ALL-->1269<!--/N--> (<!--N:CS_FILES_SRC-->1179<!--/N--> under `src/`); C# physical lines under `src/`: <!--N:CS_LOC_SRC-->732804<!--/N-->; projects (`.csproj`): <!--N:PROJECT_COUNT-->40<!--/N-->, of which <!--N:PROJECTS_IN_SOLUTION-->15<!--/N--> are in `PowerShell.sln`.

## Files and lines per language (`GENERATED`)

| Language | Files | Lines |
|---|---:|---:|
| C# | 1269 | 743579 |
| resx | 2100 | 441396 |
| PowerShell | 503 | 138559 |
| Markdown | 92 | 22706 |
| YAML | 127 | 14146 |
| JSON | 50 | 13548 |
| XSD | 50 | 7731 |
| ETW manifest | 1 | 5869 |
| text | 11 | 4628 |
| other | 107 | 4491 |
| XML | 41 | 2813 |
| shell | 13 | 1803 |
| msbuild | 43 | 1426 |
| PowerShell-data | 47 | 1334 |
| ps1xml | 9 | 932 |
| WiX | 2 | 694 |
| sln | 3 | 230 |
| MOF | 6 | 137 |
| batch | 1 | 1 |
| image | 71 | 0 |

## Top-level folders (`GENERATED`)

| Folder | Files | Lines (all text) | C# lines |
|---|---:|---:|---:|
| `src` | 3428 | 1190650 | 732804 |
| `test` | 718 | 133820 | 10740 |
| `tools` | 70 | 26058 | 0 |
| `(root files)` | 28 | 15870 | 0 |
| `CHANGELOG` | 12 | 12282 | 0 |
| `.pipelines` | 85 | 11702 | 0 |
| `.github` | 66 | 6959 | 0 |
| `docs` | 56 | 4087 | 35 |
| `.vsts-ci` | 22 | 1942 | 0 |
| `assets` | 47 | 1240 | 0 |
| `Localize` | 1 | 764 | 0 |
| `dsc` | 2 | 305 | 0 |
| `.vscode` | 4 | 159 | 0 |
| `.config` | 3 | 93 | 0 |
| `.devcontainer` | 2 | 48 | 0 |
| `docker` | 2 | 44 | 0 |

## C# lines per project (`GENERATED`)

| Project | In solution | C# files | C# lines | Tier mix |
|---|---|---:|---:|---|
| `System.Management.Automation` | yes | 704 | 563707 | A:106, B:598 |
| `System.Management.Automation` | no | 704 | 563707 | A:106, B:598 |
| `Microsoft.PowerShell.Commands.Utility` | yes | 143 | 45004 | C:143 |
| `Microsoft.PowerShell.Commands.Utility` | no | 143 | 45004 | C:143 |
| `Microsoft.PowerShell.Commands.Management` | yes | 61 | 33198 | C:61 |
| `Microsoft.PowerShell.GraphicalHost` | no | 165 | 26235 | C:165 |
| `Microsoft.PowerShell.ConsoleHost` | yes | 26 | 17831 | B:26 |
| `Microsoft.PowerShell.ConsoleHost` | no | 26 | 17831 | B:26 |
| `Microsoft.Management.Infrastructure.CimCmdlets` | yes | 35 | 15485 | C:35 |
| `Microsoft.WSMan.Management` | yes | 11 | 13139 | C:11 |
| `Microsoft.PowerShell.Security` | yes | 11 | 8196 | B:11 |
| `xUnit.tests` | yes | 29 | 5749 | C:29 |
| `Microsoft.PowerShell.Commands.Diagnostics` | yes | 8 | 4727 | C:8 |
| `Microsoft.PowerShell.CoreCLR.Eventing` | yes | 9 | 3811 | C:9 |
| `WebListener` | no | 22 | 1584 | C:22 |
| `BenchmarkDotNet.Extensions` | no | 11 | 751 | C:11 |
| `Microsoft.PowerShell.NamedPipeConnection` | no | 1 | 641 | C:1 |
| `ResultsComparer` | no | 3 | 477 | C:3 |
| `TypeCatalogGen` | no | 1 | 472 | C:1 |
| `Reporting` | no | 8 | 319 | C:8 |
| `powershell-perf` | no | 5 | 262 | C:5 |
| `TestExe` | no | 1 | 248 | C:1 |
| `hosting.tests` | no | 1 | 224 | C:1 |
| `ResGen` | no | 1 | 189 | C:1 |
| `PSVersionInfoGenerator` | yes | 1 | 136 | B:1 |
| `Microsoft.WSMan.Runtime` | yes | 1 | 112 | C:1 |
| `Test.Isolated.Init` | no | 1 | 83 | C:1 |
| `TestService` | no | 3 | 69 | C:3 |
| `Microsoft.PowerShell.GlobalTool.Shim` | no | 1 | 56 | C:1 |
| `Test.Isolated.Nested` | no | 1 | 43 | C:1 |
| `Test.Isolated.Root` | no | 1 | 39 | C:1 |
| `MyApp` | no | 1 | 35 | C:1 |
| `UnixSocket` | no | 1 | 27 | C:1 |
| `PowerShell.Windows.x64` | no | 0 | 0 |  |
| `Microsoft.PowerShell.SDK` | yes | 0 | 0 |  |
| `PSGalleryModules` | no | 0 | 0 |  |
| `powershell-unix` | yes | 0 | 0 |  |
| `powershell-win-core` | yes | 0 | 0 |  |
| `PSGalleryTestModules` | no | 0 | 0 |  |
| `Microsoft.PowerShell.Packaging` | no | 0 | 0 |  |

## Tier assignment (section 4.1)

Tier A files: <!--N:CS_FILES_TIER_A-->106<!--/N--> files / <!--N:CS_LOC_TIER_A-->125308<!--/N--> lines; Tier B: <!--N:CS_FILES_TIER_B-->636<!--/N--> files; Tier C: <!--N:CS_FILES_TIER_C-->527<!--/N--> files (C# only). Per-file assignment: `.work/tiers.csv`.

Verification: counts produced by `tools/p0_extract.py`; regenerate with `python3 docs-out/tools/p0_extract.py && python3 docs-out/tools/numbers.py gen`.
