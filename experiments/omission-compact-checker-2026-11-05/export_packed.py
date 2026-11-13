#!/usr/bin/env python3
"""Export omission-tree chunks for the compact reflective checker.

Writes (1) a catalog module `CompactChecker/<Catalog>.lean` holding the row
catalog as a binary trie of (support list, demand) pairs plus its one-time
well-formedness theorem, and (2) per-chunk modules that state the chunk's
`checkPacked ... = true` by `decide +kernel` and derive the exclusion with
`CompactChecker.checkPacked_sound`.

A chunk is the subtree under one node of the tree; its context (missing and
occupied states on the path from the root) becomes the initial mask. Leaves are
normalized exactly as in scripts/omission_lean_export.normalize_leaf (zero weights
and rows already satisfied by the missing states are dropped), and every leaf is
replayed here with the same full-load margin that the Lean checker evaluates.
Each leaf entry is the small natural number row * K + weight.
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


def trie(rows_with_index, base=None):
    """Binary trie by row bits; with base, rows carry their packed code (FCat)."""
    T = "FCat" if base else "Cat"
    if not rows_with_index:
        return f"{T}.empty"
    if len(rows_with_index) == 1:
        support, demand = rows_with_index[0]
        # the code is a small term, evaluated (and cached) by the kernel, not a literal
        code = f" (codeL {base} [{', '.join(map(str, support))}])" if base else ""
        return f"({T}.row [{', '.join(map(str, support))}] {demand}{code})"
    return (f"({T}.node {trie(rows_with_index[0::2], base)}\n  {trie(rows_with_index[1::2], base)})")


def flat_trie(rows, name, base):
    """Flat definitions (one per row and per trie node): avoids deep nested terms,
    whose parsing is superlinear."""
    T = "FCat" if base else "Cat"
    defs = []

    def build(items, path):
        if not items:
            return f"{T}.empty"
        if len(items) == 1:
            r, (support, demand) = items[0]
            sup = "[" + ", ".join(map(str, support)) + "]"
            code = f" (codeL {base} {sup})" if base else ""
            nm = f"{name}_r{r}"
            defs.append(f"noncomputable def {nm} : {T} := {T}.row {sup} {demand}{code}")
            return nm
        left = build(items[0::2], path + "0")
        right = build(items[1::2], path + "1")
        nm = f"{name}_n{path}" if path else name
        defs.append(f"noncomputable def {nm} : {T} := {T}.node {left} {right}")
        return nm

    top = build(list(enumerate(rows)), "")
    assert top == name
    return defs


def catalog_source(n, rows, name, source_hash, base=None):
    lines = ["import CompactChecker.Fast" if base else "import CompactChecker.Packed",
             "namespace CompactChecker",
             f"-- Literal omission rows; source SHA-256: {source_hash}",
             f"-- {len(rows)} rows over {n} states, as a binary trie indexed by row bits.",
             *flat_trie(rows, name, base),
             f"theorem {name}_wf : {name}.wf {n}{' ' + str(base) if base else ''} = true := by decide +kernel",
             f"#print axioms {name}_wf",
             "end CompactChecker"]
    return "\n".join(lines) + "\n"


def catalog_source_nested(n, rows, name, source_hash, base=None):
    lines = ["import CompactChecker.Fast" if base else "import CompactChecker.Packed",
             "namespace CompactChecker",
             f"-- Literal omission rows; source SHA-256: {source_hash}",
             f"-- {len(rows)} rows over {n} states, as a binary trie indexed by row bits.",
             "set_option maxRecDepth 100000 in",
             f"noncomputable def {name} : {'FCat' if base else 'Cat'} :=", "  " + trie(rows, base),
             f"theorem {name}_wf : {name}.wf {n}{' ' + str(base) if base else ''} = true := by decide +kernel",
             f"#print axioms {name}_wf",
             "end CompactChecker"]
    return "\n".join(lines) + "\n"


def lit(x, raw):
    return f"(nat_lit {x})" if raw else str(x)


def tree_term(j, nodes, rows, ctx, counts, K, blocks, block_limit, raw, corrupt):
    """Term for node j; subtrees with <= block_limit leaves become named blocks."""
    node = nodes[j]
    if node["type"] == "branch":
        if counts[j] <= block_limit and j not in blocks.get("_top", ()):
            name = f"b{j}"
            blocks["defs"].append((name, inner_term(j, nodes, rows, ctx, K, raw, corrupt)))
            return name
        z = tree_term(node["zero"], nodes, rows, ctx, counts, K, blocks, block_limit, raw, corrupt)
        o = tree_term(node["one"], nodes, rows, ctx, counts, K, blocks, block_limit, raw, corrupt)
        return f"(.split {node['vertex']} {z} {o})"
    return inner_term(j, nodes, rows, ctx, K, raw, corrupt)


def inner_term(j, nodes, rows, ctx, K, raw, corrupt):
    node = nodes[j]
    if node["type"] == "branch":
        z = inner_term(node["zero"], nodes, rows, ctx, K, raw, corrupt)
        o = inner_term(node["one"], nodes, rows, ctx, K, raw, corrupt)
        return f"(.split {node['vertex']} {z} {o})"
    if node["type"] == "over_budget":
        return ".overBudget"
    entries = normalize(rows, node, ctx[j][0])
    if j in corrupt:
        k, w = corrupt[j]
        entries = list(entries)
        entries[k] = (entries[k][0], w)
    codes = []
    for r, w in entries:
        if not 0 <= w < K:
            raise ValueError(f"weight {w} does not fit below K={K}")
        codes.append(r * K + w)
    if PER_WORD > 1:
        J = WORD_J
        assert all(c < J for c in codes)
        codes = codes + [0] * (-len(codes) % PER_WORD)  # padding entries: row 0, weight 0
        words = [sum(codes[i + t] * J ** t for t in range(PER_WORD))
                 for i in range(0, len(codes), PER_WORD)]
        return (f"(.leaf {lit(node['capacity'], raw)} (expandW {J} {PER_WORD} "
                f"[{', '.join(lit(x, raw) for x in words)}]))")
    return f"(.leaf {lit(node['capacity'], raw)} [{', '.join(lit(c, raw) for c in codes)}])"


def blocked_source(j, nodes, rows, ctx, counts, args, n, budget, base, mask,
                   corrupt, missing, occupied, leaf_ids):
    """One decide +kernel per block of <= block_limit leaves; blocks are combined
    at the Prop level by split_feas, so no leaf is evaluated twice."""
    cat, m, K = args.catalog_name, len(rows), args.K
    blocks, uppers = [], []

    def part(x):
        if counts[x] <= args.block_limit or nodes[x]["type"] != "branch":
            blocks.append(x)
        else:
            uppers.append(x)
            part(nodes[x]["zero"])
            part(nodes[x]["one"])

    part(j)
    ns = f"CompactChecker.Chunk{j}{args.suffix}"
    lines = [f"import CompactChecker.{cat[0].upper()}{cat[1:]}",
             "import CompactChecker.Split",
             *(["import CompactChecker.WordPack"] if PER_WORD > 1 else []),
             "open CompactChecker",
             "set_option maxRecDepth 100000",
             *(["set_option profiler true"] if args.profile else []),
             f"namespace {ns}",
             f"-- subtree root node {j}: {len(leaf_ids)} leaves in {len(blocks)} blocks; budget {budget}",
             f"-- context missing={sorted(missing)} occupied={sorted(occupied)}",
             f"noncomputable def mask{j} : List ℕ := [{', '.join(map(str, mask))}]"]
    for u in uppers:  # preorder: parents first
        v = nodes[u]["vertex"]
        lines.append(f"noncomputable def mask{nodes[u]['zero']} : List ℕ := mask{u}.set {v} 2")
        lines.append(f"noncomputable def mask{nodes[u]['one']} : List ℕ := mask{u}.set {v} 1")
    feas = lambda x: f"¬ ∃ holes : Fin {n} → ℕ, FFeas {cat} {m} {n} {budget} mask{x} holes"
    for b in blocks:
        lines.append(f"noncomputable def b{b} : PTree := "
                     f"{inner_term(b, nodes, rows, ctx, K, args.raw, corrupt)}")
        lines.append(f"theorem chk{b} : checkF {cat} {m} {n} {budget} {base} {K} b{b} mask{b} = true := by decide +kernel")
        lines.append(f"theorem ex{b} : {feas(b)} :=")
        lines.append(f"  checkF_feas {cat} {m} {n} {budget} {base} {K} {cat}_wf b{b} mask{b} chk{b}")
    for u in reversed(uppers):  # children before parents
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
    return lines


PER_WORD, WORD_J = 1, 1 << 29


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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path)
    ap.add_argument("tree", type=Path)
    ap.add_argument("--out", type=Path, required=True, help="directory containing CompactChecker/")
    ap.add_argument("--catalog-name", default="cat62")
    ap.add_argument("--write-catalog", action="store_true")
    ap.add_argument("--chunk", type=int, action="append", default=[],
                    help="target leaf count of a chunk (subtree); repeatable")
    ap.add_argument("--root", type=int, help="explicit subtree root node (overrides --chunk)")
    ap.add_argument("--K", type=int, default=1 << 17)
    ap.add_argument("--block-limit", type=int, default=64)
    ap.add_argument("--raw", action="store_true", help="emit nat_lit raw literals")
    ap.add_argument("--corrupt", action="store_true",
                    help="change one leaf weight so that the Python replay fails")
    ap.add_argument("--suffix", default="")
    ap.add_argument("--fast", action="store_true", help="FCat catalog + checkF (Fast.lean)")
    ap.add_argument("--blocks", action="store_true", help="one decide per block, Prop-level combination")
    ap.add_argument("--profile", action="store_true", help="emit set_option profiler true")
    ap.add_argument("--per-word", type=int, default=1, help="entries per Nat word (expandW)")
    args = ap.parse_args()
    global PER_WORD
    PER_WORD = args.per_word

    data = read_json(args.source)
    cert = read_json(args.tree)
    source_hash = sha256(args.source)
    assert cert["source_sha256"] == source_hash, "tree/source hash mismatch"
    n, rows = read_rows(data)
    nodes, budget, root = cert["nodes"], cert["hole_budget"], cert["root"]
    counts, ctx, order = annotate(nodes, root)
    largest = max(sum(w for _, w in nd["weights"]) for nd in nodes if nd["type"] == "weighted")
    base = 1 << max(1, largest.bit_length())
    cdir = args.out / "CompactChecker"
    cdir.mkdir(parents=True, exist_ok=True)
    report = {"source_sha256": source_hash, "tree_sha256": sha256(args.tree), "states": n,
              "rows": len(rows), "budget": budget, "base": base, "K": args.K,
              "exporter_sha256": sha256(__file__), "chunks": []}
    if args.write_catalog:
        path = cdir / f"{args.catalog_name[0].upper()}{args.catalog_name[1:]}.lean"
        path.write_text(catalog_source(n, rows, args.catalog_name, source_hash,
                                       base if args.fast else None))
        report["catalog"] = str(path)
    roots = [args.root] if args.root is not None else [choose_root(counts, order, t) for t in args.chunk]
    for j in roots:
        missing, occupied = ctx[j]
        leaf_ids = leaves_under(j, nodes)
        margins = {}
        for k in leaf_ids:
            nd = nodes[k]
            m, o = ctx[k]
            if nd["type"] == "over_budget":
                assert len(m) > budget
                continue
            assert nd["type"] == "weighted"
            ent = normalize(rows, nd, m)
            margins[k] = full_load_margin(n, rows, budget, m, o, nd["capacity"], ent)
            assert margins[k] > 0, (k, margins[k])
        corrupt = {}
        if args.corrupt:
            # smallest-margin leaf; first entry change (+-1 weight, then 0) that breaks it
            rng = random.Random(0)
            for k in sorted(margins, key=lambda k: margins[k]):
                nd = nodes[k]
                m, o = ctx[k]
                ent = normalize(rows, nd, m)
                found = None
                for e in range(len(ent)):
                    for w in (ent[e][1] - 1, ent[e][1] + 1, 0):
                        if w < 0:
                            continue
                        trial = list(ent)
                        trial[e] = (trial[e][0], w)
                        mg = full_load_margin(n, rows, budget, m, o, nd["capacity"], trial)
                        if mg <= 0:
                            found = (e, w, mg)
                            break
                    if found:
                        break
                if found:
                    corrupt[k] = (found[0], found[1])
                    report["corruption"] = {"leaf_node": k, "entry_index": found[0],
                                            "row": ent[found[0]][0],
                                            "old_weight": ent[found[0]][1],
                                            "new_weight": found[1],
                                            "old_margin": margins[k], "new_margin": found[2]}
                    break
            assert corrupt, "no single-weight corruption found"
        mask = [0] * n
        for i in missing:
            mask[i] = 1
        for i in occupied:
            mask[i] = 2
        if args.blocks:
            assert args.fast
            lines = blocked_source(j, nodes, rows, ctx, counts, args, n, budget, base, mask,
                                   corrupt, missing, occupied, leaf_ids)
            name = f"Chunk{j}{args.suffix}"
            path = cdir / f"{name}.lean"
            path.write_text("\n".join(lines) + "\n")
            report["chunks"].append({"module": f"CompactChecker.{name}", "file": str(path),
                                     "root": j, "leaves": len(leaf_ids),
                                     "min_margin": min(margins.values()) if margins else None,
                                     "missing": sorted(missing), "occupied": sorted(occupied),
                                     "source_bytes": path.stat().st_size, "blocks": True,
                                     "block_limit": args.block_limit,
                                     "raw_literals": args.raw, "corrupted": bool(corrupt),
                                     "sha256": sha256(path)})
            continue
        blocks = {"defs": []}
        top = tree_term(j, nodes, rows, ctx, counts, args.K, blocks, args.block_limit,
                        args.raw, corrupt)
        name = f"Chunk{j}{args.suffix}"
        ns = f"CompactChecker.{name}"
        cat = args.catalog_name
        lines = [f"import CompactChecker.{cat[0].upper()}{cat[1:]}",
                 "open CompactChecker",
                 "set_option maxRecDepth 100000",
                 *(["set_option profiler true"] if args.profile else []),
                 f"namespace {ns}",
                 f"-- subtree root node {j}: {len(leaf_ids)} leaves; budget {budget}",
                 f"-- context missing={sorted(missing)} occupied={sorted(occupied)}"]
        for bname, term in blocks["defs"]:
            lines.append(f"noncomputable def {bname} : PTree := {term}")
        lines.append(f"noncomputable def tree : PTree := {top}")
        lines.append(f"noncomputable def mask : List ℕ := [{', '.join(map(str, mask))}]")
        if args.fast:
            call = f"checkF {cat} {len(rows)} {n} {budget} {base} {args.K} tree mask"
            demand_t, supp_t = f"{cat}.dem r.val", f"fsupp {cat} {n} r.val"
            sound = f"checkF_sound {cat} {len(rows)} {n} {budget} {base} {args.K} {cat}_wf tree mask check"
        else:
            call = f"checkPacked {cat} {len(rows)} {n} {budget} {base} {args.K} mask tree"
            demand_t, supp_t = f"dem {cat} r.val", f"supp {cat} {n} r.val"
            sound = f"checkPacked_sound {cat} {len(rows)} {n} {budget} {base} {args.K} {cat}_wf tree mask check"
        lines += [f"theorem check : {call} = true := by decide +kernel",
                  "theorem excludes :",
                  f"    ¬ ∃ holes : Fin {n} → ℕ, (∀ i, holes i ≤ 1) ∧",
                  f"      (∀ r : Fin {len(rows)}, {demand_t} ≤ ∑ i ∈ {supp_t}, holes i) ∧",
                  f"      (∑ i, holes i) ≤ {budget} ∧",
                  f"      (∀ i ∈ mset {n} mask 1, holes i = 1) ∧ (∀ i ∈ mset {n} mask 2, holes i = 0) :=",
                  f"  {sound}",
                  "#print axioms excludes",
                  f"end {ns}"]
        path = cdir / f"{name}.lean"
        path.write_text("\n".join(lines) + "\n")
        report["chunks"].append({"module": f"CompactChecker.{name}", "file": str(path),
                                 "root": j, "leaves": len(leaf_ids),
                                 "entries": sum(len(normalize(rows, nodes[k], ctx[k][0]))
                                                for k in leaf_ids if nodes[k]["type"] == "weighted"),
                                 "min_margin": min(margins.values()) if margins else None,
                                 "missing": sorted(missing), "occupied": sorted(occupied),
                                 "source_bytes": path.stat().st_size,
                                 "raw_literals": args.raw, "corrupted": bool(corrupt),
                                 "sha256": sha256(path)})
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()
