#!/usr/bin/env python3
"""A2 audit: aggregate the independent encoding tests (indep_eval.py logs)."""
import collections, glob, json, os, sys
O = os.path.dirname(os.path.abspath(__file__))
tot = collections.Counter(); bym = collections.defaultdict(collections.Counter)
for f in sorted(glob.glob(os.path.join(O, "logs", "indep_*.jsonl"))):
    for l in open(f):
        r = json.loads(l)
        m, k = r["m"], r["k"]
        fr = len(r.get("nongon_false", []))
        tot["sets"] += 1; tot["frames"] += fr; tot["fail"] += bool(r["fail"])
        kf = not r["has_kgon"]
        tot["kgon_free_sets"] += kf; tot["kgon_free_frames"] += fr * kf
        tot["units_checked"] += sum(r.get("units_checked", []))
        tot["mirror_checked"] += ("mirror_ok" in r); tot["mirror_mut_caught"] += (r.get("mirror_mut_nosigma_ok") is False)
        tot["kept_only_via_mirror"] += (r.get("kept_self") is False and r.get("kept_self_or_mirror") is True)
        tot["reversed_ring_caught_frames"] += sum(1 for x in r.get("mut_reversed_false_units", []) if x > 0)
        tot["sigma_flip_caught_frames"] += sum(1 for x in r.get("mut_sigma_flip_nongon_false", []) if x > 0)
        b = bym[(m, k)]; b["sets"] += 1; b["kgon_free"] += kf; b["fail"] += bool(r["fail"])
print(json.dumps(dict(tot), indent=1))
for (m, k) in sorted(bym):
    print(f"m={m} k={k}: {dict(bym[(m, k)])}")
