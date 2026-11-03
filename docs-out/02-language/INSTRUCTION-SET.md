---
id: LANG-INSTR-001
title: Instruction set
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/interpreter/Instruction.cs, src/System.Management.Automation/engine/interpreter/InstructionList.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/interpreter/_folder.md]
generated_from: [data/instructions.json, data/types.json]
---

# Instruction set

> STATIC-ONLY — behavior not run-verified. The class list is `GENERATED` by `docs-out/tools/gen_T27.py` from `data/instructions.json` (`APPROX`: classes whose base chain reaches `Instruction`). Stack effects and semantics: [TIERING-POLICY.md](TIERING-POLICY.md) §6 and [EQUIVALENCE-SPEC.md](EQUIVALENCE-SPEC.md). Interpreter structure: [02.5-compiler-and-engine.md](02.5-compiler-and-engine.md) §7.

## 1. Purpose and scope [SPEC]

The interpreter (the "light compiler" in `engine/interpreter`) executes a flat array of `Instruction` objects over an object stack. This catalog lists the <!--N:INSTRUCTION_CLASSES-->183<!--/N--> instruction classes the scanner found (<!--N:INSTRUCTION_ABSTRACT-->17<!--/N--> abstract bases) in <!--N:INSTRUCTION_FILES-->22<!--/N--> files. Generic families that are expanded by arity (`DynamicInstruction<…>`, `ActionCallInstruction<…>`, `FuncCallInstruction<…>`) are listed once per file by the scanner and described in section 4.

## 2. Source map

| path | role |
|---|---|
| `src/System.Management.Automation/engine/interpreter/Instruction.cs` | abstract `Instruction` base, `IInstructionProvider`, `NotInstruction` |
| `src/System.Management.Automation/engine/interpreter/InstructionList.cs` | `InstructionList` emitter and `InstructionArray` |
| `src/System.Management.Automation/engine/interpreter/Interpreter.cs` | `Interpreter.Run` loop |

## 3. Instruction classes by file

### `AddInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `AddInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L20-L151` |
| `AddInstruction.AddInt32` | sealed | `AddInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L32-L42` |
| `AddInstruction.AddInt16` | sealed | `AddInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L44-L54` |
| `AddInstruction.AddInt64` | sealed | `AddInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L56-L66` |
| `AddInstruction.AddUInt16` | sealed | `AddInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L68-L78` |
| `AddInstruction.AddUInt32` | sealed | `AddInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L80-L90` |
| `AddInstruction.AddUInt64` | sealed | `AddInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L92-L102` |
| `AddInstruction.AddSingle` | sealed | `AddInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L104-L114` |
| `AddInstruction.AddDouble` | sealed | `AddInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L116-L126` |
| `AddOvfInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L153-L284` |
| `AddOvfInstruction.AddOvfInt32` | sealed | `AddOvfInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L165-L175` |
| `AddOvfInstruction.AddOvfInt16` | sealed | `AddOvfInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L177-L187` |
| `AddOvfInstruction.AddOvfInt64` | sealed | `AddOvfInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L189-L199` |
| `AddOvfInstruction.AddOvfUInt16` | sealed | `AddOvfInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L201-L211` |
| `AddOvfInstruction.AddOvfUInt32` | sealed | `AddOvfInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L213-L223` |
| `AddOvfInstruction.AddOvfUInt64` | sealed | `AddOvfInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L225-L235` |
| `AddOvfInstruction.AddOvfSingle` | sealed | `AddOvfInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L237-L247` |
| `AddOvfInstruction.AddOvfDouble` | sealed | `AddOvfInstruction` | `src/System.Management.Automation/engine/interpreter/AddInstruction.cs@L249-L259` |

### `ArrayOperations.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `NewArrayInitInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ArrayOperations.cs@L18-L42` |
| `NewArrayInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ArrayOperations.cs@L44-L58` |
| `NewArrayBoundsInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ArrayOperations.cs@L60-L87` |
| `GetArrayItemInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ArrayOperations.cs@L89-L109` |
| `SetArrayItemInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ArrayOperations.cs@L111-L132` |

