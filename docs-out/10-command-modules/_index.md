---
id: CMD-INDEX-001
title: Command module families
kind: catalog
tier: C
status: draft
run_verification: none
scope_class: EXTENDED
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: []
mirror_cards: []
generated_from: [data/cmdlets.json]
---

# Command module families

> STATIC-ONLY — behavior not run-verified. All counts are `APPROX`/`GENERATED` from regex and own-scanner extraction (no .NET SDK on the study host).

| Assembly | Cmdlets | Providers | Scope class | Document |
|---|---:|---:|---|---|
| `System.Management.Automation` | 63 | 6 | EXTENDED | [CMD-SMA-001](System.Management.Automation.md) |
| `Microsoft.PowerShell.Commands.Utility` | 118 | 0 | EXTENDED | [CMD-UTILITY-001](Microsoft.PowerShell.Commands.Utility.md) |
| `Microsoft.PowerShell.Commands.Management` | 63 | 0 | EXTENDED | [CMD-MANAGEMENT-001](Microsoft.PowerShell.Commands.Management.md) |
| `Microsoft.PowerShell.Security` | 15 | 1 | EXTENDED | [CMD-SECURITY-001](Microsoft.PowerShell.Security.md) |
| `Microsoft.PowerShell.ConsoleHost` | 2 | 0 | EXTENDED | [CMD-CONSOLEHOST-001](Microsoft.PowerShell.ConsoleHost.md) |
| `Microsoft.PowerShell.Commands.Diagnostics` | 3 | 0 | OUT-OF-SCOPE-DOCUMENTED | [CMD-DIAGNOSTICS-001](Microsoft.PowerShell.Commands.Diagnostics.md) |
| `Microsoft.WSMan.Management` | 13 | 1 | OUT-OF-SCOPE-DOCUMENTED | [CMD-WSMAN-001](Microsoft.WSMan.Management.md) |
| `Microsoft.Management.Infrastructure.CimCmdlets` | 12 | 0 | OUT-OF-SCOPE-DOCUMENTED | [CMD-CIM-001](Microsoft.Management.Infrastructure.CimCmdlets.md) |
| `Microsoft.WSMan.Runtime` | 0 | 0 | OUT-OF-SCOPE-DOCUMENTED | [CMD-WSMANRT-001](Microsoft.WSMan.Runtime.md) |
| `Microsoft.PowerShell.GraphicalHost` | 0 | 0 | OUT-OF-SCOPE-DOCUMENTED | [CMD-GRAPHICAL-001](Microsoft.PowerShell.GraphicalHost.md) |
| `Microsoft.PowerShell.CoreCLR.Eventing` | 0 | 0 | OUT-OF-SCOPE-DOCUMENTED | [CMD-EVENTING-001](Microsoft.PowerShell.CoreCLR.Eventing.md) |

Cmdlet totals: <!--N:CMDLET_CLASSES-->300<!--/N--> cmdlet classes and <!--N:PROVIDER_CLASSES-->8<!--/N--> provider classes in the tree (includes classes in test tools and samples that are not part of the product: `data/cmdlets.json` rows with project `(none)`, `Microsoft.PowerShell.NamedPipeConnection`, `Test.Isolated.*`).

## Registration summary (`FACT-SRC`)

- Engine-hosted cmdlets and providers are registered through static tables in `src/System.Management.Automation/engine/InitialSessionState.cs`; `InitialSessionState.CreateDefault2()` loads only the core snap-in plus built-in variables, functions and aliases and leaves the other cmdlets to modules (doc comment: "The default cmdlets, provider, etc are loaded via Modules").
- Every other assembly is loaded through a module manifest under `src/Modules/{Shared,Unix,Windows}` (`NestedModules = @("<Assembly>.dll")`), with separate manifests per platform because exported cmdlets differ (`src/Modules/README.md`).
