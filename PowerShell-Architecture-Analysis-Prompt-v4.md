# PowerShell Source — Forensic Architecture Study (Claude Code Master Prompt v4.0)

> Usage: run Claude Code inside the root of the **local clone** of the repository
> (the private fork `github.com/sharafee/PowerShell`, e.g. `D:\dev\PowerShell`),
> place this file there, and tell Claude Code:
> "Read PowerShell-Architecture-Analysis-Prompt-v4.md fully, then execute it."
> This prompt needs a real filesystem, shell, and subagents. It is NOT suitable for a
> chat that only receives selected files (for example claude.ai project knowledge).
> Output goes to `OUT_DIR` (default `docs-out/`) at the repo root; in this prompt
> `docs-out/` always means `OUT_DIR/`. Builds and experiments happen only in a scratch
> copy outside the repo (section 2). Never modify `src/`, `test/`, or `tools/`.
> Do not assume the fork is reachable on the public internet; everything must work
> offline against the local clone (NuGet restore excepted, section 2).
> **Prerequisites are installed by the repository owner BEFORE the run; the agent never
> installs anything:** `git`, `rg`, the .NET SDK required by `global.json` (or a
> roll-forward-compatible one) and, strongly recommended, an installed `pwsh` of nearly
> the same version. Without a usable SDK the run stops after Phase 0 unless
> `ALLOW_STATIC_ONLY=true` (section 2, item 8).

> **Run parameters** (the owner may override them in the invoking message; otherwise the
> defaults apply and are recorded in `.work/environment.md`):
>
> | Parameter | Default | Meaning |
> |---|---|---|
> | `REPO_ROOT` | current directory | root of the local clone |
> | `OUT_DIR` | `docs-out` | output tree |
> | `SCRATCH_DIR` | `../ps-scratch` | scratch copy for builds and oracle runs (section 2) |
> | `TARGET_PROFILE` | `P-FAITHFUL` | the only supported profile in v4 (section 1.3) |
> | `ALLOW_STATIC_ONLY` | `false` | if `true`, the run may continue without a built engine: every behavior claim stays `UNVERIFIED`, every document carries `run_verification: none`, and the final acceptance status is at most `CONDITIONAL` (gate 14) |
> | `DOC_LANGUAGE` | `en` | language of all authored documents |
> | `FA_DIGEST` | `false` | if `true`, Phase 9 produces a Persian digest (derived, non-authoritative) |

> **What changed from v3.1** (context for the repository owner — NOT execution
> instructions). v4.0 removes defects found in v3.1 itself and in the study outputs
> produced with it:
> 1. **Target stance made consistent with the real goal.** v3.1 said "new language from
>    scratch, no PowerShell compatibility" while the product is a PowerShell-faithful
>    interpreter and compiler. v4 defines Target Profile `P-FAITHFUL` (section 1.3):
>    observable behavior is `REPLICATE` by default; every departure is a registered
>    deviation proposal (`DEV-*`) that only the owner can approve.
> 2. **One verdict vocabulary.** v3.1 still carried three (`ADOPT-CONCEPT/ADAPT/REDESIGN/AVOID`,
>    `LESSON-RETAIN/AVOID/OPTIONAL`, `DROP`) plus a mapping between them. v4 has exactly
>    `REPLICATE | ADAPT | REDESIGN | AVOID` (rule 16).
> 3. **Evidence hierarchy that includes execution.** v3.1 called the repo the only source
>    of truth yet required running the engine; v4 defines evidence classes E1-E4 with
>    precedence (rule 1) and makes the behavioral oracle mandatory (5.4) unless the owner
>    sets `ALLOW_STATIC_ONLY=true`.
> 4. **Contradictions are mechanically detectable:** one pin (`pin.json`), a numbers
>    registry, canonical facts with a single owner document (SSOT), a claim ledger with
>    conflict check, a controlled vocabulary, and a computed document status
>    (rules 3, 11, 18-21; gate 6).
> 5. **Execution-engine fidelity deliverables** (`IR-SPEC`, `INSTRUCTION-SET`,
>    `TIERING-POLICY`, `EQUIVALENCE-SPEC`, `ORACLE-PROTOCOL`) and a rule-based
>    interpreter-strategy evaluation (2.10) that yields one recommendation per
>    deployment constraint instead of a pre-decided answer.
> 6. **Rebuild plan, deviation register, feature scope matrix**
>    (`implementation-blueprint.md`, `deviation-register.md`, `FEATURE-MATRIX.md`).
> 7. **Environment realism:** no OS assumption, a tool-language preference order, and
>    explicit hard stops (section 2, item 8) instead of silently degrading to static analysis.
> 8. **Gates:** bounded rerun cycles, a computed acceptance status
>    (`ACCEPTED | CONDITIONAL | REJECTED`), new gates for behavior, equivalence,
>    rebuild-readiness and contradiction closure.
> 9. **v3.1 inconsistencies fixed:** acceptance-question counts (46 / 54 / 60 became seeds
>    1-54 plus v4 additions, minimum 100), the interpreter-folder hint in Appendix A,
>    the undefined `verified` status, and unbounded review loops. Appendix C lists
>    discrepancies between earlier study outputs that must be resolved by evidence.

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
  shell") with **its own interpreter and compiler** (tokenizer, parser, AST, semantic
  analysis, compiler, interpreter/tiering, runtime, pipeline, type system, providers,
  security, hosting, remoting, tooling).
- **Implementation stack:** .NET / C# on a current LTS runtime (.NET 8 or newer). The
  new shell is a managed .NET application; every implementation recommendation must be
  actionable for a C# team.
- **Language stance (v4):** the new shell is **PowerShell-faithful in architecture and in
  the observable behavior of the language core** (section 1.3), implemented clean-room.
  Domain-specific parts (cmdlet set, providers, formats, file extensions, names,
  messages) are replaceable. It is not a fork. Binary/API compatibility with
  `System.Management.Automation` and byte-level `.ps1` compatibility are not goals;
  fidelity is measured against golden samples (5.4), not against a version number.
- **Two P0 axes that do not compete.** (a) **Fidelity and buildability:** the language
  pipeline and execution engine are specified at rebuild grade. (b) **Security and
  sandboxing:** the product will run untrusted and semi-trusted scripts in enterprise
  environments, so every subsystem document exposes the security surface of the
  corresponding PowerShell subsystem and states what the new shell must do instead or in
  addition. Axis (a) decides what the documents must specify; axis (b) decides which extra
  guarantees the product adds; neither changes the phase order.
- PowerShell (this repository) is the **reference implementation**: study what it does,
  why it works, where it hurts. Where it hurts, the study *proposes* deviations
  (rule 22); it never silently decides them.

### 1.2 What this means for the study

- Cover the **entire codebase at architecture level** (structure, responsibilities,
  contracts, dependencies, data flow, extension points, design decisions).
- Cover the **language pipeline at DEEP, exhaustive level**:
  `source text -> tokens -> parser -> AST -> semantic checks -> compilation/interpretation -> runtime execution`.
  A reader must be able to re-implement each stage's behavior from the documents alone;
  for `CORE` scope (section 4.3) this is verified by golden samples, not by reading.
- Extract **design lessons**: for every mechanism, record the verdict
  `REPLICATE | ADAPT | REDESIGN | AVOID` (rule 16) with evidence. `REDESIGN` and `AVOID`
  are only ever proposals (rule 22).
- Do **NOT** write line-by-line explanations of individual cmdlet implementations.
  Cmdlet assemblies are documented as module families (what they provide, how they plug
  into the engine, a mechanically extracted cmdlet inventory), not function by function.
- The documentation must **mirror the source organization exactly**
  (solution -> project -> folder -> namespace/file -> type) so every document maps
  directly to a place in the source tree, and every source folder maps to a document.
  In addition it provides thematic architecture documents on top of that mirror.
- Documents are **modular**: one subsystem or one catalog per file, stable IDs,
  relative links, a fixed template, no monolithic files.

### 1.3 Target Profile `P-FAITHFUL`

- **F1 — Default is replication.** Every observable behavior of the language core and
  engine is `REPLICATE` unless an `APPROVED` deviation (`DEV-*`) says otherwise.
- **F2 — Deviations are proposals.** The study may only write deviation rows with status
  `PROPOSED`. `APPROVED` / `REJECTED` are set by the product owner outside this run.
  Until approved, all documents and the implementation blueprint describe the baseline
  (PowerShell) behavior (rule 22).
