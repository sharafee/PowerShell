# PowerShell Source — Forensic Architecture Study (Claude Code Master Prompt v3.1)

> Usage: run Claude Code inside the root of the **local clone** of the repository
> (the private fork `github.com/sharafee/PowerShell`, e.g. `D:\dev\PowerShell`),
> place this file there, and tell Claude Code:
> "Read PowerShell-Architecture-Analysis-Prompt-v3.md fully, then execute it."
> This prompt needs a real filesystem, shell, and subagents. It is NOT suitable for a
> chat that only receives selected files (for example claude.ai project knowledge).
> Output goes to `docs-out/` at the repo root. Builds and experiments happen only in a
> scratch copy outside the repo (section 2). Never modify `src/`, `test/`, or `tools/`.
> Do not assume the fork is reachable on the public internet; everything must work
> offline against the local clone.

> **What changed from v2** (context for the repository owner — NOT execution
> instructions):
> 1. The target product is a **new shell with a brand-new language and its own
>    interpreter on .NET/C#**. It is *not* a PowerShell fork and does *not* target
>    `.ps1` script compatibility. PowerShell is used strictly as the forensic
>    reference architecture; all "compatibility" framing is replaced by
>    design-lesson framing (`LESSON` tags, design canvas).
> 2. Implementation guidance is anchored to **.NET 8/9/10 LTS** (Roslyn,
>    `System.Linq.Expressions`, `Reflection.Emit`, NativeAOT constraints,
>    `Microsoft.Extensions.*`, `AssemblyLoadContext`).
> 3. **Security & sandboxing is the P0 enterprise axis**: Phase 5 elevated, new
>    threat-model and security-blueprint deliverables, enforcement points
>    mechanically extracted into `data/enforcement-points.json`.
> 4. New deliverables: `STAGE-CONTRACTS.md`, `new-language-design-canvas.md`,
>    `language-design-principles.md`, `dotnet-runtime-integration.md`,
>    `threat-model.md`, `new-shell-security-blueprint.md`.
>    Renames: `CONFORMANCE-CORPUS.md` -> `REFERENCE-TEST-CORPUS.md`;
>    `compatibility-strategy.md` -> `language-design-principles.md`.
> 5. A one-shot offline **fork-base pinning** step replaces any fork-delta phase.
> 6. Acceptance questions extended to 46 seeds; one extra quality gate
>    (interpreter-readiness review).
>
> **v3.1 revision note** (self-review pass — precision and completeness, no scope change):
> a. One verdict vocabulary everywhere: subsystem lessons, semantic quirks, and the
>    reuse map all use `ADOPT-CONCEPT | ADAPT | REDESIGN | AVOID` (rule 16), with an
>    explicit mapping from the older `LESSON-RETAIN/AVOID/OPTIONAL` and `DROP` tags.
> b. Ownership clarified: layered architecture is a Phase 1 deliverable written to
>    `00-overview/`; review subagents return findings in their report and only the
>    coordinator writes shared files (`VERIFICATION-BACKLOG.md`, ledger, `PROGRESS.md`);
>    extraction tools live in `docs-out/tools/` but build/run in the scratch copy only.
> c. New data sets `auto-variables.json` and `attributes.json`; `data/README.md`
>    schema requirement; fixed design-canvas row-ID area codes; acceptance questions
>    47-54 added (runtime subsystems, startup, experimental features); final summary
>    persisted as `00-overview/study-summary.md`.
> d. Corrected Appendix A hints (interpreter path, runspace/pipeline location);
>    strengthened rules 1/14/16 (code beats comments, offline fallback for `EXTERNAL`
>    checks, guidance-section scope); fixed gate 1 pinned-commit wording, gate 4
>    enforcement-point ID check, gate 5 subagent/coordinator hand-off; renamed
>    `08-engineering/quality-gates.md` -> `08-engineering/engineering-processes.md`
>    to avoid collision with this prompt's own quality gates (section 10).

---

## 0. ROLE

You are a **Principal Language-Runtime / Compiler Architect** performing a forensic,
evidence-based architecture study of the PowerShell source code in this repository
(MIT licensed). You work like an auditor: you extract facts mechanically where possible,
read code line by line where it matters, and never fill gaps with memory or guesses.

You are simultaneously the **chief product architect** preparing the design basis for
the new enterprise product defined in section 1.1. Every document you produce must
serve that destination while remaining strictly evidence-based about the source you
study.

## 1. GOAL AND PRODUCT BRIEF

### 1.1 The product this study serves

- **Product:** a new, custom, enterprise-grade shell and scripting language ("the new
  shell") with **its own interpreter** (tokenizer, parser, AST, semantic analysis,
  compiler/interpreter, runtime, pipeline, type system, providers, security, hosting,
  remoting, tooling).
- **Implementation stack:** .NET / C# on a current LTS runtime (.NET 8 or newer). The
  new shell is a managed .NET application; every implementation recommendation must be
  actionable for a C# team.
- **Language stance:** the new language is **designed from scratch**. It is NOT a
  PowerShell dialect and there is **no `.ps1` compatibility goal**. PowerShell (this
  repository) is the reference architecture: the best available real-world example of
  how an industrial shell/language pipeline is engineered, warts and all. Study what it
  does, why it works, where it hurts, and decide deliberately what the new language
  does differently.
- **P0 enterprise axis: security and sandboxing.** The product will run untrusted and
  semi-trusted scripts in enterprise environments. Every subsystem document must expose
  the security surface of the corresponding PowerShell subsystem and state what the
  new product must do instead or in addition.

### 1.2 What this means for the study

- Cover the **entire codebase at architecture level** (structure, responsibilities,
  contracts, dependencies, data flow, extension points, design decisions).
- Cover the **language pipeline at DEEP, exhaustive level**:
  `source text -> tokens -> parser -> AST -> semantic checks -> compilation/interpretation -> runtime execution`.
  A reader must be able to re-implement each stage's behavior from the documents alone.
- Extract **design lessons**: for every mechanism, record whether the new shell should
  adopt the concept, adapt it, redesign it, or avoid it — always with evidence
  (operating rule 16).
- Do **NOT** write line-by-line explanations of individual cmdlet implementations.
  Cmdlet assemblies are documented as module families (what they provide, how they plug
  into the engine, a mechanically extracted cmdlet inventory), not function by function.
- The documentation must **mirror the source organization exactly**
  (solution -> project -> folder -> namespace/file -> type) so every document maps
  directly to a place in the source tree, and every source folder maps to a document.
  In addition it provides thematic architecture documents on top of that mirror.
- Documents are **modular**: one subsystem or one catalog per file, stable IDs,
  relative links, a fixed template, no monolithic files.

---

## 2. ENVIRONMENT AND PRECONDITIONS (do this before Phase 0)

1. **Host:** assume Windows 11. Detect what exists and record it in
   `docs-out/.work/environment.md`: `git`, `rg` (ripgrep), `dotnet --list-sdks`,
   `pwsh`, `powershell.exe`, `cloc`, `node`/`mmdc` (Mermaid CLI). Do not assume bash.
   Every script you write must run on Windows PowerShell 5.1 or PowerShell 7 (detect
   which one is available) or be a `dotnet` console tool. Put scripts in `docs-out/tools/`.
2. **Git state may be unusual.** The clone may be shallow (`--depth 1`) and/or a single
   "import" commit with no tags and no history. Pin the version using this fallback order,
   and record which method worked and how:
   `git describe --tags` -> `git tag --points-at HEAD` -> last commit message ->
   version metadata in the tree (`PowerShell.Common.props`, `DotnetRuntimeMetadata.json`,
   `global.json`, newest `CHANGELOG/*.md` entry, release-build version files) ->
   the version the user stated, if any.
   Do **not** rely on `git log`, `git blame`, or history for analysis. Language and feature
   evolution must be derived from the code structure plus `CHANGELOG/` and `docs/`
   only, and labelled as such.
3. **Fork-base pinning (offline, one-shot).** This repository is a fork; the upstream may
   be private or unreachable. Do NOT depend on network access to GitHub and never clone
   anything during this study. Run once: `git remote -v`. If an `upstream` remote exists
   AND is reachable, record `git merge-base HEAD upstream/<default>` and
   `git diff --stat` against it; if the diff exceeds metadata-only changes (more than
   ~20 changed files under `src/`), write `00-overview/fork-drift.md` listing the
   changed files and treat those files as first-class study subjects; otherwise record
   "pure fork, no drift detected" with the evidence. If no upstream is reachable,
   record "fork base pinned locally via version metadata" and continue. Never block on
   the network for this step.
4. **Scratch copy for anything that writes files** (build, restore, tests, experiments):
   copy the repo to `../ps-scratch/` (outside the repo) and work there. Never create
   `bin/`, `obj/`, or packages inside the analyzed repo. Before finishing, run
   `git status --porcelain` and confirm only `docs-out/` changed.
5. **No machine-wide changes.** Do not run `Start-PSBootstrap`, installers, `winget`,
   `choco`, or anything that changes system state. Use plain `dotnet restore/build`
   in the scratch copy. If the SDK required by `global.json` is missing and cannot be
   used via roll-forward, skip building, record it in `DECISIONS.md`, and continue with
   static analysis only. Network access is allowed only for NuGet restore and for fetching
   tool packages (for example Roslyn) in the scratch copy; log each use in `DECISIONS.md`.
