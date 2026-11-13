#!/usr/bin/env python3
"""Export closed budget-64 campaign contexts as Fast2 chunk modules, one context at a time
(route to ES(8) <= 310; 6 November 2026). NOTHING HERE PROVES ES(8) <= 310: that needs all 4,096
contexts closed, exported, compiled, joined by the Root and assembled with a clean axiom audit.

  export_es310.py --campaign C --source SRC --out OUT (--all-closed | --ctx k1,k2,...) --per-word k
                  [--chunk-leaves 12000] [--block-leaves 64] [--prefix E310B] [--corrupt N]
                  [--refresh-exporter] [--no-profile]

Inputs (read only; every file is opened "rb"; nothing is ever written under C):
  C/contexts.jsonl                 the 4,096 depth-12 contexts of tree-63 (validated whole, every run)
  C/runs/ctx-<k>-b64.result.json   the campaign's result (status, replay, counts, rules)
  C/runs/ctx-<k>-b64.json.gz       the context's subtree (run_context.py:162-166)
  SRC                              balanced-v2-source.json, sha256 acaf6323... (hashed here, by read_source)

Per context k (design section A of es310-design.md, with the critiques' required fixes):
  1. Not ready (skipped; exit 3 if k was named by --ctx): no result.json, a result.json that does not
     parse, a live "run_context.py --budget 64 --ctx k" process in ANY working directory (/proc scan,
     read only), a result or tree younger than 120 s, a missing tree, or a tree gz that fails to
     decompress (EOFError, CRC) or to parse.
     Refused (exit 1): any ctx-*-b64.WITNESS.json or campaign/WITNESS-ALERT.txt; status witness; status
     capped/error when k was named by --ctx (with --all-closed such a context is "not closed" and
     skipped); a missing or broken tree gz (as above) when result.json is more than 600 s old (the gz is
     written before result.json, run_context.py:165-168, so that is damage, not a write in progress;
     fixer 6 Nov, ops review 3b); budget != 64, replay not ok, replay.pending != 12, replay.leaves_checked != leaves,
     pending != 0, rules.catalog_sha256 != acaf6323...; a tree whose context, budget, status, root,
     path, missing or occupied differ from the result / contexts.jsonl; a node graph that is not a tree;
     node counts that differ from the result's.
  2. The tree is renumbered into zero-first preorder (explicit stack, pushes one then zero); every node
     must be reached exactly once. shape_info (export_es311.py:167-193) then re-asserts the preorder.
  3. Base path = the 12 context decisions, innermost first, zero (b = 0, occupied) -> (v, 2), one
     (b = 1, missing) -> (v, 1) (run_context.py:106-107, export_es311.py:180). The full path of a local
     node is path_of (local, innermost first) ++ base path; no state may be fixed twice.
  4. Every leaf is replayed twice with the full mask, by the 311 code imported unchanged:
     full_load_margin >= 1 (export_es311.py:224-235, :483-484) and lean_leaf_test must accept
     (export_es311.py:243-263, :410-413); over-budget leaves need more than 64 missing states.
     K = 2^17 or the least power of 2 above the context's largest normalized weight; J = K << 12.
     The row-code cache (one dict per leaf base) is kept across leaves, modules and contexts
     (export_es311.py:347, :373).
  5. Cut as export_es311.py:310-318 (cut(), greedy modules of at most --chunk-leaves leaves) and
     :367 (blocks of at most --block-leaves leaves). Module k, index mm (from 01):
     <Prefix>.C<kkkk><mm> in OUT/src/<Prefix>/C<kkkk><mm>.lean. Lines exactly as export_es311.py:353-431
     with params "fcat62 3131 252 64", catalog base 4194304; theorems ex<j> with j the local preorder id
     (context root = 0). Each module text must pass shapes_es311.check_text before it is written.
  6. Writes (only under OUT, never inside C or the 311 build dirs): module files to tmp names; then the
     result.json, the tree gz and the global inputs are re-read and re-hashed (refuse if any changed) and
     the /proc scan is repeated; then the modules are renamed into place and OUT/ctx/ctx-<kkkk>.json is
     written LAST (tmp then rename). Its existence means "context k is exported".
  7. Incremental: every already-exported context in OUT is re-hashed (result.json and tree gz: size and
     sha256; plus contexts.jsonl and the source). Same: skipped. Different: OUT/ALERT-changed-inputs.txt
     is written, nothing is exported, the old export is left untouched, exit 2. While that file exists
     every run exits 2. A changed run_context.py or pbb_strong.py (campaign code, not data: every leaf is
     replayed here and checked by Lean, so they cannot affect soundness) is only recorded as a warning
     ("code_changed"; fixer 6 Nov, soundness review item 7 / ops review 1). A context exported by another
     exporter sha256 is reported ("stale_exporter", exit 5) and only re-exported with --refresh-exporter. Parameters (prefix, budget, per word, chunk and block limits,
     campaign) must equal those of the contexts already in OUT.
  flock OUT/.export.lock (shared with merge_es310.py); a second exporter or merge exits 4.
  8. A refusal that concerns one context (its result, tree, leaves, cut, or inputs changing during its
     export) is recorded in "refused_ctx" and the run goes on with the other contexts; the run then exits
     1. A refusal that concerns the whole campaign (a WITNESS file or status, contexts.jsonl or the source
     changed, the campaign code missing, bad options) stops the run at once (exit 1, "refused").

Exit codes: 0 ok, 1 refused (some context or the run), 2 changed inputs (ALERT), 3 some --ctx context not
ready, 4 locked (retry later), 5 some context was exported by another exporter sha256 (stale_exporter; use
--refresh-exporter). Precedence: 1, then 3, then 5.
stdout: one JSON line (the run summary; append it to OUT/export-runs.jsonl). Diagnostics on stderr.
"""
import argparse
import fcntl
import gzip
import hashlib
import json
import os
import re
import sys
import time
import zlib
from array import array
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import export_es311 as X311  # noqa: E402
from export_es311 import (OPTS, T_BRANCH, T_OVER, T_WEIGHTED, cut, full_load_margin,  # noqa: E402
                          lean_leaf_test, lean_path, normalize, pack_words, path_of, read_source,
                          sha256_file, shape_info)
