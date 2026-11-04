---
id: LANG-TESTCORPUS-001
title: Reference test corpus
kind: catalog
tier: B
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [test/powershell/Language]
mirror_cards: []
generated_from: [data/tests.json]
---

# Reference test corpus

> STATIC-ONLY — the repository's own tests are the interim behavior evidence (no golden samples). Tables are `GENERATED` by `docs-out/tools/gen_coord.py` from `data/tests.json` (`APPROX`: Pester `Describe`/`Context`/`It` counted by regex; xUnit `[Fact]`/`[Theory]` by regex). Test files were **inventoried, not read**: they are the model for the new product's specification-test suite and the source of the "covering tests" column of the feature matrix.

## 1. Purpose and scope [SPEC]

Existing parser and language tests under `test/` that specify language behavior, grouped by feature folder with paths and counts. The Language Pester folders contain <!--N:LANGUAGE_TEST_FILES-->81<!--/N--> files and <!--N:LANGUAGE_TEST_ITS-->1249<!--/N--> `It` blocks.

## 2. Source map

`test/powershell/Language/{Parser,Operators,Scripting,Classes,Interop}`, selected `test/powershell/engine/**`, `test/xUnit/csharp/test_Binders.cs`, `test_AstDefaultVisit.cs`.

## 3. Responsibilities and non-responsibilities

Inventory only; assertions are not reproduced (clean-room: describe, do not copy).

## 4. Key types and contracts [IMPL]

Pester 5 structure: `Describe` → `Context` → `It`; tags select CI priority. xUnit tests exercise internal APIs (binders, AST visitors).

## 5. Data model — inventory

<!--GEN:tests-->
| Folder | Files | Describe | Context | It |
|---|---:|---:|---:|---:|
| `test/powershell/Language/Classes` | 10 | 42 | 26 | 158 |
| `test/powershell/Language/Interop` | 2 | 2 | 1 | 28 |
| `test/powershell/Language/Operators` | 7 | 10 | 16 | 130 |
| `test/powershell/Language/Parser` | 15 | 72 | 20 | 247 |
| `test/powershell/Language/Scripting` | 47 | 82 | 124 | 686 |
| **total Language** | **81** | **208** | **187** | **1249** |

Files (path, Describe/Context/It counts, first Describe names; `APPROX` regex extraction):

