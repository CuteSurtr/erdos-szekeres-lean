#!/usr/bin/env python3
"""TEST FIXTURES ONLY for test_coverage_es310.sh (6 November 2026). Nothing written here is ever compiled
or used as evidence; ES(8) <= 310 is NOT proved.

  make_cov_fixture_es310.py fake-campaign DIR --from C [--real 2406,2407]
      A fake campaign directory with all 4,096 contexts closed: contexts.jsonl and run_context.py copied
      from C (read only), runs/ctx-<k>-b64.{json.gz,result.json} synthesized (small trees of 1-3 leaves
      in the campaign's allocation order, so they need renumbering; leaf weights are arbitrary, NOT valid
      certificates), except the --real contexts, whose two files are copied from C byte for byte.
  make_cov_fixture_es310.py export OUT --campaign DIR --prefix E310BK [--chunk-leaves 2] [--block-leaves 1]
                                   [--per-word 3]
      Writes OUT/src/<Prefix>/C<kkkk><mm>.lean and OUT/ctx/ctx-<kkkk>.json for every context of DIR in the
      context-manifest format of export_es310.py (so that merge_es310.py accepts them), WITHOUT the leaf
      replays (the synthetic leaves would fail them). Module lines as export_es311.py:353-431 /
      export_es310.py:466-552 write them; renumbering by export_es310.renumber, cutting and paths by
      export_es311.py (shape_info :167-193, path_of :196-203, cut :206-217, normalize :220-221,
      pack_words :238-240, lean_path :266-267). The fixture is a stand-in for export_es310.py where the
      real exporter refuses synthetic leaves; coverage_es310.py itself imports none of this.
Both refuse to write anywhere but under D/build/es310/test-*.
"""
import argparse
import gzip
import hashlib
import json
import os
import random
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import export_es310 as E  # noqa: E402  (fixture only)
from export_es311 import OPTS, cut, lean_path, normalize, pack_words, path_of, read_source, shape_info  # noqa: E402

TEST_ROOT = HERE / "build" / "es310"
SRC = HERE.parent / "omission-cover-certificates-2026-10-10" / "balanced-v2-source.json"
PBB = HERE.parent / "omission-final311-2026-10-14" / "search" / "pbb_strong.py"


def guard(p):
    rp = Path(os.path.realpath(p))
    if not (rp.parent == Path(os.path.realpath(TEST_ROOT)) and rp.name.startswith("test-")) and not any(
            q.parent == Path(os.path.realpath(TEST_ROOT)) and q.name.startswith("test-") for q in rp.parents):
        sys.exit(f"refusing to write outside {TEST_ROOT}/test-*: {rp}")
    return rp


def sha(b):
    return hashlib.sha256(b).hexdigest()


def fake_campaign(args):
    out = guard(args.dir)
    src = Path(os.path.realpath(args.src_campaign))
    if out == src or src in out.parents:
        sys.exit("refusing: DIR inside the campaign")
    (out / "runs").mkdir(parents=True, exist_ok=True)
    (out / "campaign").mkdir(exist_ok=True)
    for f in ("contexts.jsonl", "run_context.py"):
        (out / f).write_bytes(open(src / f, "rb").read())
    real = {int(x) for x in args.real.split(",")} if args.real else set()
    ctxs = [json.loads(ln) for ln in open(out / "contexts.jsonl", "rb").read().decode().splitlines() if ln]
    _, n, rows = read_source(SRC)
    old = 1_700_000_000  # old mtimes: the real exporter's 120 s age rule never applies to fixtures
    for c in ctxs:
        k = c["ctx"]
        stem = out / "runs" / f"ctx-{k}-b64"
        if k in real:
            for suf in (".json.gz", ".result.json"):
                Path(str(stem) + suf).write_bytes(open(src / "runs" / f"ctx-{k}-b64{suf}", "rb").read())
        else:
            rnd = random.Random(1000 + k)
            on_path = {v for v, _ in c["path"]}
            free = [v for v in range(n) if v not in on_path]
            a, b = rnd.sample(free, 2)

            fixed = on_path | {a, b}
            keep = [r for r in range(len(rows)) if rows[r][1] >= 1 and not fixed.intersection(rows[r][0])]

            def leaf():
                # one entry that normalization always keeps (a real leaf never has an empty word list:
                # its margin would be <= 0; shapes_es311 TERM also needs one numeral), then random ones
                r0 = rnd.choice(keep)
                ws = [[r0, rnd.randint(1, 5000)]]
                for r in sorted(rnd.sample(range(len(rows)), 6)):
                    if r != r0:
                        ws.append([r, rnd.choice([0, rnd.randint(1, 5000)])])
                if k % 97 == 5:
                    ws[0][1] = 200000          # a weight above 2^17: per-context K = 2^18
                return {"type": "weighted", "capacity": rnd.choice([100, 256, 1000]), "weights": ws}

            kind = k % 3
            if kind == 0:
                nodes = [leaf()]
            elif kind == 1:
                nodes = [{"type": "branch", "vertex": a, "zero": 1, "one": 2}, leaf(), leaf()]
            else:  # allocation order as run_context.py:103-107 (one child expanded first)
                nodes = [{"type": "branch", "vertex": a, "zero": 1, "one": 2},
                         {"type": "branch", "vertex": b, "zero": 3, "one": 4}, leaf(), leaf(), leaf()]
            tree = {"context": k, "budget": 64, "missing": c["missing"], "occupied": c["occupied"],
                    "path": c["path"], "status": "closed", "root": 0, "nodes": nodes}
            nl = sum(1 for x in nodes if x["type"] != "branch")
            with gzip.open(str(stem) + ".json.gz", "wt", compresslevel=6) as f:
                json.dump(tree, f, separators=(",", ":"))
            res = {"ctx": k, "budget": 64, "missing": c["missing"], "occupied": c["occupied"],
                   "b63_record_nodes": c["nodes"], "b63_record_leaves": c["leaves"],
                   "rules": {"K_TOP": 40, "D_TOP": 12, "K_LOW": 12, "pbb_strong": str(PBB),
                             "catalog_sha256": E.SOURCE_SHA},
                   "status": "closed", "expanded": len(nodes), "nodes": len(nodes), "leaves": nl, "weighted": nl,
                   "over_budget": 0, "pending": 0,
                   "replay": {"ok": True, "leaves_checked": nl, "pending": 12, "minimum_margin": 1},
                   "tree_file": f"runs/ctx-{k}-b64.json.gz", "FIXTURE": "synthetic, not a certificate"}
            Path(str(stem) + ".result.json").write_text(json.dumps(res, indent=1))
        for suf in (".json.gz", ".result.json"):
            os.utime(str(stem) + suf, (old, old))
    print(json.dumps({"fake_campaign": str(out), "contexts": len(ctxs), "real": sorted(real)}))


