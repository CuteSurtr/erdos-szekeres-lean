#!/usr/bin/env python3
"""Sub-root and Root modules joining the exported contexts of the ES(8) <= 304 tree (FV304, 20 November 2026).
NOTHING HERE PROVES ANYTHING: Lean checks every split_pm step (both children must be stated with the right literal
path), so a missing, misplaced or mispathed context makes the module fail to compile.

  root_es304z.py --contexts C --export OUT (--sub D:P [--name NAME] | --root DS)

--sub D:P   one module E304Z.<NAME> (default S<D>_<P>) for the top-skeleton node at depth D with root-first prefix P
            (1 <= D <= 13): it imports the chunk modules of the contexts under the node, joins each multi-module
            context through its internal skeleton (theorems k<kkkk>_<u>), then the top skeleton from depth 12 up
            to D (theorems t<d>_<p>), and states `root` at the node's path.
--root DS   E304Z.Root: imports the 2^DS sub-roots S<DS>_<p> and joins depths DS-1 .. 0 into
            `E304Z.root : ¬ ∃ holes, FFeas fcatZ 3132 252 67 (pmask (zerosF 252) []) holes`.
Every context under the node must have OUT/ctx/ctx-<kkkk>.json (export_es304z.py); paths and vertices come from
contexts.jsonl (validated by export_es310.load_contexts: one complete depth-13 tree).
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import export_es310 as E  # noqa: E402
from export_es311 import OPTS, lean_path  # noqa: E402

E.DEPTH, E.N_CTX = 13, 8192
DEPTH, PREFIX = 13, "E304Z"
PARAMS = "fcatZ 3132 252 67"
M0 = "(zerosF 252)"


def feas(p):
    return f"¬ ∃ holes : Fin 252 → ℕ, FFeas {PARAMS} (pmask {M0} {lean_path(p)}) holes"


def top_path(ctxs, d, p):
    """Innermost-first Lean path of the top node (d, p): the first d decisions of a context under it."""
    c = ctxs[p << (DEPTH - d)]["path"][:d]
    return [(v, 2 if b == 0 else 1) for v, b in reversed(c)]


def header(name, imports):
    return [*(f"import {m}" for m in imports), "import CompactChecker.Path", "open CompactChecker",
            "set_option maxRecDepth 100000", *OPTS, f"namespace {name}",
            "-- FV304 (20 Nov 2026): joins of the ES(8) <= 304 compact check (budget-67 Z-row tree); Lean checks each step"]


def context_root(k, man, lines):
    """Lean term for context k's root (ex at its base path); appends the internal joins to lines."""
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
        return f"{where[x]}.ex{x}" if x in where else f"k{k:04d}_{x}"

    for u in sorted(sk, reverse=True):          # preorder ids: children have larger ids, so they come first
        e = sk[u]
        lines.append(f"theorem k{k:04d}_{u} : {feas(path(u))} :=")
        lines.append(f"  split_pm {PARAMS} {M0} {lean_path(path(u))} {e['vertex']} {ref(e['zero'])} {ref(e['one'])}")
    return f"k{k:04d}_0"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--contexts", type=Path, required=True)
    ap.add_argument("--export", type=Path, required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sub")
    g.add_argument("--root", type=int)
    ap.add_argument("--name")
    args = ap.parse_args()
    _, ctxs, pv = E.load_contexts(args.contexts)
    out = args.export / "src" / PREFIX
    if args.sub:
        d0, p0 = map(int, args.sub.split(":"))
        assert 1 <= d0 <= DEPTH and 0 <= p0 < (1 << d0)
        name = args.name or f"S{d0}_{p0}"
        ks = range(p0 << (DEPTH - d0), (p0 + 1) << (DEPTH - d0))
        mans = {k: json.loads((args.export / "ctx" / f"ctx-{k:04d}.json").read_text()) for k in ks}
        imports = [m["module"] for k in ks for m in mans[k]["modules"]]
        lines = header(f"{PREFIX}.{name}", imports)
        refs = {}
        for k in ks:
            assert [tuple(x) for x in mans[k]["base_path"]] == top_path(ctxs, DEPTH, k), k
            refs[(DEPTH, k)] = context_root(k, mans[k], lines)
        for d in range(DEPTH - 1, d0 - 1, -1):
            for p in range(p0 << (d - d0), (p0 + 1) << (d - d0)):
                v = pv[(d, p)]
                lines.append(f"theorem t{d}_{p} : {feas(top_path(ctxs, d, p))} :=")
                lines.append(f"  split_pm {PARAMS} {M0} {lean_path(top_path(ctxs, d, p))} {v} "
                             f"{refs[(d + 1, 2 * p)]} {refs[(d + 1, 2 * p + 1)]}")
                refs[(d, p)] = f"t{d}_{p}"
        lines.append(f"theorem root : {feas(top_path(ctxs, d0, p0))} := {refs[(d0, p0)]}")
        lines += ["#print axioms root", f"end {PREFIX}.{name}"]
        nm = name
    else:
        ds = args.root
        imports = [f"{PREFIX}.S{ds}_{p}" for p in range(1 << ds)]
        lines = header(PREFIX, imports)
        refs = {(ds, p): f"{PREFIX}.S{ds}_{p}.root" for p in range(1 << ds)}
        for d in range(ds - 1, -1, -1):
            for p in range(1 << d):
                v = pv[(d, p)]
                lines.append(f"theorem t{d}_{p} : {feas(top_path(ctxs, d, p))} :=")
                lines.append(f"  split_pm {PARAMS} {M0} {lean_path(top_path(ctxs, d, p))} {v} "
                             f"{refs[(d + 1, 2 * p)]} {refs[(d + 1, 2 * p + 1)]}")
                refs[(d, p)] = f"t{d}_{p}"
        lines.append(f"theorem root : {feas([])} := {refs[(0, 0)]}")
        lines += ["#print axioms root", f"end {PREFIX}"]
        nm = "Root"
    path = out / f"{nm}.lean"
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text("\n".join(lines) + "\n")
    tmp.replace(path)
    print(json.dumps({"module": f"{PREFIX}.{nm}", "file": str(path), "imports": len(imports), "lines": len(lines)}))


if __name__ == "__main__":
    main()
