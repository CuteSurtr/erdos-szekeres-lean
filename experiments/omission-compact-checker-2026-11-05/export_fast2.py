#!/usr/bin/env python3
"""Export omission-tree chunks for the fused checker `checkF2` (CompactChecker/Fast2.lean).

The catalog module (FCat, e.g. Fcat62.lean) is the one written by export_packed.py
--fast --write-catalog; this script only writes chunk modules. A chunk is the
subtree under one node; its path context becomes the initial mask. Subtrees of at
most --block-limit leaves are checked by one `decide +kernel` each and combined
with `split_feas`, as in export_packed.py --blocks.

Leaves are normalized as in scripts/omission_lean_export.normalize_leaf (zero
weights and rows already satisfied by the missing states are dropped). Each entry
is row * K + weight; --per-word entries are packed into one word in base
J = K * 2^bits(rows), least significant first, and the word list is written with
`natlits%` (raw literals). Padding entries are 0 (row 0, weight 0).

Every leaf is replayed here twice: with the full-load margin of export_packed.py,
and with a Python transcription of the Lean leaf test of Fast2.lean (fused sum,
`Q / base^n < base`, digit loop), so an encoding error shows up before Lean runs.
"""
import argparse
import hashlib
import json
import lzma
import random
import sys
from pathlib import Path


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    path = Path(path)
    raw = path.read_bytes()
    if path.suffix == ".xz":
        raw = lzma.decompress(raw)
    return json.loads(raw)


def read_rows(data):
    n = len(data["states"])
    rows = [(row["support"], row["rhs"]) for row in data["constraints"]]
    for support, demand in rows:
        assert len(set(support)) == len(support)
        assert all(type(i) is int and 0 <= i < n for i in support)
        assert type(demand) is int and 0 <= demand <= len(support)
    return n, rows


def annotate(nodes, root):
    """Leaf counts and (missing, occupied) contexts for every node."""
    counts, ctx, order = {}, {root: ((), ())}, []
    stack = [root]
    while stack:
        j = stack.pop()
        order.append(j)
        node = nodes[j]
        if node["type"] == "branch":
            m, o = ctx[j]
            v = node["vertex"]
            ctx[node["zero"]] = (m, o + (v,))
            ctx[node["one"]] = (m + (v,), o)
            stack.append(node["one"])
            stack.append(node["zero"])
    for j in reversed(order):
        node = nodes[j]
        counts[j] = counts[node["zero"]] + counts[node["one"]] if node["type"] == "branch" else 1
    return counts, ctx, order


def normalize(rows, node, missing):
    missing = set(missing)
    return [(r, w) for r, w in node["weights"]
            if w and rows[r][1] > len(set(rows[r][0]) & missing)]


def full_load_margin(n, rows, budget, missing, occupied, capacity, entries):
    """Exactly the quantity the Lean leaf test compares (rhs - lhs)."""
    loads = [0] * n
    for r, w in entries:
        for i in rows[r][0]:
            loads[i] += w
    missing, occupied = set(missing), set(occupied)
    lhs = capacity * max(0, budget - len(missing))
    for i in range(n):
        if i in missing:
            lhs += loads[i]
        elif i not in occupied:
            lhs += max(0, loads[i] - capacity)
    rhs = sum(w * rows[r][1] for r, w in entries)
    return rhs - lhs


def leaves_under(j, nodes):
    out, stack = [], [j]
    while stack:
        k = stack.pop()
        if nodes[k]["type"] == "branch":
            stack += [nodes[k]["one"], nodes[k]["zero"]]
        else:
            out.append(k)
    return out


def choose_root(counts, order, target):
    best = None
    for j in order:
        c = counts[j]
        if c == target:
            return j
        if c <= target and (best is None or c > counts[best]):
            best = j
    return best


def pack_words(codes, per_word, J):
    codes = codes + [0] * (-len(codes) % per_word)
    return [sum(codes[i + t] * J ** t for t in range(per_word))
            for i in range(0, len(codes), per_word)]


