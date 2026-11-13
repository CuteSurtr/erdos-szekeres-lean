#!/usr/bin/env python3
"""Independent coverage check of an ES(8) <= 310 compact export (6 November 2026). ES(8) <= 310 is NOT
proved; this script only checks bookkeeping in front of Lean.

  coverage_es310.py OUT --partial            every context manifest in OUT/ctx (no Root)
  coverage_es310.py OUT --subtree D:P        the contexts under the depth-D node with prefix P, and the
                                             sub-Root written there (OUT/src/<Prefix>/Root.lean)
  coverage_es310.py OUT --complete           all 4,096 contexts and the Root at [] (budget 64)
  options: --campaign C --source SRC --prefix E310B --jobs N --ctx k1,k2 (partial only)
           --cache FILE (partial only) --tree63-shape FILE --exporter-sha256 HEX --report FILE

Independence. This file imports nothing from export_es310.py, export_es311.py or merge_es310.py;
the only import from the pipeline is shapes_es311 (check_text / side_params, the line grammar). It
parses the campaign's tree files itself (stdlib json), renumbers them into zero-first preorder
itself, recomputes every path from contexts.jsonl and the trees, and re-derives the leaf words.

What is checked (design section B, steps 1-6; the critiques' fixes applied):
 1. contexts.jsonl: ctx 0..4095 exactly once; every path has 12 decisions [v, b] (b = 0 occupied,
    the zero child; b = 1 missing); the 12 bits read from the root are k in binary; every prefix
    has one branching vertex; no vertex repeats on a path; missing/occupied equal the 1/0 literals.
 2. inputs: each context manifest's result.json and tree .json.gz re-hash (sha256, size) equal to the
    current campaign files; the tree JSON, contexts.jsonl and source sha256 equal the current ones
    (run_context.py and pbb_strong.py, campaign code that cannot affect soundness, must be recorded;
    a value that differs from the current file, or between contexts, is a warning only: fixer 6 Nov,
    soundness review item 7); the result is still closed, budget 64, replay ok, replay pending
    12, leaves_checked == leaves, pending 0, catalog sha256 = sha256(source); no WITNESS file.
 3. per context, from the tree (own parse and own zero-first preorder; local id 0 = context root):
    tree fields (context, budget 64, closed, root 0, path/missing/occupied = contexts.jsonl); a
    tree (every node reached once, types branch/weighted/over_budget); no state fixed twice on a
    full path; leaves/nodes = result.json = manifest stats; subtree roots (SRs) cover every leaf
    exactly once; SR and module leaf counts; the internal skeleton (nodes outside every SR) equals
    the manifest's; canonical SR cut and module packing; module names C<kkkk><mm> and files;
    module sha256; number of .leaf/.overBudget terms; every b<j> is exactly the preorder
    serialization of the subtree at j: split vertices, leaf capacities, .overBudget, and the leaf
    words re-derived from the tree's weights after normalization (keep (r, w) iff w != 0 and
    rhs(r) > |missing(full path) & support(r)|, export_es311.py:220-221 semantics), packed as
    codes r*K + w, k per word in base J (equality implies the leaf entries are a subset of the
    tree leaf's weights with the same row/weight values; on a mismatch that subset relation is
    decoded and reported); the block base (least power of 2 above the block's largest demand
    sum); K, J, k equal the context parameters; every chk/ex statement and every split_pm carries
    the recomputed full path (local path innermost first ++ context base path) and the budget
    literal 64; blocks and combinations tile each SR (split_pm vertex and children = the tree's);
    canonical block cut; one #print axioms per SR; strict line shapes (shapes_es311.check_text).
 4. Root (--subtree / --complete): sha256 = merged manifest; shape check; imports = exactly the
    modules of the contexts in scope; the skeleton theorems ex<1000000000 + 2^d + p> (d < 12) and
    ex<(k+1)*100000 + u> (context-internal) each defined exactly once, with the recomputed path,
    vertex and children (zero child first); every context root and every SR referenced exactly
    once, from its own module; `theorem root` at the scope's path ([] for --complete) with budget
    64; definitions before use.
 5. --tree63-shape: the 4,096 context paths walk tree-63 (the exporter's shape cache) to distinct
    depth-12 nodes, each equal to the context's recorded preorder index (not needed for soundness).
 6. --partial: no Root; with --cache, a context whose manifest sha256, module sha256s, input
    hashes and this script's sha256 are unchanged since a PASS skips the expensive part of step 3.
--exporter-sha256 HEX must be 64 hex digits and must EQUAL the export_es310 sha256 that every context
manifest records (fixer 6 Nov, soundness review item 4: it was a substring test). The run holds a shared
flock on OUT/.export.lock when that file exists (opened read-only), so it never reads an export that
export_es310.py or merge_es310.py is changing; if one of them holds it, exit 4 (retry later; ops review 8).
Lean, not this script, decides correctness: a block Lean accepts certifies its statement, and the
Root's split_pm steps need both children with literal paths. This check makes sure that what Lean
is asked to check is exactly the campaign's trees, covering every leaf once, at the right paths.
Exit 0 PASS, 1 FAIL, 2 usage or environment error, 4 OUT/.export.lock is held by an exporter or merge.
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
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import shapes_es311  # noqa: E402  (line grammar only; nothing from any exporter)

REPO = HERE.parent.parent
CAMPAIGN = Path("/home/jay/research/data/es8-b64-pilot-20261105")
SRC = REPO / "experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json"
PBB = REPO / "experiments/omission-final311-2026-10-14/search/pbb_strong.py"
BAL_SHA = "acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72"
N_STATES, M_ROWS, BUDGET, CATALOG_BASE = 252, 3131, 64, 1 << 22
CATMOD, CAT = "CompactChecker.Fcat62", "fcat62"
PARAMS = f"{CAT} {M_ROWS} {N_STATES} {BUDGET}"
NCTX, DEPTH = 4096, 12
SKEL_BASE, CTX_MUL = 10 ** 9, 100000
MAX_MSG = 12  # failure messages kept per check (all failures are counted)
HEX64 = re.compile(r"[0-9a-f]{64}")

# Lean line patterns (parsed here; shapes_es311 separately checks the full line grammar)
P = r"(\[[^\]]*\])"
RE_DEF = re.compile(r"noncomputable def b(\d+) : PTree := (.*)")
RE_CHK = re.compile(r"theorem chk(\d+) : checkF2 (\w+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) b(\d+) "
                    r"\(pmask \(zerosF (\d+)\) " + P + r"\) = true := by decide \+kernel")
RE_EX = re.compile(r"theorem ex(\d+) : ¬ ∃ holes : Fin (\d+) → ℕ, FFeas (\w+) (\d+) (\d+) (\d+) "
                   r"\(pmask \(zerosF (\d+)\) " + P + r"\) holes :=")
RE_FEAS = re.compile(r"  checkF2_feas (\w+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\w+)_wf b(\d+) _ "
                     r"chk(\d+)")
RE_SPLIT = re.compile(r"  split_pm (\w+) (\d+) (\d+) (\d+) \(zerosF (\d+)\) " + P + r" (\d+) (\S+) (\S+)")
RE_ROOT = re.compile(r"theorem root : ¬ ∃ holes : Fin (\d+) → ℕ, FFeas (\w+) (\d+) (\d+) (\d+) "
                     r"\(pmask \(zerosF (\d+)\) " + P + r"\) holes := (\S+)")
RE_PRINT = re.compile(r"#print axioms (\w+)")
RE_IMPORT = re.compile(r"import (\S+)")
TOK = re.compile(r"\(\.split (\d+) |\(\.leaf (\d+) \(natlits% \[([0-9, ]*)\]\)\)|\.overBudget")


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def is_int(x):
    return type(x) is int


def pstr(pairs):
    """Lean list literal of (vertex, decision) pairs, as the exporter writes it."""
    return "[" + ", ".join(f"({v}, {x})" for v, x in pairs) + "]"


class Rec:
    """Failure collector: counts every failure per check, keeps the first MAX_MSG messages."""

    def __init__(self):
        self.checks, self.warn = {}, []

    def ran(self, name):
        self.checks.setdefault(name, [0, []])

    def fail(self, name, msg):
        c = self.checks.setdefault(name, [0, []])
        c[0] += 1
        if len(c[1]) < MAX_MSG:
            c[1].append(msg)

    def check(self, name, cond, msg):
        self.ran(name)
        if not cond:
            self.fail(name, msg)
        return bool(cond)

    def merge(self, other):
        for name, (n, msgs) in other["checks"].items():
            c = self.checks.setdefault(name, [0, []])
            c[0] += n
            c[1].extend(msgs[:max(0, MAX_MSG - len(c[1]))])
        self.warn.extend(other["warn"])

    def dump(self):
        return {"checks": self.checks, "warn": self.warn}


# ----------------------------------------------------------------------------------------------
# step 1: contexts.jsonl


def load_contexts(R, path):
    raw = open(path, "rb").read()
    lines = raw.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    ctxs = {}
    for i, ln in enumerate(lines):
        try:
            c = json.loads(ln)
        except ValueError as e:
            R.fail("contexts_jsonl", f"line {i + 1}: not JSON ({e})")
            continue
        k, pth = c.get("ctx"), c.get("path")
        if not (is_int(k) and 0 <= k < NCTX) or k in ctxs:
            R.fail("contexts_jsonl", f"line {i + 1}: ctx {k!r} out of range or repeated")
            continue
        if not (isinstance(pth, list) and len(pth) == DEPTH and all(
                isinstance(e, list) and len(e) == 2 and is_int(e[0]) and 0 <= e[0] < N_STATES
                and e[1] in (0, 1) and is_int(e[1]) for e in pth)):
            R.fail("contexts_jsonl", f"ctx {k}: path is not 12 decisions [v, 0|1]")
            continue
        bits = 0
        for _, b in pth:
            bits = 2 * bits + b
        R.check("contexts_jsonl", bits == k, f"ctx {k}: path bits read from the root give {bits}")
        vs = [v for v, _ in pth]
        R.check("contexts_jsonl", len(set(vs)) == DEPTH, f"ctx {k}: a vertex repeats on the path")
        mis, occ = c.get("missing"), c.get("occupied")
        R.check("contexts_jsonl", isinstance(mis, list) and isinstance(occ, list)
                and sorted(mis) == sorted(v for v, b in pth if b == 1)
                and sorted(occ) == sorted(v for v, b in pth if b == 0),
                f"ctx {k}: missing/occupied differ from the path literals")
        if "depth" in c:
            R.check("contexts_jsonl", c["depth"] == DEPTH, f"ctx {k}: depth {c['depth']}")
        ctxs[k] = c
    R.check("contexts_jsonl", sorted(ctxs) == list(range(NCTX)),
            f"{len(ctxs)} distinct contexts, expected 0..{NCTX - 1}")
    vert = [dict() for _ in range(DEPTH)]
    for k, c in ctxs.items():
        for d in range(DEPTH):
            p, v = k >> (DEPTH - d), c["path"][d][0]
            if vert[d].setdefault(p, v) != v:
                R.fail("contexts_jsonl", f"prefix (depth {d}, {p}) branches on {vert[d][p]} and {v}")
    for d in range(DEPTH):
        R.check("contexts_jsonl", len(vert[d]) == 1 << d, f"depth {d}: {len(vert[d])} prefixes")
    return ctxs, vert, sha_bytes(raw)


def base_pairs(ctx_line):
    """Context base path, innermost first, Lean decisions (2 = occupied/zero, 1 = missing/one)."""
    return [(v, 2 if b == 0 else 1) for v, b in reversed(ctx_line["path"])]


def skel_pairs(vert, d, p):
    """Path of the skeleton node at depth d with prefix p (bit 0 = zero child = (v, 2))."""
    out = []
    for i in range(d - 1, -1, -1):
        v = vert[i][p >> (d - i)]
        out.append((v, 2 if (p >> (d - 1 - i)) & 1 == 0 else 1))
    return out


# ----------------------------------------------------------------------------------------------
# source rows (own parse)

SUPP, RHS = None, None


def load_rows(path):
    raw = open(path, "rb").read()
    data = json.loads(raw)
    supp, rhs = [], []
    assert len(data["states"]) == N_STATES and len(data["constraints"]) == M_ROWS
    for row in data["constraints"]:
        s, d = row["support"], row["rhs"]
        assert all(is_int(i) and 0 <= i < N_STATES for i in s) and len(set(s)) == len(s)
        assert is_int(d) and 0 <= d <= len(s)
        mask = 0
        for i in s:
            mask |= 1 << i
        supp.append(mask)
        rhs.append(d)
    return sha_bytes(raw), supp, rhs


def init_worker(src):
    global SUPP, RHS
    _, SUPP, RHS = load_rows(src)


# ----------------------------------------------------------------------------------------------
# context manifest helpers (only the pinned fields are relied on; the inputs block is resolved by
# file name and key words, so that the checker does not depend on the exporter's key spelling)


def resolve_inputs(inputs):
    """{class: [records]} for result, gz, tree_json, contexts, source, run_context, pbb."""
    found = {}

    def add(cls, rec):
        found.setdefault(cls, []).append(rec)

    def walk(d, kp):
        for key, val in d.items():
            name = (kp + "/" + str(key)).lower()
            if isinstance(val, dict):
                if isinstance(val.get("path"), str) and isinstance(val.get("sha256"), str):
                    base = os.path.basename(val["path"])
                    if base.endswith("-b64.result.json"):
                        add("result", val)
                    elif base.endswith("-b64.json.gz"):
                        add("gz", val)
                    elif base == "contexts.jsonl":
                        add("contexts", val)
                    elif base == "run_context.py":
                        add("run_context", val)
                    elif base == "pbb_strong.py":
                        add("pbb", val)
                    elif base.endswith(".json") and "source" in base or base == "balanced-v2-source.json":
                        add("source", val)
                    for k2, v2 in val.items():
                        if k2 != "sha256" and isinstance(v2, str) and HEX64.fullmatch(v2):
                            if "json" in k2.lower() and base.endswith(".json.gz"):
                                add("tree_json", {"sha256": v2})
                    walk({k2: v2 for k2, v2 in val.items() if isinstance(v2, dict)}, name)
                else:
                    walk(val, name)
            elif isinstance(val, str) and HEX64.fullmatch(val):
                cls = ("pbb" if "pbb" in name else "run_context" if "run_context" in name else
                       "contexts" if "context" in name else
                       "source" if ("source" in name or "catalog" in name or "src" in name) else
                       "tree_json" if "json" in name else None)
                if cls:
                    add(cls, {"sha256": val})

    walk(inputs, "")
    return found


def one_sha(recs):
    vals = {r["sha256"] for r in recs}
    return vals.pop() if len(vals) == 1 else None


def exporter_value(man):
    for key in sorted(man):
        if "exporter" in key.lower():
            return man[key]
    return None


def module_ref(prefix, k, mi, s):
    return f"{prefix}.C{k:04d}{mi:02d}.ex{s}"


def ctx_root_info(R, k, man, prefix, base):
    """From a context manifest: the depth-12 reference of the context root and the Root theorems of
    its internal skeleton {id: (path string, vertex, zero ref, one ref)}; the deep check verifies
    the manifest's SRs and skeleton against the tree."""
    srmod = {}
    for mi, mm in enumerate(man.get("modules") or [], start=1):
        for s in sr_ids(mm):
            if s in srmod:
                R.fail("root_ctx_info", f"ctx {k}: SR {s} listed twice")
            srmod[s] = mi
    skel = {}
    for e in man.get("skeleton") or []:
        try:
            skel[int(e["u"])] = (int(e["vertex"]), int(e["zero"]), int(e["one"]))
        except (KeyError, TypeError, ValueError):
            R.fail("root_ctx_info", f"ctx {k}: bad skeleton entry {e!r}")
    par = {}
    for u, (v, z, o) in skel.items():
        par[z], par[o] = (u, 2), (u, 1)

    def ref(c):
        if c in srmod:
            return module_ref(prefix, k, srmod[c], c)
        if c in skel:
            return f"ex{(k + 1) * CTX_MUL + c}"
        R.fail("root_ctx_info", f"ctx {k}: node {c} is neither an SR nor a skeleton node")
        return f"<missing ctx {k} node {c}>"

    thms = {}
    for u, (v, z, o) in skel.items():
        if not R.check("root_ctx_info", 0 <= u < CTX_MUL, f"ctx {k}: skeleton id {u} >= {CTX_MUL}"):
            continue
        loc, x, guard = [], u, 0
        while x != 0 and guard < len(skel) + 2:
            q, dd = par.get(x, (None, None))
            if q is None:
                R.fail("root_ctx_info", f"ctx {k}: skeleton node {x} has no parent in the skeleton")
                break
            loc.append((skel[q][0], dd))
            x, guard = q, guard + 1
        thms[(k + 1) * CTX_MUL + u] = (pstr(loc + base), v, ref(z), ref(o))
    return ref(0), thms, srmod


