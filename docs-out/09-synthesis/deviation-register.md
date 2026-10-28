---
id: SYN-DEV-001
title: Deviation register
kind: synthesis
tier: B
status: partial
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: []
mirror_cards: []
generated_from: []
---

# Deviation register (rule 22)

All rows are `PROPOSED` (the only status this run may write). `APPROVED`/`REJECTED` are set by the product owner outside this run. Until approved, every document describes baseline (PowerShell) behavior.

| DEV-ID | status | baseline behavior (CF/GS) | proposed behavior | benefit | compatibility cost | affected CFs | golden samples that would change | verdict locations |
|---|---|---|---|---|---|---|---|---|
| DEV-CMD-120 | PROPOSED | Windows runtimes ship `Get-Counter`, `Get-WinEvent`, `New-WinEvent` in the default command set (assembly Microsoft.PowerShell.Commands.Diagnostics). | Do not ship OS-specific diagnostics cmdlets in the default set; offer them as optional modules. | Smaller default attack surface and a portable base command set. | Scripts calling these cmdlets need the optional module installed. | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-DIAG-01 (10-command-modules/Microsoft.PowerShell.Commands.Diagnostics.md) |
| DEV-CMD-121 | PROPOSED | WSMan client cmdlets and provider (assembly Microsoft.WSMan.Management) are part of the Windows command set. | Omit WSMan commands; remoting transport becomes pluggable behind one session abstraction. | No dependency on a Windows-only protocol stack in the base product. | WSMan-based automation breaks; an optional transport module could restore it. | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-WSMAN-01 (10-command-modules/Microsoft.WSMan.Management.md) |
| DEV-CMD-122 | PROPOSED | CIM/WMI cmdlets (assembly Microsoft.Management.Infrastructure.CimCmdlets) ship on Windows. | Provide CIM/WMI access only as an optional adapter module. | Keeps the base command set free of Windows management stacks. | Windows management scripts need the optional module. | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-CIM-01 (10-command-modules/Microsoft.Management.Infrastructure.CimCmdlets.md) |
