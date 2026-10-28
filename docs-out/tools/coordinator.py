#!/usr/bin/env python3
"""coordinator.py - merge tool for per-task outputs of authoring subagents (section 9).

Purpose : merge .work/cf/*.json -> data/canonical-facts.json + deviation register,
          .work/numbers-proposals/*.json -> data/numbers-extra.json,
          .work/claims/*.jsonl -> data/claims/, .work/annotations/*.json -> data/annotations/,
          .work/ledger-proposals/*.csv -> .work/files-ledger.csv (+ coverage), lessons extraction
          (data/lessons.json) with verdict/DEV checks.
Run     : python3 docs-out/tools/coordinator.py <merge-cf|merge-numbers|merge-claims|merge-annotations|merge-ledger|lessons|coverage|all>
Language: Python 3 (D-002)   Tested: Linux x86_64 / Python 3.13
"""
import csv
import glob
import json
import os
import re
import shutil
import sys
from collections import defaultdict

ROOT = os.path.abspath(os.environ.get("REPO_ROOT", "."))
OUT = os.path.join(ROOT, "docs-out")
DATA = os.path.join(OUT, "data")
WORK = os.path.join(OUT, ".work")
PIN = json.load(open(os.path.join(WORK, "pin.json")))


def jl(p):
    return json.load(open(p))


def jd(p, o):
    json.dump(o, open(p, "w"), indent=1)


# ------------------------------------------------------------------ lessons
LSN = re.compile(r"^\s*[-*]\s+\*\*(LSN-[A-Z0-9]+-\d+)\*\*\s*\[(REPLICATE|ADAPT|REDESIGN|AVOID)\]\s*\(area:\s*(NLD-[A-Z]+)\)\s*(.*)$")


def doc_files():
    for dp, dn, fn in os.walk(OUT):
        dn[:] = [d for d in dn if d not in (".work", "tools", "data", "src-mirror")]
        for f in sorted(fn):
            if f.endswith(".md"):
                yield os.path.join(dp, f)


def lessons():
    out, problems = [], []
    seen = set()
    for p in doc_files():
        t = open(p, encoding="utf-8").read()
        fm_id = re.search(r"^id:\s*(\S+)", t, re.M)
        for i, ln in enumerate(t.split("\n"), 1):
            m = LSN.match(ln)
            if not m:
                if "**LSN-" in ln:
                    problems.append(f"{os.path.relpath(p, OUT)}:{i}: malformed lesson line")
                continue
            lid, verdict, area, rest = m.groups()
            dev = re.search(r"DEV:\s*(DEV-[A-Z]+-\d{3})", rest)
            ev = re.search(r"Evidence:\s*(.*?)(?:\s+DEV:|$)", rest)
            if lid in seen:
                problems.append(f"{os.path.relpath(p, OUT)}:{i}: duplicate {lid}")
            seen.add(lid)
            if verdict in ("REDESIGN", "AVOID") and not dev:
                problems.append(f"{os.path.relpath(p, OUT)}:{i}: {lid} {verdict} without DEV")
            if verdict in ("REPLICATE", "ADAPT") and dev:
                problems.append(f"{os.path.relpath(p, OUT)}:{i}: {lid} {verdict} must not carry DEV")
            out.append({"id": lid, "verdict": verdict, "area": area, "text": re.sub(r"\s*Evidence:.*$", "", rest).strip(), "evidence": ev.group(1).strip() if ev else "",
                        "dev": dev.group(1) if dev else None, "doc": fm_id.group(1) if fm_id else None, "file": os.path.relpath(p, OUT), "line": i})
    jd(os.path.join(DATA, "lessons.json"), out)
    c = defaultdict(int)
    for l in out:
        c[l["verdict"]] += 1
    print("lessons:", len(out), dict(c), "problems:", len(problems))
    for pr in problems:
        print("  LESSON PROBLEM", pr)
    return problems


