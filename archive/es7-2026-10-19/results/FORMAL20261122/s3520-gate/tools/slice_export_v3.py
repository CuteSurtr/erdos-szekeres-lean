#!/usr/bin/env python3
"""s3520-gate v3 (22 Nov 2026): slice_export_w13fix.py (= res-slices-fv slice_export_w13.py + the context-id fix) made
lean for s35_20, whose contexts reach 320,422 leaves (ctx-4274). The chunk texts and manifests are meant to be byte
for byte those of slice_export_w13fix.py (controls in the s3520-gate README); only memory and I/O differ:
  - pre-pass streamed: each context gz is inflated in pieces; its header (context, root, missing, occupied) is parsed
    from the text before "nodes"; leaves are counted as occurrences of "type":"weighted" / "over_budget" and branches
    of "type":"branch"; every "type": must be one of the three, leaves = branches + 1, and the text must end "]}";
  - contexts are read node by node (JSON scanner on a sliding window of the inflated text) into flat arrays; the unit
    is grafted into an export_es310_w13l.CUnit (flat arrays, zero-first preorder); no context is ever a Python node
    list, and no leaf keeps a tuple;
  - export_es310_w13l.export_compact writes each module (to a hidden .tmp name) as soon as it has passed its checks;
    after the unit's last check the modules are renamed into place and the manifest is written LAST, as before;
  - --stop-after S: no new unit is started after S seconds (clean stop before a RuntimeMaxSec; resumable as before).
The unit cut, the leaf replays and all refusals are unchanged. NOTHING HERE PROVES ANYTHING: Lean decides every module.

res-slices-fv w13 (22 Nov 2026 evening): slice_export.py with export_es310_w13 (13-bit row digits, J = K << 13, for
catalogs of up to 8,191 rows such as s35_20's 4,642). Otherwise unchanged.
res-slices-fv (22 Nov 2026): export one residual slice tree (master + contexts) as Fast2 chunk modules.

  slice_export_v3.py TAG --budget B --master M --ctxdir DIR --extra EXTRA --out OUT
                  [--unit-leaves U] [--chunk-leaves L] [--block-leaves 64] [--per-word 16] [--units A:B]
                  [--corrupt K:MM] [--no-profile] [--stop-after S] [--prepass-only]

1. Rows: source-2650 (raw sha256 pinned) followed by EXTRA in file order (the slice's rows.txt order).
2. Master: budget B, root 0. A traversal from the root (state 0 occupied there) gives every context placeholder its
   path; the context ids are the sorted placeholder ids (distinct, non-negative; their number = master "contexts").
   A pre-pass reads each context file once (header context = k, root 0, missing / occupied = the placeholder's path
   literals with state 0 occupied), counts its leaves and hashes it.
3. Units: top-down cut of the master, placeholders weighted by their leaf counts, into subtrees of at most U leaves
   (a placeholder is never split). Unit u is the master subtree at a cut node with its contexts grafted in, renumbered
   zero-first preorder; units are numbered in preorder.
4. Each unit goes through export_es310_w13l.export_compact (export_context's zero-first preorder, both exact leaf
   replays, module and block cut, line-shape check) with base path = the unit's master path followed by (0, 2) (state
   0 occupied), catalog RS.Cat<TAG> (fcatS<TAG>, catalog base 131072), 154 states, len(rows) rows, budget B, prefix
   RS<TAG>. The header comment that names ES(8) <= 310 is replaced and the shape check run again. Writes
   OUT/src/RS<TAG>/C<uuuu><mm>.lean, then OUT/ctx/ctx-<uuuu>.json LAST (it means "unit u is exported"); an existing
   manifest with the same unit fingerprint is skipped.
5. OUT/skeleton.json: the master nodes above the cut (vertex, children, Lean path) and the unit of each cut node.
"""
import argparse
import hashlib
import json
import re
import resource
import sys
import time
import zlib
from array import array
from pathlib import Path

X = Path("/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05")
sys.path.insert(0, str(X))
import shapes_es311  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))   # the lean copy lives next to this file
import export_es310_w13l as E  # noqa: E402
from export_es311 import read_source  # noqa: E402

