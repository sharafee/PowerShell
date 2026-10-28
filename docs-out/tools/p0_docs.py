#!/usr/bin/env python3
"""p0_docs.py - render Phase 0 documents and the src-mirror cards from data/.

Purpose : 00-overview/{repo-census,source-tree-map,project-dependency-graph}.md and
          src-mirror/**/_project.md + _folder.md (cards, section 8.2/8.3).
Inputs  : data/files.csv, projects.json, types.json, numbers.json, optional
          data/annotations/folder-purposes.json  {"<folder>": {"purpose": str, "files": {"<file>": "role"}, "docs": [links]}}
          data/annotations/project-purposes.json {"<Project>": {"purpose": str, "key_files": [[path, role]], "docs": [links]}}
Outputs : markdown files (GENERATED); cards are flagged ANNOTATED when an annotation exists.
Run     : python3 docs-out/tools/p0_docs.py
Language: Python 3 (D-002)   Tested: Linux x86_64 / Python 3.13
"""
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
PIN = json.load(open(os.path.join(OUT, ".work", "pin.json")))


def fm(id_, title, kind, tier, scope, sources=(), gen=(), cf=(), mirror=()):
    return f"""---
id: {id_}
title: {title}
kind: {kind}
tier: {tier}
status: draft
run_verification: none
scope_class: {scope}
version_pin: {PIN['version_pin']}
pin_method: "{PIN['pin_method'][:60]}"
canonical_facts: [{', '.join(cf)}]
sources: [{', '.join(sources)}]
mirror_cards: [{', '.join(mirror)}]
generated_from: [{', '.join(gen)}]
---
"""


BANNER = "> STATIC-ONLY — behavior not run-verified. All counts are `APPROX`/`GENERATED` from regex and own-scanner extraction (no .NET SDK on the study host).\n\n"

files = list(csv.DictReader(open(os.path.join(DATA, "files.csv"))))
projects = json.load(open(os.path.join(DATA, "projects.json")))
types = json.load(open(os.path.join(DATA, "types.json")))
nums = {e["key"]: e["value"] for e in json.load(open(os.path.join(DATA, "numbers.json")))}


def N(k):
    return f"<!--N:{k}-->{nums[k]}<!--/N-->"


def ann(name):
    p = os.path.join(DATA, "annotations", name)
    return json.load(open(p)) if os.path.exists(p) else {}


FOLDER_ANN = ann("folder-purposes.json")
PROJ_ANN = ann("project-purposes.json")


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(text)


# ------------------------------------------------------------------ repo census
def census():
    by_lang = defaultdict(lambda: [0, 0])
    for r in files:
        by_lang[r["language"]][0] += 1
        by_lang[r["language"]][1] += int(r["loc"])
    top = defaultdict(lambda: [0, 0, 0])
    for r in files:
        t = r["path"].split("/")[0] if "/" in r["path"] else "(root files)"
        top[t][0] += 1
        top[t][1] += int(r["loc"])
        if r["language"] == "C#":
            top[t][2] += int(r["loc"])
    s = fm("OV-CENSUS-001", "Repository census", "catalog", "C", "CORE", gen=["data/files.csv", "data/projects.json", "data/numbers.json"]) + "\n# Repository census\n\n" + BANNER
    s += f"Pinned at **{PIN['version_pin']}** (commit `{PIN['commit_short']}`). Total files: {N('REPO_FILES_TOTAL')}; C# files: {N('CS_FILES_ALL')} ({N('CS_FILES_SRC')} under `src/`); C# physical lines under `src/`: {N('CS_LOC_SRC')}; projects (`.csproj`): {N('PROJECT_COUNT')}, of which {N('PROJECTS_IN_SOLUTION')} are in `PowerShell.sln`.\n\n"
    s += "## Files and lines per language (`GENERATED`)\n\n| Language | Files | Lines |\n|---|---:|---:|\n"
    for l, (c, loc) in sorted(by_lang.items(), key=lambda x: -x[1][1]):
        s += f"| {l} | {c} | {loc} |\n"
    s += "\n## Top-level folders (`GENERATED`)\n\n| Folder | Files | Lines (all text) | C# lines |\n|---|---:|---:|---:|\n"
    for t, (c, loc, cs) in sorted(top.items(), key=lambda x: -x[1][1]):
        s += f"| `{t}` | {c} | {loc} | {cs} |\n"
    s += "\n## C# lines per project (`GENERATED`)\n\n| Project | In solution | C# files | C# lines | Tier mix |\n|---|---|---:|---:|---|\n"
    tier_mix = defaultdict(Counter)
    for r in files:
        if r["language"] == "C#":
            tier_mix[r["project"]][r["tier"]] += 1
    for p in sorted(projects, key=lambda x: -x["cs_loc"]):
        mix = ", ".join(f"{k}:{v}" for k, v in sorted(tier_mix[p["name"]].items()))
        s += f"| `{p['name']}` | {'yes' if p['in_solution'] else 'no'} | {p['cs_files']} | {p['cs_loc']} | {mix} |\n"
    s += "\n## Tier assignment (section 4.1)\n\nTier A files: " + N("CS_FILES_TIER_A") + " files / " + N("CS_LOC_TIER_A") + " lines; Tier B: " + N("CS_FILES_TIER_B") + " files; Tier C: " + N("CS_FILES_TIER_C") + " files (C# only). Per-file assignment: `.work/tiers.csv`.\n\nVerification: counts produced by `tools/p0_extract.py`; regenerate with `python3 docs-out/tools/p0_extract.py && python3 docs-out/tools/numbers.py gen`.\n"
    write("00-overview/repo-census.md", s)


