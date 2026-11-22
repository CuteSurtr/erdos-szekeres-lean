#!/usr/bin/env python3
"""s3520-gate (22 Nov 2026): slice_export_w13.py with the context-id fix only (contexts are the sorted placeholder ids,
which need not be 0..K-1: bb-s1 of s35_20 has no context 4782). The reference for the byte-identity controls of
slice_export_v3.py. Otherwise unchanged.
res-slices-fv w13 (22 Nov 2026 evening): slice_export.py with export_es310_w13 (13-bit row digits, J = K << 13, for
catalogs of up to 8,191 rows such as s35_20's 4,642). Otherwise unchanged.
res-slices-fv (22 Nov 2026): export one residual slice tree (master + contexts) as Fast2 chunk modules.
NOTHING HERE PROVES ANYTHING: Lean decides every module; this only writes the texts.

  slice_export.py TAG --budget B --master M --ctxdir DIR --extra EXTRA --out OUT
                  [--unit-leaves U] [--chunk-leaves L] [--block-leaves 64] [--per-word 16] [--units A:B]
                  [--corrupt K:MM] [--no-profile]

1. Rows: source-2650 (raw sha256 pinned) followed by EXTRA in file order (the slice's rows.txt order).
2. Master: budget B, root 0. A traversal from the root (state 0 occupied there) gives every context placeholder its
   path; the context ids must be 0..K-1, once each. A pre-pass reads each context file once (header context = k,
   root 0, missing / occupied = the placeholder's path literals with state 0 occupied), counts its leaves and hashes it.
3. Units: top-down cut of the master, placeholders weighted by their leaf counts, into subtrees of at most U leaves
   (a placeholder is never split). Unit u is the master subtree at a cut node with its contexts grafted in, renumbered
   zero-first preorder; units are numbered in preorder.
4. Each unit goes through export_es310.export_context UNCHANGED (zero-first preorder renumbering, both exact leaf
   replays, module and block cut, line-shape check) with base path = the unit's master path followed by (0, 2) (state
   0 occupied), catalog RS.Cat<TAG> (fcatS<TAG>, catalog base 131072), 154 states, len(rows) rows, budget B, prefix
   RS<TAG>. The header comment that names ES(8) <= 310 is replaced and the shape check run again. Writes
   OUT/src/RS<TAG>/C<uuuu><mm>.lean, then OUT/ctx/ctx-<uuuu>.json LAST (it means "unit u is exported"); an existing
   manifest with the same unit fingerprint is skipped.
5. OUT/skeleton.json: the master nodes above the cut (vertex, children, Lean path) and the unit of each cut node.
"""
import argparse
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

X = Path("/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05")
sys.path.insert(0, str(X))
import shapes_es311  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))   # res-slices-fv w13: the widened copy lives in tools/
import export_es310_w13 as E  # noqa: E402
from export_es311 import read_source, cut  # noqa: E402

SOURCE = Path("/home/jay/research/data/es308-20261114/inputs/source-2650.json.gz")
SOURCE_RAW_SHA = "e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6"
OLD = "-- ES(8) <= 310 compact check (budget-64 campaign), balanced side, context"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write_atomic(path, data):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


class Ctx:
    """Context files, read one at a time and checked against the pre-pass hash."""

    def __init__(self, ctxdir):
        self.dir, self.sha = Path(ctxdir), {}

    def load(self, k, path=None):
        gz = (self.dir / f"ctx-{k}.json.gz").read_bytes()
        h = sha(gz)
        if k in self.sha and self.sha[k] != h:
            raise E.Refuse(f"context {k} changed since the pre-pass")
        self.sha[k] = h
        d = json.loads(gzip.decompress(gz))
        if d.get("context") != k or d.get("root") != 0:
            raise E.Refuse(f"context {k}: header context/root differ")
        if path is not None:
            mis = sorted(v for v, b in path if b == 1)
            occ = sorted([0] + [v for v, b in path if b == 0])
            if sorted(d["missing"]) != mis or sorted(d["occupied"]) != occ:
                raise E.Refuse(f"context {k}: missing/occupied differ from its master path")
        return d["nodes"]


def master_paths(nodes):
    """Placeholder paths (root-first [v, b]), node count, and a reachability check."""
    seen, paths, stack = set(), {}, [(0, [])]
    while stack:
        i, p = stack.pop()
        if i in seen:
            raise E.Refuse(f"master node {i} reached twice")
        seen.add(i)
        nd = nodes[i]
        t = nd["type"]
        if t == "branch":
            v = nd["vertex"]
            if v == 0 or v in {x for x, _ in p}:
                raise E.Refuse(f"master node {i} branches on a fixed state {v}")
            stack.append((nd["one"], p + [[v, 1]]))
            stack.append((nd["zero"], p + [[v, 0]]))
        elif t == "context":
            k = nd["context"]
            if k in paths:
                raise E.Refuse(f"context {k} placed twice")
            paths[k] = (i, p)
        elif t not in ("weighted", "over_budget"):
            raise E.Refuse(f"master node {i} has type {t!r}")
    if len(seen) != len(nodes):
        raise E.Refuse("unreachable master nodes")
    return paths


