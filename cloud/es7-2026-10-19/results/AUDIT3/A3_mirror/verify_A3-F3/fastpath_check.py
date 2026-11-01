#!/usr/bin/env python3
"""A3-F3 (d): are the 16 hand-written Grassmann-Pluecker clauses of zcnf.add_gp (the 'fast path', used when all three
products are nonzero and involve 6 distinct variables) exactly the clauses the generic enumeration path would write?
And does the auditor's mutation M6 (middle GP sign k = -1 -> +1) touch the fast path at all?

Part A (abstract, exhaustive): six literals on six distinct variables, every sign combination and every assignment of
          variable indices to the six positions; compare the fast-path clause set with the generic-path clause set
          (both transcribed from zcnf.py lines 239-257) and with the semantic definition 'forbid exactly the
          assignments where the three signed products are all equal'.
Part B (code-faithful): variants of a byte-identical copy of zcnf.py made by single text substitutions:
          nofast  : the fast-path condition is disabled (so every case goes through the generic enumeration);
          tagged  : fast-path clauses go to a separate list (the rest unchanged);
          m6      : the auditor's M6 mutation, on top of 'tagged'.
          For several small mirror instances compare the full clause multisets of original vs nofast, and the
          fast-path clause lists of tagged vs m6."""
import collections, importlib.util, itertools, os, sys

V = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(V, "zcnf_copy.py")          # sha256 13d6c162... = results/SYMZ/zcnf.py


# ---------------- Part A
def fast_clauses(l12, l34, l13, l24, l14, l23):
    out = []
    for s1, s2, s3 in itertools.product((1, -1), repeat=3):
        out.append([-s1 * l12, -s1 * l34, -s2 * l13, s2 * l24, -s3 * l14, -s3 * l23])
        out.append([-s1 * l12, s1 * l34, -s2 * l13, -s2 * l24, -s3 * l14, s3 * l23])
    return out


def generic_clauses(nz):
    out = []
    vars_ = sorted({abs(l) for tm in nz for l in tm[1]})
    for bits in itertools.product((True, False), repeat=len(vars_)):
        val = dict(zip(vars_, bits))
        sg = set()
        for k, (l1, l2) in nz:
            v1 = 1 if (val[abs(l1)] == (l1 > 0)) else -1
            v2 = 1 if (val[abs(l2)] == (l2 > 0)) else -1
            sg.add(k * v1 * v2)
        if not (1 in sg and -1 in sg):
            out.append([(-v if val[v] else v) for v in sorted(val)])
    return out


def semantic_forbidden(lits, ks):
    """set of forbidden total assignments (as frozenset of true literals) by the GP sign condition"""
    l12, l34, l13, l24, l14, l23 = lits
    vars_ = sorted({abs(l) for l in lits})
    forb = set()
    for bits in itertools.product((True, False), repeat=len(vars_)):
        val = dict(zip(vars_, bits))
        sig = lambda l: 1 if (val[abs(l)] == (l > 0)) else -1
        prods = [ks[0] * sig(l12) * sig(l34), ks[1] * sig(l13) * sig(l24), ks[2] * sig(l14) * sig(l23)]
        if len(set(prods)) == 1:
            forb.add(frozenset((v if val[v] else -v) for v in vars_))
    return forb


def clause_falsifiers(cl, vars_):
    """the unique total assignment falsifying a clause that mentions every variable once"""
    assert sorted(abs(l) for l in cl) == sorted(vars_)
    return frozenset(-l for l in cl)


def part_a():
    n = 0
    bad = 0
    for perm in itertools.permutations(range(1, 7)):
        for signs in itertools.product((1, -1), repeat=6):
            lits = [s * v for s, v in zip(signs, perm)]
            l12, l34, l13, l24, l14, l23 = lits
            F = {frozenset(c) for c in fast_clauses(*lits)}
            nz = [(1, (l12, l34)), (-1, (l13, l24)), (1, (l14, l23))]
            G = {frozenset(c) for c in generic_clauses(nz)}
            Sm = semantic_forbidden(lits, (1, -1, 1))
            Ff = {clause_falsifiers(c, perm) for c in fast_clauses(*lits)}
            n += 1
            if not (F == G and len(F) == 16 and Ff == Sm and len(Sm) == 16):
                bad += 1
    print(f"Part A: {n} literal configurations (720 index placements x 64 sign patterns); mismatches {bad}")
    return bad == 0