# ------------------------------------------------------------------ dependency graph
def depgraph():
    name_by_path = {p["path"]: p["name"] for p in projects}
    s = fm("OV-DEPS-001", "Project dependency graph", "catalog", "C", "CORE", gen=["data/projects.json"]) + "\n# Project dependency graph\n\n" + BANNER
    s += "Edges are `ProjectReference` items (dashed = analyzer/source generator, label = MSBuild condition when present; conditions are **not evaluated**). Node suffix `*` = not in `PowerShell.sln`.\n\n"
    s += "```mermaid\nflowchart LR\n"
    ids = {p["name"]: re.sub(r"\W", "_", p["path"]) for p in projects}
    for p in projects:
        mark = "" if p["in_solution"] else "*"
        s += f'  {ids[p["name"]]}["{p["name"]}{mark}"]\n'
    for p in projects:
        for r in p["project_references"]:
            tgt = name_by_path.get(r["path"])
            if not tgt:
                continue
            arrow = "-.->" if r["analyzer"] else "-->"
            lab = f'|"{r["condition"][:40].replace(chr(34), chr(39))}"|' if r["condition"] else ""
            s += f"  {ids[p['name']]} {arrow}{lab} {ids[tgt]}\n"
    s += "```\n\n## Project table (`GENERATED`)\n\n| Project | Path | Output | TFM | In sln | Project refs | Package refs |\n|---|---|---|---|---|---:|---:|\n"
    for p in projects:
        s += f"| `{p['name']}` | `{p['path']}` | {p['output_type'] or '(inherited/Library)'} | {p['target_frameworks'] or 'inherited (see `PowerShell.Common.props`)'} | {'yes' if p['in_solution'] else 'no'} | {len(p['project_references'])} | {len(p['package_references'])} |\n"
    s += "\n## Package references (`GENERATED`)\n\n| Project | Package | Version | Condition |\n|---|---|---|---|\n"
    for p in projects:
        for k in p["package_references"]:
            s += f"| `{p['name']}` | {k['name']} | {k['version'] or ''} | {k['condition'] or ''} |\n"
    s += "\n## `InternalsVisibleTo` (`GENERATED`)\n\n"
    for p in projects:
        if p["internals_visible_to"]:
            s += f"- `{p['name']}`: " + ", ".join(f"`{x}`" for x in p["internals_visible_to"]) + "\n"
    s += "\nVerification: parsed with `xml.etree` from every `.csproj`; MSBuild property functions/conditions unevaluated.\n"
    write("00-overview/project-dependency-graph.md", s)


# ------------------------------------------------------------------ source tree map + folder cards
def folder_tables():
    folders = defaultdict(lambda: {"files": [], "subs": set()})
    for r in files:
        if r["language"] != "C#" and not (r["path"].startswith("src/") and r["language"] in ("PowerShell", "ps1xml", "resx", "C++", "C", "C/C++ header")):
            continue
        parts = r["path"].split("/")
        for i in range(1, len(parts)):
            d = "/".join(parts[:i])
            folders[d]["subs"].add("/".join(parts[:i + 1]) if i + 1 < len(parts) else None)
        folders["/".join(parts[:-1])]["files"].append(r)
    for d in folders:
        folders[d]["subs"].discard(None)
        folders[d]["subs"] = {s for s in folders[d]["subs"] if s in folders}
    return folders


