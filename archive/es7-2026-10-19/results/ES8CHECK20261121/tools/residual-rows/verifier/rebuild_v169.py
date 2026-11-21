"""Reconstruct the 1,990 non-capacity rows of b35s20-v169 from files in git (verify-residual-row):
s20-v5 extra rows 2.. (971) + audit/cuts-v6..v13 replay rows (49) = s20-v13 rows 2.. (1,020),
then the audit replay rows of every batch folder cuts-v<k><suffix>, k = 101..169 (970).
Per-round counts are compared with ES307N20261118/data/rows_stated_v169.json. Not hash-bound to the
live extra.json (which is not in git): reconstruction only."""
import json, os, re, sys

REPO = sys.argv[1]
B34 = REPO + "/archive/es7-2026-10-19/results/LO33N20261113/budget34"
AUD = B34 + "/audit"
v5 = json.load(open(B34 + "/data/frozen-inputs/s20-v5/extra.json"))
base = [(sorted(r["support"]), r["rhs"]) for r in v5[2:]]
assert len(base) == 971
for k in range(6, 14):
    rr = [json.loads(l) for l in open(f"{AUD}/cuts-v{k}/replay.jsonl")]
    base += [(sorted(r["support"]), r["rhs"]) for r in rr]
print("s20-v13 rows 2.. reconstructed:", len(base))
stated = json.load(open(REPO + "/archive/es7-2026-10-19/results/ES307N20261118/data/rows_stated_v169.json"))
app, per = [], {}
for k in range(101, 170):
    ds = sorted(d for d in os.listdir(AUD) if re.fullmatch(rf"cuts-v{k}([a-z][a-z0-9]*)?", d))
    cnt = 0
    for d in ds:
        rr = [json.loads(l) for l in open(f"{AUD}/{d}/replay.jsonl")]
        app += [(sorted(r["support"]), r["rhs"]) for r in rr]
        cnt += len(rr)
    per[str(k)] = cnt
mism = {k: (per[k], v) for k, v in stated["rows_per_round"].items() if per.get(k) != v}
allr = base + app
sups = [tuple(s) for s, _ in allr]
print("appended reconstructed:", len(app), "per-round mismatches vs rows_stated_v169:", mism)
print("total non-capacity rows:", len(allr), "distinct supports:", len(set(sups)),
      "rhs counts:", {d: sum(1 for _, x in allr if x == d) for d in set(x for _, x in allr)})
with open(sys.argv[2], "w") as f:
    for s, d in allr:
        f.write(json.dumps({"support": s, "rhs": d}) + "\n")
