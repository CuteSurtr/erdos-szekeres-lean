#!/usr/bin/env python3
"""Compare the small-instance runs of tests/run_small.sh.
usage: compare_small.py DIR
For every PREFIX in DIR with PREFIX_old/new/new2.jsonl:
 - old vs new: the same nodes, the same status and units per node, the same certified set, the
   same cnf_sha256 per node, the same split records; every old field is present in the new record
   with the same value except the timing fields (solve_s, check_s); the new records add only
   cadical_args and proof_sha256, and every certified new record has a proof_sha256;
 - new vs new2 (same tools, same options, run again): the same proof_sha256 for every certified
   node (CaDiCaL on one thread is deterministic) and the same proof_bytes."""
import collections, glob, json, os, sys

d = sys.argv[1]
TIMING = {"solve_s", "check_s"}
ADDED = {"cadical_args", "proof_sha256"}
fails = 0
for fo in sorted(glob.glob(os.path.join(d, "*_old.jsonl"))):
    pre = fo[:-len("_old.jsonl")]
    R = {t: [json.loads(l) for l in open(f"{pre}_{t}.jsonl")] for t in ("old", "new", "new2")}
    by = {t: collections.OrderedDict() for t in R}
    for t, L in R.items():
        for r in L:
            by[t].setdefault((r["node"], bool(r.get("split"))), []).append(r)
    msgs = []
    if set(by["old"]) != set(by["new"]) or set(by["new"]) != set(by["new2"]):
        msgs.append("different node/split sets")
    nfield = 0
    for kx in by["old"]:
        for o, n in zip(by["old"][kx], by["new"].get(kx, [])):
            for f, v in o.items():
                if f in TIMING:
                    continue
                nfield += 1
                if n.get(f) != v:
                    msgs.append(f"{kx}: field {f}: old {v!r} new {n.get(f)!r}")
            extra = set(n) - set(o)
            if not kx[1] and extra != ADDED:
                msgs.append(f"{kx}: new adds {sorted(extra)}")
            if n.get("certified") and not n.get("proof_sha256"):
                msgs.append(f"{kx}: certified without proof_sha256")
    ndet = 0
    for kx, L in by["new"].items():
        for a, b in zip(L, by["new2"].get(kx, [])):
            if a.get("certified"):
                ndet += 1
                if (a.get("proof_sha256"), a.get("proof_bytes"), a.get("cnf_sha256")) != (b.get("proof_sha256"), b.get("proof_bytes"), b.get("cnf_sha256")):
                    msgs.append(f"{kx}: new and new2 proofs differ")
    cert = {t: sorted(k[0] for k, L in by[t].items() if any(r.get("certified") for r in L)) for t in R}
    nsplit = sum(1 for k in by["old"] if k[1])
    st = collections.Counter(r.get("status", "split") for r in R["old"])
    print(f"{os.path.basename(pre)}: records old/new/new2 {len(R['old'])}/{len(R['new'])}/{len(R['new2'])}; "
          f"certified nodes {len(cert['old'])}/{len(cert['new'])}/{len(cert['new2'])}; split records {nsplit}; "
          f"old statuses {dict(st)}; old fields compared {nfield}; new==new2 proof_sha256 on {ndet} certified records; "
          f"{'OK' if not msgs else 'FAIL'}")
    for m in msgs[:20]:
        print("  " + m)
    fails += len(msgs)
print("FAILURES", fails)
