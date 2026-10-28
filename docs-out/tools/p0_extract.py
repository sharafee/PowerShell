#!/usr/bin/env python3
"""p0_extract.py - Phase 0 mechanical extraction: files, tiers, projects, types, enums, #if symbols.

Purpose : produce docs-out/data/{files.csv, projects.json, types.json, members-tierA.json,
          enums.json, conditional-compilation.json} and docs-out/.work/{tiers.csv,files-ledger.csv}.
Inputs  : the repository working tree (REPO_ROOT = cwd or argv[1]).
Outputs : see Purpose. All C# structure output is APPROX (regex/lexer based, no Roslyn).
Run     : python3 docs-out/tools/p0_extract.py [REPO_ROOT]
Language: Python 3 (no dotnet/pwsh available; DECISIONS.md D-002)
Tested  : Linux x86_64 / Python 3.13
"""
import csv
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import csscan  # noqa: E402

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
WORK = os.path.join(OUT, ".work")
SKIP_DIRS = {".git", "docs-out", "node_modules"}
SMA = "src/System.Management.Automation/"

LANG = {
    ".cs": "C#", ".ps1": "PowerShell", ".psm1": "PowerShell", ".psd1": "PowerShell-data", ".ps1xml": "ps1xml",
    ".resx": "resx", ".cpp": "C++", ".c": "C", ".h": "C/C++ header", ".hpp": "C/C++ header", ".cc": "C++",
    ".yml": "YAML", ".yaml": "YAML", ".json": "JSON", ".md": "Markdown", ".xml": "XML", ".csproj": "msbuild",
    ".props": "msbuild", ".targets": "msbuild", ".sln": "sln", ".txt": "text", ".sh": "shell", ".bat": "batch",
    ".cmd": "batch", ".xsd": "XSD", ".mof": "MOF", ".psrc": "PowerShell-data", ".pssc": "PowerShell-data",
    ".py": "Python", ".js": "JavaScript", ".html": "HTML", ".cmake": "CMake", ".def": "def", ".rc": "rc",
    ".man": "ETW manifest", ".wxs": "WiX", ".wxl": "WiX", ".config": "XML", ".ruleset": "XML", ".svg": "image",
    ".png": "image", ".ico": "image", ".jpg": "image", ".gif": "image",
}
TEXT_EXT = {k for k, v in LANG.items() if v not in ("image",)}

# --- Tier A: language core (section 4.1). Paths relative to repo root; prefix match.
TIER_A = [
    SMA + "engine/parser/", SMA + "engine/runtime/", SMA + "engine/interpreter/", SMA + "engine/lang/",
    SMA + "engine/LanguagePrimitives.cs", SMA + "engine/ParameterBinderBase.cs", SMA + "engine/ParameterBinderController.cs",
    SMA + "engine/CmdletParameterBinderController.cs", SMA + "engine/NativeCommandParameterBinder.cs",
    SMA + "engine/NativeCommandParameterBinderController.cs", SMA + "engine/ReflectionParameterBinder.cs",
    SMA + "engine/PseudoParameterBinder.cs", SMA + "engine/MinishellParameterBinderController.cs",
    SMA + "engine/scriptparameterbinder.cs", SMA + "engine/scriptparameterbindercontroller.cs",
    SMA + "engine/CommandProcessor.cs", SMA + "engine/CommandProcessorBase.cs", SMA + "engine/ScriptCommandProcessor.cs",
    SMA + "engine/NativeCommandProcessor.cs", SMA + "engine/SessionStateScope.cs", SMA + "engine/SessionStateScopeAPIs.cs",
    SMA + "engine/SessionStateScopeEnumerator.cs", SMA + "engine/ScopedItemSearcher.cs", SMA + "engine/ShellVariable.cs",
    SMA + "engine/SpecialVariables.cs", SMA + "engine/VariablePath.cs", SMA + "engine/SessionStateVariableAPIs.cs",
    SMA + "engine/VariableAttributeCollection.cs", SMA + "engine/VariableInterfaces.cs", SMA + "engine/ScriptCommand.cs",
    SMA + "engine/CommandSearcher.cs", SMA + "engine/CommandDiscovery.cs", SMA + "engine/Pipe.cs",
    SMA + "engine/pipeline.cs", SMA + "engine/MergedCommandParameterMetadata.cs", SMA + "engine/CompiledCommandParameter.cs",
    SMA + "engine/CommandMetadata.cs", SMA + "engine/ExecutionContext.cs",
]
TIER_B_PREFIX = [SMA, "src/Microsoft.PowerShell.ConsoleHost/", "src/Microsoft.PowerShell.Security/", "src/Microsoft.PowerShell.SDK/"]
TIER_C_PREFIX = ["src/Microsoft.PowerShell.Commands.", "src/Microsoft.WSMan", "src/Microsoft.Management", "src/libpsl-native/",
                 "src/powershell-native/", "src/Modules/", "src/ResGen/", "src/TypeCatalogGen/", "src/GlobalTools/", "src/powershell-",
                 "src/Microsoft.PowerShell.CoreCLR", "src/Microsoft.PowerShell.GlobalTool", "src/PowerShell.Core.Instrumentation",
                 "src/Schemas/", "src/signing/", "src/powershell/"]