import shapes_es311  # noqa: E402

SOURCE_SHA = "acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72"  # run_context.py:33
BUDGET = 64
CATMOD, CAT = "CompactChecker.Fcat62", "fcat62"
CATALOG_BASE = 1 << 22            # export_es311.py:46 (4194304)
N_STATES, N_ROWS = 252, 3131
DEPTH, N_CTX = 12, 4096
DEFAULT_PREFIX = "E310B"
MIN_AGE = 120.0                   # seconds
SKEL_STRIDE = 100000              # context-internal skeleton node u of context k is ex<(k+1)*100000 + u> (Root)
REAL_CAMPAIGN = Path("/home/jay/research/data/es8-b64-pilot-20261105")
PROTECTED = [HERE / "build" / x for x in ("es311", "CompactChecker", "ext", "chain311")]
EXIT_OK, EXIT_REFUSE, EXIT_ALERT, EXIT_NOT_READY, EXIT_LOCKED, EXIT_STALE = 0, 1, 2, 3, 4, 5
GZ_DAMAGE_AGE = 600.0             # seconds: a broken tree gz behind an older result.json is damage
ALERT_NAME = "ALERT-changed-inputs.txt"


class Refuse(Exception):
    pass


class RefuseAll(Refuse):
    """A refusal about the whole run (never caught per context)."""


class NotReady(Exception):
    pass


class NotClosed(Exception):
    pass


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def is_int(x):
    return type(x) is int


def log(msg):
    print(f"export_es310: {msg}", file=sys.stderr, flush=True)


# ----------------------------------------------------------------------------------------------
# global inputs

def load_contexts(path):
    """sha256, {ctx: line}, {(depth, prefix): vertex} of contexts.jsonl, validated whole:
    ctx 0..4095 once each; 12 decisions [v, b] with 0 <= v < 252, b in {0, 1}, no vertex twice;
    the bits read from the root are k in binary; missing / occupied are the 1 / 0 literals;
    every depth-d prefix has exactly one branching vertex."""
    raw = Path(path).read_bytes()
    sha = sha256_bytes(raw)
    ctxs, pv = {}, {}
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        raise Refuse("contexts.jsonl is not ASCII")
    for no, line in enumerate(text.split("\n"), 1):
        if not line:
            continue
        try:
            c = json.loads(line)
        except ValueError:
            raise Refuse(f"contexts.jsonl line {no} does not parse")
        k, p = c.get("ctx"), c.get("path")
        if not (is_int(k) and 0 <= k < N_CTX) or k in ctxs:
            raise Refuse(f"contexts.jsonl line {no}: bad or repeated ctx {k!r}")
        if not (isinstance(p, list) and len(p) == DEPTH and all(
                isinstance(d, list) and len(d) == 2 and is_int(d[0]) and 0 <= d[0] < N_STATES
                and d[1] in (0, 1) and is_int(d[1]) for d in p)):
            raise Refuse(f"contexts.jsonl ctx {k}: path is not 12 decisions [v, b]")
        vs = [v for v, _ in p]
        if len(set(vs)) != DEPTH:
            raise Refuse(f"contexts.jsonl ctx {k}: a vertex repeats on the path")
        if sum(b << (DEPTH - 1 - i) for i, (_, b) in enumerate(p)) != k:
            raise Refuse(f"contexts.jsonl ctx {k}: path bits are not k in binary")
        mis, occ = c.get("missing"), c.get("occupied")
        if not (isinstance(mis, list) and isinstance(occ, list)
                and sorted(mis) == sorted(v for v, b in p if b == 1) and len(set(mis)) == len(mis)
                and sorted(occ) == sorted(v for v, b in p if b == 0) and len(set(occ)) == len(occ)):
            raise Refuse(f"contexts.jsonl ctx {k}: missing/occupied differ from the path literals")
        if c.get("depth", DEPTH) != DEPTH:
            raise Refuse(f"contexts.jsonl ctx {k}: depth {c.get('depth')!r}")
        for d in range(DEPTH):
            key = (d, k >> (DEPTH - d))
            if pv.setdefault(key, p[d][0]) != p[d][0]:
                raise Refuse(f"contexts.jsonl: the depth-{d} prefix {key[1]} has two vertices")
        ctxs[k] = c
    if set(ctxs) != set(range(N_CTX)):
        raise Refuse(f"contexts.jsonl has {len(ctxs)} contexts, not 0..{N_CTX - 1}")
    return sha, ctxs, pv


def base_path_of(ctxline):
    """The context's 12 decisions as a Lean path, innermost first: b = 0 (zero child, occupied) -> 2."""
    return [(v, 2 if b == 0 else 1) for v, b in reversed(ctxline["path"])]


def check_out(out, campaign):
    """Refuse an output directory inside the campaign (given or real), or inside a 311 build dir.
    Creates nothing."""
    o = Path(os.path.realpath(out))
    if ".lake" in o.parts:
        raise Refuse(f"--out {out} resolves to {o}, inside a .lake directory; refusing")
    for bad in [campaign, REAL_CAMPAIGN] + PROTECTED:
        b = Path(os.path.realpath(bad))
        if o == b or b in o.parents:
            raise Refuse(f"--out {out} resolves to {o}, inside {b}; refusing")
    if o in Path(os.path.realpath(campaign)).parents or o in Path(os.path.realpath(REAL_CAMPAIGN)).parents:
        raise Refuse(f"--out {out} resolves to {o}, which contains the campaign; refusing")


def witness_files(campaign):
    runs = campaign / "runs"
    found = sorted(str(p) for p in runs.glob("ctx-*-b64.WITNESS.json"))
    if (campaign / "campaign" / "WITNESS-ALERT.txt").exists():
        found.append(str(campaign / "campaign" / "WITNESS-ALERT.txt"))
    return found


def _optval(argv, name):
    """Values of option --name (also --name=v and argparse abbreviations of at least 3 characters)."""
    vals = []
    for i, a in enumerate(argv):
        if not a.startswith("--") or len(a) < 3:
            continue
        t, eq, v = a.partition("=")
        if name.startswith(t):
            if eq:
                vals.append(v)
            elif i + 1 < len(argv):
                vals.append(argv[i + 1])
    return vals


