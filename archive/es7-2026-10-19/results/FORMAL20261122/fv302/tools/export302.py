#!/usr/bin/env python3
"""Export contexts of the ES(8) <= 302 tree (budget 69, Z-row and Z*-row at 16) as Fast2 chunk modules (FV302, 24 Nov 2026).
(Adapted from export_es304z.py: constants, the catalog FcatZZs16, contexts302.jsonl of mk_ctx302.py, 5-digit manifests.)
NOTHING HERE PROVES ANYTHING: Lean decides every module; this only writes the texts.

  export_es304z.py --contexts C --source SRC --out OUT (--ctx k1,k2,... | --range A:B | --all) [--per-word 16]
                   [--chunk-leaves 12000] [--block-leaves 64] [--corrupt N] [--no-profile]

C   contexts.jsonl of mk_ctx_es304z.py (ctx = path bits; validated here again by export_es310.load_contexts)
SRC fcatz-source.json (balanced-v2-source.json + the Z-row; sha256 pinned below)

Per context, export_es310.export_context runs UNCHANGED (zero-first preorder renumbering, two exact leaf replays:
full-load margin >= 1 and the Python transcription of the Lean leaf test, cut into modules and blocks, the 311
line-shape check), with the constants BUDGET 67, CAT fcatZ (CompactChecker.FcatZ), N_ROWS 3132, DEPTH 13, N_CTX 8192.
The tree file is re-hashed against contexts.jsonl first. The one header comment that names ES(8) <= 310 is replaced
and the shape check is run again on the final text. Writes OUT/src/E304Z/C<kkkk><mm>.lean (tmp + rename), then
OUT/ctx/ctx-<kkkk>.json LAST (its existence means "context k is exported"). A context whose manifest exists with
the same tree hash is skipped. Exit 1 if any context is refused.
"""
import argparse
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path("/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05")  # FV304 tools (unchanged, imported)
sys.path.insert(0, str(HERE))
import shapes_es311  # noqa: E402
import export_es310 as E  # noqa: E402
from export_es311 import read_source  # noqa: E402

shapes_es311.CATALOGS["CompactChecker.FcatZZs16"] = "fcatZZs16"
E.BUDGET = 69
E.CATMOD, E.CAT = "CompactChecker.FcatZZs16", "fcatZZs16"
E.N_ROWS = 3133
E.DEPTH, E.N_CTX = 16, 40000      # not used by export_context; contexts come from contexts302.jsonl
SOURCE_SHA = "6d83b0f1601655b914d6618391e32b75ee5e3ed7b0613c6ea240f034a06d0c0e"
FILES = Path("/home/jay/research/data/bal186-20261119/zrow/b69zs54/files")
PREFIX = "E302ZZ"
OLD = "-- ES(8) <= 310 compact check (budget-64 campaign), balanced side, context"
NEW = "-- ES(8) <= 302 compact check (FV302, budget-69 Z/Z*-row tree), context"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write_atomic(path, data):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)



