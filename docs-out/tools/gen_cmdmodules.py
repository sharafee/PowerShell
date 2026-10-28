#!/usr/bin/env python3
"""gen_cmdmodules.py - render 10-command-modules/<Assembly>.md and _index.md (Phase 4, Tier C).

Purpose : one document per cmdlet/provider assembly family: inventory (names and files only, no per-cmdlet
          walkthroughs), registration/discovery (InitialSessionState tables and module manifests), shipped
          type/format XML, resource files, dependencies, security notes, lessons.
Inputs  : data/cmdlets.json, projects.json, types.json, resources.json, format-and-types-xml.json,
          src/Modules/**/*.psd1, src/System.Management.Automation/engine/InitialSessionState.cs,
          data/annotations/cmdmodules.json (hand-written prose per assembly).
Outputs : docs-out/10-command-modules/*.md (GENERATED + annotations; labels APPROX).
Run     : python3 docs-out/tools/gen_cmdmodules.py
Language: Python 3 (D-002)   Tested: Linux x86_64 / Python 3.13
"""
import csv
import glob
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p0_docs import fm, BANNER  # noqa: E402

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
SMA = "src/System.Management.Automation/"


def J(n):
    return json.load(open(os.path.join(DATA, n)))


cmdlets = J("cmdlets.json")
projects = {}
for _p in J("projects.json"):
    if _p["name"] not in projects or _p["path"].startswith("src/"):
        projects[_p["name"]] = _p
resources = J("resources.json")
types = J("types.json")
ps1xml = J("format-and-types-xml.json")
ann = J("annotations/cmdmodules.json") if os.path.exists(os.path.join(DATA, "annotations", "cmdmodules.json")) else {}


def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8-sig", errors="replace").read()


# ---- constant index (const string X = "..." / static readonly string)
CONST = defaultdict(dict)  # class -> name -> value
GLOBAL = defaultdict(set)
for dp, dn, fn in os.walk(os.path.join(ROOT, "src")):
    for f in fn:
        if f.endswith(".cs"):
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
            cls = None
            for ln in read(rel).split("\n"):
                m = re.search(r"\b(?:class|struct)\s+(\w+)", ln)
                if m:
                    cls = m.group(1)
                m = re.search(r'(?:const|static readonly)\s+string\s+(\w+)\s*=\s*@?"([^"]*)"', ln)
                if m and cls:
                    CONST[cls][m.group(1)] = m.group(2)
                    GLOBAL[m.group(1)].add(m.group(2))


_TYPE_FILE = {}
for _t in types:
    _TYPE_FILE.setdefault(_t["name"].split("<")[0], set()).add(_t["file"])


def _from_class_file(cls, name):
    for f in _TYPE_FILE.get(cls, ()):
        m = re.search(r"\b" + re.escape(name) + r'\s*=\s*@?"([^"]*)"', read(f))
        if m:
            return m.group(1)
    return None


def resolve(expr, cls_hint=None):
    if expr is None:
        return None
    expr = expr.strip()
    m = re.fullmatch(r'"([^"]*)"', expr)
    if m:
        return m.group(1)
    m = re.fullmatch(r"Verbs\w+\.(\w+)", expr)
    if m:
        return m.group(1)
    m = re.fullmatch(r"(\w+)\.(\w+)", expr)
    if m and m.group(2) in CONST.get(m.group(1), {}):
        return CONST[m.group(1)][m.group(2)]
    if m:
        v = _from_class_file(m.group(1), m.group(2))
        if v is not None:
            return v
    if m and len(GLOBAL.get(m.group(2), ())) == 1:
        return next(iter(GLOBAL[m.group(2)]))
    if re.fullmatch(r"\w+", expr):
        if cls_hint and expr in CONST.get(cls_hint, {}):
            return CONST[cls_hint][expr]
        if len(GLOBAL.get(expr, ())) == 1:
            return next(iter(GLOBAL[expr]))
    return None


