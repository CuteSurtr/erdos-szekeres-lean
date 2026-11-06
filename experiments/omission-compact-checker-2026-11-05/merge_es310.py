#!/usr/bin/env python3
"""Merge the per-context manifests of export_es310.py (6 November 2026; route to ES(8) <= 310).
NOTHING HERE PROVES ES(8) <= 310.

  merge_es310.py OUT (--partial | --complete | --subtree D:P) [--prefix E310B] [--no-profile]

Reads OUT/ctx/ctx-*.json (written by export_es310.py) and writes, under flock OUT/.export.lock:
  OUT/src/<Prefix>/Root.lean    only with --complete (all 4,096 contexts) or --subtree D:P (every context
                                under the depth-D skeleton node with prefix P, e.g. 11:1203 = ctx 2406, 2407)
  OUT/manifest-<Prefix>.json    LAST, in the 311 schema that shapes_es311.py (:45-52, :155-167) and
                                drive_es311.py (:276-296, :312-314) read: side, prefix, catalog, rows, states,
                                budget, catalog_base, complete, total_leaves, export_root, base_path, root
                                {module, file, sha256} or null, modules[] {module, file, sha256, leaves,
                                subtree_roots, corrupted} (plus extra keys those readers ignore).
  --partial: complete = false, root = null, export_root = base_path = null, every exported context.
  --subtree D:P: complete = true (so that a driver compiles the sub-Root), export_root = the node's skeleton
                 id 1000000000 + 2^D + P (never 0), base_path = the node's path; only the contexts under it.
  --complete: complete = true, export_root = 0, base_path = [], all 4,096 contexts.

Before writing, for every context in scope: the context manifest's result.json and tree gz are re-hashed
(changed: OUT/ALERT-changed-inputs.txt, exit 2, nothing written), the global inputs re-hashed (contexts.jsonl
and the source: one recorded value, unchanged, else ALERT; run_context.py and pbb_strong.py, campaign code that
cannot affect soundness, may differ between contexts or from the current file: recorded as "code_changed"
warnings only; fixer 6 Nov, soundness review item 7), every module
source re-hashed against its recorded sha256, the parameters checked to be uniform, the base path checked
against contexts.jsonl, and the subtree roots checked to be exactly the children of the context's internal
skeleton that are not skeleton nodes (or the context root alone).

Root.lean (ids as pinned in the es310 interface):
  imports of every module in scope / the fixed open and option lines of shapes_es311.py:84-85 /
  namespace <Prefix> / comments / then
  * context-internal skeleton node u of context k (children before parents):
      theorem ex<(k+1)*100000 + u> : <FFeas at local path(u) ++ base path(k)> :=
        split_pm fcat62 3131 252 64 (zerosF 252) <path> <vertex> <ref zero> <ref one>
  * top skeleton node at depth d (11 down to D) with root-first prefix p (zero child = bit 0 = (v, 2)):
      theorem ex<1000000000 + 2^d + p> : <FFeas at its path> := split_pm ... ex<child 2p> ex<child 2p+1>
    where the depth-12 children are the context roots: <Prefix>.C<kkkk><mm>.ex0, or ex<(k+1)*100000> when
    the context root is an internal skeleton node; vertices and paths come from contexts.jsonl;
  * theorem root : <FFeas at the subtree's path ([] for --complete)> := <ref> / #print axioms root /
    end <Prefix>.
  The text must pass shapes_es311.check_text(kind "root") before it is written. Lean decides correctness:
  split_pm needs both children stated with literal paths (Path.lean:51-56), so a missing or mispathed
  context makes the Root fail to compile. (A path that is a permutation of the right one gives the same
  mask, so literal-path equality is a coverage_es310.py check, not a Lean one; es310-crit1 item 3.)

Exit codes: 0 ok, 1 refused, 2 changed inputs (ALERT), 4 locked. stdout: one JSON summary line.
"""
import argparse
import fcntl
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import export_es310 as E  # noqa: E402
from export_es311 import OPTS, lean_path, sha256_file  # noqa: E402
import shapes_es311  # noqa: E402

TOP_BASE = 1000000000


def top_id(d, p):
    return TOP_BASE + (1 << d) + p


