---
id: LANG-EQUIV-001
title: Equivalence specification
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/interpreter/Interpreter.cs, src/System.Management.Automation/engine/interpreter/LightCompiler.cs, src/System.Management.Automation/engine/interpreter/LoopCompiler.cs, src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs, src/System.Management.Automation/engine/parser/Compiler.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/interpreter/_folder.md]
generated_from: []
---

# Equivalence specification

> STATIC-ONLY — behavior not run-verified. No oracle (`pwsh`) ran, so every statement is `FACT-SRC` about *how the code is built to be equivalent* or `INFERENCE`/`UNVERIFIED` about whether it is. Related: [TIERING-POLICY.md](TIERING-POLICY.md), [IR-SPEC.md](IR-SPEC.md), [INSTRUCTION-SET.md](INSTRUCTION-SET.md), [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md).

## 1. Purpose and scope [SPEC]

The same IR runs in two ways: through the instruction interpreter and as JIT-compiled code, and a call can switch from one to the other at any call boundary (and a running loop can switch mid-execution). Scripts must not be able to tell. This document lists the **equivalence obligations** between the two tiers and the optimized/unoptimized variants, how the code meets each (or fails to), and what a new implementation with a single tree-walking tier must preserve.

## 2. Source map

| path | role |
|---|---|
| src/System.Management.Automation/engine/interpreter/Interpreter.cs::Interpreter@L31-L109 | instruction loop |
| src/System.Management.Automation/engine/interpreter/InterpretedFrame.cs::InterpretedFrame@L28-L332 | frame: locals, stack, continuations |
| src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs::EnterTryCatchFinallyInstruction@L305-L447 | interpreted try/catch/finally |
| src/System.Management.Automation/engine/interpreter/LoopCompiler.cs::LoopCompiler@L29-L384 | hand-over of a running loop to JIT code |
| src/System.Management.Automation/engine/interpreter/LightLambda.cs::LightLambda@L43-L302 | tier switch at call boundaries |

## 3. Responsibilities and non-responsibilities

Specifies what must be equal; it does not choose the tier ([TIERING-POLICY.md](TIERING-POLICY.md)).

## 4. Key types and contracts [IMPL]

Both tiers consume the same `Expression<Action<FunctionContext>>`. The interpreter compiles it to `InstructionArray` once and runs it per call with an `InterpretedFrame`; the JIT form is `LambdaExpression.Compile()` of the same tree (for lambdas with closure variables the `LightLambdaClosureVisitor` rewrites captured variables; `Compiler` produces none, `INFERENCE`).

## 5. Data model — equivalence obligations

| ID | Obligation | How the code meets it | Status |
|---|---|---|---|
| EQ-01 | Same result and output order for every statement | one IR; instructions and LINQ nodes implement the same operations; dynamic sites use the same binders in both tiers | `FACT-SRC` (design) |
| EQ-02 | Same binding rules for operators, members, conversions | `Expression.Dynamic` becomes a `DynamicInstruction<…>` holding its own `CallSite`; binding rules come from the PowerShell binders, not from either tier | `FACT-SRC`; per-site caches are separate per tier (performance only) |
| EQ-03 | Same exception behavior: type, message, catch order, rethrow identity | interpreter `try/catch/finally` instruction uses CLR `try/catch/finally` inside the instruction and picks the first handler assignable from the exception type, as the CLR does; `RethrowException` marks a rethrow; stack trace is saved into `Exception.Data` | `FACT-SRC` code shape; stack-trace text differs (interpreted frames are reported through `InterpretedFrameInfo`) |
| EQ-04 | `finally` runs on `return`/`break`/`continue`/exception | interpreter uses continuation stacks (`EnterFinally`/`LeaveFinally`, pending continuation) for gotos leaving a `try`; JIT uses the CLR | `FACT-SRC`; equivalence untested here |
| EQ-05 | Flow-control exceptions pass through catch-alls | the IR catches `FlowControlException` first and rethrows; the interpreter lets `RethrowException` pass | `FACT-SRC` |
| EQ-06 | Same `$?`, same output pipe contents | `$?` and pipe writes are explicit IR operations (calls/field stores), not tier features | `FACT-SRC` |
| EQ-07 | Same error positions and breakpoint behavior | `UpdatePositionExpr` reduces to `DebugInfo` + store (JIT) or `UpdatePositionInstruction` (interpreter); both store the sequence-point index and call `OnSequencePointHit` if debugging | `FACT-SRC` |
| EQ-08 | Same variable visibility | locals tuple is a heap object in both tiers; the tier does not change slots | `FACT-SRC` |
| EQ-09 | Value-type receivers are mutated in place | interpreter's reflection field store works on a boxed copy, so the light compiler forces JIT for instance calls on non-primitive value types and by-ref calls | `FACT-SRC` (workaround for a known interpreter limit) |
| EQ-10 | Mid-loop promotion keeps state | `LoopCompiler` copies variables in from the frame (`Data`, closure boxes), runs the loop as JIT code, writes modified variables back in a `finally`, and exits via `frame.Goto` for jumps leaving the loop; the evaluation stack is not transferred | `FACT-SRC`; correctness of write-back for all shapes `UNVERIFIED` |
| EQ-11 | Arithmetic and comparison on primitive types | the IR uses native typed operators only for `double`; everything else is a dynamic site, so the typed interpreter instructions are not reached from PowerShell IR | `INFERENCE` (see defects below) |
| EQ-12 | Thread safety of promotion | counters race benignly; compile takes a lock and runs once; published delegate used by later calls | `FACT-SRC` |

