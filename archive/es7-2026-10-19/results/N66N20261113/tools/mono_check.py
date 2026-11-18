"""Clause-level soundness control of the monolithic CNF (mono66.generate + tail_clauses) on real point sets.
For a real (6-cap-free, 6-cup-free, octagon-free) point set the canonical assignment is
  sel_i = state i occupied;  before / cap_ge / cup_ge / orientation from the points (exact integer arithmetic);
  C_k(p,u,v) = the owners of p,u,v exist and some k-cap of the set starts at p and ends with (u,v); U_k likewise;
  CE(p,q) = some 5-cap from p to q; UE likewise;  atoms of unoccupied owners = false.
Every clause (with its selector guards) must be true, and the number of holes must be 70 - |P|.
usage: mono_check.py <seconds> <seed>      (point sets: the exact ETV 50-point set and reflections first, then
subsets, perturbations and greedy random sets)"""
import sys, json, time, random, itertools
import etv_common as ec, coupled5, mono66
from geom import labels, states, ok_class, general, det
from etvcon import etv
N = ec.N
def check_set(P):
    P = sorted(P); n = len(P); assert ok_class(P)
    st, Em, Ep = states(P)
    pos = {s: i for i, s in enumerate(st)}            # state -> position
    occ = set(st)
    # chains by position
    K = {False: {}, True: {}}                          # sign (True = cup) -> k -> set of (p,u,v)
    sgn = {}
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n): sgn[(a, b, c)] = det(P[a], P[b], P[c]) > 0
    for sg in (False, True):
        K3 = {t for t, v in sgn.items() if v == sg}
        cur = K3; lv = {3: K3}
        for k in (4, 5):
            nxt = set()
            for (p, t, u) in cur:
                for v in range(u + 1, n):
                    if sgn[(t, u, v)] == sg: nxt.add((p, u, v))
            lv[k] = nxt; cur = nxt
        K[sg] = lv
    assert not any(True for _ in ()) 
    val = {}
    stats = {'clauses': 0, 'evaluated': 0, 'violations': 0}
    holder = {}
    def lit_true(l):
        v = val.get(abs(l), False)
        return v if l > 0 else not v
    def emit(c, own):
        stats['clauses'] += 1
        for o in own:
            if o not in occ: return
        stats['evaluated'] += 1
        for l in c:
            if lit_true(l): return
        stats['violations'] += 1
        if stats['violations'] <= 3: print('VIOLATION', c, own, flush=True)
    # variable values must exist before clauses are emitted: build the id tables first with a dry generator
    cnf = coupled5.CNF(list(range(N)), static=False)
    for key, var in cnf.ids.items():
        kind = key[0]
        if kind == 'before':
            i, j = key[1:]; val[var] = (i in occ and j in occ and pos[i] < pos[j])
        elif kind in ('cap_ge', 'cup_ge'):
            i, j, k = key[1:]
            if i in occ and j in occ:
                u, v = sorted((pos[i], pos[j])); lab = (Em[u][v] - 1) if kind == 'cap_ge' else (Ep[u][v] - 1); val[var] = lab >= k
        elif kind == 'orientation':
            i, j, k = key[1:]
            if i in occ and j in occ and k in occ: val[var] = det(P[pos[i]], P[pos[j]], P[pos[k]]) > 0
    # chain atoms are numbered during generation, in a deterministic order: run the generator once without checking
    # to learn the numbering, then again with checking.
    cnf0, sel, top, C, U, CE, UE = mono66.generate(lambda c, own: None)
    for i in range(N): val[sel[i]] = i in occ
    for (k, a, b, c), var in C.items():
        if a in occ and b in occ and c in occ and pos[a] < pos[b] < pos[c]: val[var] = (pos[a], pos[b], pos[c]) in K[False][k]
    for (k, a, b, c), var in U.items():
        if a in occ and b in occ and c in occ and pos[a] < pos[b] < pos[c]: val[var] = (pos[a], pos[b], pos[c]) in K[True][k]
    for (p, q), var in CE.items():
        if p in occ and q in occ and pos[p] < pos[q]: val[var] = any((pos[p], u, pos[q]) in K[False][5] for u in range(pos[p] + 1, pos[q]))
    for (p, q), var in UE.items():
        if p in occ and q in occ and pos[p] < pos[q]: val[var] = any((pos[p], u, pos[q]) in K[True][5] for u in range(pos[p] + 1, pos[q]))
    cnf1, sel1, top1, C1, U1, CE1, UE1 = mono66.generate(emit)
    assert sel1 == sel and top1 == top and C1 == C
    holes = N - n
    tail, top2 = mono66.tail_clauses(sel, top, holes)       # budget = actual number of holes: must be satisfiable
    from pysat.solvers import Cadical153
    with Cadical153(bootstrap_with=tail) as s:
        ok = s.solve(assumptions=[sel[i] if i in occ else -sel[i] for i in range(N)])
    tail2, _ = mono66.tail_clauses(sel, top, holes - 1)
    with Cadical153(bootstrap_with=tail2) as s:
        ok2 = s.solve(assumptions=[sel[i] if i in occ else -sel[i] for i in range(N)])
    stats.update({'points': n, 'holes': holes, 'budget_holes_sat': ok, 'budget_holes_minus_1_sat': ok2,
                  'cap5_chains': len(K[False][5]), 'cup5_chains': len(K[True][5])})
    return stats
if __name__ == '__main__':
    secs = float(sys.argv[1]); rng = random.Random(int(sys.argv[2])); t0 = time.time()
    E0 = sorted(etv(8, 6, 6))
    sets = [('etv50', E0), ('etv50 mirrored', sorted((x, -y) for x, y in E0)), ('etv50 x-reversed', sorted((-x, y) for x, y in E0))]
    tot = {'sets': 0, 'clauses_evaluated': 0, 'violations': 0}
    i = 0
    while time.time() - t0 < secs:
        if i < len(sets): name, Pset = sets[i]
        elif i % 2:
            V = rng.choice([s for _, s in sets]); Pset = rng.sample(V, rng.randrange(36, 50)); name = 'etv subset'
        else:
            Pset = []; name = 'greedy'
            for _ in range(250):
                x = (rng.randrange(-10**6, 10**6), rng.randrange(-10**6, 10**6))
                if general(Pset, x) and ok_class(sorted(Pset + [x])): Pset = sorted(Pset + [x])
        i += 1
        st = check_set(Pset); st['set'] = name
        print(json.dumps(st), flush=True)
        tot['sets'] += 1; tot['clauses_evaluated'] += st['evaluated']; tot['violations'] += st['violations']
        assert st['budget_holes_sat'] and not st['budget_holes_minus_1_sat']
    tot['seconds'] = round(time.time() - t0); print(json.dumps(tot))
