#!/usr/bin/env python3
"""Export the ES(8) <= 311 certificate trees as Fast2 chunk modules (6 November 2026).

Sides (the two arithmetic facts that Final311/Final.lean consumes):
  balanced  tree-63.json.xz.part-* (budget 63, 3,131 rows, 252 states), export root = node 0,
            catalog fcat62 (CompactChecker/Fcat62.lean, rows of balanced-v2-source.json)
  residual  tree-2650-32.json.xz.part-* (budget 32, 2,650 rows, 154 states), export root = node 1,
            the zero branch of state 0 (path [(0, 2)]), catalog fcat2650 (CompactChecker/Fcat2650.lean)

The tree is streamed twice from the xz parts (it is 1.4 GB of JSON); nothing loads it whole.
Pass 1 keeps only the tree shape (cached in OUT/shape-<sha16>.json.gz, keyed by the sha256 of
the decompressed tree). Nodes are in preorder, so every subtree is a contiguous index range.

Cutting (deterministic, from the shape only):
  * subtree roots (SR): top-down from the export root, a node with at most --chunk-leaves leaves
    (or a leaf) is an SR; above them are the skeleton nodes;
  * modules: consecutive SRs (preorder) packed greedily, at most --chunk-leaves leaves each;
  * blocks: inside an SR, top-down again with --block-leaves; one `decide +kernel` per block.
Every exported statement is `¬ ∃ holes, FFeas cat m n budget (pmask (zerosF n) path) holes`, with
`path` the decisions from that node up to the tree root, innermost first (CompactChecker/Path.lean).
Blocks and SRs combine by `split_pm`; the Root module combines the SRs over the skeleton.

Every exported leaf is replayed here twice, as in export_fast2.py: the exact full-load margin
(must be >= 1) and a transcription of the Lean leaf test of Fast2.lean on the encoded words with
the block's base (must accept). Leaf bases are per block: the least power of 2 above the largest
demand sum of a leaf in the block.

Outputs (OUT = --out):
  OUT/src/<Prefix>/C<idx>.lean  chunk modules (all, or those in --only)
  OUT/src/<Prefix>/Root.lean    the skeleton composition (only when every module is written)
  OUT/manifest-<Prefix>.json    parameters, input hashes, and per module: leaves, SRs, blocks,
                                entries, words, min margin, file sha256
"""
import argparse
import gzip
import hashlib
import json
import lzma
import sys
import time
from array import array
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIDES = {
    "balanced": dict(catalog="fcat62", module="CompactChecker.Fcat62", catalog_base=1 << 22,
                     prefix="E311B", base_path=[]),
    "residual": dict(catalog="fcat2650", module="CompactChecker.Fcat2650", catalog_base=1 << 17,
                     prefix="E311R", base_path=[(0, 2)]),
}
# Sequential elaboration (so that the profiler's per-declaration "type checking" times are the
# kernel's own, not task waiting time) and no linters (about 7% of the time, no logical effect).
OPTS = ["set_option Elab.async false", "set_option linter.all false"]
T_BRANCH, T_WEIGHTED, T_OVER, T_OTHER = 0, 1, 2, 3
TYPES = {"branch": T_BRANCH, "weighted": T_WEIGHTED, "over_budget": T_OVER}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def read_source(path):
    raw = Path(path).read_bytes()
    if str(path).endswith(".gz"):
        raw = gzip.decompress(raw)
    data = json.loads(raw)
    n = len(data["states"])
    rows = []
    for row in data["constraints"]:
        s, d = row["support"], row["rhs"]
        assert len(set(s)) == len(s) and all(type(i) is int and 0 <= i < n for i in s)
        assert type(d) is int and 0 <= d <= len(s)
        rows.append((tuple(s), d))
    return hashlib.sha256(raw).hexdigest(), n, rows