def load_contexts302(path):
    """sha256 and {ctx: line} of contexts302.jsonl (mk_ctx302.py validated the cover when it wrote the file; here:
    ctx ids 0..N-1 once each, path/missing/occupied consistent, the first decision [0, 0])."""
    raw = Path(path).read_bytes()
    ctxs = {}
    for line in raw.decode("ascii").split("\n"):
        if not line:
            continue
        c = json.loads(line)
        k, p = c["ctx"], c["path"]
        assert isinstance(k, int) and k not in ctxs, k
        assert p[0] == [0, 0] and len({v for v, _ in p}) == len(p), k
        assert sorted(c["missing"]) == sorted(v for v, b in p if b == 1), k
        assert sorted(c["occupied"]) == sorted(v for v, b in p if b == 0), k
        ctxs[k] = c
    assert sorted(ctxs) == list(range(len(ctxs))), "ctx ids are not 0..N-1"
    return sha(raw), ctxs

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--contexts", type=Path, required=True)
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--ctx")
    g.add_argument("--all", action="store_true")
    g.add_argument("--range", help="A:B, contexts A..B-1")
    ap.add_argument("--per-word", type=int, default=16)
    ap.add_argument("--chunk-leaves", type=int, default=12000)
    ap.add_argument("--block-leaves", type=int, default=64)
    ap.add_argument("--corrupt", type=int)
    ap.add_argument("--no-profile", action="store_true")
    args = ap.parse_args()
    csha, ctxs = load_contexts302(args.contexts)
    ssha, n, rows = read_source(args.source)
    assert ssha == SOURCE_SHA and n == E.N_STATES and len(rows) == E.N_ROWS, (ssha, n, len(rows))
    if args.range:
        a, b = map(int, args.range.split(":"))
        sel = list(range(a, b))
    else:
        sel = sorted(ctxs) if args.all else [int(x) for x in args.ctx.split(",")]
    if args.corrupt is not None:
        assert len(sel) == 1, "--corrupt needs exactly one --ctx"
    sp = shapes_es311.side_params({"catalog": E.CATMOD, "rows": E.N_ROWS, "states": n, "budget": E.BUDGET,
                                   "catalog_base": E.CATALOG_BASE, "prefix": PREFIX})
    (args.out / "src" / PREFIX).mkdir(parents=True, exist_ok=True)
    (args.out / "ctx").mkdir(parents=True, exist_ok=True)
    code_caches, refused = {}, []
    for k in sel:
        t0 = time.time()
        c = ctxs[k]
        man = args.out / "ctx" / f"ctx-{k:05d}.json"
        if man.exists() and json.loads(man.read_text()).get("gz_sha256") == c["gz_sha256"]:
            continue
        try:
            gz = (FILES / c["file"]).read_bytes()
            if sha(gz) != c["gz_sha256"]:
                raise E.Refuse(f"ctx {k}: {c['file']} changed since contexts.jsonl")
            raw = gzip.decompress(gz)
            if sha(raw) != c["json_sha256"]:
                raise E.Refuse(f"ctx {k}: json hash differs")
            tree = json.loads(raw)
            del raw
            if tree.get("budget") != E.BUDGET or tree.get("status") != "closed" or tree.get("path") != c["path"] \
                    or tree.get("root") != 0:
                raise E.Refuse(f"ctx {k}: tree header differs from contexts.jsonl")
            hashes = {"gz": c["gz_sha256"], "json": c["json_sha256"], "result": "-", "source": ssha}
            texts, info = E.export_context(k, c, tree, rows, args, PREFIX, code_caches, hashes)
            del tree
            out_texts = []
            for (stem, data), m in zip(texts, info["modules"]):
                text = data.decode("utf-8")
                if text.count(OLD) != 1:
                    raise E.Refuse(f"ctx {k}: header comment not found once in {stem}")
                text = text.replace(OLD, NEW)
                errs = shapes_es311.check_text(text, "chunk", m["module"], sp)
                if errs:
                    raise E.Refuse(f"ctx {k}: {stem} fails the shape check after the comment change: {errs}")
                b = text.encode("utf-8")
                m["sha256"], m["source_bytes"] = sha(b), len(b)
                out_texts.append((stem, b))
            for stem, b in out_texts:
                write_atomic(args.out / "src" / PREFIX / f"{stem}.lean", b)
            info.update({"ctx": k, "file": c["file"], "file_k": c["file_k"], "gz_sha256": c["gz_sha256"],
                         "json_sha256": c["json_sha256"], "contexts_sha256": csha, "source_sha256": ssha,
                         "exporter_sha256": sha(Path(__file__).read_bytes()),
                         "export_es310_sha256": sha((HERE / "export_es310.py").read_bytes()),
                         "params": {"budget": E.BUDGET, "per_word": args.per_word, "chunk_leaves": args.chunk_leaves,
                                    "block_leaves": args.block_leaves, "catalog": E.CATMOD, "rows": E.N_ROWS,
                                    "catalog_base": E.CATALOG_BASE}, "seconds": round(time.time() - t0, 1)})
            write_atomic(man, json.dumps(info, separators=(",", ":")).encode())
            print(json.dumps({"ctx": k, "modules": len(info["modules"]), "leaves": info["stats"]["leaves"],
                              "min_margin": info["stats"]["min_margin"], "seconds": info["seconds"],
                              "corrupted": info["corruption"]}), flush=True)
        except E.Refuse as e:
            refused.append(k)
            print(json.dumps({"ctx": k, "refused": str(e)}), flush=True)
    sys.exit(1 if refused else 0)


if __name__ == "__main__":
    main()
