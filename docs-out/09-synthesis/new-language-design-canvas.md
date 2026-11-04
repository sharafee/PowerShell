---
id: SYN-CANVAS-001
title: New-language design canvas (skeleton)
kind: catalog
tier: B
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: []
mirror_cards: []
generated_from: [data/lessons.json]
---

# New-language design canvas (skeleton)

> STATIC-ONLY. Skeleton created in Phase 2 so that forward links resolve; Phase 7 fills the empty cells. Lesson counts per area and verdict are `GENERATED` by `docs-out/tools/gen_coord.py` from `data/lessons.json` (gate 6d compares them with the verdict counts of [SEMANTIC-QUIRKS](../02-language/SEMANTIC-QUIRKS.md) and the guidance sections).

## 1. Canvas rows

| Row | Area | REPLICATE | ADAPT | REDESIGN | AVOID | Baseline decision | Approved deviation | Status |
|---|---|---:|---:|---:|---:|---|---|---|
| NLD-LEX | Lexical structure and tokenizer modes | 4 | 2 | 0 | 1 | | | open |
| NLD-GRM | Grammar, AST and semantic checks | 10 | 6 | 0 | 4 | | | open |
| NLD-OP | Operators and precedence | 7 | 4 | 0 | 0 | | | open |
| NLD-TYP | Types, conversions and values | 6 | 2 | 0 | 0 | | | open |
| NLD-SCP | Scopes, variables and sessions | 11 | 3 | 0 | 0 | | | open |
| NLD-ERR | Errors, streams and recovery | 7 | 0 | 0 | 0 | | | open |
| NLD-PIP | Pipeline and output | 3 | 0 | 0 | 0 | | | open |
| NLD-MOD | Modules and packaging | 0 | 1 | 0 | 0 | | | open |
| NLD-CMD | Commands and parameter binding | 3 | 2 | 0 | 3 | | | open |
| NLD-SEC | Security, sandboxing and language modes | 6 | 5 | 0 | 5 | | | open |
| NLD-TOOL | Tooling, extension and testing | 12 | 9 | 0 | 1 | | | open |
| NLD-RUN | Execution strategy and runtime | 9 | 11 | 0 | 6 | | | open |
| **total** | | **78** | **45** | **0** | **20** | | | |

Verification: counts rendered from `data/lessons.json` (extracted from the guidance sections by `tools/coordinator.py lessons`); the other columns are intentionally empty until Phase 7.

