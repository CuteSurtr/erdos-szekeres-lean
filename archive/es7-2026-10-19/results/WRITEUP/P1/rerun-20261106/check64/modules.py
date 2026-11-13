#!/usr/bin/env python3
"""Line-modules (C such that no line through two points of S minus C separates two points of C).

Exact orientation table from z7exact.  Enumeration of all modules C with 2 <= |C| <= B (B <= n-3):
partition by the two smallest labels x < y of C; branch on violating lines with propagation:
 * convex closure: if |S - C| >= 2, every point of S inside conv(C) is in C (else a line through it and
   another outside point would split C);
 * a violating line (a, b) (a, b not in C, line splits C) forces a in C or b in C.
Validated against brute force (all subsets) on random small subsets (--selftest).
usage: modules.py FILE B [--selftest]
"""
import sys, itertools, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import z7exact as Z

sys.setrecursionlimit(10000)


def make_O(pts):
    return Z.orient_table(pts)


def is_module(O, S, C):
    Cs = set(C)
    D = [a for a in S if a not in Cs]
    C = list(C)
    for a, b in itertools.combinations(D, 2):
        Oab = O[a][b]
        s = Oab[C[0]]
        for c in C[1:]:
            if Oab[c] != s:
                return False
    return True


def enum_modules(O, S, B):
    S = sorted(S)
    n = len(S)
    assert B <= n - 3
    found = set()
    pos = {v: i for i, v in enumerate(S)}

    def inside_hull(In):
        # points of S \ In strictly inside conv(In)
        res = []
        Inl = sorted(In)
        if len(Inl) < 3:
            return res
        tris = list(itertools.combinations(Inl, 3))
        for d in S:
            if d in In:
                continue
            for p, q, r in tris:
                s1 = O[p][q][d]
                if s1 == O[q][r][d] == O[r][p][d]:
                    res.append(d)
                    break
        return res

    def violating(In):
        Inl = sorted(In)
        c0 = Inl[0]
        out = [a for a in S if a not in In]
        for i in range(len(out)):
            a = out[i]
            Oa = O[a]
            for j in range(i + 1, len(out)):
                b = out[j]
                Oab = Oa[b]
                s = Oab[c0]
                for c in Inl[1:]:
                    if Oab[c] != s:
                        return (a, b)
        return None

    def search(In, Out, x, y, seen):
        key = (frozenset(In), frozenset(Out))
        if key in seen:
            return
        seen.add(key)
        # propagate convex closure
        while True:
            if len(In) > B:
                return
            add = inside_hull(In)
            if not add:
                break
            for d in add:
                if d in Out:
                    return
            In = In | set(add)
        if len(In) > B:
            return
        v = violating(In)
        if v is None:
            found.add(frozenset(In))
            # try to extend to larger modules with the same two smallest labels
            if len(In) < B:
                cand = [z for z in S if z not in In and z not in Out and z > y]
                # branch on candidates one at a time: z in, or z out (then next)
                Out2 = set(Out)
                for z in cand:
                    search(In | {z}, set(Out2), x, y, seen)
                    Out2.add(z)
            return
        a, b = v
        if a in Out and b in Out:
            return
        if a in Out:
            search(In | {b}, Out, x, y, seen)
            return
        if b in Out:
            search(In | {a}, Out, x, y, seen)
            return
        search(In | {a}, Out, x, y, seen)
        search(In | {b}, Out | {a}, x, y, seen)

    for i in range(n):
        x = S[i]
        for j in range(i + 1, n):
            y = S[j]
            Out = set(S[:j]) - {x}
            seen = set()
            search({x, y}, Out, x, y, seen)
    # all found sets must have x,y as two smallest; check and verify
    res = []
    for C in found:
        if is_module(O, S, C):
            res.append(tuple(sorted(C)))
        else:
            raise AssertionError('non-module recorded %r' % (sorted(C),))
    return sorted(set(res), key=lambda c: (len(c), c))


def brute_modules(O, S, B):
    S = sorted(S)
    res = []
    for k in range(2, B + 1):
        for C in itertools.combinations(S, k):
            if is_module(O, S, C):
                res.append(tuple(C))
    return res


if __name__ == '__main__':
    path = sys.argv[1]
    B = int(sys.argv[2])
    pts = Z.read_pts(path)
    O = make_O(pts)
    n = len(pts)
    if '--selftest' in sys.argv:
        random.seed(7)
        bad = 0
        for t in range(40):
            if t % 2 == 0:
                cl = random.randrange(7)
                base = [cl * 6 + i for i in range(6)] + [42 + cl * 3 + i for i in range(3)]
                rest = [z for z in range(n) if z not in base]
                S = sorted(base + random.sample(rest, 6))
            else:
                S = sorted(random.sample(range(n), 14))
            Bt = len(S) - 3
            a = enum_modules(O, S, Bt)
            b = brute_modules(O, S, Bt)
            if sorted(a) != sorted(b):
                bad += 1
                print('MISMATCH', S, len(a), len(b))
        print('selftest: 40 subsets, mismatches', bad)
    mods = enum_modules(O, list(range(n)), B)
    from collections import Counter
    cnt = Counter(len(c) for c in mods)
    print('file', path)
    print('line-modules with 2 <= size <= %d: %d; by size:' % (B, len(mods)), dict(sorted(cnt.items())))
    for c in mods:
        print(len(c), c)
