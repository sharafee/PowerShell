---
id: REPO-STANDARDS-001
title: Coding standards and engineering rules in the repository
kind: subsystem
tier: C
status: draft
run_verification: none
scope_class: OUT-OF-SCOPE-DOCUMENTED
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [.editorconfig, .globalconfig, Analyzers.props, stylecop.json, Settings.StyleCop, docs/dev-process/coding-guidelines.md, docs/dev-process/breaking-change-contract.md, docs/dev-process/resx-files.md, PowerShell.Common.props]
mirror_cards: []
generated_from: [data/conditional-compilation.json]
---

# Coding standards and engineering rules in the repository

> STATIC-ONLY — behavior not run-verified.

## 1. Purpose and scope [SPEC]

Records the coding standards that are enforced mechanically (analyzers, `.editorconfig`, build flags) or documented for contributors, so the new shell can adopt the useful ones. The process side (tests, localization workflow, experimental features, API review) is continued in the Phase 6 document [engineering-processes](../08-engineering/engineering-processes.md).

## 2. Source map

| Path | Role | Tier |
|---|---|---|
| `.editorconfig` | Formatting, naming rules, C# style preferences, file header template | C |
| `.globalconfig` (596 setting lines) | Roslyn analyzer severities for CA/IDE/SA rules | C |
| `Analyzers.props` | Adds StyleCop.Analyzers 1.2.0-beta.556 and DotNetAnalyzers.DocumentationAnalyzers 1.0.0-beta.59 to projects importing it | C |
| `stylecop.json`, `Settings.StyleCop` | StyleCop analyzer settings (ordering, naming, documentation rules) | C |
| `PowerShell.Common.props` | `TreatWarningsAsErrors`, `LangVersion`, `EnforceCodeStyleInBuild`, `Features=strict` | C |
| `docs/dev-process/coding-guidelines.md` | Contributor C# guidelines | C |
| `docs/dev-process/breaking-change-contract.md` | Four-bucket breaking-change policy | C |
| `docs/dev-process/resx-files.md` | Rules for resource files | C |
| `.markdownlint.json`, `.prettierrc`, `.spelling`, `.vscode`, `.devcontainer` | Docs lint, spelling dictionary, editor/dev-container setup | C |

## 3. Responsibilities and non-responsibilities

Defines style and quality gates. Does not define runtime behavior.

## 4. Key types and contracts [IMPL]

**Build-enforced (`FACT-SRC`, `PowerShell.Common.props`):** `LangVersion` 13.0, `TreatWarningsAsErrors=true`, `AllowUnsafeBlocks=true`, `GenerateDocumentationFile=true`, `EnforceCodeStyleInBuild=true`, `Features=strict`, `DisableImplicitNamespaceImports=true`, `NeutralLanguage` en-US.
**Analyzer severities (`.globalconfig`, `GENERATED` by grep of `severity =` lines):** 112 `warning`, 308 `none`, 112 `silent`, 23 `suggestion`, 0 `error` (the build turns warnings into errors through `TreatWarningsAsErrors`, so `warning` rules are effectively blocking).
**Naming (`.editorconfig` naming rules and `coding-guidelines.md`):** `_camelCase` for private/internal instance fields, `s_` prefix for static fields, `t_` for thread-static, PascalCase for constants, types and members, camelCase for locals; visibility always explicit and first modifier; `static readonly` order; `nameof` over string literals.
**File header:** `file_header_template = Copyright (c) Microsoft Corporation.\nLicensed under the MIT License.` (`.editorconfig`).
**Formatting:** UTF-8, spaces, 4-space indent for C#/PowerShell, 2 for XML/JSON/YAML/Markdown (`.editorconfig`); the contributor guideline additionally says "File encoding should be ASCII" and braces on their own lines.
**Using directives:** `System` first, outside the namespace (`stylecop.json` `systemUsingDirectivesFirst`, `usingDirectivesPlacement: outsideNamespace`).

## 5. Data model

Not applicable.

## 6. Control flow

Not applicable.

## 7. Algorithms

Not applicable.

## 8. Observable behavior [SPEC]

Compile-time only: violations of `warning`-level rules fail the build because warnings are errors.

## 9. Error handling and edge cases

Guideline: "Avoid gratuitous exceptions... stay away from using exceptions for control flow" (`coding-guidelines.md`, Performance Considerations). Note the contrast with the engine, which uses exceptions for flow control (`break`/`continue`/`return` are implemented with exception types in the runtime; see [02.5-compiler-and-engine](../02-language/02.5-compiler-and-engine.md), `INFERENCE` until that document is complete).

## 10. Concurrency and threading

Guideline: prefer `Interlocked` over `lock` for simple atomic state.

## 11. Extension points and customization hooks