- **F3 — Default scope classes (proposal; the owner finalizes in `FEATURE-MATRIX.md`).**
  `CORE`: tokenizer, parser, AST, semantic checks, variable analysis, compiler,
  interpreter/tiering, runtime operations and binder semantics, `LanguagePrimitives`
  conversions and operators, scope and variables, flow control, errors and streams,
  pipeline and command processors, command discovery, parameter binding, cmdlet base
  lifecycle, script/function/filter/advanced-function semantics, session-state basics,
  script modules and manifests (load, export), the minimal Extended Type System needed
  for member resolution, sequence points as far as error positions need them.
  `EXTENDED`: classes and enums, providers, formatting and output, help, debugger,
  jobs and parallel execution, eventing, host abstraction, console host/REPL, tab
  completion. `OUT-OF-SCOPE-DOCUMENTED`: remoting (PSRP, WSMan, SSH, JEA), DSC/configuration,
  workflow remnants, CIM/WMI adapters, COM interop.
- **F4 — Fidelity evidence.** A `CORE` behavior counts as specified only when it has
  (i) a stated rule (a CF or a decision-table row), (ii) at least one golden sample per
  rule produced by the oracle (`FACT-RUN`, 5.4), and (iii) the repo tests that cover it
  (from `tests.json`) or an explicit "no test" note.
- **F5 — Terminology** is fixed by rule 21.

### 1.4 Definition of done: no ambiguity, no contradiction

The output is accepted only if all of these measurable properties hold (gates in section 10):

- **D1** one pinned commit everywhere (rule 3);
- **D2** every critical fact has exactly one canonical statement and one owner document (rule 18);
- **D3** every count and source constant comes from the numbers registry (rule 11);
- **D4** every factual statement carries exactly one epistemic label and no `UNVERIFIED`
  remains in `CORE` scope except as a `BLOCKED` backlog entry with an owner-actionable fix (rule 19);
- **D5** a document's `status` is computed, never self-declared (rule 20);
- **D6** the contradiction register has no `OPEN` rows (rule 23);
- **D7** one controlled vocabulary, enforced by lint (rule 21);
- **D8** a reader who has only `docs-out/` answers the acceptance questions correctly (gate 7);
- **D9** a reader who has only `docs-out/` can draft the interface skeleton and test plan for the
  first milestones of the rebuild without having to guess (gate 11).

---

## 2. ENVIRONMENT AND PRECONDITIONS (do this before Phase 0)

1. **Host:** do not assume the OS. Detect it and record in `docs-out/.work/environment.md`:
   OS and version, `git`, `rg` (ripgrep), `dotnet --list-sdks`, `pwsh` (version),
   `powershell.exe`, `cloc`, `python3`, `node`/`mmdc` (Mermaid CLI). Tool implementation
   language, in order of preference: (a) a `dotnet` console tool, (b) a PowerShell 7
   script, (c) a Python 3 script (only when neither (a) nor (b) is possible; record the
   reason in `DECISIONS.md`). Tools must run on the detected host without admin rights.
   Put them in `docs-out/tools/`; every tool starts with a header comment: purpose,
   inputs, outputs, run command, language, host it was tested on.
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
   copy the repo to `SCRATCH_DIR` (default `../ps-scratch/`, outside the repo) and work there. Never create
   `bin/`, `obj/`, or packages inside the analyzed repo. Before finishing, run
   `git status --porcelain` and confirm only `docs-out/` changed.
5. **No machine-wide changes.** The agent never installs software or changes system state
   (no `Start-PSBootstrap`, installers, `winget`, `choco`, `apt`, `brew`). Use plain
   `dotnet restore/build` in the scratch copy. Network access is allowed only for NuGet
   restore and for fetching tool packages (for example Roslyn) in the scratch copy; log
   each use in `DECISIONS.md`. If the SDK required by `global.json` is missing and cannot
   be used via roll-forward, apply the hard stop in item 8.
6. **Never execute repo scripts you have not read.** Read first, run only your own tools.
7. Preflight result: write `docs-out/.work/environment.md` and the first `PROGRESS.md`
   before starting Phase 0.
8. **Hard stops and blocked work (replaces silent degradation).** The run never asks
   clarification questions (rule 10), but it must write `docs-out/BLOCKED.md` (cause,
   evidence, exact fix command for the owner) and finish only the work that does not
   depend on the blocker, in these cases:
   a. no usable .NET SDK and `ALLOW_STATIC_ONLY=false`;
   b. a validator runs while the working tree is not exactly at the pinned commit (rule 3);
   c. `git status --porcelain` shows changes outside `docs-out/` that this run did not
      cause (report them, never clean them);
   d. the engine cannot be built after the documented fallbacks (restore errors, TFM
      mismatch) and `ALLOW_STATIC_ONLY=false`.
   With `ALLOW_STATIC_ONLY=true` the run proceeds, every document carries
   `run_verification: none` and the banner `STATIC-ONLY — behavior not run-verified`,
   and gate 9 is reported `WAIVED`, which caps the acceptance status (gate 14).

---

## 3. OPERATING RULES (non-negotiable)

1. **Evidence only, with an evidence hierarchy.** Every claim must cite evidence: for
   source evidence a repo-relative file path plus class/method name and line range,
   `src/<Project>/<path>.cs::Type.Member@L120-L188`; for run evidence a golden-sample ID
   `GS-<AREA>-<NNN>` (5.4). Evidence classes:
   - `E1 source` — the pinned working tree (design, structure, implementation: `IMPL`).
   - `E2 run` — execution of an engine **built from the pinned commit** in the scratch copy
     (observable behavior: `SPEC`).
   - `E3 run-mismatch` — execution on an installed `pwsh` of a different version (flag
     `VERSION-MISMATCH`; supports a claim, never proves it alone).
   - `E4 external` — documentation, blogs, .NET docs (flag `EXTERNAL`; cross-check only).

   Precedence on conflict: for **observable behavior** `E2` beats a reading of `E1` (a
   reading that disagrees with a run is wrong or incomplete: open a `CON-` entry, rule 23);
   for **design and implementation** `E1` beats comments and XML docs (comments are
   evidence of intent only); `E3` and `E4` never override `E1`/`E2`. If you did not read
   or run it, do not state it: tag it `UNVERIFIED` and add it to
   `docs-out/VERIFICATION-BACKLOG.md`.
2. **Never trust memory of the repo layout.** Discover the real layout with tools. Every
   file name, folder, type, method, number, or claim named in this prompt (including
   Appendices A, C and D) is only a **hint to verify**, never a fact. If a hint is wrong,
   record the real answer in `DECISIONS.md`.
3. **Pin once, use everywhere.** Phase 0 writes `.work/pin.json` (version tag or fallback,
   commit hash, target frameworks, SDK from `global.json`, how the pin was derived).
   Every document's front matter (8.1) is generated from this file, never typed. All
   front matters must be identical in these fields (gate 6g). A second commit hash
   anywhere in the output is a defect.
4. **Self-resumable.** Maintain `docs-out/PROGRESS.md` (phases, modules, task IDs, status,
   open questions). Update it after every document. If context is lost or the session
   restarts, resume from this file and `docs-out/.work/`. Write each document to disk as
   soon as it is finished.
5. **Scale with subagents** under the contract in section 9: one subagent per
   module/subsystem/stage, each writing only its own files, then a consolidation pass.
6. **Read-only on source.** Do not modify, reformat, or delete anything outside
   `docs-out/` (and the scratch copy).
7. **No assumptions about intent.** Describe what the code does; label inferences about
   *why* as `INFERENCE` and keep them separate from facts.
8. **Quote sparingly.** Short code excerpts (max ~15 lines) only when they are the
   clearest evidence. Prefer references and paraphrase. Documents must describe behavior
   in your own words so they can support a clean-room re-implementation.
9. **Language of documents:** `DOC_LANGUAGE` (default English, technical), consistent
   terminology defined in `GLOSSARY.md`. Use real identifiers exactly as in source
   (case, namespace).
10. **No clarification questions; hard stops instead.** Make the best evidence-based
    decision, record it in `docs-out/DECISIONS.md`, and continue — except in the hard-stop
    cases of section 2, item 8.
11. **Mechanical over manual; numbers come from data.** Anything countable (types, enum
    members, AST classes, token kinds, operators, resource keys, cmdlets, tests, project
    references, LOC) and every constant taken from the source (thresholds, limits,
    defaults, maximum counts) must be produced by a script into `docs-out/data/` and
    rendered into the documents from that data. Never hand-type a catalog (section 5).
    Registered numbers live in `data/numbers.json` (key, value, dataset, generation
    command, evidence class, label). Documents embed them as `<!--N:KEY-->value<!--/N-->`;
    `tools/render-numbers` fills the value and `tools/lint-numbers` fails on a hand-typed
    count or a stale embed (gate 6b). Values from `APPROX` extraction may enter
    `numbers.json` only when flagged, and any document using them has status `partial`.
