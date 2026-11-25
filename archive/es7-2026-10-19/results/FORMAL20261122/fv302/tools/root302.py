#!/usr/bin/env python3
"""FV302 (24 Nov 2026): sub-root and Root modules joining the exported contexts of the budget-69 tree.
NOTHING HERE PROVES ANYTHING: Lean checks every split_pm step (both children must be stated with the right literal
path), so a missing, misplaced or mispathed context makes the module fail to compile. Adapted from root_es304z.py
for an irregular top trie: contexts sit at bit depth 14 or 15 below the first decision [0, 0] (state 0 occupied).

  root302.py --contexts C --export OUT (--sub BITS [--name NAME] | --root D)

--sub BITS  module E302ZZ.<NAME> (default S_<BITS>) for the trie node with bit prefix BITS (below [0, 0]): imports the
            chunk modules of the contexts under it, joins each multi-module context through its internal skeleton,
            then the trie nodes under BITS bottom-up, and states `root` at the node's path.
--root D    module E302ZZ.Root: imports the sub-roots S_<p> for every trie node p at bit depth D and joins up to the
            first decision: `E302ZZ.root : ¬ ∃ holes, FFeas fcatZZs16 3133 252 69 (pmask (zerosF 252) [(0, 2)]) holes`.
"""
import argparse, json, sys
from pathlib import Path

X = Path("/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05")
sys.path.insert(0, str(X))
from export_es311 import OPTS, lean_path  # noqa: E402

PREFIX, PARAMS, M0 = "E302ZZ", "fcatZZs16 3133 252 69", "(zerosF 252)"


def feas(p):
    return f"¬ ∃ holes : Fin 252 → ℕ, FFeas {PARAMS} (pmask {M0} {lean_path(p)}) holes"


def load(cpath):
    ctx, vert = {}, {}
    for line in open(cpath):
        c = json.loads(line)
        bitsk = tuple(b for _, b in c["path"][1:])
        ctx[bitsk] = c
        for d in range(len(bitsk)):
            v = c["path"][1 + d][0]
            assert vert.setdefault(bitsk[:d], v) == v
    return ctx, vert


def node_path(ctx, vert, bits):
    """Innermost-first Lean path of the trie node with bit prefix `bits`: the first decision (0, occupied) and the
    decisions along `bits`."""
    p = [(0, 2)]
    for d, b in enumerate(bits):
        p.append((vert[bits[:d]], 2 if b == 0 else 1))
    return list(reversed(p))


def header(name, imports):
    return [*(f"import {m}" for m in imports), "import CompactChecker.Path", "open CompactChecker",
            "set_option maxRecDepth 100000", *OPTS, f"namespace {name}",
            "-- FV302 (24 Nov 2026): joins of the ES(8) <= 302 compact check (budget-69 Z/Z*-row tree); Lean checks each step"]


def context_root(k, man, lines):
    """As root_es304z.context_root: Lean term for context k's root; appends its internal joins."""
    base = [tuple(x) for x in man["base_path"]]
    mods = man["modules"]
    where = {s: m["module"] for m in mods for s, _ in m["subtree_roots"]}
    if not man["skeleton"]:
        assert list(where) == [0], (k, where)
        return f"{where[0]}.ex0"
    sk = {e["u"]: e for e in man["skeleton"]}
    parent = {}
    for e in man["skeleton"]:
        parent[e["zero"]] = (e["u"], 2)
        parent[e["one"]] = (e["u"], 1)

    def path(x):
        p = []
        while x != 0:
            u, dd = parent[x]
            p.append((sk[u]["vertex"], dd))
            x = u
        return p + base

    def ref(x):
        return f"{where[x]}.ex{x}" if x in where else f"k{k:05d}_{x}"

    for u in sorted(sk, reverse=True):
        e = sk[u]
        lines.append(f"theorem k{k:05d}_{u} : {feas(path(u))} :=")
        lines.append(f"  split_pm {PARAMS} {M0} {lean_path(path(u))} {e['vertex']} {ref(e['zero'])} {ref(e['one'])}")
    return f"k{k:05d}_0"


def join_up(ctx, vert, top, refs, lines, leaf_ref):
    """Join every trie node at or below `top` bottom-up; refs maps bit tuples to Lean terms."""
    nodes = sorted([b for b in vert if b[:len(top)] == top], key=len, reverse=True)
    for b in nodes:
        r = []
        for c in (b + (0,), b + (1,)):
            if c in refs: r.append(refs[c])
            elif c in ctx: r.append(leaf_ref(c))
            else: raise SystemExit(f"child {c} of {b} neither joined nor a context")
        nm = "t_" + ("".join(map(str, b)) or "e")
        lines.append(f"theorem {nm} : {feas(node_path(ctx, vert, b))} :=")
        lines.append(f"  split_pm {PARAMS} {M0} {lean_path(node_path(ctx, vert, b))} {vert[b]} {r[0]} {r[1]}")
        refs[b] = nm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contexts", type=Path, required=True)
    ap.add_argument("--export", type=Path, required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sub")
    g.add_argument("--root", type=int)
    ap.add_argument("--name")
    a = ap.parse_args()
    ctx, vert = load(a.contexts)
    out = a.export / "src" / PREFIX
    if a.sub is not None:
        top = tuple(int(c) for c in a.sub)
        name = a.name or "S_" + (a.sub or "e")
        ks = sorted(b for b in ctx if b[:len(top)] == top)
        mans = {b: json.loads((a.export / "ctx" / f"ctx-{ctx[b]['ctx']:05d}.json").read_text()) for b in ks}
        imports = [m["module"] for b in ks for m in mans[b]["modules"]]
        lines = header(f"{PREFIX}.{name}", imports)
        croot = {}
        for b in ks:
            assert [tuple(x) for x in mans[b]["base_path"]] == node_path(ctx, vert, b), b
            croot[b] = context_root(ctx[b]["ctx"], mans[b], lines)
        refs = {}
        if top in ctx:                      # the sub-root is a single context
            res = croot[top]
        else:
            join_up(ctx, vert, top, refs, lines, lambda c: croot[c])
            res = refs[top]
        lines.append(f"theorem root : {feas(node_path(ctx, vert, top))} := {res}")
        lines += ["#print axioms root", f"end {PREFIX}.{name}"]
        nm = name
    else:
        D = a.root
        tops = sorted({b[:D] for b in ctx})
        assert all(t in vert for t in tops), "a context lies above the sub-root depth"
        imports = [f"{PREFIX}.S_{''.join(map(str, t))}" for t in tops]
        lines = header(PREFIX, imports)
        refs = {t: f"{PREFIX}.S_{''.join(map(str, t))}.root" for t in tops}
        upper = {b: v for b, v in vert.items() if len(b) < D}
        for b in sorted(upper, key=len, reverse=True):
            r = [refs[b + (0,)], refs[b + (1,)]]
            nm = "t_" + ("".join(map(str, b)) or "e")
            lines.append(f"theorem {nm} : {feas(node_path(ctx, vert, b))} :=")
            lines.append(f"  split_pm {PARAMS} {M0} {lean_path(node_path(ctx, vert, b))} {vert[b]} {r[0]} {r[1]}")
            refs[b] = nm
        lines.append(f"theorem root : {feas([(0, 2)])} := {refs[()]}")
        lines += ["#print axioms root", f"end {PREFIX}"]
        nm = "Root"
    path = out / f"{nm}.lean"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text("\n".join(lines) + "\n")
    tmp.replace(path)
    print(json.dumps({"module": f"{PREFIX}.{nm}", "file": str(path), "imports": len(imports), "lines": len(lines)}))


if __name__ == "__main__":
    main()