def live_runs():
    """{ctx: [pid]} of live run_context.py processes for budget 64 (or no parsable budget), in ANY
    working directory. Reads /proc/<pid>/cmdline only; sends no signal."""
    out = {}
    me = os.getpid()
    for p in os.listdir("/proc"):
        if not p.isdigit() or int(p) == me:
            continue
        try:
            with open(f"/proc/{p}/cmdline", "rb") as f:
                raw = f.read()
        except OSError:
            continue
        argv = [a.decode("utf-8", "replace") for a in raw.split(b"\0") if a]
        if not any(a.endswith("run_context.py") for a in argv):
            continue
        budgets = _optval(argv, "--budget")
        if budgets and all(b.strip() != str(BUDGET) for b in budgets):
            try:
                if all(int(b) != BUDGET for b in budgets):
                    continue
            except ValueError:
                pass
        for c in _optval(argv, "--ctx"):
            try:
                out.setdefault(int(c), []).append(int(p))
            except ValueError:
                pass
    return out


# ----------------------------------------------------------------------------------------------
# one context: readiness, reading, checks

def file_rec(path, raw=None):
    st = os.stat(path)
    return {"path": str(path), "size": st.st_size, "mtime_ns": st.st_mtime_ns,
            "sha256": sha256_bytes(raw) if raw is not None else sha256_file(path)}


def read_result(campaign, k, live, now, named):
    """(result dict, raw bytes, file record) or NotReady / NotClosed / Refuse."""
    rp = campaign / "runs" / f"ctx-{k}-b64.result.json"
    if not rp.exists():
        raise NotReady("no result.json")
    if k in live:
        raise NotReady(f"live run_context.py --budget 64 --ctx {k} (pid {live[k]})")
    st = os.stat(rp)
    if now - st.st_mtime < MIN_AGE:
        raise NotReady(f"result.json is {now - st.st_mtime:.0f} s old (< {MIN_AGE:.0f} s)")
    with open(rp, "rb") as f:
        raw = f.read()
    try:
        res = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        raise NotReady("result.json does not parse")
    if not isinstance(res, dict):
        raise NotReady("result.json is not an object")
    rec = {"path": str(rp), "size": len(raw), "mtime_ns": st.st_mtime_ns, "sha256": sha256_bytes(raw)}
    status = res.get("status")
    if status == "witness":
        raise RefuseAll(f"ctx {k}: result status 'witness'")
    if status != "closed":
        if named:
            raise Refuse(f"ctx {k}: result status {status!r}, not 'closed'")
        raise NotClosed(f"status {status!r}")
    return res, raw, rec


def check_result(res, k, ctxline):
    rp = res.get("replay") or {}
    rules = res.get("rules") or {}
    checks = [
        ("ctx", res.get("ctx") == k),
        ("budget == 64", res.get("budget") == BUDGET and is_int(res.get("budget"))),
        ("status closed", res.get("status") == "closed"),
        ("replay.ok", rp.get("ok") is True),
        ("replay.pending == 12", rp.get("pending") == DEPTH),
        ("replay.leaves_checked == leaves", is_int(res.get("leaves")) and rp.get("leaves_checked") == res.get("leaves")),
        ("pending == 0", res.get("pending") == 0),
        ("rules.catalog_sha256", rules.get("catalog_sha256") == SOURCE_SHA),
        ("missing == contexts.jsonl", res.get("missing") == ctxline["missing"]),
        ("occupied == contexts.jsonl", res.get("occupied") == ctxline["occupied"]),
        ("nodes is an int", is_int(res.get("nodes"))),
    ]
    bad = [name for name, ok in checks if not ok]
    if bad:
        raise Refuse(f"ctx {k}: result.json fails {bad}")


def read_tree(campaign, k, now, res_mtime=None):
    """(tree dict, gz raw bytes, json sha256, file record) or NotReady. A missing or broken gz is NotReady
    while result.json (written after the gz) is at most GZ_DAMAGE_AGE s old, and a Refuse after that."""
    gp = campaign / "runs" / f"ctx-{k}-b64.json.gz"

    def broken(why):
        if res_mtime is not None and now - res_mtime > GZ_DAMAGE_AGE:
            return Refuse(f"ctx {k}: {why}, but result.json is {now - res_mtime:.0f} s old (> {GZ_DAMAGE_AGE:.0f} s): "
                          "the tree file is damaged")
        return NotReady(why)

    if not gp.exists():
        raise broken("no tree .json.gz")
    st = os.stat(gp)
    if now - st.st_mtime < MIN_AGE:
        raise NotReady(f"tree gz is {now - st.st_mtime:.0f} s old (< {MIN_AGE:.0f} s)")
    with open(gp, "rb") as f:
        graw = f.read()
    try:
        js = gzip.decompress(graw)
    except (EOFError, OSError, zlib.error) as e:
        raise broken(f"tree gz does not decompress ({type(e).__name__}: {e})")
    try:
        tree = json.loads(js)
    except (ValueError, UnicodeDecodeError) as e:
        raise broken(f"tree JSON does not parse ({type(e).__name__})")
    if not isinstance(tree, dict):
        raise broken("tree JSON is not an object")
    rec = {"path": str(gp), "size": len(graw), "mtime_ns": st.st_mtime_ns, "sha256": sha256_bytes(graw)}
    return tree, graw, sha256_bytes(js), rec


def check_tree_header(tree, k, ctxline):
    checks = [
        ("context", tree.get("context") == k),
        ("budget == 64", tree.get("budget") == BUDGET and is_int(tree.get("budget"))),
        ("status closed", tree.get("status") == "closed"),
        ("root == 0", tree.get("root") == 0 and is_int(tree.get("root"))),
        ("path == contexts.jsonl", tree.get("path") == ctxline["path"]),
        ("missing == contexts.jsonl", tree.get("missing") == ctxline["missing"]),
        ("occupied == contexts.jsonl", tree.get("occupied") == ctxline["occupied"]),
        ("nodes is a non-empty list", isinstance(tree.get("nodes"), list) and len(tree["nodes"]) > 0),
    ]
    bad = [name for name, ok in checks if not ok]
    if bad:
        raise Refuse(f"ctx {k}: tree fails {bad}")