### `CallInstruction.Generated.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `ActionCallInstruction` | sealed | `CallInstruction` | `src/System.Management.Automation/engine/interpreter/CallInstruction.Generated.cs@L432-L456` |
| `FuncCallInstruction` | sealed | `CallInstruction` | `src/System.Management.Automation/engine/interpreter/CallInstruction.Generated.cs@L692-L715` |
| `MethodInfoCallInstruction` | sealed | `CallInstruction` | `src/System.Management.Automation/engine/interpreter/CallInstruction.Generated.cs@L942-L954` |

### `CallInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `CallInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/CallInstruction.cs@L22-L264` |
| `MethodInfoCallInstruction` | sealed | `CallInstruction` | `src/System.Management.Automation/engine/interpreter/CallInstruction.cs@L266-L367` |

### `ControlFlowInstructions.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `OffsetInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L29-L64` |
| `BranchFalseInstruction` | sealed | `OffsetInstruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L66-L92` |
| `BranchTrueInstruction` | sealed | `OffsetInstruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L94-L120` |
| `CoalescingBranchInstruction` | sealed | `OffsetInstruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L122-L150` |
| `BranchInstruction` | concrete | `OffsetInstruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L152-L196` |
| `IndexedBranchInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L198-L227` |
| `GotoInstruction` | sealed | `IndexedBranchInstruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L250-L303` |
| `EnterTryCatchFinallyInstruction` | sealed | `IndexedBranchInstruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L305-L447` |
| `EnterFinallyInstruction` | sealed | `IndexedBranchInstruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L452-L489` |
| `LeaveFinallyInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L494-L514` |
| `EnterExceptionHandlerInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L517-L547` |
| `LeaveExceptionHandlerInstruction` | sealed | `IndexedBranchInstruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L552-L590` |
| `LeaveFaultInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L595-L627` |
| `ThrowInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L629-L669` |
| `SwitchInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L671-L690` |
| `EnterLoopInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L692-L778` |
| `CompiledLoopInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/ControlFlowInstructions.cs@L780-L794` |

### `DivInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `DivInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/DivInstruction.cs@L20-L151` |
| `DivInstruction.DivInt32` | sealed | `DivInstruction` | `src/System.Management.Automation/engine/interpreter/DivInstruction.cs@L32-L42` |
| `DivInstruction.DivInt16` | sealed | `DivInstruction` | `src/System.Management.Automation/engine/interpreter/DivInstruction.cs@L44-L54` |
| `DivInstruction.DivInt64` | sealed | `DivInstruction` | `src/System.Management.Automation/engine/interpreter/DivInstruction.cs@L56-L66` |
| `DivInstruction.DivUInt16` | sealed | `DivInstruction` | `src/System.Management.Automation/engine/interpreter/DivInstruction.cs@L68-L78` |
| `DivInstruction.DivUInt32` | sealed | `DivInstruction` | `src/System.Management.Automation/engine/interpreter/DivInstruction.cs@L80-L90` |
| `DivInstruction.DivUInt64` | sealed | `DivInstruction` | `src/System.Management.Automation/engine/interpreter/DivInstruction.cs@L92-L102` |
| `DivInstruction.DivSingle` | sealed | `DivInstruction` | `src/System.Management.Automation/engine/interpreter/DivInstruction.cs@L104-L114` |
| `DivInstruction.DivDouble` | sealed | `DivInstruction` | `src/System.Management.Automation/engine/interpreter/DivInstruction.cs@L116-L126` |

### `DynamicInstructionN.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `DynamicInstructionN` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/DynamicInstructionN.cs@L20-L77` |

### `DynamicInstructions.Generated.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `DynamicInstruction` | concrete | `Instruction` | `src/System.Management.Automation/engine/interpreter/DynamicInstructions.Generated.cs@L103-L127` |

### `DynamicSplatInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `DynamicSplatInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/DynamicSplatInstruction.cs@L23-L52` |

