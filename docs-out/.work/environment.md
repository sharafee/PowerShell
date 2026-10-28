# Environment preflight (section 2)

| Item | Result |
|---|---|
| OS | Linux 6.18.44 x86_64 (cloud container), 4 CPU, 15 GB RAM |
| git | /usr/bin/git |
| rg | /usr/bin/rg |
| dotnet | **MISSING** (global.json requires SDK 10.0.403) |
| pwsh | **MISSING** |
| powershell.exe | MISSING |
| cloc / ctags | MISSING |
| python3 | 3.13.17 |
| node | v22 (/opt/node22) |
| mmdc (Mermaid CLI) | MISSING (Mermaid blocks: syntax lint only) |
| Git state | single-branch clone, not shallow, 4 commits, no tags, remote `origin` = private fork, no `upstream` |

## Run parameters (owner answered in session)
- REPO_ROOT=/home/user/PowerShell, OUT_DIR=docs-out, SCRATCH_DIR=../ps-scratch (unused: nothing to build)
- TARGET_PROFILE=P-FAITHFUL, DOC_LANGUAGE=en, FA_DIGEST=false
- **ALLOW_STATIC_ONLY=true** (owner decision; hard stop 2.8a/d waived). Consequences: every doc `run_verification: none`, banner STATIC-ONLY, gate 9 WAIVED, acceptance status capped at CONDITIONAL.
- Output: docs-out/ inside repo, committed and pushed to branch `claude/repo-review-explanation-22f3xr`, no PR.
- Roslyn extraction impossible -> rg/python regex extraction, all counts `APPROX`.