class Stream:
    """Nodes of a (possibly split) xz-compressed tree JSON, one dict at a time."""

    def __init__(self, parts):
        self.files = [open(p, "rb") for p in parts]
        self.fi, self.dec, self.buf, self.pos, self.eof = 0, lzma.LZMADecompressor(), "", 0, False
        self.sha, self.nbytes, self.decoder = hashlib.sha256(), 0, json.JSONDecoder()

    def _more(self):
        while self.fi < len(self.files):
            chunk = self.files[self.fi].read(1 << 22)
            if not chunk:
                self.fi += 1
                continue
            out = self.dec.decompress(chunk)
            if out:
                self.sha.update(out)
                self.nbytes += len(out)
                if self.pos > (1 << 23):
                    self.buf, self.pos = self.buf[self.pos:], 0
                self.buf += out.decode("ascii")
                return True
        if not self.dec.eof:
            raise ValueError("truncated xz stream")
        self.eof = True
        return False

    def _ensure(self, k):
        while len(self.buf) - self.pos < k and not self.eof:
            self._more()

    def header(self):
        self._ensure(1 << 16)
        idx = self.buf.find('"nodes":[')
        head = self.buf[:idx].rstrip()
        assert idx > 0 and head.endswith(","), "unexpected header"
        self.pos = idx + len('"nodes":[')
        return json.loads(head[:-1] + "}")

    def nodes(self):
        while True:
            self._ensure(1 << 20)
            while self.buf[self.pos] in " \n\r\t,":
                self.pos += 1
                if self.pos >= len(self.buf):
                    self._ensure(1 << 20)
            if self.buf[self.pos] == "]":
                self.pos += 1
                return
            obj, self.pos = self.decoder.raw_decode(self.buf, self.pos)
            yield obj

    def finish(self):
        while not self.eof:
            self._more()
        tail = self.buf[self.pos:].strip()
        assert tail == "}", f"unexpected trailer {tail[:40]!r}"
        return self.sha.hexdigest(), self.nbytes


def pass1(parts, cache_dir):
    """Tree shape: type, vertex, zero, one per node, plus header and decompressed sha256."""
    key = hashlib.sha256("\n".join(sha256_file(p) for p in parts).encode()).hexdigest()[:16]
    cache = cache_dir / f"shape-{key}.json.gz"
    if cache.exists():
        d = json.loads(gzip.decompress(cache.read_bytes()))
        return d["header"], d["tree_sha256"], d["tree_bytes"], [array("i", d[k]) for k in
                                                                 ("type", "vertex", "zero", "one")]
    st = Stream(parts)
    header = st.header()
    ty, vx, z, o = array("b"), array("i"), array("i"), array("i")
    for k, nd in enumerate(st.nodes()):
        t = TYPES.get(nd["type"], T_OTHER)
        ty.append(t)
        if t == T_BRANCH:
            vx.append(nd["vertex"]); z.append(nd["zero"]); o.append(nd["one"])
        else:
            vx.append(-1); z.append(-1); o.append(-1)
    tree_sha, nbytes = st.finish()
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(gzip.compress(json.dumps(
        {"header": header, "tree_sha256": tree_sha, "tree_bytes": nbytes, "type": list(ty),
         "vertex": list(vx), "zero": list(z), "one": list(o)}).encode()))
    return header, tree_sha, nbytes, [array("i", ty), vx, z, o]


def shape_info(ty, z, o, root):
    """Parent pointers, edge decisions and leaf counts below root (preorder is checked)."""
    N = len(ty)
    parent, dec = array("i", [-1]) * N, array("b", [0]) * N
    count = array("i", [0]) * N
    order = []
    stack = [root]
    seen = 0
    while stack:
        j = stack.pop()
        order.append(j)
        seen += 1
        if ty[j] == T_BRANCH:
            for c, x in ((o[j], 1), (z[j], 2)):
                assert parent[c] == -1 and c > j, "not a tree in preorder"
                parent[c], dec[c] = j, x
            stack.append(o[j])
            stack.append(z[j])
    for j in reversed(order):
        count[j] = count[z[j]] + count[o[j]] if ty[j] == T_BRANCH else 1
    # preorder: the subtree of j is the index range [j, j + size_j)
    size = {}
    for j in reversed(order):
        size[j] = 1 + (size[z[j]] + size[o[j]] if ty[j] == T_BRANCH else 0)
        if ty[j] == T_BRANCH:
            assert z[j] == j + 1 and o[j] == j + 1 + size[z[j]], "nodes are not in preorder"
    return parent, dec, count, size


