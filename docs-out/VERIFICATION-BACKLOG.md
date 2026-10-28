# Verification backlog

Every `UNVERIFIED` claim and every `BLOCKED` item. Under STATIC-ONLY (owner decision `ALLOW_STATIC_ONLY=true`) the standing blocker below applies to all behavior claims.

| ID | status | scope | description | owner-actionable fix | impact |
|---|---|---|---|---|---|
| VB-001 | BLOCKED | all `CORE` behavior claims, golden samples, equivalence across execution modes, Roslyn-based counts | No .NET SDK (global.json requires 10.0.403) and no `pwsh` on the study host; the oracle (5.4) could not run. | Install .NET SDK 10.0.403 and `pwsh` 7.6.x on a host, run `tools/oracle-harness` (to be authored) in a scratch copy, then rerun the study with `ALLOW_STATIC_ONLY=false` (Phase 8 + gates 9, 10). | Behavior statements stay `FACT-SRC`/`INFERENCE`; acceptance status capped at CONDITIONAL. |