def tier_of(rel):
    for p in TIER_A:
        if rel.startswith(p):
            return "A"
    if rel.startswith("src/") and rel.endswith(".cs"):
        for p in TIER_C_PREFIX:
            if rel.startswith(p):
                return "C"
        for p in TIER_B_PREFIX:
            if rel.startswith(p):
                return "B"
    if rel.startswith(SMA):
        return "B"
    if rel.startswith("src/"):
        return "B" if rel.endswith((".cs", ".ps1xml", ".resx")) else "C"
    return "C"


def walk():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = sorted(d for d in dn if d not in SKIP_DIRS)
        for f in sorted(fn):
            full = os.path.join(dp, f)
            if os.path.islink(full):
                continue
            yield os.path.relpath(full, ROOT).replace(os.sep, "/")


def count_loc(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return 0
    if b"\0" in data[:4096]:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1)


def strip_ns(el):
    for e in el.iter():
        if isinstance(e.tag, str) and "}" in e.tag:
            e.tag = e.tag.split("}", 1)[1]
    return el


def load_props(path, seen=None):
    """collect properties of a props/csproj, following <Import Project> that exist on disk."""
    seen = seen or set()
    props = {}
    if path in seen or not os.path.exists(path):
        return props
    seen.add(path)
    try:
        root = strip_ns(ET.parse(path).getroot())
    except ET.ParseError:
        return props
    for imp in root.iter("Import"):
        proj = imp.get("Project", "")
        if "$(" in proj:
            continue
        ip = os.path.normpath(os.path.join(os.path.dirname(path), proj.replace("\\", "/")))
        for k, v in load_props(ip, seen).items():
            props.setdefault(k, v)
    for pg in root.iter("PropertyGroup"):
        cond = pg.get("Condition")
        for e in pg:
            if isinstance(e.tag, str) and e.text and e.text.strip():
                key = e.tag + (f" [if {cond or e.get('Condition')}]" if (cond or e.get("Condition")) else "")
                props[key] = e.text.strip()
    return props


def parse_sln(path):
    projs = set()
    if os.path.exists(path):
        for line in open(path, encoding="utf-8-sig", errors="replace"):
            m = re.match(r'Project\("\{[^}]+\}"\) = "([^"]+)", "([^"]+)"', line)
            if m and m.group(2).endswith("proj"):
                projs.add(os.path.normpath(m.group(2).replace("\\", "/")).replace(os.sep, "/"))
    return projs