# ---- engine registration tables
isc = read(SMA + "engine/InitialSessionState.cs")
reg_entries = {}
for m in re.finditer(r'new SessionStateCmdletEntry\("([^"]+)",\s*typeof\((\w+)\)', isc):
    reg_entries[m.group(2)] = (m.group(1), isc.count("\n", 0, m.start()) + 1)
prov_entries = {}
for m in re.finditer(r'new SessionStateProviderEntry\(\s*(?:\w+\.)?(\w+)?[^,]*,\s*typeof\((\w+)\)', isc):
    prov_entries[m.group(2)] = isc.count("\n", 0, m.start()) + 1

# ---- manifests
manifests = []
for f in sorted(glob.glob(os.path.join(ROOT, "src/Modules/**/*.psd1"), recursive=True)):
    rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
    t = open(f, encoding="utf-8-sig", errors="replace").read()

    def arr(key):
        m = re.search(key + r"\s*=\s*@\((.*?)\)\s*(?:\n[A-Za-z]|\n\})", t, re.S)
        return re.findall(r"['\"]([^'\"]+)['\"]", m.group(1)) if m else []

    def sc(key):
        m = re.search(key + r"\s*=\s*['\"]([^'\"]+)['\"]", t)
        return m.group(1) if m else None
    manifests.append({"path": rel, "module": os.path.basename(f)[:-5], "platform": rel.split("/")[2], "version": sc("ModuleVersion"),
                      "cmdlets": arr("CmdletsToExport"), "functions": arr("FunctionsToExport"), "aliases": arr("AliasesToExport"),
                      "nested": arr("NestedModules"), "root": sc("RootModule"), "types": arr("TypesToProcess"), "formats": arr("FormatsToProcess"),
                      "scripts": arr("ScriptsToProcess")})


def cmd_name(c):
    cls = c["class"].split(".")[-1]
    v = resolve(c.get("verb_expr"), cls)
    n = resolve(c.get("noun_expr"), cls)
    if c["kind"] == "provider":
        return resolve(c.get("verb_expr"), cls) or cls
    return f"{v}-{n}" if v and n else f"?{c.get('verb_expr')}-{c.get('noun_expr')}"


ASSEMBLIES = [
    # (project name, doc file stem, doc id, scope)
    ("System.Management.Automation", "System.Management.Automation", "CMD-SMA-001", "EXTENDED"),
    ("Microsoft.PowerShell.Commands.Utility", "Microsoft.PowerShell.Commands.Utility", "CMD-UTILITY-001", "EXTENDED"),
    ("Microsoft.PowerShell.Commands.Management", "Microsoft.PowerShell.Commands.Management", "CMD-MANAGEMENT-001", "EXTENDED"),
    ("Microsoft.PowerShell.Security", "Microsoft.PowerShell.Security", "CMD-SECURITY-001", "EXTENDED"),
    ("Microsoft.PowerShell.ConsoleHost", "Microsoft.PowerShell.ConsoleHost", "CMD-CONSOLEHOST-001", "EXTENDED"),
    ("Microsoft.PowerShell.Commands.Diagnostics", "Microsoft.PowerShell.Commands.Diagnostics", "CMD-DIAGNOSTICS-001", "OUT-OF-SCOPE-DOCUMENTED"),
    ("Microsoft.WSMan.Management", "Microsoft.WSMan.Management", "CMD-WSMAN-001", "OUT-OF-SCOPE-DOCUMENTED"),
    ("Microsoft.Management.Infrastructure.CimCmdlets", "Microsoft.Management.Infrastructure.CimCmdlets", "CMD-CIM-001", "OUT-OF-SCOPE-DOCUMENTED"),
    ("Microsoft.WSMan.Runtime", "Microsoft.WSMan.Runtime", "CMD-WSMANRT-001", "OUT-OF-SCOPE-DOCUMENTED"),
    ("Microsoft.PowerShell.GraphicalHost", "Microsoft.PowerShell.GraphicalHost", "CMD-GRAPHICAL-001", "OUT-OF-SCOPE-DOCUMENTED"),
    ("Microsoft.PowerShell.CoreCLR.Eventing", "Microsoft.PowerShell.CoreCLR.Eventing", "CMD-EVENTING-001", "OUT-OF-SCOPE-DOCUMENTED"),
]