SOURCE = Path("/home/jay/research/data/es308-20261114/inputs/source-2650.json.gz")
SOURCE_RAW_SHA = "e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6"
OLD = "-- ES(8) <= 310 compact check (budget-64 campaign), balanced side, context"
PIECE = 1 << 20                     # compressed bytes inflated per step
AHEAD = 1 << 21                     # inflated characters kept ahead of the JSON scanner (a node is a few KB)
DEC = json.JSONDecoder()
WS = re.compile(r"[ \t\n\r]*")
T_CODE = {"branch": E.T_BRANCH, "weighted": E.T_WEIGHTED, "over_budget": E.T_OVER}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write_atomic(path, data):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def inflate(gz, k):
    """The inflated pieces (bytes) of one gzip member; refuses trailing data or a truncated stream."""
    d, mv = zlib.decompressobj(16 + zlib.MAX_WBITS), memoryview(gz)
    try:
        for i in range(0, len(gz), PIECE):
            yield d.decompress(mv[i:i + PIECE])
        yield d.flush()
    except zlib.error as e:
        raise E.Refuse(f"context {k}: gzip error {e}")
    if not d.eof or d.unused_data:
        raise E.Refuse(f"context {k}: the gzip stream is not exactly one complete member")


def check_header(k, head, path):
    """The context header (all keys before "nodes", which must be the last key) against the master path."""
    j = head.find(b'"nodes":[')
    if j < 0:
        raise E.Refuse(f"context {k}: no \"nodes\" array in the first {len(head)} bytes")
    try:
        d = json.loads(head[:j] + b'"nodes":[]}')
    except ValueError:
        raise E.Refuse(f"context {k}: the header does not parse")
    if d.get("context") != k or d.get("root") != 0:
        raise E.Refuse(f"context {k}: header context/root differ")
    if path is not None:
        mis = sorted(v for v, b in path if b == 1)
        occ = sorted([0] + [v for v, b in path if b == 0])
        if sorted(d.get("missing", [None])) != mis or sorted(d.get("occupied", [None])) != occ:
            raise E.Refuse(f"context {k}: missing/occupied differ from its master path")
    return j


class Local:
    """One context as flat arrays indexed by its file node ids (released once the graft has reached every node)."""

    def __init__(self, k):
        self.k = k
        self.ty, self.vx, self.z, self.o = bytearray(), array("i"), array("i"), array("i")
        self.cap, self.wo, self.wn = array("q"), array("q"), array("i")
        self.R, self.W = array("i"), array("q")

    def add(self, nd):
        t = nd.get("type") if isinstance(nd, dict) else None
        i = len(self.ty)
        try:
            if t == "branch":
                v, zz, oo = nd.get("vertex"), nd.get("zero"), nd.get("one")
                if not (E.is_int(v) and E.is_int(zz) and E.is_int(oo)):
                    raise E.Refuse(f"context {self.k}: bad branch node {i}")
                self.vx.append(v); self.z.append(zz); self.o.append(oo); self.cap.append(-1)
                self.wn.append(0)
            elif t == "weighted":
                cap, ws = nd.get("capacity"), nd.get("weights")
                if not (E.is_int(cap) and isinstance(ws, list)):
                    raise E.Refuse(f"context {self.k}: bad weighted leaf {i}")
                for e in ws:
                    if not (isinstance(e, list) and len(e) == 2 and E.is_int(e[0]) and E.is_int(e[1])):
                        raise E.Refuse(f"context {self.k}: bad weight entry {e!r} in leaf {i}")
                self.wo.append(len(self.R))
                self.R.extend(e[0] for e in ws)
                self.W.extend(e[1] for e in ws)
                self.vx.append(-1); self.z.append(-1); self.o.append(-1); self.cap.append(cap); self.wn.append(len(ws))
                self.ty.append(E.T_WEIGHTED)
                return
            elif t == "over_budget":
                self.vx.append(-1); self.z.append(-1); self.o.append(-1); self.cap.append(-1); self.wn.append(0)
            else:
                raise E.Refuse(f"context {self.k}: node {i} has type {t!r}")
        except OverflowError:
            raise E.Refuse(f"context {self.k}: node {i} has a value outside the compact arrays")
        self.wo.append(len(self.R))
        self.ty.append(T_CODE[t])


