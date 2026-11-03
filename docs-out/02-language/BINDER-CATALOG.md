---
id: LANG-BINDERCAT-001
title: Binder catalog
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: []
sources: [src/System.Management.Automation/engine/runtime/Binding/Binders.cs, src/System.Management.Automation/engine/ComInterop/ComBinder.cs, src/System.Management.Automation/engine/ComInterop/ComInvokeAction.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/runtime/_folder.md]
generated_from: [data/binders.json]
---

# Binder catalog

> STATIC-ONLY — behavior not run-verified. The table is `GENERATED` by `docs-out/tools/gen_T26.py` from `data/binders.json` (`APPROX`) joined with hand annotations (`docs-out/tools/annotations/T26-binders.json`). Annotation level **read** = the binder's bind/fallback body was read (`FACT-SRC`); **names** = only member names and the compiler's use were read, details `UNVERIFIED` (VB-020). Narrative: [02.6-types-and-operators.md](02.6-types-and-operators.md), [RUNTIME-OPERATIONS.md](RUNTIME-OPERATIONS.md), [IR-SPEC.md](IR-SPEC.md) §5.

## 1. Purpose and scope [SPEC]

A *binder* is a DLR object that turns an operation on runtime values into code, and caches the result per call site by operand types. Every non-trivial operation in compiled PowerShell code (operators, casts, member access, indexing, enumeration, output writes) is a dynamic call site with one of these binders. The scanner found <!--N:BINDER_CLASSES-->30<!--/N--> binder classes (<!--N:BINDER_CLASSES_PS-->26<!--/N--> in `Binders.cs`, the rest COM interop), with <!--N:BINDER_CREATION_SITES-->164<!--/N--> creation or lookup sites.

## 2. Source map

| path | role |
|---|---|
| `src/System.Management.Automation/engine/runtime/Binding/Binders.cs` | all PowerShell binders (8,015 lines) |
| `src/System.Management.Automation/engine/ComInterop/ComBinder.cs`, `ComInvokeAction.cs` | COM member and invoke binders (out of scope, listed for completeness) |

## 3. Binder table

