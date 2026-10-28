# Planned document map (IDs and paths; forward links to these are allowed before the file exists)

Paths are relative to `docs-out/`. Link with relative paths from your document. Document IDs below are fixed; do not invent others for these documents.

## 00-overview / 01-repository (coordinator)
`00-overview/{repo-census,source-tree-map,project-dependency-graph,external-dependencies,layered-architecture,study-summary}.md`, `01-repository/{build-system,ci-cd-and-packaging,coding-standards}.md`

## 02-language (Phase 2)
| ID | Path | Task |
|---|---|---|
| LANG-MAP-001 | 02-language/00-pipeline-map.md | coordinator |
| LANG-TOKENIZER-001 | 02-language/02.1-tokenizer.md | T21 |
| LANG-TOKCAT-001 | 02-language/TOKEN-CATALOG.md | T21 |
| LANG-PARSER-001 | 02-language/02.2-parser.md | T22 |
| LANG-GRAMMAR-001 | 02-language/GRAMMAR.ebnf.md | T22 |
| LANG-ERRCAT-001 | 02-language/ERROR-CATALOG.md | T22 |
| LANG-AST-001 | 02-language/02.3-ast.md | T23 |
| LANG-ASTCAT-001 | 02-language/AST-CATALOG.md | T23 |
| LANG-SEMANTIC-001 | 02-language/02.4-semantic-analysis.md | T24 |
| LANG-ENGINE-001 | 02-language/02.5-compiler-and-engine.md | T25 |
| LANG-COMPMAP-001 | 02-language/COMPILATION-MAP.md | T25 |
| LANG-IR-001 | 02-language/IR-SPEC.md | T25 |
| LANG-BINDERCAT-001 | 02-language/BINDER-CATALOG.md | T26 |
| LANG-INSTR-001 | 02-language/INSTRUCTION-SET.md | T27 |
| LANG-TIERING-001 | 02-language/TIERING-POLICY.md | T27 |
| LANG-EQUIV-001 | 02-language/EQUIVALENCE-SPEC.md | T27 |
| LANG-TYPES-001 | 02-language/02.6-types-and-operators.md | T28 |
| LANG-OPTABLE-001 | 02-language/OPERATOR-TABLE.md | T28 |
| LANG-CONV-001 | 02-language/CONVERSION-RULES.md | T28 |
| LANG-SCOPE-001 | 02-language/SCOPE-AND-VARIABLES.md | T29 |
| LANG-FEATURES-001 | 02-language/02.7-language-features.md | T210 |
| LANG-HOWTO-001 | 02-language/HOWTO-extend-language.md | T210 |
| LANG-TOOLING-001 | 02-language/02.8-language-tooling.md | T211 |
| LANG-STAGES-001 | 02-language/STAGE-CONTRACTS.md | coordinator |
| LANG-CALLG-001 | 02-language/CALL-GRAPHS.md | coordinator |
| LANG-LIFECYCLE-001 | 02-language/LIFECYCLE-script-execution.md | coordinator |
| LANG-SPEC-001 | 02-language/LANGUAGE-SPEC-DRAFT.md | coordinator |
| LANG-QUIRKS-001 | 02-language/SEMANTIC-QUIRKS.md | coordinator |
| LANG-DESIGNSPACE-001 | 02-language/INTERPRETER-DESIGN-SPACE.md | coordinator |
| LANG-GOLDEN-001 | 02-language/GOLDEN-SAMPLES.md | coordinator |
| LANG-ORACLE-001 | 02-language/ORACLE-PROTOCOL.md | coordinator |
| LANG-TESTCORPUS-001 | 02-language/REFERENCE-TEST-CORPUS.md | coordinator |

## 03-runtime (Phase 3)
| ID | Path | Task |
|---|---|---|
| RT-PIPELINE-001 | 03-runtime/runspace-and-pipeline.md | T31 |
| RT-DISCOVERY-001 | 03-runtime/command-discovery-and-invocation.md | T32 |
| RT-CMDLET-001 | 03-runtime/cmdlet-infrastructure.md | T33 |
| RT-BIND-001 | 03-runtime/parameter-binding.md | T33 |
| RT-CONTEXT-001 | 03-runtime/execution-context-and-session-state.md | T29 |
| RT-PROVIDER-001 | 03-runtime/provider-model.md | T34 |
| RT-ETS-001 | 03-runtime/extended-type-system.md | T35 |
| RT-FORMAT-001 | 03-runtime/formatting-and-output.md | T36 |
| RT-MODULES-001 | 03-runtime/modules.md | T37 |
| RT-ERRORS-001 | 03-runtime/errors-and-diagnostics.md | T38 |
| RT-JOBS-001 | 03-runtime/jobs-and-concurrency.md | T39 |
| RT-DEBUGGER-001 | 03-runtime/debugger.md | T39 |
| RT-EVENTING-001 | 03-runtime/eventing.md | T39 |
| RT-HELP-001 | 03-runtime/help-system.md | T36 |

## 04-hosting .. 08-engineering, 09-synthesis, 10-command-modules
`HOST-ABSTRACTION-001` 04-hosting/host-abstraction.md; `HOST-CONSOLE-001` 04-hosting/console-host.md; `HOST-SDK-001` 04-hosting/sdk.md; `REM-PSRP-001` 05-remoting/psrp-protocol.md; `REM-TRANSPORT-001` 05-remoting/transports.md; `REM-CLIXML-001` 05-remoting/serialization-clixml.md; `REM-JEA-001` 05-remoting/jea.md; `PLAT-SPLIT-001` 06-platform/windows-unix-split.md; `PLAT-NATIVE-001` 06-platform/native-interop.md; `SEC-LANGMODE-001`, `SEC-EXECPOL-001`, `SEC-AMSI-001`, `SEC-ENFPTS-001`, `SEC-THREAT-001`, `SEC-BLUEPRINT-001` in 07-security/; `ENG-TEST-001`, `ENG-PROC-001`, `ENG-L10N-001` in 08-engineering/; `SYN-*` in 09-synthesis/; `CMD-<ASSEMBLY>-001` in 10-command-modules/<AssemblyName>.md.

## Lessons (section 18 format, machine-extracted by `tools/lessons.py`)
Each lesson is one list item: `- **LSN-<DOCSHORT>-<nn>** [REPLICATE|ADAPT|REDESIGN|AVOID] (area: NLD-<AREA>) <lesson text> Evidence: <ref>. DEV: DEV-<AREA>-<NNN>` — the `DEV:` part only for REDESIGN/AVOID. `<AREA>` is one of LEX, GRM, OP, TYP, SCP, ERR, PIP, MOD, CMD, SEC, TOOL, RUN. `DOCSHORT` is a 2-8 letter code unique per document (e.g. TOK, PARSER, AST, SEM, ENG, IR, TIER).
