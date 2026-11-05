#!/usr/bin/env python3
"""Write an FCat catalog module (CompactChecker/<Name>.lean) from a row source (6 November 2026).

Same output as `export_packed.py --fast --write-catalog` (one flat definition per row and
per trie node, rows carrying `codeL base support`, and the one-time `<name>_wf` theorem by
`decide +kernel`), but it also reads gzip sources and needs no tree. The comment records the
sha256 of the uncompressed source. Used for `Fcat2650.lean` (the 2,650-row residual catalog
of ES(8) <= 313/311):

  python3 make_fcat.py ../omission-residual32-rank-global-2026-10-10/source-2650.json.gz \
      --name fcat2650 --base 131072 --out .
"""
import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_packed import catalog_source, read_rows  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path)
    ap.add_argument("--name", required=True)
    ap.add_argument("--base", type=int, required=True)
    ap.add_argument("--out", type=Path, required=True, help="directory containing CompactChecker/")
    args = ap.parse_args()
    raw = args.source.read_bytes()
    if args.source.suffix == ".gz":
        raw = gzip.decompress(raw)
    source_hash = hashlib.sha256(raw).hexdigest()
    n, rows = read_rows(json.loads(raw))
    path = args.out / "CompactChecker" / f"{args.name[0].upper()}{args.name[1:]}.lean"
    path.write_text(catalog_source(n, rows, args.name, source_hash, args.base))
    print(json.dumps({"catalog": str(path), "source_sha256": source_hash, "states": n,
                      "rows": len(rows), "base": args.base,
                      "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    sys.setrecursionlimit(100000)
    main()