### `EqualInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `EqualInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L20-L189` |
| `EqualInstruction.EqualBoolean` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L33-L40` |
| `EqualInstruction.EqualSByte` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L42-L49` |
| `EqualInstruction.EqualInt16` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L51-L58` |
| `EqualInstruction.EqualChar` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L60-L67` |
| `EqualInstruction.EqualInt32` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L69-L76` |
| `EqualInstruction.EqualInt64` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L78-L85` |
| `EqualInstruction.EqualByte` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L87-L94` |
| `EqualInstruction.EqualUInt16` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L96-L103` |
| `EqualInstruction.EqualUInt32` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L105-L112` |
| `EqualInstruction.EqualUInt64` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L114-L121` |
| `EqualInstruction.EqualSingle` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L123-L130` |
| `EqualInstruction.EqualDouble` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L132-L139` |
| `EqualInstruction.EqualReference` | sealed | `EqualInstruction` | `src/System.Management.Automation/engine/interpreter/EqualInstruction.cs@L141-L148` |

### `FieldOperations.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `LoadStaticFieldInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/FieldOperations.cs@L21-L38` |
| `LoadFieldInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/FieldOperations.cs@L40-L59` |
| `StoreFieldInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/FieldOperations.cs@L61-L82` |
| `StoreStaticFieldInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/FieldOperations.cs@L84-L104` |

### `GreaterThanInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `GreaterThanInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L20-L168` |
| `GreaterThanInstruction.GreaterThanSByte` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L32-L40` |
| `GreaterThanInstruction.GreaterThanInt16` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L42-L50` |
| `GreaterThanInstruction.GreaterThanChar` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L52-L60` |
| `GreaterThanInstruction.GreaterThanInt32` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L62-L70` |
| `GreaterThanInstruction.GreaterThanInt64` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L72-L80` |
| `GreaterThanInstruction.GreaterThanByte` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L82-L90` |
| `GreaterThanInstruction.GreaterThanUInt16` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L92-L100` |
| `GreaterThanInstruction.GreaterThanUInt32` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L102-L110` |
| `GreaterThanInstruction.GreaterThanUInt64` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L112-L120` |
| `GreaterThanInstruction.GreaterThanSingle` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L122-L130` |
| `GreaterThanInstruction.GreaterThanDouble` | sealed | `GreaterThanInstruction` | `src/System.Management.Automation/engine/interpreter/GreaterThanInstruction.cs@L132-L140` |

### `Instruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `NotInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/Instruction.cs@L72-L87` |

### `LessThanInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `LessThanInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L20-L168` |
| `LessThanInstruction.LessThanSByte` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L32-L40` |
| `LessThanInstruction.LessThanInt16` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L42-L50` |
| `LessThanInstruction.LessThanChar` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L52-L60` |
| `LessThanInstruction.LessThanInt32` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L62-L70` |
| `LessThanInstruction.LessThanInt64` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L72-L80` |
| `LessThanInstruction.LessThanByte` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L82-L90` |
| `LessThanInstruction.LessThanUInt16` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L92-L100` |
| `LessThanInstruction.LessThanUInt32` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L102-L110` |
| `LessThanInstruction.LessThanUInt64` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L112-L120` |
| `LessThanInstruction.LessThanSingle` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L122-L130` |
| `LessThanInstruction.LessThanDouble` | sealed | `LessThanInstruction` | `src/System.Management.Automation/engine/interpreter/LessThanInstruction.cs@L132-L140` |

### `LocalAccess.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `LocalAccessInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L34-L49` |
| `LoadLocalInstruction` | sealed | `LocalAccessInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L53-L73` |
| `LoadLocalBoxedInstruction` | sealed | `LocalAccessInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L75-L90` |
| `LoadLocalFromClosureInstruction` | sealed | `LocalAccessInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L92-L107` |
| `LoadLocalFromClosureBoxedInstruction` | sealed | `LocalAccessInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L109-L124` |
| `AssignLocalInstruction` | sealed | `LocalAccessInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L130-L151` |
| `StoreLocalInstruction` | sealed | `LocalAccessInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L153-L173` |
| `AssignLocalBoxedInstruction` | sealed | `LocalAccessInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L175-L192` |
| `StoreLocalBoxedInstruction` | sealed | `LocalAccessInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L194-L211` |
| `AssignLocalToClosureInstruction` | sealed | `LocalAccessInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L213-L230` |
| `InitializeLocalInstruction` | abstract | `LocalAccessInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L237-L418` |
| `InitializeLocalInstruction.Reference` | sealed | `InitializeLocalInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L244-L266` |
| `InitializeLocalInstruction.ImmutableValue` | sealed | `InitializeLocalInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L268-L293` |
| `InitializeLocalInstruction.ImmutableBox` | sealed | `InitializeLocalInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L295-L316` |
| `InitializeLocalInstruction.ParameterBox` | sealed | `InitializeLocalInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L318-L330` |
| `InitializeLocalInstruction.Parameter` | sealed | `InitializeLocalInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L332-L359` |
| `InitializeLocalInstruction.MutableValue` | sealed | `InitializeLocalInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L361-L395` |
| `InitializeLocalInstruction.MutableBox` | sealed | `InitializeLocalInstruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L397-L417` |
| `RuntimeVariablesInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/LocalAccess.cs@L424-L453` |