def renumber(nodes, k):
    """Zero-first preorder renumbering. Returns (ty, vx, z, o, order) in the new numbering; refuses
    anything that is not a tree of branch / weighted / over_budget nodes rooted at 0."""
    N = len(nodes)
    seen = bytearray(N)
    order, stack = [], [0]
    while stack:
        j = stack.pop()
        if seen[j]:
            raise Refuse(f"ctx {k}: node {j} is reached twice (not a tree)")
        seen[j] = 1
        order.append(j)
        nd = nodes[j]
        if not isinstance(nd, dict):
            raise Refuse(f"ctx {k}: node {j} is not an object")
        t = nd.get("type")
        if t == "branch":
            v, zz, oo = nd.get("vertex"), nd.get("zero"), nd.get("one")
            if not (is_int(v) and 0 <= v < N_STATES and is_int(zz) and is_int(oo)
                    and 0 <= zz < N and 0 <= oo < N and zz != oo):
                raise Refuse(f"ctx {k}: bad branch node {j}")
            stack.append(oo)
            stack.append(zz)
        elif t not in ("weighted", "over_budget"):
            raise Refuse(f"ctx {k}: node {j} has type {t!r}")
    if len(order) != N:
        raise Refuse(f"ctx {k}: {N - len(order)} nodes are not reachable from the root")
    new = array("i", [0]) * N
    for i, j in enumerate(order):
        new[j] = i
    ty, vx, z, o = array("i"), array("i"), array("i"), array("i")
    for j in order:
        nd = nodes[j]
        if nd["type"] == "branch":
            ty.append(T_BRANCH); vx.append(nd["vertex"]); z.append(new[nd["zero"]]); o.append(new[nd["one"]])
        else:
            ty.append(T_WEIGHTED if nd["type"] == "weighted" else T_OVER)
            vx.append(-1); z.append(-1); o.append(-1)
    return ty, vx, z, o, order


# ----------------------------------------------------------------------------------------------
# one context: export (texts in memory)

