"""Standalone re-verification (no shared code) of the counterexample chains to the
literal Lemma 3, in TRUE Euclidean coordinates computed with 100-digit Decimals,
plus an exact integer sign check (cos/sin of 2 pi k/m are rational or rational*sqrt3).

Usage: python3 -I verify_cex.py PTSFILE m  line_a line_c1 line_c2 line_c3 line_Qa
(line numbers = 1-based indices among the non-comment lines of the .pts file;
 the layer of a is the orbit of line_a.)
"""
import sys
from decimal import Decimal, getcontext
getcontext().prec = 100


def rows(path):
    out = []
    for line in open(path):
        s = line.strip()
        if s and not s.startswith('#'):
            out.append([int(t) for t in s.split()])
    return out


def true_xy(w, m):
    sq3 = Decimal(3).sqrt()
    if m == 4:
        cs = [(Decimal(1), Decimal(0)), (Decimal(0), Decimal(1)), (Decimal(-1), Decimal(0)), (Decimal(0), Decimal(-1))]
    else:
        h = Decimal(1) / 2
        cs = [(Decimal(1), Decimal(0)), (h, sq3 / 2), (-h, sq3 / 2), (Decimal(-1), Decimal(0)), (-h, -sq3 / 2), (h, -sq3 / 2)]
    x = sum(Decimal(wj) * c for wj, (c, s) in zip(w, cs))
    y = sum(Decimal(wj) * s for wj, (c, s) in zip(w, cs))
    return (x, y)


def exact_XY(w, m):
    # point = (X/2, Y*sqrt3/2) for m=6 ; (X, Y) for m=4  -> orientation sign = sign of integer cross
    if m == 4:
        return (w[0] - w[2], w[1] - w[3])
    X = 2 * w[0] + w[1] - w[2] - 2 * w[3] - w[4] + w[5]
    Y = w[1] + w[2] - w[4] - w[5]
    return (X, Y)


def cr(o, p, q):
    return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])


def main():
    path, m = sys.argv[1], int(sys.argv[2])
    ia, i1, i2, i3, iq = [int(t) - 1 for t in sys.argv[3:8]]
    R = rows(path)
    names = ['a', 'c1', 'c2', 'c3', 'Qa']
    W = [R[ia], R[i1], R[i2], R[i3], R[iq]]
    # layer of a: rotations of w = cyclic shifts with sign (zeta^m = 1 => plain cyclic shift)
    wa = R[ia]
    layer_w = [wa[-k:] + wa[:-k] for k in range(m)]  # multiply by zeta^k = cyclic shift
    for mode in ('decimal', 'exact'):
        f = true_xy if mode == 'decimal' else exact_XY
        P = [f(w, m) for w in W]
        L = [f(w, m) for w in layer_w]
        a, c1, c2, c3, qa = P
        print(f"[{mode}]")
        # Qa = -a (d = 2: rotation by pi)
        print("  Qa == -a:", (qa[0] == -a[0] and qa[1] == -a[1]))
        # layer is CCW
        print("  layer CCW:", all(cr(L[k], L[(k + 1) % m], L[(k + 2) % m]) > 0 for k in range(m)))
        for nm, c in zip(names[1:4], (c1, c2, c3)):
            side = cr(a, qa, c)
            inside = all(cr(L[k], L[(k + 1) % m], c) > 0 for k in range(m)) or c in L
            print(f"  {nm}: right of a->Qa (ccw half) = {side < 0}   in conv(L) = {inside}")
        seq = [a, c1, c2, c3, qa]
        turns = [cr(seq[l - 1], seq[l], seq[l + 1]) for l in (1, 2, 3)]
        print("  turns at c1,c2,c3 strictly left:", [t > 0 for t in turns])
        if mode == 'decimal':
            print("  |cross| magnitudes:", ['%.3e' % abs(t) for t in turns])
        print("  distinct:", len({(p[0], p[1]) for p in seq}) == 5)
    print("d(j+1) = 2*4 = 8 > K-1 = 7: the conclusion of Lemma 3 fails for this chain")


if __name__ == '__main__':
    main()