def parse_projects(files):
    sln = parse_sln(os.path.join(ROOT, "PowerShell.sln"))
    res = []
    for rel in files:
        if not rel.endswith(".csproj"):
            continue
        full = os.path.join(ROOT, rel)
        root = strip_ns(ET.parse(full).getroot())
        props = load_props(full)
        p = {"path": rel, "name": os.path.basename(rel)[:-7], "in_solution": rel in sln, "sdk": root.get("Sdk")}
        pick = lambda k: next((v for kk, v in props.items() if kk == k), None)
        p["output_type"] = pick("OutputType")
        p["assembly_name"] = pick("AssemblyName") or p["name"]
        p["target_frameworks"] = pick("TargetFramework") or pick("TargetFrameworks")
        p["tfm_conditions"] = {k: v for k, v in props.items() if k.startswith(("TargetFramework", "OutputType"))}
        p["defines"] = {k: v for k, v in props.items() if k.startswith("DefineConstants")}
        p["root_namespace"] = pick("RootNamespace")
        pr, pk, ivt, removes, gens = [], [], [], [], []
        for ig in root.iter("ItemGroup"):
            gcond = ig.get("Condition")
            for it in ig:
                cond = it.get("Condition") or gcond
                if it.tag == "ProjectReference":
                    tgt = os.path.normpath(os.path.join(os.path.dirname(rel), it.get("Include", "").replace("\\", "/"))).replace(os.sep, "/")
                    pr.append({"path": tgt, "condition": cond, "analyzer": it.get("OutputItemType") == "Analyzer"})
                elif it.tag == "PackageReference":
                    pk.append({"name": it.get("Include") or it.get("Update"), "version": it.get("Version") or (it.findtext("Version")), "condition": cond})
                elif it.tag == "InternalsVisibleTo":
                    ivt.append(it.get("Include"))
                elif it.tag == "Compile" and it.get("Remove"):
                    removes.append({"remove": it.get("Remove"), "condition": cond})
        p["project_references"] = pr
        p["package_references"] = pk
        p["compile_removes"] = removes
        p["source_generators_analyzers"] = [x["path"] for x in pr if x["analyzer"]]
        # InternalsVisibleTo attributes in sources of this project
        pdir = os.path.dirname(rel)
        for dp, dn, fn in os.walk(os.path.join(ROOT, pdir)):
            dn[:] = [d for d in dn if d not in ("bin", "obj") and not os.path.exists(os.path.join(dp, d, d + ".csproj")) or os.path.join(dp, d) == os.path.join(ROOT, pdir)]
            for f in fn:
                if f.endswith(".cs") and f in ("AssemblyInfo.cs", "AssemblyAttributes.cs"):
                    txt = open(os.path.join(dp, f), encoding="utf-8-sig", errors="replace").read()
                    ivt += re.findall(r'InternalsVisibleTo\("([^"]+)"', txt)
        p["internals_visible_to"] = sorted(set(x for x in ivt if x))
        p["label"] = "GENERATED (XML parse; MSBuild conditions unevaluated)"
        res.append(p)
    return res


def owning_project(rel, proj_dirs):
    d = os.path.dirname(rel)
    while True:
        if d in proj_dirs:
            return proj_dirs[d]
        if not d:
            return "(none)"
        d = os.path.dirname(d)


