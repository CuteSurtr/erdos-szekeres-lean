#!/usr/bin/env python3
"""contexts.jsonl for the Lean check of the ES(8) <= 304 tree (FV304, 20 November 2026).

  mk_ctx_es304z.py FILES_DIR OUT/contexts.jsonl

FILES_DIR holds ctx-<k>-zb67.json.gz, k = 0..8191 (bal186-20261119/zrow/b67/files). Each file is one context of
the budget-67 Z-row tree: 13 decisions [v, b] read from the root (b = 0 occupied, b = 1 missing). The file number
k is not the path bits, so each context is renumbered: ctx = the 13 bits b read from the root. One line per
context, sorted by ctx: ctx, path, missing, occupied, depth 13, file, file_k, gz_sha256, json_sha256, nodes.
The result is validated by export_es310.load_contexts with DEPTH 13 and N_CTX 8192 (ctx 0..8191 once each, path
bits = ctx, missing/occupied = the path literals, one branching vertex per prefix: a complete depth-13 tree).
"""
import gzip
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import export_es310 as E  # noqa: E402

E.DEPTH, E.N_CTX = 13, 8192


def main():
    files, out = Path(sys.argv[1]), Path(sys.argv[2])
    lines = {}
    for k in range(E.N_CTX):
        f = files / f"ctx-{k}-zb67.json.gz"
        gz = f.read_bytes()
        raw = gzip.decompress(gz)
        cut = raw.index(b',"nodes":')                 # header keys come before the (large) node list
        d = json.loads(raw[:cut] + b"}")              # parse the header only (an OOM kill at 1 GB, 20 Nov 18:21)
        p = d["path"]
        assert d["budget"] == 67 and d["status"] == "closed" and d["context"] == k, (k, d["budget"], d["status"])
        assert len(p) == E.DEPTH and all(b in (0, 1) for _, b in p), k
        ctx = sum(b << (E.DEPTH - 1 - i) for i, (_, b) in enumerate(p))
        assert ctx not in lines, (k, ctx)
        lines[ctx] = {"ctx": ctx, "path": p, "missing": d["missing"], "occupied": d["occupied"], "depth": E.DEPTH,
                      "file": f.name, "file_k": k, "gz_sha256": hashlib.sha256(gz).hexdigest(),
                      "json_sha256": hashlib.sha256(raw).hexdigest(), "nodes": raw.count(b'"type":')}
    assert sorted(lines) == list(range(E.N_CTX))
    tmp = out.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(lines[c], separators=(",", ":")) + "\n" for c in range(E.N_CTX)))
    tmp.replace(out)
    sha, ctxs, pv = E.load_contexts(out)
    print(json.dumps({"contexts": len(ctxs), "sha256": sha, "prefix_vertices": len(pv),
                      "nodes": sum(lines[c]["nodes"] for c in lines)}))


if __name__ == "__main__":
    main()
