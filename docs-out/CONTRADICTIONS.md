# Contradictions register (rule 23)

Rows are never resolved by silent rewording. Status: `OPEN | RESOLVED`. Final state must have no `OPEN` rows (gate 12).

| CON-ID | statement A + location | statement B + location | evidence classes | status | resolution + evidence | files changed |
|---|---|---|---|---|---|---|
| CON-001 | `build.psm1::New-PSOptions` help text `.PARAMETER Framework`: "Defaults to 'net11.0'" (`build.psm1@L1230-L1260`) | same function: `[ValidateSet("net10.0")] [string]$Framework = "net10.0"` (`build.psm1@L1230-L1400`) and `PowerShell.Common.props` `TargetFramework` `net10.0` | E1 comment vs E1 code | RESOLVED | rule 1: code beats comments; framework is `net10.0` | docs-out/01-repository/build-system.md (noted in section 17) |
| CON-002 | `token.cs::TokenKind` XML doc comments mark `AndAnd`/`OrOr` as "(unimplemented)" (`src/System.Management.Automation/engine/parser/token.cs@L158-L161`) | `Tokenizer.NextToken` returns `AndAnd`/`OrOr` for `&&`/`||` in every mode (`src/System.Management.Automation/engine/parser/tokenizer.cs@L4612-L5081`) and the parser consumes them (`PipelineChainRule`) | E1 comment vs E1 code | RESOLVED | rule 1: code beats comments; the doc comment is stale. | docs-out/02-language/02.1-tokenizer.md (§6.1) |
| CON-003 | `TokenKind.Bxor` doc comment says `-xor` (`src/System.Management.Automation/engine/parser/token.cs@L256-L258`) | `s_tokenText[Bxor]` is `-bxor` and the operator table maps `bxor` to `Bxor` (`tokenizer.cs@L657-L693`) | E1 comment vs E1 code | RESOLVED | code beats comments; typo in comment. | docs-out/02-language/TOKEN-CATALOG.md |
