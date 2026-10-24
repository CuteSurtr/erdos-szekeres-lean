"""C3AUDIT4: targeted adversarial record sets (results/C3AUDIT4/TASK.md step 1), each with the outcome a correct
composer must give, judged against every composer given and against the own brute force of fuzz.py's tree.
Background: every depth-2 node certified except the target P; the scenario is built under P.
Expected: 'reject' (exit 1), 'not covered', or 'covered'; 'not covered*' = the certified leaves do cover
(brute: 0 holes) but no single route is complete, so a composer following the specification must say
not covered (covered would also be sound; reported separately).
usage: adv.py OUTDIR COMPOSER [COMPOSER ...]     (bases from $BASEDIR/b{m}{k}.cnf)"""
import hashlib, itertools, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(R, "C3a")); sys.path.insert(0, os.path.join(R, "C3AUDIT3", "tools"))
from c3cnf import C3Enc  # noqa
import mycompose as Y  # noqa  (units() only: CNF bytes)
OUT = sys.argv[1]; COMPS = sys.argv[2:]
BD = os.environ["BASEDIR"]
os.makedirs(OUT, exist_ok=True)


class T:
    def __init__(s, m, k):
        s.m, s.k = m, k
        s.base = os.path.join(BD, f"b{m}{k}.cnf")
        s.E = C3Enc(m, k)
        with open(s.base, "rb") as f:
            s.hdr = f.readline().decode().split(); s.body = f.read()
        s.pre = {}

    def sha(s, L, C=()):
        us = Y.units(s.m, s.E, L, C)
        if len(us) not in s.pre:
            h = hashlib.sha256(); h.update(f"p cnf {s.hdr[2]} {int(s.hdr[3]) + len(us)}\n".encode()); h.update(s.body); s.pre[len(us)] = h
        h = s.pre[len(us)].copy(); h.update("".join(f"{u} 0\n" for u in us).encode()); return h.hexdigest()

    def kids(s, L):
        m = s.m
        if not L:
            o = [(((0, 0),),)]
            if s.k >= 7:
                o += [(((0, 0), (a, v)),) for a in range(1, m // 2 + 1) for v in (0, 1)]
            return o
        used = {r for X in L for r, _ in X}
        fr = [r for r in range(m) if r not in used]
        o = [((r, None),) for r in fr] + [((b, x), (c, y)) for b, c in itertools.combinations(fr, 2) for x in (0, 1) for y in (0, 1)]
        if L == (((0, 0),),):
            mir = lambda X: tuple(sorted(((m - r) % m, None if v is None else 1 - v) for r, v in X))
            kk = lambda X: tuple((r, -1 if v is None else v) for r, v in sorted(X))
            o = [x for x in o if kk(x) <= kk(mir(x))]
        return [L + (x,) for x in o]

    def free(s, L, C=()):
        u = {r for X in L for r, _ in X} | {r for r, _ in C}
        return [r for r in range(1, s.m) if r not in u]

    def ckids(s, L, C):
        cv = dict(C)
        return [c for c in s.kids(L) if not any(v is not None and r in cv and cv[r] != v for r, v in c[-1])]

    def skids(s, L, C, K):
        b = s.free(L, C)[:K]
        return b, [tuple(sorted(C + tuple(zip(b, vs)))) for vs in itertools.product((0, 1), repeat=K)]


def nm(L, C=()):
    x = "_".join("-".join(str(r) if v is None else f"{r}s{v}" for r, v in X) for X in L)
    return x + ("__" + "-".join(f"{r}s{v}" for r, v in C) if C else "")


CERT = {"status": "UNSATISFIABLE", "lrat_check": "c VERIFIED", "cake_lpr": "s VERIFIED UNSAT", "certified": True}


def cert(t, L, C=()):
    return dict(CERT, node=nm(L, C), cnf_sha256=t.sha(L, C))


def sc(t, L, C):  # sigma_cubes.py record of L__C
    return dict(CERT, node=nm(L), cube={str(r): v for r, v in C}, cnf_sha256=t.sha(L, C))


def split(L, C=(), bits=None, n=0):
    r = {"node": nm(L, C), "split": True, "children": n}
    if bits is not None: r["sigma_bits"] = bits
    return r


def background(t, P):
    """all depth-2 nodes except P certified (and all depth-1 nodes split)."""
    out = []
    for c1 in t.kids(()):
        out.append(split(c1, n=len(t.kids(c1))))
        for c2 in t.kids(c1):
            if c2 != P: out.append(cert(t, c2))
    return out


def chain_to_full(t, L, C, rng_pick=0):
    """layer-split L__C (rule 3) down to a fully layered node, certifying all side children; returns
    (records, full layers).  Picks the child index rng_pick (mod len) at every level."""
    out = []
    while True:
        ch = t.ckids(L, C)
        if not ch: return out, L
        nx = ch[rng_pick % len(ch)]
        out.append(split(L, C, n=len(ch)))
        out += [cert(t, c, C) for c in ch if c != nx]
        L = nx


CASES = []


def case(name, expect, m, k):
    def deco(f):
        CASES.append((name, expect, m, k, f)); return f
    return deco


def d2(t, i=0):
    return t.kids(t.kids(())[0])[i]


# ---------- childless plain / cube nodes through rule-3 splits ----------
for (m, k) in [(5, 6), (6, 6), (7, 6), (7, 5)]:
    @case(f"c01_childless_plain_one_cube_m{m}k{k}", "not covered*", m, k)
    def _(t):
        # P sigma split on 1 bit; P__r0 certified; P__r1 layer split down to FULL__r1 certified. Then the
        # plain layer route of P is explored: its child chain toward FULL (plain) has FULL childless and uncertified.
        P = d2(t); b, cs = t.skids(P, (), 1)
        recs = background(t, P) + [split(P, (), b, 2), cert(t, P, cs[0])]
        r2, full = chain_to_full(t, P, cs[1]); recs += r2[:-0 or None]
        recs = [x for x in recs if x.get("node") != nm(P, cs[1]) or not x.get("split")]  # drop P__r1's layer split: sigma route incomplete
        recs.append(cert(t, full, cs[1]))
        # the plain layer route of P: certify every plain side child along the same chain, never FULL itself
        L = P
        while t.kids(L):
            ch = t.kids(L); nx = full[:len(L) + 1]
            recs += [cert(t, c) for c in ch if c != nx]
            L = nx
        return recs

    @case(f"c02_childless_cube_rule3_m{m}k{k}", "not covered", m, k)
    def _(t):
        # sigma route complete except: P__r1 layer split (rule 3) down to a fully layered FULL__r1 that is not certified
        P = d2(t); b, cs = t.skids(P, (), 1)
        recs = background(t, P) + [split(P, (), b, 2), cert(t, P, cs[0])]
        r2, full = chain_to_full(t, P, cs[1]); recs += r2 + [split(full, cs[1], n=0)]
        return recs

    @case(f"c02b_childless_cube_rule3_certified_m{m}k{k}", "covered", m, k)
    def _(t):
        P = d2(t); b, cs = t.skids(P, (), 1)
        recs = background(t, P) + [split(P, (), b, 2), cert(t, P, cs[0])]
        r2, full = chain_to_full(t, P, cs[1]); recs += r2 + [cert(t, full, cs[1])]
        return recs

    @case(f"c03_childless_plain_layer_route_m{m}k{k}", "not covered", m, k)
    def _(t):
        # plain layer route of P down to a FULL that is uncertified, with a 'split children 0' record (old close_tree)
        P = d2(t)
        recs = background(t, P)
        r2, full = chain_to_full(t, P, ()); recs += r2 + [split(full, n=0)]
        return recs

    @case(f"c04_childless_plain_all_but_one_cube_m{m}k{k}", "not covered", m, k)
    def _(t):
        # FULL reached by layer route; of FULL's cubes on its last one-orbit residues, all but one certified
        P = d2(t)
        recs = background(t, P)
        r2, full = chain_to_full(t, P, ()); recs += r2
        ones = [X[0][0] for X in full[2:] if len(X) == 1][:2]
        if not ones: return None
        for vs in list(itertools.product((0, 1), repeat=len(ones)))[:-1]:
            recs.append(cert(t, full, tuple(zip(ones, vs))))
        return recs

# ---------- sigma split with a missing or wrong cube ----------
for (m, k) in [(6, 6), (7, 6)]:
    for K in (1, 2, 3):
        @case(f"s01_missing_cube_K{K}_m{m}k{k}", "not covered", m, k)
        def _(t, K=K):
            P = d2(t, 3); b, cs = t.skids(P, (), K)
            return background(t, P) + [split(P, (), b, 2 ** K)] + [cert(t, P, c) for c in cs[1:]]

        @case(f"s02_wrong_cube_dup_K{K}_m{m}k{k}", "not covered", m, k)
        def _(t, K=K):
            P = d2(t, 3); b, cs = t.skids(P, (), K)
            return background(t, P) + [split(P, (), b, 2 ** K)] + [cert(t, P, c) for c in cs[1:]] + [dict(cert(t, P, cs[1]))]

        @case(f"s03_cube_on_other_residue_K{K}_m{m}k{k}", "not covered", m, k)
        def _(t, K=K):
            P = d2(t, 3); b, cs = t.skids(P, (), K)
            fr = t.free(P)
            other = fr[1:K + 1]
            oc = [tuple(sorted(zip(other, vs))) for vs in itertools.product((0, 1), repeat=K)]
            return background(t, P) + [split(P, (), b, 2 ** K)] + [cert(t, P, c) for c in cs[1:]] + [cert(t, P, oc[0])]

        @case(f"s04_complete_K{K}_m{m}k{k}", "covered", m, k)
        def _(t, K=K):
            P = d2(t, 3); b, cs = t.skids(P, (), K)
            return background(t, P) + [split(P, (), b, 2 ** K)] + [cert(t, P, c) for c in cs]

        @case(f"s05_sigma_cubes_implied_missing_K{K}_m{m}k{k}", "not covered", m, k)
        def _(t, K=K):
            P = d2(t, 3); b, cs = t.skids(P, (), K)
            return background(t, P) + [sc(t, P, c) for c in cs[:-1]]

        @case(f"s06_sigma_cubes_implied_ok_K{K}_m{m}k{k}", "covered", m, k)
        def _(t, K=K):
            P = d2(t, 3); b, cs = t.skids(P, (), K)
            return background(t, P) + [sc(t, P, c) for c in cs]

for (m, k) in [(7, 6)]:  # m = 6 has too few free residues for a nested K = 2 split
    @case(f"s07_nested_missing_m{m}k{k}", "not covered", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 2)
        recs = background(t, P) + [split(P, (), b, 4)] + [cert(t, P, c) for c in cs[1:]]
        b2, cs2 = t.skids(P, cs[0], 2)
        return recs + [split(P, cs[0], b2, 4)] + [cert(t, P, c) for c in cs2[:-1]]

    @case(f"s08_nested_ok_m{m}k{k}", "covered", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 2)
        recs = background(t, P) + [split(P, (), b, 4)] + [cert(t, P, c) for c in cs[1:]]
        b2, cs2 = t.skids(P, cs[0], 2)
        return recs + [split(P, cs[0], b2, 4)] + [cert(t, P, c) for c in cs2]

    @case(f"s09_nested_wrong_bits_m{m}k{k}", "reject", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 2)
        recs = background(t, P) + [split(P, (), b, 4)] + [cert(t, P, c) for c in cs[1:]]
        b2, cs2 = t.skids(P, cs[0], 2)
        return recs + [split(P, cs[0], b, 4)] + [cert(t, P, c) for c in cs2]  # reuses the parent's bits

for (m, k) in [(6, 6), (7, 6)]:
    @case(f"s10_finer_cubes_only_m{m}k{k}", "not covered*", m, k)
    def _(t):
        # record says K = 1, but the cubes certified are the K = 2 cubes (all 4): finer than the split
        P = d2(t, 3); b, cs = t.skids(P, (), 1); b2, cs2 = t.skids(P, (), 2)
        return background(t, P) + [split(P, (), b, 2)] + [cert(t, P, c) for c in cs2]

    @case(f"s11_cube_layer_child_dropped_conflict_ok_m{m}k{k}", "covered", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 1)
        recs = background(t, P) + [split(P, (), b, 2), cert(t, P, cs[0])]
        ch = t.ckids(P, cs[1])
        return recs + [split(P, cs[1], n=len(ch))] + [cert(t, c, cs[1]) for c in ch]

    @case(f"s12_cube_layer_child_nonconflict_dropped_m{m}k{k}", "not covered", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 1)
        recs = background(t, P) + [split(P, (), b, 2), cert(t, P, cs[0])]
        ch = t.ckids(P, cs[1])
        r = b[0]
        # drop a child whose newest layer is a one-orbit layer {r} (never conflicts)
        drop = next(c for c in ch if c[-1] == ((r, None),))
        return recs + [split(P, cs[1], n=len(ch))] + [cert(t, c, cs[1]) for c in ch if c != drop]

for (m, k) in [(6, 6), (7, 6)]:
    pass


# ---------- mixed layer and sigma routes, neither complete ----------
for (m, k) in [(6, 6), (7, 6)]:
    @case(f"x01_mixed_union_covers_m{m}k{k}", "not covered*", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 1); r = b[0]
        recs = background(t, P) + [split(P, (), b, 2), cert(t, P, ((r, 0),))]
        ch = t.kids(P)
        X = next(c for c in ch if len(c[-1]) == 2 and (r, 0) in c[-1])
        return recs + [split(P, n=len(ch))] + [cert(t, c) for c in ch if c != X]

    @case(f"x02_mixed_union_hole_m{m}k{k}", "not covered", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 1); r = b[0]
        recs = background(t, P) + [split(P, (), b, 2), cert(t, P, ((r, 0),))]
        ch = t.kids(P)
        X = next(c for c in ch if len(c[-1]) == 2 and (r, 1) in c[-1])
        return recs + [split(P, n=len(ch))] + [cert(t, c) for c in ch if c != X]

    @case(f"x03_mixed_cube_layer_route_half_m{m}k{k}", "not covered", m, k)
    def _(t):
        # P__r1 has a layer split with half its children; the other half certified as plain nodes of P's layer route
        P = d2(t, 3); b, cs = t.skids(P, (), 1)
        recs = background(t, P) + [split(P, (), b, 2), cert(t, P, cs[0])]
        ch = t.ckids(P, cs[1]); h = len(ch) // 2
        return recs + [split(P, cs[1], n=len(ch))] + [cert(t, c, cs[1]) for c in ch[:h]] + [cert(t, c) for c in ch[h:]]

    @case(f"x04_two_sigma_splits_each_incomplete_m{m}k{k}", "not covered", m, k)
    def _(t):
        # sigma_cubes cubes on residues (a) and a split record on (a, b): neither complete
        P = d2(t, 3); b1, cs1 = t.skids(P, (), 1); b2, cs2 = t.skids(P, (), 2)
        return background(t, P) + [sc(t, P, cs1[0])] + [split(P, (), b2, 4)] + [cert(t, P, c) for c in cs2 if c[0] != cs1[0][0]][:1]

# ---------- sigma_cubes records mixed into a close_tree OUT file ----------
for (m, k) in [(6, 6)]:
    @case(f"o01_sigma_cubes_completes_split_m{m}k{k}", "covered", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 2)
        return background(t, P) + [split(P, (), b, 4)] + [cert(t, P, c) for c in cs[:2]] + [sc(t, P, c) for c in cs[2:]]

    @case(f"o02_sigma_cubes_on_cube_node_m{m}k{k}", "reject", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 2)
        r = sc(t, P, cs[0]); r["node"] = nm(P, cs[0])
        return background(t, P) + [split(P, (), b, 4)] + [cert(t, P, c) for c in cs[1:]] + [r]

    @case(f"o03_sigma_cubes_empty_cube_m{m}k{k}", "reject", m, k)
    def _(t):
        P = d2(t, 3)
        r = dict(cert(t, P), cube={})
        return background(t, P) + [r]

    @case(f"o04_sigma_cubes_value2_m{m}k{k}", "reject", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 1)
        r = sc(t, P, cs[0]); r["cube"] = {str(b[0]): 2}
        return background(t, P) + [r, sc(t, P, cs[1])]

    @case(f"o05_sigma_cubes_with_plain_sha_m{m}k{k}", "reject", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 1)
        r = sc(t, P, cs[0]); r["cnf_sha256"] = t.sha(P)
        return background(t, P) + [r, sc(t, P, cs[1])]

    @case(f"o06_sigma_cubes_record_looks_split_m{m}k{k}", "not covered", m, k)
    def _(t):
        # a sigma_cubes record that is not certified but carries split: true (meta-like); one cube missing
        P = d2(t, 3); b, cs = t.skids(P, (), 1)
        r = {"node": nm(P), "cube": {str(b[0]): 1}, "split": True, "children": 0}
        return background(t, P) + [sc(t, P, cs[0]), r]

# ---------- forged sha values ----------
for (m, k) in [(6, 6)]:
    def _forge(t, f):
        P = d2(t, 3); b, cs = t.skids(P, (), 1)
        recs = background(t, P) + [split(P, (), b, 2), cert(t, P, cs[0]), cert(t, P, cs[1])]
        f(t, P, cs, recs); return recs

    for nmx, fx in [
        ("sibling_sha", lambda t, P, cs, R: R[-1].update(cnf_sha256=t.sha(P, cs[0]))),
        ("parent_sha_on_cube", lambda t, P, cs, R: R[-1].update(cnf_sha256=t.sha(P))),
        ("upper_hex", lambda t, P, cs, R: R[-1].update(cnf_sha256=R[-1]["cnf_sha256"].upper())),
        ("missing_sha", lambda t, P, cs, R: R[-1].pop("cnf_sha256")),
        ("dup_record_bad_sha", lambda t, P, cs, R: R.append(dict(R[-1], cnf_sha256="0" * 64))),
        ("unsorted_cube_sha", lambda t, P, cs, R: R.append(dict(CERT, node=nm(P, ((5, 0), (1, 1))) if t.m > 5 else nm(P), cnf_sha256="1" * 64))),
        ("wrong_base_sha_field", lambda t, P, cs, R: R[-1].update(base_sha256="ab" * 32)),
    ]:
        @case(f"f_{nmx}_m{m}k{k}", "reject", m, k)
        def _(t, fx=fx):
            return _forge(t, fx)

    @case(f"f_sha_of_other_base_m{m}k{k}", "reject", m, k)
    def _(t):
        t2 = T(7, 6) if t.m != 7 else T(6, 6)
        P = d2(t, 3); b, cs = t.skids(P, (), 1)
        recs = background(t, P) + [split(P, (), b, 2), cert(t, P, cs[0])]
        r = cert(t, P, cs[1]); h = hashlib.sha256(); h.update(b"x"); r["cnf_sha256"] = h.hexdigest()
        return recs + [r]

# ---------- sigma split at depth 1 ----------
for (m, k) in [(6, 6), (7, 7)]:
    @case(f"d01_sigma_record_H3_m{m}k{k}", "reject", m, k)
    def _(t):
        H3 = t.kids(())[0]; b, cs = t.skids(H3, (), 2)
        recs = [x for x in background(t, None) if x.get("node") != nm(H3)]
        return recs + [split(H3, (), b, 4)] + [cert(t, H3, c) for c in cs]

    @case(f"d02_sigma_cubes_only_H3_m{m}k{k}", "not covered*", m, k)
    def _(t):
        H3 = t.kids(())[0]; b, cs = t.skids(H3, (), 2)
        recs = [x for x in background(t, None) if not x.get("node", "").startswith(nm(H3) + "_")]
        recs = [x for x in recs if x.get("node") != nm(H3)]
        return recs + [sc(t, H3, c) for c in cs]

    @case(f"d03_cube_layer_split_at_depth1_m{m}k{k}", "not covered*", m, k)
    def _(t):
        # cubes of H3 with rule-3 layer splits, but no admissible sigma split of H3 (forbidden at depth 1)
        H3 = t.kids(())[0]; b, cs = t.skids(H3, (), 1)
        recs = [x for x in background(t, None) if not x.get("node", "").startswith(nm(H3))]
        for c in cs:
            ch = [x for x in t.kids(H3)]
            ch = [x for x in t.ckids(H3, c)]
            recs += [split(H3, c, n=len(ch))] + [cert(t, x, c) for x in ch]
        return recs

    if k >= 7:
        @case(f"d04_sigma_record_H6_m{m}k{k}", "reject", m, k)
        def _(t):
            H6 = t.kids(())[1]; b, cs = t.skids(H6, (), 1)
            recs = [x for x in background(t, None) if not x.get("node", "").startswith(nm(H6))]
            return recs + [split(H6, (), b, 2)] + [cert(t, H6, c) for c in cs]

# ---------- names ----------
for (m, k) in [(6, 6)]:
    @case(f"n01_unsorted_layer_name_m{m}k{k}", "either", m, k)
    def _(t):
        P = d2(t, 3)
        rev = tuple(tuple(reversed(X)) for X in P)
        return background(t, P) + [dict(CERT, node=nm(rev), cnf_sha256=t.sha(rev))] if nm(rev) != nm(P) else None

    @case(f"n02_cube_residue0_m{m}k{k}", "not covered", m, k)
    def _(t):
        # cubes on residue 0 (sigma_0 is fixed 0 by the base): P__0s0 and P__0s1 do not form a split
        P = d2(t, 3)
        return background(t, P) + [sc(t, P, ((0, 0),)), sc(t, P, ((0, 1),))]

    @case(f"n03_cube_on_layer_residue_m{m}k{k}", "not covered", m, k)
    def _(t):
        P = d2(t, 3); r = P[1][0][0]
        return background(t, P) + [sc(t, P, ((r, 0),)), sc(t, P, ((r, 1),))]

    @case(f"n04_dup_residue_in_cube_m{m}k{k}", "reject", m, k)
    def _(t):
        P = d2(t, 3); b, cs = t.skids(P, (), 1)
        return background(t, P) + [split(P, (), b, 2), cert(t, P, cs[0]), dict(CERT, node=nm(P, cs[1]) + "-" + nm((), cs[1])[2:], cnf_sha256="0" * 64)]


def brute(t, recs):
    leaves = {}
    for r in recs:
        if r.get("certified") is True and r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT":
            try:
                lay, _, cub = r["node"].partition("__")
                L = tuple(tuple(sorted((int(x.split("s")[0]), int(x.split("s")[1]) if "s" in x else None) for x in X.split("-"))) for X in lay.split("_"))
                C = tuple((int(x.split("s")[0]), int(x.split("s")[1])) for x in cub.split("-")) if cub else ()
                if "cube" in r: C = tuple(sorted((int(a), v) for a, v in r["cube"].items()))
                if len({a for a, _ in C}) != len(C) or list(C) != sorted(C): continue
            except Exception:
                continue
            leaves.setdefault(L, []).append(dict(C))
    holes = []

    def dfs(P, U):
        if P:
            U = [s for s in U if not any(all(s[r] == v for r, v in C.items()) for C in leaves.get(P, []))]
        if not U: return
        ch = t.kids(P)
        if not ch: holes.append(nm(P)); return
        for c in ch:
            dfs(c, [s for s in U if all(v is None or r == 0 or s[r] == v for r, v in c[-1])])
    dfs((), [(0,) + v for v in itertools.product((0, 1), repeat=t.m - 1)])
    return holes


def run_comp(t, who, path):
    x = subprocess.run([sys.executable, os.path.join(HERE, "runcomp.py"), who, str(t.m), str(t.k), t.base, path], capture_output=True, text=True)
    try:
        j = json.loads(x.stdout.strip().splitlines()[-1])
    except Exception:
        return "crash", {"stderr": x.stderr[-200:]}
    if j.get("reject"): return "reject", j
    return ("covered" if j["covered"] else "not covered"), j


TS = {}
summary = {"cases": 0, "pass": {c: 0 for c in COMPS}, "fail": {c: [] for c in COMPS}, "unsound": {c: [] for c in COMPS}}
for name, expect, m, k, f in CASES:
    t = TS.setdefault((m, k), T(m, k))
    recs = f(t)
    if recs is None: continue
    p = os.path.join(OUT, name + ".jsonl")
    open(p, "w").write("".join(json.dumps(r) + "\n" for r in recs))
    holes = brute(t, recs)
    row = {"case": name, "expect": expect, "records": len(recs), "brute_holes": len(holes)}
    summary["cases"] += 1
    for c in COMPS:
        v, j = run_comp(t, c, p)
        row[c] = v
        row[c + "_frontier"] = j.get("frontier_n")
        ok = v == expect.rstrip("*") or (expect == "either" and v in ("covered", "not covered"))
        if ok: summary["pass"][c] += 1
        else: summary["fail"][c].append(name)
        if v == "covered" and holes: summary["unsound"][c].append(name)
    print(json.dumps(row), flush=True)
print(json.dumps(summary))