def export(args):
    out = guard(args.out)
    camp = Path(os.path.realpath(args.campaign))
    prefix = args.prefix
    source_sha, n, rows = read_source(SRC)
    m = len(rows)
    ctx_sha, ctxs, _ = E.load_contexts(camp / "contexts.jsonl")
    gl = {"contexts_jsonl": {"path": str(camp / "contexts.jsonl"), "sha256": ctx_sha},
          "source": {"path": str(SRC), "sha256": source_sha},
          "run_context": {"path": str(camp / "run_context.py"), "sha256": E.sha256_file(camp / "run_context.py")},
          "pbb_strong": {"path": str(PBB), "sha256": E.sha256_file(PBB)}}
    exsha = {"export_es310": "fixture-" + E.sha256_file(Path(__file__)), "export_es311": "fixture"}
    src_dir, ctx_dir = out / "src" / prefix, out / "ctx"
    src_dir.mkdir(parents=True, exist_ok=True)
    ctx_dir.mkdir(parents=True, exist_ok=True)
    L, B, kw = args.chunk_leaves, args.block_leaves, args.per_word
    params = f"{E.CAT} {m} {n} {E.BUDGET}"
    M0 = f"(zerosF {n})"

    def feas(p):
        return f"¬ ∃ holes : Fin {n} → ℕ, FFeas {params} (pmask {M0} {lean_path(p)}) holes"

    only = {int(x) for x in args.ctx.split(",")} if args.ctx else None
    done = 0
    for k in sorted(ctxs):
        if only is not None and k not in only:
            continue
        rp, gp = camp / "runs" / f"ctx-{k}-b64.result.json", camp / "runs" / f"ctx-{k}-b64.json.gz"
        rraw, graw = open(rp, "rb").read(), open(gp, "rb").read()
        res, js = json.loads(rraw), gzip.decompress(graw)
        tree = json.loads(js)
        nodes = tree["nodes"]
        ty, vx, z, o, order = E.renumber(nodes, k)
        parent, dec, count, size = shape_info(ty, z, o, 0)
        base = E.base_path_of(ctxs[k])
        N = len(ty)

        def full(j):
            return path_of(j, parent, dec, vx, None) + base

        leaf, wmax = {}, 0
        for x in range(N):
            if ty[x] == E.T_BRANCH:
                continue
            missing = {v for v, d in full(x) if d == 1}
            nd = nodes[order[x]]
            ent = normalize(rows, [tuple(e) for e in nd["weights"]], missing)
            D = sum(w * rows[r][1] for r, w in ent)
            wmax = max([wmax] + [w for _, w in ent])
            leaf[x] = (nd["capacity"], ent, D)
        K = 1 << max(17, wmax.bit_length())
        J = K << m.bit_length()
        srs, skeleton = cut(0, L, ty, z, o, count)
        modules, cur, cl = [], [], 0
        for s in srs:
            if cur and cl + count[s] > L:
                modules.append(cur)
                cur, cl = [], 0
            cur.append(s)
            cl += count[s]
        modules.append(cur)
        mods = []
        for i, mod in enumerate(modules, start=1):
            stem = f"C{k:04d}{i:02d}"
            name = f"{prefix}.{stem}"
            lines = [f"import {E.CATMOD}", "import CompactChecker.Path", "open CompactChecker",
                     "set_option maxRecDepth 100000", *OPTS, f"namespace {name}",
                     f"-- TEST FIXTURE (synthetic leaves, not a certificate), context {k}, module {i}"]
            for s in mod:
                blocks, uppers = cut(s, B, ty, z, o, count)
                for b in blocks:
                    lv = [x for x in range(b, b + size[b]) if ty[x] != E.T_BRANCH]
                    base0 = 1 << max([leaf[x][2] for x in lv] + [1]).bit_length()

                    def term(x):
                        if ty[x] == E.T_BRANCH:
                            return f"(.split {vx[x]} {term(z[x])} {term(o[x])})"
                        cap, ent, _ = leaf[x]
                        words = pack_words([r * K + w for r, w in ent], kw, J)
                        return f"(.leaf {cap} (natlits% [{', '.join(map(str, words))}]))"

                    p = full(b)
                    lines.append(f"noncomputable def b{b} : PTree := {term(b)}")
                    lines.append(f"theorem chk{b} : checkF2 {params} {base0} {K} {J} {kw} b{b} "
                                 f"(pmask {M0} {lean_path(p)}) = true := by decide +kernel")
                    lines.append(f"theorem ex{b} : {feas(p)} :=")
                    lines.append(f"  checkF2_feas {params} {E.CATALOG_BASE} {base0} {K} {J} {kw} {E.CAT}_wf b{b} _ chk{b}")
                for u in reversed(uppers):
                    p = full(u)
                    lines.append(f"theorem ex{u} : {feas(p)} :=")
                    lines.append(f"  split_pm {params} {M0} {lean_path(p)} {vx[u]} ex{z[u]} ex{o[u]}")
            for s in mod:
                lines.append(f"#print axioms ex{s}")
            lines.append(f"end {name}")
            data = ("\n".join(lines) + "\n").encode()
            (src_dir / f"{stem}.lean").write_bytes(data)
            mods.append({"module": name, "file": f"src/{prefix}/{stem}.lean", "sha256": sha(data),
                         "leaves": sum(count[s] for s in mod), "subtree_roots": [[s, count[s]] for s in mod],
                         "blocks": None, "entries": None, "words": None, "min_margin": 1, "max_base": None,
                         "corrupted": False})
        man = {"ctx": k, "prefix": prefix, "campaign": str(camp),
               "params": {"budget": E.BUDGET, "K": K, "J": J, "per_word": kw, "chunk_leaves": L,
                          "block_leaves": B, "catalog_base": E.CATALOG_BASE, "catalog": E.CATMOD,
                          "rows": m, "states": n, "profile": False},
               "ctx_path": ctxs[k]["path"], "base_path": [list(d) for d in base],
               "inputs": {"result": {"path": str(rp), "size": len(rraw), "mtime_ns": os.stat(rp).st_mtime_ns,
                                     "sha256": sha(rraw)},
                          "tree_gz": {"path": str(gp), "size": len(graw), "mtime_ns": os.stat(gp).st_mtime_ns,
                                      "sha256": sha(graw)},
                          "tree_json_sha256": sha(js), **gl},
               "exporter_sha256": exsha, "modules": mods,
               "subtree_roots": [[s, count[s]] for s in srs],
               "skeleton": [{"u": u, "vertex": vx[u], "zero": z[u], "one": o[u]} for u in skeleton],
               "stats": {"leaves": count[0], "nodes": N, "weighted": count[0], "over_budget": 0, "min_margin": 1},
               "result": {"leaves": res["leaves"], "nodes": res["nodes"]}, "corruption": None,
               "FIXTURE": "no leaf replays; synthetic leaves are not certificates"}
        (ctx_dir / f"ctx-{k:04d}.json").write_text(json.dumps(man, indent=1) + "\n")
        done += 1
    print(json.dumps({"fixture_export": str(out), "contexts": done, "prefix": prefix}))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("fake-campaign")
    a.add_argument("dir", type=Path)
    a.add_argument("--from", dest="src_campaign", type=Path, required=True)
    a.add_argument("--real", default="")
    b = sub.add_parser("export")
    b.add_argument("out", type=Path)
    b.add_argument("--campaign", type=Path, required=True)
    b.add_argument("--prefix", default="E310BK")
    b.add_argument("--chunk-leaves", type=int, default=2)
    b.add_argument("--block-leaves", type=int, default=1)
    b.add_argument("--per-word", type=int, default=3)
    b.add_argument("--ctx")
    args = ap.parse_args()
    if args.cmd == "fake-campaign":
        fake_campaign(args)
    else:
        export(args)


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()