Local deviations allowed: "follow the style of the surrounding code" takes precedence over the guideline; style-only changes must be separate PRs.

## 12. Dependencies

Analyzer packages above; .NET SDK analyzers (CA/IDE rules via `.globalconfig`).

## 13. Performance notes

Repository performance rules (`coding-guidelines.md`, `FACT-SRC`): avoid LINQ in hot code (use `for`/`foreach`), avoid `params` arrays (add fixed-arity overloads), avoid string interpolation and implicit-culture overloads in hot paths, avoid allocation in loops, use `TryGetValue`, pre-size collections, use generic collections, avoid double casts, prefer `StringBuilder` in loops.

## 14. Security considerations

Policy: changes touching `password`, `crypto`, `encryption`, `decryption`, `certificate`, `authenticate`, `ssl/tls` or `protected data` require review by a designated security subject-matter expert (`coding-guidelines.md`, Security Considerations; `.github/CODEOWNERS` lists area experts). This is a process control; it creates no runtime enforcement point.

## 15. Enterprise considerations

Strong mechanical enforcement (warnings as errors, 112 warning-level rules) and a published breaking-change contract. Gap: the guideline asks for ASCII while `.editorconfig` says UTF-8; the more specific rule for the new shell should be chosen explicitly (`INFERENCE`: both statements are `FACT-SRC`, they differ in scope, no CON entry needed since they do not describe the same fact: charset of source files).

## 16. Tests

Style is validated by the compiler and analyzers; markdown by `.markdownlint.json`/`.spelling` in CI (`verify-markdown-links.yml`, super-linter under `tools/super-linter`).

## 17. Design decisions and trade-offs

- **Portable code policy** (`coding-guidelines.md`, "Portable Code"): three primary macros — `DEBUG`, `CORECLR`, `UNIX`; do not use `CORECLR`/`!CORECLR` in new code; minimize `#if UNIX`; prefer preprocessor directives over runtime OS checks unless readability wins; a single binary serves all UNIX variants so macOS-vs-Linux needs runtime checks. The extracted symbol inventory (`data/conditional-compilation.json`, `APPROX`) lists <!--N:CONDITIONAL_SYMBOLS-->21<!--/N--> distinct symbols; `UNIX` appears in 122 files and 247 type declarations, `CORECLR` in 30 files, `DEBUG` in 26, and legacy symbols (`CLR2`, `V2`, `SILVERLIGHT`, `LEGACYTELEMETRY`, `NOT_USED`, `_LATER`, `STATS`) survive in a few files — evidence that the cleanup the guideline mentions is incomplete.
- **Breaking-change contract** (`breaking-change-contract.md`): four buckets (Public Contract, Reasonable Grey Area, Unlikely Grey Area, Clearly Non-Public). Unacceptable in bucket 1: changing existing observed behavior for a given input of an API, protocol or the language; removing/renaming public types, cmdlets or parameters; narrowing accepted values; changing public constants/enum members; incompatible protocol changes without a version increment. Acceptable: new types/members/cmdlets, behavior that previously errored, protocol changes with a version increment. The policy applies only to features that shipped in a supported release.
- Public members in namespaces ending with `Internal` are not supported API (`coding-guidelines.md`, Member Conventions).

## 18. Guidance for the new shell [LESSON]

- **LSN-STD-01** [REPLICATE] (area: NLD-TOOL) Adopt warnings-as-errors with an explicit analyzer severity file from day one. Evidence: `PowerShell.Common.props` (`TreatWarningsAsErrors`), `.globalconfig`.
- **LSN-STD-02** [REPLICATE] (area: NLD-TOOL) Write the breaking-change contract before the first release and apply it to language behavior, cmdlet parameters and protocols alike. Evidence: `docs/dev-process/breaking-change-contract.md`.
- **LSN-STD-03** [ADAPT] (area: NLD-RUN) Keep platform differences behind interfaces rather than `#if` blocks across the engine (PowerShell has `UNIX` in 122 files). Evidence: `data/conditional-compilation.json`; `docs/dev-process/coding-guidelines.md` ("Portable Code").
- **LSN-STD-04** [ADAPT] (area: NLD-RUN) Use the hot-path rules (no LINQ, no `params`, pre-sized collections) only inside the interpreter and runtime core, and let a profiler decide elsewhere. Evidence: `docs/dev-process/coding-guidelines.md` ("Performance Considerations").

## 19. Open questions / UNVERIFIED items

- `UNVERIFIED`: contents of `Settings.StyleCop` beyond its existence (not read in full).
- `UNVERIFIED`: whether CI enforces `.markdownlint.json` (workflow names only).

Verification: severities counted with `grep -c 'severity = <level>' .globalconfig`; props files and guideline read in full; symbol counts from `data/conditional-compilation.json`.
