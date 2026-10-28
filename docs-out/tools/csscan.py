#!/usr/bin/env python3
"""csscan.py - light C# lexer + structural scanner (shared library for the extraction tools).

Purpose : tokenize C# source (comments/strings/char/raw strings/preprocessor aware) and
          recover namespaces, types, members, attributes, base lists, line ranges and the
          enclosing preprocessor conditions. NOT a full C# parser: every output built on it
          is labelled APPROX (rule 19) because no Roslyn is available (STATIC-ONLY run).
Inputs  : a path to a .cs file (library use) - run `python3 csscan.py <file.cs>` for a dump.
Outputs : python dicts (see scan_file); CLI prints JSON.
Run     : python3 docs-out/tools/csscan.py src/.../File.cs
Language: Python 3 (no dotnet/pwsh on this host; recorded in DECISIONS.md D-002)
Tested  : Linux x86_64, Python 3.13
"""
import json
import re
import sys

TYPE_KW = {"class", "struct", "interface", "enum", "record", "delegate"}
MODIFIERS = {
    "public", "private", "protected", "internal", "static", "abstract", "sealed", "partial",
    "virtual", "override", "readonly", "unsafe", "extern", "new", "async", "const", "volatile",
    "required", "file", "ref", "fixed",
}
ACCESS = {"public", "private", "protected", "internal"}


class Tok:
    __slots__ = ("k", "v", "line", "cond")

    def __init__(self, k, v, line, cond):
        self.k = k      # 'id' 'num' 'str' 'chr' 'p' (punct) 'dir' (preprocessor)
        self.v = v
        self.line = line
        self.cond = cond  # tuple of active #if conditions

    def __repr__(self):
        return f"{self.k}:{self.v}@{self.line}"