def export_context(k, ctxline, tree, rows, args, prefix, code_caches, hashes):
    """All module texts and the manifest fields of context k (nothing written here)."""
    n, m = N_STATES, len(rows)
    nodes = tree["nodes"]
    ty, vx, z, o, order = renumber(nodes, k)
    try:
        parent, dec, count, size = shape_info(ty, z, o, 0)   # export_es311.py:167-193 (re-asserts preorder)
    except AssertionError as e:
        raise Refuse(f"ctx {k}: shape_info: {e}")
    base = base_path_of(ctxline)
    N = len(ty)

    def full(j):
        return path_of(j, parent, dec, vx, None) + base   # export_es311.py:196-203

    # Leaf replay 1 (exact full-load margin), as export_es311.py:464-487, with the full mask.
    leaf = {}
    wmax, nover, nweighted = 0, 0, 0
    for x in range(N):
        if ty[x] == T_BRANCH:
            continue
        mask = bytearray(n)
        for v, d in full(x):
            if mask[v]:
                raise Refuse(f"ctx {k}: a state is fixed twice on the path of local node {x}")
            mask[v] = d
        missing = {v for v in range(n) if mask[v] == 1}
        if ty[x] == T_OVER:
            if not len(missing) > BUDGET:
                raise Refuse(f"ctx {k}: over-budget leaf {x} has only {len(missing)} missing states")
            leaf[x] = (T_OVER,)
            nover += 1
            continue
        nd = nodes[order[x]]
        cap, ws = nd.get("capacity"), nd.get("weights")
        if not (is_int(cap) and cap >= 0 and isinstance(ws, list)):
            raise Refuse(f"ctx {k}: bad weighted leaf {x}")
        for e in ws:
            if not (isinstance(e, list) and len(e) == 2 and is_int(e[0]) and is_int(e[1])
                    and 0 <= e[0] < m and e[1] >= 0):
                raise Refuse(f"ctx {k}: bad weight entry {e!r} in leaf {x}")
        occupied = {v for v in range(n) if mask[v] == 2}
        ent = normalize(rows, [tuple(e) for e in ws], missing)          # export_es311.py:220-221
        margin = full_load_margin(n, rows, BUDGET, missing, occupied, cap, ent)
        if margin < 1:
            raise Refuse(f"ctx {k}: leaf {x} has full-load margin {margin} < 1")
        D = sum(w * rows[r][1] for r, w in ent)
        wmax = max([wmax] + [w for _, w in ent])
        leaf[x] = (T_WEIGHTED, cap, D, margin, ent, bytes(mask))
        nweighted += 1
    K = 1 << max(17, wmax.bit_length())
    assert m.bit_length() == 12
    J = K << m.bit_length()                                            # export_es311.py:308
    k_word, L, B = args.per_word, args.chunk_leaves, args.block_leaves
    srs, skeleton = cut(0, L, ty, z, o, count)                         # export_es311.py:310
    if any(u >= SKEL_STRIDE for u in skeleton):
        raise Refuse(f"ctx {k}: a skeleton node id is >= {SKEL_STRIDE}")
    modules, cur, cur_leaves = [], [], 0                               # export_es311.py:311-318
    for s in srs:
        if cur and cur_leaves + count[s] > L:
            modules.append(cur)
            cur, cur_leaves = [], 0
        cur.append(s)
        cur_leaves += count[s]
    modules.append(cur)
    if len(modules) > 99:
        raise Refuse(f"ctx {k}: {len(modules)} modules (> 99); raise --chunk-leaves")
    if sum(count[s] for s in srs) != count[0] or count[0] != nweighted + nover:
        raise Refuse(f"ctx {k}: subtree roots do not cover the leaves")
    M0 = f"(zerosF {n})"
    params = f"{CAT} {m} {n} {BUDGET}"
    sp = shapes_es311.side_params({"catalog": CATMOD, "rows": m, "states": n, "budget": BUDGET,
                                   "catalog_base": CATALOG_BASE, "prefix": prefix})

    def feas(p):
        return f"¬ ∃ holes : Fin {n} → ℕ, FFeas {params} (pmask {M0} {lean_path(p)}) holes"

    texts, mods, corrupt_info = [], [], None
    lean_failures = 0
    for i, mod in enumerate(modules):
        mm = i + 1
        stem = f"C{k:04d}{mm:02d}"
        name = f"{prefix}.{stem}"
        mod_leaves = sum(count[s] for s in mod)
        lines = [f"import {CATMOD}", "import CompactChecker.Path", "open CompactChecker",
                 "set_option maxRecDepth 100000", *OPTS,
                 *([] if args.no_profile else ["set_option profiler true"]),
                 f"namespace {name}",
                 f"-- ES(8) <= 310 compact check (budget-64 campaign), balanced side, context {k}, "
                 f"module {mm} of {len(modules)}",
                 f"-- tree gz sha256 {hashes['gz']}; tree json sha256 {hashes['json']}; "
                 f"result sha256 {hashes['result']}; source sha256 {hashes['source']}",
                 f"-- {mod_leaves} leaves under subtree roots {mod}; budget {BUDGET}; "
                 f"context path (innermost first) {lean_path(base)}",
                 f"-- chunk limit {L}, block limit {B}, K {K}, J {J}, {k_word} entries per word"]
        mod_leaf_ids = [x for s in mod for x in range(s, s + size[s]) if ty[x] != T_BRANCH]
        corrupt_leaf = None
        if args.corrupt == mm:                                         # export_es311.py:363-365
            cands = [x for x in mod_leaf_ids if leaf[x][0] == T_WEIGHTED]
            if not cands:
                raise Refuse(f"ctx {k}: --corrupt {mm}: the module has no weighted leaf")
            corrupt_leaf = min(cands, key=lambda x: (leaf[x][3], x))
        nblocks, entries, words_n, bases = 0, 0, 0, []
        margins = [leaf[x][3] for x in mod_leaf_ids if leaf[x][0] == T_WEIGHTED]
        for s in mod:
            blocks, uppers = cut(s, B, ty, z, o, count)                # export_es311.py:367
            for b in blocks:
                leaves = [x for x in range(b, b + size[b]) if ty[x] != T_BRANCH]
                maxd = max([leaf[x][2] for x in leaves if leaf[x][0] == T_WEIGHTED] + [1])
                base0 = 1 << maxd.bit_length()                         # export_es311.py:370-371
                bases.append(base0)
                cc = code_caches.setdefault(base0, {})                 # kept across contexts

                def term(x):
                    nonlocal entries, words_n, corrupt_info, lean_failures
                    if ty[x] == T_BRANCH:
                        return f"(.split {vx[x]} {term(z[x])} {term(o[x])})"
                    rec = leaf[x]
                    if rec[0] == T_OVER:
                        return ".overBudget"
                    _, cap, D, margin, ent, mask = rec
                    if x == corrupt_leaf:                              # export_es311.py:383-405
                        found = None
                        missing = {v for v in range(n) if mask[v] == 1}
                        occupied = {v for v in range(n) if mask[v] == 2}
                        for e in range(len(ent)):
                            for w in (ent[e][1] - 1, ent[e][1] + 1, 0):
                                if w < 0 or w >= K:
                                    continue
                                trial = list(ent)
                                trial[e] = (trial[e][0], w)
                                mg = full_load_margin(n, rows, BUDGET, missing, occupied, cap, trial)
                                if mg <= 0:
                                    found = (e, w, mg)
                                    break
                            if found:
                                break
                        if not found:
                            raise Refuse(f"ctx {k}: no single-weight corruption found")
                        corrupt_info = {"module": name, "leaf_node": x, "entry_index": found[0],
                                        "row": ent[found[0]][0], "old_weight": ent[found[0]][1],
                                        "new_weight": found[1], "old_margin": margin,
                                        "new_margin": found[2]}
                        ent = list(ent)
                        ent[found[0]] = (ent[found[0]][0], found[1])
                    codes = [r * K + w for r, w in ent]
                    words = pack_words(codes, k_word, J)               # export_es311.py:238-240
                    entries += len(codes)
                    words_n += len(words)
                    ok = lean_leaf_test(n, rows, m, BUDGET, base0, K, J, k_word, cap, mask, words, cc)
                    if not ok:
                        lean_failures += 1
                        if x != corrupt_leaf:
                            raise Refuse(f"ctx {k}: the Lean leaf test fails on local node {x}")
                    elif x == corrupt_leaf:
                        raise Refuse(f"ctx {k}: the corrupted leaf {x} passes the Lean leaf test")
                    return f"(.leaf {cap} (natlits% [{', '.join(map(str, words))}]))"

                p = full(b)
                lines.append(f"noncomputable def b{b} : PTree := {term(b)}")
                lines.append(f"theorem chk{b} : checkF2 {params} {base0} {K} {J} {k_word} b{b} "
                             f"(pmask {M0} {lean_path(p)}) = true := by decide +kernel")
                lines.append(f"theorem ex{b} : {feas(p)} :=")
                lines.append(f"  checkF2_feas {params} {CATALOG_BASE} {base0} {K} {J} {k_word} "
                             f"{CAT}_wf b{b} _ chk{b}")
                nblocks += 1
            for u in reversed(uppers):                                 # export_es311.py:424-427
                p = full(u)
                lines.append(f"theorem ex{u} : {feas(p)} :=")
                lines.append(f"  split_pm {params} {M0} {lean_path(p)} {vx[u]} ex{z[u]} ex{o[u]}")
        for s in mod:
            lines.append(f"#print axioms ex{s}")
        lines.append(f"end {name}")
        text = "\n".join(lines) + "\n"
        errs = shapes_es311.check_text(text, "chunk", name, sp)
        if errs:
            raise Refuse(f"ctx {k}: module {name} fails the line-shape check: {errs}")
        if text.count("(.leaf ") + text.count(".overBudget") != mod_leaves:
            raise Refuse(f"ctx {k}: module {name} leaf-term count differs")
        data = text.encode("utf-8")
        texts.append((stem, data))
        mods.append({"module": name, "file": f"src/{prefix}/{stem}.lean", "sha256": sha256_bytes(data),
                     "source_bytes": len(data), "leaves": mod_leaves,
                     "subtree_roots": [[s, count[s]] for s in mod], "blocks": nblocks, "entries": entries,
                     "words": words_n, "min_margin": min(margins) if margins else None,
                     "max_base": max(bases), "corrupted": corrupt_leaf is not None})
    if args.corrupt is not None and corrupt_info is None:
        raise Refuse(f"ctx {k}: --corrupt {args.corrupt}: no such module or no weighted leaf")
    if lean_failures != (1 if args.corrupt is not None else 0):
        raise Refuse(f"ctx {k}: {lean_failures} Lean leaf-test failures")
    margins = [leaf[x][3] for x in leaf if leaf[x][0] == T_WEIGHTED]
    info = {
        "K": K, "J": J, "base_path": [list(d) for d in base],
        "modules": mods,
        "skeleton": [{"u": u, "vertex": vx[u], "zero": z[u], "one": o[u]} for u in skeleton],
        "subtree_roots": [[s, count[s]] for s in srs],
        "stats": {"leaves": count[0], "nodes": N, "weighted": nweighted, "over_budget": nover,
                  "min_margin": min(margins) if margins else None, "max_weight": wmax,
                  "entries": sum(x["entries"] for x in mods), "words": sum(x["words"] for x in mods),
                  "lean_test_failures": lean_failures},
        "corruption": corrupt_info,
    }
    return texts, info