6. **Never execute repo scripts you have not read.** Read first, run only your own tools.
7. Preflight result: write `docs-out/.work/environment.md` and the first `PROGRESS.md`
   before starting Phase 0.

---

## 3. OPERATING RULES (non-negotiable)

1. **Evidence only.** Every claim must cite a repo-relative file path plus
   class/method name and line range, in this format:
   `src/<Project>/<path>.cs::Type.Member@L120-L188`. If you did not read it, do not state
   it. Anything uncertain must be tagged `UNVERIFIED` and added to
   `docs-out/VERIFICATION-BACKLOG.md`. Where code and comments/XML docs conflict, the
   code is the evidence for behavior (comments are evidence of intent only); record the
   conflict in `docs-out/DECISIONS.md`.
2. **Never trust memory of the repo layout.** Discover the real layout with tools.
   Every file name, folder, type, or method named in this prompt is only a **hint to
   verify**, never a fact. If a hint is wrong, record the real answer in `DECISIONS.md`.
3. **Pin the version and the fork base.** Every document starts with a front-matter
   block (section 8.1) containing: version tag or fallback, commit hash, target
   frameworks, SDK from `global.json`, and how the pin was derived.
4. **Self-resumable.** Maintain `docs-out/PROGRESS.md` (phases, modules, task IDs,
   status, open questions). Update it after every document. If context is lost or the
   session restarts, resume from this file and `docs-out/.work/`. Write each document to
   disk as soon as it is finished.
5. **Scale with subagents** under the contract in section 9: one subagent per
   module/subsystem/stage, each writing only its own files, then a consolidation pass.
6. **Read-only on source.** Do not modify, reformat, or delete anything outside
   `docs-out/` (and the scratch copy).
7. **No assumptions about intent.** Describe what the code does; label inferences about
   *why* as `INFERENCE` and keep them separate from facts.
8. **Quote sparingly.** Short code excerpts (max ~15 lines) only when they are the
   clearest evidence. Prefer references and paraphrase. Documents must describe
   behavior in your own words so they can support a clean-room re-implementation.
9. **Language of documents:** English (technical), consistent terminology defined in
   `GLOSSARY.md`. Use real identifiers exactly as in source (case, namespace).
10. **No questions.** Do not ask for clarification; make the best evidence-based decision,
    record it in `docs-out/DECISIONS.md`, and continue.
11. **Mechanical over manual.** Anything countable (types, enum members, AST classes,
    token kinds, operators, resource keys, cmdlets, tests, project references) must be
    produced by a script into `docs-out/data/` and rendered into the documents from that
    data. Never hand-type a catalog (section 5).
12. **Completeness over brevity.** When a document or catalog promises "every X", list every
    X. No summarizing by omission. If a catalog is too large for one file, split it into
    parts (`-part-01.md`, ...) with an index file.
13. **SPEC / IMPL / LESSON tagging.** Tag every section as one of:
    `SPEC` — observable language/runtime behavior, independent of how PowerShell
    implements it (the clean-room basis for the new shell);
    `IMPL` — how this source implements it;
    `LESSON` — a design lesson for the new shell, always citing the evidence it derives
    from and carrying a verdict per rule 16.
    A new product must be buildable from `SPEC` + `LESSON` without copying `IMPL`.
14. **Repo is the only source of truth.** External documentation (learn.microsoft.com,
    .NET docs, blogs) may be used only as a clearly labelled `EXTERNAL` cross-check and
    never as evidence of behavior of this version. The same applies to claims about
    current .NET capabilities (NativeAOT, `AssemblyLoadContext`): label them `EXTERNAL`
    and keep them separate from repo evidence. If the network is unavailable, keep the
    `EXTERNAL` claim but add a `VERIFICATION-BACKLOG.md` entry recording that it could
    not be cross-checked online.
15. **Conditional compilation matters.** Types and members may exist only under
    `#if` symbols (platform, framework, feature flags). Record the symbol set per
    project and mark platform-conditional items in every catalog.
16. **New-language lens (new in v3).** Every document using the template in 8.1 (all
    subsystem documents: Phases 2-6 and the command-module families) must end its
    guidance section (template section 18) with explicit design lessons for the new
    shell, each tagged `ADOPT-CONCEPT | ADAPT | REDESIGN | AVOID` and tied to the
    evidence in the same document. These four verdicts are the **only** lesson
    vocabulary in the whole study; older variants (`LESSON-RETAIN/AVOID/OPTIONAL`,
    `DROP`) must be mapped onto them (see 2.9). Neutral observations need no verdict tag.
17. **Clean-room discipline (new in v3).** Documents must enable a clean-room
    implementation of the new shell: describe behavior and design conceptually; never
    embed source code beyond the short evidence excerpts allowed by rule 8; keep
    licensing/attribution analysis in `09-synthesis/licensing-notes.md`. Product-bound
    artifacts (design canvas, security blueprint, reference architecture) must be
    understandable and usable without re-reading the PowerShell source.

---

## 4. DEPTH TIERS AND READING PROTOCOL

### 4.1 Tiers (assign every source file to exactly one tier in the ledger)

| Tier | Scope | Required depth |
|---|---|---|
| **A — Language core** | Tokenizer, parser, AST and visitors, semantic checks, variable analysis, type resolution, class/enum compilation, compiler, dynamic binders, runtime operations, interpreter/light compiler, script block types, `LanguagePrimitives` and conversions, parameter binder, command processors, scope/variable storage | **100% of lines read.** Per-type and per-method documentation of all non-trivial members. Method-level call graph for entry points. |
| **B — Engine and platform** | Rest of the engine, runspace/pipeline, providers, ETS, modules, formatting, hosting, remoting, security, debugger, eventing, help, platform layer | Every type declaration inventoried; every public/internal contract read; key algorithms read line by line. |
| **C — Surface** | Cmdlet assemblies, providers' leaf classes, native shims, tools, generated files, resources | Inventory via scripts (types, cmdlets, registration, dependencies). Read only what is needed to explain how they plug in. |

Tier lists are decided in Phase 0 from the real tree and written to
`docs-out/.work/tiers.csv`. Moving a file to a lower tier requires a `DECISIONS.md` entry.
`tiers.csv` is the initial assignment; `.work/files-ledger.csv` (4.2) is the living
tracking record and must stay consistent with it.

### 4.2 Reading protocol for large files

- Run an outline first (types and members with line ranges) from `docs-out/data/`.
- Read files longer than 800 lines in windows of at most 300 lines. After each window
  append structured notes to `docs-out/.work/notes/<flattened-path>.md`
  (what you learned, member names, line ranges, open questions). Re-read instead of
  relying on earlier windows still being in context.
- Maintain `docs-out/.work/files-ledger.csv` with columns:
  `path, loc, tier, ranges_read, doc_ids, status` (maintained by the coordinator;
  authoring subagents propose row updates in their reports — section 9). Tier A needs
  `ranges_read` covering the whole file before its documents are marked done.
- For `partial` classes, list every file that contributes to the type.

---

## 5. MECHANICAL EXTRACTION LAYER

Build these tools in Phase 0. Tool source lives in `docs-out/tools/`; build and run
them only in the scratch copy so no `bin/`/`obj/` ever lands in the analyzed repo;
commit only tool source and their JSON/CSV output to `docs-out/`. Catalogs and folder
cards are rendered from this data, then annotated by reading. Every dataset in
`docs-out/data/` gets a schema entry (fields, types, generation command, preprocessor
symbol sets used) in `docs-out/data/README.md`.

### 5.1 Extraction approach (in order of preference)

1. **Roslyn-based `dotnet` console tool** using `Microsoft.CodeAnalysis.CSharp`:
   parse every `.cs` file, run it once per relevant preprocessor-symbol set
   (record the sets you chose: at least Windows-like and Unix-like, with the symbols the
   projects actually define in their `.csproj`/props).
2. If Roslyn is impossible: `rg`/ctags-based extraction with conservative regexes.
   Mark all such output `APPROX` and add a verification step in the quality gates.

### 5.2 Required data sets

