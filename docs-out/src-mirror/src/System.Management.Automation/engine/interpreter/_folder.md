# src/System.Management.Automation/engine/interpreter

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| A:38 | System.Management.Automation | 38 | 13810 | 271 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `AddInstruction.cs` | 285 | `AddInstruction`, `AddOvfInstruction` |  |  |
| `ArrayOperations.cs` | 133 | `NewArrayBoundsInstruction`, `NewArrayInitInstruction<TElement>`, `SetArrayItemInstruction<TElement>`, `GetArrayItemInstruction<TElement>` (+1) |  |  |
| `BranchLabel.cs` | 129 | `BranchLabel`, `RuntimeLabel` |  |  |
| `CallInstruction.Generated.cs` | 959 | `CallInstruction`, `ActionCallInstruction`, `ActionCallInstruction<T0>`, `ActionCallInstruction<T0,T1>` (+18) |  |  |
| `CallInstruction.cs` | 368 | `CallInstruction`, `MethodInfoCallInstruction` |  |  |
| `ControlFlowInstructions.cs` | 795 | `EnterTryCatchFinallyInstruction`, `EnterLoopInstruction`, `GotoInstruction`, `BranchInstruction` (+13) |  |  |
| `DivInstruction.cs` | 152 | `DivInstruction` |  |  |
| `DynamicInstructionN.cs` | 78 | `DynamicInstructionN` |  |  |
| `DynamicInstructions.Generated.cs` | 522 | `DynamicInstructionN`, `DynamicInstruction<TRet>`, `DynamicInstruction<T0,T1,TRet>`, `DynamicInstruction<T0,T1,T2,TRet>` (+13) |  |  |
| `DynamicSplatInstruction.cs` | 53 | `DynamicSplatInstruction` |  |  |
| `EqualInstruction.cs` | 190 | `EqualInstruction` |  |  |
| `FieldOperations.cs` | 105 | `StoreFieldInstruction`, `StoreStaticFieldInstruction`, `LoadFieldInstruction`, `LoadStaticFieldInstruction` |  |  |
| `GreaterThanInstruction.cs` | 169 | `GreaterThanInstruction` |  |  |
| `ILightCallSiteBinder.cs` | 28 | `ILightCallSiteBinder` |  |  |
| `Instruction.cs` | 88 | `Instruction`, `NotInstruction`, `IInstructionProvider` |  |  |
| `InstructionFactory.cs` | 130 | `InstructionFactory<T>`, `InstructionFactory` |  |  |
| `InstructionList.cs` | 1221 | `InstructionList`, `InstructionArray` |  |  |
| `InterpretedFrame.cs` | 333 | `InterpretedFrame` |  |  |
| `Interpreter.cs` | 110 | `Interpreter` |  |  |
| `LabelInfo.cs` | 364 | `LabelInfo`, `LabelScopeInfo`, `LabelScopeKind` |  |  |
| `LessThanInstruction.cs` | 169 | `LessThanInstruction` |  |  |
| `LightCompiler.cs` | 2052 | `LightCompiler`, `ExceptionHandler`, `TryCatchFinallyHandler`, `DebugInfo` (+2) |  |  |
| `LightDelegateCreator.cs` | 220 | `LightDelegateCreator` |  |  |
| `LightLambda.Generated.cs` | 769 | `LightLambda` |  |  |
| `LightLambda.cs` | 303 | `LightLambda`, `LightLambdaCompileEventArgs` |  |  |
| `LightLambdaClosureVisitor.cs` | 304 | `LightLambdaClosureVisitor` |  |  |
| `LocalAccess.cs` | 456 | `InitializeLocalInstruction`, `RuntimeVariablesInstruction`, `AssignLocalInstruction`, `LoadLocalInstruction` (+9) |  |  |
| `LocalVariables.cs` | 322 | `LocalVariables`, `LocalDefinition`, `LocalVariable` |  |  |
| `LoopCompiler.cs` | 385 | `LoopCompiler` |  |  |
| `MulInstruction.cs` | 285 | `MulInstruction`, `MulOvfInstruction` |  |  |
| `NotEqualInstruction.cs` | 190 | `NotEqualInstruction` |  |  |
| `NumericConvertInstruction.cs` | 285 | `NumericConvertInstruction` |  |  |
| `PowerShellInstructions.cs` | 51 | `UpdatePositionInstruction` |  |  |
| `RuntimeVariables.cs` | 55 | `RuntimeVariables` |  |  |
| `StackOperations.cs` | 113 | `LoadCachedObjectInstruction`, `LoadObjectInstruction`, `DupInstruction`, `PopInstruction` |  |  |
| `SubInstruction.cs` | 285 | `SubInstruction`, `SubOvfInstruction` |  |  |
| `TypeOperations.cs` | 197 | `NewInstruction`, `CreateDelegateInstruction`, `TypeAsInstruction<T>`, `TypeEqualsInstruction` (+2) |  |  |
| `Utilities.cs` | 1157 | `ThreadLocal<T>`, `HybridReferenceDictionary<TKey,TValue>`, `Utils`, `CacheDict<TKey,TValue>` (+10) |  |  |

## Partial-class and conditional-compilation notes

Partial types spanning files: `CallInstruction`, `DynamicInstructionN`, `LightLambda`, `MethodInfoCallInstruction`

No conditionally-compiled types (APPROX).

## Related documents

_none linked yet_