| File | D | C | It | First Describe names |
|---|---:|---:|---:|---|
| `test/powershell/Language/Classes/ProtectedAccess.Tests.ps1` | 3 | 0 | 35 | Protected Member Access - w/ default ctor; Protected Member Access - w/ non-default ctor |
| `test/powershell/Language/Classes/Scripting.Classes.Attributes.Tests.ps1` | 3 | 11 | 24 | Attributes Test; Type resolution with attributes |
| `test/powershell/Language/Classes/Scripting.Classes.BasicParsing.Tests.ps1` | 25 | 3 | 61 | Positive Parse Properties Tests; Negative Parsing Tests |
| `test/powershell/Language/Classes/Scripting.Classes.Break.Tests.ps1` | 1 | 4 | 7 | Break statements with classes |
| `test/powershell/Language/Classes/Scripting.Classes.Exceptions.Tests.ps1` | 3 | 3 | 14 | Exceptions flow for classes; Exception error position |
| `test/powershell/Language/Classes/Scripting.Classes.MiscOps.Tests.ps1` | 1 | 3 | 6 | Misc Test |
| `test/powershell/Language/Classes/Scripting.Classes.Modules.Tests.ps1` | 3 | 0 | 4 | PSModuleInfo.GetExportedTypeDefinitions(); use of a module from two runspaces |
| `test/powershell/Language/Classes/Scripting.Classes.NoRunspaceAffinity.Tests.ps1` | 1 | 0 | 1 | Class can be defined without Runspace affinity |
| `test/powershell/Language/Classes/Scripting.Classes.RunPath.Tests.ps1` | 1 | 0 | 1 | Script with a class definition run path |
| `test/powershell/Language/Classes/Scripting.Classes.StaticMethod.Tests.ps1` | 1 | 2 | 5 | Additional static method tests |
| `test/powershell/Language/Interop/DotNet/DotNetAPI.Tests.ps1` | 1 | 0 | 5 | DotNetAPI |
| `test/powershell/Language/Interop/DotNet/DotNetInterop.Tests.ps1` | 1 | 1 | 23 | Handle ByRef-like types gracefully |
| `test/powershell/Language/Operators/ComparisonOperator.Tests.ps1` | 2 | 0 | 13 | ComparisonOperator; Bytewise Operator |
| `test/powershell/Language/Operators/NullConditional.Tests.ps1` | 2 | 6 | 52 | NullCoalesceOperations; NullConditionalMemberAccess |
| `test/powershell/Language/Operators/PipelineChainOperator.Tests.ps1` | 1 | 2 | 7 | Experimental Feature: && and \|\| operators - Feature-Enable |
| `test/powershell/Language/Operators/RangeOperator.Tests.ps1` | 1 | 3 | 17 | Range Operator |
| `test/powershell/Language/Operators/ReplaceOperator.Tests.ps1` | 2 | 2 | 12 | Replace Operator; Culture-invariance tests for -split and -replace |
| `test/powershell/Language/Operators/SplitOperator.Tests.ps1` | 1 | 3 | 22 | Split Operator |
| `test/powershell/Language/Operators/TernaryOperator.Tests.ps1` | 1 | 0 | 7 | Using of ternary operator |
| `test/powershell/Language/Parser/Ast.Tests.ps1` | 1 | 0 | 4 | The SafeGetValue method on AST returns safe values |
| `test/powershell/Language/Parser/AutomaticVariables.Tests.ps1` | 1 | 0 | 2 | Automatic variable $input |
| `test/powershell/Language/Parser/BNotOperator.Tests.ps1` | 2 | 0 | 12 | bnot on enums; bnot on integral types |
| `test/powershell/Language/Parser/Conversions.Tests.ps1` | 5 | 1 | 24 | conversion syntax; Type resolution should prefer assemblies in powershell assem |
| `test/powershell/Language/Parser/ExtensibleCompletion.Tests.ps1` | 10 | 0 | 3 | Factory based extensible completion; Script block based extensible completion |
| `test/powershell/Language/Parser/LanguageAndParser.TestFollowup.Tests.ps1` | 12 | 0 | 23 | Clone array; Set fields through PSMemberInfo |
| `test/powershell/Language/Parser/LineContinuance.Tests.ps1` | 1 | 6 | 28 | Line Continuance |
| `test/powershell/Language/Parser/MethodInvocation.Tests.ps1` | 2 | 0 | 12 | Generic Method invocation; Interface inheritance with remoting proxies |
| `test/powershell/Language/Parser/ParameterBinding.Tests.ps1` | 3 | 0 | 14 | Argument transformation attribute on optional argument with ; Custom type conversion in parameter binding |
| `test/powershell/Language/Parser/Parser.Tests.ps1` | 1 | 9 | 85 | ParserTests (admin\monad\tests\monad\src\engine\core\ParserT |
| `test/powershell/Language/Parser/Parsing.Tests.ps1` | 27 | 0 | 14 | for statement parsing; foreach statement parsing |
| `test/powershell/Language/Parser/RedirectionOperator.Tests.ps1` | 4 | 1 | 7 | Redirection operator now supports encoding changes; File redirection mixed with Out-Null |
| `test/powershell/Language/Parser/TypeAccelerator.Tests.ps1` | 1 | 2 | 5 | Type accelerators |
| `test/powershell/Language/Parser/UsingAssembly.Tests.ps1` | 1 | 1 | 8 | Using assembly |
| `test/powershell/Language/Parser/UsingNamespace.Tests.ps1` | 1 | 0 | 6 | Using Namespace |
| `test/powershell/Language/Scripting/ActionPreference.Tests.ps1` | 2 | 7 | 36 | Tests for (error, warning, etc) action preference; ActionPreference.Break tests |
| `test/powershell/Language/Scripting/Adapter.Tests.ps1` | 2 | 0 | 5 | Interface static members; ByRef property |
| `test/powershell/Language/Scripting/Array.Tests.ps1` | 2 | 0 | 15 | ArrayExpression Tests; ArrayLiteral Tests |
| `test/powershell/Language/Scripting/CheckRestrictedlanguage.Tests.ps1` | 1 | 0 | 12 | Test restricted language check method on scriptblocks |
| `test/powershell/Language/Scripting/CleanBlockErrorHandling.Tests.ps1` | 3 | 0 | 49 | Error handling within a single 'Clean' block; Multiple errors from 'Clean' and another named block |
| `test/powershell/Language/Scripting/CmdletDeclaration.Tests.ps1` | 1 | 0 | 1 | Cmdlet declaration statement |
| `test/powershell/Language/Scripting/CommandErrorHandling.Tests.ps1` | 1 | 3 | 22 | Command error handling in general |
| `test/powershell/Language/Scripting/CommonParameters.Tests.ps1` | 1 | 10 | 22 | Common parameters support for script cmdlets |
| `test/powershell/Language/Scripting/ConstrainedLanguageMode.Tests.ps1` | 1 | 0 | 1 | Test constrained language mode |
| `test/powershell/Language/Scripting/Debugging/DebuggerCommand.Tests.ps1` | 3 | 9 | 51 | Basic debugger command tests; Simple debugger stepping command tests |
| `test/powershell/Language/Scripting/Debugging/DebuggerScriptTests.Tests.ps1` | 9 | 1 | 22 | Breakpoints set on custom FileSystem provider files should w; Tests line breakpoints on dot-sourced files |
| `test/powershell/Language/Scripting/Debugging/Debugging.Tests.ps1` | 3 | 9 | 19 | Basic debugger tests; Breakpoints when set should be hit |
| `test/powershell/Language/Scripting/Debugging/DebuggingInHost.Tests.ps1` | 1 | 0 | 4 | Tests Debugger GetCallStack() on runspaces when attached to  |
| `test/powershell/Language/Scripting/Delegates.Tests.ps1` | 1 | 0 | 8 | Test for conversion b/w script block and delegate |
| `test/powershell/Language/Scripting/DeserializedMethods.Tests.ps1` | 1 | 0 | 1 | DeserializedMethods |
| `test/powershell/Language/Scripting/DeserializedTypeConversion.Tests.ps1` | 1 | 6 | 12 | Tests conversion of deserialized types to original type usin |
| `test/powershell/Language/Scripting/DollarHook.Tests.ps1` | 1 | 1 | 4 | Tests for setting $? for execution success |
| `test/powershell/Language/Scripting/Dynamicparameters.Tests.ps1` | 1 | 0 | 5 | Dynamic parameter support in script cmdlets. |
| `test/powershell/Language/Scripting/ErrorHistoryId.Tests.ps1` | 1 | 0 | 3 | Error HistoryId Tests |
| `test/powershell/Language/Scripting/ErrorPosition.Tests.ps1` | 1 | 0 | 2 | Error position Tests |
| `test/powershell/Language/Scripting/ForeachParallel.Tests.ps1` | 1 | 5 | 10 | Parallel foreach syntax |
| `test/powershell/Language/Scripting/Generics.Tests.ps1` | 1 | 0 | 10 | Generics support |
| `test/powershell/Language/Scripting/HashtableToPSCustomObjectConversion.Tests.ps1` | 2 | 0 | 11 | Tests for hashtable to PSCustomObject conversion; Error message with settable Property information |
| `test/powershell/Language/Scripting/I18n/I18n.Tests.ps1` | 1 | 6 | 16 | Testing of script internationalization |
| `test/powershell/Language/Scripting/Indexer.Tests.ps1` | 1 | 0 | 7 | Tests for indexers |
| `test/powershell/Language/Scripting/LineEndings.Tests.ps1` | 1 | 0 | 2 | Line endings |
| `test/powershell/Language/Scripting/MyInvocation.Tests.ps1` | 1 | 2 | 8 | Testing of MyInvocation |
| `test/powershell/Language/Scripting/NativeExecution/NativeCommandArguments.Tests.ps1` | 5 | 0 | 15 | Behavior is specific for each platform; tests for multiple languages and extensions |
| `test/powershell/Language/Scripting/NativeExecution/NativeCommandPathUpdate.Tests.ps1` | 1 | 2 | 9 | Path update for package managers |
| `test/powershell/Language/Scripting/NativeExecution/NativeCommandProcessor.Tests.ps1` | 6 | 0 | 15 | Native pipeline should have proper encoding; native commands with pipeline |
| `test/powershell/Language/Scripting/NativeExecution/NativeLinuxCommands.Tests.ps1` | 2 | 0 | 8 | NativeLinuxCommands; Scripts with extensions |
| `test/powershell/Language/Scripting/NativeExecution/NativeStreams.Tests.ps1` | 2 | 1 | 6 | Native streams behavior with PowerShell; piping powershell objects to finished native executable |
| `test/powershell/Language/Scripting/NativeExecution/NativeUnixGlobbing.Tests.ps1` | 1 | 0 | 17 | Native UNIX globbing tests |
| `test/powershell/Language/Scripting/NativeExecution/NativeWindowsTildeExpansion.Tests.ps1` | 1 | 0 | 3 | Native Windows tilde expansion tests |
| `test/powershell/Language/Scripting/OrderedAttributeForHashTables.Tests.ps1` | 1 | 3 | 4 | Test for cmdlet to support Ordered Attribute on hash literal |
| `test/powershell/Language/Scripting/OutErrorVariable.Tests.ps1` | 3 | 1 | 15 | Tests OutVariable only; Test ErrorVariable only |
| `test/powershell/Language/Scripting/PSSerializer.Tests.ps1` | 1 | 0 | 3 | Tests for lossless rehydration of serialized types. |
| `test/powershell/Language/Scripting/ParameterBinding.Tests.ps1` | 1 | 2 | 40 | Tests for parameter binding |
| `test/powershell/Language/Scripting/PipelineBehaviour.Tests.ps1` | 2 | 5 | 29 | Function Pipeline Behaviour; Other Pipeline Behaviour |
| `test/powershell/Language/Scripting/PipelineStoppedToken.Tests.ps1` | 1 | 0 | 2 | PipelineStopToken tests |
| `test/powershell/Language/Scripting/Requires.Tests.ps1` | 2 | 7 | 8 | Requires tests; #requires -Modules |
| `test/powershell/Language/Scripting/ScriptHelp.Tests.ps1` | 3 | 28 | 92 | get-help HelpFunc1; get-help file |
| `test/powershell/Language/Scripting/Scripting.Followup.Tests.ps1` | 1 | 0 | 10 | Scripting.Followup.Tests |
| `test/powershell/Language/Scripting/SuppressAnsiEscapeSequence.Tests.ps1` | 1 | 2 | 6 | $env:__SuppressAnsiEscapeSequences tests |
| `test/powershell/Language/Scripting/SwitchParallel.Tests.ps1` | 1 | 3 | 5 | Parallel switch syntax |
| `test/powershell/Language/Scripting/Trap.Tests.ps1` | 1 | 1 | 4 | Test trap |
| `test/powershell/Language/Scripting/TryCatch.Tests.ps1` | 1 | 10 | 37 | Test try/catch |

Engine tests that also specify language behavior (selected by path keywords, `APPROX`):

| File | It |
|---|---:|
| `test/powershell/engine/Api/BasicEngine.Tests.ps1` | 9 |
| `test/powershell/engine/Api/GetMethodInfoOverloadDefinition.Tests.ps1` | 11 |
| `test/powershell/engine/Api/GetNewClosure.Tests.ps1` | 2 |
| `test/powershell/engine/Api/InitialSessionState.Tests.ps1` | 8 |
| `test/powershell/engine/Api/LanguagePrimitive.Tests.ps1` | 23 |
| `test/powershell/engine/Api/PSCommand.Tests.ps1` | 4 |
| `test/powershell/engine/Api/ProxyCommand.Tests.ps1` | 3 |
| `test/powershell/engine/Api/Serialization.Tests.ps1` | 7 |
| `test/powershell/engine/Api/SuspiciousContentChecker.Tests.ps1` | 1 |
| `test/powershell/engine/Api/TaskBasedAsyncPowerShellAPI.Tests.ps1` | 9 |
| `test/powershell/engine/Api/TypeInference.Tests.ps1` | 202 |
| `test/powershell/engine/Basic/Assembly.LoadBytesAndLoadFile.Tests.ps1` | 2 |
| `test/powershell/engine/Basic/Assembly.LoadFrom.Tests.ps1` | 1 |
| `test/powershell/engine/Basic/Assembly.LoadNative.Tests.ps1` | 1 |
| `test/powershell/engine/Basic/Assembly.LoadWithPartialName.Tests.ps1` | 1 |
| `test/powershell/engine/Basic/Assembly.LoadedInSeparateALC.Tests.ps1` | 1 |
| `test/powershell/engine/Basic/Attributes.Tests.ps1` | 1 |
| `test/powershell/engine/Basic/CLRBinding.Tests.ps1` | 12 |
| `test/powershell/engine/Basic/CommandDiscovery.Tests.ps1` | 15 |
| `test/powershell/engine/Basic/Credential.Tests.ps1` | 2 |
| `test/powershell/engine/Basic/DefaultCommands.Tests.ps1` | 6 |
| `test/powershell/engine/Basic/Encoding.Tests.ps1` | 7 |
| `test/powershell/engine/Basic/GroupPolicySettings.Tests.ps1` | 6 |
| `test/powershell/engine/Basic/NativeCommandBytePiping.Tests.ps1` | 8 |
| `test/powershell/engine/Basic/NativeCommandErrorHandling.Tests.ps1` | 10 |
| `test/powershell/engine/Basic/PropertyAccessor.Tests.ps1` | 4 |
| `test/powershell/engine/Basic/SemanticVersion.Tests.ps1` | 19 |
| `test/powershell/engine/Basic/StandardLibraryTypes.Tests.ps1` | 1 |
| `test/powershell/engine/Basic/Telemetry.Tests.ps1` | 11 |
| `test/powershell/engine/Basic/TypeResolution.Tests.ps1` | 1 |
| `test/powershell/engine/Basic/ValidateAttributes.Tests.ps1` | 17 |
| `test/powershell/engine/ETS/TypeTable.Tests.ps1` | 4 |
| `test/powershell/engine/Remoting/RunspacePool.Tests.ps1` | 1 |

xUnit tests on the language layer:

| File | Facts | Theories | Classes |
|---|---:|---:|---|
| `test/xUnit/csharp/test_Binders.cs` | 1 | 0 | PSEnumerableBinderTests |
| `test/xUnit/csharp/test_AstDefaultVisit.cs` | 2 | 0 | MyICustomAstVisitor2, MyDefaultCustomAstVisitor2, MyAstVisitor2, AstDefaultVisitTests |
| `test/xUnit/csharp/test_CommandLineParser.cs` | 55 | 52 | PSCommandLineParserTests, TestDataSettingsFile, TestDataLastFile |
<!--/GEN:tests-->

Feature mapping (by folder, `INFERENCE` from names): `Parser/` — tokenizer, parser, AST, semantic errors ([02.1](02.1-tokenizer.md)-[02.4](02.4-semantic-analysis.md)); `Operators/` — operator semantics ([OPERATOR-TABLE.md](OPERATOR-TABLE.md), [CONVERSION-RULES.md](CONVERSION-RULES.md)); `Scripting/` — flow control, functions, scoping, errors, pipelines, redirection ([02.5](02.5-compiler-and-engine.md), [SCOPE-AND-VARIABLES.md](SCOPE-AND-VARIABLES.md)); `Classes/` — class and enum features (EXTENDED); `Interop/` — .NET interop and ETS-related behavior.

## 6. Control flow

Not applicable.

## 7. Algorithms

Not applicable.

## 8. Observable behavior [SPEC]

Each `It` is a behavior statement; the new product should port the *intent* of the Language tests as its own specification tests, after the oracle confirms current behavior.

## 9. Error handling and edge cases

`APPROX` counts miss parameterized and generated `It` blocks (`parameterized_blocks` field in the dataset).

## 10. Concurrency and threading

Not applicable.

## 11. Extension points and customization hooks

Tags (`CI`, `Feature`, `Slow`) in the dataset tree.

## 12. Dependencies

[GOLDEN-SAMPLES.md](GOLDEN-SAMPLES.md), [ORACLE-PROTOCOL.md](ORACLE-PROTOCOL.md).

## 13. Performance notes

Not applicable.

## 14. Security considerations (mandatory)

Tests run scripts; they were not executed here.

## 15. Enterprise considerations

Not applicable.

## 16. Tests

This document is the test inventory.

## 17. Design decisions and trade-offs

Inventory by path and counts rather than by assertion keeps the study clean-room and cheap; the cost is that tests are not yet linked to individual claims (VB-005).

## 18. Guidance for MicroteamShell [LESSON]

- **LSN-CORPUS-01** [REPLICATE] (area: NLD-TOOL) Organize the new shell's specification tests by the same feature folders (parser, operators, scripting, classes) and keep one behavior per test. Evidence: `test/powershell/Language/Parser/` (folder layout in `data/tests.json`).
- **LSN-CORPUS-02** [ADAPT] (area: NLD-TOOL) Write the new suite in the shell's own language plus a small C# harness, so tests run without PowerShell. Why: same coverage, no dependency on the reference implementation. Evidence: `test/xUnit/csharp/test_Binders.cs` (xUnit tests of internal binders).

## 19. Open questions / UNVERIFIED

- Per-claim linking of tests (VB-005).
- Tests for Phase 3 areas (modules, providers) are outside this table.

Verification: counts come from `data/tests.json` through the generator; the number of Language files and `It` blocks is registered (`LANGUAGE_TEST_FILES`, `LANGUAGE_TEST_ITS`).