# ---------------- Part B
FAST_COND = "if all(tm is not None for tm in terms) and len({abs(l) for tm in terms for l in tm[1]}) == 6:"
FAST_ADD1 = "self.sink.add([-s1 * l12, -s1 * l34, -s2 * l13, s2 * l24, -s3 * l14, -s3 * l23])"
FAST_ADD2 = "self.sink.add([-s1 * l12, s1 * l34, -s2 * l13, -s2 * l24, -s3 * l14, s3 * l23])"
INIT = "self.sink = Sink(body)"
M6_OLD = "((y[0], y[2]), (y[1], y[3]), -1)"
M6_NEW = "((y[0], y[2]), (y[1], y[3]), 1)"


def variant(name, subs):
    src = open(SRC).read()
    for old, new in subs:
        assert src.count(old) == 1, (name, old, src.count(old))
        src = src.replace(old, new)
    path = os.path.join(V, f"variant_{name}.py")
    open(path, "w").write(src)
    spec = importlib.util.spec_from_file_location(f"variant_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(mod, t, K, axis, tag):
    body = os.path.join(V, f"tmp_{tag}_{t}_{K}_{axis}.body")
    out = os.path.join(V, f"tmp_{tag}_{t}_{K}_{axis}.cnf")
    enc = mod.ZEncoding("mirror", t, K, body=body, axis=axis)
    enc.build(sb=True, hull=False)
    info = enc.write(out, None, body)
    cls = collections.Counter()
    with open(out) as f:
        hdr = [next(f), next(f)]
        for line in f:
            cls[tuple(sorted(int(x) for x in line.split()[:-1]))] += 1
    os.remove(out)
    return enc, info, hdr[1].strip(), cls


def part_b():
    orig = variant("orig", [])
    nofast = variant("nofast", [(FAST_COND, "if False and " + FAST_COND[3:])])
    tag_subs = [(INIT, INIT + "\n        self.fastsink = []"),
                (FAST_ADD1, FAST_ADD1.replace("self.sink.add(", "self.fastsink.append(")),
                (FAST_ADD2, FAST_ADD2.replace("self.sink.add(", "self.fastsink.append("))]
    tagged = variant("tagged", tag_subs)
    m6 = variant("m6", tag_subs + [(M6_OLD, M6_NEW)])
    ok = True
    for t, K, axis in ((4, 5, 0), (4, 5, 1), (4, 5, 2), (5, 6, 0), (5, 6, 1), (5, 6, 2), (6, 7, 0), (6, 7, 1),
                       (6, 6, 2)):
        e0, i0, h0, c0 = build(orig, t, K, axis, "orig")
        e1, i1, h1, c1 = build(nofast, t, K, axis, "nofast")
        e2, i2, h2, c2 = build(tagged, t, K, axis, "tagged")
        e3, i3, h3, c3 = build(m6, t, K, axis, "m6")
        same_full = (c0 == c1 and h0 == h1)
        nf = len(e2.fastsink)
        fast_same_m6 = (sorted(map(tuple, e2.fastsink)) == sorted(map(tuple, e3.fastsink)))
        generic_diff_m6 = sum(((c2 - c3) + (c3 - c2)).values())
        tot = sum(c0.values())
        print(f"mirror t={t} K={K} axis={axis}: header {h0}; orig == nofast (clause multiset): {same_full}; "
              f"fast-path clauses {nf} of {tot} ({nf // 16} hits); "
              f"M6 leaves fast-path clauses unchanged: {fast_same_m6}; M6 changes {generic_diff_m6} non-fast clauses")
        ok &= same_full and fast_same_m6 and nf > 0 and generic_diff_m6 > 0
    for n in ("orig", "nofast", "tagged", "m6"):
        os.remove(os.path.join(V, f"variant_{n}.py"))
    return ok


if __name__ == "__main__":
    a = part_a()
    b = part_b()
    print("RESULT", "PASS" if (a and b) else "FAIL")