### `MulInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `MulInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L20-L151` |
| `MulInstruction.MulInt32` | sealed | `MulInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L32-L42` |
| `MulInstruction.MulInt16` | sealed | `MulInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L44-L54` |
| `MulInstruction.MulInt64` | sealed | `MulInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L56-L66` |
| `MulInstruction.MulUInt16` | sealed | `MulInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L68-L78` |
| `MulInstruction.MulUInt32` | sealed | `MulInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L80-L90` |
| `MulInstruction.MulUInt64` | sealed | `MulInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L92-L102` |
| `MulInstruction.MulSingle` | sealed | `MulInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L104-L114` |
| `MulInstruction.MulDouble` | sealed | `MulInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L116-L126` |
| `MulOvfInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L153-L284` |
| `MulOvfInstruction.MulOvfInt32` | sealed | `MulOvfInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L165-L175` |
| `MulOvfInstruction.MulOvfInt16` | sealed | `MulOvfInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L177-L187` |
| `MulOvfInstruction.MulOvfInt64` | sealed | `MulOvfInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L189-L199` |
| `MulOvfInstruction.MulOvfUInt16` | sealed | `MulOvfInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L201-L211` |
| `MulOvfInstruction.MulOvfUInt32` | sealed | `MulOvfInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L213-L223` |
| `MulOvfInstruction.MulOvfUInt64` | sealed | `MulOvfInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L225-L235` |
| `MulOvfInstruction.MulOvfSingle` | sealed | `MulOvfInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L237-L247` |
| `MulOvfInstruction.MulOvfDouble` | sealed | `MulOvfInstruction` | `src/System.Management.Automation/engine/interpreter/MulInstruction.cs@L249-L259` |

### `NotEqualInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `NotEqualInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L20-L189` |
| `NotEqualInstruction.NotEqualBoolean` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L33-L40` |
| `NotEqualInstruction.NotEqualSByte` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L42-L49` |
| `NotEqualInstruction.NotEqualInt16` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L51-L58` |
| `NotEqualInstruction.NotEqualChar` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L60-L67` |
| `NotEqualInstruction.NotEqualInt32` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L69-L76` |
| `NotEqualInstruction.NotEqualInt64` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L78-L85` |
| `NotEqualInstruction.NotEqualByte` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L87-L94` |
| `NotEqualInstruction.NotEqualUInt16` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L96-L103` |
| `NotEqualInstruction.NotEqualUInt32` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L105-L112` |
| `NotEqualInstruction.NotEqualUInt64` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L114-L121` |
| `NotEqualInstruction.NotEqualSingle` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L123-L130` |
| `NotEqualInstruction.NotEqualDouble` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L132-L139` |
| `NotEqualInstruction.NotEqualReference` | sealed | `NotEqualInstruction` | `src/System.Management.Automation/engine/interpreter/NotEqualInstruction.cs@L141-L148` |

### `NumericConvertInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `NumericConvertInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/NumericConvertInstruction.cs@L18-L284` |
| `NumericConvertInstruction.Unchecked` | sealed | `NumericConvertInstruction` | `src/System.Management.Automation/engine/interpreter/NumericConvertInstruction.cs@L38-L159` |
| `NumericConvertInstruction.Checked` | sealed | `NumericConvertInstruction` | `src/System.Management.Automation/engine/interpreter/NumericConvertInstruction.cs@L162-L283` |