# ----------------------------------------------------------------------------------------------
# writing

def write_atomic(path, data):
    tmp = path.parent / f".{path.name}.tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, path)


def global_inputs(campaign, source, res_rules):
    """Hashes of the inputs shared by every context."""
    rc = campaign / "run_context.py"
    pbb_s = (res_rules or {}).get("pbb_strong")
    pbb = Path(pbb_s) if isinstance(pbb_s, str) and pbb_s else None
    out = {"contexts_jsonl": {"path": str(campaign / "contexts.jsonl"),
                              "sha256": sha256_file(campaign / "contexts.jsonl")},
           "source": {"path": str(source), "sha256": read_source(source)[0]},
           "run_context": {"path": str(rc), "sha256": sha256_file(rc) if rc.exists() else None},
           "pbb_strong": {"path": str(pbb) if pbb else None,
                          "sha256": sha256_file(pbb) if pbb and pbb.is_file() else None}}
    return out


GLOBAL_KEYS = ("contexts_jsonl", "source", "run_context", "pbb_strong")
DATA_KEYS = ("contexts_jsonl", "source")          # a change is an ALERT (or a refusal during an export)
CODE_KEYS = ("run_context", "pbb_strong")         # a change is a recorded warning ("code_changed") only


def exporter_shas():
    return {"export_es310": sha256_file(Path(__file__).resolve()),
            "export_es311": sha256_file(Path(X311.__file__).resolve())}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--campaign", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--all-closed", action="store_true", help="every closed context not yet exported")
    g.add_argument("--ctx", help="comma-separated context numbers")
    ap.add_argument("--chunk-leaves", type=int, default=12000)
    ap.add_argument("--block-leaves", type=int, default=64)
    ap.add_argument("--per-word", type=int, required=True)
    ap.add_argument("--prefix", default=DEFAULT_PREFIX)
    ap.add_argument("--corrupt", type=int, help="module index within the one --ctx context: break its "
                    "min-margin leaf (rejection test; not with the default prefix)")
    ap.add_argument("--refresh-exporter", action="store_true",
                    help="re-export contexts whose inputs are unchanged but whose exporter sha256 differs")
    ap.add_argument("--no-profile", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    summary = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "out": str(args.out),
               "prefix": args.prefix, "mode": "all-closed" if args.all_closed else "ctx",
               "exported": [], "skipped_same": [], "stale_exporter": [], "mtime_changed": [],
               "not_ready": {}, "not_closed": {}, "refused": None, "refused_ctx": {}, "code_changed": [],
               "alert": None}
    code = EXIT_OK
    try:
        code = run(args, summary, t0)
    except Refuse as e:
        summary["refused"] = str(e)
        log(f"REFUSED: {e}")
        code = EXIT_REFUSE
    summary["exit"] = code
    summary["seconds"] = round(time.time() - t0, 1)
    print(json.dumps(summary), flush=True)
    sys.exit(code)


