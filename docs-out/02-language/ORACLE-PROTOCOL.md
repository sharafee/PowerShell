---
id: LANG-ORACLE-001
title: Oracle protocol
kind: guide
tier: B
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: []
mirror_cards: []
generated_from: []
---

# Oracle protocol

> STATIC-ONLY — the oracle was **waived** for this run (no .NET SDK 10.0.403 and no `pwsh` on the study host; backlog VB-001). This document records what the protocol would be, so a later run on a suitable host can execute it. Nothing here was executed.

## 1. Purpose and scope [SPEC]

How to obtain golden samples ([GOLDEN-SAMPLES.md](GOLDEN-SAMPLES.md)): run snippets through a real `pwsh` 7.6.x built from the pinned commit (or the matching release), capture tokens, AST, results and errors, normalize them, and diff against the claims of the study and later against MicroteamShell.

## 2. Source map

Planned tools: `docs-out/tools/oracle-harness` (not authored), `docs-out/tools/verify-with-pwsh.ps1` (not authored; the Lite prompt names it).

## 3. Responsibilities and non-responsibilities

Specifies commands and normalization; does not execute.

## 4. Key types and contracts [IMPL]

Inputs: a snippet list (from [REFERENCE-TEST-CORPUS.md](REFERENCE-TEST-CORPUS.md) and [SEMANTIC-QUIRKS.md](SEMANTIC-QUIRKS.md)); outputs: one JSON record per snippet ([GOLDEN-SAMPLES.md](GOLDEN-SAMPLES.md) §4).

## 5. Data model

Normalization: replace absolute paths and GUIDs, fix culture to invariant (and repeat selected snippets under a second culture), record `$PSVersionTable`, OS and time zone, serialize objects with type names and property values (depth-limited), sort hashtable keys.

## 6. Control flow

1. Build or install `pwsh` 7.6.x; verify `git rev-parse HEAD` equals the pin (the pin in `.work/pin.json`).
2. For each snippet: tokenize and parse with `[System.Management.Automation.Language.Parser]::ParseInput` (tokens, AST type names, errors); execute in a fresh runspace with `-NoProfile`; capture success output, error records, other streams, `$?`, `$LASTEXITCODE`.
3. Force execution modes: interpreted vs compiled by repeating a function call 40 times (JIT after the 33rd call) and a loop 20 times; optimized vs unoptimized by dot-sourcing; Constrained Language via `$ExecutionContext.SessionState.LanguageMode`. A mode that cannot be forced is reported as such (prompt 5.4).
4. Write the record; mark the matching claims verified.

## 7. Algorithms

Not applicable.

## 8. Observable behavior [SPEC]

Not applicable.

## 9. Error handling and edge cases

Snippets that hang or prompt are killed after a timeout and recorded as such.

## 10. Concurrency and threading

Each snippet runs in its own process for isolation.

## 11. Extension points and customization hooks

None.

## 12. Dependencies

[TIERING-POLICY.md](TIERING-POLICY.md) §7 (thresholds used to force modes), [EQUIVALENCE-SPEC.md](EQUIVALENCE-SPEC.md) (what to compare across modes).

## 13. Performance notes

Not applicable.

## 14. Security considerations (mandatory)

Snippets run arbitrary code: use a disposable scratch copy, no network, no credentials, and never run repository scripts other than the snippets.

## 15. Enterprise considerations

Record tool versions and hashes with every run.

## 16. Tests

Not applicable.

## 17. Design decisions and trade-offs

Waived for this run by the owner; static reading plus the repository's own tests is the interim evidence.

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-ORACLE-01** [ADAPT] (area: NLD-TOOL) Use the recorded oracle outputs as the expected values of the new interpreter's conformance suite and re-run the oracle for each new quirk. Why: same coverage with an automated diff instead of manual review. Evidence: `test/powershell/Language/Operators/` (existing assertion style).

## 19. Open questions / UNVERIFIED

Everything in this file is unexecuted (VB-001).

Verification: none (design only).