## 6. Control flow

Not applicable: this document specifies properties, not a flow. The tier-switch points are: (1) call boundary (`LightLambda.TryGetCompiled`), (2) loop-top arrival (`EnterLoopInstruction`).

## 7. Algorithms

### 7.1 Known non-equivalences and defects (reading only, not run)

- **Interpreter instruction defects.** `AddInstruction`, `SubInstruction`, `MulInstruction`, `DivInstruction` (and their overflow variants) cast `UInt64` operands to `Int16` in the `UInt64` nested class (sites: `AddInstruction.cs` L98 and L231, same lines in `Sub`/`Mul`, `DivInstruction.cs` L98); `EqualInstruction.Create`/`NotEqualInstruction.Create` map the unsigned integer types to the signed classes; `EqualInstruction.Create(typeof(string))` falls through to `NotImplementedException`. These classes are inherited DLR code; the compiler emits typed arithmetic only for `double` (`Compiler.cs` L5742-L5771), so they should be unreachable (`INFERENCE`, VB-016).
- **Unsupported shapes** throw `NotImplementedException` in the light compiler ([IR-SPEC.md](IR-SPEC.md) §7.2).
- **`LessThanOrEqual`/`GreaterThanOrEqual`** have no instruction (`InstructionList` throws `NotSupportedException`).
- **Nondeterministic tier** (async promotion): only performance and debugger-visible differences are allowed.
- **Exception stack traces** differ in shape between tiers.

### 7.2 Obligations for a single-tier tree-walker (the MicroteamShell case)

A tree-walking evaluator inherits EQ-01..EQ-08 automatically if it implements the protocols of [IR-SPEC.md](IR-SPEC.md) §5 once. It needs no EQ-09..EQ-12. It must still decide: evaluation order (arguments left to right; for assignments the right side before the left target's member/index operands); that `finally` runs on every exit; that flow-control signals are not swallowed by catch-all handling; that each statement updates the current sequence point before evaluation.

## 8. Observable behavior [SPEC]

None directly. Verification plan: run each corpus snippet with the call counter forced low and forced high (`UNVERIFIED`, needs a hook not present in release builds), compare output, error records and `$?`.

## 9. Error handling and edge cases

A compile failure of the JIT form on the pool thread leaves the interpreted form running; whether the failure is logged was not found (`UNVERIFIED`).

## 10. Concurrency and threading

EQ-12. A call may run interpreted while the same lambda is being compiled on another thread; both forms read the same `FunctionContext` types and heap locals.

## 11. Extension points and customization hooks

`IInstructionProvider` lets an extension node supply interpreter instructions directly; every new extension node must also have a correct `Reduce()` for the JIT (the two must stay equivalent).

## 12. Dependencies

`System.Linq.Expressions` (JIT), the interpreter folder, the PowerShell binders.

## 13. Performance notes

Equivalence is the reason for forced JIT on by-ref/value-type calls: correctness over start-up speed.

## 14. Security considerations (mandatory)

Security checks (language mode, AMSI, logging) sit outside both tiers (in `InvokeWithPipeImpl` and `PerformSecurityChecks`), so tier choice cannot bypass them; the debugger-induced switch to unoptimized code does not change enforcement (`FACT-SRC`, [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §14).

## 15. Enterprise considerations

No differential-test harness for tier equivalence was found in the source tree (`UNVERIFIED`); this is the main testability gap.

## 16. Tests

None located for tier parity (VB-014).

## 17. Design decisions and trade-offs

| Decision | Label | Consequence |
|---|---|---|
| keep one IR for both tiers | `FACT-SRC` | equivalence by construction for ordinary nodes |
| work around interpreter limits by forcing JIT | `FACT-SRC` | unsupported cases cost start-up time instead of correctness |
| inherit DLR interpreter wholesale | `INFERENCE` | dead and defective instruction classes remain |

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-EQV-01** [REPLICATE] (area: NLD-RUN) Define behavior once, in the evaluator and the protocols, never per execution strategy; if two strategies are ever added, test them differentially. Evidence: src/System.Management.Automation/engine/interpreter/Interpreter.cs::Interpreter@L31-L109.
- **LSN-EQV-02** [REPLICATE] (area: NLD-ERR) `finally` must run for every exit (return, break, continue, throw) and flow-control signals must never be swallowed by catch-all handlers. Evidence: src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs::EnterTryCatchFinallyInstruction@L305-L447.
- **LSN-EQV-03** [AVOID] (area: NLD-RUN) Do not port the typed arithmetic/comparison instruction families or the DLR-derived interpreter; they are unreachable or defective for PowerShell. Replace with the evaluator's own numeric semantics from [CONVERSION-RULES.md](CONVERSION-RULES.md). Evidence: src/System.Management.Automation/engine/interpreter/Instruction.cs::Instruction@L27-L70. DEV: DEV-EQV-061

## 19. Open questions / UNVERIFIED

- VB-016: confirm by a search of `Compiler.cs` and binder code that no path creates a typed instruction for `UInt64`/`string`.
- Whether mid-loop promotion preserves all `try/finally` states entered before the loop (the stack is not transferred).
- No oracle: all of EQ-01..EQ-12 remain design claims.

Verification: `ControlFlowInstructions.cs`, `LoopCompiler.cs`, `LightLambda.cs`, `LightCompiler.cs`, `InstructionList.cs`, the arithmetic instruction files and `Utilities.cs` were read in full (interpreter notes); defect sites re-checked in the notes with line numbers; `Compiler.cs` arithmetic emission L5742-L5771 cross-read.
