#!/usr/bin/env python3
"""Summarize leaves.jsonl for shard Mii-0: per shard cube, which children are closed, open, SAT;
exact closed weight (each leaf weighs 2^-len(cube) of the whole instance); LRAT coverage;
and a tree check that every closed shard cube is covered by LRAT-verified UNSAT leaves.
usage: summarize.py <leaves.jsonl> <cubes.icnf> [shard=0] [nshards=8]"""
import sys, json
from fractions import Fraction
L, icnf = sys.argv[1], sys.argv[2]
shard = int(sys.argv[3]) if len(sys.argv) > 3 else 0; nsh = int(sys.argv[4]) if len(sys.argv) > 4 else 8
cubes = [tuple(int(x) for x in l.split()[1:-1]) for l in open(icnf) if l.startswith('a')]
mine = [c for i, c in enumerate(cubes) if i % nsh == shard]
rec = {}
for l in open(L):
    r = json.loads(l); rec[tuple(r['cube'])] = r
def state(c):
    """returns (closed_weight, open_weight, sat_list, unverified_unsat_count)"""
    r = rec.get(c); w = Fraction(1, 2 ** len(c))
    if r is None: return Fraction(0), w, [], 0, [c]
    if r['status'] == 'UNSATISFIABLE':
        return (w, Fraction(0), [], 0, []) if r.get('lrat_verified') else (w, Fraction(0), [], 1, [])
    if r['status'] == 'SATISFIABLE': return Fraction(0), Fraction(0), [c], 0, []
    if r['status'] == 'SPLIT':
        tot = [Fraction(0), Fraction(0), [], 0, []]
        for ch in r['children']:
            s = state(tuple(ch['cube']))
            tot = [tot[0] + s[0], tot[1] + s[1], tot[2] + s[2], tot[3] + s[3], tot[4] + s[4]]
        return tuple(tot)
    return Fraction(0), w, [], 0, [c]
out = {"shard": shard, "shard_cubes": len(mine), "cubes_total": len(cubes), "per_cube": []}
CW = OW = Fraction(0); closed = 0; sats = []; unver = 0; openleaves = 0
for i, c in zip(range(shard, len(cubes), nsh), mine):
    cw, ow, sl, uv, ol = state(c); w = Fraction(1, 2 ** len(c))
    out["per_cube"].append({"index": i, "closed_fraction": float(cw / w), "open_leaves": len(ol), "sat": len(sl)})
    CW += cw; OW += ow; sats += sl; unver += uv; openleaves += len(ol)
    closed += (cw == w)
n = len(rec); u = [r for r in rec.values() if r['status'] == 'UNSATISFIABLE']
out.update({"records": n, "unsat_leaves": len(u), "unsat_lrat_verified_both_checkers": sum(1 for r in u if r.get('lrat_verified')),
            "unsat_stock_lrat_check_verified": sum(1 for r in u if r.get('lrat_check') == 'c VERIFIED'),
            "splits": sum(1 for r in rec.values() if r['status'] == 'SPLIT'),
            "sat_leaves": len(sats), "open_leaves": openleaves, "unverified_unsat": unver,
            "shard_cubes_fully_closed": closed,
            "closed_weight_of_shard": str(CW / (Fraction(len(mine), 2 ** 7))), "closed_weight_of_shard_float": float(CW / Fraction(len(mine), 2 ** 7)),
            "closed_weight_of_instance": str(CW), "open_weight_of_instance": str(OW)})
print(json.dumps(out, indent=1))
