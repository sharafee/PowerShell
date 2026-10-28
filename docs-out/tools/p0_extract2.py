#!/usr/bin/env python3
"""p0_extract2.py - Phase 0 datasets built on top of p0_extract.py output.

Purpose : ast-hierarchy.json, visitors.json, binders.json, instructions.json, cmdlets.json,
          resources.json, auto-variables.json, attributes.json, tests.json, tables.json,
          format-and-types-xml.json, parser-methods.json, enforcement-points.json (seed).
Inputs  : docs-out/data/types.json, files.csv and the source tree.
Outputs : docs-out/data/*.json (all APPROX / GENERATED-by-regex; no Roslyn available).
Run     : python3 docs-out/tools/p0_extract2.py [REPO_ROOT]   (run p0_extract.py first)
Language: Python 3 (D-002)   Tested: Linux x86_64 / Python 3.13
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
DATA = os.path.join(ROOT, "docs-out", "data")
SMA = "src/System.Management.Automation/"


def jload(n):
    return json.load(open(os.path.join(DATA, n)))


def jdump(n, obj):
    json.dump(obj, open(os.path.join(DATA, n), "w"), indent=1)


def short(n):
    return n.split(".")[-1].split("<")[0]


def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8-sig", errors="replace").read()


types = jload("types.json")
by_short = defaultdict(list)
for t in types:
    by_short[short(t["full_name"])].append(t)
children = defaultdict(list)
for t in types:
    for b in t["bases"]:
        children[short(b)].append(t)


def closure(base_short):
    seen, out, stack = set(), [], [base_short]
    while stack:
        b = stack.pop()
        for c in children.get(b, []):
            key = (c["full_name"], c["file"])
            if key in seen:
                continue
            seen.add(key)
            out.append(c)
            stack.append(short(c["full_name"]))
    return out


def chain(t):
    ch, cur, guard = [], t, 0
    while cur["bases"] and guard < 20:
        b = short(cur["bases"][0])
        ch.append(b)
        nxt = by_short.get(b)
        if not nxt:
            break
        cur = nxt[0]
        guard += 1
    return ch


# --------------------------------------------------------------------------- AST hierarchy
def ast_hierarchy():
    asts = [t for t in closure("Ast") if t["kind"] == "class"]
    parser_src = read(SMA + "engine/parser/Parser.cs")
    ctor_sites = defaultdict(list)
    cur_method = None
    p_scan = csscan.scan_file(os.path.join(ROOT, SMA + "engine/parser/Parser.cs"))
    methods = []
    for ty in p_scan["types"]:
        if ty.get("ident") == "Parser":
            methods = [m for m in ty["members"] if m["kind"] == "method"]
    lines = parser_src.split("\n")
    for t in asts:
        nm = short(t["full_name"])
        for i, ln in enumerate(lines, 1):
            if re.search(r"new\s+" + re.escape(nm) + r"\s*\(", ln):
                meth = next((m for m in methods if m["start"] <= i <= m["end"]), None)
                ctor_sites[nm].append({"method": meth["name"] if meth else None, "line": i})
    # child properties of AST type (ctor-param / property types) from source of the file
    out = []
    ast_names = {short(t["full_name"]) for t in asts} | {"Ast"}
    for t in sorted(asts, key=lambda x: (x["file"], x["start"])):
        nm = short(t["full_name"])
        sc = None
        out.append({
            "name": t["full_name"], "file": t["file"], "start": t["start"], "end": t["end"],
            "base_chain": chain(t), "modifiers": t["modifiers"], "accessibility": t["accessibility"], "cond": t["cond"],
            "created_by_parser": ctor_sites.get(nm, []), "label": "APPROX",
        })
    # AST-typed members (children): scan members of each ast type for property/field types that are Ast types
    scan = {}
    for rel in sorted({o["file"] for o in out}):
        scan[rel] = csscan.scan_file(os.path.join(ROOT, rel))
    for o in out:
        sc = scan[o["file"]]
        ty = next((x for x in sc["types"] if x.get("full") == o["name"] and x["start"] == o["start"]), None)
        kids = []
        if ty:
            for m in ty["members"]:
                if m["kind"] in ("property", "field") and m["access"] in ("public", "internal", None):
                    sig = m.get("sig", "")
                    if any(re.search(r"\b" + a + r"\b", sig) for a in ast_names) or "ReadOnlyCollection" in sig and "Ast" in sig:
                        kids.append({"name": m["name"], "sig": sig[:160], "line": m["start"]})
        o["ast_typed_members"] = kids
    return out


# --------------------------------------------------------------------------- visitors / binders / instructions
def impl_closure(bases):
    res = {}
    for b in bases:
        for c in children.get(b, []):
            res[(c["full_name"], c["file"])] = c
        for c in closure(b):
            res[(c["full_name"], c["file"])] = c
    return list(res.values())


def visitors():
    ims = impl_closure(["ICustomAstVisitor", "ICustomAstVisitor2", "AstVisitor", "AstVisitor2", "ICustomAstVisitor3"])
    out = []
    for t in ims:
        if t["kind"] != "class":
            continue
        sc = csscan.scan_file(os.path.join(ROOT, t["file"]))
        ty = next((x for x in sc["types"] if x.get("full") == t["full_name"] and x["start"] == t["start"]), None)
        visits = sorted({m["name"] for m in (ty["members"] if ty else []) if m["kind"] == "method" and m["name"].startswith("Visit")})
        out.append({"name": t["full_name"], "file": t["file"], "start": t["start"], "end": t["end"], "bases": t["bases"],
                    "visit_methods": visits, "visit_method_count": len(visits), "label": "APPROX"})
    # interfaces / base visitor types themselves
    for nm in ("ICustomAstVisitor", "ICustomAstVisitor2", "AstVisitor", "AstVisitor2"):
        for t in by_short.get(nm, []):
            sc = csscan.scan_file(os.path.join(ROOT, t["file"]))
            ty = next((x for x in sc["types"] if x.get("full") == t["full_name"] and x["start"] == t["start"]), None)
            visits = sorted({m["name"] for m in (ty["members"] if ty else []) if m["kind"] == "method" and m["name"].startswith("Visit")})
            out.append({"name": t["full_name"], "file": t["file"], "start": t["start"], "end": t["end"], "bases": t["bases"],
                        "visit_methods": visits, "visit_method_count": len(visits), "role": "visitor interface/base", "label": "APPROX"})
    return sorted(out, key=lambda x: x["name"])


def binders():
    bs = impl_closure(["DynamicMetaObjectBinder", "CallSiteBinder", "ILightCallSiteBinder", "InvokeBinder", "GetMemberBinder", "SetMemberBinder",
                       "InvokeMemberBinder", "BinaryOperationBinder", "UnaryOperationBinder", "ConvertBinder", "GetIndexBinder", "SetIndexBinder",
                       "CreateInstanceBinder", "DeleteMemberBinder", "DeleteIndexBinder", "PSInvokeMemberBinder"])
    out = []
    for t in bs:
        if t["kind"] != "class":
            continue
        nm = short(t["full_name"])
        sites = []
        pat = re.compile(r"\b" + re.escape(nm) + r"\.Get\w*\(|new\s+" + re.escape(nm) + r"\s*\(")
        for dp, dn, fn in os.walk(os.path.join(ROOT, "src")):
            for f in fn:
                if f.endswith(".cs") and not f.endswith(".Generated.cs"):
                    rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
                    if rel.startswith(SMA):
                        txt = read(rel)
                        for m in pat.finditer(txt):
                            sites.append({"file": rel, "line": txt.count("\n", 0, m.start()) + 1})
        out.append({"name": t["full_name"], "file": t["file"], "start": t["start"], "end": t["end"], "bases": t["bases"],
                    "chain": chain(t), "created_or_obtained_at": sites[:25], "site_count": len(sites), "label": "APPROX"})
    return sorted(out, key=lambda x: (x["file"], x["start"]))


def instructions():
    ins = [t for t in closure("Instruction") if t["kind"] == "class"]
    out = []
    for t in sorted(ins, key=lambda x: (x["file"], x["start"])):
        out.append({"name": t["full_name"], "file": t["file"], "start": t["start"], "end": t["end"], "chain": chain(t),
                    "modifiers": t["modifiers"], "label": "APPROX"})
    return out


# --------------------------------------------------------------------------- cmdlets / providers
def cmdlets():
    out = []
    for t in types:
        if t["kind"] != "class":
            continue
        attrs = t["attributes"]
        if "Cmdlet" in attrs or "CmdletProvider" in attrs:
            src = read(t["file"]).split("\n")
            # find the attribute text by scanning backwards from class line
            i = t["start"] - 1
            blob = []
            j = i
            while j >= 0 and j > i - 40:
                blob.insert(0, src[j])
                if re.match(r"\s*(//|/\*|\*)", src[j]) is None and re.search(r"\}\s*$|;\s*$", src[j]) and j != i:
                    break
                j -= 1
            text = " ".join(blob)
            m = re.search(r"\[(?:Cmdlet|CmdletProvider)\(\s*([^,\)]+)(?:,\s*([^,\)]+?))?\s*[,\)]", text)
            rec = {"class": t["full_name"], "file": t["file"], "start": t["start"], "project": t["project"], "bases": t["bases"],
                   "kind": "provider" if "CmdletProvider" in attrs else "cmdlet", "attributes": attrs, "cond": t["cond"]}
            if m:
                rec["verb_expr"] = m.group(1).strip()
                rec["noun_expr"] = m.group(2).strip() if m.group(2) else None
            ps = re.search(r"DefaultParameterSetName\s*=\s*([^,\)]+)", text)
            rec["default_parameter_set"] = ps.group(1).strip() if ps else None
            rec["supports_should_process"] = "SupportsShouldProcess = true" in text
            rec["has_dynamic_parameters"] = False
            body = "\n".join(src[t["start"] - 1:t["end"]])
            rec["parameter_attribute_count"] = len(re.findall(r"\[\s*Parameter\b", body))
            rec["parameter_sets"] = sorted(set(re.findall(r"ParameterSetName\s*=\s*([\w\.\"]+)", body)))
            rec["has_dynamic_parameters"] = "IDynamicParameters" in " ".join(t["bases"]) or "GetDynamicParameters" in body
            rec["lifecycle_overrides"] = sorted(set(re.findall(r"override\s+void\s+(BeginProcessing|ProcessRecord|EndProcessing|StopProcessing|Dispose|CleanProcessing)\s*\(", body)))
            out.append(rec)
    # unresolved classes deriving from Cmdlet/PSCmdlet without attribute (base classes)
    return out


# --------------------------------------------------------------------------- resources
CULTURES = {"cs", "de", "es", "fr", "it", "ja", "ko", "pl", "pt-BR", "ru", "tr", "zh-Hans", "zh-Hant"}


def resources():
    """neutral (non-localized) .resx only; localized copies are counted in numbers.json."""
    res = {}
    rdir = SMA + "resources"
    resx_files = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "src")):
        for f in fn:
            if f.endswith(".resx") and os.path.basename(dp) not in CULTURES:
                resx_files.append(os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/"))
    # usage index: class name -> pattern "ParserStrings.Key"
    cs_texts = {}
    for dp, dn, fn in os.walk(os.path.join(ROOT, "src")):
        for f in fn:
            if f.endswith(".cs"):
                rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
                cs_texts[rel] = read(rel)
    for rx in sorted(resx_files):
        cls = os.path.basename(rx)[:-5]
        try:
            root = ET.parse(os.path.join(ROOT, rx)).getroot()
        except ET.ParseError:
            continue
        keys = []
        for d in root.findall("data"):
            nm = d.get("name")
            if nm is None or d.get("mimetype"):
                continue
            keys.append(nm)
        usage = defaultdict(list)
        pat = re.compile(r"\b" + re.escape(cls) + r"\.(\w+)")
        for rel, txt in cs_texts.items():
            if cls not in txt:
                continue
            for m in pat.finditer(txt):
                usage[m.group(1)].append({"file": rel, "line": txt.count("\n", 0, m.start()) + 1})
        res[rx] = {"class": cls, "key_count": len(keys), "keys": [
            {"key": k, "uses": usage.get(k, [])[:6], "use_count": len(usage.get(k, []))} for k in keys]}
    return res


# --------------------------------------------------------------------------- automatic variables
def auto_variables():
    txt = read(SMA + "engine/SpecialVariables.cs")
    consts = []
    for m in re.finditer(r"internal\s+const\s+string\s+(\w+)\s*=\s*\"([^\"]*)\"", txt):
        consts.append({"field": m.group(1), "name": m.group(2), "line": txt.count("\n", 0, m.start()) + 1})
    # writer sites: SpecialVariables.<Field>VarPath or ...<Field> used in SetVariable-like calls
    cs = {}
    for dp, dn, fn in os.walk(os.path.join(ROOT, "src")):
        for f in fn:
            if f.endswith(".cs"):
                rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
                if rel.startswith(SMA) or rel.startswith("src/Microsoft.PowerShell.ConsoleHost"):
                    cs[rel] = read(rel)
    for c in consts:
        sites = []
        pat = re.compile(r"SpecialVariables\." + re.escape(c["field"]) + r"(VarPath)?\b")
        for rel, t in cs.items():
            for m in pat.finditer(t):
                ln = t.count("\n", 0, m.start()) + 1
                line = t.split("\n")[ln - 1].strip()
                kind = "write?" if re.search(r"(Set|New|Add|Update|Assign)\w*Variable|SetValue|\.Value\s*=|new PSVariable|PSNoteProperty", line) else "ref"
                sites.append({"file": rel, "line": ln, "kind": kind})
        c["reference_count"] = len(sites)
        c["write_candidate_sites"] = [s for s in sites if s["kind"] == "write?"][:15]
        c["label"] = "APPROX"
    # lists of automatic/preference variables (arrays in SpecialVariables)
    arrays = []
    for m in re.finditer(r"internal\s+static\s+readonly\s+(string\[\]|Type\[\]|VariablePath\[\])\s+(\w+)\s*=\s*new[^{]*\{(.*?)\};", txt, re.S):
        arrays.append({"field": m.group(2), "type": m.group(1), "entries": re.findall(r"[\w\.]+", m.group(3))[:200],
                       "line": txt.count("\n", 0, m.start()) + 1})
    return {"source": SMA + "engine/SpecialVariables.cs", "constants": consts, "arrays": arrays}


# --------------------------------------------------------------------------- attributes
def attributes():
    atypes = [t for t in closure("Attribute") if t["kind"] == "class"]
    out = []
    for t in sorted(atypes, key=lambda x: (x["project"], x["full_name"])):
        out.append({"name": t["full_name"], "file": t["file"], "start": t["start"], "bases": t["bases"],
                    "chain": chain(t), "attributes": t["attributes"], "project": t["project"], "label": "APPROX"})
    # enforcement: where each attribute type is referenced inside engine
    return out


# --------------------------------------------------------------------------- tests
def tests():
    out = {"pester": [], "xunit": [], "other": []}
    sys.stderr.write("tests: scanning\n")
    for dp, dn, fn in os.walk(os.path.join(ROOT, "test")):
        for f in fn:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
            if f.endswith(".Tests.ps1"):
                txt = open(full, encoding="utf-8-sig", errors="replace").read()
                tree = []
                for m in re.finditer(r"^\s*(Describe|Context|It)\s+(['\"])(.*?)\2([^\n]*)", txt, re.M | re.I):
                    kind, name, rest = m.group(1).capitalize(), m.group(3), m.group(4)
                    tags = re.findall(r"-Tag\s+(?:@\()?([^\)\n{]+)", rest, re.I)
                    tree.append({"kind": kind, "name": name, "line": txt.count("\n", 0, m.start()) + 1,
                                 "tags": [x.strip().strip("'\"") for t in tags for x in re.split(r"[,\s]+", t) if x.strip()]})
                tc = len(re.findall(r"-TestCases|-ForEach", txt))
                out["pester"].append({"path": rel, "describe": sum(1 for x in tree if x["kind"] == "Describe"), "context": sum(1 for x in tree if x["kind"] == "Context"),
                                      "it": sum(1 for x in tree if x["kind"] == "It"), "parameterized_blocks": tc, "tree": tree, "extraction": "regex (APPROX; no pwsh parser available)"})
            elif f.endswith(".cs") and rel.startswith("test/xUnit/"):
                txt = open(full, encoding="utf-8-sig", errors="replace").read()
                facts = len(re.findall(r"\[(?:Fact|Theory)\b", txt))
                cls = re.findall(r"\bclass\s+(\w+)", txt)
                out["xunit"].append({"path": rel, "classes": cls, "facts": facts, "theories": len(re.findall(r"\[Theory\b", txt)),
                                     "extraction": "regex (APPROX)"})
    for dp, dn, fn in os.walk(os.path.join(ROOT, "test")):
        for f in fn:
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")
            if f.endswith(".cs") and not rel.startswith("test/xUnit/"):
                out["other"].append({"path": rel, "kind": "C# test/tool source"})
    return out


# --------------------------------------------------------------------------- tables (keyword / operator / token text)
def tables():
    out = {}
    for rel, names in ((SMA + "engine/parser/tokenizer.cs", None), (SMA + "engine/parser/token.cs", None), (SMA + "engine/parser/CharTraits.cs", None),
                       (SMA + "engine/parser/Parser.cs", None), (SMA + "engine/parser/SemanticChecks.cs", None), (SMA + "engine/parser/Compiler.cs", None)):
        txt = read(rel)
        for m in re.finditer(r"(?:private|internal|public)\s+(?:static\s+)?(?:readonly\s+)?(?:const\s+)?([\w<>\[\], ]+?)\s+(\w+)\s*=\s*(?:new\s+[\w<>\[\], ]*\s*(?:\([^)]*\))?\s*)?\{", txt):
            start = m.end() - 1
            depth, i = 0, start
            while i < len(txt):
                if txt[i] == "{":
                    depth += 1
                elif txt[i] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                i += 1
            body = txt[start:i + 1]
            ty = m.group(1).strip()
            if not re.search(r"static|\[\]|Dictionary|HashSet|List", ty + txt[m.start():m.end()]):
                continue
            ln0 = txt.count("\n", 0, m.start()) + 1
            ln1 = txt.count("\n", 0, i) + 1
            if ln1 - ln0 > 600:
                continue
            out[f"{rel}::{m.group(2)}"] = {"type": ty, "file": rel, "start": ln0, "end": ln1, "text": body[:20000], "label": "FACT-SRC (verbatim text of the table)"}
    # CharTraits enum + token table are retained verbatim by the table text above
    return out


# --------------------------------------------------------------------------- ps1xml
def ps1xml():
    out = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "src")):
        for f in fn:
            if f.endswith(".ps1xml"):
                full = os.path.join(dp, f)
                rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
                try:
                    root = ET.parse(full).getroot()
                except ET.ParseError as e:
                    out.append({"path": rel, "error": str(e)})
                    continue
                rec = {"path": rel, "root": root.tag}
                if root.tag == "Types":
                    rec["types"] = [{"name": (t.findtext("Name") or "").strip(), "member_count": len(t.find("Members")) if t.find("Members") is not None else 0} for t in root.findall("Type")]
                elif root.tag == "Configuration":
                    views = []
                    for v in root.iter("View"):
                        views.append({"name": (v.findtext("Name") or "").strip(),
                                      "selected_types": [x.text for x in v.iter("TypeName")]})
                    rec["views"] = views
                out.append(rec)
    return out


# --------------------------------------------------------------------------- parser methods + production graph
def parser_methods():
    out = []
    for rel in (SMA + "engine/parser/Parser.cs", SMA + "engine/parser/tokenizer.cs"):
        sc = csscan.scan_file(os.path.join(ROOT, rel))
        txt = read(rel).split("\n")
        for ty in sc["types"]:
            ms = [m for m in ty["members"] if m["kind"] in ("method", "ctor")]
            names = {m["name"] for m in ms}
            for m in ms:
                body = "\n".join(txt[m["start"] - 1:m["end"]])
                calls = sorted({c for c in re.findall(r"\b(\w+)\s*\(", body) if c in names and c != m["name"]})
                out.append({"type": ty.get("full"), "file": rel, "method": m["name"], "start": m["start"], "end": m["end"], "access": m["access"],
                            "calls": calls, "label": "APPROX (name-based call extraction)"})
    return out


# --------------------------------------------------------------------------- enforcement-point seeds
SEEDS = [
    ("language-mode", r"LanguageMode\b"), ("language-mode", r"CheckRestrictedLanguage"), ("language-mode", r"CheckLanguageFeatures"),
    ("language-mode", r"PSLanguageMode\.(Constrained|NoLanguage|Restricted)"), ("amsi", r"AmsiUtils|AmsiNativeMethods|AmsiScanBuffer"),
    ("execution-policy", r"ExecutionPolicy"), ("signature", r"SignatureHelper|Authenticode|CatalogHelper|IsSignatureValid"),
    ("securestring", r"SecureString"), ("logging", r"ScriptBlockLogging|ModuleLogging|PSTranscript|Transcript"),
    ("app-control", r"SystemPolicy|WldpNativeMethods|AppLocker|WDAC"), ("jea", r"JEA|RoleCapabilit|SessionConfiguration|IsolatedMode"),
    ("trust-boundary", r"IsTrusted|SecurityZone|MarkOfTheWeb|Zone\.Identifier"),
    ("constrained-types", r"CoreTypes|IsAllowedForConstrained|TypeAccelerator"),
    ("remoting-deser", r"DeserializationLevel|AllowedTypes|InternalDeserializer"),
]


def enforcement_seeds():
    out = []
    files = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "src")):
        for f in fn:
            if f.endswith(".cs"):
                files.append(os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/"))
    ty_index = defaultdict(list)
    for t in types:
        ty_index[t["file"]].append(t)
    for rel in sorted(files):
        txt = read(rel)
        lines = txt.split("\n")
        for cat, pat in SEEDS:
            rx = re.compile(pat)
            for i, ln in enumerate(lines, 1):
                if rx.search(ln) and not ln.strip().startswith("//") and not ln.strip().startswith("///"):
                    owner = next((t for t in sorted(ty_index.get(rel, []), key=lambda x: x["end"] - x["start"]) if t["start"] <= i <= t["end"]), None)
                    out.append({"category": cat, "pattern": pat, "file": rel, "line": i, "type": owner["full_name"] if owner else None,
                                "text": ln.strip()[:200], "verified": False, "sec_enf_id": None, "label": "APPROX (seed; verified by reading in Phase 5)"})
    return out


def main():
    jdump("ast-hierarchy.json", ast_hierarchy())
    jdump("visitors.json", visitors())
    jdump("binders.json", binders())
    jdump("instructions.json", instructions())
    jdump("cmdlets.json", cmdlets())
    jdump("resources.json", resources())
    jdump("auto-variables.json", auto_variables())
    jdump("attributes.json", attributes())
    jdump("tests.json", tests())
    jdump("tables.json", tables())
    jdump("format-and-types-xml.json", ps1xml())
    jdump("parser-methods.json", parser_methods())
    jdump("enforcement-points.json", enforcement_seeds())
    for n in ("ast-hierarchy", "visitors", "binders", "instructions", "cmdlets", "attributes", "enforcement-points", "parser-methods"):
        print(n, len(jload(n + ".json")))
    print("resources", len(jload("resources.json")), "tests", {k: len(v) for k, v in jload("tests.json").items()}, "tables", len(jload("tables.json")))


if __name__ == "__main__":
    main()
