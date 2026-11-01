"""Independent derivation of the triple-variable classes of zcnf.py rot (m = 2), and a check of the encoder's map.

Elements: points 0..N-1 (N = 2t; pair o = {2o, 2o+1}, h(i) = i ^ 1) and the centre Z = N.
Derived in proof.md (Lemma 4), by hand, not by union-find:
  * zero triples: exactly {Z, 2o, 2o+1};
  * type A: a triple of three points from three different pairs; its class is {T, h(T)} and
    chi(h a, h b, h d) = chi(a, b, d);
  * type B: for two different pairs P = {p, hp}, Q = {q, hq} (p, q even), one class of 8 triples
        (c,p,q) +s   (c,p,hq) -s   (c,hp,q) -s   (c,hp,hq) +s
        (hp,p,q) +s  (hp,p,hq) -s  (hq,q,p) -s   (hq,q,hp) +s      where s = chi(c, p, q).
So there are C(t,3)*4 type-A classes and C(t,2) type-B classes.
"""
import itertools
import json
import sys


def perm_sign(seq):
    """sign of the permutation that sorts seq (distinct entries)"""
    s = 1
    seq = list(seq)
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                s = -s
    return s


def ordered_to_sorted(T, rel):
    """chi(T as ordered) = rel * ref  ->  (sorted T, sign with chi(sorted T) = sign * ref)"""
    return tuple(sorted(T)), rel * perm_sign(T)


def my_classes(t):
    """dict: sorted triple -> (class key, sign) with chi(triple) = sign * chi(class reference)"""
    N, Z = 2 * t, 2 * t
    h = lambda i: i ^ 1
    cl = {}
    # type A
    for a, b, d in itertools.combinations(range(N), 3):
        if len({a >> 1, b >> 1, d >> 1}) < 3:
            continue
        key = ("A", min((a, b, d), tuple(sorted((h(a), h(b), h(d))))))
        ref = key[1]
        if (a, b, d) == ref:
            cl[(a, b, d)] = (key, 1)
        else:
            # (a,b,d) = h(ref) as sets; chi(h r0, h r1, h r2) = chi(r0, r1, r2) = ref
            img = tuple(h(x) for x in ref)            # ordered image of the sorted reference
            S, s = ordered_to_sorted(img, 1)
            assert S == (a, b, d)
            cl[(a, b, d)] = (key, s)
    # type B
    for P, Q in itertools.combinations(range(t), 2):
        p, q = 2 * P, 2 * Q
        hp, hq = h(p), h(q)
        key = ("B", P, Q)
        for T, rel in [((Z, p, q), 1), ((Z, p, hq), -1), ((Z, hp, q), -1), ((Z, hp, hq), 1),
                       ((hp, p, q), 1), ((hp, p, hq), -1), ((hq, q, p), -1), ((hq, q, hp), 1)]:
            S, s = ordered_to_sorted(T, rel)
            assert S not in cl
            cl[S] = (key, s)
    return cl


def zero_triples(t):
    N = 2 * t
    return {(2 * o, 2 * o + 1, N) for o in range(t)}


def check_map(info, verbose=True):
    """compare the encoder's map (zcnf --map JSON) with my_classes; returns (ok, messages, tv)"""
    t, N, Z = info["t"], info["N"], info["Z"]
    msgs = []
    assert info["kind"] == "rot" and info["m"] == 2 and info["axis"] == 0 and N == 2 * t and Z == N
    tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
    mine = my_classes(t)
    allT = set(itertools.combinations(range(N + 1), 3))
    ok = True
    if set(tv) != set(mine):
        ok = False
        msgs.append(f"triple sets differ: map-only {len(set(tv) - set(mine))}, mine-only {len(set(mine) - set(tv))}")
    if allT - set(tv) != zero_triples(t):
        ok = False
        msgs.append("triples missing from the map are not exactly the zero triples {Z, 2o, 2o+1}")
    # partition and relative signs: for each of my classes, the map must use one variable, with s_map * s_mine const
    byclass = {}
    for T, (key, s) in mine.items():
        if T in tv:
            byclass.setdefault(key, []).append((T, s))
    var_of_key = {}
    for key, lst in byclass.items():
        vs = {tv[T][0] for T, _ in lst}
        prods = {tv[T][1] * s for T, s in lst}
        if len(vs) != 1 or len(prods) != 1:
            ok = False
            msgs.append(f"class {key}: map variables {vs}, relative-sign products {prods}")
        var_of_key[key] = next(iter(vs))
    if len(set(var_of_key.values())) != len(var_of_key):
        ok = False
        msgs.append("two of my classes share a map variable (map is coarser than the derived partition)")
    nA = sum(1 for k in byclass if k[0] == "A")
    nB = sum(1 for k in byclass if k[0] == "B")
    expA, expB = 4 * t * (t - 1) * (t - 2) // 6, t * (t - 1) // 2
    if (nA, nB) != (expA, expB):
        ok = False
        msgs.append(f"class counts A={nA} B={nB}, expected {expA} {expB}")
    if info["X_vars"] != expA + expB or set(var_of_key.values()) != set(range(1, expA + expB + 1)):
        ok = False
        msgs.append("triple variables are not exactly 1..X_vars")
    msgs.append(f"t={t}: {len(tv)} nonzero triples, {nA} type-A + {nB} type-B classes = {nA + nB}; "
                f"X_vars={info['X_vars']}; partition and signs {'agree' if ok else 'DISAGREE'}")
    return ok, msgs, tv


def conv_numbering(N, K, X_vars):
    """conv variables as documented in zcnf.py add_kgon: r = 4..K-1, combinations in lexicographic order, only sets
    that are lexicographically <= their half-turn image (sorted), numbered from X_vars + 1.  Returns list of sets."""
    h = lambda i: i ^ 1
    sets = []
    for r in range(4, K):
        for S in itertools.combinations(range(N), r):
            if S <= tuple(sorted(h(x) for x in S)):
                sets.append(S)
    return sets       # variable of sets[i] is X_vars + 1 + i


if __name__ == "__main__":
    info = json.load(open(sys.argv[1]))
    ok, msgs, _ = check_map(info)
    print("\n".join(msgs))
    sets = conv_numbering(info["N"], info["K"], info["X_vars"])
    nv = info["X_vars"] + len(sets)
    print(f"conv sets {len(sets)}; X_vars + conv = {nv}; header vars {info['vars']}: "
          f"{'OK' if nv == info['vars'] else 'MISMATCH'}")
    print("MAP CHECK", "PASSED" if ok and nv == info["vars"] else "FAILED")