12. **Completeness over brevity.** When a document or catalog promises "every X", list
    every X. No summarizing by omission. If a catalog is too large for one file, split it
    into parts (`-part-01.md`, ...) with an index file.
13. **SPEC / IMPL / LESSON tagging.** Tag every section as one of:
    `SPEC` — observable language/runtime behavior, independent of how PowerShell
    implements it (the clean-room basis for the new shell);
    `IMPL` — how this source implements it;
    `LESSON` — a design lesson for the new shell, always citing the evidence it derives
    from and carrying a verdict per rule 16.
    A new product must be buildable from `SPEC` + `LESSON` without copying `IMPL`.
    These tags describe the *kind* of a section; the epistemic labels of rule 19
    describe the *certainty* of a statement. They are orthogonal.
14. **Evidence boundary.** The pinned repository and the engine built from it are the only
    sources of truth for PowerShell behavior (rule 1). External documentation
    (learn.microsoft.com, .NET docs, blogs) may be used only as a clearly labelled
    `EXTERNAL` cross-check and never as evidence of behavior of this version. The same
    applies to claims about current .NET capabilities (NativeAOT, `AssemblyLoadContext`):
    label them `EXTERNAL` and keep them separate from repo evidence. If the network is
    unavailable, keep the `EXTERNAL` claim but add a `VERIFICATION-BACKLOG.md` entry
    recording that it could not be cross-checked online.
15. **Conditional compilation matters.** Types and members may exist only under `#if`
    symbols (platform, framework, feature flags). Record the symbol set per project and
    mark platform-conditional items in every catalog.
16. **One verdict vocabulary.** Every document using the template in 8.1 (all subsystem
    documents: Phases 2-6 and the command-module families) must end its guidance section
    (template section 18) with explicit lessons for the new shell, each carrying exactly
    one verdict, tied to evidence in the same document:
    - `REPLICATE` — the new shell reproduces the observable behavior **and** the essential
      mechanism. Default for `CORE` scope.
    - `ADAPT` — the new shell reproduces the observable behavior with a different internal
      mechanism (state why; example: hand-rolled call-site caches instead of the DLR).
      In effect without owner approval because observable behavior is unchanged.
    - `REDESIGN` — observable behavior is intentionally different. A deviation *proposal*
      only: exactly one `DEV-*` row (rule 22).
    - `AVOID` — the feature or mechanism is omitted; state what replaces it, if anything.
      A deviation *proposal* only: exactly one `DEV-*` row.

    These four are the **only** lesson vocabulary in the whole study. Legacy tags in earlier
    drafts map as follows: `ADOPT-CONCEPT` -> `REPLICATE` (behavior and mechanism kept) or
    `ADAPT` (mechanism changed); `LESSON-RETAIN` -> `REPLICATE`/`ADAPT`; `LESSON-AVOID` ->
    `AVOID`; `LESSON-OPTIONAL` -> an open `PROPOSED` deviation; `DROP` -> `AVOID`.
    Neutral observations need no verdict tag.
17. **Clean-room discipline.** Documents must enable a clean-room implementation of the new
    shell: describe behavior and design conceptually; never embed source code beyond the
    short evidence excerpts allowed by rule 8; keep licensing/attribution analysis in
    `09-synthesis/licensing-notes.md`. Product-bound artifacts (design canvas, security
    blueprint, reference architecture, implementation blueprint) must be understandable
    and usable without re-reading the PowerShell source.
18. **Single source of truth (SSOT) for critical facts.** A critical fact has exactly one
    canonical statement in `data/canonical-facts.json` (`CF-<AREA>-<NNN>`: subject,
    statement, label, evidence, owner document, status `open | closed`) and exactly one
    owner document (Appendix D lists the minimum set). Every other document links to it
    (`[CF-CMP-001]`) or embeds it only through `<!--CF:ID-->…<!--/CF-->` blocks rendered by
    `tools/render-canonical`; hand-restating a critical fact is forbidden. If two documents
    need different wording because their scopes differ, the registry holds two CFs with
    explicit scopes — never two statements of one fact. Any fact stated in more than one
    document becomes a CF.
19. **Claim labels.** Every factual statement carries exactly one label (inline for
    non-trivial claims, or per block when a whole block shares it): `FACT-SRC` (evidence
    `E1`), `FACT-RUN` (evidence `E2`), `INFERENCE`, `EXTERNAL`, `UNVERIFIED`. Optional
    modifiers: `APPROX` (regex/heuristic extraction), `GENERATED` (rendered from data),
    `VERSION-MISMATCH` (`E3`). Authoring subagents also write each non-trivial claim to the
    claim ledger `.work/claims/<task-id>.jsonl` (schema: Appendix E), which the coordinator
    merges into `data/claims/` and checks for conflicts (gate 6e).
20. **Status integrity.** Front-matter `status` is computed by `tools/check-status`, never
    self-declared: `verified` requires zero `UNVERIFIED`/`APPROX`/`BLOCKED` labels in the
    document, every referenced CF `closed`, all counts from the numbers registry, full
    line coverage of its Tier A sources, and — for `CORE` behavior sections —
    `run_verification: full`. Anything else is `partial` (or `draft` before review).
21. **Controlled vocabulary.** `GLOSSARY.md` holds `preferred term | definition | forbidden
    synonyms`, seeded in Phase 0 with at least these study-wide definitions (the *words*
    are fixed here; what the repo does under each word is established by evidence and
    recorded as a CF):
    - `tokenize` / `parse` / `analyze` — text -> tokens / tokens -> AST / AST -> checks.
    - `compile` — AST -> intermediate representation (expression trees in PowerShell);
      `JIT-compile` — intermediate representation -> executable delegate (IL) at run time;
      `interpret` — execute the intermediate representation with an instruction-based
      interpreter (the light-compiler in PowerShell); `tree-walk` — evaluate the AST
      directly (any statement that PowerShell tree-walks must cite evidence);
      `tier`/`tiering` — switching the execution mode of the same script block or loop
      between interpret and JIT-compile; `execute` — umbrella word, only in lifecycle
      documents.
    - `script block`, `function`, `filter`, `cmdlet`, `command`, `pipeline`, `runspace`,
      `session state`, `scope`, `provider`: defined once each, with the source types that
      implement them.
    - Never use one term for two concepts or two terms for one. `tools/lint-terms` fails
      on forbidden synonyms (gate 6c).
22. **Deviation discipline.** The study may only *propose* deviations from PowerShell's
    observable behavior. Each proposal is one row in
    `09-synthesis/deviation-register.md` with ID `DEV-<AREA>-<NNN>`, status `PROPOSED`
    (the only status the agent may write), evidence, benefit, compatibility cost, affected
    CFs, and the golden samples that would change. `APPROVED`/`REJECTED` are set by the
    product owner outside this run. Until approved, every document and the implementation
    blueprint treat the behavior as `REPLICATE`.
23. **Contradictions are recorded, never silently resolved.** Whenever two statements
    disagree (between documents, between a document and the source, between a source
    reading and a run, between an earlier draft and the source), create `CON-###` in
    `CONTRADICTIONS.md`: both statements and locations, evidence classes, status
    `OPEN | RESOLVED`, the resolution with evidence, and the files changed. Do not
    "harmonize" by rewording one side without a `CON-` entry. The final state has no
    `OPEN` rows (gate 12).

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

### 4.3 Scope classes (feature depth) versus tiers (file depth)

Tiers (4.1) classify **source files** by reading depth. Scope classes classify
**features** by documentation depth for the faithful rebuild. Both are recorded in
`FEATURE-MATRIX.md`, which has one row per feature named in Phases 2-4 with: scope class,
source tiers, owner documents, grammar productions, CFs, golden-sample count, covering
tests, status. Defaults come from section 1.3 F3; the owner finalizes the classification
and changes are recorded in `DECISIONS.md`.

| Class | Meaning | Required output |
|---|---|---|
| `CORE` | must be replicated for the new shell to count as PowerShell-faithful | rebuild-grade `SPEC`: rules, decision tables, CFs, golden samples (`E2`) for every rule, covering tests |
| `EXTENDED` | replicated later or partially | architecture + `SPEC` summary + golden samples for the headline behaviors |
| `OUT-OF-SCOPE-DOCUMENTED` | not replicated now | architecture-level description; extension points and security surface still documented |

