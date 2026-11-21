"""Negative/maximal controls (own code):
 (1) cups-caps extremal set A(7,7) (252 points, no 7-cup, no 7-cup) built recursively with exact ints:
     states must be a bijection onto the 252 catalog states; Z- and Z*-owners (70 each) must have no
     6-cap/6-cup (Lemma Z / Z* need only no 7-cap/7-cup); first two states.
 (2) random subsets of A(7,7) (contain octagons): checks (a)-(d) and how often rows are violated.
 (3) control_wide_middle_k8.txt (64 points WITH an octagon) under random linear maps + 7-pruning.
 (4) widened classes as negative controls for (b)/(c).
usage: python octcontrol.py <seed> <seconds> <outprefix>
"""
import json, sys, time, random, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from esz import sign_tensor, states, longest_chains, max_convex, ranks, sort_check
import run
from run import analyse, agg_init, agg_add, prune_7, STATES, SIDX, Z, ZS, ROWS_ALL, SUPP, RHS


def build(k, l):
    """No k-cup, no l-cap, C(k+l-4, k-2) points (Erdos-Szekeres cups-caps construction)."""
    if k == 2 or l == 2:
        return [(0, 0)]
    L = build(k - 1, l)
    R = build(k, l - 1)
    B = 1 + max(max(x, y) for x, y in L + R)
    X = B
    Y = B * (2 * B + 1) + B
    return L + [(x + X, y + Y) for x, y in R]


def main(seed, secs, prefix):
    rng = random.Random(seed)
    t0 = time.time()
    out = {}
    P = build(7, 7)
    P = sort_check(P)
    S, ok = sign_tensor(P)
    st, mcap, mcup = states(S)
    idx = [SIDX[s] for s in st]
    zown = [v for v in range(len(P)) if idx[v] in set(Z)]
    zsown = [v for v in range(len(P)) if idx[v] in set(ZS)]
    out['A77'] = {'n': len(P), 'gp': ok, 'mcap': mcap, 'mcup': mcup, 'distinct_states': len(set(idx)),
                  'bijection_onto_catalog': sorted(idx) == list(range(252)),
                  'first_two': [st[0], st[1]],
                  'z_owners': len(zown), 'z_owner_longest_cap_cup': longest_chains(S, zown),
                  'zs_owners': len(zsown), 'zs_owner_longest_cap_cup': longest_chains(S, zsown),
                  'max_coord_bits': max(max(abs(x), abs(y)) for x, y in P).bit_length(),
                  'secs': time.time() - t0}
    # widened classes (negative controls)
    wideZ = [i for i, f in enumerate(STATES) if f[4] == 0]                 # f(0) <= 5, f(4) = 0
    wideZs = [i for i, f in enumerate(STATES) if f[0] >= 4 and f[4] >= 1]  # f(0) >= 4, f(4) >= 1
    for nm, cls in (('wideZ_f4eq0', wideZ), ('wideZs_f0ge4_f4ge1', wideZs)):
        own = [v for v in range(len(P)) if idx[v] in set(cls)]
        out['A77'][nm] = {'owners': len(own), 'longest_cap_cup': longest_chains(S, own)}
    h = np.ones(252, dtype=np.int32); h[idx] = 0
    out['A77']['rows_violated_full_set'] = int(((SUPP @ h - RHS) < 0).sum())
    print(json.dumps(out['A77']), flush=True)
    # (2) random subsets of A(7,7)
    A = agg_init()
    recs = []
    t1 = time.time()
    wide_counts = {'wideZs_has6': 0, 'sets': 0}
    while time.time() - t1 < secs * 0.5:
        m = rng.randint(20, 120)
        keep = sorted(rng.sample(range(len(P)), m))
        Q = [P[i] for i in keep]
        r = analyse(Q, 'A77sub', A, save_viol=True)
        agg_add(A, r)
        if r is not None:
            recs.append({k: r[k] for k in ('n', 'maxconvex', 'n_viol', 'occupied', 'z_owners', 'zs_owners') if k in r})
            # widened Z* control on the subset
            sub = S[np.ix_(keep, keep, keep)]
            sst, _, _ = states(sub)
            own = [v for v in range(m) if SIDX[sst[v]] in set(wideZs)]
            c = longest_chains(sub, own)
            wide_counts['sets'] += 1
            wide_counts['wideZs_has6'] += (c[0] >= 6 or c[1] >= 6)
    out['A77_subsets'] = {'agg': A, 'wideZs': wide_counts}
    print(json.dumps(out['A77_subsets']), flush=True)
    # (3) control_wide_middle_k8 (has an octagon) under random linear maps
    base = run.load_sets()
    C = base['control_wide_middle_k8.txt']
    A2 = agg_init()
    t2 = time.time()
    while time.time() - t2 < secs * 0.5:
        while True:
            a, b, c, d = [rng.randint(-7, 7) for _ in range(4)]
            if a * d - b * c != 0:
                break
        Q = sort_check([(a * x + b * y, c * x + d * y) for x, y in C])
        if Q is None:
            continue
        S2, ok2 = sign_tensor(Q)
        if not ok2:
            continue
        Q = prune_7(Q, rng)
        r = analyse(Q, 'ctrlwide', A2, save_viol=True)
        agg_add(A2, r)
    out['control_wide_middle'] = A2
    print(json.dumps(A2), flush=True)
    out['elapsed'] = time.time() - t0
    json.dump(out, open(prefix + '.json', 'w'), default=list)


if __name__ == '__main__':
    main(int(sys.argv[1]), float(sys.argv[2]), sys.argv[3])
