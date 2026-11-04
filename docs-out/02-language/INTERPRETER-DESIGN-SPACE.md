---
id: LANG-DESIGNSPACE-001
title: Interpreter design space
kind: guide
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/parser/Compiler.cs, src/System.Management.Automation/engine/interpreter/LightCompiler.cs, src/System.Management.Automation/engine/runtime/CompiledScriptBlock.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/interpreter/_folder.md]
generated_from: [data/interpreter-scores.json]
---

# Interpreter design space

> STATIC-ONLY — behavior not run-verified. Facts about PowerShell's own strategy (`S0`) are **linked, not restated**: [TIERING-POLICY.md](TIERING-POLICY.md), [IR-SPEC.md](IR-SPEC.md), [INSTRUCTION-SET.md](INSTRUCTION-SET.md), [EQUIVALENCE-SPEC.md](EQUIVALENCE-SPEC.md). `FACT-SRC` = repository evidence, `EXTERNAL` = .NET facts (cross-check only), `INFERENCE` = this study's reasoning. A claim that PowerShell does not interpret the AST directly is a statement about PowerShell (`S0`); a recommendation to start with an AST tree-walker is a statement about the new shell (`S1`); they are kept separate (contradiction candidate C5 of the study prompt).

## 1. Purpose and scope [SPEC]

