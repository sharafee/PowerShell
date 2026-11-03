---
id: LANG-SCRIPTBLOCK-001
title: Script blocks
kind: subsystem
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/lang/scriptblock.cs, src/System.Management.Automation/engine/runtime/CompiledScriptBlock.cs, src/System.Management.Automation/engine/runtime/ScriptBlockToPowerShell.cs, src/System.Management.Automation/engine/Modules/PSModuleInfo.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/lang/_folder.md]
generated_from: [data/members-tierA.json]
---

# Script blocks

> STATIC-ONLY — behavior not run-verified. `FACT-SRC` unless marked. Related: [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) (compilation and invocation), [SCOPE-AND-VARIABLES.md](SCOPE-AND-VARIABLES.md) (`$using:`), [TIERING-POLICY.md](TIERING-POLICY.md).

## 1. Purpose and scope [SPEC]

A *script block* (`ScriptBlock`) is the first-class value for a piece of code: the content of `{ … }`, a function body, a script file or a module. It can be stored in variables, passed to cmdlets (`ForEach-Object { }`), invoked with `&`/`.`/`.Invoke()`, bound to a session state (closures, modules) and converted to a .NET delegate. This document covers the `ScriptBlock` type, its creation and sharing rules, invocation entry points, closure binding and `$using:` support.

## 2. Source map

| path | type | role | tier |
|---|---|---|---|
| src/System.Management.Automation/engine/lang/scriptblock.cs::ScriptBlock@L83-L1085 | partial class | public API: `Create`, `Invoke*`, `GetNewClosure`, `GetPowerShell`, delegates | A |
| src/System.Management.Automation/engine/runtime/CompiledScriptBlock.cs::ScriptBlock@L542-L2177 | partial class | cache, `InvokeWithPipeImpl`, compile access | A |
| src/System.Management.Automation/engine/runtime/CompiledScriptBlock.cs::CompiledScriptBlockData@L41-L540 | class | shared data (AST, delegates, metadata) | A |
| src/System.Management.Automation/engine/lang/scriptblock.cs::SteppablePipeline@L1095-L1332 | class | step-by-step pipeline from a script block (not analyzed) | A |
| src/System.Management.Automation/engine/runtime/ScriptBlockToPowerShell.cs::ScriptBlockToPowerShellConverter@L210-L952 | class | convert a simple script block to a `PowerShell` object | A |
| src/System.Management.Automation/engine/Modules/PSModuleInfo.cs::PSModuleInfo@L23-L1554 | class | module object used to bind closures | A |

## 3. Responsibilities and non-responsibilities

Value semantics of script blocks: creation, identity, sharing, binding, invocation entry points. Not responsible for compilation internals (T25) or for function/filter definition (command discovery, T32).

## 4. Key types and contracts [IMPL]