def path_of(j, parent, dec, vx, stop_path_root):
    """Decisions from j up to the tree root, innermost first."""
    p = []
    while parent[j] != -1:
        q = parent[j]
        p.append((vx[q], dec[j]))
        j = q
    return p


def cut(root, limit, ty, z, o, count):
    """Top-down cut: (roots of subtrees with <= limit leaves, nodes above them), both preorder."""
    tops, uppers, stack = [], [], [root]
    while stack:
        j = stack.pop()
        if count[j] <= limit or ty[j] != T_BRANCH:
            tops.append(j)
        else:
            uppers.append(j)
            stack.append(o[j])
            stack.append(z[j])
    return tops, uppers


def normalize(rows, weights, missing):
    return [(r, w) for r, w in weights if w and rows[r][1] > len(missing.intersection(rows[r][0]))]


def full_load_margin(n, rows, budget, missing, occupied, capacity, entries):
    loads = {}
    for r, w in entries:
        for i in rows[r][0]:
            loads[i] = loads.get(i, 0) + w
    lhs = capacity * max(0, budget - len(missing))
    for i, l in loads.items():
        if i in missing:
            lhs += l
        elif i not in occupied and l > capacity:
            lhs += l - capacity
    return sum(w * rows[r][1] for r, w in entries) - lhs


def pack_words(codes, k, J):
    codes = codes + [0] * (-len(codes) % k)
    return [sum(codes[i + t] * J ** t for t in range(k)) for i in range(0, len(codes), k)]