def run(args, summary, t0):
    if not re.fullmatch(r"[A-Z][A-Za-z0-9]*", args.prefix):
        raise Refuse(f"bad prefix {args.prefix!r}")
    if args.per_word < 1 or args.chunk_leaves < 1 or args.block_leaves < 1:
        raise Refuse("--per-word, --chunk-leaves and --block-leaves must be positive")
    campaign = Path(os.path.realpath(args.campaign))
    check_out(args.out, campaign)
    named = None
    if args.ctx is not None:
        try:
            named = sorted({int(x) for x in args.ctx.split(",") if x.strip()})
        except ValueError:
            raise Refuse(f"bad --ctx {args.ctx!r}")
        if not named or not all(0 <= x < N_CTX for x in named):
            raise Refuse(f"bad --ctx {args.ctx!r}")
    if args.corrupt is not None:
        if args.prefix == DEFAULT_PREFIX:
            raise Refuse("--corrupt is a test switch; use a test prefix (E310BX), never E310B")
        if named is None or len(named) != 1:
            raise Refuse("--corrupt needs exactly one --ctx")
    # global inputs
    source_sha, n, rows = read_source(args.source)                       # export_es311.py:66-78
    if source_sha != SOURCE_SHA:
        raise Refuse(f"source sha256 {source_sha} != {SOURCE_SHA}")
    if n != N_STATES or len(rows) != N_ROWS:
        raise Refuse(f"source has {n} states and {len(rows)} rows")
    wit = witness_files(campaign)
    if wit:
        raise Refuse(f"WITNESS files present: {wit}")
    ctx_sha, ctxs, _ = load_contexts(campaign / "contexts.jsonl")
    # output dir and lock
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    lockf = open(out / ".export.lock", "w")
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log(f"another export_es310.py / merge_es310.py holds {out / '.export.lock'}")
        summary["refused"] = "locked"
        return EXIT_LOCKED
    if (out / ALERT_NAME).exists():
        summary["alert"] = f"{out / ALERT_NAME} exists; resolve it by hand first"
        log(summary["alert"])
        return EXIT_ALERT
    ctx_dir, src_dir = out / "ctx", out / "src" / args.prefix
    exsha = exporter_shas()
    # Existing exports: parameters, then a re-hash of every one of them.
    existing = {}
    for f in sorted(ctx_dir.glob("ctx-*.json")) if ctx_dir.exists() else []:
        try:
            man = json.loads(f.read_bytes())
        except ValueError:
            raise Refuse(f"{f} does not parse")
        if f.name != f"ctx-{man.get('ctx', -1):04d}.json":
            raise Refuse(f"{f}: file name and ctx {man.get('ctx')!r} differ")
        existing[man["ctx"]] = man
    want = {"budget": BUDGET, "per_word": args.per_word, "chunk_leaves": args.chunk_leaves,
            "block_leaves": args.block_leaves, "catalog_base": CATALOG_BASE}
    any_rules = None
    for kk, man in existing.items():
        got = {x: man["params"].get(x) for x in want}
        if man.get("prefix") != args.prefix or got != want or man.get("campaign") != str(campaign):
            raise Refuse(f"OUT already holds ctx {kk} exported with prefix {man.get('prefix')!r}, "
                         f"params {got}, campaign {man.get('campaign')!r}; this run: {args.prefix!r}, {want}, "
                         f"{str(campaign)!r}")
    # The rules (pbb_strong path) of the first readable result decide the global input record; the
    # pbb_strong path must be the same in every result.
    alerts = []
    gl_cache = {}

    def globals_for(rules):
        key = (rules or {}).get("pbb_strong", "")
        if key not in gl_cache:
            gl_cache[key] = global_inputs(campaign, args.source, rules)
        return gl_cache[key]

    for kk, man in sorted(existing.items()):
        inp = man["inputs"]
        for which in ("result", "tree_gz"):
            p = Path(inp[which]["path"])
            if not p.exists():
                alerts.append(f"ctx {kk}: {which} {p} is gone")
                continue
            now_rec = file_rec(p)
            if now_rec["sha256"] != inp[which]["sha256"] or now_rec["size"] != inp[which]["size"]:
                alerts.append(f"ctx {kk}: {which} {p} changed: sha256 {inp[which]['sha256']} -> "
                              f"{now_rec['sha256']}, size {inp[which]['size']} -> {now_rec['size']}")
            elif now_rec["mtime_ns"] != inp[which]["mtime_ns"]:
                summary["mtime_changed"].append(kk)
        gl = globals_for({"pbb_strong": inp["pbb_strong"]["path"]})
        for key in DATA_KEYS:
            if gl[key]["sha256"] != inp[key]["sha256"]:
                alerts.append(f"ctx {kk}: {key} changed: {inp[key]['sha256']} -> {gl[key]['sha256']}")
        for key in CODE_KEYS:
            if gl[key]["sha256"] != inp[key]["sha256"]:
                w = f"{key} differs from the one recorded at export: {inp[key]['sha256']} -> {gl[key]['sha256']}"
                if w not in summary["code_changed"]:
                    summary["code_changed"].append(w)
                    log("warning: " + w + " (recorded only; campaign code cannot affect soundness)")
    if alerts:
        text = (f"{time.strftime('%Y-%m-%d %H:%M:%S %Z')} export_es310.py: inputs of already-exported contexts "
                f"changed; nothing was exported and the old export is untouched.\n" + "\n".join(alerts) + "\n")
        write_atomic(out / ALERT_NAME, text.encode())
        summary["alert"] = alerts
        log("ALERT: " + "; ".join(alerts[:5]))
        return EXIT_ALERT
    # Candidates.
    if named is not None:
        cands = named
    else:
        cands = []
        for p in (campaign / "runs").glob("ctx-*-b64.result.json"):
            try:
                kk = int(p.name[4:-len("-b64.result.json")])
            except ValueError:
                continue
            if 0 <= kk < N_CTX:
                cands.append(kk)
        cands = sorted(set(cands) | set(existing))
    todo = []
    for kk in cands:
        man = existing.get(kk)
        if man is not None:
            if args.corrupt is not None:
                raise Refuse(f"ctx {kk} is already exported in OUT; --corrupt needs a fresh OUT")
            if man["exporter_sha256"] == exsha:
                summary["skipped_same"].append(kk)
                continue
            if not args.refresh_exporter:
                summary["stale_exporter"].append(kk)
                continue
        todo.append(kk)
    # Pre-scan: readiness and the result.json checks, before anything is written.
    live = live_runs()
    now = time.time()
    ready = []
    for kk in todo:
        try:
            res, rraw, rrec = read_result(campaign, kk, live, now, named is not None)
            check_result(res, kk, ctxs[kk])
            ready.append(kk)
        except NotReady as e:
            summary["not_ready"][str(kk)] = str(e)
        except NotClosed as e:
            summary["not_closed"][str(kk)] = str(e)
        except RefuseAll:
            raise
        except Refuse as e:  # this context only (fixer 6 Nov, ops review 3c)
            summary["refused_ctx"][str(kk)] = str(e)
            log(f"REFUSED ctx {kk}: {e}")
    code_caches = {}

    def export_one(kk):
        tk = time.time()
        live = live_runs()
        now = time.time()
        try:
            res, rraw, rrec = read_result(campaign, kk, live, now, named is not None)
            check_result(res, kk, ctxs[kk])
            tree, graw, json_sha, grec = read_tree(campaign, kk, now, rrec["mtime_ns"] / 1e9)
        except NotReady as e:
            summary["not_ready"][str(kk)] = str(e)
            return
        except NotClosed as e:
            summary["not_closed"][str(kk)] = str(e)
            return
        check_tree_header(tree, kk, ctxs[kk])
        if len(tree["nodes"]) != res["nodes"]:
            raise Refuse(f"ctx {kk}: tree has {len(tree['nodes'])} nodes, result says {res['nodes']}")
        gl = globals_for(res.get("rules"))
        if gl["contexts_jsonl"]["sha256"] != ctx_sha:
            raise RefuseAll("contexts.jsonl changed during the run")
        if gl["pbb_strong"]["sha256"] is None or gl["run_context"]["sha256"] is None:
            raise RefuseAll(f"ctx {kk}: pbb_strong.py ({gl['pbb_strong']['path']}) or run_context.py missing")
        hashes = {"gz": grec["sha256"], "json": json_sha, "result": rrec["sha256"], "source": source_sha}
        texts, info = export_context(kk, ctxs[kk], tree, rows, args, args.prefix, code_caches, hashes)
        st = info["stats"]
        if (st["leaves"] != res["leaves"] or st["nodes"] != res["nodes"]
                or st["weighted"] != res.get("weighted") or st["over_budget"] != res.get("over_budget")):
            raise Refuse(f"ctx {kk}: counts {st['leaves']}/{st['nodes']}/{st['weighted']}/{st['over_budget']} "
                         f"differ from the result's {res['leaves']}/{res['nodes']}/{res.get('weighted')}/"
                         f"{res.get('over_budget')}")
        # Write modules to tmp names; final checks; rename; manifest last.
        src_dir.mkdir(parents=True, exist_ok=True)
        ctx_dir.mkdir(parents=True, exist_ok=True)
        tmps = []
        try:
            for stem, data in texts:
                tmp = src_dir / f".{stem}.lean.tmp"
                with open(tmp, "wb") as f:
                    f.write(data)
                tmps.append((tmp, src_dir / f"{stem}.lean"))
            # re-read and re-hash every input; repeat the /proc scan
            changed = []
            for name, rec in (("result", rrec), ("tree_gz", grec)):
                now_rec = file_rec(rec["path"])
                if any(now_rec[x] != rec[x] for x in ("size", "mtime_ns", "sha256")):
                    changed.append(f"{name}: {rec} -> {now_rec}")
            gl2 = global_inputs(campaign, args.source, res.get("rules"))
            for key in DATA_KEYS:
                if gl2[key]["sha256"] != gl[key]["sha256"]:
                    raise RefuseAll(f"{key} changed during the export of ctx {kk}")
            for key in CODE_KEYS:
                if gl2[key]["sha256"] != gl[key]["sha256"]:
                    w = f"{key} changed during the export of ctx {kk}: {gl[key]['sha256']} -> {gl2[key]['sha256']}"
                    summary["code_changed"].append(w)
                    log("warning: " + w + " (recorded only)")
            if witness_files(campaign):
                raise RefuseAll(f"a WITNESS file appeared during the export of ctx {kk}: {witness_files(campaign)}")
            if kk in live_runs():
                changed.append("a live run_context.py for this context appeared")
            if changed:
                raise Refuse(f"ctx {kk}: inputs changed during the export: {changed}")
        except BaseException:
            for tmp, _ in tmps:
                try:
                    tmp.unlink()
                except FileNotFoundError:
                    pass
            raise
        new_files = set()
        for tmp, final in tmps:
            os.replace(tmp, final)
            new_files.add(final.name)
        for f in src_dir.glob(f"C{kk:04d}[0-9][0-9].lean"):
            if f.name not in new_files:      # left by an earlier failed or refreshed export of this context
                log(f"removing stale {f}")
                f.unlink()
        man = {
            "ctx": kk, "prefix": args.prefix, "campaign": str(campaign),
            "params": {"budget": BUDGET, "K": info["K"], "J": info["J"], "per_word": args.per_word,
                       "chunk_leaves": args.chunk_leaves, "block_leaves": args.block_leaves,
                       "catalog_base": CATALOG_BASE, "catalog": CATMOD, "rows": N_ROWS, "states": N_STATES,
                       "profile": not args.no_profile},
            "ctx_path": ctxs[kk]["path"],
            "base_path": info["base_path"],
            "inputs": {"result": rrec, "tree_gz": grec, "tree_json_sha256": json_sha,
                       **{key: gl[key] for key in GLOBAL_KEYS}},
            "exporter_sha256": exsha,
            "modules": info["modules"],
            "subtree_roots": info["subtree_roots"],
            "skeleton": info["skeleton"],
            "stats": info["stats"],
            "result": {"leaves": res["leaves"], "nodes": res["nodes"], "weighted": res.get("weighted"),
                       "over_budget": res.get("over_budget"),
                       "minimum_margin": (res.get("replay") or {}).get("minimum_margin")},
            "corruption": info["corruption"],
        }
        write_atomic(ctx_dir / f"ctx-{kk:04d}.json", (json.dumps(man, indent=1) + "\n").encode())
        summary["exported"].append({"ctx": kk, "leaves": info["stats"]["leaves"],
                                    "modules": len(info["modules"]), "K": info["K"],
                                    "skeleton": len(info["skeleton"]),
                                    "min_margin": info["stats"]["min_margin"],
                                    "seconds": round(time.time() - tk, 2)})
        log(f"ctx {kk}: {info['stats']['leaves']} leaves, {len(info['modules'])} module(s), K {info['K']}, "
            f"{time.time() - tk:.1f} s")

    for kk in ready:
        try:
            export_one(kk)
        except RefuseAll:
            raise
        except Refuse as e:  # this context only; its tmp files are already removed (fixer 6 Nov, ops review 3c)
            summary["refused_ctx"][str(kk)] = str(e)
            log(f"REFUSED ctx {kk}: {e}")
    if summary["refused_ctx"]:
        return EXIT_REFUSE
    if named is not None and (summary["not_ready"] or summary["not_closed"]):
        return EXIT_NOT_READY
    if summary["stale_exporter"]:
        log(f"{len(summary['stale_exporter'])} contexts were exported by another exporter sha256 "
            f"(e.g. {summary['stale_exporter'][:5]}); re-export them with --refresh-exporter")
        return EXIT_STALE
    return EXIT_OK


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()
