#!/usr/bin/env python3
"""consist.py - consistency tooling for gate 2 / gate 6 (one file, subcommands).

Purpose : render-canonical, check-claims, lint-terms, check-front-matter, check-status,
          validate-refs, check-links, idreg  (rules 3, 11, 18-21, 23; gates 1, 2, 6).
Inputs  : docs-out/**/*.md, data/canonical-facts.json, data/claims/*.jsonl, GLOSSARY.md,
          .work/pin.json, data/types.json, CONTRADICTIONS.md.
Outputs : stdout findings + exit code 1 on FAIL; `check-status --write` and `idreg` rewrite files.
Run     : python3 docs-out/tools/consist.py <render-canonical [--check]|check-claims|lint-terms|
          check-front-matter|check-status [--write]|validate-refs|check-links|idreg|all>
Language: Python 3 (D-002)   Tested: Linux x86_64 / Python 3.13
"""
import glob
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
PIN = json.load(open(os.path.join(OUT, ".work", "pin.json")))
SKIP = {".work", "tools", "data"}


def docs(include_cards=False):
    for dp, dn, fn in os.walk(OUT):
        dn[:] = [d for d in dn if d not in SKIP and (include_cards or d != "src-mirror")]
        for f in sorted(fn):
            if f.endswith(".md"):
                yield os.path.join(dp, f)


def rel(p):
    return os.path.relpath(p, OUT)