def type_index():
    idx = defaultdict(list)
    for t in types:
        idx[t["file"]].append(t)
    return idx


def tree_map(folders):
    s = fm("OV-TREE-001", "Source tree map", "catalog", "C", "CORE", gen=["data/files.csv", "data/types.json"]) + "\n# Source tree map\n\n" + BANNER
    s += "Real folder tree (folders that contain source files or sub-folders with them): `files` = direct source files, `LOC` = direct lines, `types` = types declared directly. Mirrors `src-mirror/`.\n\n"
    tix = type_index()

    def rec_totals(d):
        f = len(folders[d]["files"])
        loc = sum(int(x["loc"]) for x in folders[d]["files"])
        ty = sum(len(tix[x["path"]]) for x in folders[d]["files"])
        for sd in folders[d]["subs"]:
            a, b, c = rec_totals(sd)
            f, loc, ty = f + a, loc + b, ty + c
        return f, loc, ty
    tot = {d: rec_totals(d) for d in folders}
    s += "| Folder | Files (rec.) | LOC (rec.) | Types (rec.) | Direct files |\n|---|---:|---:|---:|---:|\n"
    for d in sorted(folders):
        depth = d.count("/")
        if not (d.startswith(("src", "test", "tools"))):
            continue
        if depth > 6:
            continue
        f, loc, ty = tot[d]
        s += f"| {'&nbsp;&nbsp;' * depth}`{os.path.basename(d) if depth else d}` | {f} | {loc} | {ty} | {len(folders[d]['files'])} |\n"
    s += "\nVerification: folder list from `data/files.csv`; regenerated by `tools/p0_docs.py`.\n"
    write("00-overview/source-tree-map.md", s)
    return tot