---

## 5. MECHANICAL EXTRACTION LAYER

Build these tools in Phase 0. Tool source lives in `docs-out/tools/`; build and run
them only in the scratch copy so no `bin/`/`obj/` ever lands in the analyzed repo;
commit only tool source and their JSON/CSV output to `docs-out/`. Catalogs and folder
cards are rendered from this data, then annotated by reading. Every dataset in
`docs-out/data/` gets a schema entry (fields, types, generation command, preprocessor
symbol sets used) in `docs-out/data/README.md`.

### 5.1 Extraction approach

1. **Roslyn-based `dotnet` console tool** using `Microsoft.CodeAnalysis.CSharp` is
   **required** whenever a .NET SDK is available: parse every `.cs` file, run it once per
   relevant preprocessor-symbol set (record the sets you chose: at least Windows-like and
   Unix-like, with the symbols the projects actually define in their `.csproj`/props).
   Output is labelled `GENERATED`.
2. Only when no SDK exists (`ALLOW_STATIC_ONLY=true`, section 2 item 8): `rg`/ctags-based
   extraction with conservative regexes. All such output is labelled `APPROX`; documents
   using it have status `partial` (rule 20) and gate 4 reconciles it against a second
   method as far as possible.
3. Whatever the method, counts and constants go through `numbers.json` (rule 11).

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
| `enforcement-points.json` | Every security/policy enforcement point: language-mode checks, execution-policy gates, AMSI scan hooks, signature validation, constrained-language checks, secure-string handling, JEA-related checks. Mechanically seeded by searching for known APIs and patterns (`ExecutionContext.LanguageMode`, `CheckRestrictedLanguage`, `Compiler.CheckLanguageFeatures`, AMSI interop types, `Authenticode`/signature types, transcription/logging entry points), then verified by reading. Entry: file, type, method, line range, what it enforces, trigger condition, assigned `SEC-ENF-###` ID. |
| `numbers.json` | Registered numbers and source constants (rule 11): key, value, dataset, generation command, evidence class, label |
| `canonical-facts.json` | Canonical facts (rule 18): id, subject, statement, label, evidence, owner document, status |
| `claims/*.jsonl` | Claim ledger (rule 19; schema in Appendix E), one file per authoring task |
| `interpreter-scores.json` | Strategy scores for 2.10: option, criterion, score, justification, label |
| `golden/parse/`, `golden/behavior/` | Oracle outputs (5.4) |

### 5.3 Reflection cross-check (when an engine is built or a matching `pwsh` is available)

Use reflection on the engine built in the scratch copy (`E2`), or on an installed `pwsh`
of nearly the same version (`E3`, flagged `VERSION-MISMATCH`), to independently count
public AST types, `TokenKind` members, public operators, automatic variables, and public
cmdlets. Counts must match the static data, or every difference must be explained
(conditional compilation, internal types, version mismatch) and recorded in
`numbers.json` notes.

### 5.4 Behavioral oracle (golden samples) — mandatory when an engine can be built

Tool: `docs-out/tools/oracle-harness` (dotnet console tool, else PowerShell 7 script),
running in the scratch copy against the engine built from the pinned commit (`E2`).

1. **Parse oracle:** for each snippet dump tokens (kind, flags, text, extent), the AST
   (node type, children, extents) and parse errors (ID, message key, extent) through the
   real parser API -> `data/golden/parse/GS-<AREA>-<NNN>.json`.
2. **Behavior oracle:** for each snippet run it and record the ordered success-stream
   objects (type name, invariant string form, selected properties), every other stream
   (error, warning, verbose, debug, information, progress) with `ErrorRecord` details
   (`FullyQualifiedErrorId`, category, position), `$?`, `$LASTEXITCODE`, the terminating
   exception type, and the variable values the sample asks for ->
   `data/golden/behavior/GS-<AREA>-<NNN>.json`. Every file records the fixed environment:
   OS, culture (invariant where possible, otherwise recorded), engine commit, execution mode.
3. **Execution modes.** Run every behavior sample in as many of these modes as the source
   allows: (a) cold first execution; (b) after the tiering threshold has been crossed;
   (c) forced never-compile; (d) forced always-compile. How a mode is forced (public
   switch, internal API via reflection or `InternalsVisibleTo` in the scratch copy only,
   test hook) is established by reading the source and recorded in `TIERING-POLICY.md` and
   `ORACLE-PROTOCOL.md`; a mode that cannot be forced is reported as such, together with
   the modes actually reached. Results from different modes must be equal; any difference
   is a `CON-` entry and feeds `EQUIVALENCE-SPEC.md`.
4. **Corpus minimum:** every grammar production at least 2 valid + 1 invalid sample; every
   operator x operand-type family x precedence/associativity edge; every CF; every quirk in
   `SEMANTIC-QUIRKS.md`; every step of `CONVERSION-RULES.md`; every parameter-binding
   decision-table row; every flow-control construct including nesting (break/continue in
   nested loops, `try/finally` with `return`, `trap` scope); every tokenizer-mode
   transition and here-string/escape/numeric-suffix variant; every command-resolution
   step. Each sample has an ID `GS-<AREA>-<NNN>` registered in `ID-REGISTRY.md` and a
   one-line intent.
5. **Reproducibility:** one command (`tools/run-oracle`) regenerates all golden files;
   gate 9 reruns a random 10% and requires identical results after normalizing volatile
   fields (timestamps, paths, process IDs), the normalization being documented in
   `ORACLE-PROTOCOL.md`.
6. Samples are evidence for behavior (`SPEC`); the source remains evidence for design (`IMPL`).
7. If no engine can be built or run, apply section 2, item 8.

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
- Write `.work/pin.json` (rule 3); create `data/numbers.json` (rule 11) and
  `data/canonical-facts.json` with every CF ID of Appendix D reserved (`status: open`);
  create the empty registers `CONTRADICTIONS.md` and
  `09-synthesis/deviation-register.md` (table header only) and the `FEATURE-MATRIX.md`
  skeleton with the default scope classes of section 1.3 F3.
- Seed `GLOSSARY.md` with the controlled vocabulary of rule 21.
- Build the consistency tooling named in gate 6: `render-numbers`, `lint-numbers`,
  `render-canonical`, `check-claims`, `lint-terms`, `check-front-matter`, `check-status`.
- Build the oracle harness (5.4) and run one smoke sample end to end; if that is
  impossible, apply section 2, item 8.
- Deliverables: `00-overview/` and `data/` (including `fork-drift.md` when drift was
  detected in section 2 step 3), `.work/pin.json`, the registers and tools above.

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
- `02-language/STAGE-CONTRACTS.md`: for every pipeline boundary —
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

- **Execution-fidelity deliverables (new in v4; Tier A, scope `CORE`).** The new shell must
  reproduce PowerShell's execution pipeline; these four documents are its rebuild-grade
  specification:
  - `IR-SPEC.md`: for every AST node type, the exact intermediate representation the
    compiler emits (expression-tree node shapes, call-site/binder usage, runtime helper
    calls, labels, exception regions, sequence-point updates, prolog/epilog and the
    function-context contract), derived from the compiler visitor and verified by at least
    one golden sample per node type. It must agree with `COMPILATION-MAP.md`, which stays
    the one-row-per-node index.
  - `INSTRUCTION-SET.md`: the complete instruction catalog of the interpreter/light
    compiler: instruction, operands, stack effect, emitted-for (which IR node), conditional
    behavior; the frame/locals/closure model; the loop-compilation (on-stack-replacement)
    mechanism; which IR nodes the interpreter cannot execute and how they are handled.
  - `TIERING-POLICY.md` (**owner document** of CF-CMP-*): the complete compile-vs-interpret
    decision rule from script-block creation to execution: every strategy mode, every
    threshold and limit with its source constant name and evidence, what is counted
    (executions, loop iterations, statements), synchronous vs background compilation,
    caching and invalidation, the optimized/unoptimized split with its exact
    preconditions (debugging, dot-sourcing, variable scope modifiers, language mode), and
    how each mode can be forced for the oracle. Every other document links here and never
    restates these values.
  - `EQUIVALENCE-SPEC.md`: the invariants that make interpreted, JIT-compiled and tiered
    execution observably identical (results, streams, errors, positions, variable
    visibility), plus the complete list of **known divergences** (with golden samples) and
    the verdict per divergence.

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
  language change reaches, which the new implementation should minimize through its internal structure (mechanism only — observable language behavior stays `REPLICATE`).