def split_fm(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            fm = {}
            for ln in text[4:end].split("\n"):
                m = re.match(r"^([A-Za-z_]+):\s*(.*)$", ln)
                if m:
                    fm[m.group(1)] = m.group(2).strip()
            return fm, text[end + 5:]
    return None, text


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


# ------------------------------------------------------------------ render-canonical
CFRE = re.compile(r"<!--CF:([A-Z]+-[A-Z]+-\d{3})-->(.*?)<!--/CF-->", re.S)


def render_canonical(check):
    cfs = {c["id"]: c for c in json.load(open(os.path.join(DATA, "canonical-facts.json")))}
    bad, n = [], 0
    for p in docs():
        t = open(p, encoding="utf-8").read()

        def sub(m):
            c = cfs.get(m.group(1))
            if not c:
                bad.append((rel(p), "unknown CF " + m.group(1)))
                return m.group(0)
            new = f"<!--CF:{c['id']}-->{c['statement']}<!--/CF-->"
            if new != m.group(0):
                bad.append((rel(p), f"divergent embed of {c['id']}"))
            return new
        t2 = CFRE.sub(sub, t)
        if not check and t2 != t:
            open(p, "w", encoding="utf-8").write(t2)
            n += 1
    if check:
        for b in bad:
            print("RENDER-CANONICAL FAIL", *b)
        print("render-canonical --check:", "FAIL" if bad else "PASS")
        return 1 if bad else 0
    print("render-canonical: rewrote", n)
    return 0


# ------------------------------------------------------------------ check-claims
def check_claims():
    groups = defaultdict(list)
    for f in glob.glob(os.path.join(DATA, "claims", "*.jsonl")):
        for i, ln in enumerate(open(f, encoding="utf-8"), 1):
            ln = ln.strip()
            if not ln:
                continue
            try:
                c = json.loads(ln)
            except json.JSONDecodeError:
                print("CHECK-CLAIMS FAIL bad json", f, i)
                return 1
            groups[(c.get("subject_key"), c.get("predicate"))].append((f, i, c))
    con = open(os.path.join(OUT, "CONTRADICTIONS.md"), encoding="utf-8").read() if os.path.exists(os.path.join(OUT, "CONTRADICTIONS.md")) else ""
    bad = 0
    for k, lst in groups.items():
        vals = {str(c["value"]) for _, _, c in lst}
        if len(vals) > 1:
            ids = [c["id"] for _, _, c in lst]
            resolved = any(re.search(r"CON-\d+.*RESOLVED", ln) and all(i in ln for i in ids[:2]) for ln in con.split("\n"))
            if not resolved:
                bad += 1
                print("CHECK-CLAIMS CONFLICT", k, sorted(vals)[:4], ids[:6])
    print("check-claims:", "FAIL" if bad else "PASS", f"{sum(len(v) for v in groups.values())} claims, {bad} conflicts")
    return 1 if bad else 0


# ------------------------------------------------------------------ lint-terms
def lint_terms():
    g = os.path.join(OUT, "GLOSSARY.md")
    forb = {}
    for ln in open(g, encoding="utf-8"):
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[2] and not cells[0].startswith(("---", "preferred")) and "forbidden" not in cells[0].lower():
            for w in re.split(r"[;,]", cells[2]):
                w = w.strip().strip("`").strip()
                if w and w not in ("-", "none", "—"):
                    forb[w.lower()] = cells[0]
    bad = 0
    for p in docs():
        if os.path.basename(p) == "GLOSSARY.md":
            continue
        _, body = split_fm(open(p, encoding="utf-8").read())
        text = strip_code(body)
        for w, pref in forb.items():
            for m in re.finditer(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", text, re.I):
                bad += 1
                print(f"LINT-TERMS FAIL {rel(p)}: forbidden '{w}' (use '{pref}')")
                break
    print("lint-terms:", "FAIL" if bad else "PASS", f"{len(forb)} forbidden synonyms, {bad} findings")
    return 1 if bad else 0


# ------------------------------------------------------------------ front matter / status
REQ = ["id", "title", "kind", "tier", "status", "run_verification", "scope_class", "version_pin", "pin_method", "canonical_facts", "sources", "mirror_cards", "generated_from"]


def check_front_matter():
    bad = 0
    ids = {}
    for p in docs():
        fm, _ = split_fm(open(p, encoding="utf-8").read())
        if p.endswith(("README.md",)) and fm is None and os.path.dirname(p) == OUT:
            continue
        if fm is None:
            if os.path.basename(p) in ("GLOSSARY.md", "DECISIONS.md", "PROGRESS.md", "BLOCKED.md", "VERIFICATION-BACKLOG.md", "CONTRADICTIONS.md",
                                       "ID-REGISTRY.md", "COVERAGE.md", "TRACEABILITY.md", "CANONICAL-FACTS.md", "FEATURE-MATRIX.md", "ACCEPTANCE-QUESTIONS.md", "README.md"):
                continue
            print("CHECK-FM FAIL no front matter:", rel(p))
            bad += 1
            continue
        for k in REQ:
            if k not in fm:
                print(f"CHECK-FM FAIL {rel(p)}: missing {k}")
                bad += 1
        if fm.get("version_pin") != PIN["version_pin"]:
            print(f"CHECK-FM FAIL {rel(p)}: version_pin {fm.get('version_pin')}")
            bad += 1
        if fm.get("pin_method", "").strip('"') != PIN["pin_method"][:60]:
            print(f"CHECK-FM FAIL {rel(p)}: pin_method differs from .work/pin.json")
            bad += 1
        if "id" in fm:
            if fm["id"] in ids:
                print(f"CHECK-FM FAIL duplicate id {fm['id']}: {rel(p)} / {ids[fm['id']]}")
                bad += 1
            ids[fm["id"]] = rel(p)
        if fm.get("scope_class") not in ("CORE", "EXTENDED", "OUT-OF-SCOPE-DOCUMENTED"):
            print(f"CHECK-FM FAIL {rel(p)}: scope_class {fm.get('scope_class')}")
            bad += 1
    print("check-front-matter:", "FAIL" if bad else "PASS", f"{len(ids)} documents, {bad} findings")
    return 1 if bad else 0


def compute_status(fm, body):
    cfs = {c["id"]: c for c in json.load(open(os.path.join(DATA, "canonical-facts.json")))}
    text = strip_code(body)
    flags = []
    if re.search(r"\bTODO\b|<!--DRAFT-->", body):
        return "draft", ["TODO/DRAFT marker"]
    for lab in ("UNVERIFIED", "APPROX", "BLOCKED"):
        if re.search(r"\b" + lab + r"\b", body):
            flags.append(lab)
    for cf in re.findall(r"CF-[A-Z]+-\d{3}", fm.get("canonical_facts", "")):
        if cfs.get(cf, {}).get("status") != "closed":
            flags.append("open " + cf)
    if fm.get("run_verification") != "full" and fm.get("scope_class") == "CORE":
        flags.append("run_verification!=full (CORE)")
    return ("verified" if not flags else "partial"), flags


def check_status(write):
    bad = 0
    for p in docs():
        t = open(p, encoding="utf-8").read()
        fm, body = split_fm(t)
        if not fm or "status" not in fm:
            continue
        st, flags = compute_status(fm, body)
        if fm["status"] != st:
            if write:
                t = re.sub(r"^status:.*$", f"status: {st}", t, count=1, flags=re.M)
                open(p, "w", encoding="utf-8").write(t)
            else:
                print(f"CHECK-STATUS FAIL {rel(p)}: declared {fm['status']} computed {st} {flags[:3]}")
                bad += 1
    print("check-status:", "WRITTEN" if write else ("FAIL" if bad else "PASS"), bad)
    return 1 if bad and not write else 0


# ------------------------------------------------------------------ validate-refs (gate 1)
REF = re.compile(r"((?:src|test|tools|docs)/[\w\./\-]+?\.(?:csproj|cs|ps1xml|ps1|psm1|resx|md|props|json|yml|cpp|c|h)(?![\w]))(?:::([\w\.<>,]+))?(?:@L(\d+)(?:-L?(\d+))?)?")


def validate_refs():
    types = json.load(open(os.path.join(DATA, "types.json")))
    by_file = defaultdict(list)
    for t in types:
        by_file[t["file"]].append(t)
    members = {}
    mp = os.path.join(DATA, "members-tierA.json")
    if os.path.exists(mp):
        for t in json.load(open(mp)):
            members[(t["file"], t["full_name"].split(".")[-1])] = t["members"]
    # pin integrity
    try:
        changed = subprocess.run(["git", "diff", "--name-only", PIN["commit"], "HEAD", "--", ".", ":!docs-out"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    except Exception:
        changed = []
    if changed:
        print("VALIDATE-REFS BLOCKED: working tree differs from pin outside docs-out:", changed[:5])
        return 2
    nlines = {}
    bad = total = 0
    for p in docs(include_cards=False):
        t = open(p, encoding="utf-8").read()
        for m in REF.finditer(t):
            path, member, l1, l2 = m.groups()
            total += 1
            if not os.path.exists(os.path.join(ROOT, path)):
                if "*" in path or "<" in path:
                    continue
                print(f"VALIDATE-REFS FAIL {rel(p)}: missing file {path}")
                bad += 1
                continue
            if path not in nlines:
                try:
                    nlines[path] = open(os.path.join(ROOT, path), encoding="utf-8-sig", errors="replace").read().count("\n") + 1
                except Exception:
                    nlines[path] = 10 ** 9
            if l1 and (int(l1) > nlines[path] or (l2 and int(l2) > nlines[path] or (l2 and int(l2) < int(l1)))):
                print(f"VALIDATE-REFS FAIL {rel(p)}: implausible range {path}@L{l1}-{l2} (file has {nlines[path]} lines)")
                bad += 1
            if member and path.endswith(".cs"):
                tn = member.split(".")[0]
                ts = [x for x in by_file.get(path, []) if x["name"].split("<")[0] == tn or x["full_name"].split(".")[-1] == tn]
                if not ts:
                    print(f"VALIDATE-REFS FAIL {rel(p)}: type {tn} not in {path}")
                    bad += 1
                elif "." in member and (path, tn) in members:
                    mn = member.split(".", 1)[1]
                    if not any(mm["name"] == mn for mm in members[(path, tn)]):
                        print(f"VALIDATE-REFS FAIL {rel(p)}: member {member} not found in {path}")
                        bad += 1
    print("validate-refs:", "FAIL" if bad else "PASS", f"{total} refs, {bad} failures")
    return 1 if bad else 0


# ------------------------------------------------------------------ check-links / mermaid lint
def check_links():
    bad = 0
    mm = 0
    for p in docs(include_cards=True):
        t = open(p, encoding="utf-8").read()
        for m in re.finditer(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)\)", strip_code_keep_links(t)):
            href = m.group(1)
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            href = href.split("#")[0]
            if not href:
                continue
            tgt = os.path.normpath(os.path.join(os.path.dirname(p), href))
            if not os.path.exists(tgt):
                print(f"CHECK-LINKS FAIL {rel(p)}: broken link {href}")
                bad += 1
        for blk in re.findall(r"```mermaid\n(.*?)```", t, re.S):
            mm += 1
            first = blk.strip().split("\n")[0].split()[0] if blk.strip() else ""
            if first not in ("flowchart", "graph", "sequenceDiagram", "stateDiagram-v2", "classDiagram", "erDiagram", "gantt", "pie", "journey", "stateDiagram"):
                print(f"CHECK-LINKS FAIL {rel(p)}: unknown mermaid diagram type '{first}'")
                bad += 1
            if blk.count("[") != blk.count("]") or blk.count("(") != blk.count(")") or blk.count("{") != blk.count("}"):
                print(f"CHECK-LINKS WARN {rel(p)}: unbalanced brackets in a mermaid block (lint only; mmdc unavailable)")
    print("check-links:", "FAIL" if bad else "PASS", f"{bad} broken, {mm} mermaid blocks linted (syntax lint only; no mmdc)")
    return 1 if bad else 0


def strip_code_keep_links(t):
    return re.sub(r"```.*?```", "", t, flags=re.S)


# ------------------------------------------------------------------ idreg
IDRE = re.compile(r"\b((?:SEC-ENF-\d{3,4})|(?:NLD-[A-Z]+-\d{3})|(?:CF-[A-Z]+-\d{3})|(?:DEV-[A-Z]+-\d{3})|(?:CON-\d{3})|(?:GS-[A-Z]+-\d{3,4})|(?:CLM-[A-Z]+-\d{4}))\b")


def idreg():
    defs, refs = defaultdict(set), defaultdict(set)
    for p in docs(include_cards=False):
        t = open(p, encoding="utf-8").read()
        fm, _ = split_fm(t)
        if fm and "id" in fm:
            defs[fm["id"]].add(rel(p))
        for ln in t.split("\n"):
            m = re.match(r"^\|\s*\**((?:SEC-ENF|NLD|CF|DEV|CON|GS|CLM)-[A-Z0-9\-]+)\**\s*\|", ln)
            if m:
                defs[m.group(1)].add(rel(p))
            m = re.match(r"^#{2,4}\s+((?:SEC-ENF|NLD|CF|DEV|CON|GS|CLM)-[A-Z0-9\-]+)\b", ln)
            if m:
                defs[m.group(1)].add(rel(p))
            for i in IDRE.findall(ln):
                refs[i].add(rel(p))
    for c in json.load(open(os.path.join(DATA, "canonical-facts.json"))):
        defs[c["id"]].add(c["owner"])
    for f in glob.glob(os.path.join(DATA, "golden", "*", "GS-*.json")):
        defs[os.path.basename(f)[:-5]].add(rel(f))
    s = "# ID registry\n\nGenerated by `tools/consist.py idreg`. `defined in` = front matter, table row or heading that defines the ID; undefined references are listed at the end.\n\n| ID | defined in | referenced in (count) |\n|---|---|---:|\n"
    for i in sorted(defs):
        s += f"| {i} | {', '.join(sorted(defs[i]))} | {len(refs.get(i, []))} |\n"
    und = sorted(set(refs) - set(defs))
    s += f"\n## Referenced but not defined ({len(und)})\n\n" + "\n".join(f"- {i}: {', '.join(sorted(refs[i])[:4])}" for i in und) + "\n"
    open(os.path.join(OUT, "ID-REGISTRY.md"), "w", encoding="utf-8").write(s)
    print("idreg:", len(defs), "defined,", len(und), "undefined references")
    return 0


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else "all"
    a = sys.argv[2:]
    r = 0
    if c in ("render-canonical",):
        r = render_canonical("--check" in a)
    elif c == "check-claims":
        r = check_claims()
    elif c == "lint-terms":
        r = lint_terms()
    elif c == "check-front-matter":
        r = check_front_matter()
    elif c == "check-status":
        r = check_status("--write" in a)
    elif c == "validate-refs":
        r = validate_refs()
    elif c == "check-links":
        r = check_links()
    elif c == "idreg":
        r = idreg()
    elif c == "all":
        idreg()
        for fn in (lambda: render_canonical(True), check_claims, lint_terms, check_front_matter, lambda: check_status(False), validate_refs, check_links):
            r |= fn()
    sys.exit(r)


if __name__ == "__main__":
    main()
