# powershell-perf

| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |
|---|---|---|---|---|---|---|
| `test/perf/benchmarks/powershell-perf.csproj` | Exe | net10.0 | cross-platform (conditional items) | `powershell-perf` | DefineConstants [if  '$(IsWindows)' != 'true' ]=$(DefineConstants);UNIX | C:5 |

**Purpose.** _GENERATED stub — no annotation yet._ Project `powershell-perf` (5 C# files, 262 lines).

## Top-level folders

| Folder | Files (rec.) | LOC (rec.) |
|---|---:|---:|

## Public API surface (APPROX)

5 types, 5 public top-level types.

## References

Project refs: `BenchmarkDotNet.Extensions`, `Microsoft.PowerShell.SDK`, `Microsoft.PowerShell.Commands.Diagnostics`, `Microsoft.WSMan.Management`

Packages: Microsoft.PowerShell.SDK $(PerfTargetVersion), Microsoft.PowerShell.Commands.Diagnostics $(PerfTargetVersion), Microsoft.PowerShell.Commands.Management $(PerfTargetVersion), Microsoft.PowerShell.Commands.Utility $(PerfTargetVersion), Microsoft.PowerShell.ConsoleHost $(PerfTargetVersion), Microsoft.PowerShell.Security $(PerfTargetVersion), Microsoft.PowerShell.CoreCLR.Eventing $(PerfTargetVersion), Microsoft.WSMan.Management $(PerfTargetVersion), Microsoft.WSMan.Runtime $(PerfTargetVersion), System.Management.Automation $(PerfTargetVersion)

Referenced by: none

## Key files (top 10 by LOC unless annotated)

| File | LOC | Role |
|---|---:|---|
| `test/perf/benchmarks/Engine.Compiler.cs` | 78 | _GENERATED_ |
| `test/perf/benchmarks/Engine.ScriptBlock.cs` | 77 | _GENERATED_ |
| `test/perf/benchmarks/Program.cs` | 56 | _GENERATED_ |
| `test/perf/benchmarks/Categories.cs` | 28 | _GENERATED_ |
| `test/perf/benchmarks/Engine.Parser.cs` | 23 | _GENERATED_ |

## Related documents

_none linked yet_
