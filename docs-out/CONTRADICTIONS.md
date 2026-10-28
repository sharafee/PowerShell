# Contradictions register (rule 23)

Rows are never resolved by silent rewording. Status: `OPEN | RESOLVED`. Final state must have no `OPEN` rows (gate 12).

| CON-ID | statement A + location | statement B + location | evidence classes | status | resolution + evidence | files changed |
|---|---|---|---|---|---|---|
| CON-001 | `build.psm1::New-PSOptions` help text `.PARAMETER Framework`: "Defaults to 'net11.0'" (`build.psm1@L1230-L1260`) | same function: `[ValidateSet("net10.0")] [string]$Framework = "net10.0"` (`build.psm1@L1230-L1400`) and `PowerShell.Common.props` `TargetFramework` `net10.0` | E1 comment vs E1 code | RESOLVED | rule 1: code beats comments; framework is `net10.0` | docs-out/01-repository/build-system.md (noted in section 17) |
