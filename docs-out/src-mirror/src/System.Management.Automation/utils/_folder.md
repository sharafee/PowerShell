# src/System.Management.Automation/utils

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| B:46 | System.Management.Automation | 46 | 22046 | 148 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `ClrFacade.cs` | 371 | `ClrFacade` |  |  |
| `CommandDiscoveryExceptions.cs` | 477 | `ScriptRequiresException`, `CommandNotFoundException` |  |  |
| `CommandProcessorExceptions.cs` | 100 | `ApplicationFailedException` |  |  |
| `CoreProviderCmdlets.cs` | 197 | `ProviderCmdlet` |  |  |
| `CryptoUtils.cs` | 1175 | `PSRemotingCryptoHelper`, `PSRSACryptoServiceProvider`, `PSCryptoNativeConverter`, `PSRemotingCryptoHelperServer` (+3) |  |  |
| `EncodingUtils.cs` | 159 | `EncodingConversion`, `ArgumentToEncodingTransformationAttribute`, `ArgumentEncodingCompletionsAttribute` |  |  |
| `ExecutionExceptions.cs` | 977 | `ActionPreferenceStopException`, `CmdletInvocationException`, `CmdletProviderInvocationException`, `ParentContainsErrorRecordException` (+6) |  |  |
| `ExtensionMethods.cs` | 135 | `PSTypeExtensions`, `EnumerableExtensions`, `ExtensionMethods`, `WeakReferenceExtensions` |  |  |
| `FormatAndTypeDataHelper.cs` | 210 | `FormatAndTypeDataHelper`, `PSSnapInTypeAndFormatErrors` |  |  |
| `FuzzyMatch.cs` | 87 | `FuzzyMatcher` |  |  |
| `GraphicalHostReflectionWrapper.cs` | 218 | `GraphicalHostReflectionWrapper` |  |  |
| `HostInterfacesExceptions.cs` | 228 | `HostException`, `PromptingException` |  |  |
| `IObjectReader.cs` | 180 | `PipelineReader<T>` |  |  |
| `IObjectWriter.cs` | 193 | `PipelineWriter`, `DiscardingPipelineWriter` |  |  |
| `MetadataExceptions.cs` | 269 | `ValidationMetadataException`, `MetadataException`, `ArgumentTransformationMetadataException`, `ParsingMetadataException` |  |  |
| `MshArgumentException.cs` | 134 | `PSArgumentException` |  |  |
| `MshArgumentNullException.cs` | 131 | `PSArgumentNullException` |  |  |
| `MshArgumentOutOfRangeException.cs` | 117 | `PSArgumentOutOfRangeException` |  |  |
| `MshInvalidOperationException.cs` | 122 | `PSInvalidOperationException` |  |  |
| `MshNotImplementedException.cs` | 97 | `PSNotImplementedException` |  |  |
| `MshNotSupportedException.cs` | 98 | `PSNotSupportedException` |  |  |
| `MshObjectDisposedException.cs` | 103 | `PSObjectDisposedException` |  |  |
| `MshTraceSource.cs` | 538 | `PSTraceSource` |  |  |
| `ObjectReader.cs` | 824 | `ObjectReaderBase<T>`, `PSDataCollectionPipelineReader<T,TReturn>`, `PSDataCollectionReader<T,TResult>`, `PSObjectReader` (+1) |  |  |
| `ObjectStream.cs` | 1943 | `ObjectStream`, `PSDataCollectionStream<T>`, `ObjectStreamBase` |  |  |
| `ObjectWriter.cs` | 231 | `ObjectWriter`, `PSDataCollectionWriter<T>` |  |  |
| `PInvokeDllNames.cs` | 141 | `PinvokeDllNames` |  |  |
| `PSTelemetryMethods.cs` | 534 | `TelemetryAPI`, `ScriptBlockTelemetry`, `IHostProvidesTelemetryData` |  |  |
| `PSTelemetryWrapper.cs` | 150 | `TelemetryWrapper` |  |  |
| `ParameterBinderExceptions.cs` | 1031 | `ParameterBindingException`, `ParameterBindingValidationException`, `ParameterBindingParameterDefaultValueException`, `ParameterBindingArgumentTransformationException` |  |  |
| `ParserException.cs` | 251 | `ParseException`, `IncompleteParseException` |  |  |
| `PathUtils.cs` | 907 | `PathUtils` |  |  |
| `PlatformInvokes.cs` | 679 | `PlatformInvokes` |  |  |
| `PowerShellETWTracer.cs` | 1540 | `PowerShellTraceSource`, `PowerShellTraceEvent`, `PowerShellTraceOperationCode`, `PowerShellChannelWriter` (+7) |  |  |
| `PowerShellExecutionHelper.cs` | 198 | `PowerShellExecutionHelper`, `PowerShellExtensionHelpers` |  |  |
| `PsUtils.cs` | 562 | `PsUtils`, `StringToBase64Converter`, `CRC32Hash`, `ReferenceEqualityComparer` |  |  |
| `ResourceManagerCache.cs` | 244 | `ResourceManagerCache` |  |  |
| `RuntimeException.cs` | 299 | `RuntimeException` |  |  |
| `SessionStateExceptions.cs` | 971 | `ProviderInvocationException`, `SessionStateException`, `ProviderNameAmbiguousException`, `SessionStateUnauthorizedAccessException` (+4) |  |  |
| `StringUtil.cs` | 273 | `StringUtil` |  |  |
| `StructuredTraceSource.cs` | 1849 | `PSTraceSource`, `ScopeTracer`, `PSTraceSourceOptions`, `TraceSourceAttribute` (+1) |  |  |
| `Telemetry.cs` | 1035 | `ApplicationInsightsTelemetry`, `TelemetryType`, `NameObscurerTelemetryInitializer` |  |  |
| `VTUtils.cs` | 85 | `VTUtility` |  |  |
| `Verbs.cs` | 1601 | `VerbAliasPrefixes`, `Verbs`, `VerbsCommon`, `VerbsData` (+7) |  |  |
| `WindowsDataCollectionSetting.cs` | 185 | `WindowsDataCollectionSetting`, `PlatformDataCollectionLevel`, `IPlatformDiagnosticsAndUsageDataSettingsStatics`, `IInspectable` |  |  |
| `assert.cs` | 197 | `Diagnostics`, `AssertException` |  |  |

## Subfolders

- [tracing](tracing/_folder.md) (11 files, 3403 LOC)

## Partial-class and conditional-compilation notes

Partial types spanning files: `PSTraceSource`, `PowerShellTraceKeywords`, `PowerShellTraceSourceFactory`, `PowerShellTraceSource`, `PowerShellTraceTask`

`#if` conditions on types here: `!UNIX`, `LEGACYTELEMETRY`

## Related documents

_none linked yet_
