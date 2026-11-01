#!/usr/bin/env python3
"""A6 audit: recount the threefold spot-check (results/C3SPOT) from its raw files.
- units6.tsv: rows, per-source counts, sigma-cube ('__') nodes; each row's expected CNF hash against the certified
  record of that node in the named record file;
- out.jsonl: rows, verdicts, CNF hash equal to the units6 expectation, base hash, sigma-cube nodes among the solved,
  and whether the solved rows are the first N rows of the shuffled list.
usage: c3spot_check.py RESULTS_DIR
"""
import json, os, sys
from collections import Counter, defaultdict

RES = sys.argv[1]
D = os.path.join(RES, "C3SPOT")
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(D, "units6.tsv")) if l.strip()]
print("units6 rows:", len(rows), "| distinct nodes:", len({r[1] for r in rows}))


def group(src):  # record-source group as in summary.md (directory, plus /LOCAL)
    parts = src.split("/")
    return parts[0] + ("/LOCAL" if len(parts) > 2 and parts[1].startswith("LOCAL") else "")


g = Counter(group(r[4]) for r in rows)
print("per source group (sample):", dict(sorted(g.items())), "| groups:", len(g))
print("sigma-cube nodes in sample:", sum("__" in r[1] for r in rows))

# expected hash vs the original certified record
cache = {}
mism, missing = [], []
for ph, node, opts, sha, src in rows:
    if src not in cache:
        d = defaultdict(list)
        p = os.path.join(RES, src)
        if os.path.exists(p):
            for l in open(p):
                if l.strip():
                    try:
                        r = json.loads(l)
                    except Exception:
                        continue
                    if r.get("node") is not None:
                        d[r["node"]].append(r)
        cache[src] = d
    recs = [r for r in cache[src].get(node, []) if r.get("certified")]
    if not recs:
        missing.append((node, src))
    elif sha not in {r.get("cnf_sha256") for r in recs}:
        mism.append((node, src))
print("units6 expected hash == certified original record hash: missing", len(missing), "mismatch", len(mism),
      missing[:3], mism[:3])

out = [json.loads(l) for l in open(os.path.join(D, "out.jsonl")) if l.strip()]
exp = {r[1]: r[3] for r in rows}
pos = {r[1]: i for i, r in enumerate(rows)}
ok = [o for o in out if o["status"] == "UNSATISFIABLE" and o["lrat_check"] == "c VERIFIED"
      and o["cake_lpr"] == "s VERIFIED UNSAT" and o.get("certified") is True and exp.get(o["node"]) == o["cnf_sha256"]]
print("out rows:", len(out), "| distinct nodes:", len({o['node'] for o in out}), "| all four checks pass:", len(ok))
print("statuses:", Counter(o["status"] for o in out), "| base hashes:", Counter(o.get("base_sha256", "")[:12] for o in out))
print("sigma-cube nodes among solved:", sum("__" in o["node"] for o in out))
print("proof_sha256 present:", sum(bool(o.get("proof_sha256")) for o in out))
idx = sorted(pos[o["node"]] for o in out if o["node"] in pos)
print("solved rows are rows 0..N-1 of the shuffled list:", idx == list(range(len(idx))), "| max index:", idx[-1] if idx else None)
print("solved by group:", dict(sorted(Counter(group(dict((r[1], r[4]) for r in rows)[o["node"]]) for o in out).items())))