### `PowerShellInstructions.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `UpdatePositionInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/PowerShellInstructions.cs@L18-L50` |

### `StackOperations.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `LoadObjectInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/StackOperations.cs@L21-L42` |
| `LoadCachedObjectInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/StackOperations.cs@L44-L70` |
| `PopInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/StackOperations.cs@L72-L90` |
| `DupInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/StackOperations.cs@L92-L112` |

### `SubInstruction.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `SubInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L20-L151` |
| `SubInstruction.SubInt32` | sealed | `SubInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L32-L42` |
| `SubInstruction.SubInt16` | sealed | `SubInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L44-L54` |
| `SubInstruction.SubInt64` | sealed | `SubInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L56-L66` |
| `SubInstruction.SubUInt16` | sealed | `SubInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L68-L78` |
| `SubInstruction.SubUInt32` | sealed | `SubInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L80-L90` |
| `SubInstruction.SubUInt64` | sealed | `SubInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L92-L102` |
| `SubInstruction.SubSingle` | sealed | `SubInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L104-L114` |
| `SubInstruction.SubDouble` | sealed | `SubInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L116-L126` |
| `SubOvfInstruction` | abstract | `Instruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L153-L284` |
| `SubOvfInstruction.SubOvfInt32` | sealed | `SubOvfInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L165-L175` |
| `SubOvfInstruction.SubOvfInt16` | sealed | `SubOvfInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L177-L187` |
| `SubOvfInstruction.SubOvfInt64` | sealed | `SubOvfInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L189-L199` |
| `SubOvfInstruction.SubOvfUInt16` | sealed | `SubOvfInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L201-L211` |
| `SubOvfInstruction.SubOvfUInt32` | sealed | `SubOvfInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L213-L223` |
| `SubOvfInstruction.SubOvfUInt64` | sealed | `SubOvfInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L225-L235` |
| `SubOvfInstruction.SubOvfSingle` | sealed | `SubOvfInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L237-L247` |
| `SubOvfInstruction.SubOvfDouble` | sealed | `SubOvfInstruction` | `src/System.Management.Automation/engine/interpreter/SubInstruction.cs@L249-L259` |

### `TypeOperations.cs`

| Class | Kind | Base | Source |
|---|---|---|---|
| `CreateDelegateInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/TypeOperations.cs@L21-L55` |
| `NewInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/TypeOperations.cs@L57-L99` |
| `DefaultValueInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/TypeOperations.cs@L101-L119` |
| `TypeIsInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/TypeOperations.cs@L121-L140` |
| `TypeAsInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/TypeOperations.cs@L142-L170` |
| `TypeEqualsInstruction` | sealed | `Instruction` | `src/System.Management.Automation/engine/interpreter/TypeOperations.cs@L172-L196` |

## 4. Generated families (not enumerated by the scanner)

| Family | Members | Evidence |
|---|---|---|
| `DynamicInstruction<…>` | 16 generic classes, 0..15 call arguments (`DynamicInstruction<TRet>` … `<T0..T14,TRet>`) | `src/System.Management.Automation/engine/interpreter/DynamicInstructions.Generated.cs` (notes W1-W2) |
| `ActionCallInstruction<…>` | 10 classes, 0..9 arguments | `src/System.Management.Automation/engine/interpreter/CallInstruction.Generated.cs` |
| `FuncCallInstruction<…>` | 10 classes, 0..9 arguments | same file |
| `GetArrayItemInstruction<T>`, `SetArrayItemInstruction<T>`, `TypeIsInstruction<T>`, `TypeAsInstruction<T>`, `DefaultValueInstruction<T>`, `NewArrayInstruction<T>`, `NewArrayInitInstruction<T>` | created per element type on demand by `InstructionFactory` (15 pre-seeded types) | `src/System.Management.Automation/engine/interpreter/InstructionFactory.cs` |

Counts for these families come from the generated-file notes (`FACT-SRC`), not from `data/instructions.json`.

Verification: instruction class list reconciles with `data/instructions.json` (count above); abstract/sealed taken from the class modifiers; family sizes from the three generated source files read in full (notes `.work/notes/src_System.Management.Automation_engine_interpreter_*`).