class Ctx:
    """Context files, read one at a time and checked against the pre-pass hash."""

    def __init__(self, ctxdir):
        self.dir, self.sha = Path(ctxdir), {}

    def raw(self, k):
        gz = (self.dir / f"ctx-{k}.json.gz").read_bytes()
        h = sha(gz)
        if k in self.sha and self.sha[k] != h:
            raise E.Refuse(f"context {k} changed since the pre-pass")
        self.sha[k] = h
        return gz

    def count(self, k, path):
        """Pre-pass (streamed): (leaves, branches) of context k; checks the header, the node types and the end."""
        pats = (b'"type":', b'"type":"branch"', b'"type":"weighted"', b'"type":"over_budget"')
        cnt, tails, head, end = [0] * 4, [b""] * 4, b"", b""     # end: the last 16 inflated bytes
        for piece in inflate(self.raw(k), k):
            if len(head) < 65536:
                head += piece[:65536 - len(head)]
            for j, p in enumerate(pats):          # whole occurrences in the piece, then those across its start
                L = len(p) - 1
                cnt[j] += piece.count(p) + (tails[j] + piece[:L]).count(p)
                tails[j] = piece[-L:] if len(piece) >= L else (tails[j] + piece)[-L:]
            end = (end + piece[-16:])[-16:]
        check_header(k, head, path)
        if cnt[0] != cnt[1] + cnt[2] + cnt[3]:
            raise E.Refuse(f"context {k}: {cnt[0] - cnt[1] - cnt[2] - cnt[3]} nodes of another type or spelling")
        if cnt[2] + cnt[3] != cnt[1] + 1:
            raise E.Refuse(f"context {k}: {cnt[2] + cnt[3]} leaves but {cnt[1]} branches")
        if not end.rstrip().endswith(b"]}"):
            raise E.Refuse(f"context {k}: the text does not end with the nodes array")
        return cnt[2] + cnt[3], cnt[1]

    def load_compact(self, k, path):
        """Context k as a Local (streamed: the inflated text is never held whole)."""
        pieces = inflate(self.raw(k), k)
        buf, pos, eof = "", 0, False

        def need(nc):                             # at least nc characters ahead of pos, unless at the end
            nonlocal buf, pos, eof
            while len(buf) - pos < nc and not eof:
                try:
                    data = next(pieces)
                except StopIteration:
                    eof = True
                    break
                try:
                    buf = buf[pos:] + data.decode("ascii")
                except UnicodeDecodeError:
                    raise E.Refuse(f"context {k}: the text is not ASCII")
                pos = 0
            return len(buf) - pos >= nc

        need(65536)
        pos = check_header(k, buf[:65536].encode("ascii"), path) + len('"nodes":[')
        loc = Local(k)
        need(1)
        if buf[pos:pos + 1] == "]":
            pos += 1
        else:
            while True:
                need(AHEAD)
                pos = WS.match(buf, pos).end()
                try:
                    nd, end = DEC.raw_decode(buf, pos)
                except ValueError:
                    raise E.Refuse(f"context {k}: node {len(loc.ty)} does not parse")
                loc.add(nd)
                pos = WS.match(buf, end).end()
                if not need(1):
                    raise E.Refuse(f"context {k}: the text ends inside the nodes array")
                c, pos = buf[pos], pos + 1
                if c == "]":
                    break
                if c != ",":
                    raise E.Refuse(f"context {k}: {c!r} after node {len(loc.ty) - 1}")
        while need(len(buf) - pos + 1):           # the rest of the text must be the closing brace
            pass
        if buf[pos:].strip() != "}":
            raise E.Refuse(f"context {k}: the text does not end with the nodes array")
        loc.N = len(loc.ty)
        loc.seen, loc.nseen = bytearray(loc.N), 0
        return loc


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


