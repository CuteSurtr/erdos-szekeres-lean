"""Bounded geometry-only profile of a specified existing-pool slice."""
import argparse
import hashlib
import json
from pathlib import Path
from exact_envelope import model, serial

ap = argparse.ArgumentParser()
ap.add_argument("source", type=Path)
ap.add_argument("--first", type=int, required=True, help="one-based inclusive")
ap.add_argument("--last", type=int, required=True, help="one-based inclusive")
ap.add_argument("--out", type=Path, required=True)
args = ap.parse_args()
blob = args.source.read_bytes()
rows = blob.decode().splitlines()
args.out.mkdir(parents=True, exist_ok=True)
for i in range(args.first-1, min(args.last, len(rows))):
    row = json.loads(rows[i])
    p = sorted(row["P"])
    g = model(p)
    mixed = [dict(pair=pair, **s) for pair, s in g["states"].items()
             if s["safe"] and len(s["certificate"]) == 2]
    report = dict(label="COMPUTED", source=str(args.source),
                  source_sha256=hashlib.sha256(blob).hexdigest(), line=i+1,
                  P=p, m=len(p), caps4=len(g["caps4"]),
                  bad_triples=len(g["bad"]), hull=g["hull"],
                  right_breaks=[t for _, t in g["hull"] if t is not None and t>0],
                  two_support_pairs=mixed,
                  limitations="Geometry only; no validity or Delta-existence claim.")
    (args.out/f"line{i+1}.json").write_text(json.dumps(serial(report), indent=2)+"\n")
    print(json.dumps(dict(line=i+1, m=len(p), bad=len(g["bad"]),
                         breaks=len(report["right_breaks"]), two_support=len(mixed))), flush=True)