def gen(proj, stem, did, scope):
    P = projects[proj]
    a = ann.get(proj, {})
    mine = [c for c in cmdlets if c["project"] == proj]
    cm = sorted(((cmd_name(c), c) for c in mine if c["kind"] == "cmdlet"), key=lambda x: (x[0], x[1]["file"]))
    pv = sorted(((cmd_name(c), c) for c in mine if c["kind"] == "provider"), key=lambda x: (x[0], x[1]["file"]))
    pdir = os.path.dirname(P["path"])
    res = {k: v for k, v in resources.items() if k.startswith(pdir + "/")}
    # manifests that reference this assembly
    dll = proj + ".dll"
    mf = [m for m in manifests if dll in m["nested"] or m["root"] == dll or (m["root"] or "").endswith(dll)]
    # types / formats xml in project dir or manifests
    xml = [x["path"] for x in ps1xml if x["path"].startswith(pdir + "/")]
    s = fm(did, f"Command module family: {proj}", "subsystem", "C", scope, sources=[P["path"]], gen=["data/cmdlets.json", "data/projects.json", "data/resources.json"],
           mirror=[f"src-mirror/{pdir}/_project.md"]) + f"\n# Command module family: {proj}\n\n> STATIC-ONLY — behavior not run-verified. Inventory is `APPROX` (regex/own-scanner extraction); cmdlets are listed by name and file only (no per-cmdlet walkthroughs, by design).\n\n"
    s += "## 1. Purpose and scope [SPEC]\n\n" + (a.get("purpose") or "_GENERATED stub._") + "\n\n"
    s += "## 2. Source map\n\n| Path | Type/class | Role | Tier |\n|---|---|---|---|\n"
    s += f"| `{P['path']}` | project | {P['output_type'] or 'Library'}, TFM {P['target_frameworks'] or 'inherited net10.0'} | C |\n"
    s += f"| `{pdir}/` | {P['cs_files']} C# files, {P['cs_loc']} lines | assembly sources | C |\n"
    s += "\n## 3. Responsibilities and non-responsibilities\n\n" + (a.get("responsibilities") or "Provides the cmdlets/providers inventoried in section 4; contains no language, parser or pipeline logic (those live in `System.Management.Automation`).") + "\n\n"
    s += f"## 4. Key types and contracts [IMPL]\n\n**Cmdlet inventory** (<!--N:CMDLET_CLASSES-->{sum(1 for c in cmdlets if c['kind']=='cmdlet')}<!--/N--> cmdlet classes in the whole tree; this assembly: {len(cm)}; `APPROX`, `GENERATED` from `data/cmdlets.json`). Platform-conditional classes are marked by their `#if` condition.\n\n"
    if cm:
        s += "| Cmdlet | Class | File@Line | Parameter sets | ShouldProcess | Dynamic params | Condition |\n|---|---|---|---:|---|---|---|\n"
        for n, c in cm:
            s += f"| `{n}` | `{c['class'].split('.')[-1]}` | `{c['file']}@L{c['start']}` | {len(c['parameter_sets'])} | {'yes' if c['supports_should_process'] else ''} | {'yes' if c['has_dynamic_parameters'] else ''} | {' && '.join(c['cond']) if c['cond'] else ''} |\n"
    else:
        s += "No `[Cmdlet]` classes in this assembly.\n"
    if pv:
        s += "\n**Provider inventory**\n\n| Provider | Class | File@Line | Condition |\n|---|---|---|---|\n"
        for n, c in pv:
            s += f"| `{n}` | `{c['class'].split('.')[-1]}` | `{c['file']}@L{c['start']}` | {' && '.join(c['cond']) if c['cond'] else ''} |\n"
    s += "\n## 5. Data model\n\n" + (a.get("data_model") or "Not applicable beyond the cmdlet and provider classes listed above.") + "\n\n"
    s += "## 6. Control flow\n\n```mermaid\nflowchart LR\n  M[Module manifest or InitialSessionState table] --> L[Engine loads assembly]\n  L --> R[Engine registers cmdlet and provider classes]\n  R --> D[Command discovery resolves name to CmdletInfo]\n  D --> P[CommandProcessor runs lifecycle methods]\n```\n\nThe flow is the generic registration path; see [command discovery](../03-runtime/command-discovery-and-invocation.md) and [modules](../03-runtime/modules.md).\n\n"
    s += "## 7. Algorithms\n\nNot applicable: no non-trivial algorithm is documented at family level.\n\n"
    s += "## 8. Observable behavior [SPEC]\n\n" + (a.get("observable") or "Cmdlet behavior is out of scope for this family-level document. No golden sample: STATIC-ONLY.") + "\n\n"
    s += "## 9. Error handling and edge cases\n\n" + (a.get("errors") or "Cmdlets report through the engine's error-record APIs (`WriteError`, `ThrowTerminatingError`), described in [errors-and-diagnostics](../03-runtime/errors-and-diagnostics.md).") + "\n\n"
    s += "## 10. Concurrency and threading\n\nCmdlets run on the pipeline thread of their runspace; lifecycle overrides per class are in `data/cmdlets.json` (`lifecycle_overrides`). " + (a.get("concurrency") or "") + "\n\n"
    s += "## 11. Extension points and customization hooks\n\n### Registration and discovery (`FACT-SRC`)\n\n"
    ent = [(c["class"].split(".")[-1], reg_entries[c["class"].split(".")[-1]]) for n, c in cm if c["class"].split(".")[-1] in reg_entries]
    if ent:
        s += f"{len(ent)} of the {len(cm)} cmdlet classes are registered directly in the engine's built-in tables in `{SMA}engine/InitialSessionState.cs` through `SessionStateCmdletEntry(name, typeof(Class), helpFile)` (first and last entry lines @L{min(e[1][1] for e in ent)}-L{max(e[1][1] for e in ent)}).\n\n"
    if mf:
        s += "Module manifests that load this assembly (`NestedModules`/`RootModule`):\n\n| Manifest | Platform content folder | Cmdlets exported | Aliases | Types/Formats |\n|---|---|---:|---:|---|\n"
        for m in mf:
            s += f"| `{m['path']}` | {m['platform']} | {len(m['cmdlets'])} | {len(m['aliases'])} | {', '.join(m['types'] + m['formats']) or '-'} |\n"
        code_names = {n for n, c in cm}
        for m in mf:
            exp = set(m["cmdlets"])
            only_code = sorted(code_names - exp)
            only_man = sorted(exp - code_names)
            s += f"\nConsistency `{m['path']}`: exported but not found as a `[Cmdlet]` class in this assembly: {', '.join(only_man) or 'none'}; `[Cmdlet]` classes in this assembly not exported by this manifest: {len(only_code)}" + (f" ({', '.join(only_code[:12])}{'...' if len(only_code) > 12 else ''})" if only_code else "") + " (`APPROX`; differences arise from platform-conditional classes, cmdlets exported by other manifests, or verb/noun expressions the extractor could not resolve).\n"
    else:
        s += "No module manifest under `src/Modules` loads this assembly by name (registered another way — see annotations).\n"
    s += "\n" + (a.get("extension") or "") + "\n\n"
    s += "## 12. Dependencies\n\nProject references: " + (", ".join(f"`{r['path'].split('/')[-1][:-7]}`" for r in P["project_references"]) or "none") + ". Packages: " + (", ".join(f"{k['name']} {k['version'] or ''}" for k in P["package_references"]) or "none") + ". `InternalsVisibleTo` granted by this assembly: " + (", ".join(f"`{x}`" for x in P["internals_visible_to"]) or "none") + ".\n\n"
    s += "## 13. Performance notes\n\n" + (a.get("performance") or "Not applicable at family level.") + "\n\n"
    s += "## 14. Security considerations\n\n" + (a.get("security") or "No dedicated enforcement point identified at family level (`UNVERIFIED`; Phase 5 enumerates enforcement points across the tree).") + "\n\n"
    s += "## 15. Enterprise considerations\n\n" + (a.get("enterprise") or "Replaceable surface: a new shell chooses its own cmdlet set; the engine contracts these cmdlets use are the stable part.") + "\n\n"
    s += "## 16. Tests\n\n" + (a.get("tests") or "Pester tests under `test/powershell/Modules` and `test/powershell/engine` exercise these cmdlets (see [REFERENCE-TEST-CORPUS](../02-language/REFERENCE-TEST-CORPUS.md)).") + "\n\n"
    s += "## 17. Design decisions and trade-offs\n\n" + (a.get("decisions") or "Not applicable.") + "\n\n"
    s += "## 18. Guidance for the new shell [LESSON]\n\n"
    for i, l in enumerate(a.get("lessons", []), 1):
        s += f"- **LSN-{a['short']}-{i:02d}** [{l['verdict']}] (area: {l['area']}) {l['text']} Evidence: {l['evidence']}." + (f" DEV: {l['dev']}" if l.get("dev") else "") + "\n"
    if not a.get("lessons"):
        s += "- Not applicable: no lesson beyond the generic ones in [_index.md](_index.md).\n"
    s += "\n## 19. Open questions / UNVERIFIED items\n\n" + (a.get("open") or "- `UNVERIFIED`: per-cmdlet behavior (out of scope).") + "\n\n"
    shipped = ", ".join(f"`{x}`" for x in xml) or "none in the project folder"
    s += f"**Shipped type/format XML (project folder):** {shipped}. **Resource files:** " + (", ".join(f"`{os.path.basename(k)}` ({v['key_count']} keys)" for k, v in sorted(res.items())) or "none (neutral)") + ".\n\n"
    s += f"Verification: inventory from `data/cmdlets.json` filtered by project (`{proj}`); manifests parsed from `src/Modules/**/*.psd1`; counts reconcile with `numbers.json` key CMDLET_CLASSES for the whole tree.\n"
    open(os.path.join(OUT, "10-command-modules", stem + ".md"), "w", encoding="utf-8").write(s)
    return len(cm), len(pv), did, stem, scope