def main():
    os.makedirs(DATA, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    files = list(walk())
    projects = parse_projects(files)
    proj_dirs = {os.path.dirname(p["path"]): p["name"] for p in projects}
    # files.csv / tiers.csv / ledger
    rows = []
    for rel in files:
        ext = os.path.splitext(rel)[1].lower()
        lang = LANG.get(ext, "other")
        loc = count_loc(os.path.join(ROOT, rel)) if ext in TEXT_EXT or ext == "" else 0
        gen = bool(re.search(r"\.Generated\.cs$|/gen/|\.g\.cs$|/obj/", rel))
        rows.append({"path": rel, "language": lang, "loc": loc, "tier": tier_of(rel), "project": owning_project(rel, proj_dirs), "generated": gen})
    with open(os.path.join(DATA, "files.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(WORK, "tiers.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["path", "tier"])
        for r in rows:
            if r["language"] == "C#" or r["path"].startswith("src/"):
                w.writerow([r["path"], r["tier"]])
    with open(os.path.join(WORK, "files-ledger.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["path", "loc", "tier", "ranges_read", "doc_ids", "status"])
        for r in rows:
            if r["language"] == "C#" or (r["path"].startswith("src/") and r["language"] in ("PowerShell", "ps1xml", "resx", "C++", "C", "C/C++ header")):
                w.writerow([r["path"], r["loc"], r["tier"], "", "", "unread"])
    # projects.json: add file/LOC aggregates
    agg = defaultdict(lambda: {"cs_files": 0, "cs_loc": 0})
    for r in rows:
        if r["language"] == "C#":
            a = agg[r["project"]]
            a["cs_files"] += 1
            a["cs_loc"] += r["loc"]
    for p in projects:
        p.update(agg.get(p["name"], {"cs_files": 0, "cs_loc": 0}))
    json.dump(projects, open(os.path.join(DATA, "projects.json"), "w"), indent=1)

    # C# structure
    types, enums, cond_syms, members_a, parse_fail = [], [], defaultdict(lambda: {"files": set(), "types": set()}), [], []
    by_full = defaultdict(list)
    cs_rows = [r for r in rows if r["language"] == "C#"]
    for r in cs_rows:
        try:
            sc = csscan.scan_file(os.path.join(ROOT, r["path"]))
        except Exception as e:  # noqa
            parse_fail.append({"path": r["path"], "error": repr(e)})
            continue
        for sym in sc["directives"]:
            for s in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", sym):
                if s not in ("true", "false"):
                    cond_syms[s]["files"].add(r["path"])
        stack = {}
        for t in sc["types"]:
            ident = t.get("ident") or t["name"]
            full = t.get("full") or ((t["namespace"] + ".") if t["namespace"] else "") + t["name"]
            mc = defaultdict(int)
            for m in t["members"]:
                mc[m["kind"]] += 1
            rec = {
                "kind": t["kind"], "name": t["name"], "full_name": full, "namespace": t["namespace"], "parent": t.get("parent"),
                "project": r["project"], "file": r["path"], "start": t["start"], "end": t["end"],
                "accessibility": next((m for m in t["modifiers"] if m in csscan.ACCESS), "internal" if not t.get("parent") else "private"),
                "modifiers": t["modifiers"], "bases": t["bases"], "attributes": t["attributes"], "cond": t["cond"],
                "member_counts": dict(mc), "tier": r["tier"], "generated": r["generated"],
            }
            if "partial" in t["modifiers"]:
                rec["partial"] = True
            types.append(rec)
            by_full[(r["project"], full)].append(rec)
            for c in t["cond"]:
                for s in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", c):
                    cond_syms[s]["types"].add(full)
            if t["kind"] == "enum":
                enums.append({"full_name": full, "namespace": t["namespace"], "project": r["project"], "file": r["path"], "start": t["start"], "end": t["end"],
                              "accessibility": rec["accessibility"], "attributes": t["attributes"], "cond": t["cond"],
                              "members": t.get("enum_members", [])})
            if r["tier"] == "A" and t["members"]:
                members_a.append({"full_name": full, "file": r["path"], "kind": t["kind"], "members": [
                    {"kind": m["kind"], "name": m["name"], "access": m["access"], "modifiers": m["modifiers"], "start": m["start"], "end": m["end"],
                     "returns": m.get("returns"), "sig": m.get("sig"), "attributes": m["attributes"], "cond": m["cond"]} for m in t["members"]]})
    for (proj, full), lst in by_full.items():
        if len(lst) > 1:
            files_ = sorted({x["file"] for x in lst})
            for x in lst:
                x["partial_files"] = files_
    json.dump(types, open(os.path.join(DATA, "types.json"), "w"), indent=0)
    json.dump(members_a, open(os.path.join(DATA, "members-tierA.json"), "w"), indent=0)
    json.dump(enums, open(os.path.join(DATA, "enums.json"), "w"), indent=0)
    json.dump({k: {"files": sorted(v["files"]), "types": sorted(v["types"])} for k, v in sorted(cond_syms.items())},
              open(os.path.join(DATA, "conditional-compilation.json"), "w"), indent=0)
    json.dump(parse_fail, open(os.path.join(WORK, "scan-failures.json"), "w"), indent=1)
    print(f"files={len(rows)} projects={len(projects)} cs_files={len(cs_rows)} types={len(types)} enums={len(enums)} syms={len(cond_syms)} failures={len(parse_fail)}")


if __name__ == "__main__":
    main()
