#!/usr/bin/env python3
"""Pick V3 leaf records (verdict VERIFIED, with cnf_sha256) for the byte check, one per case,
preferring leaves that share literals with their case cube (the deduplication rule) and
leaves whose unsorted literal order differs from sorted-by-abs.
usage: pick_leaves.py RESULTS_DIR N OUT.tsv   (OUT lines: case_index case sha256 lits)"""
import glob, json, os, sys
root, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
cases = [json.loads(l)["case"] for l in open(os.path.join(root, "Mii-S/cases.jsonl"))]
cubes = [l.split()[1:-1] for l in open(os.path.join(root, "Mii-S/cases.icnf")) if l.startswith("a ")]
idx = {c: i for i, c in enumerate(cases)}
cube = {c: set(map(int, cubes[i])) for c, i in idx.items()}
recs = {}
files = sorted(f for d in ["V3Z", "V3A", "V3B", "V3C", "V3D", "V3E"]
               for f in glob.glob(os.path.join(root, d, "**", "*.jsonl"), recursive=True))
for f in files:
    for l in open(f):
        try:
            o = json.loads(l)
        except ValueError:
            continue
        if o.get("kind") == "leaf" and o.get("verdict") == "VERIFIED" and o.get("cnf_sha256"):
            c = o["case"]
            score = (len(set(o["lits"]) & cube[c]) > 0, o["lits"] != sorted(o["lits"], key=abs))
            if c not in recs or score > recs[c][0]:
                recs[c] = (score, o, f)
print("leaf records with sha from", len(files), "files; cases covered:", len(recs), file=sys.stderr)
chosen = sorted(recs.items(), key=lambda kv: (not kv[1][0][0], not kv[1][0][1], idx[kv[0]]))[:n]
with open(out, "w") as w:
    for c, (score, o, f) in chosen:
        w.write(f"{idx[c]}\t{c}\t{o['cnf_sha256']}\t{','.join(map(str, o['lits']))}\t{os.path.relpath(f, root)}\n")
print("chosen", len(chosen), "with cube overlap:", sum(1 for _, (s, _, _) in chosen if s[0]), file=sys.stderr)