def build_unit(t, nodes, ctx, kpath):
    """The unit's nodes, zero-first preorder, contexts grafted in."""
    out, stack = [], [(None, t, -1, None)]
    visited = set()
    while stack:
        src, i, par, side = stack.pop()              # src: None (master) or (k, nodes of context k)
        if src is None and nodes[i]["type"] == "context":
            k = nodes[i]["context"]
            src = (k, ctx.load(k, kpath[k]))
            i = 0
        cur = nodes if src is None else src[1]
        key = (-1 if src is None else src[0], i)
        if key in visited:
            raise E.Refuse("a node is reached twice while grafting")
        visited.add(key)
        nd = cur[i]
        me = len(out)
        if par >= 0:
            out[par][side] = me
        if nd["type"] == "branch":
            out.append({"type": "branch", "vertex": nd["vertex"], "zero": None, "one": None})
            stack.append((src, nd["one"], me, "one"))
            stack.append((src, nd["zero"], me, "zero"))
        else:
            out.append(nd)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tag")
    ap.add_argument("--budget", type=int, required=True)
    ap.add_argument("--master", type=Path, required=True)
    ap.add_argument("--ctxdir", type=Path, required=True)
    ap.add_argument("--extra", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--unit-leaves", type=int, default=300000)
    ap.add_argument("--chunk-leaves", type=int, default=8000)
    ap.add_argument("--block-leaves", type=int, default=64)
    ap.add_argument("--per-word", type=int, default=16)
    ap.add_argument("--units")
    ap.add_argument("--corrupt")
    ap.add_argument("--no-profile", action="store_true")
    args = ap.parse_args()
    tag, B = args.tag, args.budget
    ssha, n, rows = read_source(SOURCE)
    assert ssha == SOURCE_RAW_SHA and n == 154 and len(rows) == 2650, (ssha, n, len(rows))
    xraw = args.extra.read_bytes()
    for r in json.loads(xraw):
        s = r["support"]
        assert len(set(s)) == len(s) and all(type(i) is int and 0 <= i < n for i in s) and 0 <= r["rhs"] <= len(s)
        rows.append((tuple(s), r["rhs"]))
    E.BUDGET, E.N_STATES, E.N_ROWS = B, n, len(rows)
    E.CATMOD, E.CAT, E.CATALOG_BASE = f"RS.Cat{tag}", f"fcatS{tag}", 131072
    E.SKEL_STRIDE = 1 << 62                      # skeleton ids are only named k<u>_<id> by root_slice.py
    shapes_es311.CATALOGS[E.CATMOD] = E.CAT
    prefix = f"RS{tag}"
    sp = shapes_es311.side_params({"catalog": E.CATMOD, "rows": len(rows), "states": n, "budget": B,
                                   "catalog_base": E.CATALOG_BASE, "prefix": prefix})
    mraw = args.master.read_bytes()
    master = json.loads(mraw)
    if master.get("budget") != B or master.get("root") != 0:
        raise E.Refuse("master budget/root differ")
    nodes = master["nodes"]
    kpath = {}
    for k, (i, p) in master_paths(nodes).items():
        kpath[k] = p
    K = len(kpath)
    ids = sorted(kpath)                          # s3520-gate: the placeholder ids, not range(K)
    if any(type(k) is not int or k < 0 for k in ids) or master.get("contexts", K) != K:
        raise E.Refuse("context ids are not distinct non-negative integers, or their number differs")
    out = args.out
    (out / "src" / prefix).mkdir(parents=True, exist_ok=True)
    (out / "ctx").mkdir(parents=True, exist_ok=True)
    ctx = Ctx(args.ctxdir)
    pre = out / "prepass.json"
    if pre.exists() and json.loads(pre.read_text()).get("master_sha256") == sha(mraw):
        pp = json.loads(pre.read_text())
        kleaves = {int(k): v for k, v in pp["leaves"].items()}
        ctx.sha = {int(k): v for k, v in pp["gz_sha256"].items()}
    else:
        kleaves = {}
        for k in ids:
            cn = ctx.load(k, kpath[k])
            kleaves[k] = sum(1 for x in cn if x["type"] != "branch")
            del cn
        pp = {"master": str(args.master), "master_sha256": sha(mraw), "contexts": K,
              "leaves": kleaves, "gz_sha256": ctx.sha,
              "contexts_digest": sha("".join(f"{k} {ctx.sha[k]}\n" for k in ids).encode())}
        write_atomic(pre, json.dumps(pp).encode())
    # leaf counts of the master subtrees (post-order over an explicit preorder list)
    order, stack = [], [0]
    while stack:
        i = stack.pop()
        order.append(i)
        if nodes[i]["type"] == "branch":
            stack.append(nodes[i]["one"])
            stack.append(nodes[i]["zero"])
    cnt = {}
    for i in reversed(order):
        nd = nodes[i]
        cnt[i] = (cnt[nd["zero"]] + cnt[nd["one"]] if nd["type"] == "branch"
                  else kleaves[nd["context"]] if nd["type"] == "context" else 1)
    total = cnt[0]
    # the cut: tops in preorder (zero first), uppers above them
    tops, uppers, stack, mpath = [], [], [0], {0: []}
    while stack:
        i = stack.pop()
        nd = nodes[i]
        if nd["type"] != "branch" or cnt[i] <= args.unit_leaves:
            tops.append(i)
            continue
        uppers.append(i)
        v = nd["vertex"]
        mpath[nd["one"]] = mpath[i] + [[v, 1]]
        mpath[nd["zero"]] = mpath[i] + [[v, 0]]
        stack.append(nd["one"])
        stack.append(nd["zero"])
    unit_of = {t: u for u, t in enumerate(tops)}

    def lean_path(p):                            # root-first [v, b] -> innermost first (v, 2|1), then (0, 2)
        return [(v, 2 if b == 0 else 1) for v, b in reversed(p)] + [(0, 2)]

    skel = {"tag": tag, "budget": B, "rows": len(rows), "states": n, "total_leaves": total, "units": len(tops),
            "master_sha256": sha(mraw), "contexts_digest": pp["contexts_digest"], "extra_sha256": sha(xraw),
            "source_raw_sha256": ssha, "unit_leaves": args.unit_leaves,
            "tops": [{"node": t, "unit": unit_of[t], "leaves": cnt[t], "path": lean_path(mpath[t])} for t in tops],
            "uppers": [{"node": i, "vertex": nodes[i]["vertex"], "zero": nodes[i]["zero"], "one": nodes[i]["one"],
                        "path": lean_path(mpath[i])} for i in uppers]}
    if args.corrupt is None:
        write_atomic(out / "skeleton.json", json.dumps(skel, indent=0).encode())
    sel = range(len(tops))
    if args.units:
        a, b = map(int, args.units.split(":"))
        sel = range(a, min(b, len(tops)))
    cmod = None
    if args.corrupt:
        cu, cmod = map(int, args.corrupt.split(":"))
        sel = [cu]
    args.corrupt = cmod
    code_caches, refused = {}, []
    for u in sel:
        t0 = time.time()
        t = tops[u]
        fp = sha(json.dumps([skel["master_sha256"], skel["contexts_digest"], skel["extra_sha256"], ssha, B,
                             t, mpath[t], args.chunk_leaves, args.block_leaves, args.per_word, cmod]).encode())
        man = out / "ctx" / f"ctx-{u:04d}.json"
        if man.exists() and json.loads(man.read_text()).get("fingerprint") == fp:
            continue
        try:
            sub = build_unit(t, nodes, ctx, kpath)
            ctxline = {"path": [[0, 0]] + mpath[t]}
            hashes = {"gz": skel["master_sha256"], "json": skel["contexts_digest"], "result": "-", "source": ssha}
            texts, info = E.export_context(u, ctxline, {"nodes": sub}, rows, args, prefix, code_caches, hashes)
            del sub
            assert info["base_path"] == [list(x) for x in lean_path(mpath[t])], "base path differs"
            new = f"-- res-slices-fv residual slice check (Res118 slice B={B}), unit"
            out_texts = []
            for (stem, data), m in zip(texts, info["modules"]):
                text = data.decode("utf-8")
                if text.count(OLD) != 1:
                    raise E.Refuse(f"unit {u}: header comment not found once in {stem}")
                text = text.replace(OLD, new)
                errs = shapes_es311.check_text(text, "chunk", m["module"], sp)
                if errs:
                    raise E.Refuse(f"unit {u}: {stem} fails the shape check: {errs}")
                b = text.encode("utf-8")
                m["sha256"], m["source_bytes"] = sha(b), len(b)
                out_texts.append((stem, b))
            for stem, b in out_texts:
                write_atomic(out / "src" / prefix / f"{stem}.lean", b)
            info.update({"unit": u, "top": t, "fingerprint": fp, "leaves_expected": cnt[t],
                         "exporter_sha256": sha(Path(__file__).read_bytes()),
                         "export_es310_sha256": sha((Path(__file__).resolve().parent / "export_es310_w13.py").read_bytes()),
                         "params": {"budget": B, "per_word": args.per_word, "chunk_leaves": args.chunk_leaves,
                                    "block_leaves": args.block_leaves, "catalog": E.CATMOD, "rows": len(rows),
                                    "catalog_base": E.CATALOG_BASE}, "seconds": round(time.time() - t0, 1)})
            if info["stats"]["leaves"] != cnt[t]:
                raise E.Refuse(f"unit {u}: {info['stats']['leaves']} leaves, expected {cnt[t]}")
            write_atomic(man, json.dumps(info, separators=(",", ":")).encode())
            print(json.dumps({"unit": u, "modules": len(info["modules"]), "leaves": info["stats"]["leaves"],
                              "min_margin": info["stats"]["min_margin"], "seconds": info["seconds"],
                              "corrupted": info["corruption"]}), flush=True)
        except E.Refuse as e:
            refused.append(u)
            print(json.dumps({"unit": u, "refused": str(e)}), flush=True)
    sys.exit(1 if refused else 0)


if __name__ == "__main__":
    main()