def sr_ids(mm):
    out = []
    for e in mm.get("subtree_roots") or []:
        out.append(int(e[0]) if isinstance(e, list) else int(e))
    return out


# ----------------------------------------------------------------------------------------------
# step 2 + 3: one context (runs in a worker)


def check_context(job):
    try:
        return _check_context(job)
    except Exception as e:  # never crash on malformed input: record a failure for this context
        import traceback
        R = Rec()
        R.fail("internal_error", f"ctx {job[0]}: {e!r} {traceback.format_exc(limit=3)[-300:]}")
        return {"k": job[0], **R.dump(), "stats": {"ctx": job[0], "leaves": 0, "deep": False}}


def _check_context(job):
    k, out, prefix, campaign, ctx_line, ctx_sha, src_sha, cache_hit = job
    R = Rec()
    stats = {"ctx": k, "leaves": 0, "nodes": 0, "modules": 0, "blocks": 0, "deep": not cache_hit}
    out, campaign = Path(out), Path(campaign)
    mpath = out / "ctx" / f"ctx-{k:04d}.json"
    try:
        mraw = open(mpath, "rb").read()
        man = json.loads(mraw)
    except (OSError, ValueError) as e:
        R.fail("ctx_manifest_fields", f"ctx {k}: cannot read {mpath}: {e}")
        return {"k": k, **R.dump(), "stats": stats}
    stats["manifest_sha256"] = sha_bytes(mraw)
    F = "ctx_manifest_fields"
    pr = man.get("params") or {}
    K, J, kw = pr.get("K"), pr.get("J"), pr.get("per_word")
    L, B = pr.get("chunk_leaves"), pr.get("block_leaves")
    R.check(F, man.get("ctx") == k, f"ctx {k}: manifest ctx {man.get('ctx')!r}")
    R.check(F, man.get("prefix") == prefix, f"ctx {k}: manifest prefix {man.get('prefix')!r}")
    R.check(F, pr.get("budget") == BUDGET, f"ctx {k}: params.budget {pr.get('budget')!r} (must be 64)")
    R.check(F, pr.get("catalog_base") == CATALOG_BASE, f"ctx {k}: params.catalog_base {pr.get('catalog_base')!r}")
    okK = is_int(K) and K >= 1 << 17 and K & (K - 1) == 0
    R.check(F, okK, f"ctx {k}: params.K {K!r} is not a power of 2 >= 2^17")
    R.check(F, okK and J == K << M_ROWS.bit_length(), f"ctx {k}: params.J {J!r} != K << 12")
    R.check(F, is_int(kw) and kw >= 1, f"ctx {k}: params.per_word {kw!r}")
    R.check(F, is_int(L) and L >= 1 and is_int(B) and B >= 1, f"ctx {k}: chunk/block leaves {L!r}/{B!r}")
    base = base_pairs(ctx_line)
    R.check(F, man.get("base_path") == [list(e) for e in base],
            f"ctx {k}: base_path {man.get('base_path')!r} != {base}")
    for key in ("modules", "skeleton", "stats", "inputs"):
        R.check(F, key in man, f"ctx {k}: manifest has no '{key}'")
    if not (okK and is_int(kw) and kw >= 1 and is_int(L) and is_int(B) and isinstance(man.get("modules"), list)):
        return {"k": k, **R.dump(), "stats": stats}

    # ---- step 2: inputs against the current campaign files
    I = "inputs_rehash"
    inp = resolve_inputs(man.get("inputs") or {})
    rpath = campaign / "runs" / f"ctx-{k}-b64.result.json"
    gpath = campaign / "runs" / f"ctx-{k}-b64.json.gz"
    cur = {}
    for cls, fpath in (("result", rpath), ("gz", gpath)):
        recs = inp.get(cls) or []
        if not R.check(I, len(recs) == 1, f"ctx {k}: {len(recs)} '{cls}' input records"):
            continue
        rec = recs[0]
        try:
            st = os.stat(fpath)
            data = open(fpath, "rb").read()
        except OSError as e:
            R.fail(I, f"ctx {k}: {fpath}: {e}")
            continue
        cur[cls] = data
        R.check(I, os.path.realpath(rec["path"]) == os.path.realpath(fpath)
                or os.path.realpath(campaign / rec["path"]) == os.path.realpath(fpath),
                f"ctx {k}: {cls} path {rec['path']!r} is not {fpath}")
        R.check(I, sha_bytes(data) == rec.get("sha256") and len(data) == rec.get("size"),
                f"ctx {k}: {fpath.name} changed since export (sha256/size)")
        if rec.get("mtime_ns") is not None and rec.get("mtime_ns") != st.st_mtime_ns:
            R.warn.append(f"ctx {k}: {fpath.name} mtime_ns {st.st_mtime_ns} != recorded {rec.get('mtime_ns')}")
    for cls, want in (("contexts", ctx_sha), ("source", src_sha)):
        got = one_sha(inp.get(cls) or [])
        R.check(I, got == want, f"ctx {k}: recorded {cls} sha256 {got} != current {want}")
    stats["run_context_sha256"] = one_sha(inp.get("run_context") or [])
    stats["pbb_sha256"] = one_sha(inp.get("pbb") or [])
    R.check(I, stats["run_context_sha256"] is not None and stats["pbb_sha256"] is not None,
            f"ctx {k}: run_context.py / pbb_strong.py sha256 not recorded")
    tj = one_sha(inp.get("tree_json") or [])
    R.check(I, tj is not None, f"ctx {k}: tree JSON sha256 not recorded")
    stats["exporter"] = json.dumps(exporter_value(man), sort_keys=True)
    stats["params"] = json.dumps({x: pr.get(x) for x in ("budget", "per_word", "chunk_leaves", "block_leaves",
                                                          "catalog_base")}, sort_keys=True)
    W = "witness_absent"
    R.check(W, not (campaign / "runs" / f"ctx-{k}-b64.WITNESS.json").exists(), f"ctx {k}: WITNESS file exists")
    res = None
    if "result" in cur:
        try:
            res = json.loads(cur["result"])
        except ValueError as e:
            R.fail("result_closed", f"ctx {k}: result.json does not parse: {e}")
    if res is not None:
        rp = res.get("replay") or {}
        rc = "result_closed"
        R.check(rc, res.get("status") == "closed", f"ctx {k}: status {res.get('status')!r}")
        R.check(rc, res.get("ctx") == k and res.get("budget") == BUDGET, f"ctx {k}: result ctx/budget")
        R.check(rc, rp.get("ok") is True and rp.get("pending") == DEPTH, f"ctx {k}: replay {rp}")
        R.check(rc, is_int(res.get("leaves")) and rp.get("leaves_checked") == res.get("leaves"),
                f"ctx {k}: replay.leaves_checked {rp.get('leaves_checked')} != leaves {res.get('leaves')}")
        R.check(rc, res.get("pending") == 0, f"ctx {k}: pending {res.get('pending')}")
        R.check(rc, (res.get("rules") or {}).get("catalog_sha256") == src_sha, f"ctx {k}: rules.catalog_sha256")
        R.check(rc, sorted(res.get("missing") or []) == sorted(ctx_line["missing"])
                and sorted(res.get("occupied") or []) == sorted(ctx_line["occupied"]),
                f"ctx {k}: result missing/occupied differ from contexts.jsonl")
        own = man.get("result") if isinstance(man.get("result"), dict) else {}
        for f2 in ("leaves", "nodes"):
            v = own.get(f2, man.get(f"result_{f2}"))
            if v is None:
                R.warn.append(f"ctx {k}: manifest does not record the result's own {f2}")
            else:
                R.check(rc, v == res.get(f2), f"ctx {k}: manifest result {f2} {v} != result.json {res.get(f2)}")

    # module files: sha256 always (cheap), even on a cache hit
    mods = man["modules"]
    for mi, mm in enumerate(mods, start=1):
        name, file = f"{prefix}.C{k:04d}{mi:02d}", f"src/{prefix}/C{k:04d}{mi:02d}.lean"
        R.check("module_names", mm.get("module") == name and mm.get("file") == file,
                f"ctx {k}: module {mi} is {mm.get('module')!r} / {mm.get('file')!r}, expected {name} / {file}")
        try:
            got = sha_file(out / file)
        except OSError as e:
            got = f"unreadable ({e})"
        R.check("module_sha256", got == mm.get("sha256"), f"ctx {k}: {file} sha256 {got} != manifest")
        R.check("module_not_corrupted", mm.get("corrupted") is False, f"ctx {k}: {name} corrupted={mm.get('corrupted')!r}")
    stats["modules"] = len(mods)
    if cache_hit:
        stats["leaves"] = (man.get("stats") or {}).get("leaves") or 0
        return {"k": k, **R.dump(), "stats": stats}

    # ---- step 3: the tree, own parse
    T = "tree_fields"
    if "gz" not in cur:
        return {"k": k, **R.dump(), "stats": stats}
    try:
        raw = gzip.decompress(cur["gz"])
        tree = json.loads(raw)
    except Exception as e:  # truncated gz, CRC error, bad JSON
        R.fail(T, f"ctx {k}: tree does not decompress/parse: {e!r}")
        return {"k": k, **R.dump(), "stats": stats}
    R.check(I, sha_bytes(raw) == tj, f"ctx {k}: tree JSON sha256 differs from the manifest")
    R.check(T, tree.get("context") == k and tree.get("budget") == BUDGET and tree.get("status") == "closed"
            and tree.get("root") == 0, f"ctx {k}: tree context/budget/status/root")
    R.check(T, tree.get("path") == ctx_line["path"] and sorted(tree.get("missing") or []) == sorted(ctx_line["missing"])
            and sorted(tree.get("occupied") or []) == sorted(ctx_line["occupied"]),
            f"ctx {k}: tree path/missing/occupied differ from contexts.jsonl")
    nodes = tree.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        R.fail(T, f"ctx {k}: no nodes")
        return {"k": k, **R.dump(), "stats": stats}
    N = len(nodes)
    # own zero-first preorder: local id = position in the DFS that visits the zero child first
    TT = "tree_is_tree"
    loc, order, stack, bad = [-1] * N, [], [0], False
    while stack:
        i = stack.pop()
        if not (is_int(i) and 0 <= i < N) or loc[i] != -1:
            R.fail(TT, f"ctx {k}: node index {i!r} out of range or reached twice")
            bad = True
            break
        loc[i] = len(order)
        order.append(i)
        nd = nodes[i]
        t = nd.get("type") if isinstance(nd, dict) else None
        if t == "branch":
            stack.append(nd.get("one"))
            stack.append(nd.get("zero"))
        elif t not in ("weighted", "over_budget"):
            R.fail(TT, f"ctx {k}: node {i} has type {t!r}")
            bad = True
            break
    if not bad:
        R.check(TT, len(order) == N, f"ctx {k}: {N - len(order)} nodes unreachable from the root")
    if bad or len(order) != N:
        return {"k": k, **R.dump(), "stats": stats}
    typ = bytearray(N)  # 0 branch, 1 weighted, 2 over
    vtx, zc, oc = [0] * N, [0] * N, [0] * N
    par, dec = [-1] * N, bytearray(N)
    for j, i in enumerate(order):
        nd = nodes[i]
        t = nd["type"]
        if t == "branch":
            v = nd.get("vertex")
            if not (is_int(v) and 0 <= v < N_STATES):
                R.fail(TT, f"ctx {k}: branch vertex {v!r}")
                return {"k": k, **R.dump(), "stats": stats}
            vtx[j], zc[j], oc[j] = v, loc[nd["zero"]], loc[nd["one"]]
            par[zc[j]], dec[zc[j]] = j, 2
            par[oc[j]], dec[oc[j]] = j, 1
        else:
            typ[j] = 1 if t == "weighted" else 2
    cnt, size = [0] * N, [0] * N
    for j in range(N - 1, -1, -1):
        if typ[j] == 0:
            cnt[j], size[j] = cnt[zc[j]] + cnt[oc[j]], 1 + size[zc[j]] + size[oc[j]]
        else:
            cnt[j], size[j] = 1, 1
    R.check(TT, all(typ[j] != 0 or (zc[j] == j + 1 and oc[j] == j + 1 + size[j + 1]) for j in range(N)),
            f"ctx {k}: own preorder self-check failed")
    # masks along full paths (base path included); no state fixed twice
    bmiss = bfix = 0
    for v, x in base:
        bfix |= 1 << v
        if x == 1:
            bmiss |= 1 << v
    miss, fix = [0] * N, [0] * N
    miss[0], fix[0] = bmiss, bfix
    twice = 0
    for j in range(1, N):
        q = par[j]
        v = vtx[q]
        if fix[q] >> v & 1:
            twice += 1
        fix[j] = fix[q] | (1 << v)
        miss[j] = miss[q] | (1 << v) if dec[j] == 1 else miss[q]
    R.check("no_state_fixed_twice", twice == 0, f"ctx {k}: {twice} edges fix an already fixed state")
    nleaves = cnt[0]
    nover = sum(1 for j in range(N) if typ[j] == 2)
    stats["leaves"], stats["nodes"] = nleaves, N
    R.check("over_budget_leaves", all(miss[j].bit_count() > BUDGET for j in range(N) if typ[j] == 2),
            f"ctx {k}: an over_budget leaf has <= 64 missing states")
    TC = "tree_counts"
    if res is not None:
        R.check(TC, nleaves == res.get("leaves") and N == res.get("nodes") and nover == res.get("over_budget"),
                f"ctx {k}: tree leaves/nodes/over {nleaves}/{N}/{nover} != result {res.get('leaves')}/"
                f"{res.get('nodes')}/{res.get('over_budget')}")
    ms = man.get("stats") or {}
    R.check(TC, ms.get("leaves") == nleaves and ms.get("nodes") == N and ms.get("over_budget") == nover,
            f"ctx {k}: manifest stats {ms} != tree {nleaves}/{N}/{nover}")
    R.check(TC, is_int(ms.get("min_margin")) and ms.get("min_margin") >= 1 or (nleaves == nover),
            f"ctx {k}: manifest stats.min_margin {ms.get('min_margin')!r}")

    # ---- SRs, coverage, skeleton, canonical cut
    C = "subtree_roots_cover"
    srs, cover = [], bytearray(N)
    for mi, mm in enumerate(mods, start=1):
        tot = 0
        for e in mm.get("subtree_roots") or []:
            s, c = (e[0], e[1]) if isinstance(e, list) and len(e) == 2 else (e, None)
            if not (is_int(s) and 0 <= s < N):
                R.fail(C, f"ctx {k}: module {mi}: SR {s!r} is not a node")
                continue
            R.check(C, c == cnt[s], f"ctx {k}: SR {s} recorded with {c} leaves, tree has {cnt[s]}")
            srs.append(s)
            tot += cnt[s]
            for x in range(s, s + size[s]):
                cover[x] += 1
        R.check(C, tot == mm.get("leaves"), f"ctx {k}: module {mi} leaves {mm.get('leaves')} != SR sum {tot}")
        R.check(C, bool(mm.get("subtree_roots")), f"ctx {k}: module {mi} has no SR")
    R.check(C, all(cover[j] == 1 for j in range(N) if typ[j] != 0),
            f"ctx {k}: {sum(1 for j in range(N) if typ[j] != 0 and cover[j] != 1)} leaves not covered exactly once")
    R.check(C, sum(mm.get("leaves") or 0 for mm in mods) == nleaves, f"ctx {k}: module leaves do not sum to {nleaves}")
    outside = [j for j in range(N) if cover[j] == 0]
    skel = {}
    for e in man.get("skeleton") or []:
        try:
            skel[int(e["u"])] = (int(e["vertex"]), int(e["zero"]), int(e["one"]))
        except (KeyError, TypeError, ValueError):
            R.fail("skeleton_matches", f"ctx {k}: bad skeleton entry {e!r}")
    R.check("skeleton_matches", set(outside) == set(skel) and len(skel) == len(man.get("skeleton") or []) and all(
        typ[u] == 0 and skel[u] == (vtx[u], zc[u], oc[u]) for u in outside),
        f"ctx {k}: skeleton (nodes outside every SR) differs from the manifest ({len(outside)} vs {len(skel)})")
    R.check("skeleton_matches", all(u < CTX_MUL for u in outside), f"ctx {k}: skeleton id >= {CTX_MUL}")
    # canonical SR cut (top-down, <= L leaves or a leaf) and greedy module packing, preorder: the rule of
    # export_es311.py:206-217 (cut) and :311-318 (packing), re-implemented here, not imported
    want_srs, st = [], [0]
    while st:
        j = st.pop()
        if cnt[j] <= L or typ[j] != 0:
            want_srs.append(j)
        else:
            st += [oc[j], zc[j]]
    packs, curp, curl = [], [], 0
    for s in want_srs:
        if curp and curl + cnt[s] > L:
            packs.append(curp)
            curp, curl = [], 0
        curp.append(s)
        curl += cnt[s]
    packs.append(curp)
    R.check("canonical_cut", [sr_ids(mm) for mm in mods] == packs,
            f"ctx {k}: SRs/modules are not the canonical cut at L={L}")

    # ---- module files
    sp = shapes_es311.side_params({"catalog": CATMOD, "rows": M_ROWS, "states": N_STATES, "budget": BUDGET,
                                   "catalog_base": CATALOG_BASE, "prefix": prefix})
    J_SHIFT = J.bit_length() - 1
    base_tail = [f"({v}, {x})" for v, x in base]
    pcache = {}

    def fullpath(j):
        s = pcache.get(j)
        if s is None:
            parts, x = [], j
            while par[x] != -1:
                parts.append(f"({vtx[par[x]]}, {dec[x]})")
                x = par[x]
            s = pcache[j] = "[" + ", ".join(parts + base_tail) + "]"
        return s

    wcheck = {"bad_weight": 0, "big_weight": 0}
    maxw_tree = [0]

    def leaf_text(j):
        """Expected leaf term, its demand sum, and the normalized entries."""
        nd = nodes[order[j]]
        if typ[j] == 2:
            return ".overBudget", None, None
        cap, wts = nd.get("capacity"), nd.get("weights")
        if not (is_int(cap) and cap >= 0 and isinstance(wts, list)):
            wcheck["bad_weight"] += 1
            return "<bad leaf>", 0, []
        mj, codes, dsum, ents = miss[j], [], 0, []
        for e in wts:
            if not (isinstance(e, list) and len(e) == 2 and is_int(e[0]) and is_int(e[1])
                    and 0 <= e[0] < M_ROWS and e[1] >= 0):
                wcheck["bad_weight"] += 1
                continue
            r, w = e
            if w > maxw_tree[0]:
                maxw_tree[0] = w
            # normalization semantics of export_es311.py:220-221 (re-implemented; masks instead of sets)
            if w and RHS[r] > (SUPP[r] & mj).bit_count():
                if w >= K:
                    wcheck["big_weight"] += 1
                codes.append(r * K + w)
                dsum += w * RHS[r]
                ents.append((r, w))
        words = []  # packing of export_es311.py:238-240 (codes < J, so OR of shifted codes = sum c*J^t)
        for i0 in range(0, len(codes), kw):
            wd = 0
            for t, c in enumerate(codes[i0:i0 + kw]):
                wd |= c << (t * J_SHIFT)
            words.append(wd)
        return f"(.leaf {cap} (natlits% [{', '.join(map(str, words))}]))", dsum, ents

    def expected_block(b):
        parts, st2, maxd = [], [b], 0
        while st2:
            x = st2.pop()
            if isinstance(x, str):
                parts.append(x)
            elif typ[x] == 0:
                parts.append(f"(.split {vtx[x]} ")
                st2 += [")", oc[x], " ", zc[x]]
            else:
                s2, dsum, _ = leaf_text(x)
                parts.append(s2)
                if dsum is not None and dsum > maxd:
                    maxd = dsum
        return "".join(parts), 1 << max(maxd, 1).bit_length()  # block base rule, export_es311.py:370-371

    def diagnose(b, got_term):
        """First difference between the module's term and the tree's subtree at b."""
        got = TOK.findall(got_term)
        want, st2 = [], [b]
        while st2:
            x = st2.pop()
            want.append(x)
            if typ[x] == 0:
                st2 += [oc[x], zc[x]]
        for idx, x in enumerate(want):
            if idx >= len(got):
                return f"term ends early at node {x}"
            gs, gl, gw = got[idx]
            if typ[x] == 0:
                if not gs:
                    return f"node {x}: expected (.split {vtx[x]}, found another term"
                if int(gs) != vtx[x]:
                    return f"node {x}: split vertex {gs}, tree has {vtx[x]}"
            elif typ[x] == 2:
                if gs or gl:
                    return f"node {x}: expected .overBudget"
            else:
                if not gl:
                    return f"node {x}: expected a leaf"
                nd = nodes[order[x]]
                if int(gl) != nd.get("capacity"):
                    return f"node {x}: capacity {gl}, tree has {nd.get('capacity')}"
                if f"(.leaf {gl} (natlits% [{gw}]))" == leaf_text(x)[0]:
                    continue  # this leaf is as expected; report the first one that differs
                ents = []
                for wd in (int(a) for a in gw.split(", ") if a):
                    for _ in range(kw):
                        e, wd = wd % J, wd // J
                        if e:
                            ents.append(divmod(e, K))
                tw = {(r, w) for r, w in nd.get("weights") or []}
                sub = all(e in tw for e in ents)
                _, _, norm = leaf_text(x)
                return (f"node {x}: leaf entries differ from the normalized tree weights "
                        f"(module {len(ents)} entries, normalized {len(norm)}; module entries a subset of the "
                        f"tree leaf's weights: {sub})")
        return "term has extra tokens" if len(got) > len(want) else "terms differ in spacing/format"

    for mi, mm in enumerate(mods, start=1):
        name, file = f"{prefix}.C{k:04d}{mi:02d}", out / f"src/{prefix}/C{k:04d}{mi:02d}.lean"
        try:
            text = open(file, "rb").read().decode("utf-8")
        except (OSError, UnicodeDecodeError) as e:
            R.fail("module_parse", f"ctx {k}: {file}: {e}")
            continue
        errs = shapes_es311.check_text(text, "chunk", name, sp)
        R.check("module_shapes", not errs, f"{name}: {errs[:2]}")
        nleaf = text.count("(.leaf ") + text.count(".overBudget")
        R.check("module_leaf_terms", nleaf == mm.get("leaves"), f"{name}: {nleaf} leaf terms, manifest {mm.get('leaves')}")
        my_srs = [s for s in sr_ids(mm) if is_int(s) and 0 <= s < N]
        lines = text.split("\n")
        blocks, uppers, prints, defined = {}, {}, [], set()
        j = 0
        while j < len(lines):
            ln = lines[j]
            m = RE_DEF.fullmatch(ln)
            if m:
                b = int(m.group(1))
                mc = RE_CHK.fullmatch(lines[j + 1]) if j + 1 < len(lines) else None
                me = RE_EX.fullmatch(lines[j + 2]) if j + 2 < len(lines) else None
                mf = RE_FEAS.fullmatch(lines[j + 3]) if j + 3 < len(lines) else None
                if not (mc and me and mf):
                    R.fail("module_parse", f"{name}: b{b} is not followed by chk/ex/checkF2_feas")
                    j += 1
                    continue
                if b in blocks or f"ex{b}" in defined:
                    R.fail("module_parse", f"{name}: b{b} defined twice")
                blocks[b] = (m.group(2), mc.groups(), me.groups(), mf.groups())
                defined.add(f"ex{b}")
                j += 4
                continue
            m = RE_EX.fullmatch(ln)
            if m:
                u = int(m.group(1))
                ms2 = RE_SPLIT.fullmatch(lines[j + 1]) if j + 1 < len(lines) else None
                if not ms2:
                    R.fail("module_parse", f"{name}: ex{u} is not proved by split_pm")
                    j += 1
                    continue
                if u in uppers or f"ex{u}" in defined:
                    R.fail("module_parse", f"{name}: ex{u} defined twice")
                for rf_ in (ms2.group(8), ms2.group(9)):
                    R.check("defined_before_use", rf_ in defined, f"{name}: ex{u} uses {rf_} before its definition")
                uppers[u] = (m.groups(), ms2.groups())
                defined.add(f"ex{u}")
                j += 2
                continue
            m = RE_PRINT.fullmatch(ln)
            if m:
                prints.append(m.group(1))
            elif ln.startswith("theorem") or ln.startswith("noncomputable") or ln.startswith("  "):
                R.fail("module_parse", f"{name}: unparsed line {ln[:80]!r}")
            j += 1
        stats["blocks"] += len(blocks)
        # tiling: from each SR, combinations (uppers) down to block roots
        reached_b, reached_u = [], []
        for s in my_srs:
            st2 = [s]
            while st2:
                x = st2.pop()
                if x in blocks:
                    reached_b.append(x)
                elif x in uppers and typ[x] == 0:
                    reached_u.append(x)
                    st2 += [oc[x], zc[x]]
                else:
                    R.fail("blocks_tile_subtree_roots", f"{name}: node {x} under SR {s} is neither a block nor a combination")
        R.check("blocks_tile_subtree_roots", sorted(reached_b) == sorted(blocks) and sorted(reached_u) == sorted(uppers),
                f"{name}: blocks/combinations not reached exactly once from the module's SRs")
        # canonical block cut (export_es311.py:367 applies cut() with the block limit inside each SR)
        wb, wu = set(), set()
        for s in my_srs:
            st2 = [s]
            while st2:
                x = st2.pop()
                if cnt[x] <= B or typ[x] != 0:
                    wb.add(x)
                else:
                    wu.add(x)
                    st2 += [oc[x], zc[x]]
        R.check("canonical_blocks", wb == set(blocks) and wu == set(uppers), f"{name}: not the canonical block cut at B={B}")
        R.check("print_axioms", sorted(prints) == sorted(f"ex{s}" for s in my_srs) and len(prints) == len(my_srs),
                f"{name}: #print axioms lines {prints[:5]} != SRs {my_srs[:5]}")
        for b, (term, chk, exs, feas) in blocks.items():
            if not (0 <= b < N):
                R.fail("block_terms", f"{name}: b{b} is not a node")
                continue
            want, wbase = expected_block(b)
            if term != want:
                R.fail("block_terms", f"{name}: b{b}: {diagnose(b, term)}")
            (c_k, c_cat, c_m, c_n, c_bud, c_base, c_K, c_J, c_kw, c_b, c_zn, c_path) = chk
            (e_k, e_fin, e_cat, e_m, e_n, e_bud, e_zn, e_path) = exs
            (f_cat, f_m, f_n, f_bud, f_b0, f_base, f_K, f_J, f_kw, f_wf, f_b, f_c) = feas
            R.check("budget_literal", c_bud == e_bud == f_bud == str(BUDGET),
                    f"{name}: b{b}: budget literals {c_bud}/{e_bud}/{f_bud}")
            R.check("statement_params", (c_cat, c_m, c_n, c_zn) == (CAT, str(M_ROWS), str(N_STATES), str(N_STATES))
                    and (e_cat, e_m, e_n, e_fin, e_zn) == (CAT, str(M_ROWS), str(N_STATES), str(N_STATES), str(N_STATES))
                    and (f_cat, f_m, f_n, f_wf) == (CAT, str(M_ROWS), str(N_STATES), CAT)
                    and c_k == c_b == e_k == f_b == f_c == str(b), f"{name}: b{b}: catalog/rows/states/names")
            R.check("block_params", (c_K, c_J, c_kw) == (str(K), str(J), str(kw)) == (f_K, f_J, f_kw)
                    and c_base == f_base and f_b0 == str(CATALOG_BASE),
                    f"{name}: b{b}: K/J/k/base0 {c_K}/{c_J}/{c_kw}/{f_b0} vs params {K}/{J}/{kw}")
            R.check("block_base", c_base == str(wbase), f"{name}: b{b}: base {c_base}, expected {wbase}")
            fp = fullpath(b)
            R.check("statement_paths", c_path == fp and e_path == fp, f"{name}: b{b}: path {c_path[:60]} != {fp[:60]}")
        for u, (exs, spl) in uppers.items():
            (e_k, e_fin, e_cat, e_m, e_n, e_bud, e_zn, e_path) = exs
            (s_cat, s_m, s_n, s_bud, s_zn, s_path, s_v, s_z, s_o) = spl
            if not (0 <= u < N and typ[u] == 0):
                R.fail("blocks_tile_subtree_roots", f"{name}: combination ex{u} is not a branch node")
                continue
            R.check("budget_literal", e_bud == s_bud == str(BUDGET), f"{name}: ex{u}: budget literals {e_bud}/{s_bud}")
            R.check("statement_params", (e_cat, e_m, e_n, e_fin, e_zn, s_cat, s_m, s_n, s_zn)
                    == (CAT, str(M_ROWS), str(N_STATES), str(N_STATES), str(N_STATES), CAT, str(M_ROWS),
                        str(N_STATES), str(N_STATES)), f"{name}: ex{u}: catalog/rows/states")
            fp = fullpath(u)
            R.check("statement_paths", e_path == fp and s_path == fp, f"{name}: ex{u}: path {e_path[:60]} != {fp[:60]}")
            R.check("split_vertex_children", (s_v, s_z, s_o) == (str(vtx[u]), f"ex{zc[u]}", f"ex{oc[u]}"),
                    f"{name}: ex{u}: split_pm {s_v} {s_z} {s_o}, tree has {vtx[u]} ex{zc[u]} ex{oc[u]}")
    R.check("leaf_weights_valid", wcheck["bad_weight"] == 0, f"ctx {k}: {wcheck['bad_weight']} malformed leaf weights")
    R.check("K_rule", wcheck["big_weight"] == 0 and K <= max(1 << 17, 1 << maxw_tree[0].bit_length()),
            f"ctx {k}: K {K}: {wcheck['big_weight']} kept weights >= K, or K above max(2^17, 2^bitlen(max weight))")
    return {"k": k, **R.dump(), "stats": stats}


