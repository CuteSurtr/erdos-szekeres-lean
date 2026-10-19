#!/usr/bin/env python3
"""Mirror CNF post-processor for tools/etv/gen_etv.py output.

Reads a CNF produced by gen_etv.py --mirror [--hull] and
 * substitutes every orientation variable by the representative (smallest index) of its
   mirror orbit, dropping the equivalence clauses (which become tautologies) and duplicate
   clauses;
 * optionally (--interior, only without --hull, N odd) adds the two clauses saying the axis
   point c = (N+1)/2 is not extreme: some (i,c,k), i<c<k, is a cup (X true; c is not on the
   upper hull) and some is a cap (X false; c is not on the lower hull);
 * optionally (--yflip-unit) adds the unit X(1,2,3) (WLOG under the global y-reflection,
   which negates every orientation and maps the instance to itself when A = U and no
   --hull units are present);
 * writes the orbit representatives (split candidates) to <out>.reps.

The mirror orbit of X(i,j,k) is {X(i,j,k), X(m-k,m-j,m-i)}, m = N+1 (no hull) or N+2 (hull,
indices 2..N), exactly the identification gen_etv.py writes.
"""
import argparse, itertools, json, sys
ap = argparse.ArgumentParser()
ap.add_argument("cnf"); ap.add_argument("N", type=int)
ap.add_argument("--hull", action="store_true")
ap.add_argument("--interior", action="store_true")
ap.add_argument("--yflip-unit", action="store_true")
ap.add_argument("-o", required=True)
a = ap.parse_args(); N = a.N
idx = {t: n + 1 for n, t in enumerate(itertools.combinations(range(1, N + 1), 3))}
nX = len(idx)
lo = 2 if a.hull else 1; m = N + lo
rep = {}
for (i, j, k), v in idx.items():
    if i < lo:
        rep[v] = v; continue
    w = idx[tuple(sorted((m - k, m - j, m - i)))]
    rep[v] = min(v, w)
def sub(l):
    v = abs(l)
    if v <= nX:
        r = rep[v]; return r if l > 0 else -r
    return l
nv = 0; out = []; seen = set(); taut = dup = 0
with open(a.cnf) as f:
    for line in f:
        if line.startswith('p'):
            nv = int(line.split()[2]); continue
        if line.startswith('c') or not line.strip(): continue
        c = [sub(l) for l in map(int, line.split()[:-1])]
        s = set(c)
        if any(-l in s for l in s): taut += 1; continue
        key = tuple(sorted(s))
        if key in seen: dup += 1; continue
        seen.add(key); out.append(key)
extra = []
if a.interior:
    assert not a.hull and N % 2 == 1
    c = (N + 1) // 2
    cup = sorted(set(sub(idx[(i, c, k)]) for i in range(1, c) for k in range(c + 1, N + 1)))
    extra.append(tuple(cup)); extra.append(tuple(-l for l in cup))
if a.yflip_unit:
    assert not a.hull
    extra.append((sub(idx[(1, 2, 3)]),))
out += extra
with open(a.o, "w") as f:
    f.write(f"p cnf {nv} {len(out)}\n")
    for c in out: f.write(" ".join(map(str, c)) + " 0\n")
reps = sorted(set(rep[idx[t]] for t in idx if t[0] >= lo))  # hull units X(1,i,j) are not split candidates
with open(a.o + ".reps", "w") as f:
    f.write(" ".join(map(str, reps)) + "\n")
print(json.dumps({"in": a.cnf, "out": a.o, "N": N, "vars": nv, "X": nX, "orbit_reps": len(reps),
                  "clauses": len(out), "tautologies_dropped": taut, "duplicates_dropped": dup,
                  "interior": a.interior, "yflip_unit": a.yflip_unit, "hull": a.hull}))
