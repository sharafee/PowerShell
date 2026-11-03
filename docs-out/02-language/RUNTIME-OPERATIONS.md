---
id: LANG-RTOPS-001
title: Runtime operations
kind: subsystem
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/runtime/Operations/MiscOps.cs, src/System.Management.Automation/engine/runtime/Operations/ArrayOps.cs, src/System.Management.Automation/engine/runtime/Operations/NumericOps.cs, src/System.Management.Automation/engine/runtime/Operations/StringOps.cs, src/System.Management.Automation/engine/runtime/Operations/VariableOps.cs, src/System.Management.Automation/engine/runtime/Operations/ClassOps.cs, src/System.Management.Automation/engine/lang/parserutils.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/runtime/_folder.md]
generated_from: [data/types.json, data/members-tierA.json]
---

# Runtime operations

> STATIC-ONLY — behavior not run-verified. `FACT-SRC` unless marked. These are the helper classes that compiled code calls ([COMPILATION-MAP.md](COMPILATION-MAP.md), [IR-SPEC.md](IR-SPEC.md)); the binder rules that choose them are in [BINDER-CATALOG.md](BINDER-CATALOG.md).

## 1. Purpose and scope [SPEC]

Catalog and semantics of the static helper classes in `engine/runtime/Operations/*.cs` plus the operator helpers and flow-control exceptions in `engine/lang/parserutils.cs` (a file whose name does not say so, CON-010). Each helper implements one runtime rule of the language: error-action handling, pipeline invocation, redirections, enumeration, array/hashtable/string arithmetic, numeric overflow rules, type tests, switch matching, class method wrappers.

## 2. Source map

Generated list of every helper type (<!--N:RUNTIME_OP_TYPES-->51<!--/N--> types, `GENERATED` from `data/types.json` and `data/members-tierA.json`):

<!--GEN:runtimeops-->
| Type | File | Lines | Members (scan) |
|---|---|---|---:|
| `FlowControlException` | `parserutils.cs` | L28-L31 | 1 |
| `LoopFlowException` | `parserutils.cs` | L36-L67 | 5 |
| `BreakException` | `parserutils.cs` | L72-L88 | 3 |
| `ContinueException` | `parserutils.cs` | L93-L109 | 3 |
| `ReturnException` | `parserutils.cs` | L111-L119 | 2 |
| `ExitException` | `parserutils.cs` | L124-L139 | 3 |
| `ExitNestedPromptException` | `parserutils.cs` | L144-L146 | 0 |
| `TerminateException` | `parserutils.cs` | L151-L153 | 0 |
| `StopUpstreamCommandsException` | `parserutils.cs` | L160-L168 | 2 |
| `SplitOptions` | `parserutils.cs` | L176-L221 | 0 |
| `PowerShellBinaryOperator` | `parserutils.cs` | L225-L225 | 0 |
| `ParserOps` | `parserutils.cs` | L232-L1624 | 45 |
| `ParserOps.SplitImplOptions` | `parserutils.cs` | L398-L402 | 0 |
| `ParserOps.ReplaceOperatorImpl` | `parserutils.cs` | L963-L1035 | 7 |
| `CompareDelegate` | `parserutils.cs` | L1330-L1330 | 0 |
| `RangeEnumerator` | `parserutils.cs` | L1633-L1699 | 13 |
| `CharRangeEnumerator` | `parserutils.cs` | L1705-L1756 | 9 |
| `InterpreterError` | `parserutils.cs` | L1761-L1966 | 6 |
| `ScriptTrace` | `parserutils.cs` | L1970-L2008 | 2 |
| `ArrayOps` | `ArrayOps.cs` | L13-L301 | 9 |
| `Internal.SessionStateKeeper` | `ClassOps.cs` | L32-L95 | 4 |
| `Internal.ScriptBlockMemberMethodWrapper` | `ClassOps.cs` | L98-L269 | 13 |
| `Internal.ClassOps` | `ClassOps.cs` | L274-L374 | 7 |
| `PipelineOps` | `MiscOps.cs` | L29-L889 | 18 |
| `CommandRedirection` | `MiscOps.cs` | L893-L944 | 4 |
| `MergingRedirection` | `MiscOps.cs` | L946-L1061 | 4 |
| `FileRedirection` | `MiscOps.cs` | L1063-L1333 | 12 |
| `FunctionOps` | `MiscOps.cs` | L1337-L1366 | 1 |
| `ScriptBlockExpressionWrapper` | `MiscOps.cs` | L1368-L1389 | 4 |
| `ByRefOps` | `MiscOps.cs` | L1391-L1400 | 1 |
| `HashtableOps` | `MiscOps.cs` | L1402-L1458 | 2 |
| `ExceptionHandlingOps` | `MiscOps.cs` | L1460-L2197 | 20 |
| `ExceptionHandlingOps.CatchAll` | `MiscOps.cs` | L1462-L1462 | 0 |
| `ExceptionHandlingOps.HandlerSearchResult` | `MiscOps.cs` | L1467-L1481 | 5 |
| `TypeOps` | `MiscOps.cs` | L2199-L2434 | 8 |
| `SwitchOps` | `MiscOps.cs` | L2436-L2590 | 3 |
| `WhereOperatorSelectionMode` | `MiscOps.cs` | L2595-L2621 | 0 |
| `EnumerableOps` | `MiscOps.cs` | L2623-L3667 | 21 |
| `EnumerableOps.NonEnumerableObjectEnumerator` | `MiscOps.cs` | L3408-L3441 | 7 |
| `MemberInvocationLoggingOps` | `MiscOps.cs` | L3669-L3764 | 3 |
| `Boxed` | `NumericOps.cs` | L9-L13 | 2 |
| `IntOps` | `NumericOps.cs` | L15-L129 | 12 |
| `UIntOps` | `NumericOps.cs` | L131-L211 | 11 |
| `LongOps` | `NumericOps.cs` | L213-L310 | 11 |
| `ULongOps` | `NumericOps.cs` | L312-L395 | 11 |
| `DecimalOps` | `NumericOps.cs` | L397-L682 | 32 |
| `DoubleOps` | `NumericOps.cs` | L684-L883 | 18 |
| `CharOps` | `NumericOps.cs` | L885-L944 | 5 |
| `StringOps` | `StringOps.cs` | L15-L107 | 6 |
| `VariableOps` | `VariableOps.cs` | L15-L326 | 8 |
| `VariableOps.UsingResult` | `VariableOps.cs` | L287-L290 | 1 |
<!--/GEN:runtimeops-->

