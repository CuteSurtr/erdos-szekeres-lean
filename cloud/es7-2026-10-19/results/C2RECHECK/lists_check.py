#!/usr/bin/env python3
"""Check that the unit lists of this directory cover the gaps they are meant to close.

usage: lists_check.py [RESULTS]   (RESULTS = cloud/es7-2026-10-19/results; default: the parent of this directory)
Reads the wave records C2P*/*/out.jsonl, the pilot table C2C34/logs/p8_units.tsv and C2FINAL/sample/out.jsonl, and
from this directory the unit lists and sample_*.jsonl. Only records with "certified" true (pilot rows: UNSAT with both
checker verdicts) count; third-layer pieces (unit names with "/") close no orbit. The orbit of subcase (P_a, V) is
{V, (a - V) mod 17} (reduction B)."""
import collections, csv, glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
units = lambda fn: [l.strip() for l in open(os.path.join(HERE, fn)) if l.strip()]
jl = lambda p: [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []


def orbit(unit):
    case, rest = unit.split("_", 1)
    a, v = int(case[1:]), tuple(sorted(int(x) for x in rest.split("-")))
    return case, min(v, tuple(sorted((a - i) % 17 for i in v)))


kinds, covers, lanes = collections.defaultdict(set), collections.defaultdict(set), collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    src = "/".join(f.split(os.sep)[-3:-1])
    kind = "mac" if "LOCAL" in src else "cloud"
    for r in jl(f):
        if r.get("certified"):
            lanes[src].append((r["solve_s"], r["unit"]))
            if r["unit"].endswith("_cover"):
                covers[r["unit"]].add(kind)
            elif "/" not in r["unit"]:
                kinds[orbit(r["unit"])].add(kind)
for r in csv.DictReader(open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")), delimiter="\t"):
    if (r["unit"].startswith("P8_") and r["status"] == "UNSATISFIABLE" and r["lrat_check"] == "c VERIFIED"
            and r["cake_lpr"] == "s VERIFIED UNSAT"):
        k = "pilot" if r["cnf_sha256"] else "pilot without CNF hash"
        (covers[r["unit"]] if r["unit"].endswith("_cover") else kinds[orbit(r["unit"])]).add(k)
out = {"orbits": len(kinds),
       "orbits_by_evidence": {" + ".join(sorted(k)): n for k, n in
                              collections.Counter(frozenset(v) for v in kinds.values()).most_common()},
       "covers_by_evidence": {u: " + ".join(sorted(v)) for u, v in sorted(covers.items())}}
pil = [u.split("@")[0] for u in units("pilot_units_1.txt") + units("pilot_units_2.txt")]
out["pilot_list_is_one_unit_per_pilot_only_orbit"] = (
    len(pil) == len({orbit(u) for u in pil}) and {orbit(u) for u in pil} == {o for o, v in kinds.items() if v == {"pilot"}})
loc = [u.split("@")[0] for u in units("local_units_1.txt") + units("local_units_2.txt")]
lo, lc = [u for u in loc if not u.endswith("_cover")], [u for u in loc if u.endswith("_cover")]
out["local_list_is_one_unit_per_mac_only_orbit"] = (
    len(lo) == len({orbit(u) for u in lo}) and {orbit(u) for u in lo} == {o for o, v in kinds.items() if v == {"mac"}})
out["local_list_covers_are_the_mac_only_covers"] = set(lc) == {u for u, v in covers.items() if v == {"mac"}}
touched = {r["record_source"] for p in (os.path.join(RES, "C2FINAL", "sample", "out.jsonl"),
                                       os.path.join(HERE, "sample_q3.jsonl"), os.path.join(HERE, "sample_extra.jsonl"))
           for r in jl(p)}
touched |= {u.split("@")[1] for u in units("local_units_1.txt") + units("local_units_2.txt")}
spot = [u.split("@") for u in units("lanespot_units.txt")]
untouched = {s for s in lanes if s not in touched}
out["lanes_with_certified_records"] = len(lanes)
out["lanes_touched_before"] = len(touched & set(lanes))
out["untouched_lanes_not_in_spot_list"] = sorted(untouched - {s for _, s in spot})
out["spot_list_one_unit_per_untouched_lane"] = len(spot) == len({s for _, s in spot}) and {s for _, s in spot} <= untouched
out["spot_list_mac_lanes"] = sorted(s for _, s in spot if "LOCAL" in s)
out["spot_picks_not_shortest_in_lane"] = [f"{u}@{s} (shortest: {min(lanes[s])[1]})" for u, s in spot
                                          if dict((x, t) for t, x in lanes[s])[u] != min(lanes[s])[0]]
rec_s = [dict((x, t) for t, x in lanes[s])[u] for u, s in spot]
out["spot_list_sorted_by_recorded_solve_time"] = rec_s == sorted(rec_s)
print(json.dumps(out, indent=1))
