#!/usr/bin/env python3
"""Compare the cmp_* runs of tests/run_small.sh: C3T close_tree (_old) against C3U close_tree with
the default (_new) and with --sigma-split 0 (_new0).  For each instance: the same records in the
same multiset (records keyed by node and split flag), every field equal except the timings
(solve_s, check_s); in particular the same certified nodes, cnf_sha256, units, caps, status,
cadical_args and proof_sha256, and the same split records.
usage: compare_small.py DIR"""
import collections, glob, json, os, sys

d = sys.argv[1]
TIMING = {"solve_s", "check_s"}
fails = 0


def key(r):
    return json.dumps({k: v for k, v in r.items() if k not in TIMING}, sort_keys=True)


for fo in sorted(glob.glob(os.path.join(d, "cmp_*_old.jsonl"))):
    pre = fo[:-len("_old.jsonl")]
    R = {t: [json.loads(l) for l in open(f"{pre}_{t}.jsonl")] for t in ("old", "new", "new0")}
    C = {t: collections.Counter(key(r) for r in L) for t, L in R.items()}
    msgs = [f"{t} differs from old: {sum((C['old'] - C[t]).values())} old records missing, "
            f"{sum((C[t] - C['old']).values())} extra" for t in ("new", "new0") if C[t] != C["old"]]
    st = collections.Counter("split" if r.get("split") else r["status"] for r in R["old"])
    cert = sum(1 for r in R["old"] if r.get("certified"))
    print(f"{os.path.basename(pre)}: records old/new/new0 {len(R['old'])}/{len(R['new'])}/{len(R['new0'])}; "
          f"old {dict(st)}, certified {cert}; {'OK' if not msgs else 'FAIL'}")
    for x in msgs:
        print("  " + x)
    fails += len(msgs)
print("FAILURES", fails)
