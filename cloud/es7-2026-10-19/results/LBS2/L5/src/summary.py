#!/usr/bin/env python3
"""LBS2 L5: merge run/out_near.jsonl and run/out_anneal.jsonl into out.jsonl (one line per set,
first occurrence of each id) and print the summary used in README.md."""
import collections, json
rows, seen = [], set()
for f in ("run/out_anneal.jsonl", "run/out_near.jsonl"):
    for l in open(f):
        r = json.loads(l)
        if r["id"] in seen: continue
        seen.add(r["id"]); rows.append(r)
with open("out.jsonl", "w") as o:
    for r in rows: o.write(json.dumps(r) + "\n")
def src(r):
    if r["gen"] == "nearmiss-drop": return "nearmiss-" + r["id"].split(":")[1].split("/")[0]
    return r["gen"]
st = collections.Counter((src(r), r["status"].split(" (")[0].split(":")[0]) for r in rows)
print("sets by source and status:")
for k, v in sorted(st.items()): print(f"  {k[0]:24s} {k[1]:40s} {v}")
T = [r for r in rows if r["status"] == "tested"]
allots = {r["ot_hash"] for r in rows if r["status"] in ("tested",) or r["status"].startswith("duplicate")}
print("sets with c7 = 0 checked:", sum(1 for r in rows if r["status"] == "tested" or r["status"].startswith("duplicate")))
print("distinct order types:", len(allots), " tested by sat:", len(T))
for s in sorted({src(r) for r in T}):
    print(f"  {s}: {len({r['ot_hash'] for r in T if src(r) == s})} order types")
print("sat / sat_wide:", collections.Counter(r["sat_variant"] for r in T))
print("all saturated:", all(r["saturated"] for r in T), " bad_candidates total:", sum(r["bad_candidates"] for r in T))
print("faces_euler == faces_hit for all:", all(r["faces_euler_eq_hit"] for r in T))
print("largest convex subset:", collections.Counter(r["largest_convex_subset"] for r in T))
print("vfy7 gp and c7 = 0 and saturate.py gp for all:", all(r["vfy_gp"] and r["c7"] == 0 and r["saturate_gp"] for r in T))
print("faces:", sorted(collections.Counter(r["faces"] for r in T).items()))
def dist(vals, edges):
    c = collections.Counter()
    for v in vals:
        for a, b in zip(edges, edges[1:]):
            if a <= v < b: c[f"[{a},{b})"] += 1; break
    return [(k, c[k]) for k in (f"[{a},{b})" for a, b in zip(edges, edges[1:])) if c[k]]
E = [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 50000, 10**9]
for s in sorted({src(r) for r in T}):
    v = [r["c6"] for r in T if src(r) == s]
    print(f"c6 {s}: min {min(v)} median {sorted(v)[len(v)//2]} max {max(v)}  {dist(v, E)}")
print("sat cpu seconds: median", sorted(r["sat_cpu_seconds"] for r in T)[len(T)//2], "max", max(r["sat_cpu_seconds"] for r in T))