# ------------------------------------------------------------------ cf + deviations
def merge_cf():
    cfp = os.path.join(DATA, "canonical-facts.json")
    cfs = {c["id"]: c for c in jl(cfp)}
    devs = {}
    msgs = []
    for f in sorted(glob.glob(os.path.join(WORK, "cf", "*.json"))):
        task = os.path.basename(f)[:-5]
        try:
            d = jl(f)
        except Exception as e:  # noqa
            msgs.append(f"{f}: bad json {e}")
            continue
        for c in d.get("cfs", []):
            old = cfs.get(c["id"])
            if old and old.get("_task") and old["_task"] != task:
                msgs.append(f"CF {c['id']} proposed by {old['_task']} and {task}: kept first")
                continue
            new = {"id": c["id"], "subject": c.get("subject") or (old or {}).get("subject", ""), "statement": c.get("statement", ""),
                   "label": c.get("label", "UNVERIFIED"), "evidence": c.get("evidence", []),
                   "owner": c.get("owner") or (old or {}).get("owner", ""), "status": c.get("status", "open"), "_task": task}
            cfs[c["id"]] = new
        for dv in d.get("deviations", []):
            if dv["id"] in devs:
                msgs.append(f"DEV {dv['id']} proposed twice ({devs[dv['id']]['_task']}, {task}): kept first")
                continue
            dv["_task"] = task
            devs[dv["id"]] = dv
    for c in cfs.values():
        if not c.get("statement"):
            c["status"] = "open"
    jd(cfp, [cfs[k] for k in sorted(cfs)])
    # deviation register
    lsn = jl(os.path.join(DATA, "lessons.json")) if os.path.exists(os.path.join(DATA, "lessons.json")) else []
    loc = defaultdict(list)
    for l in lsn:
        if l["dev"]:
            loc[l["dev"]].append(f"{l['id']} ({l['file']})")
    rows = ""
    for k in sorted(devs):
        d = devs[k]
        rows += "| {id} | PROPOSED | {b} | {p} | {be} | {c} | {a} | none (STATIC-ONLY; would change golden samples of the affected CFs once the oracle exists) | {v} |\n".format(
            id=k, b=str(d.get("baseline_behavior", "")).replace("|", "/"), p=str(d.get("proposed_behavior", "")).replace("|", "/"),
            be=str(d.get("benefit", "")).replace("|", "/"), c=str(d.get("compatibility_cost", "")).replace("|", "/"),
            a=", ".join(d.get("affected_cfs", [])) or "-", v="; ".join(loc.get(k, [])) or "(no lesson cites it yet)")
    p = os.path.join(OUT, "09-synthesis", "deviation-register.md")
    t = open(p, encoding="utf-8").read()
    head = t.split("| DEV-ID |")[0]
    hdr = "| DEV-ID | status | baseline behavior (CF/GS) | proposed behavior | benefit | compatibility cost | affected CFs | golden samples that would change | verdict locations |\n|---|---|---|---|---|---|---|---|---|\n"
    open(p, "w", encoding="utf-8").write(head + hdr + rows)
    orphan = [k for k in devs if k not in loc]
    missing = sorted({l["dev"] for l in lsn if l["dev"] and l["dev"] not in devs})
    print(f"merge-cf: {len(cfs)} CFs ({sum(1 for c in cfs.values() if c['status']=='closed')} closed), {len(devs)} DEVs; DEV without lesson: {orphan}; lesson DEV without row: {missing}")
    for m in msgs:
        print("  ", m)


# ------------------------------------------------------------------ numbers
def merge_numbers():
    p = os.path.join(DATA, "numbers-extra.json")
    cur = {e["key"]: e for e in jl(p)} if os.path.exists(p) else {}
    for f in sorted(glob.glob(os.path.join(WORK, "numbers-proposals", "*.json"))):
        for e in jl(f):
            if e["key"] in cur and cur[e["key"]]["cmd"] != e["cmd"]:
                print("  numbers: key", e["key"], "proposed with a different command by", os.path.basename(f), "- kept first")
                continue
            cur[e["key"]] = e
    jd(p, list(cur.values()))
    print("merge-numbers:", len(cur), "extra keys")


# ------------------------------------------------------------------ claims
def merge_claims():
    os.makedirs(os.path.join(DATA, "claims"), exist_ok=True)
    n = 0
    for f in glob.glob(os.path.join(WORK, "claims", "*.jsonl")):
        shutil.copyfile(f, os.path.join(DATA, "claims", os.path.basename(f)))
        n += sum(1 for ln in open(f) if ln.strip())
    keys = set()
    for f in glob.glob(os.path.join(DATA, "claims", "*.jsonl")):
        for ln in open(f):
            if ln.strip():
                try:
                    keys.add(json.loads(ln)["subject_key"])
                except Exception:  # noqa
                    pass
    jd(os.path.join(DATA, "subject-keys.json"), {k: "" for k in sorted(keys)})
    print("merge-claims:", n, "claims,", len(keys), "subject keys")