| File in `docs-out/data/` | Content |
|---|---|
| `projects.json` | Every `.csproj` (also those not in the `.sln`, each flagged `in_solution: true/false`): path, output type, TFMs, assembly name, `ProjectReference`, `PackageReference` (with conditions), `InternalsVisibleTo`, defines, source generators, analyzers |
| `files.csv` | Every file under `src/`, `test/`, `tools/`, `docs/`, build and pipeline folders: path, language, LOC, tier, owning project |
| `types.json` | Every type (class, struct, interface, enum, delegate, record): kind, name, namespace, project, file, start/end line, accessibility, modifiers, base types, interfaces, `partial` file list, attributes, conditional-compilation symbols, member counts |
| `members-tierA.json` | For every Tier A type: all members with signature, accessibility, line range, syntactic callees (best-effort), and referenced enum/string tables |
| `enums.json` | Every enum with every member, value, attributes, doc comment (must include `TokenKind`, `TokenFlags` and all language-related enums) |
| `ast-hierarchy.json` | Transitive closure of types deriving from the AST base type, with base chain, children (properties/fields of AST type), and the parser method(s) that construct each node |
| `parser-methods.json` | Every parser/tokenizer method with line range and the methods it calls (production graph) |
| `tables.json` | Keyword tables, operator tables, precedence tables, character-class tables, and similar static tables, exactly as they appear in source |
| `resources.json` | Every `.resx` key by resource class (parser error IDs, runtime errors) with the code location(s) that use it |
| `cmdlets.json` | Every type carrying a cmdlet attribute: verb, noun, class, file, project, parameter sets, dynamic parameter use; every provider with its capabilities |
| `visitors.json` | Every class implementing an AST visitor interface and which node types it overrides |
| `binders.json` | Every dynamic-binder class, which operation it handles, and where it is created |
| `auto-variables.json` | Every automatic variable: name, definition site (code or resource), every writer site, type when statically known; feeds `SCOPE-AND-VARIABLES.md` and the reflection cross-check in 5.3 |
| `attributes.json` | Every attribute type used by cmdlets and the language (`Cmdlet`, `Parameter`, `Validate*`, `Allow*`, `ArgumentCompleter`, argument-transformation, `OutputType`, `Alias`, ...): valid targets, properties, and where the engine enforces it |
| `tests.json` | Every test project and test file; for Pester files the `Describe/Context/It` tree and tags (parse with the PowerShell parser API when `pwsh` is available, else conservative regex — record which was used); for xUnit the classes/facts/theories; mapping to features where the name allows |
| `conditional-compilation.json` | Every `#if` symbol used, files and types affected |
| `format-and-types-xml.json` | Contents of `*.ps1xml`-style files (type extensions, format views) by name and target type |
| `enforcement-points.json` (new in v3) | Every security/policy enforcement point: language-mode checks, execution-policy gates, AMSI scan hooks, signature validation, constrained-language checks, secure-string handling, JEA-related checks. Mechanically seeded by searching for known APIs and patterns (`ExecutionContext.LanguageMode`, `CheckRestrictedLanguage`, `Compiler.CheckLanguageFeatures`, AMSI interop types, `Authenticode`/signature types, transcription/logging entry points), then verified by reading. Entry: file, type, method, line range, what it enforces, trigger condition, assigned `SEC-ENF-###` ID. |

### 5.3 Reflection cross-check (when a build or a matching `pwsh` is available)

Use reflection (from the built engine in the scratch copy, or from an installed `pwsh`
of nearly the same version, flagged `VERSION-MISMATCH` in that case) to independently
count public AST types, `TokenKind` members, public operators, automatic variables, and
public cmdlets. Counts must match the static data or every difference must be explained
(conditional compilation, internal types, version mismatch).

### 5.4 Differential oracle (golden samples)

If the engine can be built or run, write `docs-out/tools/dump-parse.ps1` that, for a list
of snippets, dumps tokens (kind, flags, text, extent) and the AST tree (node type,
children, extents) plus parse errors (ID, message key, extent) using the real parser API.
Store results in `docs-out/data/golden/`. Rules:

- Every grammar production in `GRAMMAR.ebnf.md` needs at least 2 valid and 1 invalid
  golden sample.
- Every operator in `OPERATOR-TABLE.md` needs samples covering its operand-type
  families and the precedence/associativity edge cases.
- Samples are evidence for behavior; the source remains the evidence for design.
- If nothing can be built or run, record that and mark all behavior-only claims that
  would have been sample-verified as `UNVERIFIED`.

---

## 6. PHASES

Execute in order. Do not skip. Finish each phase's deliverables before the next.
Independent work inside a phase runs in parallel under section 9.

### Phase 0 — Reconnaissance, pinning, tooling

- Do the environment preflight (section 2), including the fork-base pinning step.
  Record version metadata (rule 3).
- Read `README.md`, `docs/`, `build.psm1`, `PowerShell.sln`, `PowerShell.Common.props`,
  `Analyzers.props`, `global.json`, `nuget.config`, `DotnetRuntimeMetadata.json`, and every
  `Directory.*.props/targets` you find.
