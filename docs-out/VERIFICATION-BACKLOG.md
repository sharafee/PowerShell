# Verification backlog

Every `UNVERIFIED` claim and every `BLOCKED` item. Under STATIC-ONLY (owner decision `ALLOW_STATIC_ONLY=true`) the standing blocker below applies to all behavior claims.

| ID | status | scope | description | owner-actionable fix | impact |
|---|---|---|---|---|---|
| VB-001 | BLOCKED | all `CORE` behavior claims, golden samples, equivalence across execution modes, Roslyn-based counts | No .NET SDK (global.json requires 10.0.403) and no `pwsh` on the study host; the oracle (5.4) could not run. | Install .NET SDK 10.0.403 and `pwsh` 7.6.x on a host, run `tools/oracle-harness` (to be authored) in a scratch copy, then rerun the study with `ALLOW_STATIC_ONLY=false` (Phase 8 + gates 9, 10). | Behavior statements stay `FACT-SRC`/`INFERENCE`; acceptance status capped at CONDITIONAL. |
| VB-002 | OPEN | LANG-TOKENIZER-001 §7.1 | Behavior of a bare `0x` (no digits): scanner prepends `0` to the digit string, so the emptiness test cannot fire (`tokenizer.cs::Tokenizer.ScanNumberHelper@L3933-L4163`). | Run `pwsh -c '0x'` and tokenizer API on the host (`UNVERIFIED`). | Number-literal edge case. |
| VB-003 | OPEN | LANG-TOKENIZER-001 §7.4 | `#requires` match does not check the character after `requires`, so `#requiresX` may be treated as a requires line. | Run `[System.Management.Automation.Language.Parser]::ParseInput` on `#requiresfoo` and inspect `ScriptRequirements`. | Pragma edge case. |
| VB-004 | OPEN | LANG-TOKENIZER-001 §7.2 | `$(...)` inside a string is pre-scanned by counting parentheses only; a `)` inside a quoted string within it may end the scan early. | Run `"$(  ')' )"` with `pwsh`; also search `test/powershell/Language/Parser` for an asserting test. | String-interpolation edge case. |
| VB-005 | OPEN | LANG-TOKENIZER-001 §16 | Per-assertion mapping from `test/powershell/Language/Parser/*` to tokenizer rules not done. | Pester inventory pass for tokenizer-specific `Describe/Context/It` names. | Test citations. |
