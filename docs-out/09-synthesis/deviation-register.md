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
| DEV-AST-020 | PROPOSED | AST nodes carry mutable compiler caches (TupleIndex, RuntimeUsingIndex, TypeDefinitionAst.Type) and implement compile-time assignment protocols (ISupportsAssignment/IAssignableValue). | AST stays purely syntactic; slot indexes and assignment code generation live in compiler side tables keyed by node. | Immutable shareable trees; clean separation of parser and compiler; easier tooling reuse. | None observable by scripts; internal refactor only. | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-AST-07 (02-language/02.3-ast.md) |
| DEV-CMD-120 | PROPOSED | Windows runtimes ship `Get-Counter`, `Get-WinEvent`, `New-WinEvent` in the default command set (assembly Microsoft.PowerShell.Commands.Diagnostics). | Do not ship OS-specific diagnostics cmdlets in the default set; offer them as optional modules. | Smaller default attack surface and a portable base command set. | Scripts calling these cmdlets need the optional module installed. | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-DIAG-01 (10-command-modules/Microsoft.PowerShell.Commands.Diagnostics.md) |
| DEV-CMD-121 | PROPOSED | WSMan client cmdlets and provider (assembly Microsoft.WSMan.Management) are part of the Windows command set. | Omit WSMan commands; remoting transport becomes pluggable behind one session abstraction. | No dependency on a Windows-only protocol stack in the base product. | WSMan-based automation breaks; an optional transport module could restore it. | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-WSMAN-01 (10-command-modules/Microsoft.WSMan.Management.md) |
| DEV-CMD-122 | PROPOSED | CIM/WMI cmdlets (assembly Microsoft.Management.Infrastructure.CimCmdlets) ship on Windows. | Provide CIM/WMI access only as an optional adapter module. | Keeps the base command set free of Windows management stacks. | Windows management scripts need the optional module. | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-CIM-01 (10-command-modules/Microsoft.Management.Infrastructure.CimCmdlets.md) |
| DEV-ENG-040 | PROPOSED | Compilation of a top-level script block runs an AMSI scan, admin-block check and suspicious-content hashing. | Compilation is policy-free; an optional policy hook runs before execution. | Smaller engine core; platform-independent. | No AMSI integration or forced logging on suspicious content. | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-ENG-07 (02-language/02.5-compiler-and-engine.md) |
| DEV-EQV-061 | PROPOSED | Interpreter keeps typed arithmetic/comparison instruction families inherited from the DLR. | Do not port them; numeric semantics come from the evaluator's conversion rules. | Removes dead and defective code. | None observable (instructions unreachable from PowerShell IR). | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-EQV-03 (02-language/EQUIVALENCE-SPEC.md) |
| DEV-GRM-010 | PROPOSED | The parser resolves `using assembly` paths against the filesystem and may create a runspace for `configuration` while parsing. | Parsing is pure: directives are recorded in the AST and resolved in a later phase. | Deterministic, side-effect-free parse; safe for tooling and untrusted text. | Errors for a missing assembly appear at a later phase than in PowerShell. | CF-GRM-001 | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-PARSER-07 (02-language/02.2-parser.md) |
| DEV-LEX-001 | PROPOSED | Tokenizer detects signature-block lookalikes and processes #requires comment lines at parse time. | Omit both from the tokenizer; if wanted, handle pragmas in a dedicated post-tokenize pass. | Keeps the tokenizer a pure text-to-token function; removes security-sensitive fuzzy matching from the hot path. | Scripts using #requires get no version/module check; signed-script trailer detection unavailable. | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-TOK-07 (02-language/02.1-tokenizer.md) |
| DEV-SEM-030 | PROPOSED | `using module` is resolved at parse time by running Get-Module -ListAvailable in a PowerShell instance. | The directive is recorded; module import happens in a later phase. | Parsing has no side effects or I/O. | Missing-module errors appear later than in PowerShell. | - | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-SEM-06 (02-language/02.4-semantic-analysis.md) |
| DEV-TIER-060 | PROPOSED | Hot loops are promoted from interpreter to JIT in the background mid-execution via in-place instruction replacement. | No mid-execution promotion; any optimizer runs synchronously at defined points. | Deterministic execution, simpler frames. | Long top-level loops lose the speed-up PowerShell gets. | CF-CMP-002 | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | LSN-TIER-04 (02-language/TIERING-POLICY.md) |