Choose an execution strategy for MicroteamShell (C#/.NET, personal use, Windows). This document describes the options, scores them with fixed criteria and weights, applies hard gates, and gives two recommendations (JIT allowed, NativeAOT required) with sensitivity and a build order.

## 2. Anatomy of PowerShell's strategy (links only)

What is compiled, interpreted and dynamic: AST → expression trees ([COMPILATION-MAP.md](COMPILATION-MAP.md)); trees → instruction array or JIT delegate ([TIERING-POLICY.md](TIERING-POLICY.md) §7.2); dynamic call sites with per-site caches ([BINDER-CATALOG.md](BINDER-CATALOG.md) §4); start-up and warm-up (interpret first, JIT after counters, optimized variant only without debugging, [TIERING-POLICY.md](TIERING-POLICY.md) §7.1); caching (script block cache, shared compiled data, [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §4). Equivalence obligations between tiers: [EQUIVALENCE-SPEC.md](EQUIVALENCE-SPEC.md). Facts versus inference are separated in those documents.

## 3. .NET constraints (EXTERNAL, cross-check only)

- NativeAOT forbids `Reflection.Emit` and runtime code generation; `Expression.Compile` then falls back to an interpreter with degraded performance (`EXTERNAL`).
- Lightweight code generation used by the DLR is unavailable under AOT (`EXTERNAL`).
- `AssemblyLoadContext` allows collectible assemblies, which bound the memory of dynamic assemblies, but Windows-only personal use does not need unloading (`EXTERNAL`, `INFERENCE`).
- ReadyToRun reduces JIT start-up cost at the price of larger binaries and less optimized code until tiered JIT replaces it (`EXTERNAL`).

## 4. Options

`S0` PowerShell-faithful tiered pipeline; `S1` AST tree-walking interpreter; `S2` custom bytecode VM; `S3` `System.Linq.Expressions` compilation to delegates (cache and invalidation by script block identity); `S4` `Reflection.Emit` dynamic assemblies; `S5` source-generated ahead-of-time code for built-in commands (a complement, not a script engine); `S6` hybrid of `S1` and `S2` with count-based promotion. S2 sketch: a stack machine over an `object` stack with locals in a frame array, one instruction per AST operation, jump offsets for loops and `try` regions, explicit continuation records for `finally` (the structure of the instruction set in [INSTRUCTION-SET.md](INSTRUCTION-SET.md)).

## 5. Scoring (rendered from data)

Weights sum to 100 (fidelity 25, sandboxability 15, startup 10, throughput 10, debuggability 10, AOT-friendliness 10, determinism 5, memory 5, observability 5, simplicity 5). Scores 1-5 from `data/interpreter-scores.json`; totals, gates and recommendations are computed by `tools/gen_coord.py` (<!--N:INTERPRETER_OPTIONS-->7<!--/N--> options).

<!--GEN:scores-->
| Option | Name | Behavioral fidelity (25) | Sandboxability (15) | Startup latency (10) | Steady-state throughput (10) | Debuggability (10) | AOT-friendliness (10) | Determinism (5) | Memory footprint (5) | Observability (5) | Implementation simplicity (5) | Weighted total (max 5) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S0 | PowerShell-faithful tiered pipeline (AST → expression trees → light interpreter → JIT) | 5 | 3 | 3 | 5 | 4 | 1 | 2 | 2 | 4 | 1 | **3.45** |
| S1 | AST tree-walking interpreter | 4 | 5 | 5 | 2 | 5 | 5 | 5 | 4 | 4 | 5 | **4.35** |
| S2 | Custom bytecode VM | 4 | 5 | 4 | 3 | 3 | 5 | 5 | 4 | 3 | 2 | **3.95** |
| S3 | System.Linq.Expressions compilation to delegates | 5 | 3 | 2 | 5 | 3 | 2 | 3 | 2 | 3 | 3 | **3.45** |
| S4 | Reflection.Emit dynamic assemblies | 3 | 2 | 1 | 5 | 2 | 1 | 3 | 1 | 2 | 1 | **2.30** |
| S5 | Source-generated ahead-of-time compilation (built-in commands) | 2 | 4 | 5 | 5 | 2 | 5 | 5 | 5 | 3 | 3 | **3.60** |
| S6 | Hybrid: tree-walker plus bytecode tier for hot paths | 4 | 5 | 4 | 4 | 3 | 5 | 4 | 3 | 3 | 2 | **3.95** |

Justifications (one sentence per score, label in brackets):

**S0 PowerShell-faithful tiered pipeline (AST → expression trees → light interpreter → JIT)**
- Behavioral fidelity = 5 [FACT-SRC] It is the strategy PowerShell itself uses, so observable behavior is reproduced by construction (TIERING-POLICY, EQUIVALENCE-SPEC).
- Sandboxability = 3 [INFERENCE] Expression trees and call sites run arbitrary delegates; hooks exist at binders and runtime helpers but the JIT tier bypasses interpreter-level checks.
- Startup latency = 3 [FACT-SRC] The interpreter tier starts cheaply but the compiler front end builds trees for every block (COMPILATION-MAP).
- Steady-state throughput = 5 [FACT-SRC] Hot blocks and loops are JIT-compiled after 32 calls or 16 iterations (TIERING-POLICY).
- Debuggability = 4 [FACT-SRC] Sequence points and debugger hooks are emitted in both tiers (IR-SPEC §5).
- AOT-friendliness = 1 [EXTERNAL] Expression.Compile and Reflection.Emit need a JIT; under NativeAOT trees fall back to a slow interpreter.
- Determinism = 2 [FACT-SRC] Asynchronous promotion makes the executing tier nondeterministic (TIERING-POLICY §7.5).
- Memory footprint = 2 [FACT-SRC] Trees, instruction arrays, call sites and caches are retained per block.
- Observability = 4 [FACT-SRC] ETW compile events and script block logging exist (02.5 §14).
- Implementation simplicity = 1 [FACT-SRC] About 6,600 lines of compiler plus the interpreter, binders and DLR dependency.

**S1 AST tree-walking interpreter**
- Behavioral fidelity = 4 [INFERENCE] Every protocol of IR-SPEC §5 can be implemented once in the evaluator; no PowerShell-visible behavior requires a compiled form.
- Sandboxability = 5 [INFERENCE] All execution passes through one evaluator, so policy checks sit at every node visit and call.
- Startup latency = 5 [INFERENCE] No compile step: execution starts at the first node.
- Steady-state throughput = 2 [INFERENCE] Each node costs a virtual dispatch and allocations for values; no slot access without a resolver pass.
- Debuggability = 5 [INFERENCE] The evaluator is the debugger: breakpoints and stepping are plain hooks on statements.
- AOT-friendliness = 5 [EXTERNAL] Pure managed code without dynamic code generation runs under NativeAOT.
- Determinism = 5 [INFERENCE] Single tier: results never depend on promotion timing.
- Memory footprint = 4 [INFERENCE] Only the AST is retained; no trees or instruction arrays.
- Observability = 4 [INFERENCE] Trace of statements and calls is trivial to emit.
- Implementation simplicity = 5 [INFERENCE] Smallest implementation; the main work is the language rules, not an engine.

**S2 Custom bytecode VM**
- Behavioral fidelity = 4 [INFERENCE] A VM can implement the same protocols; the extra translation step adds risk of divergence from the AST semantics.
- Sandboxability = 5 [INFERENCE] A VM executes only its own instructions, so hooks go into the instruction loop.
- Startup latency = 4 [INFERENCE] A compile step to bytecode is cheap compared with trees but not free.
- Steady-state throughput = 3 [INFERENCE] A tight instruction loop beats tree-walking (PowerShell's own interpreter is of this kind, INSTRUCTION-SET).
- Debuggability = 3 [INFERENCE] Needs source maps from instructions to sequence points.
- AOT-friendliness = 5 [EXTERNAL] Managed bytecode interpreter has no AOT constraints.
- Determinism = 5 [INFERENCE] Single tier, deterministic.
- Memory footprint = 4 [INFERENCE] Instruction arrays and constant pools per block.
- Observability = 3 [INFERENCE] Instruction-level tracing is possible but noisy.
- Implementation simplicity = 2 [INFERENCE] A compiler, an instruction set and a frame model must be designed and tested.

**S3 System.Linq.Expressions compilation to delegates**
- Behavioral fidelity = 5 [FACT-SRC] PowerShell compiles to expression trees; behavior is reproduced via the same IR (COMPILATION-MAP).
- Sandboxability = 3 [INFERENCE] Compiled delegates run unchecked CLR code once produced; policy must be emitted into the trees.
- Startup latency = 2 [FACT-SRC] Tree building and Expression.Compile cost start-up time; PowerShell avoids it by interpreting first.
- Steady-state throughput = 5 [FACT-SRC] JIT-compiled delegates are the fast path of PowerShell hot code.
- Debuggability = 3 [INFERENCE] Debug info is possible (DebugInfo nodes) but stepping compiled code is harder.
- AOT-friendliness = 2 [EXTERNAL] Expression.Compile under NativeAOT degrades to an interpreter.
- Determinism = 3 [INFERENCE] Compile on demand with caching is deterministic if synchronous.
- Memory footprint = 2 [FACT-SRC] Delegates and trees are cached per block (CompiledScriptBlockData).
- Observability = 3 [INFERENCE] Compile events can be logged.
- Implementation simplicity = 3 [FACT-SRC] Needs the compiler, binders and caches but not the light interpreter.

**S4 Reflection.Emit dynamic assemblies**
- Behavioral fidelity = 3 [FACT-SRC] PowerShell uses Reflection.Emit only to define classes and enums (TypeDefiner), not for the dynamic language core.
- Sandboxability = 2 [INFERENCE] Emitted code calls the CLR directly; checks must be emitted explicitly.
- Startup latency = 1 [EXTERNAL] Emitting and loading assemblies costs the most start-up time of the options.
- Steady-state throughput = 5 [EXTERNAL] Emitted IL is JIT-compiled to native code.
- Debuggability = 2 [INFERENCE] Debugging emitted code needs symbol emission.
- AOT-friendliness = 1 [EXTERNAL] Reflection.Emit is unavailable under NativeAOT.
- Determinism = 3 [INFERENCE] Deterministic if emission is synchronous.
- Memory footprint = 1 [EXTERNAL] Dynamic assemblies stay loaded unless collectible (AssemblyLoadContext).
- Observability = 2 [INFERENCE] Emitted code is opaque to tracing.
- Implementation simplicity = 1 [INFERENCE] Emitting IL for dynamic scoping, pipelines and error-action semantics is the most complex option.

**S5 Source-generated ahead-of-time compilation (built-in commands)**
- Behavioral fidelity = 2 [INFERENCE] It cannot run user scripts; it only compiles the shell's own built-in commands.
- Sandboxability = 4 [INFERENCE] Generated code is reviewed at build time and calls only allowed APIs.
- Startup latency = 5 [EXTERNAL] AOT or R2R code needs no JIT at start-up.
- Steady-state throughput = 5 [EXTERNAL] Native code is the fastest.
- Debuggability = 2 [INFERENCE] Generated code is debuggable like normal C#.
- AOT-friendliness = 5 [EXTERNAL] Fully compatible with NativeAOT.
- Determinism = 5 [INFERENCE] Deterministic.
- Memory footprint = 5 [EXTERNAL] No runtime code generation memory.
- Observability = 3 [INFERENCE] Generated hooks can add tracing.
- Implementation simplicity = 3 [INFERENCE] A source generator is extra work but each command stays plain code.

**S6 Hybrid: tree-walker plus bytecode tier for hot paths**
- Behavioral fidelity = 4 [INFERENCE] Behavior is defined by the tree-walker; the bytecode tier must match it (EQUIVALENCE-SPEC applies).
- Sandboxability = 5 [INFERENCE] Both tiers are interpreters, so hooks are placed in two loops.
- Startup latency = 4 [INFERENCE] Starts as a tree-walker; bytecode is generated only for hot code.
- Steady-state throughput = 4 [INFERENCE] Hot paths run the bytecode loop.
- Debuggability = 3 [INFERENCE] Two tiers need two debug paths.
- AOT-friendliness = 5 [EXTERNAL] Managed code only; no JIT requirement.
- Determinism = 4 [INFERENCE] Deterministic if promotion is synchronous and count-based.
- Memory footprint = 3 [INFERENCE] AST plus bytecode for hot blocks.
- Observability = 3 [INFERENCE] Promotion events can be traced.
- Implementation simplicity = 2 [INFERENCE] Two engines and an equivalence test harness.

Hard gates (H1 reproduces `CORE` observable behavior; H2 feasible under the deployment constraint; H3 policy hooks possible at every boundary of [STAGE-CONTRACTS.md](STAGE-CONTRACTS.md)):

| Option | H1 | H2 JIT-allowed | H2 NativeAOT-required | H3 | Gate note |
|---|---|---|---|---|---|
| S0 | pass | pass | FAIL | pass | AOT: JIT tier and Expression.Compile unavailable (EXTERNAL) |
| S1 | pass | pass | pass | pass | Fidelity depends on implementing the protocols of IR-SPEC §5 and the equivalence obligations EQ-01..EQ-08 |
| S2 | pass | pass | pass | pass | Must reproduce flow-control and error-action protocols in the instruction set |
| S3 | pass | pass | FAIL | pass | AOT: Expression.Compile falls back to interpretation (EXTERNAL) |
| S4 | FAIL | pass | FAIL | FAIL | No evidence it can host the dynamic-scoping core (INFERENCE); emitted code bypasses evaluator hooks |
| S5 | FAIL | pass | pass | pass | Complement for built-in commands, not a strategy for user scripts |
| S6 | pass | pass | pass | pass | Build only after S1 is verified; triggers in INTERPRETER-DESIGN-SPACE §7 |

Recommendations (computed; label `INFERENCE`):

- **JIT-allowed**: S1 AST tree-walking interpreter (4.35); runner-up S2 Custom bytecode VM (3.95); candidates passing all gates: S1, S2, S6, S3, S0.
- **NativeAOT-required**: S1 AST tree-walking interpreter (4.35); runner-up S2 Custom bytecode VM (3.95); candidates passing all gates: S1, S2, S6.

Sensitivity (weight of one criterion raised, other weights scaled to keep the sum at 100; smallest weight at which the JIT-allowed winner changes):

- Behavioral fidelity (weight 25): winner becomes S3 at weight 61
- Sandboxability (weight 15): no change up to weight 70
- Startup latency (weight 10): no change up to weight 70
- Steady-state throughput (weight 10): winner becomes S6 at weight 26
- Debuggability (weight 10): no change up to weight 70
- AOT-friendliness (weight 10): no change up to weight 70
- Determinism (weight 5): no change up to weight 70
- Memory footprint (weight 5): no change up to weight 70
- Observability (weight 5): no change up to weight 70
- Implementation simplicity (weight 5): no change up to weight 70
<!--/GEN:scores-->

## 6. Reading the result

`INFERENCE`. The fidelity criterion rewards options whose behavior is defined by one evaluator: with the protocols of [IR-SPEC.md](IR-SPEC.md) §5 as the contract, `S1` can satisfy the equivalence obligations EQ-01 to EQ-08 trivially (single tier), which is why it passes H1 despite not copying PowerShell's architecture. Throughput is where `S1` loses; `S6` is the first step if measurements demand it. The recommendation is the same under both deployment constraints because the only options that fail the NativeAOT gate (`S0`, `S3`, `S4`) were already behind `S1` and `S6` on the weighted total. This is a property of the weights; the sensitivity list above shows which weight change flips the JIT-allowed winner.

## 7. Build order with triggers

1. **Phase A — `S1` tree-walker**, implementing the protocols of [IR-SPEC.md](IR-SPEC.md) §5 and the conformance corpus; verified against the oracle ([ORACLE-PROTOCOL.md](ORACLE-PROTOCOL.md)) before any optimizer exists. Trigger to leave Phase A: the benchmark set (tight loops of 1e6 iterations, function-call heavy recursion depth 1e4, pipeline of 1e5 objects) exceeds the owner's acceptable time (owner sets the numbers; suggested starting threshold: any benchmark above 5 s).
2. **Phase B — measured optimizations inside `S1`**: variable slots resolved by a pre-pass ([02.4-semantic-analysis.md](02.4-semantic-analysis.md) §7.2 simplified), cached operator dispatch, constant folding. Trigger to leave: benchmarks still above threshold after B, or a profile shows more than 50% of time in node dispatch.
3. **Phase C — `S6`**: bytecode tier for hot loops and functions with synchronous count-based promotion and a differential test harness (every corpus snippet run in both tiers, [EQUIVALENCE-SPEC.md](EQUIVALENCE-SPEC.md) §7.2).
4. **Phase D — `S5`** for built-in commands only if start-up of the built-in command set is the measured bottleneck.

## 8. Observable behavior [SPEC]

Not applicable (design document).

## 9. Error handling and edge cases

Hard-gate failures are reported per option in the gate table; ties go to the simpler option.

## 10. Concurrency and threading

Phase C promotion must be synchronous (determinism); no background compilation.

## 11. Extension points and customization hooks

The `Executable` contract of B4 in [STAGE-CONTRACTS.md](STAGE-CONTRACTS.md) lets Phase C replace the executable without touching the front end.

## 12. Dependencies

[STAGE-CONTRACTS.md](STAGE-CONTRACTS.md), [EQUIVALENCE-SPEC.md](EQUIVALENCE-SPEC.md), [TIERING-POLICY.md](TIERING-POLICY.md).

## 13. Performance notes

Scores for throughput and start-up are `INFERENCE` from structure, not measurements.

## 14. Security considerations (mandatory)

Single-evaluator strategies (`S1`, `S2`, `S6`) give one place for policy checks (gate H3); compiled strategies need checks emitted into generated code.

## 15. Enterprise considerations

Debuggability and observability criteria favor interpreters.

## 16. Tests

The first executable component is the oracle-diffed tree-walker.

## 17. Design decisions and trade-offs

| Decision | Label | Consequence |
|---|---|---|
| recommend `S1` first under both constraints | `INFERENCE` | least code, most debuggable; revisit with measurements |
| keep promotion synchronous and count-based | `INFERENCE` | determinism over peak performance |

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-DESIGN-01** [ADAPT] (area: NLD-RUN) Build `S1`, a tree-walking evaluator that implements the protocols of IR-SPEC §5, as the first and only engine until measurements justify another tier. Why: same observable behavior as PowerShell's compiled pipeline with a fraction of the machinery. Evidence: `src/System.Management.Automation/engine/parser/Compiler.cs::Compiler@L816-L6661`.
- **LSN-DESIGN-02** [REPLICATE] (area: NLD-RUN) If a second tier is added, test it differentially against the first on the whole corpus. Evidence: `src/System.Management.Automation/engine/interpreter/LightLambda.cs::LightLambda@L43-L303`.
- **LSN-DESIGN-03** [AVOID] (area: NLD-RUN) Do not adopt `Reflection.Emit` or `Expression.Compile` as the core engine. Evidence: `src/System.Management.Automation/engine/parser/PSType.cs::TypeDefiner@L18-L1505`. DEV: DEV-DESIGN-110

## 19. Open questions / UNVERIFIED

- Scores are structural estimates; no benchmark exists.
- The owner's performance thresholds are not set.

Verification: weights and scores live in `data/interpreter-scores.json`; totals, gates, recommendations and sensitivity are computed (`tools/gen_coord.py`); S0 facts are links to documents that cite source.
