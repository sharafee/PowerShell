# LocalAccess.cs (456) fully read, 2 windows
- IBoxableInstruction L28 (BoxIfIndexMatches). LocalAccessInstruction abstract L34 (_index).
- Load: LoadLocal (produce 1; push Data[idx]), LoadLocalBoxed (StrongBox<object>.Value), LoadLocalFromClosure (frame.Closure[idx].Value), LoadLocalFromClosureBoxed (pushes the box itself).
- Store/Assign: AssignLocal (peek -> Data[idx], keeps value), StoreLocal (pop), AssignLocalBoxed, StoreLocalBoxed, AssignLocalToClosure (peek->Closure[idx].Value).
- Initialize (abstract InitializeLocalInstruction L237 with nested classes): Reference ("InitRef" -> null), ImmutableValue ("InitImmutableValue"), ImmutableBox ("InitImmutableBox": new StrongBox), ParameterBox (wrap param in box), Parameter ("InitParameter": nop), MutableValue ("InitMutableValue": Activator.CreateInstance(type); TargetInvocationException unwrapped), MutableBox ("InitMutableBox").
- RuntimeVariablesInstruction L424: consumes _count boxes (IStrongBox), pushes RuntimeVariables.Create(ret).
