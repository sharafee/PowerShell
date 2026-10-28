# src/System.Management.Automation/engine/parser

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| A:18 | System.Management.Automation | 18 | 48688 | 212 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `AstVisitor.cs` | 822 | `AstSearcher`, `ICustomAstVisitor`, `DefaultCustomAstVisitor`, `CheckAllParentsSet` (+3) |  |  |
| `CharTraits.cs` | 414 | `CharExtensions`, `CharTraits`, `SpecialChars` |  |  |
| `Compiler.cs` | 7082 | `Compiler`, `CachedReflectionInfo`, `InvokeMemberAssignableValue`, `IndexAssignableValue` (+8) |  |  |
| `ConstantValues.cs` | 578 | `IsConstantValueVisitor`, `ConstantValueVisitor` |  |  |
| `DebugViewWriter.cs` | 1219 | `DebugViewWriter` |  |  |
| `PSType.cs` | 1520 | `TypeDefiner`, `NoRunspaceAffinityAttribute` |  |  |
| `Parser.cs` | 8279 | `Parser`, `ParseError`, `ParserEventSource`, `ParseMode` |  |  |
| `Position.cs` | 816 | `PositionUtilities`, `ScriptExtent`, `ScriptPosition`, `InternalScriptExtent` (+6) |  |  |
| `PreOrderVisitor.cs` | 264 | `AstVisitor`, `AstVisitor2`, `AstVisitAction`, `IAstPostVisitHandler` |  |  |
| `SafeValues.cs` | 807 | `GetSafeValueVisitor`, `IsSafeValueVisitor` |  |  |
| `SemanticChecks.cs` | 2455 | `SemanticChecks`, `RestrictedLanguageChecker`, `DscResourceChecker` |  |  |
| `SymbolResolver.cs` | 763 | `SymbolResolver`, `Scope`, `SymbolTable`, `SymbolResolvePostActionVisitor` (+2) |  |  |
| `TypeInferenceVisitor.cs` | 3338 | `TypeInferenceVisitor`, `TypeInferenceContext`, `AstTypeInference`, `TypeInferenceExtension` (+2) |  |  |
| `TypeResolver.cs` | 980 | `TypeResolver`, `TypeResolutionState`, `TypeAccelerators`, `CoreTypes` (+1) |  |  |
| `VariableAnalysis.cs` | 1848 | `VariableAnalysis`, `FindAllVariablesVisitor`, `VariableAnalysisDetails`, `VariablePathExtensions` |  |  |
| `ast.cs` | 10845 | `ScriptBlockAst`, `ConfigurationDefinitionAst`, `DynamicKeywordStatementAst`, `Ast` (+94) |  |  |
| `token.cs` | 1575 | `TokenKind`, `TokenTraits`, `TokenFlags`, `Token` (+12) |  |  |
| `tokenizer.cs` | 5083 | `Tokenizer`, `DynamicKeyword`, `DynamicKeywordProperty`, `DynamicKeywordExtension` (+7) |  |  |

## Partial-class and conditional-compilation notes

No partial types spanning files (APPROX).

`#if` conditions on types here: `DEBUG`, `ENABLE_BINDER_DEBUG_LOGGING`

## Related documents

_none linked yet_
