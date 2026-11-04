---
id: LANG-GOLDEN-001
title: Golden samples
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

# Golden samples

> STATIC-ONLY — **no golden samples exist** (`data/golden/` is empty by owner decision, backlog VB-001). This file is the index the study prompt requires; it states the empty state and defines the format so samples can be added when a host with `pwsh` is available. No `GS-*` identifier is used anywhere in this study.

## 1. Purpose and scope [SPEC]

A golden sample is a script snippet with the observable result recorded from a real `pwsh` run (token kinds, AST node types, output objects, error ids, `$?`). Samples turn `UNVERIFIED` behavior claims into verified ones and feed the conformance corpus of the new shell.

## 2. Source map

Not applicable (no data).

## 3. Responsibilities and non-responsibilities

Index and format only. Execution of samples is specified in [ORACLE-PROTOCOL.md](ORACLE-PROTOCOL.md).

## 4. Key types and contracts [IMPL]

Planned record (JSON, one file per sample under `data/golden/`): `id` (`GS-<AREA>-<NNN>`, assigned only when a sample is created from a run), `snippet`, `pwsh_version`, `commit`, `tokens`, `ast_node_types`, `output` (typed, serialized), `errors` (ids and messages), `question_mark`, `streams`, `notes`.

## 5. Data model

Coverage report (computed when samples exist): per document claim marked `UNVERIFIED`, whether a sample covers it. Today: 0 samples, coverage 0%; every behavior statement in the study is `FACT-SRC` (read) or `INFERENCE`/`UNVERIFIED`.

## 6. Control flow

Not applicable.

## 7. Algorithms

Not applicable.

## 8. Observable behavior [SPEC]

Not applicable: no samples.

## 9. Error handling and edge cases

A sample whose run depends on the host (culture, OS) must record those inputs.

## 10. Concurrency and threading

Not applicable.

## 11. Extension points and customization hooks

Samples are added by the oracle harness; claims are re-labelled by `tools/consist.py check-claims` once a sample id is attached.

## 12. Dependencies

[ORACLE-PROTOCOL.md](ORACLE-PROTOCOL.md), [SEMANTIC-QUIRKS.md](SEMANTIC-QUIRKS.md), [REFERENCE-TEST-CORPUS.md](REFERENCE-TEST-CORPUS.md).

## 13. Performance notes

Not applicable.

## 14. Security considerations (mandatory)

Running snippets executes code; the protocol requires a scratch copy and no network. No security surface in this index.

## 15. Enterprise considerations

Not applicable.

## 16. Tests

The existing repository tests are the interim behavior evidence ([REFERENCE-TEST-CORPUS.md](REFERENCE-TEST-CORPUS.md)).

## 17. Design decisions and trade-offs

Owner decision: static-only run (D-001..D-011, VB-001).

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-GOLD-01** [REPLICATE] (area: NLD-TOOL) Keep an oracle-recorded conformance corpus as the acceptance test of the new interpreter. Evidence: `test/powershell/Language/Parser/` (the repository's own language tests, see REFERENCE-TEST-CORPUS).

## 19. Open questions / UNVERIFIED

All samples are future work (VB-001).

Verification: `data/golden/` was found empty at the start of the run.