## 3. Responsibilities and non-responsibilities

Implements run-time rules called from the IR. Does not decide which rule applies (binders) or how a command is found (command discovery, T32).

## 4. Key types and contracts [IMPL]

| Group | Types | Contract |
|---|---|---|
| Error handling | `ExceptionHandlingOps` | `CheckActionPreference(funcContext, exception)`, `FindMatchingHandler`, `ProcessTraps`, `ConvertToException`, `SuspendStoppingPipeline`/`RestoreStoppingPipeline` |
| Pipelines | `PipelineOps`, `CommandRedirection`, `MergingRedirection`, `FileRedirection` | `InvokePipeline(input, ignoreInput, commands, ast, redirections, funcContext)`, `InvokePipelineInBackground`, argument splatting, exit exceptions, interrupt checks |
| Enumeration | `EnumerableOps` | enumerators, output unrolling, array concatenation and repetition, `Compare` (array filter), `.Where()` / `.ForEach()` intrinsic methods, member access over collections |
| Arrays and strings | `ArrayOps`, `StringOps`, `CharOps` | repetition, slicing, multi-dimensional access, format operator, string comparison |
| Numbers | `IntOps`, `UIntOps`, `LongOps`, `ULongOps`, `DecimalOps`, `DoubleOps` | arithmetic and comparison with PowerShell overflow and zero-division rules |
| Variables | `VariableOps` | see [SCOPE-AND-VARIABLES.md](SCOPE-AND-VARIABLES.md) |
| Types and switch | `TypeOps`, `SwitchOps`, `HashtableOps`, `FunctionOps`, `ByRefOps` | `-is`/`-as`, switch clause matching, hashtable literal construction, function definition |
| Classes | `ClassOps`, `ScriptBlockMemberMethodWrapper`, `SessionStateKeeper` | class property validation, base calls, method bodies as script blocks |
| Operators | `ParserOps` | `-like`, `-match`, `-replace`, `-split`, `-join`, range, `-contains`, user-defined operator lookup |
| Flow control | `FlowControlException`, `LoopFlowException`, `BreakException`, `ContinueException`, `ReturnException`, `ExitException`, `ExitNestedPromptException`, `TerminateException`, `StopUpstreamCommandsException` | exceptions used for non-local control flow |

## 5. Data model

Flow-control exceptions: `LoopFlowException` carries a label; `MatchLabel` compares ordinal-ignoring-case and an **empty label matches any** loop; `BreakException`/`ContinueException` derive from it; `ReturnException` is internal; `ExitException` carries the exit argument. Boxed constants for `bool` and small `int`s avoid allocations (`Boxed`, caches -100..1000 in `ParserOps`).