**2.8 Tooling that depends on the pipeline**
- Tab completion (`CommandCompletion`), syntax-highlighting tokenization API, script
  analysis hooks, debugger breakpoint/sequence-point mapping, formatting of error positions
  (`InvocationInfo`, `ScriptExtent`), help-comment parsing.

**2.9 Language specification draft and semantic quirks**
- `LANGUAGE-SPEC-DRAFT.md` (all `SPEC`): the baseline behavior specification of the target
  language (= PowerShell's observable behavior, rebuild-grade for `CORE` scope) — lexical
  structure, grammar summary, type system, expressions, statements, scoping, pipeline
  semantics, error semantics — with every statement linked to evidence (`GS-` IDs and tests).
  Each major section ends with a `DEVIATIONS:` note (3-10 lines) listing the `DEV-*`
  proposals and canvas rows (`09-synthesis/new-language-design-canvas.md`) that concern it,
  or "none", so no section silently diverges from the baseline.
- **Canvas skeleton first.** Create `09-synthesis/new-language-design-canvas.md` at the
  start of Phase 2 with all row IDs reserved and cells empty, so the forward links from
  `LANGUAGE-SPEC-DRAFT.md`, `SEMANTIC-QUIRKS.md`, and every guidance section resolve
  immediately; Phase 7 fills the content.
- `SEMANTIC-QUIRKS.md`: every surprising behavior found (implicit unrolling, comparison
  coercions, parsing ambiguities, output pollution rules, etc.) with evidence, a golden
  sample, and a rule-16 verdict with a one-sentence rationale. A quirk with verdict
  `REPLICATE` or `ADAPT` is part of the baseline; a quirk with `REDESIGN` or `AVOID` has
  exactly one `DEV-*` row (rule 22) and stays baseline behavior until the owner approves.
  The design canvas consumes these verdicts and the per-verdict counts must match (gate 6d).

**2.10 Interpreter design space (.NET-anchored)**
- `INTERPRETER-DESIGN-SPACE.md`: anatomy of PowerShell's execution strategy (what is
  compiled, what is interpreted, what is dynamic, startup and warm-up behavior, caching;
  the light-compiler/interpreter model and its instruction set; DLR call-site caching).
  Facts and `INFERENCE` clearly separated.
- Then the design evaluation **for the new shell on .NET 8/9/10 LTS**. Evaluate these
  strategies, each as a named option with an ID: `S0` PowerShell-faithful tiered pipeline
  (AST -> expression trees -> light-compiler interpretation, with JIT-compilation of hot
  code according to `TIERING-POLICY.md`); `S1` AST tree-walking interpreter; `S2` custom
  bytecode VM (sketch the instruction set and stack/frame model); `S3`
  `System.Linq.Expressions` compilation to delegates (with cache strategy and
  invalidation); `S4` `Reflection.Emit` dynamic assemblies/methods (what PowerShell's
  class compilation does); `S5` source-generated ahead-of-time compilation (for built-in
  commands); `S6` hybrid of `S1`/`S2` with hot-path tiering.
- Document the hard .NET constraints with `EXTERNAL` labels: NativeAOT forbids
  `Reflection.Emit` and runtime JIT (interpreter or pre-generated code only, and
  `Expression.Compile` falls back to an interpreter with degraded performance under
  AOT); DLR lightweight code generation unavailable under AOT; `AssemblyLoadContext`
  capabilities and limits; ReadyToRun/JIT startup trade-offs. Keep repo evidence for
  what PowerShell itself does strictly separate from these `EXTERNAL` facts.
- **Scoring is rule-based.** Criteria and fixed weights (sum 100): behavioral fidelity to
  the target profile 25, sandboxability 15, startup latency 10, steady-state throughput 10,
  debuggability 10, AOT-friendliness 10, determinism 5, memory footprint 5,
  observability 5, tooling/implementation complexity 5. Score each option 1-5 per
  criterion with a one-sentence justification and its label (`FACT-SRC` for what
  PowerShell does, `EXTERNAL` for .NET facts, `INFERENCE` otherwise). Weighted totals are
  computed by a script from `data/interpreter-scores.json` and rendered, never typed.
- **Recommendation rule.** Produce **two** recommendations, because the deployment
  constraint is a product-owner decision and not a study finding: `JIT-allowed` and
  `NativeAOT-required`. For each, the recommended option is the highest weighted total
  among options that pass three hard gates: H1 (can reproduce the observable behavior of
  `CORE` scope, i.e. can satisfy the invariants of `EQUIVALENCE-SPEC.md` in principle),
  H2 (feasible under that deployment constraint, with the `EXTERNAL` facts cited), H3
  (policy/security hooks can be placed at every boundary of `STAGE-CONTRACTS.md`). Ties go
  to the lower implementation complexity. Label the result `INFERENCE`, state its
  sensitivity (which weight change flips it), then give a phased build order with
  measurable triggers for moving to the next phase. The first executable component must
  be verifiable against the golden samples (its results can be diffed with the oracle)
  before any optimizer is built.
- `INTERPRETER-DESIGN-SPACE.md` states the facts about PowerShell's own strategy (`S0`)
  only by *linking* to `TIERING-POLICY.md`, `IR-SPEC.md` and `INSTRUCTION-SET.md`; it does
  not restate them (rule 18).

**Phase 2 mandatory deliverables:**
`02-language/GRAMMAR.ebnf.md` (normative and complete: lexical and syntactic grammar with
the tokenizer-mode rules; every production linked to its parser method and golden
samples), `TOKEN-CATALOG.md`, `AST-CATALOG.md`, `OPERATOR-TABLE.md`, `COMPILATION-MAP.md`,
`IR-SPEC.md`, `INSTRUCTION-SET.md`, `TIERING-POLICY.md`, `EQUIVALENCE-SPEC.md`,
`BINDER-CATALOG.md`, `CONVERSION-RULES.md`, `ERROR-CATALOG.md`,
`SCOPE-AND-VARIABLES.md`, `LANGUAGE-SPEC-DRAFT.md`, `SEMANTIC-QUIRKS.md`,
`HOWTO-extend-language.md`, `INTERPRETER-DESIGN-SPACE.md`, `STAGE-CONTRACTS.md`,
`GOLDEN-SAMPLES.md` (index of `data/golden/` with the coverage report of 5.4),
`ORACLE-PROTOCOL.md` (5.4 as executed: commands, modes, forcing methods, normalization),
`CALL-GRAPHS.md` (entry-point call graphs for tokenize, parse, check, compile,
invoke, as Mermaid, generated from `members-tierA.json`),
`LIFECYCLE-script-execution.md` (end-to-end sequence diagram from `pwsh -c "<text>"` to
output, naming every class and method touched), and `REFERENCE-TEST-CORPUS.md` (existing
parser/language tests under `test/` that specify language behavior, grouped by feature
with paths and counts from `tests.json` — the model for the new product's own
specification-test suite and the source of the "covering tests" column of
`FEATURE-MATRIX.md`).

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
- Every `CORE`-scope subsystem above additionally carries golden samples (5.4) for every
  rule in its algorithm sections and registers its critical facts as CFs (rule 18).
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

### Phase 5 — Security architecture (P0 enterprise axis (b), section 1.1)

Security is P0 enterprise axis (b) of section 1.1 (it does not outrank the fidelity axis (a); both are required). This phase is
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
  rule-16 verdicts `REPLICATE | ADAPT | REDESIGN | AVOID` (a `REDESIGN` or `AVOID`
  verdict must reference its `DEV-*` row and state what replaces the component), with
  justification and dependency notes (for building an independent implementation).
- **Enterprise-readiness gap analysis** for the new product — **prioritized**:
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
  evidence, verdict (rule 16), consequences. Principles that would change observable
  behavior are *candidate deviations*: each is a `PROPOSED` row in
  `deviation-register.md` and not in effect (rule 22).
- **`new-language-design-canvas.md`**: the working decision canvas for the
  new language — the single entry point a designer reads first after the pipeline map.
  Fill in the skeleton created at the start of Phase 2 (2.9).
  For each design area — lexical rules and tokens; keywords (reserved vs contextual);
  grammar shape (statement/expression split, pipelines as first-class); operators and
  precedence; type system and coercion policy; scoping and variables (including what
  replaces automatic variables); error model; pipeline semantics; module/extension model;
  command discovery and naming; security model; tooling hooks (completion, highlighting,
  debugging, LSP) — produce a table:
  `Area | PowerShell's choice (evidence) | Verdict (REPLICATE/ADAPT/REDESIGN/AVOID) |
  DEV-ID (for REDESIGN/AVOID) | Rationale | Open decisions for the product owner`.
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
- **`dotnet-runtime-integration.md`**: how the new shell should sit on .NET:
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
- **`deviation-register.md`** (rule 22): all rows `PROPOSED`; every `REDESIGN`/`AVOID`
  verdict anywhere in the study has exactly one row here, and each row cites the places
  where its verdict appears (checked by gate 6d). Candidate deviations named in
  `language-design-principles.md` and the canvas are rows here; none of them is in effect.