- Build the **repo census**: every top-level folder, project count, file counts per
  language (C#, PowerShell, ps1xml, resx, native, YAML), LOC per project
  (`cloc` or your own script).
- Build the **project dependency graph** from every `.csproj` (`ProjectReference`,
  `PackageReference`, target frameworks, conditional platform references) as a Mermaid
  graph plus a table. Identify **all** projects including those not in the `.sln`
  (build-only, tests, tools, source generators, native shims).
- Identify **external dependencies not in this repo** (NuGet packages, bundled modules
  such as the interactive line editor, external native libraries) and document what each
  is used for and how it integrates (`00-overview/external-dependencies.md`).
- Build and run the extraction tools (section 5). Produce `files.csv`, `tiers.csv`,
  `files-ledger.csv`.
- Generate the **source-tree map**: the real folder tree down to every folder that
  contains source files, with file/type/LOC counts (`00-overview/source-tree-map.md`).
  This drives the `src-mirror/` structure.
- Deliverables: `00-overview/` and `data/` (including `fork-drift.md` when drift was
  detected in section 2 step 3).

### Phase 1 — Repository-wide architecture map

- Layered architecture: host layer, engine, command modules, SDK, tooling. Written to
  `00-overview/layered-architecture.md` (a Phase 1 deliverable that lives in
  `00-overview/`).
- Build system: how `build.psm1` and `tools/` compile, package, and publish; per-platform
  differences; configuration matrix (Debug/Release/Linux/CodeCoverage); source generators;
  resource and type-catalog generation; experimental feature flags.
- CI/CD and packaging pipelines (`.pipelines`, `.vsts-ci`, `.github`): stages, artifacts,
  signing, supported platforms.
- Cross-cutting: logging/eventing, telemetry, localization (`.resx`), analyzers/StyleCop
  rules and `.editorconfig` (coding standards worth adopting).
- Deliverables: `01-repository/`.

### Phase 2 — LANGUAGE PIPELINE (deepest phase, Tier A)

For **each** stage below document: purpose, entry points, key types and their
responsibilities, inputs/outputs, invariants, error handling and recovery, performance
characteristics, extension points, and **every public/internal contract** other stages
depend on. Add a Mermaid sequence/flow diagram per stage. All stage documents follow the
template in 8.1 and tag sections `SPEC`/`IMPL` (and `LESSON` per rule 16).

**2.0 Pipeline map, stage contracts, and Tier A outlines**
- One-page map: stage -> files -> entry points -> data handed to the next stage
  (`02-language/00-pipeline-map.md`).
- `02-language/STAGE-CONTRACTS.md` (new in v3): for every pipeline boundary —
  text -> tokens, tokens -> AST, AST -> semantic model/checks, AST -> compiled artifact
  (expression trees / interpreter instructions), runtime -> values, values -> output
  objects — document PowerShell's exact data contract: the types exchanged, ownership
  and lifetime, invariants, the error channel at that boundary (`ParseError`,
  `RuntimeException`, `ErrorRecord`), and threading rules, each with evidence. End each
  contract with a short `NEW-SHELL CONTRACT` recommendation: what the new shell's
  equivalent contract should be and why. For each boundary, also note the natural
  insertion point where the new shell would place policy/security hooks (feeds Phase 5).
  This document is the spine the new implementation is built around.
- Per Tier A file: outline with line ranges from `members-tierA.json`, partial-class map,
  `#if` map. Stored in `docs-out/data/tierA-outlines/`.

**2.1 Tokenizer / lexer**
- Token kinds and flags (complete table from `enums.json`), keyword table (including
  contextual keywords), operator table, character classification tables.
- Tokenizer modes (command vs expression mode, how the parser switches them), here-strings,
  string expansion and sub-expressions, nested tokens, numeric literal rules (radix,
  suffixes, multipliers), escape handling, comments (line, block, help comments),
  line continuation, generic/redirection tokens, member-name vs operator ambiguity.
- Position/extent tracking, error tokens, and the public tokenization API.
- Mapping: token kind -> parser rules that consume it.

**2.2 Parser**
- Grammar reconstruction: produce an **EBNF-style grammar** derived strictly from the
  parser code (statements, pipelines, commands, expressions, operator precedence and
  associativity table, attributes, type literals, hashtables, script blocks, param blocks,
  `DynamicParam`/`begin`/`process`/`end`/`clean` blocks, classes, enums, configurations,
  `using` statements, etc.). Mark each production with the parser method, file and line
  range it comes from. Produce the **production table**:
  `Production | Method | File@Lines | Tokens consumed | AST produced | Error IDs`.
- Parsing strategy (recursive descent? lookahead? backtracking? token pushback?), how it
  distinguishes command vs expression context, newline and statement-terminator
  sensitivity, how ambiguity is resolved, **error recovery strategy** (what the parser
  returns when errors exist: partial AST? skipped tokens? synchronization points) and the
  **error message catalog** (ParseError IDs, resource keys, triggering rules) in
  `02-language/ERROR-CATALOG.md`.
- Public API (`Parser.ParseInput/ParseFile`, `Tokenize`, extents, `ParseError`).

**2.3 AST**
- **Complete node catalog** from `ast-hierarchy.json`: every AST class, base type,
  fields/children, and which parser production creates it. Document the visitor
  infrastructure (interfaces, default visitors, `Visit` dispatch, AST copy/clone,
  `Find/FindAll`, `GetScriptBlock`, `SafeGetValue`/constant and safe-expression evaluation).
- Node metadata: extents, parent links, type info, cached compile-time info.
- Table: `NodeType | Base | Children | Created by | Consumed by (visitors/compiler/checks)`.

**2.4 Semantic analysis / static checks**
- Symbol resolution, variable analysis (usage, scope, auto/pre-defined variables,
  `using:` / `$local:` / `$script:` etc.), type resolution for type literals and classes,
  attribute validation, duplicate/invalid construct checks, language-mode restrictions at
  analysis time, and any optimizer or constant-folding passes.
- Every check as a table row: `Check | Where | Trigger | Error ID | Phase it runs in`.

**2.5 Compilation and execution engine**
- How AST becomes executable code: expression-tree compilation, `ScriptBlock` and compiled
  script block lifecycle (lazy compile, caching, optimized vs unoptimized, the
  interpreter/light-compiler fallback), **the rule that selects compiled vs interpreted**,
  dynamic call-site binders (member access, invoke, convert, binary/unary ops, index,
  etc.) and the PowerShell-specific **binding rules** (method overload resolution,
  argument conversion, property/adapter lookup, COM/WMI/CIM/XML/DataRow adapters),
  scope and variable storage model (locals tuple, dynamic vs fixed slots, how variable
  lookup works at runtime), flow-control implementation
  (break/continue/return/throw/trap/try-catch-finally), pipeline integration of
  statements, `$_`/`$PSItem`, automatic variables, output-stream semantics
  (success/error/warning/verbose/debug/information/progress), caches (script block caches,
  binder caches, type caches) and their invalidation.
- Record precisely **how the DLR is used** (`CallSite`, custom binders, lightweight code
  generation) and, for each use, note what the equivalent design on current .NET would be
  (hand-written caches, `Expression.Compile` with caching, or interpreter fallback) —
  tagged `LESSON`, feeding section 2.10.
- Tables: **each AST node type -> how it is compiled/interpreted** (`COMPILATION-MAP.md`)
  and the binder catalog (`BINDER-CATALOG.md`, from `binders.json`).
- `SCOPE-AND-VARIABLES.md`: precise model of scopes, variable tables, dynamic scoping,
  `Set-Variable` options (constant/readonly/private/allscope), and closure behavior.

**2.6 Type conversion and operators**
- `LanguagePrimitives` conversion pipeline (converter order, type converters,
  `PSTypeConverter`, implicit/explicit rules), comparison and equality semantics,
  operator semantics (arithmetic, string, comparison with case-sensitivity variants,
  `-match`/`-replace`/`-split`/`-join`/`-like`/`-is`/`-as`/`-in`/`-contains`, range,
  format, redirection), numeric promotion rules, string-to-number parsing rules,
  collection unrolling and enumeration rules, `$null` handling.
- `OPERATOR-TABLE.md`: operator | token | precedence | associativity | AST node |
  runtime implementation | operand-type behavior | golden samples.
- `CONVERSION-RULES.md`: ordered conversion algorithm with a decision table.

**2.7 Language features implemented on top of the core**
- Classes and enums (`class` compilation to dynamic assemblies), `using` statements,
  `DSC configuration` keyword/DSL extension mechanism, workflow remnants (if any),
  script/module parameter metadata, attributes and validation attributes, argument
  transformation/completers, `ForEach-Object -Parallel` / thread job boundaries, pipeline
  chain operators (`&&`, `||`), ternary, null-coalescing, null-conditional access, etc.
  Document how each feature touches tokenizer, parser, AST, checks, compiler and runtime
  (derive this from the code, not from history).
- **`HOWTO-extend-language.md`:** for each of (a) a new binary operator, (b) a new
  statement keyword, (c) a new AST node kind, (d) a new literal syntax, (e) a new automatic
  variable, (f) a new type conversion, (g) a new attribute: the ordered list of files,
  classes, and methods that must change. Base each recipe on tracing 1-2 existing
  features end to end through the code, and cite evidence for every step. This document
  is the touchpoint map for the new shell's own pipeline — it shows how many places a
  language change reaches, which the new design must reduce.

**2.8 Tooling that depends on the pipeline**
- Tab completion (`CommandCompletion`), syntax-highlighting tokenization API, script
  analysis hooks, debugger breakpoint/sequence-point mapping, formatting of error positions
  (`InvocationInfo`, `ScriptExtent`), help-comment parsing.

**2.9 Language specification draft and semantic quirks**
- `LANGUAGE-SPEC-DRAFT.md` (all `SPEC`): a reference behavior specification **of
  PowerShell** — lexical structure, grammar summary, type system, expressions, statements,
  scoping, pipeline semantics, error semantics — with every statement linked to evidence
  and to the tests that specify it. This is the prior-art record for the new language,
  NOT the new language's spec. Each major section ends with a `NEW-LANGUAGE-DELTA:` note
  (3-10 lines) naming what the new language must decide differently, linking to the
  corresponding row in `09-synthesis/new-language-design-canvas.md`.
- **Canvas skeleton first.** Create `09-synthesis/new-language-design-canvas.md` at the
  start of Phase 2 with all row IDs reserved and cells empty, so the forward links from
  `LANGUAGE-SPEC-DRAFT.md`, `SEMANTIC-QUIRKS.md`, and every guidance section resolve
  immediately; Phase 7 fills the content.
- `SEMANTIC-QUIRKS.md`: every surprising behavior found (implicit unrolling, comparison
  coercions, parsing ambiguities, output pollution rules, etc.) with evidence, a golden
  sample, and a recommendation tag `LESSON-RETAIN | LESSON-AVOID | LESSON-OPTIONAL`
  (replaces v2's compatibility tags) with a one-sentence rationale each. When these
  quirks enter the design canvas, map them onto the rule-16 verdicts:
  `LESSON-RETAIN` -> `ADOPT-CONCEPT` or `ADAPT`, `LESSON-AVOID` -> `AVOID`,
  `LESSON-OPTIONAL` -> an open `NLD` row for the product owner. The design canvas
  consumes these verdicts.

**2.10 Interpreter design space (.NET-anchored)**
- `INTERPRETER-DESIGN-SPACE.md`: anatomy of PowerShell's execution strategy (what is
  compiled, what is interpreted, what is dynamic, startup and warm-up behavior, caching;
  the light-compiler/interpreter model and its instruction set; DLR call-site caching).
  Facts and `INFERENCE` clearly separated.
- Then the design evaluation **for the new shell on .NET 8/9/10 LTS**. Evaluate and score
  each alternative: (1) AST tree-walking interpreter; (2) custom bytecode VM (sketch the
  instruction set and stack/frame model); (3) `System.Linq.Expressions` compilation to
  delegates (with cache strategy and invalidation); (4) `Reflection.Emit` dynamic
  assemblies/methods (what PowerShell's class compilation does); (5) source-generated
  ahead-of-time compilation; (6) hybrid interpreter + optimizer (PowerShell-like
  light-compiler model).
- Document the hard .NET constraints with `EXTERNAL` labels: NativeAOT forbids
  `Reflection.Emit` and runtime JIT (interpreter or pre-generated code only, and
  `Expression.Compile` falls back to an interpreter with degraded performance under
  AOT); DLR lightweight code generation unavailable under AOT; `AssemblyLoadContext`
  capabilities and limits; ReadyToRun/JIT startup trade-offs. Keep repo evidence for
  what PowerShell itself does strictly separate from these `EXTERNAL` facts.
- Score matrix criteria (enterprise): startup latency, steady-state throughput,
  debuggability (breakpoints/stepping/inspection), sandboxability, determinism, memory
  footprint, AOT-friendliness, observability/profilability, tooling complexity.
- End with a **RECOMMENDATION** section (labelled `INFERENCE`): the recommended execution
  strategy for the new shell on .NET, a phased adoption path (e.g., tree-walking
  interpreter first, bytecode later), and the measurable triggers that would justify
  moving to the next phase.

**Phase 2 mandatory deliverables:**
`02-language/GRAMMAR.ebnf.md`, `TOKEN-CATALOG.md`, `AST-CATALOG.md`, `OPERATOR-TABLE.md`,
`COMPILATION-MAP.md`, `BINDER-CATALOG.md`, `CONVERSION-RULES.md`, `ERROR-CATALOG.md`,
`SCOPE-AND-VARIABLES.md`, `LANGUAGE-SPEC-DRAFT.md`, `SEMANTIC-QUIRKS.md`,
`HOWTO-extend-language.md`, `INTERPRETER-DESIGN-SPACE.md`, `STAGE-CONTRACTS.md`,
`GOLDEN-SAMPLES.md`,
`CALL-GRAPHS.md` (entry-point call graphs for tokenize, parse, check, compile,
invoke, as Mermaid, generated from `members-tierA.json`),
`LIFECYCLE-script-execution.md` (end-to-end sequence diagram from `pwsh -c "<text>"` to
output, naming every class and method touched), and `REFERENCE-TEST-CORPUS.md` (existing
parser/language tests under `test/` that specify language behavior, grouped by feature
with paths and counts from `tests.json` — used as the **model for the new product's own
specification-test suite**, not as a compatibility target).

### Phase 3 — Runtime and execution model (Tier B, with Tier A parts)

For every subsystem below, add a subsection **"Security surface"** listing the
enforcement points from `enforcement-points.json` that live in this subsystem (with
`SEC-ENF` IDs) and what the new shell must guarantee here. Document each subsystem with
the same per-module template (8.1):

- **Runspace and Pipeline**: runspace types, runspace pools, pipeline types, `PowerShell`
  API, `Invoke/BeginInvoke`, stopping/cancellation, state machines (draw state diagrams),
  thread model and synchronization, `PipelineProcessor`/`Pipe` internals, object flow and
  back-pressure.
- **Command discovery and invocation**: command resolution order, command types
  (Alias/Function/Filter/Cmdlet/Script/Application/ExternalScript/Workflow),
  `CommandProcessor`, `ScriptCommandProcessor`, native command processor (argument passing,
  redirection, encoding, process lifecycle).
- **Cmdlet infrastructure**: `Cmdlet`/`PSCmdlet` base types, lifecycle
  (`BeginProcessing/ProcessRecord/EndProcessing/StopProcessing`), attributes,
  `ShouldProcess`, stream-writing APIs, dynamic parameters.
- **Parameter binding**: metadata construction, binding algorithm (named, positional,
  pipeline by value/by property name, parameter-set resolution, type coercion, mandatory
  prompting, validation and transformation attributes). Provide the **algorithm as ordered
  steps** plus a decision table for parameter-set resolution.
- **Execution context and session state**: scopes, variables, functions, aliases, drives,
  modules, `SessionStateProxy`, `InitialSessionState`, language modes, constrained
  language enforcement points.
- **Provider model**: `NavigationCmdletProvider` hierarchy, provider contracts, path
  resolution, drive management, built-in providers.
- **Extended Type System (ETS)**: type adapters, `PSObject`, `PSMemberInfo` hierarchy,
  type-extension XML mechanism, `TypeTable`, script/note/alias properties, adapter
  selection order.
- **Formatting and output**: format data pipeline, default views, `Out-Default`, `Out-*`,
  formatter host interaction, view selection rules.
- **Modules**: manifest model, module loading/analysis, auto-loading, versioning,
  `PSModulePath` resolution, binary vs script modules, nested/required modules.
- **Errors and diagnostics**: `ErrorRecord`, exception hierarchy, `$Error`, `$?`,
  `$LASTEXITCODE`, `ErrorActionPreference` semantics, transcripts.
- **Jobs and concurrency**: job model, background/thread jobs, parallel foreach.
- **Debugger**: breakpoint types, debug mode, runspace debugging, sequence points.
- **Eventing and engine events**: event model, `Register-*Event` infrastructure.
- **Help system**: help content discovery, comment-based help, updatable help.
- Deliverables: `03-runtime/`.

### Phase 4 — Hosting, SDK, remoting, platform, command-module families

- **Host abstraction**: `PSHost`, `PSHostUserInterface`, `PSHostRawUserInterface`,
  `InitialSessionState`, the minimal contract a new host must implement.
- **ConsoleHost**: startup sequence (argument parsing, profile loading, `ExecutionPolicy`,
  `-Command/-File/-EncodedCommand`), REPL loop, input handling (note external dependencies
  such as the line editor that are NOT in this repo and how they integrate), exit codes.
- **SDK**: public API surface for embedding (`PowerShell`, `Runspace`,
  `CommandInvocationIntrinsics`), NuGet packaging model, API stability policy.
- **Remoting**: PSRP protocol layers (transport, fragmentation, serialization,
  negotiation), WSMan transport, SSH transport, named-pipe/process transport,
  `Enter-PSSession/Invoke-Command` flow, session configurations, JEA mechanics,
  **serialization format** (CLIXML) with type-fidelity rules, deserialized object model.
- **Platform abstraction**: Windows vs Unix split, native interop layers, `Platform` class,
  filesystem/path/encoding differences, signals, terminal handling.
- **Command-module families** (`10-command-modules/`): for each cmdlet/provider assembly:
  purpose, cmdlet and provider inventory table (from `cmdlets.json`, names and files only),
  how the assembly is registered and discovered by the engine, which engine internals it
  depends on, type/format XML it ships, resource files. No per-cmdlet implementation
  walkthroughs.
- Deliverables: `04-hosting/`, `05-remoting/`, `06-platform/`, `10-command-modules/`.

### Phase 5 — Security architecture (P0 enterprise axis — elevated in v3)

Security is the highest-priority enterprise axis for the new product. This phase is
written as if the new shell's security architect will read nothing else. Use
`data/enforcement-points.json` as the mechanical backbone; every cited check carries a
`SEC-ENF-###` ID registered in `ID-REGISTRY.md`.

- Execution policy, language modes (Full/Constrained/NoLanguage/Restricted), AMSI
  integration, script block logging / module logging / transcription, application control
  (WDAC/AppLocker) integration points, JEA role capabilities, signature validation, secure
  string handling, trust boundaries, and known enforcement points (**list each enforcement
  check with file/method/line and `SEC-ENF` ID**).
- **Threat model of the engine as-is** (`07-security/threat-model.md`): assets (process
  integrity, secrets, host filesystem, network, audit integrity), trust boundaries
  (script input, module load, remoting/deserialization, providers, host UI), attack
  surface per boundary, existing mitigations (with `SEC-ENF` IDs), residual gaps. Render
  as tables plus a Mermaid trust-boundary diagram. Label every judgement `FACT` (with
  evidence) or `INFERENCE`.
- **Security blueprint for the new shell** (`07-security/new-shell-security-blueprint.md`):
  - Policy engine design: deny-by-default, explicit capability grants per script/module
    (file, network, registry, process, execution), and the policy decision points placed
    on the new shell's command lifecycle (use the Phase 3 command-pipeline evidence to
    place the hooks precisely).
  - Language-mode equivalent: where PowerShell enforces each mode, why in-process
    enforcement is fragile (cite the enforcement points and their assumptions), and what
    the new product must do — including host-level or process-level isolation when policy
    demands guarantees.
  - Sandbox options on .NET compared honestly: in-process restrictions (weak — evidence
    from how constrained mode relies on voluntary checks), `AssemblyLoadContext`
    (assembly isolation, NOT a security boundary), child-process/job-object isolation,
    OS-level containers. Recommendation matrix by threat level, labelled `INFERENCE`.
  - Audit event model: which events must exist (command start/stop, policy decision,
    security-relevant API use, module load, script-block execution), tamper-evidence
    requirements, and forwarding (ETW / OpenTelemetry).
  - AMSI-equivalent: a pluggable content-scan interface at the same lifecycle points
    where PowerShell scans (script-block creation, command execution) — cite those points.
  - Secrets handling: PowerShell's `SecureString` reality (evidence: DPAPI use,
    plaintext-exposure paths) and what the new shell must provide instead (OS keychain
    integration, honest limits of memory-zeroing in managed code).
  - Every recommendation ties to evidence: what PowerShell does (cite), where it is weak
    (cite or `INFERENCE`), what to change.