## 6. Control flow

### 6.1 `CheckActionPreference` (statement-level error handling)

Called from the per-statement catch block of compiled code ([02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §6.2). Steps (`FACT-SRC`, src/System.Management.Automation/engine/runtime/Operations/MiscOps.cs::ExceptionHandlingOps.CheckActionPreference@L1699-L1788):

1. Unwrap `TargetInvocationException`; convert a non-`RuntimeException` to one (`ConvertToRuntimeException`), updating its error record with the current script position and history id.
2. Set `$Error`/error variables for the statement (`SetErrorVariables`) and set `$?` to `$false`.
3. Read `$ErrorActionPreference` (default `Continue`). If it is `Break` and this is a first-time exception, break into the debugger.
4. If the current block has trap handlers: run `ProcessTraps` (finds a handler by the inner exception type first, then by the outer; runs the handler lambda in a **new scope** with `$_` set to a new `ErrorRecord` and the other automatic variables copied; a `continue` in the trap means *SilentlyContinue*, a `break` means *Stop*; otherwise the action is queried from the exception).
5. Else, if the exception is of a kind that cannot be stopped, continued or ignored → rethrow.
6. Else if the preference is `Inquire` (and prompting is allowed) → ask the host.
7. `SilentlyContinue`/`Ignore` → return (execution resumes at the next statement). `Stop` → mark prompts suppressed and rethrow. Otherwise (`Continue`): if there is no trap and the exception came from a `throw` statement → rethrow; else report the error record to the error stream (`ReportErrorRecord`) and, if it cannot be reported, rethrow.

This is the rule that makes ordinary errors in script statements non-terminating by default while `throw` and `-ErrorAction Stop` terminate. The terminating/non-terminating canonical fact CF-ERR-001 is owned by the errors document (planned T38).

### 6.2 Collections and arrays

`EnumerableOps.WriteEnumerableToPipe` unrolls one level and disposes the enumerator (CF-PIP-001, [02.6-types-and-operators.md](02.6-types-and-operators.md)). `ArrayOps.Multiply<T>(array, times)`: `times == 1` returns the same array; 0 or empty gives an empty array; the result is built by repeated doubling copies; the element count must fit `int` (else an invalid-cast error); in RestrictedLanguage mode (data sections) the result may not exceed 1,024 elements. `ArrayOps.SlicingIndex` collects `indexer(target, i)` results for each index and drops `AutomationNull` results. `ArrayOps.AddObjectArray` appends by resizing (array `+` scalar returns a new array).

### 6.3 Strings and hashtables

`StringOps.Multiply(s, n)`: negative `n` throws `ArgumentOutOfRangeException` (a source TODO says it should be a runtime error); 0 or empty gives the empty string; in RestrictedLanguage mode the result may not exceed 1,024 characters. `StringOps.Add` is `string.Concat`. `HashtableOps.AddKeyValuePair` rejects a `$null` key (`InvalidNullKey`) and a duplicate key (`DuplicateKeyInHashLiteral`, key text truncated to 40 characters); `HashtableOps.Add(a, b)` builds a new `Hashtable` (or `OrderedDictionary` when the left side is ordered) with a culture-ignore-case comparer and `Add`s all keys, so a key present on both sides throws. **Quirk:** hashtable literals use an ordinal-ignore-case comparer (`Compiler.BuildHashtable`) while `+` uses the current-culture-ignore-case comparer.

## 7. Algorithms

Numeric operators: see [02.6-types-and-operators.md](02.6-types-and-operators.md) §7.2. Flow control: [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §6.3-6.4. Operator helpers and their regex cache: [OPERATOR-TABLE.md](OPERATOR-TABLE.md).

## 8. Observable behavior [SPEC]

`$a = 1,2; $a * 2` gives a 4-element array; `"ab" * 2` gives `"abab"`; `@{a=1} + @{a=2}` throws; `@{a=1;A=2}` throws a duplicate-key error; a failing statement in a script continues unless the preference or a trap says otherwise. No golden sample: STATIC-ONLY.

## 9. Error handling and edge cases

`InterpreterError.NewInterpreterException` builds runtime errors whose ids and messages are `ParserStrings` keys ([ERROR-CATALOG.md](ERROR-CATALOG.md) §4); `NewBackupInterpreterException` falls back to a generic message when the resource lookup fails. `ScriptTrace.Trace` writes `Set-PSDebug -Trace` lines when the trace level is high enough.

## 10. Concurrency and threading

All helpers are static and stateless except caches: boxed-int cache, regex cache (≤1,000 per option set), `s_` caches in `EnumerableOps`; they rely on the execution context obtained from thread-local storage (`LocalPipeline.GetExecutionContextFromTLS`).

## 11. Extension points and customization hooks

None public; adding a runtime rule means adding a helper and calling it from the compiler or a binder ([HOWTO-extend-language.md](HOWTO-extend-language.md)).

## 12. Dependencies

Inbound: compiled code, binders. Outbound: execution context, command processors (pipelines), providers (redirection to files), debugger, `PSObject`.

## 13. Performance notes

Boxed constants and small caches; array repetition by doubling copies; `IntOps` returns boxed objects but avoids exceptions on overflow.

## 14. Security considerations (mandatory)

RestrictedLanguage mode caps `string * n` and array repetition at 1,024 to bound data-section evaluation; no such cap exists in Full Language mode. `MemberInvocationLoggingOps` logs member invocations when enabled. `ExceptionHandlingOps.CheckActionPreference` honors `Inquire` prompts through the host. `SwitchOps.ResolveFilePath` resolves the `-file` argument at run time.

## 15. Enterprise considerations

Error variables, `$?`, error records with script positions and history ids are produced here; `ScriptTrace` offers statement tracing. Missing: no cap on repeated sizes outside data sections.

## 16. Tests

Not read per assertion (VB-005).

## 17. Design decisions and trade-offs

| Decision | Label | Consequence |
|---|---|---|
| language rules as static helpers called from compiled code | `FACT-SRC` | rules testable in isolation; compiler stays small per node |
| non-local control flow by exceptions | `FACT-SRC` | simple across script-block boundaries, slow for deep unwinding |
| errors are reported and execution continues by default | `FACT-SRC` | shell-style resilience; `throw`/Stop needed to abort |

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-RTOPS-01** [REPLICATE] (area: NLD-ERR) Implement the seven-step error-action algorithm of §6.1 as one function used by the statement runner. Evidence: src/System.Management.Automation/engine/runtime/Operations/MiscOps.cs::ExceptionHandlingOps.CheckActionPreference@L1699-L1788.
- **LSN-RTOPS-02** [REPLICATE] (area: NLD-PIP) Use label-carrying break/continue signals where an empty label matches any loop. Evidence: src/System.Management.Automation/engine/lang/parserutils.cs::LoopFlowException@L36-L67.
- **LSN-RTOPS-03** [REPLICATE] (area: NLD-OP) Hashtable literal construction rejects null and duplicate keys; `+` of hashtables creates a new table and throws on a shared key. Evidence: src/System.Management.Automation/engine/runtime/Operations/MiscOps.cs::HashtableOps@L1402-L1458.
- **LSN-RTOPS-04** [ADAPT] (area: NLD-OP) Cap string and array repetition in all modes (not only data sections). Why: PowerShell caps only in restricted mode; a personal shell should not be able to exhaust memory by accident. Evidence: src/System.Management.Automation/engine/runtime/Operations/StringOps.cs::StringOps@L15-L107, src/System.Management.Automation/engine/runtime/Operations/ArrayOps.cs::ArrayOps@L13-L301.
- **LSN-RTOPS-05** [AVOID] (area: NLD-RUN) Do not port the class-method wrapper machinery (`ScriptBlockMemberMethodWrapper`, `SessionStateKeeper`, Reflection.Emit class definition) in the first versions; classes are EXTENDED scope. Evidence: src/System.Management.Automation/engine/runtime/Operations/ClassOps.cs::ScriptBlockMemberMethodWrapper@L98-L269. DEV: DEV-RTOPS-051

## 19. Open questions / UNVERIFIED

- Not read: `PipelineOps.InvokePipeline`, redirection classes, `EnumerableOps.Where/ForEach/MethodInvoker`, `TypeOps`, `SwitchOps`, `ClassOps` bodies (names and ranges only, VB-021).
- `ConvertToException` / `ReportErrorRecord` details; `QueryForAction` for traps.

Verification: `ExceptionHandlingOps.CheckActionPreference` and `ProcessTraps` (L1699-L1908), `HashtableOps` (L1402-L1458), `ArrayOps` (L15-L112), `StringOps` (L15-L60), `EnumerableOps.WriteEnumerableToPipe` (L3623-L3640) were read; `parserutils.cs` from the earlier notes (W1-W7); the type table is generated.