# ----------------------------------------------------------------------------------------------
# step 4: Root


def check_root(R, out, prefix, scope, vert, ctxs, mans, root_rec):
    d0, p0 = scope
    rfile = out / f"src/{prefix}/Root.lean"
    RF = "root_file"
    if not R.check(RF, rfile.exists(), f"{rfile} missing"):
        return
    data = open(rfile, "rb").read()
    R.check(RF, root_rec is not None and root_rec.get("sha256") == sha_bytes(data)
            and root_rec.get("file") == f"src/{prefix}/Root.lean" and root_rec.get("module") == f"{prefix}.Root",
            f"merged manifest root record {root_rec!r} does not match {rfile}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        R.fail(RF, "Root is not UTF-8")
        return
    sp = shapes_es311.side_params({"catalog": CATMOD, "rows": M_ROWS, "states": N_STATES, "budget": BUDGET,
                                   "catalog_base": CATALOG_BASE, "prefix": prefix})
    errs = shapes_es311.check_text(text, "root", prefix, sp)
    R.check("root_shape", not errs, f"Root: {errs[:3]}")
    in_scope = [k for k in range(NCTX) if k >> (DEPTH - d0) == p0]
    # expected theorems
    want, ctx_ref, mods_want = {}, {}, []
    for k in in_scope:
        rref, thms, _ = ctx_root_info(R, k, mans[k], prefix, base_pairs(ctxs[k]))
        ctx_ref[k] = rref
        want.update(thms)
        mods_want += [mm.get("module") for mm in mans[k]["modules"]]

    def sref(d, p):
        return f"ex{SKEL_BASE + (1 << d) + p}" if d < DEPTH else ctx_ref[p]

    nskel = 0
    for d in range(d0, DEPTH):
        for p in range(p0 << (d - d0), (p0 + 1) << (d - d0)):
            want[SKEL_BASE + (1 << d) + p] = (pstr(skel_pairs(vert, d, p)), vert[d][p], sref(d + 1, 2 * p),
                                             sref(d + 1, 2 * p + 1))
            nskel += 1
    want_root = (pstr(skel_pairs(vert, d0, p0)), sref(d0, p0))
    # parse
    lines = text.split("\n")
    imports, got, roots, defined, used = [], {}, [], set(), {}
    j = 0
    while j < len(lines):
        ln = lines[j]
        m = RE_IMPORT.fullmatch(ln)
        if m:
            imports.append(m.group(1))
            j += 1
            continue
        m = RE_EX.fullmatch(ln)
        if m:
            ms2 = RE_SPLIT.fullmatch(lines[j + 1]) if j + 1 < len(lines) else None
            if not ms2:
                R.fail("root_theorems", f"Root: ex{m.group(1)} not proved by split_pm")
                j += 1
                continue
            i = int(m.group(1))
            (e_k, e_fin, e_cat, e_m, e_n, e_bud, e_zn, e_path) = m.groups()
            (s_cat, s_m, s_n, s_bud, s_zn, s_path, s_v, s_z, s_o) = ms2.groups()
            R.check("root_budget_literal", e_bud == s_bud == str(BUDGET), f"Root: ex{i}: budget {e_bud}/{s_bud}")
            R.check("root_theorems", (e_cat, e_m, e_n, e_fin, e_zn, s_cat, s_m, s_n, s_zn) == (
                CAT, str(M_ROWS), str(N_STATES), str(N_STATES), str(N_STATES), CAT, str(M_ROWS), str(N_STATES),
                str(N_STATES)), f"Root: ex{i}: catalog/rows/states")
            R.check("root_theorems", e_path == s_path, f"Root: ex{i}: statement and split_pm paths differ")
            R.check("root_theorems", i not in got, f"Root: ex{i} defined twice")
            got[i] = (e_path, s_v, s_z, s_o)
            for rf_ in (s_z, s_o):
                used[rf_] = used.get(rf_, 0) + 1
                if not rf_.startswith(prefix + "."):
                    R.check("root_defined_before_use", rf_ in defined, f"Root: ex{i} uses {rf_} before its definition")
            defined.add(f"ex{i}")
            j += 2
            continue
        m = RE_ROOT.fullmatch(ln)
        if m:
            roots.append(m.groups())
            used[m.group(8)] = used.get(m.group(8), 0) + 1
            if not m.group(8).startswith(prefix + "."):
                R.check("root_defined_before_use", m.group(8) in defined, "Root: root uses an undefined ex")
        j += 1
    R.check("root_imports", sorted(imports) == sorted(mods_want) and len(set(imports)) == len(imports),
            f"Root imports {len(imports)} modules ({len(set(imports))} distinct), expected {len(mods_want)}: "
            f"missing {sorted(set(mods_want) - set(imports))[:5]}, extra {sorted(set(imports) - set(mods_want))[:5]}")
    missing = sorted(set(want) - set(got))
    extra = sorted(set(got) - set(want))
    R.check("root_theorems", not missing and not extra,
            f"Root theorems: {len(missing)} missing (e.g. {missing[:4]}), {len(extra)} unexpected (e.g. {extra[:4]})")
    for i in sorted(set(want) & set(got)):
        wp, wv, wz, wo = want[i]
        gp, gv, gz, go = got[i]
        R.check("root_paths", gp == wp, f"Root: ex{i}: path {gp[:70]} != {wp[:70]}")
        R.check("root_vertices", gv == str(wv), f"Root: ex{i}: vertex {gv} != {wv}")
        R.check("root_references", (gz, go) == (wz, wo), f"Root: ex{i}: children {gz} {go} != {wz} {wo}")
    wanted_refs = {}
    for _, _, wz, wo in want.values():
        for r_ in (wz, wo):
            wanted_refs[r_] = wanted_refs.get(r_, 0) + 1
    wanted_refs[want_root[1]] = wanted_refs.get(want_root[1], 0) + 1
    R.check("root_references", all(v == 1 for v in wanted_refs.values()),
            "internal: an expected reference is wanted twice")
    dup = sorted(r_ for r_, c in used.items() if c != 1)
    R.check("root_references", not dup, f"Root: references used more than once: {dup[:6]}")
    R.check("root_references", set(used) == set(wanted_refs),
            f"Root: references differ: missing {sorted(set(wanted_refs) - set(used))[:4]}, "
            f"extra {sorted(set(used) - set(wanted_refs))[:4]}")
    for k in in_scope:
        R.check("root_context_refs", used.get(ctx_ref[k]) == 1, f"Root: context {k} root {ctx_ref[k]} used {used.get(ctx_ref[k], 0)} times")
    if R.check("root_statement", len(roots) == 1, f"Root has {len(roots)} 'theorem root' lines"):
        (r_fin, r_cat, r_m, r_n, r_bud, r_zn, r_path, r_ref) = roots[0]
        R.check("root_statement", (r_fin, r_cat, r_m, r_n, r_bud, r_zn) == (
            str(N_STATES), CAT, str(M_ROWS), str(N_STATES), str(BUDGET), str(N_STATES)),
            f"Root: theorem root has catalog/budget {r_cat} {r_m} {r_n} {r_bud} (budget must be 64)")
        R.check("root_statement", r_path == want_root[0] and r_ref == want_root[1],
                f"Root: theorem root at {r_path[:60]} := {r_ref}, expected {want_root[0][:60]} := {want_root[1]}")
    R.check("root_statement", "#print axioms root" in lines, "Root has no '#print axioms root'")
    return {"skeleton_theorems": nskel, "context_internal_theorems": len(want) - nskel, "imports": len(imports)}


# ----------------------------------------------------------------------------------------------
# merged manifest (311 schema)


def check_merged(R, out, prefix, mode, scope, mans, in_scope, vert):
    mf = out / f"manifest-{prefix}.json"
    M = "merged_manifest"
    if not mf.exists():
        R.check(M, mode == "partial", f"{mf} missing")
        if mode == "partial":
            R.warn.append(f"{mf.name} not present (partial mode: not checked)")
        return None
    man = json.loads(open(mf, "rb").read())
    for key in ("side", "prefix", "catalog", "rows", "states", "budget", "catalog_base", "complete", "total_leaves",
                "export_root", "base_path", "root", "modules"):
        R.check(M, key in man, f"{mf.name}: no '{key}'")
    R.check(M, man.get("prefix") == prefix and man.get("catalog") == CATMOD and man.get("rows") == M_ROWS
            and man.get("states") == N_STATES and man.get("budget") == BUDGET and man.get("catalog_base") == CATALOG_BASE,
            f"{mf.name}: prefix/catalog/rows/states/budget/catalog_base "
            f"{[man.get(x) for x in ('prefix', 'catalog', 'rows', 'states', 'budget', 'catalog_base')]}")
    if man.get("side") != "balanced":
        R.warn.append(f"{mf.name}: side {man.get('side')!r}")
    by_name = {}
    for k in mans:
        for mm in mans[k]["modules"]:
            by_name[mm.get("module")] = (k, {x: mm.get(x) for x in ("module", "file", "sha256", "leaves",
                                                                    "subtree_roots", "corrupted")})
    got = {}
    for mm in man.get("modules") or []:
        nm = mm.get("module")
        R.check(M, nm not in got, f"{mf.name}: module {nm} listed twice")
        got[nm] = {x: mm.get(x) for x in ("module", "file", "sha256", "leaves", "subtree_roots", "corrupted")}
        R.check(M, nm in by_name and by_name[nm][1] == got[nm],
                f"{mf.name}: module {nm} differs from (or is absent in) its context manifest")
    R.check(M, man.get("total_leaves") == sum((m_.get("leaves") or 0) for m_ in got.values()),
            f"{mf.name}: total_leaves {man.get('total_leaves')} != sum of its modules")
    # merge_es310.py records the sha256 of every context manifest it merged: a context re-exported after
    # the merge would leave the merged manifest (and Root) built from other manifests
    if isinstance(man.get("ctx_manifests"), list):
        rec = {e.get("ctx"): e.get("sha256") for e in man["ctx_manifests"] if isinstance(e, dict)}
        if mode == "partial":
            R.check(M, set(rec) <= set(mans), f"{mf.name}: ctx_manifests lists contexts without a checked manifest: "
                    f"{sorted(set(rec) - set(mans))[:5]}")
        else:
            R.check(M, sorted(rec) == sorted(in_scope), f"{mf.name}: ctx_manifests lists {len(rec)} contexts, "
                    f"scope has {len(in_scope)}")
        stale = [k for k in rec if k in mans and (out / "ctx" / f"ctx-{k:04d}.json").exists()
                 and rec[k] != sha_file(out / "ctx" / f"ctx-{k:04d}.json")]
        R.check(M, not stale, f"{mf.name}: {len(stale)} context manifests changed since the merge, e.g. {stale[:5]}")
    else:
        R.warn.append(f"{mf.name}: no ctx_manifests record (context manifests merged are not pinned)")
    if mode == "partial":
        extra = sorted(set(by_name) - set(got))
        if extra:
            R.warn.append(f"{len(extra)} exported modules are not (yet) in {mf.name}, e.g. {extra[:3]}")
        return man
    want_names = {mm.get("module") for k in in_scope for mm in mans[k]["modules"]}
    R.check(M, set(got) == want_names, f"{mf.name}: modules differ from the contexts in scope "
            f"({len(set(got) - want_names)} extra, {len(want_names - set(got))} missing)")
    R.check(M, man.get("complete") is True and man.get("root") is not None, f"{mf.name}: complete/root not set")
    want_base = [list(e) for e in skel_pairs(vert, *scope)]
    R.check(M, man.get("base_path") == want_base, f"{mf.name}: base_path {man.get('base_path')!r} != {want_base}")
    if mode == "complete":
        R.check(M, man.get("export_root") == 0 and man.get("base_path") == [], f"{mf.name}: export_root/base_path")
    return man


def check_tree63(R, shape_file, ctxs):
    d = json.loads(gzip.decompress(open(shape_file, "rb").read()))
    ty, vx, z, o = d["type"], d["vertex"], d["zero"], d["one"]
    root = d["header"]["root"]
    seen = set()
    for k in range(NCTX):
        c, j = ctxs[k], root
        for v, b in c["path"]:
            if not (ty[j] == 0 and vx[j] == v):
                R.fail("tree63_shape", f"ctx {k}: tree-63 node {j} is not a branch on {v}")
                break
            j = z[j] if b == 0 else o[j]
        else:
            R.check("tree63_shape", j not in seen and j == c.get("preorder"),
                    f"ctx {k}: walks to node {j}, recorded preorder {c.get('preorder')}")
            seen.add(j)
    R.check("tree63_shape", len(seen) == NCTX, f"{len(seen)} distinct depth-12 nodes")
    R.check("tree63_shape", d["header"].get("source_sha256") == BAL_SHA, "tree-63 source sha256")


# ----------------------------------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", type=Path)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--partial", action="store_true")
    g.add_argument("--complete", action="store_true")
    g.add_argument("--subtree", help="D:P, a sub-Root at the depth-D node with prefix P")
    ap.add_argument("--campaign", type=Path, default=CAMPAIGN)
    ap.add_argument("--source", type=Path, default=SRC)
    ap.add_argument("--pbb", type=Path, default=PBB)
    ap.add_argument("--prefix", default="E310B")
    ap.add_argument("--ctx", help="partial mode: only these contexts (comma-separated)")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--cache", type=Path, help="partial mode: verdict cache file")
    ap.add_argument("--tree63-shape", type=Path)
    ap.add_argument("--exporter-sha256", help="pin: the export_es310.py sha256 every context manifest must record")
    ap.add_argument("--report", type=Path, help="also write the JSON result here")
    args = ap.parse_args()
    t0 = time.time()
    out = args.out.resolve()
    camp = args.campaign.resolve()
    if not out.is_dir():
        print(json.dumps({"PASS": False, "error": f"{out} is not a directory"}))
        sys.exit(2)
    if args.exporter_sha256 is not None and not re.fullmatch(r"[0-9a-f]{64}", args.exporter_sha256):
        print(json.dumps({"PASS": False, "error": f"--exporter-sha256 {args.exporter_sha256!r} is not 64 hex digits"}))
        sys.exit(2)
    lockp = out / ".export.lock"
    if lockp.is_file():  # a shared lock: exporter and merge take it exclusively (export_es310.py, merge_es310.py)
        lockf = open(lockp, "rb")
        try:
            fcntl.flock(lockf, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except BlockingIOError:
            print(json.dumps({"PASS": False, "error": f"{lockp} is held (an export or merge runs); retry later"}))
            sys.exit(4)
    if str(out).startswith(str(camp) + os.sep) or out == camp:
        print(json.dumps({"PASS": False, "error": "OUT is inside the campaign directory"}))
        sys.exit(2)
    if args.cache and not args.partial:
        print(json.dumps({"PASS": False, "error": "--cache is allowed with --partial only"}))
        sys.exit(2)
    mode = "partial" if args.partial else "complete" if args.complete else "subtree"
    scope = (0, 0)
    if args.subtree:
        try:
            d0, p0 = (int(x) for x in args.subtree.split(":"))
            assert 0 <= d0 <= DEPTH and 0 <= p0 < (1 << d0)
        except (ValueError, AssertionError):
            print(json.dumps({"PASS": False, "error": f"bad --subtree {args.subtree!r}"}))
            sys.exit(2)
        scope = (d0, p0)
    R = Rec()
    res = {"out": str(out), "mode": mode, "prefix": args.prefix, "campaign": str(camp),
           "scope": list(scope) if mode != "partial" else None}
    # step 1
    ctxs, vert, ctx_sha = load_contexts(R, camp / "contexts.jsonl")
    if R.checks["contexts_jsonl"][0]:   # nothing else can be checked against a broken contexts.jsonl
        res["checks"] = {n: ({"ok": True} if c[0] == 0 else {"ok": False, "failures": c[0], "first": c[1]})
                         for n, c in sorted(R.checks.items())}
        res["PASS"] = False
        res["contexts_checked"], res["leaves"], res["seconds"] = 0, 0, round(time.time() - t0, 1)
        print(json.dumps(res, indent=1))
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(res, indent=1) + "\n")
        sys.exit(1)
    src_sha, _, _ = load_rows(args.source)
    R.check("source", src_sha == BAL_SHA, f"source sha256 {src_sha} != {BAL_SHA}")
    R.check("witness_absent", not (camp / "campaign" / "WITNESS-ALERT.txt").exists(), "campaign/WITNESS-ALERT.txt exists")
    # which contexts
    present = sorted(int(p.name[4:8]) for p in (out / "ctx").glob("ctx-*.json")
                     if re.fullmatch(r"ctx-\d{4}\.json", p.name) and int(p.name[4:8]) < NCTX)
    stray = [p.name for p in (out / "ctx").glob("*") if not re.fullmatch(r"ctx-\d{4}\.json", p.name)] \
        if (out / "ctx").is_dir() else []
    if stray:
        R.warn.append(f"non-manifest files in ctx/: {stray[:5]}")
    if mode == "partial":
        todo = present if not args.ctx else sorted(int(x) for x in args.ctx.split(","))
        R.check("ctx_manifests_present", set(todo) <= set(present), f"requested contexts without a manifest: "
                f"{sorted(set(todo) - set(present))[:10]}")
        todo = [k for k in todo if k in present]
        R.check("ctx_manifests_present", bool(todo), "no context manifest to check")
    else:
        todo = [k for k in range(NCTX) if k >> (DEPTH - scope[0]) == scope[1]]
        miss = sorted(set(todo) - set(present))
        R.check("ctx_manifests_present", not miss, f"{len(miss)} contexts in scope have no manifest, e.g. {miss[:8]}")
        todo = [k for k in todo if k in present]
    # cache (partial only)
    me_sha = sha_file(__file__)
    cache = {}
    if args.cache and args.cache.exists():
        try:
            cache = json.loads(args.cache.read_text())
        except ValueError:
            cache = {}
    if cache.get("checker_sha256") != me_sha or cache.get("contexts_sha256") != ctx_sha:
        cache = {"checker_sha256": me_sha, "contexts_sha256": ctx_sha, "ctx": {}}
    jobs = []
    for k in todo:
        msha = sha_file(out / "ctx" / f"ctx-{k:04d}.json")
        hit = bool(args.cache) and cache["ctx"].get(str(k)) == msha
        jobs.append((k, str(out), args.prefix, str(camp), ctxs[k], ctx_sha, src_sha, hit))
    results = []
    if args.jobs > 1 and len(jobs) > 1:
        with ProcessPoolExecutor(max_workers=args.jobs, initializer=init_worker, initargs=(str(args.source),)) as ex:
            for i, r in enumerate(ex.map(check_context, jobs, chunksize=1)):
                results.append(r)
                if (i + 1) % 200 == 0:
                    print(f"[coverage_es310] {i + 1}/{len(jobs)} contexts, {time.time() - t0:.0f} s", file=sys.stderr)
    else:
        init_worker(str(args.source))
        for i, jb in enumerate(jobs):
            results.append(check_context(jb))
            if (i + 1) % 200 == 0:
                print(f"[coverage_es310] {i + 1}/{len(jobs)} contexts, {time.time() - t0:.0f} s", file=sys.stderr)
    mans, failed_ctx, tot_leaves, deep = {}, [], 0, 0
    rc_shas, pbb_shas, exp_vals, par_vals = set(), set(), set(), set()
    for r in results:
        R.merge(r)
        k = r["k"]
        if any(n for n, _ in r["checks"].values()):
            failed_ctx.append(k)
        st = r["stats"]
        tot_leaves += st.get("leaves", 0)
        deep += 1 if st.get("deep") else 0
        rc_shas.add(st.get("run_context_sha256"))
        pbb_shas.add(st.get("pbb_sha256"))
        exp_vals.add(st.get("exporter"))
        par_vals.add(st.get("params"))
        try:
            mans[k] = json.loads(open(out / "ctx" / f"ctx-{k:04d}.json", "rb").read())
        except (OSError, ValueError):
            pass
        if args.cache and not any(n for n, _ in r["checks"].values()) and st.get("manifest_sha256"):
            cache["ctx"][str(k)] = st["manifest_sha256"]
        elif args.cache:
            cache["ctx"].pop(str(k), None)
    # campaign-wide input hashes: one value across manifests, equal to the current files
    if results:
        cur_rc = sha_file(camp / "run_context.py") if (camp / "run_context.py").is_file() else None
        cur_pbb = sha_file(args.pbb) if args.pbb.is_file() else None
        res["campaign_code"] = {"run_context_recorded": sorted(map(str, rc_shas)), "run_context_current": cur_rc,
                                "pbb_strong_recorded": sorted(map(str, pbb_shas)), "pbb_strong_current": cur_pbb}
        if rc_shas != {cur_rc}:
            R.warn.append(f"campaign code: run_context.py sha256 recorded {sorted(map(str, rc_shas))[:3]}, current "
                          f"{cur_rc} (warning only: it cannot affect soundness)")
        if pbb_shas != {cur_pbb}:
            R.warn.append(f"campaign code: pbb_strong.py sha256 recorded {sorted(map(str, pbb_shas))[:3]}, current "
                          f"{cur_pbb} (warning only: it cannot affect soundness)")
        R.check("ctx_manifest_uniform", len(exp_vals) == 1 and len(par_vals) == 1,
                f"{len(exp_vals)} exporter sha256 values and {len(par_vals)} parameter sets across context manifests")
        ev = next(iter(exp_vals)) if len(exp_vals) == 1 else None
        res["exporter_sha256"] = json.loads(ev) if ev else None
        res["params"] = json.loads(next(iter(par_vals))) if len(par_vals) == 1 else None
        if args.exporter_sha256:  # exact (it was a substring test of the JSON text)
            R.check("exporter_pinned", isinstance(res["exporter_sha256"], dict)
                    and res["exporter_sha256"].get("export_es310") == args.exporter_sha256,
                    f"exporter sha256 {args.exporter_sha256} is not the export_es310 sha256 the manifests record "
                    f"({(res['exporter_sha256'] or {}).get('export_es310') if isinstance(res['exporter_sha256'], dict) else None})")
        for fn in ("export_es310.py", "export_es311.py"):
            if (HERE / fn).exists() and ev and sha_file(HERE / fn) not in ev:
                R.warn.append(f"current {fn} sha256 is not the one recorded in the context manifests")
    if args.cache:
        args.cache.write_text(json.dumps(cache))
    in_scope = todo if mode == "partial" else [k for k in range(NCTX) if k >> (DEPTH - scope[0]) == scope[1]]
    try:
        merged = check_merged(R, out, args.prefix, mode, scope, mans, in_scope, vert)
    except Exception as e:
        R.fail("merged_manifest", f"merged manifest check raised {e!r}")
        merged = None
    if mode != "partial":
        if all(k in mans for k in in_scope) and not R.checks.get("ctx_manifests_present", [0])[0]:
            try:
                res["root"] = check_root(R, out, args.prefix, scope, vert, ctxs, mans,
                                         merged.get("root") if merged else None)
            except Exception as e:
                R.fail("root_file", f"Root check raised {e!r}")
        else:
            R.fail("root_file", "Root not checked: contexts in scope are missing")
    if args.tree63_shape:
        check_tree63(R, args.tree63_shape, ctxs)
    # stray module files
    sdir = out / "src" / args.prefix
    if sdir.is_dir():
        listed = {Path(mm.get("file") or "").name for m_ in mans.values() for mm in m_.get("modules") or []}
        stray_src = sorted(p.name for p in sdir.glob("*.lean") if p.name != "Root.lean" and p.name not in listed)
        if stray_src:
            R.warn.append(f"{len(stray_src)} source files in src/{args.prefix} belong to no checked context manifest, "
                          f"e.g. {stray_src[:3]}")
    res["contexts_checked"] = len(results)
    res["contexts_deep_checked"] = deep
    res["contexts_failed"] = failed_ctx[:50]
    res["leaves"] = tot_leaves
    res["checker_sha256"] = me_sha
    res["contexts_sha256"] = ctx_sha
    res["merged_manifest_sha256"] = (sha_file(out / f"manifest-{args.prefix}.json")
                                     if (out / f"manifest-{args.prefix}.json").exists() else None)
    res["checks"] = {n: ({"ok": True} if c[0] == 0 else {"ok": False, "failures": c[0], "first": c[1]})
                     for n, c in sorted(R.checks.items())}
    res["warnings"] = R.warn[:40]
    res["n_warnings"] = len(R.warn)
    res["seconds"] = round(time.time() - t0, 1)
    res["PASS"] = all(c[0] == 0 for c in R.checks.values()) and bool(results)
    txt = json.dumps(res, indent=1)
    print(txt)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(txt + "\n")
    sys.exit(0 if res["PASS"] else 1)


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()
