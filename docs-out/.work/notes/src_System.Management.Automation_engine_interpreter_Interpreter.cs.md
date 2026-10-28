# Interpreter.cs (110) fully read
- L31 class Interpreter: forth-style stack machine (doc L22-30). NoValue sentinel L33; RethrowOnReturn = Int32.MaxValue L35. L37-39 comment: "zero: sync compilation; negative: default" for _compilationThreshold.
- L47 ctor(name, locals, labelMapping, InstructionArray, debugInfos, compilationThreshold).
- L78-81 `CompileSynchronously => _compilationThreshold <= 1`.
- L98-108 Run(InterpretedFrame): `while (index < instructions.Length) { index += instructions[index].Run(frame); frame.InstructionIndex = index; }` (NoInlining + SpecialName).