- **`implementation-blueprint.md`** (the rebuild plan of the faithful shell): ordered
  milestones following the build order of 2.10; for each milestone: scope (documents and CF
  IDs implemented), the public C# interfaces to define (signatures only, never copied
  bodies), inputs and outputs, the golden samples that must pass (`GS-` IDs), acceptance
  criteria, risks. It references only behavior that is `REPLICATE` or `ADAPT` (never a
  `PROPOSED` deviation) and must be consistent with `reference-architecture.md`.
- **`FEATURE-MATRIX.md`** (root): final state of the matrix defined in 4.3.
- Deliverables: `09-synthesis/` (plus `FEATURE-MATRIX.md` and `CONTRADICTIONS.md` at the root).

### Phase 8 — Behavioral verification, equivalence and consolidation (new in v4)

- Run the complete oracle (5.4) over every golden sample in all reachable modes and
  reconcile every behavior claim in all documents: `UNVERIFIED` becomes `FACT-RUN` (cite the
  `GS-` ID) or the document is corrected. Disagreements between a source reading and a run
  become `CON-` entries resolved by the precedence of rule 1 before any document is changed.
- Complete `EQUIVALENCE-SPEC.md` from the cross-mode results.
- Run all mechanical tools of gate 6 (numbers, canonical facts, claims conflicts,
  terminology, status, front matter), fix every finding, and rerun until clean.
- Write the final `VERIFICATION-BACKLOG.md`: every remaining entry is `BLOCKED` with an
  owner-actionable fix and an impact statement.
- Deliverables: updated documents, `data/golden/`, `data/claims/`, `CONTRADICTIONS.md`
  with no `OPEN` rows.

### Phase 9 — Optional Persian digest (only if `FA_DIGEST=true`)

After all gates have run, produce `docs-out/fa-digest/` with Persian translations of:
`README.md`, `00-overview/study-summary.md`, `02-language/00-pipeline-map.md`,
`02-language/TIERING-POLICY.md`, `09-synthesis/implementation-blueprint.md`,
`09-synthesis/deviation-register.md`. Rules: translation only — no new claims, and no
number, CF, DEV or GS ID changed (values are rendered from the same registries);
identifiers, code and IDs stay in Latin script; each file's front matter has
`derived_from` and `authoritative: false`; on any difference the English document wins;
`tools/lint-terms` runs with the Persian term mapping kept in `GLOSSARY.md`.

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
│                                  #   (SPEC/IMPL/LESSON, verdicts, FACT-SRC/FACT-RUN/INFERENCE/
│                                  #   EXTERNAL/UNVERIFIED + APPROX/GENERATED/VERSION-MISMATCH), controlled
│                                  #   vocabulary (rule 21), ID schemes
├── DECISIONS.md                   # decisions made while documenting
├── VERIFICATION-BACKLOG.md        # all UNVERIFIED and BLOCKED items
├── COVERAGE.md                    # coverage matrix (section 10)
├── TRACEABILITY.md                # source folder/project <-> documents, both directions
├── ID-REGISTRY.md                 # every stable ID (incl. SEC-ENF, NLD, CF, DEV, CON, GS, CLM) and where defined
├── ACCEPTANCE-QUESTIONS.md        # cold-read test and answers (Appendix B)
├── CANONICAL-FACTS.md             # rendered view of data/canonical-facts.json (CF IDs, owner documents)
├── CONTRADICTIONS.md              # CON-### register (rule 23); no OPEN rows at the end
├── FEATURE-MATRIX.md              # features x scope class x documents x golden samples (4.3)
├── BLOCKED.md                     # only if a hard stop occurred (section 2 item 8)
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
│   ├── IR-SPEC.md
│   ├── INSTRUCTION-SET.md
│   ├── TIERING-POLICY.md
│   ├── EQUIVALENCE-SPEC.md
│   ├── ORACLE-PROTOCOL.md
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
│   ├── deviation-register.md
│   ├── implementation-blueprint.md
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
├── fa-digest/                     # only if FA_DIGEST=true (Phase 9; derived, non-authoritative)
├── data/                          # machine-extracted JSON/CSV (section 5.2) + golden/{parse,behavior}/
│                                  #   + claims/ + numbers.json + canonical-facts.json
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
status: draft | partial | verified      # computed by tools/check-status (rule 20), never self-declared
run_verification: full | partial | none # `none` is mandatory under ALLOW_STATIC_ONLY
scope_class: CORE | EXTENDED | OUT-OF-SCOPE-DOCUMENTED   # 4.3 (catalogs: class of the feature they serve)
version_pin: <from .work/pin.json>      # identical in every document (rule 3)
pin_method: <from .work/pin.json>
canonical_facts: [CF-...]               # CFs this document owns or embeds (rule 18)
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
18. Guidance for the new shell   (design lessons, each with one verdict
                                 REPLICATE | ADAPT | REDESIGN | AVOID, evidence-linked;
                                 REDESIGN/AVOID cite their DEV-id; rule 16)
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
- `LESSON` verdicts (`REPLICATE | ADAPT | REDESIGN | AVOID`), design-canvas rows (`NLD-*`),
  canonical facts (`CF-<AREA>-<NNN>`), deviations (`DEV-<AREA>-<NNN>`), contradictions
  (`CON-<NNN>`), golden samples (`GS-<AREA>-<NNN>`) and claims (`CLM-<AREA>-<NNNN>`) are
  first-class registered artifacts, not prose decorations. `CF`, `DEV`, `GS` and `CLM` use
  the same area codes as `NLD` plus `PIN`, `CMP`, `CNV`, `FLW`, `BND`, `DSC`, `LCY`, `ETS`.
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
scope, (h) the path of its claims file (rule 19) and the `CF`/`GS`/`DEV` IDs it proposes.

**The coordinator** merges those reports into the shared files, resolves terminology
conflicts, merges the claims files into `data/claims/`, runs `check-claims` and
`render-canonical --check` (conflicts become `CON-` entries, rule 23), and updates
`PROGRESS.md` after each subagent finishes.

**Review subagents** are separate from authoring subagents and re-read each Phase 2,
Phase 3, and Phase 5 document against the source and `data/` (section 10, item 5).

---

## 10. QUALITY GATES

The coordinator runs the gates in this order with tools from `docs-out/tools/`. The
result of every gate (`PASS`, `FAIL`, `WAIVED` with reason, `FAIL-RECORDED`; counts, commit,
date) is written to `COVERAGE.md` and `00-overview/study-summary.md`. A `FAIL` is fixed
and the gate rerun, at most **3 rerun cycles per gate**; after that every remaining
finding becomes a `BLOCKED` entry in `VERIFICATION-BACKLOG.md` (with an owner-actionable
fix) and the gate is reported `FAIL-RECORDED`, which caps the acceptance status (gate 14).

1. **Evidence validator:** write `docs-out/tools/validate-refs` that extracts every
   repo-relative path, every `file::Type.Member@Lx-Ly` reference and every `GS-` ID from
   the documents and checks — after confirming that `git rev-parse HEAD` equals the commit
   in `.work/pin.json` — that the file exists, the type/member exists, the line range is
   plausible, and the golden sample exists. Run it; fix all failures; keep the tool.
2. **Link, ID and diagram validator:** all relative links resolve; all IDs in front matter
   are unique and registered in `ID-REGISTRY.md` (families: `SEC-ENF`, `NLD`, `CF`, `DEV`,
   `CON`, `GS`, `CLM`, plus document IDs); if the Mermaid CLI is available every Mermaid
   block renders, otherwise run a syntax lint and record the limitation.
3. **Coverage matrix** (`COVERAGE.md`): every `.csproj`, every source folder and every
   file in the ledger maps to at least one document or card; Tier A files show 100%
   lines read (machine-checked from `ranges_read`); every `FEATURE-MATRIX.md` row has its
   owner documents; list anything uncovered with the reason.