- `ScriptBlock.Create(string)` parses with a new `Parser` and caches by (file name, text); the internal overload taking an `ExecutionContext` additionally binds the block to the current module session state when the engine is inside a module (src/System.Management.Automation/engine/lang/scriptblock.cs::ScriptBlock.Create@L90-L99).
- A `ScriptBlock` object is a thin handle: `_scriptBlockData` (the shared `CompiledScriptBlockData`), a bound session state, and the language mode captured from the creating context. `Clone()` makes a new handle over the **same** data, so compiled delegates are shared between clones and between cached copies (src/System.Management.Automation/engine/runtime/CompiledScriptBlock.cs::ScriptBlock.TryGetCachedScriptBlock@L583-L601).
- Properties: `Attributes`, `File`, `IsFilter`, `IsConfiguration`, `Module`, `StartPosition`, `LanguageMode`, `OutputType`, `SessionState` (src/System.Management.Automation/engine/lang/scriptblock.cs::ScriptBlock@L83-L1085).
- Invocation: `Invoke(args)` (returns a `Collection<PSObject>`), `InvokeReturnAsIs(args)` (result object as is), `InvokeWithContext(functions, variables, args)` (defines extra functions/variables in a new scope), `InvokeUsingCmdlet`, all funneling into `DoInvoke`/`DoInvokeReturnAsIs` → `InvokeWithPipeImpl` ([02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §6.1). `InvokeAsMemberFunction*` serve class methods. `GetDelegate`/`CreateDelegate` convert to a delegate type.

## 5. Data model

Handle fields: bound `SessionStateInternal` (or null = use the caller's), `LanguageMode`, debugger-hidden flags; shared data fields: AST, per-clause delegates (optimized and unoptimized), locals tuple types, name → slot map, sequence points, a `Guid` id per data object (new for each parsed script block, not for clones).

## 6. Control flow

Creation → (parse) → handle; invocation → bind arguments, choose variant, create scope or push dotted scope, run clause delegate. A closure is created as follows (`GetNewClosure`): make a dynamic module object (`new PSModuleInfo(true)`); `CaptureLocals` copies into the module's session state every variable of the **current scope** (the locals tuple plus the scope's variable table) whose options are `None` (not read-only, constant, private or all-scope, and not the `$null` variable), as new `PSVariable` objects holding the current **values** (a value snapshot, not a reference; parent-scope variables are not captured); `NewBoundScriptBlock` clones the script block with `SessionState` set to the module's session state, so that variables are resolved there when it runs (src/System.Management.Automation/engine/lang/scriptblock.cs::ScriptBlock.GetNewClosure@L119-L124, src/System.Management.Automation/engine/Modules/PSModuleInfo.cs::PSModuleInfo.CaptureLocals@L1343-L1370, src/System.Management.Automation/engine/Modules/PSModuleInfo.cs::PSModuleInfo.NewBoundScriptBlock@L1245-L1269).

## 7. Algorithms

- **Binding to a module/session state**: `PSModuleInfo.Invoke(sb, args)` temporarily sets the script block's session state to the module's and calls `InvokeReturnAsIs`, restoring the old one in a `finally`; `NewBoundScriptBlock` swaps `context.EngineSessionState` under a lock while cloning.
- **`$using:`**: the compiler replaces `$using:name` by `VariableOps.GetUsingValue(locals, key, index, context)`; values are supplied through `$PSBoundParameters.ImplicitUsingParameters` set by the caller that starts the script block elsewhere (jobs, remoting, `ForEach-Object -Parallel`) ([SCOPE-AND-VARIABLES.md](SCOPE-AND-VARIABLES.md) §7.4). `ScriptBlock.GetPowerShell(variables, out usingVariables, …)` extracts the using variables of a block into a dictionary and builds a `PowerShell` object for it (`ScriptBlockToPowerShellConverter`; details of the converter and of its restrictions to simple pipelines are `UNVERIFIED`, `GetSimplePipeline` rules are in [02.3-ast.md](02.3-ast.md) §5 notes).
- **Delegate conversion**: a language conversion from `ScriptBlock` to any delegate type (`ConvertScriptBlockToDelegate`, [CONVERSION-RULES.md](CONVERSION-RULES.md) §7.1 step 8).

## 8. Observable behavior [SPEC]

Read from source: two `ScriptBlock.Create` calls with the same text return different handles sharing compiled data; a block created in a module is bound to that module's session state; `$f = { $x }.GetNewClosure()` keeps the value `$x` had when the closure was made (snapshot) while a plain block sees the variable at call time through dynamic scoping. No golden sample: STATIC-ONLY. Tests: `test/powershell/Language/Scripting/` (mapping `UNVERIFIED`).

## 9. Error handling and edge cases

`Create` throws `ParseException` for syntax errors; `GetScriptBlock()` on an AST with errors throws; `Invoke` of an empty or missing clause returns nothing; `Clean` is not invokable through `InvokeWithPipeImpl`. Binding a closure to a binary module throws `InvalidOperationOnBinaryModule`. A closure captured inside a loop copies only the current scope's variables, so loop variables from parent scopes are not captured.

## 10. Concurrency and threading

Compiled data are shared and published under locks (T25); the script block cache is a `ConcurrentDictionary`; handles are not thread-affine but the session state they bind is.

## 11. Extension points and customization hooks

Delegates created from script blocks, `ScriptBlock.Create` for code generation, `InvokeWithContext` to inject functions/variables, `ScriptBlockInvocationEventArgs` for host/job instrumentation (`UNVERIFIED`).

## 12. Dependencies

Inbound: functions, scripts, modules, `ForEach-Object`/`Where-Object`, jobs, remoting, event handlers. Outbound: parser, compiler, session state, module system, `PowerShell` API.

## 13. Performance notes

Cloning avoids recompilation; `GetNewClosure` allocates a module object and copies variables each time (cost proportional to the scope size).

## 14. Security considerations (mandatory)

A script block remembers the language mode of its creator, so passing a constrained block into a full-language session does not elevate it; the transition rules are in `InvokeWithPipeImpl` ([02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §14). `GetPowerShell` and `$using:` extraction run in an untrusted-input mode unless `isTrustedInput` is passed.

## 15. Enterprise considerations

Script block logging uses the shared data's id and text ([02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §14). Missing: no public identity for a block independent of its text.

## 16. Tests

Not read (VB-005).

## 17. Design decisions and trade-offs

| Decision | Label | Consequence |
|---|---|---|
| handle + shared compiled data | `FACT-SRC` | cheap clones, cached compilation; state binding is per handle |
| closures via a dynamic module | `FACT-SRC` | reuses module session state; snapshot semantics; only current-scope variables |
| language mode captured at creation | `FACT-SRC` | policy follows the code, not the caller |

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-SB-01** [REPLICATE] (area: NLD-SCP) Make a script block a first-class value with an AST, a bound scope (optional), and a captured language mode (if any); share the parsed/compiled data between clones. Evidence: src/System.Management.Automation/engine/runtime/CompiledScriptBlock.cs::ScriptBlock.TryGetCachedScriptBlock@L583-L601.
- **LSN-SB-02** [REPLICATE] (area: NLD-SCP) `GetNewClosure` snapshots the **current scope's** unrestricted variables by value into a private scope bound to the clone. Evidence: src/System.Management.Automation/engine/Modules/PSModuleInfo.cs::PSModuleInfo.CaptureLocals@L1343-L1370.
- **LSN-SB-03** [REPLICATE] (area: NLD-SCP) Provide `Invoke`, `InvokeReturnAsIs` (call operator semantics) and `InvokeWithContext` as separate entry points funneling into one invoke routine. Evidence: src/System.Management.Automation/engine/lang/scriptblock.cs::ScriptBlock.InvokeWithContext@L412-L443.
- **LSN-SB-04** [ADAPT] (area: NLD-SCP) Implement closures without a module object: a scope object holding the snapshot. Why: same observable behavior; module objects are EXTENDED scope. Evidence: src/System.Management.Automation/engine/lang/scriptblock.cs::ScriptBlock.GetNewClosure@L119-L124.
- **LSN-SB-05** [AVOID] (area: NLD-RUN) Omit steppable pipelines and the `PowerShell` object conversion (`GetPowerShell`) in the first versions. Evidence: src/System.Management.Automation/engine/lang/scriptblock.cs::SteppablePipeline@L1095-L1332. DEV: DEV-SB-090

## 19. Open questions / UNVERIFIED

- `ScriptBlockToPowerShellConverter` rules for which blocks convert, parameter and `$using` rewriting (VB-022).
- Behavior of `InvokeWithContext` variable/function injection beyond its signature.
- `SteppablePipeline` and `ScriptBlockInvocationEventArgs` semantics.

Verification: `scriptblock.cs` public surface (L83-L400, member list L83-L1085), `GetNewClosure`, `PSModuleInfo.CaptureLocals`/`NewBoundScriptBlock`/`Invoke`, `ScriptBlock.TryGetCachedScriptBlock`/`CacheScriptBlock` and `InvokeWithPipeImpl` (earlier notes) were read; the rest of the 1,479-line file is inventory.