def cards(folders, tot):
    tix = type_index()
    pn = {p["name"]: p for p in projects}
    # projects
    refd_by = defaultdict(list)
    name_by_path = {p["path"]: p["name"] for p in projects}
    for p in projects:
        for r in p["project_references"]:
            if r["path"] in name_by_path:
                refd_by[name_by_path[r["path"]]].append(p["name"])
    for p in projects:
        pdir = os.path.dirname(p["path"])
        a = PROJ_ANN.get(p["name"], {})
        s = f"# {p['name']}\n\n"
        s += f"| Path | OutputType | TFMs | Platforms | Assembly name | Defines | Tier |\n|---|---|---|---|---|---|---|\n"
        tmix = Counter(r["tier"] for r in files if r["project"] == p["name"] and r["language"] == "C#")
        defs = "; ".join(f"{k}={v}" for k, v in p["defines"].items()) or "(none in csproj)"
        s += f"| `{p['path']}` | {p['output_type'] or 'Library (default)'} | {p['target_frameworks'] or 'inherited'} | {'cross-platform (conditional items)' } | `{p['assembly_name']}` | {defs} | {', '.join(f'{k}:{v}' for k, v in sorted(tmix.items())) or '-'} |\n\n"
        s += "**Purpose.** " + (a.get("purpose") or f"_GENERATED stub — no annotation yet._ Project `{p['name']}` ({p['cs_files']} C# files, {p['cs_loc']} lines).") + "\n\n"
        s += "## Top-level folders\n\n| Folder | Files (rec.) | LOC (rec.) |\n|---|---:|---:|\n"
        for d in sorted(folders):
            if os.path.dirname(d) == pdir and d in tot:
                s += f"| [{os.path.basename(d)}]({os.path.basename(d)}/_folder.md) | {tot[d][0]} | {tot[d][1]} |\n"
        pt = [t for t in types if t["project"] == p["name"]]
        pub = [t for t in pt if t["accessibility"] == "public" and not t.get("parent")]
        s += f"\n## Public API surface (APPROX)\n\n{len(pt)} types, {len(pub)} public top-level types.\n\n"
        s += "## References\n\nProject refs: " + (", ".join(f"`{name_by_path.get(r['path'], r['path'])}`" for r in p["project_references"]) or "none") + "\n\n"
        s += "Packages: " + (", ".join(f"{k['name']} {k['version'] or ''}" for k in p["package_references"]) or "none") + "\n\n"
        s += "Referenced by: " + (", ".join(f"`{x}`" for x in sorted(refd_by.get(p["name"], []))) or "none") + "\n\n"
        s += "## Key files (top 10 by LOC unless annotated)\n\n| File | LOC | Role |\n|---|---:|---|\n"
        kf = a.get("key_files")
        if kf:
            for path, role in kf:
                s += f"| `{path}` | | {role} |\n"
        else:
            cands = sorted((r for r in files if r["project"] == p["name"] and r["language"] == "C#"), key=lambda r: -int(r["loc"]))[:10]
            for r in cands:
                s += f"| `{r['path']}` | {r['loc']} | _GENERATED_ |\n"
        s += "\n## Related documents\n\n" + ("\n".join(f"- {x}" for x in a.get("docs", [])) or "_none linked yet_") + "\n"
        root = "src-mirror/" + pdir
        write(f"{root}/_project.md", s)
    # folders
    for d, info in sorted(folders.items()):
        if d in ("src", "test", "tools") or not d.startswith(("src/", "test/", "tools/")):
            continue
        a = FOLDER_ANN.get(d, {})
        rows = sorted(info["files"], key=lambda r: r["path"])
        loc = sum(int(r["loc"]) for r in rows)
        ntypes = sum(len(tix[r["path"]]) for r in rows)
        tiers = Counter(r["tier"] for r in rows)
        flags = "ANNOTATED" if a else "GENERATED"
        s = f"# {d}\n\n| Tier | Project | File count | LOC | Type count | Flags |\n|---|---|---:|---:|---:|---|\n"
        proj = rows[0]["project"] if rows else (next(iter(info["subs"]), None) and "(see subfolders)")
        s += f"| {', '.join(f'{k}:{v}' for k, v in sorted(tiers.items())) or '-'} | {proj} | {len(rows)} | {loc} | {ntypes} | {flags} |\n\n"
        s += "**Purpose.** " + (a.get("purpose") or "_GENERATED stub — not annotated by reading._") + "\n\n"
        s += "## Files\n\n| File | LOC | Main types | Role | Covering document |\n|---|---:|---|---|---|\n"
        for r in rows:
            ts = [t for t in tix[r["path"]] if not t.get("parent")]
            main = ", ".join(f"`{t['name']}`" for t in sorted(ts, key=lambda t: -(t["end"] - t["start"]))[:4]) or "-"
            more = f" (+{len(ts) - 4})" if len(ts) > 4 else ""
            fname = os.path.basename(r["path"])
            s += f"| `{fname}` | {r['loc']} | {main}{more} | {a.get('files', {}).get(fname, '')} | {a.get('files_docs', {}).get(fname, '')} |\n"
        if info["subs"]:
            s += "\n## Subfolders\n\n" + "\n".join(f"- [{os.path.basename(x)}]({os.path.basename(x)}/_folder.md) ({tot[x][0]} files, {tot[x][1]} LOC)" for x in sorted(info["subs"])) + "\n"
        part = [(r["path"], t["full_name"]) for r in rows for t in tix[r["path"]] if t.get("partial_files") and len(t["partial_files"]) > 1 and not t.get("parent")]
        cond = sorted({c for r in rows for t in tix[r["path"]] for c in t["cond"]})
        s += "\n## Partial-class and conditional-compilation notes\n\n"
        s += ("Partial types spanning files: " + ", ".join(sorted({f"`{n.split('.')[-1]}`" for _, n in part})) + "\n\n") if part else "No partial types spanning files (APPROX).\n\n"
        s += ("`#if` conditions on types here: " + ", ".join(f"`{c}`" for c in cond[:20]) + "\n") if cond else "No conditionally-compiled types (APPROX).\n"
        s += "\n## Related documents\n\n" + ("\n".join(f"- {x}" for x in a.get("docs", [])) or "_none linked yet_") + "\n"
        write(f"src-mirror/{d}/_folder.md", s)


def main():
    census()
    depgraph()
    folders = folder_tables()
    tot = tree_map(folders)
    cards(folders, tot)
    n = sum(1 for dp, dn, fn in os.walk(os.path.join(OUT, "src-mirror")) for f in fn if f == "_folder.md")
    print("folder cards:", n)


if __name__ == "__main__":
    main()
