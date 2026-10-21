#!/usr/bin/env python3
"""Summary of data/e*_w*.jsonl.part*.gz (run sync.py first) -> stdout and data/summary.json."""
import collections, glob, gzip, json, os, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
recs = [json.loads(l) for f in sorted(glob.glob(os.path.join(HERE, "data", "e*_w*.jsonl.part*.gz"))) for l in gzip.open(f, "rt") if l.strip()]
tested = [r for r in recs if "skipped" not in r]
skipped = [r for r in recs if "skipped" in r]
hashes = collections.Counter(r["ot_hash"] for r in tested)
def q(v):
    v = sorted(v)
    return {"min": v[0], "p10": v[len(v)//10], "median": v[len(v)//2], "p90": v[9*len(v)//10], "max": v[-1]} if v else {}
s = {
    "lines": len(recs), "sets_tested": len(tested), "skipped": len(skipped),
    "distinct_order_types": len(hashes), "order_types_tested_more_than_once": sum(1 for h, c in hashes.items() if c > 1),
    "all_saturated": all(r.get("saturated") is True for r in tested),
    "not_saturated": [r for r in tested if r.get("saturated") is not True][:5],
    "bad_candidates_total": sum(r.get("bad_candidates") or 0 for r in tested),
    "faces_covered_all": all(r.get("faces_covered") for r in tested),
    "py_largest_convex_subset": dict(collections.Counter(r["py_largest_convex_subset"] for r in tested)),
    "vfy4_vs_py_GP_agree": all(r["py_general_position"] is True for r in tested),
    "c6": q([r["c6"] for r in tested]), "c5": q([r["c5"] for r in tested]),
    "faces": q([r["faces"] for r in tested]), "hull": dict(collections.Counter(r["hull"] for r in tested)),
    "max_abs_coord": q([r["max_abs_coord"] for r in tested]),
    "walk_len": q([r["walk_len"] for r in tested]),
    "by_base_mild": dict(collections.Counter(r["base_mild"] for r in tested)),
    "distinct_bases": len({(r["base_mild"], r["base_seed"] if r["base_mild"] else 0) for r in tested}),
    "seconds_mean": round(statistics.mean(r["seconds"] for r in tested), 3) if tested else None,
}
c6h = collections.Counter((r["c6"] // 5000) * 5000 for r in tested)
s["c6_histogram_5000"] = dict(sorted(c6h.items()))
fh = collections.Counter((r["faces"] // 1000) * 1000 for r in tested)
s["faces_histogram_1000"] = dict(sorted(fh.items()))
for g in sorted({r["generator"] for r in tested}):
    t = [r for r in tested if r["generator"] == g]
    s["by_generator_" + g] = {"sets": len(t), "distinct_order_types": len({r["ot_hash"] for r in t}),
                             "saturated": sum(1 for r in t if r.get("saturated") is True),
                             "c6": q([r["c6"] for r in t]), "faces": q([r["faces"] for r in t])}
s["min_c6_records"] = [{k: r.get(k) for k in ("generator", "worker", "run", "base_seed", "walk_seed", "beta", "walk_len", "ot_hash", "c6", "c5", "hull", "faces", "bad_candidates")}
                       for r in sorted(tested, key=lambda r: r["c6"])[:3]]
json.dump(s, open(os.path.join(HERE, "data", "summary.json"), "w"), indent=1)
print(json.dumps(s, indent=1))
