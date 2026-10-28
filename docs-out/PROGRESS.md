# PROGRESS (resumable checklist, rule 4)

Run mode: STATIC-ONLY (`ALLOW_STATIC_ONLY=true`). Branch `claude/repo-review-explanation-22f3xr`. Pin v7.6.9 / `523031e`. Resume from this file and `.work/`.

## Phases
| Phase | Status | Notes |
|---|---|---|
| Preflight (section 2) | done | `.work/environment.md`, `.work/pin.json`, DECISIONS D-001..D-011 |
| 0 Recon, pinning, tooling | done | datasets in `data/`, tools in `tools/`, registers, glossary, census, dependency graph, source-tree map, 297 folder cards + 40 project cards (generated; annotation overlay pending) |
| 1 Repository map | todo | layered-architecture, build-system, ci-cd-and-packaging, coding-standards |
| 2 Language pipeline | in progress | wave 1: T21 T22 T23 T24 T25 T27 |
| 3 Runtime | todo | |
| 4 Hosting/SDK/remoting/platform/command modules | todo | |
| 5 Security | todo | |
| 6 Engineering | todo | |
| 7 Synthesis | todo | |
| 8 Verification/consolidation | todo | oracle waived (VB-001) |
| 9 FA digest | skipped | `FA_DIGEST=false` |

## Task IDs
T21 tokenizer | T22 parser/grammar/errors | T23 AST | T24 semantic | T25 compiler/IR | T26 binders+runtime ops | T27 interpreter+tiering | T28 types/operators/conversion | T29 scope/variables+execution context | T210 language features+HOWTO | T211 tooling | T31..T39 runtime subsystems (see `.work/DOC-MAP.md`).

## Document checklist
Maintained as agents report; see `.work/reports/`.