| Binder | Base | Operation (annotation) | Level | Used for | Creation sites | Source |
|---|---|---|---|---|---:|---|
| `ComBinder.ComGetMemberBinder` | `GetMemberBinder` | COM interop binder (out of scope). | names | COM objects | 1 | `src/System.Management.Automation/engine/ComInterop/ComBinder.cs::ComGetMemberBinder@L308-L336` |
| `ComBinder.ComInvokeMemberBinder` | `InvokeMemberBinder` | COM interop binder (out of scope). | names | COM objects | 1 | `src/System.Management.Automation/engine/ComInterop/ComBinder.cs::ComInvokeMemberBinder@L341-L375` |
| `ComInvokeAction` | `InvokeBinder` | COM interop binder (out of scope). | names | COM objects | 1 | `src/System.Management.Automation/engine/ComInterop/ComInvokeAction.cs::ComInvokeAction@L16-L41` |
| `SplatInvokeBinder` | `CallSiteBinder` | COM interop binder (out of scope). | names | COM objects | 1 | `src/System.Management.Automation/engine/ComInterop/ComInvokeAction.cs::SplatInvokeBinder@L47-L83` |
| `PSEnumerableBinder` | `ConvertBinder` | Convert a value to an IEnumerator following the enumeration rule (CF-PIP-001): AutomationNull = empty; null, string, PSObject-without-base, IDictionary, XmlNode = not enumerable (null result); arrays, DataTable rows, COM enumerables, IEnumerable<T> (typed enumerator preferred), IEnumerable, IEnumerator = enumerated. | read | foreach, switch, pipelines, @(), operators that accept collections | 8 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSEnumerableBinder@L518-L780` |
| `PSToObjectArrayBinder` | `DynamicMetaObjectBinder` | Value to object[]: AutomationNull = empty array; non-enumerable = one-element array; List<object> = ToArray; any enumerable = array of its elements. | read | `@( … )` over a single value | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSToObjectArrayBinder@L785-L839` |
| `PSPipeWriterBinder` | `DynamicMetaObjectBinder` | Write a statement value to the output pipe: AutomationNull writes nothing; non-enumerable written as one object (mutable value types copied via PSVariableAssignmentBinder); enumerable unrolled one level and disposed. | read | every bare expression statement (CallAddPipe) | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSPipeWriterBinder@L841-L926` |
| `PSArrayAssignmentRHSBinder` | `DynamicMetaObjectBinder` | Shape the right side of `$a,$b,$c = …` to exactly n elements: list of n = as is; fewer = padded with $null; more = last target receives the rest as a slice; non-list = first target gets it, others $null. | read | array destructuring assignment | 3 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSArrayAssignmentRHSBinder@L935-L1042` |
| `PSToStringBinder` | `DynamicMetaObjectBinder` | Convert a value to string for expandable strings, -f arguments and file names (ToString via the engine string parser; InvokeToString helper). | names | expandable strings, format operator, redirection file names | 16 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSToStringBinder@L1054-L1114` |
| `PSPipelineResultToBoolBinder` | `DynamicMetaObjectBinder` | Captured pipeline list to bool: 0 elements = false; 1 element = that element converted to bool; more than 1 = true. | read | conditions of if/while/for/switch/do | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSPipelineResultToBoolBinder@L1119-L1178` |
| `PSInvokeDynamicMemberBinder` | `DynamicMetaObjectBinder` | Invoke a method whose name is computed at run time (`$o.$name(args)`). | names | dynamic member invocation | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSInvokeDynamicMemberBinder@L1180-L1276` |
| `PSGetDynamicMemberBinder` | `DynamicMetaObjectBinder` | Get a member whose name is computed at run time (`$o.$name`). | names | dynamic member read | 3 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSGetDynamicMemberBinder@L1291-L1399` |
| `PSSetDynamicMemberBinder` | `DynamicMetaObjectBinder` | Set a member whose name is computed at run time. | names | dynamic member write | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSSetDynamicMemberBinder@L1401-L1491` |
| `PSSwitchClauseEvalBinder` | `DynamicMetaObjectBinder` | Evaluate a non-constant switch clause expression against `$_` according to the switch flags (regex, wildcard, exact, case-sensitive, script block). | names | switch clauses that are not constants | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSSwitchClauseEvalBinder@L1493-L1609` |
| `PSAttributeGenerator` | `CreateInstanceBinder` | Create an attribute instance from positional and named argument values (CreateInstanceBinder); compiled lambda cached per call shape. | names | attribute creation for parameters/functions | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSAttributeGenerator@L1613-L1792` |
| `PSCustomObjectConverter` | `DynamicMetaObjectBinder` | Convert an ordered dictionary to a PSCustomObject. | names | `[pscustomobject]@{…}` | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSCustomObjectConverter@L1794-L1828` |
| `PSDynamicConvertBinder` | `DynamicMetaObjectBinder` | Conversion whose target type is resolved at run time (type name unresolved at compile time). | names | `[SomeType]$x` with late-bound type | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSDynamicConvertBinder@L1830-L1863` |
| `PSVariableAssignmentBinder` | `DynamicMetaObjectBinder` | Copy mutable value types when a value is stored in a variable or written to the pipe (so later mutation does not alias); also notes types with instance members. | names | assignment to object-typed variables, pipe writes | 5 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSVariableAssignmentBinder@L1868-L2110` |
| `PSBinaryOperationBinder` | `BinaryOperationBinder` | Binary operators on arbitrary operands: dispatch on the operation, then rules per operand types (numeric promotion, string/array/hashtable arithmetic, comparison with enumerable filtering, user-defined op_* methods). See OPERATOR-TABLE.md. | read | every non-native binary operator | 25 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder@L2119-L3422` |
| `PSUnaryOperationBinder` | `UnaryOperationBinder` | Unary Not, OnesComplement (-bnot), plus, minus, increment, decrement (members Not, BNot, UnaryPlus, UnaryMinus, IncrDecr). | names | unary operators | 10 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSUnaryOperationBinder@L3427-L3738` |
| `PSConvertBinder` | `ConvertBinder` | Cast/conversion: AutomationNull converts to the default value of the target; otherwise FigureConversion(value, type) and invoke the converter with invariant culture; binding is restricted by a version number and the language mode; ThrowNoConversion raises the cast error. | read | `[type]value`, typed variables, parameter conversions | 16 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSConvertBinder@L3743-L3941` |
| `PSGetIndexBinder` | `GetIndexBinder` | Index read: dictionaries, arrays (negative indices count from the end, multi-dimensional arrays, slicing by index lists), strings, objects with an indexer, null-conditional; errors via CannotIndexTarget. | names | `$x[i]`, `?[` | 7 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSGetIndexBinder@L3946-L4533` |
| `PSSetIndexBinder` | `SetIndexBinder` | Index write with the same shapes as read, plus value conversion. | names | `$x[i] = v` | 4 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSSetIndexBinder@L4538-L4905` |
| `PSGetMemberBinder` | `GetMemberBinder` | Property/field read: instance (ETS) members, adapted .NET members, hashtable/dictionary keys, member enumeration over collections, reserved intrinsic members; strict-mode property-missing errors; language-mode checks. | names | `$x.Name`, `[T]::Name` | 25 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSGetMemberBinder@L4910-L5956` |
| `PSGetMemberBinder.ReservedMemberBinder` | `PSGetMemberBinder` | Handles intrinsic reserved members of PSObject-style access (nested binder). | names | reserved member names | 5 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::ReservedMemberBinder@L4936-L4974` |
| `PSSetMemberBinder` | `SetMemberBinder` | Property/field write with value conversion to the member type, instance members and adapted members. | names | `$x.Name = v` | 4 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSSetMemberBinder@L5961-L6594` |
| `PSInvokeBinder` | `InvokeBinder` | Invoke a callable value. | names | invocation of delegates/script blocks | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSInvokeBinder@L6596-L6606` |
| `PSInvokeMemberBinder` | `InvokeMemberBinder` | Method call: overload resolution (FindBestMethod with conversion ranks), .Where()/.ForEach() intrinsic methods on collections, method call on each element of a collection, parameterized properties, COM, member-invocation logging. | names | `$x.Method(args)`, `[T]::Method(args)` | 4 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSInvokeMemberBinder@L6608-L7737` |
| `PSCreateInstanceBinder` | `CreateInstanceBinder` | Constructor call for `[T]::new(args)` / `New-Object`-style creation; rejects by-ref-like and (optionally) non-public types. | names | `[T]::new(…)` | 3 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSCreateInstanceBinder@L7739-L7932` |
| `PSInvokeBaseCtorBinder` | `InvokeMemberBinder` | Call a base-class constructor from a class constructor. | names | `: base(args)` in class constructors | 2 | `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSInvokeBaseCtorBinder@L7934-L8012` |

Rows: **30** (`GENERATED`). Binders without annotation: none.

## 4. Common mechanics [IMPL]

- **Defer when values are missing**: a binder first checks `target.HasValue`; if an operand is a `PSObject` wrapper with a different base object it defers to a PSObject-aware path (`DeferForPSObject`), except `Add` on enumerables.
- **Restrictions**: each produced rule is guarded by type restrictions (`PSGetTypeRestriction`) and, for conversions, by a binder *version* and the language mode, so a language-mode change or a type-table change invalidates cached rules (`InvalidateCache`, version counters; `ExecutionContext.LanguageMode` setter).
- **Per-site caches**: each emitted dynamic expression has its own `CallSite`; both execution tiers use them ([EQUIVALENCE-SPEC.md](EQUIVALENCE-SPEC.md) EQ-02).
- **Fallback with error suggestion**: binders pass an `errorSuggestion` so that "operation not supported" throws a PowerShell error instead of a DLR error.

## 5. Guidance for MicroteamShell [LESSON]

- **LSN-BIND-01** [ADAPT] (area: NLD-RUN) Replace DLR binders by explicit dispatch functions per operation (`Add(left, right)`, `Convert(value, type)`, `GetMember(target, name)`, `Index(target, args)`) with a small per-site cache only if profiling shows a need. Why: the DLR is a mechanism, the observable behavior is the rule set. Evidence: `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSBinaryOperationBinder@L2119-L3422`.
- **LSN-BIND-02** [REPLICATE] (area: NLD-TYP) Keep the dedicated helper operations (enumerate, to-object-array, write-to-pipe, array-assignment shaping, pipeline-result-to-bool); they encode language rules. Evidence: `src/System.Management.Automation/engine/runtime/Binding/Binders.cs::PSEnumerableBinder@L518-L780`, `PSPipeWriterBinder@L841-L926`, `PSArrayAssignmentRHSBinder@L935-L1042`, `PSPipelineResultToBoolBinder@L1119-L1178`.
- **LSN-BIND-03** [AVOID] (area: NLD-RUN) Do not port COM binders and `PSGetMemberBinder`'s COM/ETS-adapter paths in the first versions. Replace with a plain reflection member lookup. Evidence: `src/System.Management.Automation/engine/ComInterop/ComBinder.cs::ComBinder@L1-L378`. DEV: DEV-BIND-050

Verification: binder list reconciles with `data/binders.json` (counts above); `PSEnumerableBinder`, `PSToObjectArrayBinder`, `PSPipeWriterBinder`, `PSArrayAssignmentRHSBinder`, `PSPipelineResultToBoolBinder`, `PSConvertBinder.FallbackConvert`, `PSBinaryOperationBinder` (dispatch, add, multiply, divide/remainder, equality, numeric) bodies were read; the others by member list and compiler use.

