# Decisions made while documenting

| ID | Decision | Rationale / evidence |
|---|---|---|
| D-001 | `ALLOW_STATIC_ONLY=true`. | Owner decision in session: no .NET SDK / `pwsh` on host; install not authorized (section 2 item 5). Run is STATIC-ONLY; gate 9 `WAIVED`; acceptance capped at `CONDITIONAL`. |
| D-002 | Tool language is Python 3 (tools in `docs-out/tools/`). | Section 2 item 1 preference (a) dotnet, (b) pwsh are unavailable on the host (`.work/environment.md`); (c) Python 3.13 is present. |
| D-003 | Pin = commit `523031e0af7fa960441734e6cacdf9e927d81619` (HEAD at run start). `validate-refs` checks `git diff --name-only <pin> HEAD -- . ':!docs-out'` is empty instead of `HEAD == pin`. | The study commits `docs-out/` on top of the pin, so HEAD necessarily moves; the source tree must stay identical (rule 3, gate 6g, gate 13). |
| D-004 | Version pin `v7.6.9` derived from commit `d4d786f` message "Import PowerShell v7.6.9" and `CHANGELOG/7.6.md` first entry `[7.6.9]`; `global.json` SDK 10.0.403. | Section 2 item 2 fallback order (no tags, no history). |
| D-005 | No `upstream` remote: "fork base pinned locally via version metadata"; no drift analysis possible, so `00-overview/fork-drift.md` is not produced. | Section 2 item 3; `git remote -v` shows only `origin`. |
| D-006 | C# structure is extracted by an own scanner (`tools/csscan.py`) not Roslyn; every count is `APPROX`. Quality cross-check: type declaration count differs from an independent `rg` regex count by <3% (see Phase 0 notes in `00-overview/repo-census.md`). | Section 5.1 item 2. |
| D-007 | Localized `.resx` copies (13 cultures) are excluded from `resources.json`; only neutral resources are catalogued. | Localized files duplicate the keys; counted separately in `repo-census.md`. |
| D-008 | Tier A list (106 C# files) is path-rule based (`tools/p0_extract.py::TIER_A`): `engine/parser`, `engine/runtime`, `engine/interpreter`, `engine/lang`, `LanguagePrimitives.cs`, parameter binders, command processors, scope/variable storage, command discovery/search, pipeline types. | Section 4.1 Tier A list read against the real tree. |
| D-009 | The interpreter lives in `src/System.Management.Automation/engine/interpreter/` (38 files). | Closes hint C4 of Appendix C; confirmed by directory listing. |
| D-010 | Documents are committed to branch `claude/repo-review-explanation-22f3xr` per phase; no PR. | Owner answer in session. |
| D-011 | `DotnetRuntimeMetadata.json` channel `9.0.1xx-preview6` is inconsistent with `sdkImageVersion` `10.0.403`; `global.json` + `PowerShell.Common.props` (net10.0) are taken as authoritative for the pin. | Observed in the file; left unresolved because the file is only build metadata (see external-dependencies.md). |
