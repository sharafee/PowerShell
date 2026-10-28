# LightDelegateCreator.cs (220) fully read in 1 window
- L30 class; fields _interpreter (null if forced compile), _lambda, _compiledDelegateType, _compiled, _compileLock.
- L78-112 CreateDelegate(closure): if _compiled != null and SameDelegateType -> return compiled delegate directly; if _interpreter==null => Compile(null) synchronously then CreateCompiledDelegate; else new LightLambda(this, closure, _interpreter._compilationThreshold).MakeDelegate(DelegateType).
- L132 CreateCompiledDelegate(closure): if HasClosure, _compiled is Func<StrongBox<object>[],Delegate> applied to closure.
- L151-188 Compile(state): lock(_compileLock), once; if interpreter!=null: change lambda delegate type to Func/Action (GetFuncOrAction L190); HasClosure => LightLambdaClosureVisitor.BindLambda(lambda, ClosureVariables) else lambda.Compile() (IL JIT via System.Linq.Expressions).