def lean_leaf_test(n, rows, m, budget, base, K, J, k, cap, mask, words, code_cache):
    """Python transcription of Fast2.leafF2 (exact integers)."""
    BN = base ** n
    Q = 0
    for y in words:
        for _ in range(k):
            e, y = y % J, y // J
            r, w = e // K, e % K
            if w and r < m and rows[r][1] > 0:
                c = code_cache.get(r)
                if c is None:
                    c = code_cache[r] = sum(base ** i for i in rows[r][0]) + BN * rows[r][1]
                Q += w * c
    big = (n + 1) * base
    X, p = 0, Q
    for i in range(n):
        v = mask[i]
        c, p = p % base, p // base
        X += c + big if v == 1 else 0 if v == 2 else max(0, c - cap)
    T = Q // BN
    return 1 < base and T < base and cap * max(0, budget - X // big) + X % big < T


def lean_path(p):
    return "[" + ", ".join(f"({v}, {x})" for v, x in p) + "]"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--side", choices=sorted(SIDES), required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--tree", type=Path, nargs="+", required=True, help="the xz parts, in order")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--chunk-leaves", type=int, required=True)
    ap.add_argument("--block-leaves", type=int, required=True)
    ap.add_argument("--per-word", type=int, default=4)
    ap.add_argument("--K", type=int, default=1 << 17)
    ap.add_argument("--prefix", help="module prefix (default E311B / E311R)")
    ap.add_argument("--export-root", type=int, help="export only this subtree (tests); default: the side's root")
    ap.add_argument("--only", help="comma-separated module indices to write (trial); no Root then")
    ap.add_argument("--corrupt", type=int, help="module index: break the min-margin leaf (rejection test)")
    ap.add_argument("--no-profile", action="store_true")
    ap.add_argument("--cache", type=Path, help="directory of the shape cache (default: the parent of --out)")
    args = ap.parse_args()
    t0 = time.time()
    side = SIDES[args.side]
    prefix = args.prefix or side["prefix"]
    cat, catmod = side["catalog"], side["module"]
    source_sha, n, rows = read_source(args.source)
    m = len(rows)
    header, tree_sha, tree_bytes, (ty, vx, z, o) = pass1(args.tree, args.cache or args.out.parent)
    assert header["source_sha256"] == source_sha, "tree/source mismatch"
    budget = header["hole_budget"]
    if args.side == "residual":
        r0 = header["root"]
        assert ty[r0] == T_BRANCH and vx[r0] == 0 and z[r0] == r0 + 1
        default_root = z[r0]
    else:
        default_root = header["root"]
    root = default_root if args.export_root is None else args.export_root
    parent, dec, count, size = shape_info(ty, z, o, header["root"])
    base_path = path_of(root, parent, dec, vx, None)
    if args.export_root is None:
        assert base_path == side["base_path"], base_path
    K, k = args.K, args.per_word
    J = K << m.bit_length()
    L, B = args.chunk_leaves, args.block_leaves
    srs, skeleton = cut(root, L, ty, z, o, count)
    modules, cur, cur_leaves = [], [], 0
    for s in srs:
        if cur and cur_leaves + count[s] > L:
            modules.append(cur)
            cur, cur_leaves = [], 0
        cur.append(s)
        cur_leaves += count[s]
    modules.append(cur)
    width = max(5, len(str(len(modules))))
    names = [f"C{i:0{width}d}" for i in range(1, len(modules) + 1)]
    only = None if args.only is None else {int(x) for x in args.only.split(",")}
    write = [only is None or (i + 1) in only for i in range(len(modules))]
    total_leaves = count[root]
    assert sum(count[s] for s in srs) == total_leaves
    src_dir = args.out / "src" / prefix
    src_dir.mkdir(parents=True, exist_ok=True)
    exporter_sha = sha256_file(__file__)
    M0 = f"(zerosF {n})"
    params = f"{cat} {m} {n} {budget}"

    def feas(p):
        return f"¬ ∃ holes : Fin {n} → ℕ, FFeas {params} (pmask {M0} {lean_path(p)}) holes"

    # Pass 2: stream again; buffer the raw leaves of one module at a time.
    mod_of_index = []  # (first index, last index + 1, module number)
    for i, mod in enumerate(modules):
        mod_of_index.append((mod[0], mod[-1] + size[mod[-1]], i))
    last_needed = max((e for (b0, e, i) in mod_of_index if write[i]), default=0)
    report_modules = []
    stats = {"leaves": 0, "weighted": 0, "over_budget": 0, "entries": 0, "words": 0,
             "lean_test_failures": 0}
    corrupt_info = None
    st = Stream(args.tree)
    st.header()
    mi = 0
    buf = {}
    code_caches = {}

    def emit(i):
        nonlocal corrupt_info
        mod = modules[i]
        name = f"{prefix}.{names[i]}"
        lines = [f"import {catmod}", "import CompactChecker.Path", "open CompactChecker",
                 "set_option maxRecDepth 100000", *OPTS,
                 *([] if args.no_profile else ["set_option profiler true"]),
                 f"namespace {name}",
                 f"-- ES(8) <= 311 compact recheck, {args.side} side, module {i + 1} of {len(modules)}",
                 f"-- tree sha256 {tree_sha}; source sha256 {source_sha}; exporter sha256 {exporter_sha}",
                 f"-- {sum(count[s] for s in mod)} leaves under subtree roots {mod}; budget {budget}",
                 f"-- chunk limit {L}, block limit {B}, K {K}, J {J}, {k} entries per word"]
        exported, nblocks, entries, words_n, margins, bases = [], 0, 0, 0, [], []
        corrupt_leaf = None
        if args.corrupt == i + 1:
            # the weighted leaf of least margin in this module
            corrupt_leaf = min((x for x in buf if buf[x][0] == T_WEIGHTED), key=lambda x: buf[x][3])
        for s in mod:
            blocks, uppers = cut(s, B, ty, z, o, count)
            for b in blocks:
                leaves = [x for x in range(b, b + size[b]) if ty[x] != T_BRANCH]
                maxd = max([buf[x][2] for x in leaves if buf[x][0] == T_WEIGHTED] + [1])
                base = 1 << maxd.bit_length()
                bases.append(base)
                cc = code_caches.setdefault(base, {})

                def term(x):
                    nonlocal entries, words_n, corrupt_info
                    if ty[x] == T_BRANCH:
                        return f"(.split {vx[x]} {term(z[x])} {term(o[x])})"
                    rec = buf[x]
                    if rec[0] == T_OVER:
                        return ".overBudget"
                    _, cap, D, margin, ent, mask = rec
                    if x == corrupt_leaf:
                        found = None
                        missing = {v for v in range(n) if mask[v] == 1}
                        occupied = {v for v in range(n) if mask[v] == 2}
                        for e in range(len(ent)):
                            for w in (ent[e][1] - 1, ent[e][1] + 1, 0):
                                if w < 0:
                                    continue
                                trial = list(ent)
                                trial[e] = (trial[e][0], w)
                                mg = full_load_margin(n, rows, budget, missing, occupied, cap, trial)
                                if mg <= 0:
                                    found = (e, w, mg)
                                    break
                            if found:
                                break
                        assert found, "no single-weight corruption found"
                        corrupt_info = {"module": name, "leaf_node": x, "entry_index": found[0],
                                        "row": ent[found[0]][0], "old_weight": ent[found[0]][1],
                                        "new_weight": found[1], "old_margin": margin,
                                        "new_margin": found[2]}
                        ent = list(ent)
                        ent[found[0]] = (ent[found[0]][0], found[1])
                    codes = [r * K + w for r, w in ent]
                    words = pack_words(codes, k, J)
                    entries += len(codes)
                    words_n += len(words)
                    ok = lean_leaf_test(n, rows, m, budget, base, K, J, k, cap, mask, words, cc)
                    if not ok:
                        stats["lean_test_failures"] += 1
                        assert x == corrupt_leaf, f"Lean leaf test fails on node {x}"
                    return f"(.leaf {cap} (natlits% [{', '.join(map(str, words))}]))"

                p = path_of(b, parent, dec, vx, None)
                lines.append(f"noncomputable def b{b} : PTree := {term(b)}")
                lines.append(f"theorem chk{b} : checkF2 {params} {base} {K} {J} {k} b{b} "
                             f"(pmask {M0} {lean_path(p)}) = true := by decide +kernel")
                lines.append(f"theorem ex{b} : {feas(p)} :=")
                lines.append(f"  checkF2_feas {params} {side['catalog_base']} {base} {K} {J} {k} "
                             f"{cat}_wf b{b} _ chk{b}")
                nblocks += 1
            for u in reversed(uppers):
                p = path_of(u, parent, dec, vx, None)
                lines.append(f"theorem ex{u} : {feas(p)} :=")
                lines.append(f"  split_pm {params} {M0} {lean_path(p)} {vx[u]} ex{z[u]} ex{o[u]}")
            exported.append(s)
        for s in exported:
            lines.append(f"#print axioms ex{s}")
        lines.append(f"end {name}")
        for x in buf:
            if buf[x][0] == T_WEIGHTED:
                margins.append(buf[x][3])
        path = src_dir / f"{names[i]}.lean"
        path.write_text("\n".join(lines) + "\n")
        report_modules[i].update({
            "file": str(path.relative_to(args.out)), "sha256": sha256_file(path),
            "source_bytes": path.stat().st_size, "blocks": nblocks, "entries": entries,
            "words": words_n, "min_margin": min(margins) if margins else None,
            "max_block_base": max(bases), "corrupted": corrupt_leaf is not None})
        stats["entries"] += entries
        stats["words"] += words_n

    for i, mod in enumerate(modules):
        report_modules.append({"index": i + 1, "module": f"{prefix}.{names[i]}",
                               "leaves": sum(count[s] for s in mod),
                               "subtree_roots": [[s, count[s]] for s in mod],
                               "node_range": [mod[0], mod[-1] + size[mod[-1]]],
                               "file": None, "sha256": None})
    complete = all(write)
    for x, nd in enumerate(st.nodes()):
        if x >= last_needed:
            if complete:
                continue  # read to the end, so that the sha256 of the whole stream is checked
            break
        while mi < len(mod_of_index) and x >= mod_of_index[mi][1]:
            if write[mi]:
                emit(mi)
            buf = {}
            mi += 1
        if mi >= len(mod_of_index) or x < mod_of_index[mi][0] or not write[mi]:
            continue
        t = TYPES.get(nd["type"], T_OTHER)
        if t == T_BRANCH:
            continue
        assert t in (T_WEIGHTED, T_OVER), (x, nd["type"])
        mask = [0] * n
        for v, d in path_of(x, parent, dec, vx, None):
            assert mask[v] == 0, "a state is fixed twice on a path"
            mask[v] = d
        missing = {v for v in range(n) if mask[v] == 1}
        stats["leaves"] += 1
        if t == T_OVER:
            assert len(missing) > budget
            stats["over_budget"] += 1
            buf[x] = (T_OVER,)
            continue
        occupied = {v for v in range(n) if mask[v] == 2}
        ent = normalize(rows, nd["weights"], missing)
        assert all(0 < w < K for _, w in ent)
        cap = nd["capacity"]
        margin = full_load_margin(n, rows, budget, missing, occupied, cap, ent)
        assert margin >= 1, (x, margin)
        D = sum(w * rows[r][1] for r, w in ent)
        stats["weighted"] += 1
        buf[x] = (T_WEIGHTED, cap, D, margin, ent, mask)
    while mi < len(mod_of_index) and mod_of_index[mi][1] <= last_needed:
        if write[mi]:
            emit(mi)
        buf = {}
        mi += 1
    if complete:
        _, n_bytes = st.finish()
        assert st.sha.hexdigest() == tree_sha, "tree changed between passes"
        assert stats["leaves"] == total_leaves
        # Root: the skeleton above the subtree roots, children before parents.
        home = {s: names[i] for i, mod in enumerate(modules) for s in mod}
        rl = [f"import {prefix}.{nm}" for nm in names]
        rl += ["open CompactChecker", "set_option maxRecDepth 100000", *OPTS,
               *([] if args.no_profile else ["set_option profiler true"]),
               f"namespace {prefix}",
               f"-- ES(8) <= 311 compact recheck, {args.side} side: {total_leaves} leaves, "
               f"{len(modules)} modules, {len(srs)} subtree roots, {len(skeleton)} skeleton nodes",
               f"-- tree sha256 {tree_sha}; exporter sha256 {exporter_sha}"]

        def ref(c):
            return f"{prefix}.{home[c]}.ex{c}" if c in home else f"ex{c}"

        for u in reversed(skeleton):
            p = path_of(u, parent, dec, vx, None)
            rl.append(f"theorem ex{u} : {feas(p)} :=")
            rl.append(f"  split_pm {params} {M0} {lean_path(p)} {vx[u]} {ref(z[u])} {ref(o[u])}")
        rl.append(f"theorem root : {feas(base_path)} := {ref(root)}")
        rl += ["#print axioms root", f"end {prefix}"]
        rpath = src_dir / "Root.lean"
        rpath.write_text("\n".join(rl) + "\n")
        root_report = {"module": f"{prefix}.Root", "file": str(rpath.relative_to(args.out)),
                       "sha256": sha256_file(rpath), "skeleton_nodes": len(skeleton)}
    else:
        root_report = None
    manifest = {
        "side": args.side, "prefix": prefix, "complete": complete,
        "tree_parts": [{"file": str(p), "sha256": sha256_file(p)} for p in args.tree],
        "tree_sha256": tree_sha, "tree_bytes": tree_bytes, "source": str(args.source),
        "source_sha256": source_sha, "exporter_sha256": exporter_sha,
        "catalog": catmod, "catalog_base": side["catalog_base"], "states": n, "rows": m,
        "budget": budget, "export_root": root, "base_path": base_path,
        "chunk_leaves": L, "block_leaves": B, "per_word": k, "K": K, "J": J,
        "total_leaves": total_leaves, "subtree_roots": len(srs), "skeleton_nodes": len(skeleton),
        "modules": report_modules, "root": root_report,
        "skeleton": [[u, vx[u], z[u], o[u]] for u in skeleton],
        "written_stats": stats, "corruption": corrupt_info,
        "seconds": round(time.time() - t0, 1)}
    mpath = args.out / f"manifest-{prefix}.json"
    mpath.write_text(json.dumps(manifest, indent=1))
    print(json.dumps({k2: manifest[k2] for k2 in ("side", "prefix", "complete", "total_leaves",
                                                    "subtree_roots", "skeleton_nodes", "written_stats",
                                                    "corruption", "seconds")}
                     | {"modules": len(modules), "manifest": str(mpath)}))


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()