4. **Catalog completeness checks:** AST-CATALOG covers **all** classes deriving from the
   AST base type (counts from `ast-hierarchy.json` and from reflection, 5.3);
   TOKEN-CATALOG covers all token kinds and flags; OPERATOR-TABLE covers all operator
   tokens; ERROR-CATALOG covers all parser error resource keys; BINDER-CATALOG covers all
   binder classes; `INSTRUCTION-SET.md` covers all instruction classes; cmdlet inventories
   match `cmdlets.json`; every row of `enforcement-points.json` carries a `SEC-ENF` ID
   registered in `ID-REGISTRY.md`. Give counts through `numbers.json` and reconcile every
   difference.
5. **Second-pass review:** separate review subagents re-read each Phase 2, Phase 3 and
   Phase 5 document against the source and `data/` and return discrepancies in their
   report (they write no shared files; the coordinator records them in
   `VERIFICATION-BACKLOG.md` or `CONTRADICTIONS.md`); fix them or mark `UNVERIFIED`. For
   Phase 5, additionally verify that every claimed enforcement point exists in the source
   exactly as cited.
6. **Mechanical consistency pass** (all sub-checks are tools, not reading):
   a. canonical facts: every Appendix D CF exists and is `closed` or has a `BLOCKED`
      backlog entry; `render-canonical --check` finds no divergent embedded copy; the
      lint finds no restatement of a CF statement outside its owner document and embeds;
   b. numbers: `lint-numbers` finds no hand-typed count and no stale embed;
   c. terminology: `lint-terms` finds no forbidden synonym; every term used is in the glossary;
   d. verdicts: per-verdict counts (`REPLICATE`/`ADAPT`/`REDESIGN`/`AVOID`) are equal
      between subsystem documents and the canvas; every `REDESIGN`/`AVOID` has exactly one
      `DEV-*` row; every `DEV-*` row is `PROPOSED`;
   e. claims: `check-claims` finds no two claims with the same subject key and predicate but
      different values, unless a `CON-` entry linking them is `RESOLVED`;
   f. status: `check-status` confirms rule 20 for every document;
   g. front matter: pin fields identical in all documents; `scope_class` present;
   h. diagrams match text: every node and edge name of a Mermaid diagram occurs in its
      document, and the review subagents of gate 5 confirm the sequence/flow itself.
7. **Cold-read test:** a fresh subagent with access **only** to `docs-out/` (not to the
   source) answers every question in `ACCEPTANCE-QUESTIONS.md` (Appendix B) with
   citations. A second reviewer checks each answer against the source. Required result:
   at least 95% correct with valid citations and no wrong answer in `CORE` scope. Every
   wrong or "cannot answer" result produces a fix in the documents; at most 3 cycles, then
   the remainder is recorded as `BLOCKED`.
8. **Interpreter-readiness review:** a fresh subagent with access only to `docs-out/` must
   be able to (a) state the recommended execution strategy for both deployment constraints
   (2.10) with rationale and sensitivity, (b) enumerate the stage contracts and the data
   handed across each boundary, (c) list the security gates that must exist at
   script-execution time, and (d) draft the design-canvas rows for 5 core flows (literal,
   variable, command invocation, pipeline, error). Any failure is fixed in the documents.
9. **Behavior verification gate:** every behavior claim in `CORE` scope is `FACT-RUN` with
   a `GS-` ID, or `BLOCKED`; the corpus minimum of 5.4 is covered 100%; a random 10% rerun
   reproduces identical results after normalization; the parse oracle agrees with
   `GRAMMAR.ebnf.md` on every sample (accept/reject and tree shape). Reported `WAIVED` only
   under `ALLOW_STATIC_ONLY=true`.
10. **Equivalence gate:** for every behavior sample, all reachable execution modes give equal
    results, or the divergence is listed in `EQUIVALENCE-SPEC.md` with its sample.
11. **Rebuild-readiness review:** a fresh subagent with access only to `docs-out/` drafts,
    from `implementation-blueprint.md` and the cited documents, the interface skeleton and
    the test plan for the milestones from tokenizer through interpreter, and lists every
    point where it had to guess or found two answers. Each point is fixed in the
    documents; no guess may remain in `CORE` scope (otherwise `BLOCKED`).
12. **Contradiction closure:** `CONTRADICTIONS.md` has no `OPEN` rows; every `RESOLVED`
    row cites evidence and the files changed.
13. **Source integrity:** `git status --porcelain` shows changes only under `docs-out/`.
14. **Finalize and acceptance status:** write `README.md` (index and reading order for an
    architect building the new shell: 00 -> 01 -> 02 -> 03 -> 07 -> 09 as the core path,
    with 07 (security blueprint) mandatory before any sandboxing/policy design,
    04-06/08/10 as needed, and `src-mirror/` cards for drill-down) and `PROGRESS.md` (all
    green). Compute the **acceptance status**: `ACCEPTED` — gates 1-13 all `PASS`;
    `CONDITIONAL` — the only non-`PASS` results are `WAIVED` (static-only run) or
    `FAIL-RECORDED` findings confined to `EXTENDED`/`OUT-OF-SCOPE-DOCUMENTED` scope;
    `REJECTED` — anything else. Write it as the first line of `00-overview/study-summary.md`.

---

## 11. EXECUTION PROCEDURE

1. First action: run the environment preflight (section 2, including fork-base pinning and
   the hard stops) and Phase 0 discovery, then write `PROGRESS.md` with the full checklist
   derived from the *real* project and folder list, including one task per folder-card
   group and per document.
2. Proceed phase by phase. For Phase 2, process stages in pipeline order, and at the end
   write the lifecycle document that stitches them together.
3. Spawn subagents for independent modules (Phases 2-4) under section 9; after every
   merge run `check-claims` and `render-canonical --check` so contradictions surface
   while the work is fresh, not at the end.
4. After each completed document: update `PROGRESS.md` and the ledger, run
   `render-numbers`/`render-canonical`, then continue automatically.
5. Run Phase 8 (and Phase 9 if requested), then the gates of section 10.
6. At the end, print a short summary: acceptance status, documents produced, counts
   (projects, folders, types, AST nodes, token kinds, operators, parser error IDs, binders,
   instructions, cmdlets, enforcement points; all from `numbers.json`), ledger coverage per
   tier, number of golden samples per area and mode, CFs closed/open, `DEV-*` proposals,
   `CON-` entries, `UNVERIFIED`/`BLOCKED` counts, acceptance-question pass rate, and the top
   10 insights most relevant to building the faithful interpreter and compiler on .NET.
   Persist the same summary as `00-overview/study-summary.md` and list the highest-risk
   `VERIFICATION-BACKLOG.md` entries there.

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
| Interpreter / light compiler | `src/System.Management.Automation/engine/interpreter/` (an earlier run found it here; also check under `engine/runtime/` — verify; look for `LightCompiler.cs`, `LightLambda.cs`, `LoopCompiler.cs`, `Instruction*.cs`) |
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

## APPENDIX B — ACCEPTANCE QUESTIONS (seed list; extend to at least 100)

Create `docs-out/ACCEPTANCE-QUESTIONS.md` from this list: questions 1-54 are the seeds of
v3/v3.1 (29-46 added in v3 for stage contracts, interpreter/.NET and security; 47-54
added in v3.1 for runtime subsystems, startup and experimental features); questions
55-84 are added in v4 for execution-engine fidelity, equivalence, the oracle, canonical
facts and deviations. Add questions for every Phase 3-5 subsystem until the file holds at
least 100 questions in total. The cold-read reviewer must answer each using only
`docs-out/`, with citations. The expected answers are written by the coordinator from the
source and the golden samples, never from the documents under test.

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
27. Which PowerShell semantics carry an `AVOID` or `REDESIGN` verdict, which `DEV-*` proposal covers each, and what is the baseline (`REPLICATE`) behavior while the proposal is not approved?
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
55. State the complete compile-versus-interpret decision rule, every threshold with its
    source constant, and where each one is enforced (`TIERING-POLICY.md` and source).
56. How is each execution mode forced for testing, and which cannot be forced?
57. For `if`, `foreach`, `switch`, `try/catch/finally`, `trap` and `return`: what is the IR
    shape, and which interpreter instructions execute it?
58. How is a loop promoted from interpreted to compiled execution in mid-flight, and which
    state is transferred?
59. Which IR nodes can the interpreter not execute directly, and how is each handled?
60. What does the function context contain, who creates it, and who consumes each field?
61. Which conditions force unoptimized variable storage, and which observable behavior
    differs from optimized storage?
62. How do sequence points produce error positions and breakpoint hits in compiled versus
    interpreted code?
63. List every known observable divergence between interpreted, compiled and tiered
    execution, with golden samples.
64. For each dynamic binder: what does it cache, what keys the cache, and what invalidates it?
65. Which operators depend on operand order or on the type of the left operand? Give the
    exact rule (CF and golden samples).