- Deliverables: `07-security/` (`language-modes.md`, `execution-policy.md`,
  `amsi-logging.md`, `enforcement-points.md`, `threat-model.md`,
  `new-shell-security-blueprint.md`).

### Phase 6 — Testing, quality, and engineering practices

- Test layout under `test/` (xUnit vs Pester vs others), test-tag strategy, how tests are
  run per platform, fixtures/tools, coverage setup, performance tests, how language/parser
  behavior is specified by tests (feeds `REFERENCE-TEST-CORPUS.md`).
- Code quality: analyzers, StyleCop, `.editorconfig` rules, API review, experimental
  feature process, breaking-change policy, localization workflow.
- Deliverables: `08-engineering/`.

### Phase 7 — Cross-cutting synthesis and blueprint

- **Architecture decision log:** at least 30 notable design decisions found in the code
  (decision, evidence, consequences, strengths, weaknesses).
- **Strengths to adopt / weaknesses to avoid / technical debt** found while reading.
- **Component inventory and reuse map**: for every major component classify with the
  rule-16 verdicts `ADOPT-CONCEPT | ADAPT | REDESIGN | AVOID` (an `AVOID` verdict must
  state what replaces the component), with justification and dependency notes
  (for building an independent implementation).
- **Enterprise-readiness gap analysis** for the new product — **prioritized (new in v3)**:
  - **P0 — security and sandboxing** (deepest section; summarizes and links
    `07-security/threat-model.md` and `new-shell-security-blueprint.md`; do not re-derive).
  - **P1** — policy & governance, audit, multi-tenancy/isolation, secrets management,
    resource limits (CPU/memory/time/output), observability (structured logs, metrics,
    traces), deterministic/reproducible execution.
  - **P2** — supportability, versioning and compatibility guarantees (of the new
    language's own contracts), plug-in model, performance targets, memory/threading model,
    testability, packaging/updating, LTS strategy, accessibility/localization.
  - Each criterion: how PowerShell does it (cite evidence) and what it lacks, then a
    concrete recommendation for the new product.
- **`language-design-principles.md`** (replaces v2's compatibility strategy): the
  language-design principles for the new language, each derived from cited evidence —
  e.g., explicitness vs implicit coercion (link `CONVERSION-RULES.md`,
  `SEMANTIC-QUIRKS.md`), structured objects vs text (link `03-runtime/` docs), error
  semantics (`ErrorRecord` model vs exceptions), scoping model (`SCOPE-AND-VARIABLES.md`),
  formatting/output separation, module/extension model. Each principle: statement,
  evidence, verdict for the new language, consequences.
- **`new-language-design-canvas.md`** (new in v3): the working decision canvas for the
  new language — the single entry point a designer reads first after the pipeline map.
  Fill in the skeleton created at the start of Phase 2 (2.9).
  For each design area — lexical rules and tokens; keywords (reserved vs contextual);
  grammar shape (statement/expression split, pipelines as first-class); operators and
  precedence; type system and coercion policy; scoping and variables (including what
  replaces automatic variables); error model; pipeline semantics; module/extension model;
  command discovery and naming; security model; tooling hooks (completion, highlighting,
  debugging, LSP) — produce a table:
  `Area | PowerShell's choice (evidence) | Verdict (ADOPT-CONCEPT/ADAPT/REDESIGN/AVOID) |
  Rationale | Open decisions for the product owner`.
  Rows get stable IDs `NLD-<AREA>-<NNN>` registered in `ID-REGISTRY.md`. The canvas
  aggregates the `LESSON` tags from all subsystem documents (rule 16 scope) and must be internally
  consistent with `language-design-principles.md`.
- **Requirements trace** (`09-synthesis/requirements-trace.md`): each enterprise
  criterion (security first) -> PowerShell component/evidence -> proposed new-product
  component -> verification idea.
- **New-shell specification outline** (`09-synthesis/new-shell-spec-outline.md`):
  table of contents for the new product's **new-language spec**, runtime spec, API/ABI
  spec, extension model, and operational guide, each item linked to the source documents
  that feed it.
- **Proposed reference architecture** for the new shell (layer diagram, module boundaries,
  interface contracts), expressed as a mapping: `PowerShell component -> new component`.
- **`dotnet-runtime-integration.md`** (new in v3): how the new shell should sit on .NET:
  target framework and LTS policy; `Microsoft.Extensions.Hosting` (DI, configuration,
  structured logging, health checks) as the enterprise baseline PowerShell predates;
  OpenTelemetry observability baseline; threading model (PowerShell's sync-heavy pipeline
  vs async-first for the new shell — evidence-based trade-offs); GC and allocation
  strategy for pipeline objects (cost of a `PSObject`-like wrapper — evidence from the
  ETS documents); deployment modes (framework-dependent, self-contained, NativeAOT) and
  their consequences for the execution strategy chosen in 2.10; `AssemblyLoadContext`
  for module isolation and plugin loading; trimming/AOT-annotation rules; NuGet packaging
  and tool distribution (dotnet global tool model vs PowerShell's package model).
- **Licensing notes** (informational, not legal advice): MIT obligations, files from
  `ThirdPartyNotices.txt`, and a "clean-room vs derived-work" checklist that uses the
  `SPEC`/`IMPL`/`LESSON` tags.
- Deliverables: `09-synthesis/`.

---

## 7. OUTPUT STRUCTURE (mirror the source; standard, modular)

Two coordinated trees: `src-mirror/` is a strict 1:1 mirror of the real source layout
(fully generated skeleton, annotated by reading); the numbered folders are the thematic
architecture documents. Neither replaces the other.

```
docs-out/
├── README.md                      # index, how to read, version pin, reading order
├── PROGRESS.md                    # resumable checklist, task IDs (rule 4)
├── GLOSSARY.md                    # all terms, abbreviations, tag vocabularies
│                                  #   (SPEC/IMPL/LESSON, verdicts, FACT/INFERENCE/
│                                  #   UNVERIFIED/APPROX/GENERATED/VERSION-MISMATCH), ID schemes
├── DECISIONS.md                   # decisions made while documenting
├── VERIFICATION-BACKLOG.md        # all UNVERIFIED items
├── COVERAGE.md                    # coverage matrix (section 10)
├── TRACEABILITY.md                # source folder/project <-> documents, both directions
├── ID-REGISTRY.md                 # every stable ID (incl. SEC-ENF, NLD) and where defined
├── ACCEPTANCE-QUESTIONS.md        # cold-read test and answers (Appendix B)
├── 00-overview/
│   ├── repo-census.md
│   ├── source-tree-map.md
│   ├── project-dependency-graph.md
│   ├── external-dependencies.md
│   ├── fork-drift.md              # only if drift detected (section 2 step 3)
│   ├── layered-architecture.md
│   └── study-summary.md           # final counts + top-10 insights (section 11.5), written at the end
├── 01-repository/
│   ├── build-system.md
│   ├── ci-cd-and-packaging.md
│   └── coding-standards.md
├── 02-language/                   # deepest section
│   ├── 00-pipeline-map.md
│   ├── 02.1-tokenizer.md
│   ├── 02.2-parser.md
│   ├── 02.3-ast.md
│   ├── 02.4-semantic-analysis.md
│   ├── 02.5-compiler-and-engine.md
│   ├── 02.6-types-and-operators.md
│   ├── 02.7-language-features.md
│   ├── 02.8-language-tooling.md
│   ├── GRAMMAR.ebnf.md
│   ├── TOKEN-CATALOG.md
│   ├── AST-CATALOG.md
│   ├── OPERATOR-TABLE.md
│   ├── COMPILATION-MAP.md
│   ├── BINDER-CATALOG.md
│   ├── CONVERSION-RULES.md
│   ├── ERROR-CATALOG.md
│   ├── SCOPE-AND-VARIABLES.md
│   ├── STAGE-CONTRACTS.md
│   ├── CALL-GRAPHS.md
│   ├── LIFECYCLE-script-execution.md
│   ├── LANGUAGE-SPEC-DRAFT.md
│   ├── SEMANTIC-QUIRKS.md
│   ├── HOWTO-extend-language.md
│   ├── INTERPRETER-DESIGN-SPACE.md
│   ├── GOLDEN-SAMPLES.md
│   └── REFERENCE-TEST-CORPUS.md
├── 03-runtime/
│   ├── runspace-and-pipeline.md
│   ├── command-discovery-and-invocation.md
│   ├── cmdlet-infrastructure.md
│   ├── parameter-binding.md
│   ├── execution-context-and-session-state.md
│   ├── provider-model.md
│   ├── extended-type-system.md
│   ├── formatting-and-output.md
│   ├── modules.md
│   ├── errors-and-diagnostics.md
│   ├── jobs-and-concurrency.md
│   ├── debugger.md
│   ├── eventing.md
│   └── help-system.md
├── 04-hosting/        (host-abstraction.md, console-host.md, sdk.md)
├── 05-remoting/       (psrp-protocol.md, transports.md, serialization-clixml.md, jea.md)
├── 06-platform/       (windows-unix-split.md, native-interop.md)
├── 07-security/       (language-modes.md, execution-policy.md, amsi-logging.md,
│                       enforcement-points.md, threat-model.md,
│                       new-shell-security-blueprint.md)
├── 08-engineering/    (test-strategy.md, engineering-processes.md, localization.md)
├── 09-synthesis/
│   ├── architecture-decision-log.md
│   ├── reuse-map.md
│   ├── enterprise-gap-analysis.md
│   ├── language-design-principles.md
│   ├── new-language-design-canvas.md
│   ├── dotnet-runtime-integration.md
│   ├── requirements-trace.md
│   ├── new-shell-spec-outline.md
│   ├── reference-architecture.md
│   └── licensing-notes.md
├── 10-command-modules/            # one file per cmdlet/provider assembly family
│                                  #   named <AssemblyName>.md, plus _index.md
├── src-mirror/                    # STRICT mirror of the real tree
│   ├── src/
│   │   └── <Project>/
│   │       ├── _project.md        # project card (8.2)
│   │       └── <folder>/.../_folder.md   # folder card (8.3), one per source folder
│   ├── test/                      # same structure for test projects
│   └── tools/                     # same for build/tooling folders
├── data/                          # machine-extracted JSON/CSV (section 5.2) + golden/
│                                  #   + tierA-outlines/ + README.md (dataset schemas)
├── tools/                         # extraction, validation, and rendering scripts
└── .work/                         # environment, tiers, ledger, notes (resume state)
```

Rules for the trees:

- Folder and file names under `src-mirror/` equal the real folder names exactly.
- Adjust names of thematic folders/files only if the real source structure demands it, and
  record the change in `DECISIONS.md`.
- Every source folder that contains source files gets a `_folder.md`. Tier A and B cards
  are annotated by reading; Tier C cards may remain script-generated and carry the flag
  `GENERATED`.
- Each thematic document lists, in its Source map, the `src-mirror/` cards it covers,
  and each card links back to the thematic documents (maintained in `TRACEABILITY.md`).

---

## 8. DOCUMENT TEMPLATES

### 8.1 Subsystem document (mandatory sections, in this order)

Every document begins with front matter:

```
---
id: LANG-PARSER-001            # stable ID (see 8.4)
title: <Title>
kind: subsystem | catalog | guide | synthesis
tier: A | B | C
status: draft | verified | partial
version_pin: <tag or fallback> | commit <hash> | TFMs <...> | SDK <...>
pin_method: <how the version was derived>
sources: [<repo-relative paths covered>]
mirror_cards: [<src-mirror paths>]
generated_from: [<data/*.json files used>]
---
```

```
# <Title>

1. Purpose and scope                     [SPEC]
2. Source map            (table: path | type/class | role | tier)
3. Responsibilities and non-responsibilities
4. Key types and contracts   (public/internal interfaces, invariants)   [IMPL]
5. Data model            (structures, state, lifecycle)
6. Control flow          (Mermaid sequence/flowchart; ordered steps)
7. Algorithms            (stepwise; only where non-trivial)
8. Observable behavior   (what a user/script can observe; golden samples)   [SPEC]
9. Error handling and edge cases
10. Concurrency and threading
11. Extension points and customization hooks
12. Dependencies         (inbound / outbound, with paths)
13. Performance notes    (caching, allocation, hot paths)
14. Security considerations   (mandatory: trust assumptions, what this subsystem
                              enforces, `SEC-ENF` cross-links; write "no security
                              surface" only with justification)
15. Enterprise considerations   (P0 security first, then observability, supportability,
                                 testability, resource limits; what is missing)
16. Tests               (where it is specified/tested)
17. Design decisions and trade-offs   (FACT vs INFERENCE labelled)
18. Guidance for the new shell   (design lessons tagged
                                 ADOPT-CONCEPT | ADAPT | REDESIGN | AVOID,
                                 each evidence-linked; rule 16)
19. Open questions / UNVERIFIED items
Verification: <what was cross-checked and how; counts reconciled with data/>
```

Each section is tagged `SPEC`, `IMPL`, or `LESSON` where it matters (rules 13 and 16).
Sections that do not apply say "Not applicable" with the reason; they are never silently
dropped.

### 8.2 Project card (`src-mirror/<root>/<Project>/_project.md`)

```
# <ProjectName>
Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier
Purpose (2-3 sentences)
Top-level folders/namespaces (table with links to folder cards)
Public API surface summary (counts + notable types)
References (project/package) and who references it
Key files (top 10 by importance, with one-line role)
Related documents (links into 02..10)
```

### 8.3 Folder card (`src-mirror/.../<folder>/_folder.md`)

```
# <relative folder path>
Tier | Project | File count | LOC | Type count | Flags (GENERATED | ANNOTATED)
Purpose (1-3 sentences, evidence-based for Tier A/B)
Files (table: file | LOC | main types | role | covering document)
Subfolders (links)
Partial-class and conditional-compilation notes
Related documents (links into 02..10)
```

### 8.4 Conventions

- Mermaid for all diagrams (flowchart, sequenceDiagram, stateDiagram-v2, classDiagram).
- Tables for catalogs (token, AST, operator, parameter attribute, cmdlet, etc.),
  rendered from `data/`.
- Cross-link documents with relative links. Every claim links to evidence
  (format in rule 1).
- Stable IDs `<AREA>-<TOPIC>-<NNN>`: `LANG-PARSER-001`, `RT-BIND-004`, `SEC-ENF-012`,
  etc. Register all in `ID-REGISTRY.md`. Never reuse or renumber an ID.
- Design-canvas row IDs use fixed area codes: `NLD-LEX`, `NLD-GRM`, `NLD-OP`, `NLD-TYP`,
  `NLD-SCP`, `NLD-ERR`, `NLD-PIP`, `NLD-MOD`, `NLD-CMD`, `NLD-SEC`, `NLD-TOOL`,
  `NLD-RUN` (execution strategy / runtime). A new area code is registered in
  `ID-REGISTRY.md` before its first use.
- `LESSON` verdicts (`ADOPT-CONCEPT | ADAPT | REDESIGN | AVOID`) and design-canvas rows
  (`NLD-*`) are first-class registered artifacts, not prose decorations.
- Documents longer than 1,500 lines are split into numbered parts with an index.
- Each document ends with its **Verification** line.

---

## 9. SUBAGENT CONTRACT

Subagents are mandatory for Phases 2-4 (including all of `10-command-modules/`). Run
at most 4-6 in parallel to keep quality high.

**Every subagent task prompt must contain:**

1. Task ID, scope (exact paths), tier, and the list of files it owns for writing.
2. The evidence and tagging rules (section 3), the reading protocol (4.2), the template
   (section 8), the product brief (section 1.1), and the relevant `data/` files.
3. Required outputs (document paths) and the definition of done:
   proposed `.work/files-ledger.csv` row updates included in the report (the
   coordinator merges them — subagents never write shared files), no `TODO`, all
   catalogs rendered from `data/`, guidance section (template section 18) filled with
   tagged lessons, Verification line filled in.
4. Hard limits: write only to its own output files and `.work/notes/`; do not edit shared
   files (`PROGRESS.md`, `GLOSSARY.md`, `ID-REGISTRY.md`, `DECISIONS.md`,
   `VERIFICATION-BACKLOG.md`, `TRACEABILITY.md`); do not modify source.

**Every subagent returns:** a short report with (a) files written, (b) new glossary terms,
(c) new IDs (including `SEC-ENF`/`NLD`), (d) cross-document dependencies it found,
(e) `UNVERIFIED` items, (f) decisions it made, (g) ledger coverage percentage for its
scope.

**The coordinator** merges those reports into the shared files, resolves terminology
conflicts, and updates `PROGRESS.md` after each subagent finishes.

**Review subagents** are separate from authoring subagents and re-read each Phase 2,
Phase 3, and Phase 5 document against the source and `data/` (section 10, item 5).

---

## 10. QUALITY GATES

Before declaring done:

1. **Path validator:** write `docs-out/tools/validate-refs.ps1` that extracts every
   repo-relative path and `file::Type.Member@Lx-Ly` reference from the documents and
   checks — after confirming with `git rev-parse HEAD` that the working tree is exactly
   at the pinned commit — that the file exists, the type/member exists, and the line
   range is plausible. Run it; fix all failures; keep the script in the output.
2. **Link and diagram validator:** check that all relative links resolve, all IDs in
   front matter are unique and registered, and (if Mermaid CLI is available) that every
   Mermaid block renders; otherwise run a basic syntax lint and record the limitation.
3. **Coverage matrix** (`COVERAGE.md`): every `.csproj`, every source folder, and every
   file in the ledger maps to at least one document or card; Tier A files show 100%
   lines read; list anything uncovered with the reason.
4. **Catalog completeness checks:** AST-CATALOG covers **all** classes deriving from the
   AST base type (counts from `ast-hierarchy.json` and from reflection when available);
   TOKEN-CATALOG covers all token kinds and flags; OPERATOR-TABLE covers all operator
   tokens; ERROR-CATALOG covers all parser error resource keys; cmdlet inventories match
   `cmdlets.json`; every row of `enforcement-points.json` carries a `SEC-ENF` ID that is
   registered in `ID-REGISTRY.md`. Give counts and reconcile every difference.
5. **Second-pass review:** separate review subagents re-read each Phase 2, Phase 3, and
   Phase 5 document against the source and return discrepancies in their report (they
   write no shared files; the coordinator records them in `VERIFICATION-BACKLOG.md`);
   fix them or mark `UNVERIFIED`. For Phase 5, additionally verify that every claimed
   enforcement point exists in the source exactly as cited.
6. **Consistency pass:** terminology matches `GLOSSARY.md`; no contradictory statements
   across documents; diagrams match text; `SPEC`/`IMPL`/`LESSON` tags are present; the
   design canvas agrees with the `LESSON` tags in the subsystem documents, and the
   per-verdict counts (`ADOPT-CONCEPT`/`ADAPT`/`REDESIGN`/`AVOID`) match between the
   subsystem documents and the canvas.
7. **Cold-read test:** a fresh subagent that has access **only** to `docs-out/` (not to
   the source) answers every question in `ACCEPTANCE-QUESTIONS.md` (Appendix B). A second
   reviewer checks each answer against the source. Every wrong or "cannot answer" result
   produces a fix in the documents; repeat until all pass or the remainder is recorded as
   `UNVERIFIED`.
8. **Interpreter-readiness review (new-language gate, new in v3):** a fresh subagent with
   access only to `docs-out/` must be able to (a) state the recommended execution
   strategy for the new shell with rationale, (b) enumerate the stage contracts and the
   data handed across each boundary, (c) list the security gates that must exist at
   script-execution time, and (d) draft the design-canvas rows for 5 core flows (literal,
   variable, command invocation, pipeline, error). Any failure is fixed in the documents.
9. **Source integrity:** `git status --porcelain` shows changes only under `docs-out/`.
10. **Finalize** `README.md` (index + reading order for an architect building the new
    shell: 00 -> 01 -> 02 -> 03 -> 07 -> 09 as the core path, with 07 (security
    blueprint) mandatory before any sandboxing/policy design, 04-06/08/10 as needed,
    and `src-mirror/` cards for drill-down) and `PROGRESS.md` (all green).

---

## 11. EXECUTION PROCEDURE

1. First action: run the environment preflight (section 2, including fork-base pinning)
   and Phase 0 discovery, then write `PROGRESS.md` with the full checklist derived from
   the *real* project and folder list, including one task per folder card group and per
   document.
2. Proceed phase by phase. For Phase 2, process stages in pipeline order, and at the end
   write the lifecycle document that stitches them together.
3. Spawn subagents for independent modules (Phases 2-4) under section 9, merge outputs,
   and run the quality gates.
4. After each completed document: update `PROGRESS.md` and the ledger, then continue
   automatically.
5. At the end, print a short summary: documents produced, counts (projects, folders,
   types, AST nodes, token kinds, operators, parser error IDs, cmdlets, enforcement
   points), ledger coverage per tier, `UNVERIFIED` count, acceptance-question pass rate,
   and the top 10 insights most relevant to building a new language and interpreter
   on .NET. Persist the same summary as `00-overview/study-summary.md` so it survives
   the session, and list the highest-risk `VERIFICATION-BACKLOG.md` entries there.

Begin now with section 2 (preflight), then Phase 0.

---

## APPENDIX A — SOURCE-TREE HINT MAP (hints to verify, never facts)

Layouts below are commonly seen in recent PowerShell releases. Confirm each in the real
tree; correct mismatches in `DECISIONS.md`.

| Area | Where to look first (verify) |
|---|---|
| Engine core assembly | `src/System.Management.Automation/` |
| Tokenizer, parser, AST, visitors, semantic checks, type resolver, variable analysis | `src/System.Management.Automation/engine/parser/` |
| Compiled execution, binders, runtime operations, script blocks | `src/System.Management.Automation/engine/runtime/` (and subfolders for binding/operations) |
| Interpreter / light compiler | `src/System.Management.Automation/engine/runtime/interpreter/` (verify; look for `Interpreter.cs`, `LightCompiler.cs`) |
| Runspace, pipeline, command processors | `src/System.Management.Automation/engine/` (files like `Runspace*`, `Pipeline*`, `CommandProcessor*` — verify) |
| Host interfaces | `src/System.Management.Automation/engine/hostifaces/` |
| Remoting (PSRP) | `src/System.Management.Automation/engine/remoting/` |
| Modules, session state, command discovery, completion, debugger | `engine/Modules/`, `engine/SessionState*`, `engine/CommandDiscovery/`, `engine/CommandCompletion/`, `engine/debugger/` |
| Providers and namespaces | `src/System.Management.Automation/namespaces/` |
| Formatting and output | `src/System.Management.Automation/FormatAndOutput/` |
| Help, security, utilities, logging, CIM/DSC support | `help/`, `security/`, `utils/`, `logging/`, `cimSupport/`, `DscSupport/` |
| Console host | `src/Microsoft.PowerShell.ConsoleHost/` |
| Cmdlet assemblies | `src/Microsoft.PowerShell.Commands.Management/`, `Microsoft.PowerShell.Commands.Utility/`, `Microsoft.PowerShell.Security/`, `Microsoft.PowerShell.Commands.Diagnostics/`, `Microsoft.WSMan.*`, CIM cmdlets, markdown rendering |
| Entry-point projects / packaging shims | `src/powershell-win-core/`, `src/powershell-unix/`, global tool shim |
| Code generators and build helpers | resource generation, type-catalog generation, version-info source generator, `tools/` |
| Native code | native shim / native library folders under `src/` |
| Tests | `test/xUnit/`, `test/powershell/` (Pester), `test/tools/`, `test/perf/`, hosting tests |
| Build/CI | `build.psm1`, `.pipelines/`, `.vsts-ci/`, `.github/`, `tools/releaseBuild/` |

---

## APPENDIX B — ACCEPTANCE QUESTIONS (seed list; extend to at least 60)

Create `docs-out/ACCEPTANCE-QUESTIONS.md` from this list (plus questions you add for
every Phase 3-5 subsystem until the file holds at least 60 questions). The cold-read
reviewer must answer each using only `docs-out/`, with citations. Questions 29-46 are
new in v3 (stage contracts, interpreter/.NET, and security focus); questions 47-54 were
added in the v3.1 revision to cover runtime subsystems, startup, and experimental
features.

1. List every token kind and mark which ones are keywords, operators, and literals.
2. How does the tokenizer decide between command mode and expression mode at the start of
   a statement and after each token?
3. Give the complete operator precedence and associativity table.
4. Which AST node represents each of `??`, `?.`, `?:`, `&&`, `||`, and how is each compiled?
5. How are `$using:`, `$script:`, and `$local:` resolved, and at which stage?
6. What does the parser return after a syntax error (partial AST? tokens skipped?) and
   which synchronization points does it use?
7. What is the full command resolution order and where is it implemented?
8. State the parameter binding algorithm as ordered steps, including parameter-set
   resolution and mandatory prompting.
9. How and when does a script block get compiled, which strategy is chosen
   (compiled vs interpreted), and what caches exist?
10. How do the dynamic binders resolve method overloads and convert arguments?
11. State the conversion order used by `LanguagePrimitives` for an arbitrary
    `source -> target` request.
12. How is a `class` compiled into a runtime type, step by step?
13. How are pipeline chain operators represented in the AST and executed?
14. How are scopes and variables stored at runtime (slots, tuples, dynamic tables)?
15. List every place where constrained language mode is enforced.
16. Trace `pwsh -c "1+1"` from process start to output, naming each class and method.
17. What are the CLIXML type-fidelity rules for serialization and deserialization?
18. What is the minimal contract a new host must implement?
19. How are native command arguments built, and how are encoding and redirection handled?
20. How does `SafeGetValue` decide what is a safe constant expression?
21. Which tests specify here-string behavior? List paths and counts.
22. How is a format view selected for an object?
23. List, in order, every file and method to touch to add a new binary operator.
24. Where are sequence points created and how do breakpoints map to them?
25. Which parts of the engine differ by platform, and how is the split implemented?
26. What are the enterprise gaps in the audit/logging design, with evidence?
27. Which PowerShell semantics are tagged `LESSON-AVOID` and why?
28. Which component is classified `REDESIGN` in the reuse map, and what replaces it?
29. What exact data does each pipeline stage hand to the next, and where is each contract
    defined in code? (Use `STAGE-CONTRACTS.md` and cite the source.)
30. What is the contract for errors at each stage boundary (`ParseError` vs
    `RuntimeException` vs `ErrorRecord`), and where does each arise?
31. Which execution strategies are viable under NativeAOT on .NET, and which of them does
    PowerShell's own design most resemble?
32. How are dynamic call-site caches structured and invalidated, and what should the new
    shell cache instead?
33. What instructions does the light-compiler interpreter execute, and how complete is its
    coverage compared with the compiled path?
34. Where exactly is each language mode enforced, and which enforcement points rely on
    voluntary in-process checks?
35. What audit and logging hooks exist (script block logging, transcription, module
    logging), which events do they capture, and what is missing for enterprise audit?
36. How does CLIXML/PSRP deserialization protect against malicious type reuse?
37. How are runspaces isolated from each other within one process, and where does that
    isolation end?
38. What is the performance cost structure of `PSObject`/ETS adaptation on hot paths
    (evidence from code structure; label inference), and what should the new shell's
    object model do differently?
39. In what order does `LanguagePrimitives` try converters, and where do the surprising
    coercions enter?
40. How are automatic variables bound and updated, and what cleaner mechanism could
    replace them in the new language?
41. Which PowerShell behaviors look like implementation accidents rather than deliberate
    design? Tag each, with evidence (comments, tests, docs).
42. How do Ctrl-C, `StopProcessing`, and pipeline stop propagate through native and cmdlet
    commands, and what must the new interpreter guarantee for cancellation?
43. Which engine features exist purely to support tooling (extents, sequence points,
    completion APIs, error positions), and how should the new language design these in
    from day one?
44. Which enterprise hosting capabilities (DI, configuration, structured logging, health
    checks) does PowerShell's host model lack, and how would `Microsoft.Extensions.*`
    fill them in the new shell?
45. What resource limits (memory, CPU, time, output size, concurrent pipelines) does
    PowerShell enforce today, and where would a resource governor hook in?
46. Based on the command lifecycle, where would a deny-by-default policy engine place its
    decision points with minimal invasive surface?
47. How does provider path resolution work (drives, wildcards, home/current-location
    semantics), which provider capabilities exist, and how does dynamic provider
    parameter handling work?
48. How does module auto-loading find and cache commands, what invalidates that cache,
    and how do manifest fields (exported functions/cmdlets/aliases) drive discovery?
49. In what exact order does the ETS resolve a member (adapter order, type-extension
    XML, `PSObject` members), and where is `TypeTable` built and cached?
50. How do jobs, thread jobs, and `ForEach-Object -Parallel` differ in session/runspace
    isolation, and exactly which state is shared or copied?
51. Which engine events exist, how are subscriber actions stored and invoked, and what
    throttling/queue limits apply?
52. How is help (comment-based and cmdlet XML/MAML) discovered and bound to a command,
    and how does updatable help replace it?
53. Where are experimental features declared, gated, and enabled, and at which pipeline
    stages can a feature change parse or runtime behavior?
54. What does the full startup sequence do before the first prompt (SDK probe, profile
    loading, module scan, telemetry init), and which parts would the new shell cut or
    defer for fast startup?
