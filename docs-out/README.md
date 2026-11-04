# PowerShell v7.6.9 architecture study (static-only) — index

Pin: version `v7.6.9`, commit `523031e` (`.work/pin.json`). STATIC-ONLY run: nothing was built or executed; behavior claims are labelled `FACT-SRC` / `INFERENCE` / `UNVERIFIED` (see `VERIFICATION-BACKLOG.md`). Progress: `PROGRESS.md`. Decisions: `DECISIONS.md`. Contradictions: `CONTRADICTIONS.md`. Glossary: `GLOSSARY.md`.

## Reading order for the language core (`02-language/`)

1. [00-pipeline-map.md](02-language/00-pipeline-map.md) → [STAGE-CONTRACTS.md](02-language/STAGE-CONTRACTS.md) → [LIFECYCLE-script-execution.md](02-language/LIFECYCLE-script-execution.md) → [CALL-GRAPHS.md](02-language/CALL-GRAPHS.md)
2. Front end: [02.1-tokenizer.md](02-language/02.1-tokenizer.md), [TOKEN-CATALOG.md](02-language/TOKEN-CATALOG.md), [02.2-parser.md](02-language/02.2-parser.md), [GRAMMAR.ebnf.md](02-language/GRAMMAR.ebnf.md), [ERROR-CATALOG.md](02-language/ERROR-CATALOG.md), [02.3-ast.md](02-language/02.3-ast.md), [AST-CATALOG.md](02-language/AST-CATALOG.md), [02.4-semantic-analysis.md](02-language/02.4-semantic-analysis.md)
3. Back end: [02.5-compiler-and-engine.md](02-language/02.5-compiler-and-engine.md), [COMPILATION-MAP.md](02-language/COMPILATION-MAP.md), [IR-SPEC.md](02-language/IR-SPEC.md), [TIERING-POLICY.md](02-language/TIERING-POLICY.md), [INSTRUCTION-SET.md](02-language/INSTRUCTION-SET.md), [EQUIVALENCE-SPEC.md](02-language/EQUIVALENCE-SPEC.md)
4. Semantics: [02.6-types-and-operators.md](02-language/02.6-types-and-operators.md), [OPERATOR-TABLE.md](02-language/OPERATOR-TABLE.md), [CONVERSION-RULES.md](02-language/CONVERSION-RULES.md), [BINDER-CATALOG.md](02-language/BINDER-CATALOG.md), [RUNTIME-OPERATIONS.md](02-language/RUNTIME-OPERATIONS.md), [SCOPE-AND-VARIABLES.md](02-language/SCOPE-AND-VARIABLES.md), [SCRIPT-BLOCKS.md](02-language/SCRIPT-BLOCKS.md), [execution-context-and-session-state.md](03-runtime/execution-context-and-session-state.md)
5. Synthesis: [LANGUAGE-SPEC-DRAFT.md](02-language/LANGUAGE-SPEC-DRAFT.md), [SEMANTIC-QUIRKS.md](02-language/SEMANTIC-QUIRKS.md), [INTERPRETER-DESIGN-SPACE.md](02-language/INTERPRETER-DESIGN-SPACE.md), [02.7-language-features.md](02-language/02.7-language-features.md), [HOWTO-extend-language.md](02-language/HOWTO-extend-language.md), [02.8-language-tooling.md](02-language/02.8-language-tooling.md), [new-language-design-canvas.md](09-synthesis/new-language-design-canvas.md)
6. Evidence and verification: [REFERENCE-TEST-CORPUS.md](02-language/REFERENCE-TEST-CORPUS.md), [GOLDEN-SAMPLES.md](02-language/GOLDEN-SAMPLES.md) (empty), [ORACLE-PROTOCOL.md](02-language/ORACLE-PROTOCOL.md) (waived)

## Runtime (`03-runtime/`)

1. Execution: [runspace-and-pipeline.md](03-runtime/runspace-and-pipeline.md) (CF-LCY-001) → [command-discovery-and-invocation.md](03-runtime/command-discovery-and-invocation.md) (CF-DSC-001) → [parameter-binding.md](03-runtime/parameter-binding.md) (CF-BND-001) → [cmdlet-infrastructure.md](03-runtime/cmdlet-infrastructure.md) → [errors-and-diagnostics.md](03-runtime/errors-and-diagnostics.md) (CF-ERR-001)
2. State and types: [execution-context-and-session-state.md](03-runtime/execution-context-and-session-state.md), [extended-type-system.md](03-runtime/extended-type-system.md) (CF-ETS-001), [modules.md](03-runtime/modules.md) (CF-MOD-001), [provider-model.md](03-runtime/provider-model.md)
3. Output and tooling: [formatting-and-output.md](03-runtime/formatting-and-output.md), [help-system.md](03-runtime/help-system.md), [jobs-and-concurrency.md](03-runtime/jobs-and-concurrency.md), [debugger.md](03-runtime/debugger.md), [eventing.md](03-runtime/eventing.md)

## Repository overview (`00-overview/`, `01-repository/`, `10-command-modules/`)

[repo-census](00-overview/repo-census.md), [source-tree-map](00-overview/source-tree-map.md), [project-dependency-graph](00-overview/project-dependency-graph.md), [external-dependencies](00-overview/external-dependencies.md), [layered-architecture](00-overview/layered-architecture.md), [build-system](01-repository/build-system.md), [ci-cd-and-packaging](01-repository/ci-cd-and-packaging.md), [coding-standards](01-repository/coding-standards.md), [command module families](10-command-modules/_index.md).

## Data and tools

`data/` holds the extracted datasets (all `APPROX`, see `data/README.md`); `tools/` holds the extraction and generator scripts (`gen_T21.py` … `gen_coord.py`, `expand_refs.py`, `consist.py`, `numbers.py`, `coordinator.py`); `.work/` holds notes, claims, ledgers and per-task proposals.