def build_unit_compact(t, nodes, ctx, kpath):
    """The unit as a CUnit: zero-first preorder, contexts grafted in (as slice_export_w13.build_unit, then renumber's
    checks: every node reached once, branch fields in range, every node of a context reachable)."""
    U, n = E.CUnit(), E.N_STATES
    mloc = None                                   # master leaves of the unit, as a Local
    stack, visited, loaded = [(None, t, -1, 0)], set(), []
    while stack:
        src, i, par, side = stack.pop()           # src: None (master) or the Local of a context
        if src is None and nodes[i]["type"] == "context":
            k = nodes[i]["context"]
            src = ctx.load_compact(k, kpath[k])
            src.sid = len(U.sources)
            U.sources.append((src.R, src.W))
            loaded.append(src)
            i = 0
        me = len(U.ty)
        if par >= 0:
            (U.z if side == 0 else U.o)[par] = me
        if src is None:
            if i in visited:
                raise E.Refuse("a node is reached twice while grafting")
            visited.add(i)
            nd = nodes[i]
            if nd["type"] == "branch":
                v = nd["vertex"]
                if not (E.is_int(v) and 0 <= v < n):
                    raise E.Refuse(f"master node {i}: bad vertex")
                U.ty.append(E.T_BRANCH); U.vx.append(v); U.z.append(-1); U.o.append(-1)
                U.cap.append(-1); U.src.append(-1); U.wo.append(0); U.wn.append(0)
                stack.append((None, nd["one"], me, 1))
                stack.append((None, nd["zero"], me, 0))
                continue
            if mloc is None:
                mloc = Local("master")
                mloc.sid = len(U.sources)
                U.sources.append((mloc.R, mloc.W))
            mloc.add(nd)
            j = len(mloc.ty) - 1
            U.ty.append(mloc.ty[j]); U.vx.append(-1); U.z.append(-1); U.o.append(-1)
            U.cap.append(mloc.cap[j]); U.src.append(mloc.sid); U.wo.append(mloc.wo[j]); U.wn.append(mloc.wn[j])
            continue
        if src.seen is None or not 0 <= i < src.N or src.seen[i]:
            raise E.Refuse(f"ctx {src.k}: node {i} is reached twice or does not exist (not a tree)")
        src.seen[i] = 1
        src.nseen += 1
        if src.ty[i] == E.T_BRANCH:
            v, zz, oo = src.vx[i], src.z[i], src.o[i]
            if not (0 <= v < n and 0 <= zz < src.N and 0 <= oo < src.N and zz != oo):
                raise E.Refuse(f"ctx {src.k}: bad branch node {i}")
            U.ty.append(E.T_BRANCH); U.vx.append(v); U.z.append(-1); U.o.append(-1)
            U.cap.append(-1); U.src.append(-1); U.wo.append(0); U.wn.append(0)
            stack.append((src, oo, me, 1))
            stack.append((src, zz, me, 0))
        else:
            U.ty.append(src.ty[i]); U.vx.append(-1); U.z.append(-1); U.o.append(-1)
            U.cap.append(src.cap[i]); U.src.append(src.sid); U.wo.append(src.wo[i]); U.wn.append(src.wn[i])
        if src.nseen == src.N:                    # the whole context is grafted: drop its node arrays
            src.ty = src.vx = src.z = src.o = src.cap = src.wo = src.wn = src.seen = None
    for src in loaded:
        if src.nseen != src.N:
            raise E.Refuse(f"ctx {src.k}: {src.N - src.nseen} nodes are not reachable from the root")
    return U


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
    ap.add_argument("--stop-after", type=float)
    ap.add_argument("--prepass-only", action="store_true")
    args = ap.parse_args()
    t_start = time.time()
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
        if sorted(kleaves) != ids or sorted(ctx.sha) != ids:
            raise E.Refuse("prepass.json does not cover exactly the master's contexts")
    else:
        kleaves, kbranches = {}, {}
        for j, k in enumerate(ids):
            kleaves[k], kbranches[k] = ctx.count(k, kpath[k])
            if (j + 1) % 500 == 0 or j + 1 == K:
                print(json.dumps({"prepass": j + 1, "of": K, "leaves_so_far": sum(kleaves.values()),
                                  "seconds": round(time.time() - t_start, 1)}), flush=True)
        pp = {"master": str(args.master), "master_sha256": sha(mraw), "contexts": K,
              "leaves": kleaves, "gz_sha256": ctx.sha,
              "contexts_digest": sha("".join(f"{k} {ctx.sha[k]}\n" for k in ids).encode()),
              "branches": kbranches, "prepass": "slice_export_v3 streamed count"}
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
    if args.prepass_only:
        print(json.dumps({"total_leaves": total, "units": len(tops), "contexts": K,
                          "seconds": round(time.time() - t_start, 1)}), flush=True)
        return
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
    me_sha = sha(Path(__file__).read_bytes())
    core_sha = sha((Path(__file__).resolve().parent / "export_es310_w13l.py").read_bytes())
    new = f"-- res-slices-fv residual slice check (Res118 slice B={B}), unit"
    for u in sel:
        if args.stop_after is not None and time.time() - t_start > args.stop_after:
            print(json.dumps({"stopped_before_unit": u, "seconds": round(time.time() - t_start, 1)}), flush=True)
            break
        t0 = time.time()
        t = tops[u]
        fp = sha(json.dumps([skel["master_sha256"], skel["contexts_digest"], skel["extra_sha256"], ssha, B,
                             t, mpath[t], args.chunk_leaves, args.block_leaves, args.per_word, cmod]).encode())
        man = out / "ctx" / f"ctx-{u:04d}.json"
        if man.exists() and json.loads(man.read_text()).get("fingerprint") == fp:
            continue
        written = []

        def emit(stem, text):                    # header replaced, shape check again, written under a hidden name
            if text.count(OLD) != 1:
                raise E.Refuse(f"unit {u}: header comment not found once in {stem}")
            text = text.replace(OLD, new)
            errs = shapes_es311.check_text(text, "chunk", f"{prefix}.{stem}", sp)
            if errs:
                raise E.Refuse(f"unit {u}: {stem} fails the shape check: {errs}")
            b = text.encode("utf-8")
            tmp = out / "src" / prefix / f".{stem}.lean.tmp"
            tmp.write_bytes(b)
            written.append((tmp, out / "src" / prefix / f"{stem}.lean"))
            return sha(b), len(b)

        try:
            U = build_unit_compact(t, nodes, ctx, kpath)
            ctxline = {"path": [[0, 0]] + mpath[t]}
            hashes = {"gz": skel["master_sha256"], "json": skel["contexts_digest"], "result": "-", "source": ssha}
            info = E.export_compact(u, ctxline, U, rows, args, prefix, code_caches, hashes, emit)
            nnodes = len(U.ty)
            del U
            assert info["base_path"] == [list(x) for x in lean_path(mpath[t])], "base path differs"
            if info["stats"]["leaves"] != cnt[t]:
                raise E.Refuse(f"unit {u}: {info['stats']['leaves']} leaves, expected {cnt[t]}")
            for tmp, final in written:
                tmp.replace(final)
            info.update({"unit": u, "top": t, "fingerprint": fp, "leaves_expected": cnt[t],
                         "exporter_sha256": me_sha, "export_es310_sha256": core_sha,
                         "params": {"budget": B, "per_word": args.per_word, "chunk_leaves": args.chunk_leaves,
                                    "block_leaves": args.block_leaves, "catalog": E.CATMOD, "rows": len(rows),
                                    "catalog_base": E.CATALOG_BASE}, "seconds": round(time.time() - t0, 1)})
            write_atomic(man, json.dumps(info, separators=(",", ":")).encode())
            print(json.dumps({"unit": u, "modules": len(info["modules"]), "leaves": info["stats"]["leaves"],
                              "min_margin": info["stats"]["min_margin"], "seconds": info["seconds"],
                              "corrupted": info["corruption"], "nodes": nnodes,
                              "maxrss_mb": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024}), flush=True)
        except E.Refuse as e:
            for tmp, _ in written:
                tmp.unlink(missing_ok=True)
            refused.append(u)
            print(json.dumps({"unit": u, "refused": str(e)}), flush=True)
    sys.exit(1 if refused else 0)


if __name__ == "__main__":
    main()