def lean_leaf_test(n, rows, m, budget, base, K, J, k, cap, mask, words):
    """Python transcription of Fast2.leafF2 (exact integers)."""
    BN = base ** n
    Q = 0
    for y in words:
        for _ in range(k):
            e, y = y % J, y // J
            r, w = e // K, e % K
            if r < m and rows[r][1] > 0:
                Q += w * (sum(base ** i for i in rows[r][0]) + BN * rows[r][1])
    big = (n + 1) * base
    X, p = 0, Q
    for i in range(n):
        v = mask[i] if i < len(mask) else 0
        c, p = p % base, p // base
        X += c + big if v == 1 else 0 if v == 2 else max(0, c - cap)
    T = Q // BN
    return 1 < base and T < base and cap * max(0, budget - X // big) + X % big < T


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path)
    ap.add_argument("tree", type=Path)
    ap.add_argument("--out", type=Path, required=True, help="directory containing CompactChecker/")
    ap.add_argument("--catalog-name", default="fcat62")
    ap.add_argument("--catalog-base", type=int, default=1 << 22,
                    help="base of the catalog's own wf theorem (fcat62_wf)")
    ap.add_argument("--base", type=int, default=0,
                    help="leaf base; default: least power of 2 above every leaf's demand sum in the tree")
    ap.add_argument("--chunk", type=int, help="target leaf count of the chunk (subtree)")
    ap.add_argument("--root", type=int, help="explicit subtree root node (overrides --chunk)")
    ap.add_argument("--K", type=int, default=1 << 17)
    ap.add_argument("--per-word", type=int, default=4)
    ap.add_argument("--block-limit", type=int, default=64)
    ap.add_argument("--corrupt", action="store_true",
                    help="change one leaf weight so that the Python replay fails")
    ap.add_argument("--suffix", default="G")
    ap.add_argument("--profile", action="store_true", help="emit set_option profiler true")
    ap.add_argument("--ofnat", action="store_true",
                    help="write words as ordinary literals instead of natlits%% (for comparison)")
    args = ap.parse_args()

    data = read_json(args.source)
    cert = read_json(args.tree)
    source_hash = sha256(args.source)
    assert cert["source_sha256"] == source_hash, "tree/source hash mismatch"
    n, rows = read_rows(data)
    m = len(rows)
    nodes, budget, root = cert["nodes"], cert["hole_budget"], cert["root"]
    counts, ctx, order = annotate(nodes, root)

    K = args.K
    J = K << m.bit_length()
    max_d, max_w = 0, 0
    for k, nd in enumerate(nodes):
        if nd["type"] == "weighted":
            ent = normalize(rows, nd, ctx[k][0])
            max_d = max(max_d, sum(w * rows[r][1] for r, w in ent))
            max_w = max(max_w, max((w for _, w in ent), default=0))
    base = args.base or 1 << max(1, max_d.bit_length())
    assert base > max_d and base > 1, (base, max_d)
    assert max_w < K, (max_w, K)

    j = args.root if args.root is not None else choose_root(counts, order, args.chunk)
    missing, occupied = ctx[j]
    leaf_ids = leaves_under(j, nodes)
    mask = [0] * n
    for i in missing:
        mask[i] = 1
    for i in occupied:
        mask[i] = 2

    margins = {}
    for k in leaf_ids:
        nd = nodes[k]
        mi, oc = ctx[k]
        if nd["type"] == "over_budget":
            assert len(mi) > budget
            continue
        assert nd["type"] == "weighted"
        ent = normalize(rows, nd, mi)
        assert all(rows[r][1] >= 1 for r, _ in ent)
        margins[k] = full_load_margin(n, rows, budget, mi, oc, nd["capacity"], ent)
        assert margins[k] > 0, (k, margins[k])

    corrupt, report_corrupt = {}, None
    if args.corrupt:
        for k in sorted(margins, key=lambda k: margins[k]):
            nd = nodes[k]
            mi, oc = ctx[k]
            ent = normalize(rows, nd, mi)
            for e in range(len(ent)):
                for w in (ent[e][1] - 1, ent[e][1] + 1, 0):
                    if w < 0:
                        continue
                    trial = list(ent)
                    trial[e] = (trial[e][0], w)
                    mg = full_load_margin(n, rows, budget, mi, oc, nd["capacity"], trial)
                    if mg <= 0:
                        corrupt[k] = (e, w)
                        report_corrupt = {"leaf_node": k, "entry_index": e, "row": ent[e][0],
                                          "old_weight": ent[e][1], "new_weight": w,
                                          "old_margin": margins[k], "new_margin": mg}
                        break
                if corrupt:
                    break
            if corrupt:
                break
        assert corrupt, "no single-weight corruption found"

    stats = {"entries": 0, "words": 0, "lean_test_failures": 0}

    def node_mask(x):
        mm = [0] * n
        for i in ctx[x][0]:
            mm[i] = 1
        for i in ctx[x][1]:
            mm[i] = 2
        return mm

    def term(x):
        nd = nodes[x]
        if nd["type"] == "branch":
            return f"(.split {nd['vertex']} {term(nd['zero'])} {term(nd['one'])})"
        if nd["type"] == "over_budget":
            return ".overBudget"
        ent = normalize(rows, nd, ctx[x][0])
        if x in corrupt:
            e, w = corrupt[x]
            ent = list(ent)
            ent[e] = (ent[e][0], w)
        codes = [r * K + w for r, w in ent]
        words = pack_words(codes, args.per_word, J)
        stats["entries"] += len(codes)
        stats["words"] += len(words)
        ok = lean_leaf_test(n, rows, m, budget, base, K, J, args.per_word, nd["capacity"],
                            node_mask(x), words)
        if not ok:
            stats["lean_test_failures"] += 1
            assert x in corrupt, f"Lean leaf test fails on node {x}"
        lst = f"[{', '.join(map(str, words))}]"
        return f"(.leaf {nd['capacity']} {lst if args.ofnat else f'(natlits% {lst})'})"

    blocks, uppers = [], []

    def part(x):
        if counts[x] <= args.block_limit or nodes[x]["type"] != "branch":
            blocks.append(x)
        else:
            uppers.append(x)
            part(nodes[x]["zero"])
            part(nodes[x]["one"])

    part(j)
    cat = args.catalog_name
    name = f"Chunk{j}{args.suffix}"
    ns = f"CompactChecker.{name}"
    params = f"{cat} {m} {n} {budget} {base} {K} {J} {args.per_word}"
    sparams = f"{cat} {m} {n} {budget} {args.catalog_base} {base} {K} {J} {args.per_word}"
    lines = [f"import CompactChecker.{cat[0].upper()}{cat[1:]}",
             "import CompactChecker.Fast2",
             "open CompactChecker",
             "set_option maxRecDepth 100000",
             *(["set_option profiler true"] if args.profile else []),
             f"namespace {ns}",
             f"-- subtree root node {j}: {len(leaf_ids)} leaves in {len(blocks)} blocks; budget {budget}",
             f"-- context missing={sorted(missing)} occupied={sorted(occupied)}",
             f"-- leaf base {base}, K {K}, J {J}, {args.per_word} entries per word",
             f"noncomputable def mask{j} : List ℕ := [{', '.join(map(str, mask))}]"]
    for u in uppers:
        v = nodes[u]["vertex"]
        lines.append(f"noncomputable def mask{nodes[u]['zero']} : List ℕ := mask{u}.set {v} 2")
        lines.append(f"noncomputable def mask{nodes[u]['one']} : List ℕ := mask{u}.set {v} 1")
    feas = lambda x: f"¬ ∃ holes : Fin {n} → ℕ, FFeas {cat} {m} {n} {budget} mask{x} holes"
    for b in blocks:
        lines.append(f"noncomputable def b{b} : PTree := {term(b)}")
        lines.append(f"theorem chk{b} : checkF2 {params} b{b} mask{b} = true := by decide +kernel")
        lines.append(f"theorem ex{b} : {feas(b)} :=")
        lines.append(f"  checkF2_feas {sparams} {cat}_wf b{b} mask{b} chk{b}")
    for u in reversed(uppers):
        v = nodes[u]["vertex"]
        lines.append(f"theorem ex{u} : {feas(u)} :=")
        lines.append(f"  split_feas {cat} {m} {n} {budget} mask{u} {v} ex{nodes[u]['zero']} ex{nodes[u]['one']}")
    lines += ["theorem excludes :",
              f"    ¬ ∃ holes : Fin {n} → ℕ, (∀ i, holes i ≤ 1) ∧",
              f"      (∀ r : Fin {m}, {cat}.dem r.val ≤ ∑ i ∈ fsupp {cat} {n} r.val, holes i) ∧",
              f"      (∑ i, holes i) ≤ {budget} ∧",
              f"      (∀ i ∈ mset {n} mask{j} 1, holes i = 1) ∧ (∀ i ∈ mset {n} mask{j} 2, holes i = 0) :=",
              f"  ex{j}",
              "#print axioms excludes",
              f"end {ns}"]
    path = args.out / "CompactChecker" / f"{name}.lean"
    path.write_text("\n".join(lines) + "\n")
    report = {"source_sha256": source_hash, "tree_sha256": sha256(args.tree), "states": n,
              "rows": m, "budget": budget, "leaf_base": base, "tree_max_demand_sum": max_d,
              "catalog_base": args.catalog_base, "K": K, "J": J, "per_word": args.per_word,
              "raw_literals": not args.ofnat,
              "exporter_sha256": sha256(__file__),
              "chunk": {"module": ns, "file": str(path), "root": j, "leaves": len(leaf_ids),
                        "blocks": len(blocks), "block_limit": args.block_limit,
                        "entries": stats["entries"], "words": stats["words"],
                        "min_margin": min(margins.values()) if margins else None,
                        "lean_test_failures": stats["lean_test_failures"],
                        "missing": sorted(missing), "occupied": sorted(occupied),
                        "source_bytes": path.stat().st_size, "corrupted": bool(corrupt),
                        "corruption": report_corrupt, "sha256": sha256(path)}}
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()
