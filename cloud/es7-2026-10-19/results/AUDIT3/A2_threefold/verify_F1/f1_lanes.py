#!/usr/bin/env python3
"""verify_F1 part 3: per-lane (record file = one machine/session) coverage by C3SPOT, counting any
re-solved record of the lane (cut or not), and spot-check vs original check throughput.
usage: python3 -I f1_lanes.py R AUDIT_REPORT_JSON"""
import collections, json, os, sys, statistics
R, rep = sys.argv[1], sys.argv[2]
BASE = "bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da"
def canon(r):
    n = r["node"]
    if "cube" in r:
        n += "__" + "-".join(f"{a}s{b}" for a, b in sorted((int(x), int(v)) for x, v in r["cube"].items()))
    return n
def ok(r):
    return (r.get("certified") is True and r.get("status") == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED"
            and r.get("cake_lpr") == "s VERIFIED UNSAT" and r.get("base_sha256", BASE) == BASE)
files = [l.strip() for l in open(os.path.join(R, "C3FINAL/compose_files.txt")) if l.strip()]
cert = collections.defaultdict(list)
for f in files:
    for l in open(os.path.join(R, f)):
        l = l.strip()
        if not l: continue
        r = json.loads(l)
        if "node" in r and "meta" not in r and ok(r):
            cert[canon(r)].append((f, r))
cut = json.load(open(rep))["cut"]
spot = [json.loads(l) for l in open(os.path.join(R, "C3SPOT/out.jsonl")) if l.strip()]
spotn = {s["node"] for s in spot}
# lane = directory of the record file (machine/session); several files may share a lane dir
lane = lambda f: os.path.dirname(f)
lane_cut = collections.Counter(); lane_any_spot = collections.Counter()
for n in cut:
    for L in {lane(f) for f, _ in cert[n]}:
        lane_cut[L] += 1
for n in spotn:
    for L in {lane(f) for f, _ in cert.get(n, [])}:
        lane_any_spot[L] += 1
zero = sorted(((L, c) for L, c in lane_cut.items() if lane_any_spot[L] == 0), key=lambda x: -x[1])
print("lane dirs contributing to the cut:", len(lane_cut), "; with no re-solved record at all:", len(zero),
      "holding", sum(c for _, c in zero), "cut pieces")
for L, c in zero:
    print("   ", L, c)
# throughput: original records vs spot re-solves of the same nodes
pairs = []
for s in spot:
    o = cert.get(s["node"], [])
    if o and s.get("check_s") and o[0][1].get("check_s"):
        pairs.append((o[0][1]["proof_bytes"] / o[0][1]["check_s"], s["proof_bytes"] / s["check_s"], s["proof_bytes"] == o[0][1]["proof_bytes"]))
print("spot rows with both check times:", len(pairs))
print("  orig throughput MB/s median %.1f max %.1f; spot throughput median %.1f max %.1f" % (
    statistics.median(p[0] for p in pairs) / 1e6, max(p[0] for p in pairs) / 1e6,
    statistics.median(p[1] for p in pairs) / 1e6, max(p[1] for p in pairs) / 1e6))
print("  spot rows whose re-solved proof has the same byte size as the original record:", sum(p[2] for p in pairs))
