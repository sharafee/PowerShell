# Glossary and controlled vocabulary (rule 21)

## Tag and label vocabularies

- Section tags (rule 13): `SPEC` (observable behavior), `IMPL` (this source's implementation), `LESSON` (design lesson for the new shell).
- Verdicts (rule 16, the only lesson vocabulary): `REPLICATE`, `ADAPT`, `REDESIGN`, `AVOID`. `REDESIGN`/`AVOID` are proposals only (one `DEV-*` row each).
- Epistemic labels (rule 19): `FACT-SRC` (E1), `FACT-RUN` (E2), `INFERENCE`, `EXTERNAL`, `UNVERIFIED`; modifiers `APPROX`, `GENERATED`, `VERSION-MISMATCH`.
- Evidence classes (rule 1): `E1` source, `E2` run of engine built from the pin, `E3` run on other-version pwsh, `E4` external.
- Scope classes (4.3): `CORE`, `EXTENDED`, `OUT-OF-SCOPE-DOCUMENTED`. Tiers (4.1): `A`, `B`, `C`.
- ID schemes: `CF-<AREA>-NNN`, `DEV-<AREA>-NNN`, `CON-NNN`, `GS-<AREA>-NNN`, `CLM-<AREA>-NNNN`, `SEC-ENF-NNN`, `NLD-<AREA>-NNN`, document IDs `<AREA>-<TOPIC>-NNN`.

## Pipeline vocabulary (the words are fixed here; what the repo does under each word is established by evidence and recorded as a CF)

| preferred term | definition | forbidden synonyms |
|---|---|---|
| tokenize | text -> tokens | lexing, lexer |
| parse | tokens -> AST | syntax-analyze |
| analyze | AST -> checks (semantic analysis, static checks) | semantically-validate |
| compile | AST -> intermediate representation (expression trees in PowerShell) | transpile |
| JIT-compile | intermediate representation -> executable delegate (IL) at run time | jit-compilation step |
| interpret | execute the intermediate representation with an instruction-based interpreter (the light compiler in PowerShell) | light-interpret |
| tree-walk | evaluate the AST directly; any statement that PowerShell tree-walks must cite evidence | ast-interpret |
| tier / tiering | switching the execution mode of the same script block or loop between interpret and JIT-compile | promotion to compiled mode |
| execute | umbrella word, used only in lifecycle documents | |

## Engine vocabulary (each defined once, with the implementing source types; verified present by `data/types.json`)

| preferred term | definition | forbidden synonyms |
|---|---|---|
| script block | a parsed, invocable block of script; `System.Management.Automation.ScriptBlock` (`engine/lang/scriptblock.cs`, `engine/runtime/CompiledScriptBlock.cs`) | scriptblock (in prose), code block |
| function | a named script block registered in session state; `FunctionInfo` (`engine/FunctionInfo.cs`) | proc, procedure |
| filter | a function whose body runs as a `process` block; `FilterInfo` (`engine/FilterInfo.cs`) | |
| cmdlet | a .NET class deriving from `Cmdlet`/`PSCmdlet` with a `[Cmdlet]` attribute; `CmdletInfo`, `Cmdlet`, `PSCmdlet` | commandlet |
| command | any invocable thing resolved by name: alias, function, filter, cmdlet, script, application; `CommandInfo` and subclasses | |
| pipeline | a sequence of commands connected by pipes; `PipelineProcessor` (`engine/pipeline.cs`), `Pipe` (`engine/Pipe.cs`); the public wrapper is `Runspaces.Pipeline` | |
| runspace | the execution environment owning an `ExecutionContext`/session state; `Runspaces.Runspace`, `LocalRunspace` | run space |
| session state | per-runspace store of variables, functions, aliases, drives, providers, modules; `SessionState`, `SessionStateScope` | sessionstate (in prose) |
| scope | a variable/function/alias namespace layer with a parent; `SessionStateScope` | |
| provider | a data-store adapter exposing items under drives; `Provider.CmdletProvider`, `ProviderInfo`, `PSDriveInfo` | data provider |

## Persian term mapping

Not used (`FA_DIGEST=false`).
