#!/usr/bin/env python3
"""Claim 7 (mirror reduction) tested directly with my own normal form.

For real S (centrally symmetric, parallelogram hull, m odd) and its reflection R(S) = {(-x, y)}:
  (a) the two admissible rs edges of S (V1V2 and its opposite) give the same labelled order type;
  (b) if the inner nu-coordinates (w.r.t. the chosen edge) are pairwise distinct (including p vs -p), then
      o_R(i,j,k) = -chi_S(t(i),t(j),t(k)) for ALL triples, t swapping 1<->2 and n-1<->n;
      in particular o_R = -o_S on every inner triple;
  (c) with ties in nu the relation can fail; a symmetric perturbation that keeps the (point-identity) order type
      removes the ties and restores (b);
  (d) the second-layer cube satisfied by L(S) and by L(R(S)) are mirror names: Q3.x <-> Q3.(n+1-x),
      H3.a.b <-> H3.(n+1-b).(n+1-a); and the third layer likewise (layerwise rule);
  (e) exactly one of L(S), L(R(S)) has o(I,J,K) false for several inner triples.
usage: t4_mirror.py GEN SEED TRIALS N"""
import itertools, json, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rv import *
from t3_n34 import gen as gen34
from t2_cnf import load32


def nu_ties(S, info):
    nu = info["nu"]; n = len(S)
    vals = [dot(nu, p) for p in S[2:n - 2]]
    return len(set(vals)) != len(vals)


def layer_names(S):
    """my own computation of the nested inner hull layers, named like l2sgn/l3sgn (v1 = min label of the layer)."""
    n = len(S); A = lambda x: n + 1 - x
    R = list(range(3, n - 1)); names = []
    while len(R) >= 4:
        pts = [S[x - 1] for x in R]
        H = hull_ccw(pts)
        lab = {S[x - 1]: x for x in R}
        cyc = [lab[p] for p in H]
        first = min(R)
        if first not in cyc:
            return names + ["ERR-min-not-vertex"]
        r = cyc.index(first); cyc = cyc[r:] + cyc[:r]
        h = len(cyc) // 2
        assert all(cyc[i + h] == A(cyc[i]) for i in range(h))
        if h == 2:
            names.append(f"Q{cyc[0]}.{cyc[1]}")
        elif h == 3:
            names.append(f"H{cyc[0]}.{cyc[1]}.{cyc[2]}")
        else:
            names.append(f"X{h}")
            break
        used = set(cyc); R = [x for x in R if x not in used]
    return names


def mirror_name(name, n):
    A = lambda x: n + 1 - x
    out = []
    for layer in name:
        if layer[0] == "Q":
            v1, v2 = map(int, layer[1:].split(".")); out.append(f"Q{v1}.{A(v2)}")
        elif layer[0] == "H":
            v1, v2, v3 = map(int, layer[1:].split(".")); out.append(f"H{v1}.{A(v3)}.{A(v2)}")
        else:
            out.append(layer)
    return out


def perturb(P, rng, L=10 ** 6, eps=50):
    reps = sorted({max(p, neg(p)) for p in P})
    Q = []
    img = {}
    for p in reps:
        dlt = (rng.randint(-eps, eps), rng.randint(-eps, eps))
        q = (p[0] * L + dlt[0], p[1] * L + dlt[1])
        img[p] = q; img[neg(p)] = neg(q)
    Pp = [img[p] for p in P]
    for a, b, c in itertools.combinations(range(len(P)), 3):
        if (det(P[a], P[b], P[c]) > 0) != (det(Pp[a], Pp[b], Pp[c]) > 0):
            return None
    return Pp


def gen_small(rng, n):
    """random parallelogram set with n points (uniform) or antipodal subset of the real 32-point set."""
    if rng.random() < 0.5:
        while True:
            P = rand_par_set(rng, n // 2 - 2, R=rng.choice([30, 1000]))
            if P is not None and len(hull_ccw(P)) == 4:
                return P
    Q = load32(); H = hull_ccw(Q); hs = set(H)
    inner = sorted({max(p, neg(p)) for p in Q if p not in hs}); hp = sorted({max(p, neg(p)) for p in H})
    sub = rng.sample(inner, n // 2 - 2)
    return [x for p in hp + sub for x in (p, neg(p))]


if __name__ == "__main__":
    g, seed, T, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed); t0 = time.time()
    assert (n // 2 - 2) % 2 == 1
    st = dict(trials=0, a_same_type=0, generic=0, b_ok=0, b_fail=0, ties=0, c_tie_fail=0, c_perturbed_ok=0,
              c_perturb_failed=0, d_ok=0, d_bad=0, d_layers_checked=0, e_ok=0, e_bad=0)
    examples = []
    triples = [(3, 4, 5), (3, n // 2, n // 2 + 1), (n // 2 - 1, n // 2, n // 2 + 1), (3, 5, n - 3), (4, 9, 13)]
    tau = lambda x: {1: 2, 2: 1, n - 1: n, n: n - 1}.get(x, x)
    for tr in range(T):
        P = gen34(g, rng) if n == 34 else gen_small(rng, n)
        st["trials"] += 1
        S0, i0 = par_normal_form(P, rs=True, choice=0)
        S1, i1 = par_normal_form(P, rs=True, choice=1)
        assert i0["ngood"] == 2
        if orient_table(S0) == orient_table(S1):
            st["a_same_type"] += 1
        Ps = [P]
        if nu_ties(S0, i0):
            st["ties"] += 1
            Pp = None
            for _ in range(20):
                Pp = perturb(P, rng)
                if Pp is not None and not nu_ties(*par_normal_form(Pp, rs=True)):
                    break
                Pp = None
            if Pp is None:
                st["c_perturb_failed"] += 1
            else:
                Ps.append(Pp)
        for idx, Q in enumerate(Ps):
            S, info = par_normal_form(Q, rs=True, choice=rng.randrange(2))
            RS, rinfo = par_normal_form(reflect(Q), rs=True, choice=rng.randrange(2))
            oS, oR = orient_table(S), orient_table(RS)
            rel = all(oR[t] == (not chi_real(S, tau(t[0]), tau(t[1]), tau(t[2]))) for t in oR)
            tie = nu_ties(S, info)
            if not tie:
                st["generic"] += 1
                if rel:
                    st["b_ok"] += 1
                else:
                    st["b_fail"] += 1; examples.append(("b_fail", Q))
                if idx == 1:
                    st["c_perturbed_ok"] += int(rel)
                # (d)
                nS, nR = layer_names(S), layer_names(RS)
                if mirror_name(nS, n) == nR:
                    st["d_ok"] += 1; st["d_layers_checked"] += len(nS)
                else:
                    st["d_bad"] += 1; examples.append(("d_bad", nS, nR))
                # (e)
                for t in triples:
                    if oS[t] != oR[t]:
                        st["e_ok"] += 1
                    else:
                        st["e_bad"] += 1; examples.append(("e_bad", t))
            else:
                if not rel:
                    st["c_tie_fail"] += 1
    print(json.dumps({"gen": g, "n": n, **st}))
    for e in examples[:3]:
        print("EXAMPLE", e)
    print("time", round(time.time() - t0, 1))