def main():
    os.makedirs(os.path.join(OUT, "10-command-modules"), exist_ok=True)
    rows = []
    for a in ASSEMBLIES:
        if a[0] in projects:
            rows.append(gen(*a))
    idx = fm("CMD-INDEX-001", "Command module families", "catalog", "C", "EXTENDED", gen=["data/cmdlets.json"]) + "\n# Command module families\n\n" + BANNER
    idx += "| Assembly | Cmdlets | Providers | Scope class | Document |\n|---|---:|---:|---|---|\n"
    for nc, npv, did, stem, scope in rows:
        idx += f"| `{stem}` | {nc} | {npv} | {scope} | [{did}]({stem}.md) |\n"
    idx += "\nCmdlet totals: <!--N:CMDLET_CLASSES-->?<!--/N--> cmdlet classes and <!--N:PROVIDER_CLASSES-->?<!--/N--> provider classes in the tree (includes classes in test tools and samples that are not part of the product: `data/cmdlets.json` rows with project `(none)`, `Microsoft.PowerShell.NamedPipeConnection`, `Test.Isolated.*`).\n\n## Registration summary (`FACT-SRC`)\n\n- Engine-hosted cmdlets and providers are registered through static tables in `src/System.Management.Automation/engine/InitialSessionState.cs`; `InitialSessionState.CreateDefault2()` loads only the core snap-in plus built-in variables, functions and aliases and leaves the other cmdlets to modules (doc comment: \"The default cmdlets, provider, etc are loaded via Modules\").\n- Every other assembly is loaded through a module manifest under `src/Modules/{Shared,Unix,Windows}` (`NestedModules = @(\"<Assembly>.dll\")`), with separate manifests per platform because exported cmdlets differ (`src/Modules/README.md`).\n"
    open(os.path.join(OUT, "10-command-modules", "_index.md"), "w", encoding="utf-8").write(idx)
    print([(r[3], r[0], r[1]) for r in rows])


if __name__ == "__main__":
    main()