_ID_START = re.compile(r"[A-Za-z_@\u0080-￿]")
_ID = re.compile(r"@?[A-Za-z_\u0080-￿][A-Za-z0-9_\u0080-￿]*")
_NUM = re.compile(r"0[xX][0-9a-fA-F_]+[uUlL]*|0[bB][01_]+[uUlL]*|\d[\d_]*(\.\d[\d_]*)?([eE][+-]?\d+)?[fFdDmMuUlL]*")
_PUNCT3 = {">>=", "<<=", "??=", "...", "?.["}
_PUNCT2 = {"=>", "==", "!=", "<=", ">=", "&&", "||", "??", "?.", "::", "++", "--", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<", "->"}


def tokenize(src):
    toks = []
    i, n, line = 0, len(src), 1
    cond_stack = []   # list of lists (each #if group: list of branch conditions)
    cur_cond = ()
    at_line_start = True

    def cond_now():
        c = []
        for grp in cond_stack:
            c.extend(grp["active"])
        return tuple(c)

    while i < n:
        ch = src[i]
        if ch == "\n":
            line += 1
            i += 1
            at_line_start = True
            continue
        if ch in " \t\r\f\v﻿":
            i += 1
            continue
        # preprocessor directive
        if ch == "#" and at_line_start:
            j = src.find("\n", i)
            if j == -1:
                j = n
            text = src[i:j].strip()
            m = re.match(r"#\s*(if|elif|else|endif|region|endregion|pragma|nullable|define|undef|line|error|warning)\b\s*(.*)", text)
            if m:
                d, rest = m.group(1), re.sub(r"//.*$", "", m.group(2)).strip()
                if d == "if":
                    cond_stack.append({"branches": [rest], "active": [rest]})
                elif d == "elif" and cond_stack:
                    g = cond_stack[-1]
                    prev = g["branches"]
                    g["branches"] = prev + [rest]
                    g["active"] = ["!(" + " || ".join(prev) + ")", rest]
                elif d == "else" and cond_stack:
                    g = cond_stack[-1]
                    g["active"] = ["!(" + " || ".join(g["branches"]) + ")"]
                elif d == "endif" and cond_stack:
                    cond_stack.pop()
            toks.append(Tok("dir", text, line, cond_now()))
            i = j
            continue
        at_line_start = False
        # comments
        if ch == "/" and i + 1 < n:
            nx = src[i + 1]
            if nx == "/":
                j = src.find("\n", i)
                i = n if j == -1 else j
                continue
            if nx == "*":
                j = src.find("*/", i + 2)
                j = n if j == -1 else j + 2
                line += src.count("\n", i, j)
                i = j
                continue
        c = cond_now()
        # raw string """ ... """
        if ch == '"' and src.startswith('"""', i):
            m = re.match(r'"{3,}', src[i:])
            q = m.group(0)
            j = src.find(q, i + len(q))
            j = n if j == -1 else j + len(q)
            toks.append(Tok("str", "", line, c))
            line += src.count("\n", i, j)
            i = j
            continue
        # strings: ", @", $", $@", @$"
        m = re.match(r'(\$+@?|@\$*)?"', src[i:i + 8])
        if m and (ch in '"$@'):
            prefix = m.group(1) or ""
            if ch == '"' or prefix:
                verbatim = "@" in prefix
                interp = "$" in prefix
                j = i + len(m.group(0))
                depth = 0
                start_line = line
                while j < n:
                    cj = src[j]
                    if cj == "\n":
                        line += 1
                    if interp and cj == "{":
                        if src.startswith("{{", j) and depth == 0:
                            j += 2
                            continue
                        depth += 1
                    elif interp and cj == "}" and depth > 0:
                        depth -= 1
                    elif depth == 0:
                        if verbatim:
                            if cj == '"':
                                if src.startswith('""', j):
                                    j += 2
                                    continue
                                j += 1
                                break
                        else:
                            if cj == "\\":
                                j += 2
                                continue
                            if cj == '"':
                                j += 1
                                break
                    j += 1
                toks.append(Tok("str", "", start_line, c))
                i = j
                continue
        if ch == "'":
            j = i + 1
            while j < n and src[j] != "'":
                if src[j] == "\\":
                    j += 1
                j += 1
            toks.append(Tok("chr", "", line, c))
            i = j + 1
            continue
        m = _ID.match(src, i)
        if m:
            toks.append(Tok("id", m.group(0).lstrip("@"), line, c))
            i = m.end()
            continue
        if ch.isdigit() or (ch == "." and i + 1 < n and src[i + 1].isdigit()):
            m = _NUM.match(src, i) or re.match(r"\.\d+", src[i:])
            toks.append(Tok("num", m.group(0), line, c))
            i += len(m.group(0)) if hasattr(m, "group") else 1
            continue
        t3, t2 = src[i:i + 3], src[i:i + 2]
        if t3 in _PUNCT3:
            toks.append(Tok("p", t3, line, c)); i += 3; continue
        if t2 in _PUNCT2:
            toks.append(Tok("p", t2, line, c)); i += 2; continue
        toks.append(Tok("p", ch, line, c))
        i += 1
    return toks


def _match_brace(toks):
    """map index of '{' -> index of matching '}' (and '(' ')' , '[' ']')."""
    pairs = {"{": "}", "(": ")", "[": "]"}
    stacks = {k: [] for k in pairs}
    close_to_open = {v: k for k, v in pairs.items()}
    m = {}
    for idx, t in enumerate(toks):
        if t.k != "p":
            continue
        if t.v in pairs:
            stacks[t.v].append(idx)
        elif t.v in close_to_open:
            st = stacks[close_to_open[t.v]]
            if st:
                o = st.pop()
                m[o] = idx
                m[idx] = o
    return m


def _skip_attrs(toks, i, end, match):
    """consume leading [attr] groups (and #dir tokens); return (new_i, [attribute names])."""
    attrs = []
    while i < end:
        t = toks[i]
        if t.k == "dir":
            i += 1
            continue
        if t.k == "p" and t.v == "[":
            j = match.get(i, i)
            # attribute names: identifiers directly after '[' or ',' (depth 1)
            depth, k, expect = 0, i + 1, True
            while k < j:
                tk = toks[k]
                if tk.k == "p" and tk.v in "([{":
                    depth += 1
                elif tk.k == "p" and tk.v in ")]}":
                    depth -= 1
                elif depth == 0 and tk.k == "p" and tk.v == ",":
                    expect = True
                elif depth == 0 and expect and tk.k == "id":
                    name = tk.v
                    # target specifier "assembly:" / "return:"
                    if k + 1 < j and toks[k + 1].k == "p" and toks[k + 1].v == ":":
                        k += 2
                        continue
                    while k + 2 < j and toks[k + 1].v == "." and toks[k + 2].k == "id":
                        name += "." + toks[k + 2].v
                        k += 2
                    attrs.append(name)
                    expect = False
                k += 1
            i = j + 1
            continue
        break
    return i, attrs


def _parse_header(h):
    """h: list of tokens of a declaration header (before '{' ';' '=>' '=')."""
    mods = [t.v for t in h if t.k == "id" and t.v in MODIFIERS]
    return mods


def _angle_end(h, i):
    """index after matching '>' for generic list starting at h[i]=='<'."""
    d = 0
    while i < len(h):
        if h[i].v == "<":
            d += 1
        elif h[i].v == ">":
            d -= 1
            if d == 0:
                return i + 1
        elif h[i].v == ">>":
            d -= 2
            if d <= 0:
                return i + 1
        i += 1
    return i


def _typename(h, i):
    """parse a (possibly generic/nullable/array/qualified) type starting at h[i]; return (text, next_i)."""
    s = []
    n = len(h)
    depth = 0
    while i < n:
        t = h[i]
        if t.k == "id" or (t.k == "p" and t.v in "<>.,?[]*:" and (depth > 0 or t.v in "<.?[]*:")) or t.v in ("::", ">>"):
            if t.v == "<":
                depth += 1
            elif t.v == ">":
                depth -= 1
            elif t.v == ">>":
                depth -= 2
            if t.k == "id" and depth == 0 and s and s[-1] not in ("<", ".", "::", ",", "[", "?", "*") and not s[-1].endswith("."):
                break
            if t.v == "?" and depth == 0 and i + 1 < n and h[i + 1].k != "id" and h[i + 1].v not in ("[", "?"):
                s.append(t.v); i += 1; break
            s.append(t.v)
            i += 1
            if t.v == "]" and depth == 0:
                continue
        elif t.v == "(" and not s:
            # tuple type
            d = 0
            while i < n:
                s.append(h[i].v)
                if h[i].v == "(":
                    d += 1
                elif h[i].v == ")":
                    d -= 1
                    if d == 0:
                        i += 1
                        break
                i += 1
        else:
            break
    return "".join(s), i


def scan_tokens(toks):
    match = _match_brace(toks)
    n = len(toks)
    types = []
    namespaces = []

    def end_line_of(idx_close):
        return toks[idx_close].line

    def parse_block(i, end, ns, parent):
        """parse declarations in toks[i:end] (a namespace or type body)."""
        while i < end:
            t = toks[i]
            if t.k == "dir":
                i += 1
                continue
            if t.k == "p" and t.v in ("{", "}", ";"):
                i += 1
                continue
            start = i
            i, attrs = _skip_attrs(toks, i, end, match)
            if i >= end:
                break
            # file-scoped / block namespace
            if toks[i].k == "id" and toks[i].v == "namespace":
                j = i + 1
                name = []
                while j < end and toks[j].v not in ("{", ";"):
                    name.append(toks[j].v)
                    j += 1
                nsname = "".join(name)
                full = (ns + "." + nsname) if ns else nsname
                namespaces.append({"name": full, "line": toks[i].line})
                if j < end and toks[j].v == "{":
                    close = match.get(j, end)
                    parse_block(j + 1, close, full, None)
                    i = close + 1
                else:  # file scoped: rest of file belongs to ns
                    parse_block(j + 1, end, full, None)
                    return
                continue
            if toks[i].k == "id" and toks[i].v in ("using", "extern") and not parent:
                while i < end and toks[i].v != ";":
                    i += 1
                i += 1
                continue
            if toks[i].k == "id" and toks[i].v == "using" and parent:
                while i < end and toks[i].v != ";":
                    i += 1
                i += 1
                continue
            # collect header up to first top-level { ; => =
            h = []
            j = i
            depth = 0
            hit = None
            while j < end:
                tj = toks[j]
                if tj.k == "dir":
                    j += 1
                    continue
                if tj.k == "p":
                    if tj.v in "([":
                        # skip balanced group but keep tokens in header
                        c = match.get(j, j)
                        h.extend(x for x in toks[j:c + 1] if x.k != "dir")
                        j = c + 1
                        continue
                    if tj.v in ("{", ";", "=>", "="):
                        hit = tj.v
                        break
                    if tj.v == "}":
                        hit = "}"
                        break
                h.append(tj)
                j += 1
            if not h:
                i = j + 1 if j < end else end
                continue
            ids = [x.v for x in h if x.k == "id"]
            # --- type declaration?
            kwpos = None
            for idx, x in enumerate(h):
                if x.k == "id" and x.v in TYPE_KW:
                    # record/class/struct/enum/interface/delegate (record struct handled)
                    if x.v == "record" and idx + 1 < len(h) and h[idx + 1].v in ("class", "struct"):
                        continue
                    kwpos = idx
                    break
                if x.k == "p" and x.v == "(" and kwpos is None and not any(y.v in TYPE_KW for y in h[:idx]):
                    break
            is_type = kwpos is not None and all(
                (y.k == "id" and (y.v in MODIFIERS or y.v in TYPE_KW)) or y.k == "p" for y in h[:kwpos]
            )
            if is_type and h[kwpos].v == "delegate":
                # delegate <ret> Name<T>(params);
                nm = None
                for idx in range(kwpos + 1, len(h)):
                    if h[idx].k == "id" and idx + 1 < len(h) and h[idx + 1].v in ("(", "<"):
                        nm = h[idx].v
                        break
                end_idx = j
                if hit == "{":
                    end_idx = j
                types.append({
                    "kind": "delegate", "name": nm, "namespace": ns, "parent": parent["full"] if parent else None,
                    "start": h[0].line, "end": toks[min(j, n - 1)].line, "modifiers": _parse_header(h[:kwpos]),
                    "bases": [], "attributes": attrs, "cond": list(h[0].cond), "members": [],
                })
                i = j + 1 if hit == ";" else j
                continue
            if is_type:
                kind = h[kwpos].v
                if kind == "record" and kwpos + 1 < len(h) and False:
                    pass
                k = kwpos + 1
                if kind == "record" and k < len(h) and h[k].v in ("class", "struct"):
                    k += 1
                name = h[k].v if k < len(h) else "?"
                k += 1
                gen = ""
                if k < len(h) and h[k].v == "<":
                    e = _angle_end(h, k)
                    gen = "".join(x.v for x in h[k:e])
                    k = e
                # primary ctor params for records/classes: skip balanced ()
                if k < len(h) and h[k].v == "(":
                    d = 0
                    while k < len(h):
                        if h[k].v == "(":
                            d += 1
                        elif h[k].v == ")":
                            d -= 1
                            if d == 0:
                                k += 1
                                break
                        k += 1
                bases = []
                if k < len(h) and h[k].v == ":":
                    k += 1
                    while k < len(h) and not (h[k].k == "id" and h[k].v == "where"):
                        tn, k2 = _typename(h, k)
                        if tn:
                            bases.append(tn)
                        k = k2 if k2 > k else k + 1
                        if k < len(h) and h[k].v == ",":
                            k += 1
                full = (parent["full"] + "." if parent else (ns + "." if ns else "")) + name
                rec = {
                    "kind": kind, "name": name + gen if gen else name, "ident": name, "namespace": ns,
                    "parent": parent["full"] if parent else None, "full": full,
                    "start": h[0].line, "modifiers": _parse_header(h[:kwpos]), "bases": bases,
                    "attributes": attrs, "cond": list(h[0].cond), "members": [], "end": h[0].line,
                }
                types.append(rec)
                if hit == "{":
                    close = match.get(j, end)
                    rec["end"] = toks[close].line
                    if kind == "enum":
                        rec["enum_members"] = parse_enum(j + 1, close)
                    else:
                        parse_block(j + 1, close, ns, rec)
                    i = close + 1
                elif hit == ";":
                    rec["end"] = toks[j].line
                    i = j + 1
                else:
                    i = j + 1
                continue
            # --- member (only inside a type)
            if hit == "}":
                i = j + 1
                continue
            if parent is None:
                # top-level statement or something unknown; skip to ; or block
                if hit == "{":
                    i = match.get(j, j) + 1
                else:
                    i = j + 1
                continue
            mem = classify_member(h, hit, j, attrs, end, parent)
            if mem is None:
                if hit == "{":
                    i = match.get(j, j) + 1
                else:
                    i = j + 1
                continue
            # find end of member
            if mem["kind"] in ("method", "ctor", "dtor", "operator", "conversion") or (mem["kind"] == "property" and hit == "{"):
                if hit == "{":
                    close = match.get(j, j)
                    mem["end"] = toks[close].line
                    if mem["kind"] == "property":
                        body = {x.v for x in toks[j:close] if x.k == "id" and x.v in ("get", "set", "init")}
                        mem["accessors"] = sorted(body)
                    i = close + 1
                elif hit == "=>":
                    k2 = j
                    d = 0
                    while k2 < end:
                        v = toks[k2].v
                        if toks[k2].k == "p" and v in "([{":
                            k2 = match.get(k2, k2)
                        elif v == ";" and toks[k2].k == "p":
                            break
                        k2 += 1
                    mem["end"] = toks[min(k2, n - 1)].line
                    i = k2 + 1
                else:  # ';' abstract/extern/interface
                    mem["end"] = toks[j].line if j < n else mem["start"]
                    i = j + 1
            else:
                # field/event/const/property-with-initializer/enum-like: scan to ';' (balanced)
                k2 = j
                while k2 < end:
                    tk = toks[k2]
                    if tk.k == "p" and tk.v in "([{":
                        k2 = match.get(k2, k2) + 1
                        continue
                    if tk.k == "p" and tk.v == ";":
                        break
                    k2 += 1
                if mem["kind"] == "property" and hit == "{":
                    pass
                mem["end"] = toks[min(k2, n - 1)].line
                i = k2 + 1
            parent["members"].append(mem)
        return

    def classify_member(h, hit, j, attrs, end, parent):
        mods = _parse_header(h)
        vis = next((m for m in mods if m in ACCESS), None)
        line = h[0].line
        ids = [x for x in h if x.k == "id"]
        vals = [x.v for x in h]
        base = {"modifiers": mods, "access": vis, "start": line, "attributes": attrs, "cond": list(h[0].cond)}
        if "operator" in vals:
            op = vals[vals.index("operator") + 1] if vals.index("operator") + 1 < len(vals) else "?"
            if "implicit" in vals or "explicit" in vals:
                return dict(base, kind="conversion", name=("implicit " if "implicit" in vals else "explicit ") + "operator", sig=" ".join(vals))
            return dict(base, kind="operator", name="operator " + op, sig=" ".join(vals))
        if "event" in vals:
            nm = [x.v for x in h if x.k == "id" and x.v != "event"]
            return dict(base, kind="event", name=nm[-1] if nm else "?", sig=" ".join(vals))
        if "const" in vals:
            nm = [x.v for x in h if x.k == "id"]
            return dict(base, kind="const", name=nm[-1] if nm else "?", sig=" ".join(vals))
        # find '(' at depth 0 to identify method/ctor
        paren = None
        for idx, x in enumerate(h):
            if x.k == "p" and x.v == "(":
                paren = idx
                break
        if paren is not None and hit in ("{", ";", "=>", None, "}"):
            # name = identifier before '(' (skip generic list)
            k = paren - 1
            if k >= 0 and h[k].v == ">":
                d = 0
                while k >= 0:
                    if h[k].v == ">":
                        d += 1
                    elif h[k].v == "<":
                        d -= 1
                        if d == 0:
                            break
                    k -= 1
                k -= 1
            nm = h[k].v if k >= 0 else "?"
            if k >= 1 and h[k - 1].v == "~":
                return dict(base, kind="dtor", name="~" + nm, sig=" ".join(vals))
            if k >= 1 and h[k - 1].v == ".":  # explicit interface impl
                nm = h[k - 1 - 1].v + "." + nm if k >= 2 else nm
            kind = "ctor" if (nm == parent.get("ident") and (k == 0 or all(x.v in MODIFIERS for x in [y for y in h[:k] if y.k == "id"]))) else "method"
            ret = " ".join(x.v for x in h[:k] if not (x.k == "id" and x.v in MODIFIERS))
            return dict(base, kind=kind, name=nm, returns=ret, sig=" ".join(vals)[:300])
        # property / indexer / field
        if "this" in vals and "[" in vals:
            return dict(base, kind="indexer", name="this[]", sig=" ".join(vals)[:200])
        nm = None
        for x in reversed(h):
            if x.k == "id":
                nm = x.v
                break
        if hit == "{":
            return dict(base, kind="property", name=nm or "?", sig=" ".join(vals)[:200])
        if hit == "=>":
            return dict(base, kind="property", name=nm or "?", sig=" ".join(vals)[:200], expr_bodied=True)
        if hit in ("=", ";"):
            return dict(base, kind="field", name=nm or "?", sig=" ".join(vals)[:200])
        return None

    def parse_enum(i, end):
        members = []
        k = i
        while k < end:
            k, attrs = _skip_attrs(toks, k, end, match)
            if k >= end:
                break
            t = toks[k]
            if t.k == "id":
                name = t.v
                line = t.line
                val_toks = []
                k += 1
                if k < end and toks[k].v == "=":
                    k += 1
                    d = 0
                    while k < end:
                        tk = toks[k]
                        if tk.k == "p" and tk.v in "([{":
                            c = match.get(k, k)
                            val_toks.extend(toks[k:c + 1])
                            k = c + 1
                            continue
                        if tk.k == "p" and tk.v == "," and d == 0:
                            break
                        val_toks.append(tk)
                        k += 1
                members.append({"name": name, "line": line, "value": " ".join(x.v if x.k != "str" else '"..."' for x in val_toks) or None,
                                "attributes": attrs, "cond": list(t.cond)})
            while k < end and not (toks[k].k == "p" and toks[k].v == ","):
                if toks[k].k == "id":
                    break
                k += 1
            if k < end and toks[k].v == ",":
                k += 1
        return members

    parse_block(0, n, "", None)
    return types, namespaces


def scan_file(path):
    with open(path, encoding="utf-8-sig", errors="replace") as f:
        src = f.read()
    toks = tokenize(src)
    types, namespaces = scan_tokens(toks)
    return {"path": path, "loc": src.count("\n") + (0 if src.endswith("\n") or not src else 1), "types": types,
            "namespaces": namespaces, "directives": sorted({t.v.split()[1] if len(t.v.split()) > 1 else "" for t in toks if t.k == "dir" and t.v.startswith("#if")} - {""})}


if __name__ == "__main__":
    r = scan_file(sys.argv[1])
    json.dump(r, sys.stdout, indent=1)
