# LightLambda.cs (303) fully read
- L33 LightLambdaCompileEventArgs. L43 LightLambda partial: fields _closure, _interpreter, s_runCache CacheDict<Type,Func<LightLambda,Delegate>>(100) L47, _delegateCreator, _compiled, _compilationThreshold (per instance, mutable int). Event Compile.
- L67-158 GetRunDelegateCtor/MakeRunDelegateCtor: picks RunN/RunVoidN by Invoke signature; MaxParameters (16, in .Generated) -> null => CreateCustomDelegate (L161: builds Expression lambda calling Run(object[]) and lambda.Compile()); by-ref params => null (custom); special RunVoidRef2 for (ref,ref) void; DynamicMethod FastCtor via IL (ldftn+newobj).
- L184 MakeDelegate(type).
- **L197-246 TryGetCompiled**: if _delegateCreator.HasCompiled => _compiled = CreateCompiledDelegate(_closure); raise Compile event if SameDelegateType; return true. Else **`if (unchecked(_compilationThreshold--) == 0)`** -> if _interpreter.CompileSynchronously => _delegateCreator.Compile(null) then TryGetCompiled(); else **ThreadPool.QueueUserWorkItem(_delegateCreator.Compile, null)** (background). Comment: racing threads OK; no lock on hot path.
  => count semantics: counter starts at T; call k reads T-k+1; compile triggered when read==0 i.e. on call T+1 (33rd call for T=32); that call still interpreted (async). For T<=1 sync: threshold 0: first call (reads 0) compiles synchronously; threshold 1: second call.
  Hmm threshold==1: call1 reads 1 no; call2 reads 0 -> sync compile. threshold 0 call1 reads 0.
- L277 Run(params object[]): generic path (used by custom delegates): `_compiled.DynamicInvoke(arguments)`; else MakeFrame, copy args to frame.Data, Enter/Leave, return frame.Pop().
- L253 RunVoidRef2 copy-in/copy-out; compiled path commented out.