def log(msg):
    print(f"merge_es310: {msg}", file=sys.stderr, flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", type=Path)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--partial", action="store_true")
    g.add_argument("--complete", action="store_true")
    g.add_argument("--subtree", help="D:P, the depth-D skeleton node with root-first prefix P (1 <= D <= 12)")
    ap.add_argument("--prefix", default=E.DEFAULT_PREFIX)
    ap.add_argument("--no-profile", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    summary = {"out": str(args.out), "prefix": args.prefix, "mode": None, "refused": None, "alert": None}
    try:
        code = run(args, summary)
    except E.Refuse as e:
        summary["refused"] = str(e)
        log(f"REFUSED: {e}")
        code = E.EXIT_REFUSE
    summary["exit"] = code
    summary["seconds"] = round(time.time() - t0, 1)
    print(json.dumps(summary), flush=True)
    sys.exit(code)


def run(args, summary):
    out = args.out
    prefix = args.prefix
    if args.complete:
        mode, d0, p0 = "complete", 0, 0
    elif args.partial:
        mode, d0, p0 = "partial", None, None
    else:
        mode = "subtree"
        try:
            d0, p0 = (int(x) for x in args.subtree.split(":"))
        except ValueError:
            raise E.Refuse(f"bad --subtree {args.subtree!r}")
        if not (1 <= d0 <= E.DEPTH and 0 <= p0 < (1 << d0)):
            raise E.Refuse(f"bad --subtree {args.subtree!r} (need 1 <= D <= 12, 0 <= P < 2^D; D = 0 is --complete)")
    summary["mode"] = mode
    ctx_dir = out / "ctx"
    if not ctx_dir.is_dir():
        raise E.Refuse(f"{ctx_dir} does not exist")
    lockf = open(out / ".export.lock", "w")
    try:
        fcntl.flock(lockf, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log(f"another export_es310.py / merge_es310.py holds {out / '.export.lock'}")
        summary["refused"] = "locked"
        return E.EXIT_LOCKED
    if (out / E.ALERT_NAME).exists():
        summary["alert"] = f"{out / E.ALERT_NAME} exists; resolve it by hand first"
        log(summary["alert"])
        return E.EXIT_ALERT
    # Context manifests.
    mans, man_sha = {}, {}
    for f in sorted(ctx_dir.glob("ctx-*.json")):
        raw = f.read_bytes()
        try:
            man = json.loads(raw)
        except ValueError:
            raise E.Refuse(f"{f} does not parse")
        k = man.get("ctx")
        if not (E.is_int(k) and 0 <= k < E.N_CTX) or f.name != f"ctx-{k:04d}.json":
            raise E.Refuse(f"{f}: bad ctx {k!r}")
        if man.get("prefix") != prefix:
            raise E.Refuse(f"{f}: prefix {man.get('prefix')!r}, not {prefix!r}")
        mans[k] = man
        man_sha[k] = E.sha256_bytes(raw)
    if not mans:
        raise E.Refuse(f"no context manifest in {ctx_dir}")
    # Uniform parameters and campaign, over every manifest in OUT.
    pkeys = ("budget", "per_word", "chunk_leaves", "block_leaves", "catalog_base", "catalog", "rows", "states")
    first = mans[min(mans)]
    common = {x: first["params"].get(x) for x in pkeys}
    if (common["budget"], common["catalog_base"], common["catalog"], common["rows"], common["states"]) != \
            (E.BUDGET, E.CATALOG_BASE, E.CATMOD, E.N_ROWS, E.N_STATES):
        raise E.Refuse(f"unexpected parameters {common}")
    campaign = first["campaign"]
    for k, man in mans.items():
        got = {x: man["params"].get(x) for x in pkeys}
        if got != common or man["campaign"] != campaign:
            raise E.Refuse(f"ctx {k}: parameters {got} / campaign {man['campaign']} differ from ctx {min(mans)}'s")
        if man["params"]["J"] != man["params"]["K"] << 12:
            raise E.Refuse(f"ctx {k}: J != K << 12")
    # Scope.
    if mode == "partial":
        scope = sorted(mans)
    else:
        sh = E.DEPTH - d0
        need = list(range(p0 << sh, (p0 + 1) << sh))
        absent = [k for k in need if k not in mans]
        if absent:
            raise E.Refuse(f"{len(absent)} of the {len(need)} contexts under {d0}:{p0} are not exported "
                           f"(first: {absent[:10]})")
        scope = need
    # Global inputs: contexts.jsonl (validated whole), source, run_context.py, pbb_strong.py.
    campaign_p = Path(campaign)
    ctx_sha, ctxs, pv = E.load_contexts(campaign_p / "contexts.jsonl")
    gnow, code_changed = {}, []
    for key in E.GLOBAL_KEYS:
        vals = {(mans[k]["inputs"][key]["path"], mans[k]["inputs"][key]["sha256"]) for k in scope}
        if key in E.CODE_KEYS:  # campaign code: warnings only
            paths = sorted({str(p) for p, _ in vals})
            if len(paths) != 1:
                raise E.Refuse(f"the contexts in scope record {len(paths)} different {key} paths: {paths[:3]}")
            path = paths[0]
            now = sha256_file(path) if path and Path(path).is_file() else None
            shas = sorted({str(s) for _, s in vals})
            if shas != [now]:
                code_changed.append(f"{key}: recorded {shas}, current {now}")
                log(f"warning: {key}: the contexts in scope record {shas}, the current file has {now} "
                    "(recorded only; campaign code cannot affect soundness)")
            gnow[key] = {"path": path, "sha256": shas[0] if len(shas) == 1 else shas, "now": now}
            continue
        if len(vals) != 1:
            raise E.Refuse(f"the contexts in scope record {len(vals)} different {key} inputs")
        (path, sha), = vals
        if key == "source":
            now = E.read_source(path)[0]
        else:
            now = sha256_file(path) if path and Path(path).is_file() else None
        gnow[key] = {"path": path, "sha256": sha, "now": now}
    alerts = [f"{key} changed: {v['sha256']} -> {v['now']}" for key, v in gnow.items()
              if key in E.DATA_KEYS and v["now"] != v["sha256"]]
    summary["code_changed"] = code_changed
    if gnow["contexts_jsonl"]["sha256"] != ctx_sha:
        alerts.append("contexts.jsonl changed while it was read")
    if gnow["source"]["sha256"] != E.SOURCE_SHA:
        raise E.Refuse(f"source sha256 {gnow['source']['sha256']} != {E.SOURCE_SHA}")
    wit = E.witness_files(campaign_p)
    if wit:
        raise E.Refuse(f"WITNESS files present: {wit}")
    # Per context: inputs re-hashed, module sources re-hashed, structure checked.
    sr_home = {}        # (k, s) -> module name
    skel_of = {}        # k -> {u: (vertex, zero, one)}
    modules_out = []
    total = 0
    exporters = set()
    corrupted = []
    for k in scope:
        man = mans[k]
        for which in ("result", "tree_gz"):
            rec = man["inputs"][which]
            p = Path(rec["path"])
            if not p.exists():
                alerts.append(f"ctx {k}: {which} {p} is gone")
                continue
            if p.stat().st_size != rec["size"] or sha256_file(p) != rec["sha256"]:
                alerts.append(f"ctx {k}: {which} {p} changed (recorded sha256 {rec['sha256']})")
        if alerts:
            continue
        if [list(x) for x in man["base_path"]] != [list(x) for x in E.base_path_of(ctxs[k])] \
                or man["ctx_path"] != ctxs[k]["path"]:
            raise E.Refuse(f"ctx {k}: base path differs from contexts.jsonl")
        exporters.add(tuple(sorted(man["exporter_sha256"].items())))
        if man["result"]["leaves"] != man["stats"]["leaves"]:
            raise E.Refuse(f"ctx {k}: result leaves {man['result']['leaves']} != exported {man['stats']['leaves']}")
        mods = man["modules"]
        if not mods:
            raise E.Refuse(f"ctx {k}: no modules")
        srs = set()
        for i, mm in enumerate(mods, 1):
            stem = f"C{k:04d}{i:02d}"
            if mm["module"] != f"{prefix}.{stem}" or mm["file"] != f"src/{prefix}/{stem}.lean":
                raise E.Refuse(f"ctx {k}: module {i} is named {mm['module']} / {mm['file']}")
            f = out / mm["file"]
            if not f.is_file() or sha256_file(f) != mm["sha256"]:
                raise E.Refuse(f"ctx {k}: {mm['file']} is missing or differs from its recorded sha256")
            if sum(c for _, c in mm["subtree_roots"]) != mm["leaves"]:
                raise E.Refuse(f"ctx {k}: {mm['module']}: subtree-root leaves do not add up")
            for s, _ in mm["subtree_roots"]:
                if s in srs:
                    raise E.Refuse(f"ctx {k}: subtree root {s} listed twice")
                srs.add(s)
                sr_home[(k, s)] = mm["module"]
            if mm.get("corrupted"):
                corrupted.append(mm["module"])
            modules_out.append({"module": mm["module"], "file": mm["file"], "sha256": mm["sha256"],
                                "leaves": mm["leaves"], "subtree_roots": mm["subtree_roots"],
                                "corrupted": bool(mm.get("corrupted")), "ctx": k, "K": man["params"]["K"],
                                "J": man["params"]["J"], "blocks": mm.get("blocks"), "entries": mm.get("entries"),
                                "words": mm.get("words"), "min_margin": mm.get("min_margin"),
                                "max_base": mm.get("max_base"), "source_bytes": mm.get("source_bytes")})
        leaves = sum(mm["leaves"] for mm in mods)
        if leaves != man["stats"]["leaves"]:
            raise E.Refuse(f"ctx {k}: module leaves {leaves} != {man['stats']['leaves']}")
        total += leaves
        skel = {}
        for e in man["skeleton"]:
            u = e["u"]
            if not (E.is_int(u) and 0 <= u < E.SKEL_STRIDE) or u in skel:
                raise E.Refuse(f"ctx {k}: bad or repeated skeleton node {u!r}")
            skel[u] = (e["vertex"], e["zero"], e["one"])
        if skel:
            kids = [c for (_, zz, oo) in skel.values() for c in (zz, oo)]
            if 0 not in skel or len(kids) != len(set(kids)) or 0 in kids:
                raise E.Refuse(f"ctx {k}: the skeleton is not a tree rooted at 0")
            if set(skel) - {0} - set(kids):
                raise E.Refuse(f"ctx {k}: skeleton nodes without a skeleton parent")
            if set(c for c in kids if c not in skel) != srs:
                raise E.Refuse(f"ctx {k}: subtree roots are not the non-skeleton children of the skeleton")
        elif srs != {0}:
            raise E.Refuse(f"ctx {k}: no skeleton, but the subtree roots are {sorted(srs)[:5]} (not [0])")
        skel_of[k] = skel
    if alerts:
        text = (f"{time.strftime('%Y-%m-%d %H:%M:%S %Z')} merge_es310.py: inputs of exported contexts changed; "
                f"nothing was written.\n" + "\n".join(alerts) + "\n")
        E.write_atomic(out / E.ALERT_NAME, text.encode())
        summary["alert"] = alerts
        log("ALERT: " + "; ".join(alerts[:5]))
        return E.EXIT_ALERT
    if len(exporters) != 1 and mode != "partial":
        raise E.Refuse(f"{len(exporters)} different exporter sha256 pairs among the contexts in scope")
    if corrupted and mode == "complete":
        raise E.Refuse(f"corrupted test modules in a complete merge: {corrupted[:5]}")
    n = E.N_STATES
    params = f"{E.CAT} {E.N_ROWS} {n} {E.BUDGET}"
    M0 = f"(zerosF {n})"

    def feas(p):
        return f"¬ ∃ holes : Fin {n} → ℕ, FFeas {params} (pmask {M0} {lean_path(p)}) holes"

    def top_path(d, p):
        return [(v, 2 if b == 0 else 1) for v, b in reversed(ctxs[p << (E.DEPTH - d)]["path"][:d])]

    def ctx_root_ref(k):
        if (k, 0) in sr_home:
            return f"{sr_home[(k, 0)]}.ex0"
        return f"ex{(k + 1) * E.SKEL_STRIDE}"

    root_report, export_root, base_path, nskel = None, None, None, 0
    if mode != "partial":
        sp = shapes_es311.side_params({"catalog": E.CATMOD, "rows": E.N_ROWS, "states": n, "budget": E.BUDGET,
                                       "catalog_base": E.CATALOG_BASE, "prefix": prefix})
        rl = [f"import {mm['module']}" for mm in modules_out]
        rl += ["open CompactChecker", "set_option maxRecDepth 100000", *OPTS,
               *([] if args.no_profile else ["set_option profiler true"]),
               f"namespace {prefix}",
               f"-- ES(8) <= 310 compact check (budget-64 campaign), balanced side: root at depth {d0} prefix {p0}, "
               f"{len(scope)} contexts, {total} leaves, {len(modules_out)} modules",
               f"-- contexts.jsonl sha256 {ctx_sha}; source sha256 {gnow['source']['sha256']}"]
        body = []
        # context-internal skeleton nodes, children before parents
        for k in scope:
            skel = skel_of[k]
            if not skel:
                continue
            base = E.base_path_of(ctxs[k])
            paths, order, st = {0: base}, [], [0]
            while st:
                u = st.pop()
                order.append(u)
                v, zz, oo = skel[u]
                for c, x in ((oo, 1), (zz, 2)):
                    paths[c] = [(v, x)] + paths[u]
                    if c in skel:
                        st.append(c)
            if len(order) != len(skel):
                raise E.Refuse(f"ctx {k}: skeleton not connected")

            def ref(c, k=k, skel=skel):
                return f"ex{(k + 1) * E.SKEL_STRIDE + c}" if c in skel else f"{sr_home[(k, c)]}.ex{c}"

            for u in reversed(order):
                v, zz, oo = skel[u]
                body.append(f"theorem ex{(k + 1) * E.SKEL_STRIDE + u} : {feas(paths[u])} :=")
                body.append(f"  split_pm {params} {M0} {lean_path(paths[u])} {v} {ref(zz)} {ref(oo)}")
                nskel += 1
        # top skeleton, depth 11 down to d0
        for d in range(E.DEPTH - 1, d0 - 1, -1):
            sh = d - d0
            for p in range(p0 << sh, (p0 + 1) << sh):
                v = pv[(d, p)]
                kids = []
                for q in (2 * p, 2 * p + 1):
                    kids.append(ctx_root_ref(q) if d + 1 == E.DEPTH else f"ex{top_id(d + 1, q)}")
                P = top_path(d, p)
                body.append(f"theorem ex{top_id(d, p)} : {feas(P)} :=")
                body.append(f"  split_pm {params} {M0} {lean_path(P)} {v} {kids[0]} {kids[1]}")
                nskel += 1
        base_path = top_path(d0, p0) if d0 < E.DEPTH else E.base_path_of(ctxs[p0])
        root_ref = f"ex{top_id(d0, p0)}" if d0 < E.DEPTH else ctx_root_ref(p0)
        body.append(f"theorem root : {feas(base_path)} := {root_ref}")
        body += ["#print axioms root", f"end {prefix}"]
        text = "\n".join(rl + body) + "\n"
        errs = shapes_es311.check_text(text, "root", prefix, sp)
        if errs:
            raise E.Refuse(f"the Root fails the line-shape check: {errs}")
        src_dir = out / "src" / prefix
        src_dir.mkdir(parents=True, exist_ok=True)
        rpath = src_dir / "Root.lean"
        data = text.encode("utf-8")
        E.write_atomic(rpath, data)
        root_report = {"module": f"{prefix}.Root", "file": f"src/{prefix}/Root.lean",
                       "sha256": E.sha256_bytes(data), "skeleton_nodes": nskel}
        export_root = 0 if mode == "complete" else top_id(d0, p0)
        base_path = [list(x) for x in base_path]
        if mode == "complete" and base_path != []:
            raise E.Refuse("complete root path is not []")
    manifest = {
        "side": "balanced", "prefix": prefix, "catalog": E.CATMOD, "rows": E.N_ROWS, "states": n,
        "budget": E.BUDGET, "catalog_base": E.CATALOG_BASE, "complete": mode != "partial",
        "total_leaves": total, "export_root": export_root, "base_path": base_path,
        "root": root_report, "modules": modules_out,
        "mode": mode, "subtree": None if mode == "partial" else f"{d0}:{p0}",
        "contexts": scope, "contexts_in_out": len(mans),
        "ctx_manifests": [{"ctx": k, "file": f"ctx/ctx-{k:04d}.json", "sha256": man_sha[k]} for k in scope],
        "per_word": common["per_word"], "chunk_leaves": common["chunk_leaves"],
        "block_leaves": common["block_leaves"], "campaign": campaign,
        "inputs": {key: {"path": v["path"], "sha256": v["sha256"]} for key, v in gnow.items()},
        "exporter_sha256": [dict(x) for x in sorted(exporters)],
        "merger_sha256": sha256_file(Path(__file__).resolve()),
        "subtree_roots": len(sr_home), "skeleton_theorems": nskel, "corrupted_modules": corrupted,
        "code_changed": code_changed,
    }
    E.write_atomic(out / f"manifest-{prefix}.json", (json.dumps(manifest, indent=1) + "\n").encode())
    summary.update({"contexts": len(scope), "modules": len(modules_out), "total_leaves": total,
                    "skeleton_theorems": nskel, "root": root_report, "export_root": export_root,
                    "manifest": str(out / f"manifest-{prefix}.json")})
    return E.EXIT_OK


if __name__ == "__main__":
    main()
