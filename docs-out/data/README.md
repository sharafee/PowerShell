# Dataset schemas (section 5.2)

All datasets are produced by `tools/*.py` (Python 3; no Roslyn available — D-002, D-006). Unless stated, labels are `APPROX`. Preprocessor handling: `csscan.py` does not evaluate `#if`; it records the enclosing condition expressions per type/member (`cond`), so both Windows-like and Unix-like branches are present in the data and platform-conditional items are marked by non-empty `cond`. The symbol sets actually used by the projects are listed in `conditional-compilation.json` (21 symbols) and `projects.json` (`defines`).

| File | Producer | Fields |
|---|---|---|
| `files.csv` | `p0_extract.py` | path, language, loc, tier, project, generated |
| `projects.json` | `p0_extract.py` | path, name, in_solution, sdk, output_type, assembly_name, target_frameworks, tfm_conditions, defines, project_references[{path,condition,analyzer}], package_references[{name,version,condition}], compile_removes, source_generators_analyzers, internals_visible_to, cs_files, cs_loc |
| `types.json` | `p0_extract.py` | kind, name, full_name, namespace, parent, project, file, start, end, accessibility, modifiers, bases, attributes, cond, member_counts, tier, generated, partial, partial_files |
| `members-tierA.json` | `p0_extract.py` | per Tier A type: members[{kind,name,access,modifiers,start,end,returns,sig,attributes,cond}] (callees only in `parser-methods.json`) |
| `enums.json` | `p0_extract.py` | full_name, file, start, end, accessibility, attributes, cond, members[{name,line,value,attributes,cond}] |
| `conditional-compilation.json` | `p0_extract.py` | symbol -> {files, types} |
| `ast-hierarchy.json` | `p0_extract2.py` | name, file, start, end, base_chain, modifiers, created_by_parser[{method,line}], ast_typed_members |
| `visitors.json` | `p0_extract2.py` | name, file, bases, visit_methods |
| `binders.json` | `p0_extract2.py` | name, file, chain, created_or_obtained_at[{file,line}] |
| `instructions.json` | `p0_extract2.py` | interpreter instruction classes (name, file, chain, modifiers) |
| `cmdlets.json` | `p0_extract2.py` | class, file, project, kind (cmdlet\|provider), verb_expr, noun_expr, default_parameter_set, parameter_sets, parameter_attribute_count, supports_should_process, has_dynamic_parameters, lifecycle_overrides, cond |
| `resources.json` | `p0_extract2.py` | neutral .resx -> {class, key_count, keys[{key,uses,use_count}]} |
| `auto-variables.json` | `p0_extract2.py` | SpecialVariables constants (+ reference counts, write-candidate sites) and arrays |
| `attributes.json` | `p0_extract2.py` | attribute types (name, file, chain, AttributeUsage-bearing attributes) |
| `tests.json` | `p0_extract2.py` | pester[{path,describe,context,it,tree}], xunit[{path,classes,facts,theories}] (regex; no pwsh parser available) |
| `tables.json` | `p0_extract2.py` | static tables from tokenizer/token/parser sources, verbatim text |
| `format-and-types-xml.json` | `p0_extract2.py` | `*.ps1xml` types / views |
| `parser-methods.json` | `p0_extract2.py` | method, line range, name-based callee list for `Parser.cs` and `tokenizer.cs` |
| `enforcement-points.json` | `p0_extract2.py` | **seed hits only** (unverified); verified entries get `SEC-ENF-###` in Phase 5 |
| `numbers.json` | `numbers.py gen` | key, value, dataset, command, evidence, label, notes |
| `canonical-facts.json` | Phase 0 (seed) + authors | id, subject, statement, label, evidence, owner, status |
| `claims/*.jsonl` | authoring subagents | Appendix E claim schema |
| `interpreter-scores.json` | Phase 2.10 | option, criterion, score, justification, label |
| `golden/` | — | **empty by design**: no engine could be built (VB-001) |
| `annotations/*.json` | authors | overlays for `src-mirror` cards (`folder-purposes.json`, `project-purposes.json`) |