# ------------------------------------------------------------------ annotations
def merge_annotations():
    fa, pa = {}, {}
    ap = os.path.join(DATA, "annotations")
    for fn, d in (("folder-purposes.json", fa), ("project-purposes.json", pa)):
        if os.path.exists(os.path.join(ap, fn)):
            d.update(jl(os.path.join(ap, fn)))
    for f in sorted(glob.glob(os.path.join(WORK, "annotations", "T*.json"))):
        try:
            a = jl(f)
        except Exception:  # noqa
            continue
        if not isinstance(a, dict) or not ({"folders", "projects"} & set(a)):
            continue
        for k, v in a.get("folders", {}).items():
            cur = fa.setdefault(k, {"purpose": "", "files": {}, "docs": []})
            if v.get("purpose") and not cur["purpose"]:
                cur["purpose"] = v["purpose"]
            cur["files"].update(v.get("files", {}))
            for dd in v.get("docs", []):
                if dd not in cur["docs"]:
                    cur["docs"].append(dd)
        for k, v in a.get("projects", {}).items():
            cur = pa.setdefault(k, {"purpose": "", "key_files": [], "docs": []})
            if v.get("purpose") and not cur["purpose"]:
                cur["purpose"] = v["purpose"]
            cur["key_files"] = cur["key_files"] or v.get("key_files", [])
            for dd in v.get("docs", []):
                if dd not in cur["docs"]:
                    cur["docs"].append(dd)
    jd(os.path.join(ap, "folder-purposes.json"), fa)
    jd(os.path.join(ap, "project-purposes.json"), pa)
    print("merge-annotations:", len(fa), "folders,", len(pa), "projects")


# ------------------------------------------------------------------ ledger
def parse_ranges(s):
    r = []
    for part in re.split(r"[;,]", s or ""):
        part = part.strip()
        m = re.match(r"^(\d+)\s*-\s*(\d+)$", part)
        if m:
            r.append((int(m.group(1)), int(m.group(2))))
        elif part.isdigit():
            r.append((int(part), int(part)))
    return r


def union(rs):
    rs = sorted(rs)
    out = []
    for a, b in rs:
        if out and a <= out[-1][1] + 1:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def merge_ledger():
    lp = os.path.join(WORK, "files-ledger.csv")
    rows = list(csv.DictReader(open(lp)))
    idx = {r["path"]: r for r in rows}
    for f in sorted(glob.glob(os.path.join(WORK, "ledger-proposals", "*.csv"))):
        for pr in csv.DictReader(open(f)):
            r = idx.get(pr["path"])
            if not r:
                print("  ledger: unknown path", pr["path"], "in", os.path.basename(f))
                continue
            cur = parse_ranges(r["ranges_read"])
            new = cur + parse_ranges(pr["ranges_read"])
            rr = union(new)
            r["ranges_read"] = ";".join(f"{a}-{b}" for a, b in rr)
            docs = set(x for x in r["doc_ids"].split(";") if x) | set(x for x in re.split(r"[;,]", pr.get("doc_ids", "")) if x.strip())
            r["doc_ids"] = ";".join(sorted(x.strip() for x in docs))
    for r in rows:
        loc = int(r["loc"])
        covered = sum(b - a + 1 for a, b in parse_ranges(r["ranges_read"]))
        r["status"] = "read" if loc and covered >= loc else ("partial" if covered else "unread")
    with open(lp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["path", "loc", "tier", "ranges_read", "doc_ids", "status"])
        w.writeheader()
        w.writerows(rows)
    coverage()


def coverage():
    rows = list(csv.DictReader(open(os.path.join(WORK, "files-ledger.csv"))))
    by = defaultdict(lambda: [0, 0])
    a_missing = []
    for r in rows:
        if not r["path"].endswith(".cs"):
            continue
        loc = int(r["loc"])
        cov = sum(b - a + 1 for a, b in parse_ranges(r["ranges_read"]))
        cov = min(cov, loc)
        by[r["tier"]][0] += loc
        by[r["tier"]][1] += cov
        if r["tier"] == "A" and cov < loc:
            a_missing.append((r["path"], loc, cov))
    for t in "ABC":
        l, c = by[t]
        print(f"coverage tier {t}: {c}/{l} lines read ({(100*c/l if l else 0):.1f}%)")
    print("tier A files not fully read:", len(a_missing))
    return a_missing


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "all"
    if c == "lessons":
        lessons()
    elif c == "merge-cf":
        lessons()
        merge_cf()
    elif c == "merge-numbers":
        merge_numbers()
    elif c == "merge-claims":
        merge_claims()
    elif c == "merge-annotations":
        merge_annotations()
    elif c == "merge-ledger":
        merge_ledger()
    elif c == "coverage":
        coverage()
    elif c == "all":
        lessons()
        merge_cf()
        merge_numbers()
        merge_claims()
        merge_annotations()
        merge_ledger()
