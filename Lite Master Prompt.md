# PowerShell Interpreter Study — Lite Master Prompt (static analysis only)

> **Usage.** Run Claude Code inside the root of a local clone of the PowerShell repository (MIT license). Put this file in the root and say: "Read PowerShell-Architecture-Analysis-Prompt-LITE.md fully, then execute it."
> **This run never builds, installs, or executes anything from the repository.** It only reads source and writes documents. No .NET SDK and no `pwsh` are required.

## Run parameters (defaults; the owner may override in the invoking message)

| Parameter | Default | Meaning |
|---|---|---|
| `REPO_ROOT` | current directory | root of the local clone |
| `OUT_DIR` | `docs-out` | output tree (the only place you may write) |
| `DOC_LANGUAGE` | `fa` | language of prose in authored documents (Persian). Identifiers, file paths, code, type and method names always stay in Latin script exactly as in source. Use `en` for English. |

---

## 0. ROLE AND GOAL

You are a principal language-runtime architect doing an evidence-based study of how PowerShell tokenizes, parses, represents, and executes scripts.

**Why this study exists.** The owner is building a personal interpreter and CLI named **MicroteamShell** (company **Microteam**, script extension **`.mtsh`**, written in C#/.NET, solution format `.slnx`, installed on Windows). It must behave like PowerShell's *language* (tokenizer, parser, AST, pipeline, functions, `try/catch/finally`, scopes, parameter binding, errors and streams). It does **not** need to run Windows commands, replicate Windows-specific cmdlets, or be enterprise-grade. It is a personal platform for personal projects.

**Your output** must let a C# developer who has never opened the PowerShell source implement MicroteamShell's language core and engine from your documents alone.

You do **not** write the implementation. You do **not** explain individual cmdlets line by line.

---

## 1. NON-NEGOTIABLE RULES

1. **Evidence only.** Every factual claim cites a repo-relative path, a type/method name, and a line range: `src/System.Management.Automation/engine/parser/Parser.cs::Parser.IfStatementRule@L1200-L1290`. If you did not read it, do not state it.
2. **Never trust memory or this prompt's file names.** Every path, class, or method named in this prompt (including section 4) is only a **hint**. Discover the real layout with `rg`, `find`/`ls`, and reading. If a hint is wrong, record the real answer in `docs-out/DECISIONS.md`.
3. **Three labels, exactly one per factual statement** (inline for non-trivial claims, or per block when a whole block shares it):
   - `FACT-SRC` — read directly in the pinned source (including test assertions).
   - `INFERENCE` — your reasoning about *why* or about unread connections.
   - `UNVERIFIED` — plausible but not confirmed in source; add it to `docs-out/VERIFICATION-BACKLOG.md`.
   Because nothing is executed in this run, **behavior claims are `FACT-SRC` only when a source or a test in the repo shows it**; otherwise `UNVERIFIED`.
4. **Pin once.** Phase 0 writes `docs-out/.work/pin.json` (version, commit hash, how derived). The clone may be shallow with no tags; derive the version from: `git describe --tags` -> `git tag --points-at HEAD` -> last commit message -> `PowerShell.Common.props` / `DotnetRuntimeMetadata.json` / `global.json` / newest `CHANGELOG/*.md`. Do not rely on `git log` or `git blame` for analysis. Every document's front matter copies the pin; never retype it differently.
5. **Read-only.** Never modify files outside `OUT_DIR`. Never run `dotnet`, `msbuild`, `pwsh`, `powershell.exe`, installers, or repo scripts. Allowed tools: `git` (read-only commands), `rg`, `find`, `wc`, `sed -n`, and your own small scripts in `docs-out/tools/` (Python 3 preferred; else shell) that only read files. At the end run `git status --porcelain` and confirm only `OUT_DIR` changed.
6. **Self-resumable.** Maintain `docs-out/PROGRESS.md` (phases, task IDs, status, open questions). Update after every document. If context is lost, resume from `PROGRESS.md` and `docs-out/.work/`.
7. **Read large files in windows** of at most 300 lines. After each window append notes (member names, line ranges, open questions) to `docs-out/.work/notes/<flattened-path>.md`. Re-read instead of trusting earlier context.
8. **Counts and tables come from scripts.** Anything countable (token kinds, AST classes, enum members, operators, keywords, error resource keys) is extracted by a script into `docs-out/data/` and rendered into documents from that data. Never hand-type a catalog or a count. If a script uses regex, label its output `APPROX` and say so in the document.
9. **Completeness over brevity.** When a catalog promises "every X", list every X. If too large, split into numbered parts with an index.
10. **No clarification questions.** Make the best evidence-based decision, record it in `DECISIONS.md`, continue. If the repo cannot be found or read, write `docs-out/BLOCKED.md` (cause, evidence, exact fix) and stop.
11. **Describe in your own words.** Short code excerpts (max ~15 lines) only when they are the clearest evidence. Do not paste whole methods. (The code is MIT-licensed, so the owner may later reuse it with the copyright notice; your documents still describe behavior and design so they are usable without the source.)
12. **Contradictions are recorded, never silently resolved.** If two statements disagree (between documents, between a document and the source, between a source reading and a test), add `CON-###` to `docs-out/CONTRADICTIONS.md` with both statements, locations, and the resolution with evidence.
13. **Conditional compilation.** Types and members may exist only under `#if` symbols (platform, framework, features). Mark platform-conditional items; for MicroteamShell, **Windows-only code paths are allowed to inform the study, but flag them** so the owner can drop them.
14. **One verdict per lesson.** Every subsystem document ends with "Guidance for MicroteamShell": each lesson carries exactly one verdict:
    - `REPLICATE` — copy observable behavior and the essential mechanism.
    - `ADAPT` — copy observable behavior with a simpler/different mechanism (state why).
    - `AVOID` — omit this; say what (if anything) replaces it.
    Default for language-core behavior: `REPLICATE`. A departure from PowerShell's observable behavior is only a **proposal**, never a decision; the owner decides.

---

## 2. SCOPE CLASSES (default; the owner may edit `FEATURE-MATRIX.md`)

| Class | Features |
|---|---|
| `CORE` (documented to rebuild-grade) | tokenizer (command/expression modes), parser, AST, semantic checks, variables and scopes, operators and conversions (`LanguagePrimitives`), flow control (`if/elseif/else`, loops, `switch`, `break/continue/return/throw`), `try/catch/finally`, `trap`, functions/filters/advanced functions (`param`, `[CmdletBinding()]`, `begin/process/end`), pipeline, command discovery, parameter binding, cmdlet base lifecycle, errors and streams, script file execution, dot-sourcing, splatting, redirection |
| `EXTENDED` (architecture + headline behavior only) | classes and enums, script modules and manifests, providers, Extended Type System basics, formatting/output, host abstraction and console REPL, tab completion, jobs, ternary / null-coalescing / pipeline-chain operators |
| `OUT-OF-SCOPE` (one paragraph each, nothing more) | remoting (PSRP, WSMan, SSH, JEA), DSC/configuration, workflows, CIM/WMI/COM adapters, AMSI, execution policy, security/sandboxing, debugger, eventing, help system, updatable help, telemetry, build/CI/packaging of PowerShell itself |

Do **not** study the `OUT-OF-SCOPE` areas beyond a short note in `FEATURE-MATRIX.md` (what it is, where it lives in the tree).

---

## 3. PHASES (execute in order; independent work may run in parallel under section 6)

### Phase 0 — Reconnaissance and tooling (small)

- Read `README.md`, `global.json`, `PowerShell.Common.props`, `DotnetRuntimeMetadata.json`, newest `CHANGELOG/*.md`, and top-level folder layout.
- Write `.work/pin.json` (rule 4) and `docs-out/DECISIONS.md`.
- Locate the real paths of every file in section 4 and write `docs-out/00-overview/source-map.md`: path, LOC (`wc -l`), role, scope class. Mark each file `read-all` (Tier A: whole file will be read), `read-key` (key methods only), or `inventory` (declarations only).
- Create `docs-out/.work/files-ledger.csv` with columns `path, loc, tier, ranges_read, doc_ids, status`.
- Build the extraction scripts (section 5) and run them. Outputs go to `docs-out/data/`.
- Create `docs-out/GLOSSARY.md` (section 7) and empty `CONTRADICTIONS.md`, `VERIFICATION-BACKLOG.md`, `FEATURE-MATRIX.md` (rows from section 2).
- Deliverables: `00-overview/source-map.md`, `.work/*`, `data/*`, registers.

### Phase 1 — Tokenizer

Document purpose, entry points, key types and responsibilities, inputs/outputs, invariants, error handling.

- **Tokenizer modes:** how the parser selects *command* vs *expression* mode, what changes between them (barewords, `-Name` parameters vs minus operator, generic tokens such as `C:\a\b.txt` or `*.log`), how the mode is switched back. Provide a **mode-transition table**: trigger -> mode -> why, each with evidence.
- **Token catalog:** every token kind and flag (from `data/`), keyword table including contextual keywords, operator table (symbol and dash operators), character-class tables.
- **Lexical rules:** numbers (radix, suffixes, multipliers like `kb`), variables (`$x`, `${x y}`, scope prefixes, `$using:`, splatting `@x`), single/double-quoted strings, expandable strings and nested sub-expressions, here-strings (opening/closing rules), escapes, comments (line, block, help comments), backtick line continuation, redirection tokens, newline/terminator sensitivity, member-name vs operator ambiguity.
- **Position tracking:** how extents and line/column are computed.
- Mapping: token kind -> parser rules that consume it.
- Deliverables: `02-language/02.1-tokenizer.md`, `02-language/TOKEN-CATALOG.md`.

### Phase 2 — Parser

- **Strategy:** recursive descent? lookahead? token pushback? How it decides command vs expression context, how it resolves ambiguity, **how newlines and `;` end statements**, how a newline inside `()`, `{}` or after an operator continues an expression.
- **Production table:** `Production | Method | File@Lines | Tokens consumed | AST produced | Error IDs` for every parser method (seed from `data/parser-methods.*`, then verify by reading).
- **Grammar:** reconstruct an EBNF-style grammar *derived strictly from the parser code* (statements, pipelines, commands and command elements, expressions, precedence and associativity of every operator, attributes, type literals, hashtables, script blocks, param blocks, named blocks, `try/catch/finally`, `trap`, `switch` including its flags, `function`/`filter`, loops with labels, `using`, splatting, redirection). Every production links to its parser method.
- **Operator precedence table** extracted from the parser (not from documentation): operator -> precedence level -> associativity -> parser method.
- **Error recovery:** what the parser returns when errors exist (partial AST? skipped tokens?), synchronization points, and the **error catalog** (parse error IDs, resource keys, triggering conditions) rendered from `data/`.
- **Public API:** `ParseInput`/`ParseFile`/`Tokenize` entry points and what they return.
- Deliverables: `02-language/02.2-parser.md`, `02-language/GRAMMAR.ebnf.md`, `02-language/OPERATOR-TABLE.md`, `02-language/ERROR-CATALOG.md`.

### Phase 3 — AST and semantic checks

- **Node catalog:** every AST class from `data/ast-hierarchy.*`: base type, children (fields/properties), which parser production creates it, which visitors/compiler paths consume it. Table: `NodeType | Base | Children | Created by | Consumed by`.
- Visitor infrastructure (interfaces, dispatch, default visitors), `Copy`, `Find/FindAll`, extents, parent links, constant/safe-value evaluation.
- **Semantic checks:** table `Check | Where | Trigger | Error ID | Runs when`, covering at least: break/continue/return placement, duplicate parameters, attribute validation, invalid assignment targets, variable analysis (scope prefixes, `using:`), type resolution.
- Deliverables: `02-language/02.3-ast.md`, `02-language/AST-CATALOG.md`, `02-language/02.4-semantic-analysis.md`.

### Phase 4 — Execution model

Explain how a parsed script runs, focusing on **what MicroteamShell must reproduce**.

- **Pipeline of execution:** from `ScriptBlock` creation to output, as a Mermaid sequence diagram naming every class/method touched. (`LIFECYCLE-script-execution.md`.)
- **Compile vs interpret:** how PowerShell turns AST into executable form (expression trees, lazy compile, caching, the interpreter fallback) and **the rule that chooses between them** (modes, thresholds, constants, with their source names). Then a short, labelled `INFERENCE` section: a simple **tree-walking evaluator over the AST** is a valid starting point for MicroteamShell; list which observable behaviors a tree-walker must preserve (results, streams, errors, positions, variable visibility).
- **Per node type:** table `NodeType -> how it is compiled/executed` (`COMPILATION-MAP.md`), derived from the compiler visitor.
- **Flow control:** how `break/continue/return/throw`, `try/catch/finally`, `trap`, and loop labels are implemented (exceptions vs flags vs jumps), including the interaction of `finally` with `return`/`break`.
- **Statement output rule:** how every statement can emit output into the pipeline and how that output is collected, and how `return` interacts with it.
- **Dynamic binding:** list each binder (member access, invoke, convert, binary/unary operations, index, etc.) and the PowerShell-specific rules it implements (method overload resolution, argument conversion, property lookup). Table `Binder | Operation | Where created` from `data/`.
- Deliverables: `02-language/02.5-compiler-and-engine.md`, `COMPILATION-MAP.md`, `BINDER-CATALOG.md`, `LIFECYCLE-script-execution.md`.

### Phase 5 — Runtime core

For each subsystem use the template in section 8. Mark scope class in front matter.

- **Types and operators:** `LanguagePrimitives` conversion pipeline as an **ordered algorithm with a decision table**; comparison and equality (left-operand-driven typing, case sensitivity variants); truthiness; numeric promotion; string-to-number parsing; collection unrolling; `$null` handling; array behavior of `-eq/-like/-match`; regex operators and `$Matches`. Deliverables: `02.6-types-and-operators.md`, `CONVERSION-RULES.md`.
- **Scopes and variables:** scope chain, read/write rules, `global/script/local/private/using` prefixes, variable options (ReadOnly/Constant/AllScope/Private), automatic variables (`$_`, `$?`, `$args`, `$input`, `$PSItem`, `$LASTEXITCODE`, `$Error`, `$MyInvocation`, ...), preference variables, dot-sourcing behavior, closures. Deliverable: `SCOPE-AND-VARIABLES.md`.
- **Command discovery and invocation:** resolution order, command types (alias/function/filter/cmdlet/script/application), caching, command processors (cmdlet, script block, external application argument passing). Deliverable: `03-runtime/command-discovery-and-invocation.md`.
- **Parameter binding:** metadata construction and the **binding algorithm as ordered steps**: named (exact/alias/prefix), positional, pipeline by value, pipeline by property name, `ValueFromRemainingArguments`, parameter-set resolution (**decision table**), mandatory handling, type coercion, validation and transformation attributes, common parameters, switch parameters, splatting. Deliverable: `03-runtime/parameter-binding.md`.
- **Pipeline processor:** `begin/process/end` lifecycle, object flow between stages, streaming vs buffering, `Pipe`, stop/cancellation, `ForEach-Object` / `Where-Object` mechanics (`$_`). Deliverable: `03-runtime/pipeline.md`.
- **Errors and streams:** the six streams, terminating vs non-terminating errors, `ErrorRecord` structure, `$ErrorActionPreference` and `-ErrorAction` semantics, how a non-terminating error becomes terminating, `$?`, `$Error`, `throw`, redirection operators. Deliverable: `03-runtime/errors-and-streams.md`.
- **Cmdlet base lifecycle:** `Cmdlet`/`PSCmdlet`, `BeginProcessing/ProcessRecord/EndProcessing/StopProcessing`, attributes, `Write*` APIs, `ShouldProcess`, dynamic parameters. Deliverable: `03-runtime/cmdlet-infrastructure.md`.
- **Script execution:** how a `.ps1` file is loaded, parsed whole before running, how `param()` at file level binds, `exit` and exit codes, dot-sourcing vs `&`. Deliverable: `03-runtime/script-execution.md`.

### Phase 6 — Extended features (architecture level only)

One short document each, marked `EXTENDED`: classes/enums, script modules and manifests (load, export), host abstraction (`PSHost`, `PSHostUserInterface`) and console REPL basics, providers (contract only), formatting/output (how default output is chosen), tab completion hooks, ternary / null-coalescing / pipeline-chain operators. Include only what MicroteamShell would need to decide whether to implement it.
Deliverable: `04-extended/`.

### Phase 7 — Behavior evidence from repository tests (static substitute for running)

Because nothing is executed, use the repo's own tests as behavior evidence.

- Inventory parser/language tests under `test/powershell/Language/` (and any xUnit parser tests) into `data/tests.*`: file, `Describe/Context/It` names (regex is acceptable; label `APPROX`).
- Write `docs-out/05-corpus/CORPUS-CANDIDATES.md`: **60 to 100 short `.mtsh`-style snippets** (one to five lines each), grouped by feature (tokenizer modes, operators, strings/here-strings, conversions, scopes, functions/param, pipeline, binding, `try/catch/finally`, `switch`, loops, splatting, redirection, errors). For each: ID `CS-<AREA>-<NNN>`, the snippet, the **expected behavior** (taken from a cited test assertion, else marked `UNVERIFIED`), and the rule it exercises. No snippet may invoke Windows-specific commands (use only language constructs and a few core cmdlets: `Write-Output`, `ForEach-Object`, `Where-Object`, `Select-Object`).
- Write `docs-out/tools/verify-with-pwsh.ps1` (**write only, never run**): reads `CORPUS-CANDIDATES.md` snippets and, on a machine that has `pwsh`, dumps tokens, AST node type names, and output/errors per snippet to JSON so the owner can later turn `UNVERIFIED` into verified. It must only parse and run the snippets from the corpus. Add a header comment explaining it was not executed by this run.
- Deliverables: `05-corpus/`, `data/tests.*`, `tools/verify-with-pwsh.ps1`.

### Phase 8 — Synthesis for MicroteamShell

- **`06-synthesis/mtsh-reference-architecture.md`:** proposed solution layout (`Mtsh.slnx`; projects `Mtsh.Language`, `Mtsh.Engine`, `Mtsh.Runtime`, `Mtsh.Cmdlets`, `Mtsh.Host`, `Mtsh.Cli`; dependency direction), and a mapping table `PowerShell component -> MicroteamShell component` with verdict.
- **`06-synthesis/compat-matrix.md`:** every language feature found in the study with: source evidence, scope class, verdict (`REPLICATE | ADAPT | AVOID`), suggested implementation phase (1-4), and difficulty. Proposed deviations from PowerShell are listed in a separate section marked `PROPOSED` with rationale; none is in effect.
- **`06-synthesis/semantic-quirks.md`:** every surprising behavior found (implicit unrolling, comparison coercions, parsing ambiguities, output pollution, etc.) with evidence and verdict.
- **`06-synthesis/implementation-roadmap.md`:** ordered milestones: infrastructure (source text, extents, diagnostics) -> tokenizer -> parser -> AST -> tree-walking evaluator -> scopes -> cmdlet base + parameter binding -> pipeline -> functions and advanced functions -> errors, streams, `try/catch` -> host/REPL -> `.mtsh` file execution. For each milestone: scope, the public C# interfaces to define (signatures only), documents and corpus IDs it relies on, acceptance criteria, risks.
- **`06-synthesis/extension-recipes.md`:** for (a) a new operator, (b) a new statement keyword, (c) a new AST node, (d) a new literal, (e) a new automatic variable, (f) a new type conversion: the ordered list of source places PowerShell changes. Trace one or two existing features end to end and cite evidence.
- **Decision log:** at least 20 notable design decisions found in the code (decision, evidence, consequence, strength, weakness) in `06-synthesis/architecture-decision-log.md`.
- **`06-synthesis/minimum-cmdlets.md`:** the smallest cmdlet set needed to make the language usable (output, pipeline, variables, simple file operations, object helpers), with the base-class features each needs.
- `00-overview/study-summary.md` (written last): counts (rendered from data), top-10 insights, remaining `UNVERIFIED` count.

---

## 4. FILE HINTS (verify; paths may differ in this clone)

Base: `src/System.Management.Automation/`

| Area | Hint | Depth |
|---|---|---|
| Tokens | `engine/parser/token.cs`, `tokenizer.cs` | read-all |
| Parser | `engine/parser/Parser.cs` | read-all |
| AST | `engine/parser/ast.cs`, `Position.cs` | read-all (`ast.cs`: catalog from data, read all constructors/visit methods) |
| Semantic | `engine/parser/SemanticChecks.cs`, `VariableAnalysis.cs`, `TypeResolver.cs`, `ConstantValues.cs` | read-all |
| Compiler | `engine/parser/Compiler.cs` | read-key (every `Visit*` method, flow-control and pipeline emission) |
| Interpreter | the interpreter / light-compiler folder (find via `rg "Instruction"`) | read-key (instruction catalog, tiering rule) |
| Binders | `engine/runtime/Binding/`, `engine/runtime/Operations/` | read-key |
| Engine | `engine/AutomationEngine.cs`, `ExecutionContext.cs`, `CommandDiscovery.cs`, `CommandSearcher` | read-all |
| Processors | `CommandProcessor*.cs`, `ScriptCommandProcessor.cs`, `MshCommandRuntime.cs`, `Pipe.cs`, `PipelineProcessor.cs` | read-all |
| Binding | `ParameterBinderController*.cs`, `ParameterBinderBase.cs`, `CommandParameterInternal*`, metadata classes | read-all |
| Scope | `SessionState*.cs`, scope and variable classes | read-all |
| Conversion | `LanguagePrimitives.cs`, `ErrorPackage.cs` (ErrorRecord) | read-all |
| Cmdlet base | `Cmdlet.cs`, `PSCmdlet.cs`, `InternalCommands.cs` | read-key |
| Host | `PSHost` and `PSHostUserInterface` files | read-key |
| Tests | `test/powershell/Language/` (Parser, Operators, Scripting, flow control, functions) | inventory + cited assertions |

Everything else: `inventory` only (type declarations), no reading beyond what a document needs.

---

## 5. EXTRACTION SCRIPTS (static, no build)

Write small Python scripts in `docs-out/tools/` that **only read** source files and write to `docs-out/data/`. Because no compiler is used, outputs are `APPROX`; each must be cross-checked by reading.

| Output | Content |
|---|---|
| `files.csv` | path, LOC, area, tier |
| `types.json` | type name, kind, namespace, file, line range, base types (regex-based) |
| `enums.json` | every enum with members, notably `TokenKind`, `TokenFlags`, and parser/language enums |
| `ast-hierarchy.json` | classes whose name ends in `Ast` with base class and the properties that are AST-typed |
| `parser-methods.json` | every method in `Parser.cs` and `tokenizer.cs` with line range and the methods it calls (regex call extraction) |
| `tables.json` | keyword, operator, and character-class tables as in source |
| `resources.json` | parser/runtime error resource keys (`.resx`) and the code locations that reference them |
| `visitors.json` | classes implementing AST visitor interfaces |
| `binders.json` | binder classes and where they are instantiated |
| `automatic-variables.json` | automatic and preference variable names and definition sites |
| `tests.json` | test files with `Describe/Context/It` names |

Document each script's header: purpose, inputs, outputs, run command. Every count used in a document is read from these files.

---

## 6. SUBAGENTS

Use subagents for Phases 1-6 (one per topic or subsystem), at most 4 in parallel.

**Each task prompt contains:** task ID, exact source paths, the rules of section 1, the template of section 8, the relevant `data/` files, the output paths it owns, and a definition of done (no `TODO`, all catalogs rendered from `data/`, guidance section with verdicts, Verification line filled).
**Hard limits:** write only own output files and `.work/notes/`; never edit shared files (`PROGRESS.md`, `GLOSSARY.md`, `DECISIONS.md`, `VERIFICATION-BACKLOG.md`, `CONTRADICTIONS.md`, `files-ledger.csv`); never modify source.
**Each returns:** files written, new glossary terms, `UNVERIFIED` items, decisions made, proposed ledger updates (path -> ranges read), and any contradiction found.
**The coordinator** merges reports into the shared files and updates `PROGRESS.md` after each subagent.
Separate **review subagents** re-read each Phase 1-5 document against the source and report discrepancies (they fix nothing in shared files).

---

## 7. GLOSSARY (seed; extend as needed)

Use these words consistently and never use one word for two concepts:

- `tokenize` — text to tokens. `parse` — tokens to AST. `analyze` — AST to checks.
- `compile` — AST to an intermediate executable form. `interpret` — execute an instruction-based form. `tree-walk` — evaluate the AST directly. `execute` — umbrella word, only in lifecycle documents.
- `script block`, `function`, `filter`, `cmdlet`, `command`, `pipeline`, `scope`, `session state`: define once each, with the source types that implement them.

---

## 8. DOCUMENT TEMPLATE

Front matter:

```
---
id: <AREA-TOPIC-NNN>            # e.g. LANG-PARSER-001
title: <title>
scope_class: CORE | EXTENDED | OUT-OF-SCOPE
version_pin: <from .work/pin.json>
sources: [<repo-relative paths covered>]
generated_from: [<data/*.json files used>]
---
```

Sections, in order (write "Not applicable: <reason>" rather than dropping one):

1. Purpose and scope
2. Source map (table: path | type | role)
3. Key types and contracts
4. Data model
5. Control flow (Mermaid diagram or ordered steps)
6. Algorithm (stepwise; only where non-trivial)
7. Observable behavior (with test citations or `UNVERIFIED`)
8. Error handling and edge cases
9. Dependencies (inbound/outbound)
10. Extension points
11. Tests that specify this behavior
12. Design decisions and trade-offs (`FACT-SRC` vs `INFERENCE`)
13. **Guidance for MicroteamShell** (lessons with one verdict each: `REPLICATE | ADAPT | AVOID`)
14. Open questions / `UNVERIFIED`
15. Verification: what was cross-checked and how (counts reconciled with `data/`)

Conventions: Mermaid for diagrams; catalogs as tables rendered from `data/`; relative links between documents; stable IDs `<AREA>-<TOPIC>-<NNN>`, never reused. Documents over 1,500 lines are split into numbered parts with an index.

---

## 9. OUTPUT STRUCTURE

```
docs-out/
├── README.md                  # index, reading order, pin
├── PROGRESS.md  GLOSSARY.md  DECISIONS.md  VERIFICATION-BACKLOG.md
├── CONTRADICTIONS.md  FEATURE-MATRIX.md  COVERAGE.md  ACCEPTANCE-QUESTIONS.md
├── BLOCKED.md                 # only if blocked
├── 00-overview/   source-map.md, study-summary.md
├── 02-language/   02.1-tokenizer.md, 02.2-parser.md, 02.3-ast.md, 02.4-semantic-analysis.md,
│                  02.5-compiler-and-engine.md, 02.6-types-and-operators.md,
│                  TOKEN-CATALOG.md, GRAMMAR.ebnf.md, OPERATOR-TABLE.md, ERROR-CATALOG.md,
│                  AST-CATALOG.md, COMPILATION-MAP.md, BINDER-CATALOG.md, CONVERSION-RULES.md,
│                  SCOPE-AND-VARIABLES.md, LIFECYCLE-script-execution.md
├── 03-runtime/    command-discovery-and-invocation.md, parameter-binding.md, pipeline.md,
│                  errors-and-streams.md, cmdlet-infrastructure.md, script-execution.md
├── 04-extended/   one short file per extended feature
├── 05-corpus/     CORPUS-CANDIDATES.md
├── 06-synthesis/  mtsh-reference-architecture.md, compat-matrix.md, semantic-quirks.md,
│                  implementation-roadmap.md, extension-recipes.md,
│                  architecture-decision-log.md, minimum-cmdlets.md
├── data/          extracted JSON/CSV + README.md (schemas, how generated)
├── tools/         extraction scripts, verify-with-pwsh.ps1 (written, not run)
└── .work/         pin.json, files-ledger.csv, notes/, progress state
```

---

## 10. QUALITY GATES (lightweight; at most 2 rerun cycles per gate)

1. **Reference check.** Write `tools/validate-refs` (script): every cited path exists in the clone, every cited line range lies within the file's length, every cited type/method name occurs in that file. Fix failures. Confirm `git rev-parse HEAD` equals the commit in `pin.json` first.
2. **Link check.** All relative links and Mermaid code fences are well-formed; IDs in front matter are unique.
3. **Coverage.** Every `read-all` file has `ranges_read` covering the whole file in `files-ledger.csv`; every `FEATURE-MATRIX.md` row names its owner documents. Report in `COVERAGE.md`.
4. **Catalog completeness.** Token catalog, AST catalog, operator table, error catalog, and binder catalog match the counts in `data/` (reconcile any difference: conditional compilation, internal types, regex limits).
5. **Second-pass review.** Review subagents re-read every Phase 1-5 document against the source and report discrepancies; fix them or mark `UNVERIFIED`.
6. **Label hygiene.** No factual statement without a label; no hand-typed count; terminology matches the glossary; every `CORE` behavior statement is `FACT-SRC` (source or test citation) or listed in `VERIFICATION-BACKLOG.md`.
7. **Cold-read test.** A fresh subagent given **only** `docs-out/` (not the source) answers `ACCEPTANCE-QUESTIONS.md` with citations. Write at least **40 questions** covering: token modes, `-` handling in command vs expression mode, here-string rules, operator precedence, how a newline ends a statement, which AST node a `try/catch/finally` becomes, how `catch [Type]` is matched, what `finally` does with `return`, parameter-binding order, how `$_` is set, command-resolution order, scope write rules, `$ErrorActionPreference` effects, how a non-terminating error is raised, and how a script file is executed. Required: at least 90% correct with valid citations. At most 2 fix cycles; remaining gaps go to `VERIFICATION-BACKLOG.md` with the fix.
8. **Source untouched.** `git status --porcelain` shows only `docs-out/` changes.

After the gates, write the result of each (`PASS`, `FAIL-RECORDED` with reason) into `COVERAGE.md` and `00-overview/study-summary.md`.

---

## 11. WHAT "DONE" MEANS

- One pinned commit everywhere.
- Every factual statement is labelled; no claim without a citation.
- All catalogs are generated from `data/`, not typed.
- A C# developer reading only `docs-out/` can implement MicroteamShell's tokenizer, parser, AST, tree-walking evaluator, scopes, parameter binding, pipeline, and `try/catch/finally` without opening the PowerShell source.
- `CORPUS-CANDIDATES.md` and `verify-with-pwsh.ps1` let the owner confirm the `UNVERIFIED` behaviors later with a real `pwsh`.