66. State the exact output-unrolling rules across pipeline stages, with samples for
    scalars, arrays, nested arrays, hashtables, `$null` and empty arrays.
67. What is the observable difference between `return`, plain output and flow-control
    exceptions inside nested script blocks, pipelines and `ForEach-Object`?
68. How are `break`, `continue` and labels resolved across script-block and function
    boundaries?
69. State the order of events for `try/catch/finally` combined with `return`/`break` and with
    terminating versus non-terminating errors, and the scope behavior of `trap`.
70. In which exact order are named, positional, default, dynamic and pipeline parameters bound?
    Give the decision table for ambiguous parameter-set resolution, with samples.
71. When exactly are `begin`, `process`, `end` and `clean` executed for each command type,
    including pipeline-stop and error cases?
72. How does command resolution treat name qualification, case, wildcards, alias-versus-function
    precedence and module-qualified names? Give a sample per step.
73. Which `CORE` features are required to run a given sample script, and which documents
    specify them (`FEATURE-MATRIX.md`)?
74. Pick five keys of `numbers.json` and regenerate their values from the stated commands.
75. Which CFs exist, which document owns each, and which are not `closed`?
76. For each `PROPOSED` deviation: what is the baseline behavior, which golden samples would
    change, and what is the compatibility cost?
77. Give the minimal C# interface skeleton for the chain tokenizer -> parser -> AST ->
    semantic checks -> compiler -> interpreter and the golden samples that gate each milestone.
78. Which behaviors depend on culture, OS or environment, and how does the oracle normalize them?
79. How do dot-sourced, `$using:` and nested-scope variable accesses work in each execution mode?
80. How are error positions (line, column, extent) produced for multi-line statements,
    here-strings and nested script blocks?
81. How do `ErrorActionPreference`, `-ErrorAction`, `$?` and `$LASTEXITCODE` interact for
    native, cmdlet and script commands (samples)?
82. What do script blocks capture and when (`GetNewClosure`, `$using:`, nested functions)?
83. Which language semantics need runtime type information from the Extended Type System,
    and what is the minimum ETS needed for `CORE` scope?
84. Which statements of the earlier study drafts listed in Appendix C were confirmed,
    corrected or rejected, and with which evidence?

---

## APPENDIX C — KNOWN DISCREPANCIES IN EARLIER STUDY OUTPUTS (resolve by evidence; assume neither side)

Every row is a **claim to verify**, not a fact (rule 2). Each ends as a `CON-` entry
(rule 23) and in the answer to acceptance question 84.

| # | Discrepancy | Resolve in |
|---|---|---|
| C1 | Two earlier document sets pin two different commit hashes. | `.work/pin.json`, gate 6g |
| C2 | One earlier draft claims the compile/interpret policy is: script blocks compile after 32 executions, loops after 16 iterations, nothing is compiled above 300 statements, compilation of hot code runs on a background thread; the other draft does not contain these values. | `TIERING-POLICY.md`, CF-CMP-* |
| C3 | One earlier draft counts 26 custom binders, another lists 23. | `BINDER-CATALOG.md`, `numbers.json` |
| C4 | The earlier Appendix A hint placed the interpreter under `engine/runtime/interpreter/`; an earlier run found `engine/interpreter/`. | Appendix A, `DECISIONS.md` |
| C5 | One draft states that PowerShell does not interpret the AST directly (it interprets expression trees); another recommends an AST tree-walker as the first phase. The first is a claim about PowerShell (`S0`), the second a recommendation (`S1`): keep them separate. | `INTERPRETER-DESIGN-SPACE.md` |
| C6 | Counts in earlier outputs came from regex extraction (e.g. type, member, cmdlet and seeded enforcement-point counts, parser error key counts). | gate 4, `numbers.json` |
| C7 | Earlier documents carried `status: verified` while containing `UNVERIFIED` behavior claims. | rule 20, gate 6f |
| C8 | The earlier `data/golden/` directory was empty and golden samples were never executed. | 5.4, gate 9 |
| C9 | The earlier run had no .NET SDK and no `pwsh` (static analysis only). | section 2 item 8, gate 14 |

---

## APPENDIX D — CANONICAL FACT SEEDS (minimum set; reserve the IDs in Phase 0)

Each row is a subject that needs exactly one canonical statement (rule 18). The statement
itself is established by evidence in the run; this table fixes only subject and owner.
Add further CFs for any fact stated in more than one document.

| CF prefix | Subject | Owner document |
|---|---|---|
| `CF-PIN-001` | version, commit and pin method | `README.md` |
| `CF-LEX-001` | tokenizer mode switching rule (command vs expression mode, when it switches) | `02-language/02.1-tokenizer.md` |
| `CF-LEX-002` | numeric-literal rules (radix, suffixes, multipliers) | `02-language/02.1-tokenizer.md` |
| `CF-GRM-001` | statement, pipeline and command grammar; statement terminators | `02-language/GRAMMAR.ebnf.md` |
| `CF-OP-001` | operator precedence and associativity | `02-language/OPERATOR-TABLE.md` |
| `CF-CMP-001` | compile-versus-interpret decision rule | `02-language/TIERING-POLICY.md` |
| `CF-CMP-002` | every threshold and limit of the tiering policy | `02-language/TIERING-POLICY.md` |
| `CF-CMP-003` | optimized-versus-unoptimized preconditions | `02-language/TIERING-POLICY.md` |
| `CF-CNV-001` | conversion algorithm and converter order | `02-language/CONVERSION-RULES.md` |
| `CF-PIP-001` | output unrolling and enumeration rules | `02-language/02.6-types-and-operators.md` |
| `CF-SCP-001` | scope, variable lookup and assignment rules | `02-language/SCOPE-AND-VARIABLES.md` |
| `CF-FLW-001` | flow-control semantics (break, continue, return, labels) | `02-language/02.5-compiler-and-engine.md` |
| `CF-ERR-001` | terminating/non-terminating errors; try/catch/finally/trap ordering | `03-runtime/errors-and-diagnostics.md` |
| `CF-ERR-002` | parse-error limits and recovery rule | `02-language/ERROR-CATALOG.md` |
| `CF-BND-001` | parameter-binding order and parameter-set resolution | `03-runtime/parameter-binding.md` |
| `CF-DSC-001` | command resolution order | `03-runtime/command-discovery-and-invocation.md` |
| `CF-LCY-001` | command and script lifecycle (begin/process/end/clean, cmdlet lifecycle, stop) | `03-runtime/runspace-and-pipeline.md` |
| `CF-ETS-001` | member resolution order | `03-runtime/extended-type-system.md` |
| `CF-MOD-001` | module load, export and auto-load rules | `03-runtime/modules.md` |
| `CF-SEC-001` | language-mode semantics | `07-security/language-modes.md` |

---

## APPENDIX E — SCHEMAS (placeholders show the shape only, never values)

- `data/numbers.json` entry: `{"key": "<UPPER_SNAKE>", "value": <number|string>, "dataset": "<file>", "command": "<regeneration command>", "evidence": "E1|E2", "label": "GENERATED|FACT-SRC|APPROX", "notes": "<optional>"}`
- `data/canonical-facts.json` entry: `{"id": "CF-<AREA>-<NNN>", "subject": "<text>", "statement": "<one canonical statement>", "label": "FACT-SRC|FACT-RUN|INFERENCE", "evidence": ["<path::Type.Member@Lx-Ly>", "<GS-ID>"], "owner": "<document path>", "status": "open|closed"}`
- `.work/claims/<task-id>.jsonl` line: `{"id": "CLM-<AREA>-<NNNN>", "subject_key": "<dotted.lower_snake from data/subject-keys.json>", "predicate": "<text>", "value": "<normalized value>", "label": "FACT-SRC|FACT-RUN|INFERENCE|EXTERNAL|UNVERIFIED", "evidence": ["<ref>"], "doc": "<document id>", "cf": "<CF id or null>"}`
- `data/interpreter-scores.json` entry: `{"option": "S0..S6", "criterion": "<name>", "score": <1-5>, "justification": "<one sentence>", "label": "FACT-SRC|EXTERNAL|INFERENCE"}`
- Deviation row (`deviation-register.md`): `DEV-ID | status (PROPOSED) | baseline behavior (CF/GS) | proposed behavior | benefit | compatibility cost | affected CFs | golden samples that would change | verdict locations`.
- Contradiction row (`CONTRADICTIONS.md`): `CON-ID | statement A + location | statement B + location | evidence classes | status | resolution + evidence | files changed`.
