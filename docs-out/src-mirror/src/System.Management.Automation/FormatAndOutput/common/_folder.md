# src/System.Management.Automation/FormatAndOutput/common

| Tier | Project | File count | LOC | Type count | Flags |
|---|---|---:|---:|---:|---|
| B:24 | System.Management.Automation | 24 | 12179 | 161 | GENERATED |

**Purpose.** _GENERATED stub — not annotated by reading._

## Files

| File | LOC | Main types | Role | Covering document |
|---|---:|---|---|---|
| `BaseCommand.cs` | 407 | `ImplementationCommandBase`, `FrontEndCommandBase`, `CommandWrapper`, `TerminatingErrorContext` |  |  |
| `BaseFormattingCommand.cs` | 899 | `InnerFormatShapeCommand`, `OuterFormatShapeCommandBase`, `OuterFormatTableBase`, `OuterFormatTableAndListBase` (+1) |  |  |
| `BaseFormattingCommandParameters.cs` | 489 | `ExpressionEntryDefinition`, `AlignmentEntryDefinition`, `FormattingCommandLineParameters`, `WidthEntryDefinition` (+14) |  |  |
| `BaseOutputtingCommand.cs` | 1395 | `OutCommandInner` |  |  |
| `ColumnWidthManager.cs` | 208 | `ColumnWidthManager` |  |  |
| `ComplexWriter.cs` | 829 | `StringManipulationHelper`, `ComplexWriter`, `IndentationManager`, `GetWordsResult` |  |  |
| `FormatGroupManager.cs` | 123 | `GroupingInfoManager` |  |  |
| `FormatMsgCtxManager.cs` | 144 | `FormatMessagesContextManager` |  |  |
| `FormatViewGenerator.cs` | 465 | `ViewGenerator` |  |  |
| `FormatViewGenerator_Complex.cs` | 774 | `ComplexViewObjectBrowser`, `ComplexControlGenerator`, `ComplexViewGenerator`, `TraversalInfo` |  |  |
| `FormatViewGenerator_List.cs` | 236 | `ListViewGenerator` |  |  |
| `FormatViewGenerator_Table.cs` | 493 | `TableViewGenerator` |  |  |
| `FormatViewGenerator_Wide.cs` | 197 | `WideViewGenerator` |  |  |
| `FormatViewManager.cs` | 685 | `FormatViewManager`, `FormatErrorManager`, `OutOfBandFormatViewManager`, `DefaultScalarTypes` |  |  |
| `FormatXMLWriter.cs` | 454 | `FormatXmlWriter` |  |  |
| `FormattingObjects.cs` | 395 | `FormatStartData`, `TableColumnInfo`, `FormatEntry`, `FormatInfoData` (+29) |  |  |
| `FormattingObjectsDeserializer.cs` | 700 | `FormatObjectDeserializer`, `FormatInfoDataClassFactory`, `FormatInfoDataListDeserializer<T>`, `TableHeaderInfo` (+18) |  |  |
| `ILineOutput.cs` | 580 | `DisplayCells`, `WriteLineHelper`, `TextWriterLineOutput`, `LineOutput` (+1) |  |  |
| `ListWriter.cs` | 288 | `ListWriter` |  |  |
| `OutputManager.cs` | 327 | `SubPipelineManager`, `OutputManagerInner` |  |  |
| `OutputQueue.cs` | 333 | `OutputGroupQueue`, `FormattedObjectsCache` |  |  |
| `PSStyle.cs` | 916 | `PSStyle`, `OutputRendering`, `ProgressView` |  |  |
| `StringDecorated.cs` | 189 | `ValueStringDecorated`, `StringDecorated` |  |  |
| `TableWriter.cs` | 653 | `TableWriter` |  |  |

## Subfolders

- [DisplayDatabase](DisplayDatabase/_folder.md) (19 files, 9755 LOC)
- [Utilities](Utilities/_folder.md) (4 files, 1785 LOC)

## Partial-class and conditional-compilation notes

Partial types spanning files: `AutosizeInfo`, `ControlInfoData`, `FormatEntryData`, `FormatEntry`, `FormatInfoData`, `FormatPropertyField`, `FormatStartData`, `FormatTextField`, `FrameInfo`, `FreeFormatEntry`, `ListViewEntry`, `ListViewField`, `RawTextFormatEntry`, `StartData`, `TableColumnInfo`, `TableHeaderInfo`, `TableRowEntry`, `WideViewEntry`, `WideViewHeaderInfo`

No conditionally-compiled types (APPROX).

## Related documents

_none linked yet_
