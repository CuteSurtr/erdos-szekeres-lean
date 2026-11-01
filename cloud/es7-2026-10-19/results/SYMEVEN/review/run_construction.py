"""Scan eps = 1/E for the construction as written; check everything exactly with referee code."""
import sys, time
from math import comb
from rconstruct import G, check_G, middle_set, verify_middle, build, base_abscissae
from rhyp import check
from rg import max_convex_cupcap, max_convex_angular, convex_position_bf, count_convex_cupcap


def ingredients(k):
    m = k // 2
    print("== k=%d ingredients" % k)
    for j in range(k - 1):
        a, b = j + 2, k - j
        P = G(a, b)
        lc, lk = check_G(a, b, P)
        print("  G(%d,%d): size %d = C(%d,%d); longest cup %d (< %d), longest cap %d (< %d)"
              % (a, b, len(P), a + b - 4, a - 2, lc, a, lk, b))
    M0, t = middle_set(m)
    rep = verify_middle(m, M0)
    print("  M0 (m=%d, t=%s): %s" % (m, t, rep))


def scan(k, Es, mid_pow=2, count=False, label="written"):
    n = k - 2
    xs = base_abscissae(k)
    print("== k=%d scan (%s, middle scale eps^%d)" % (k, label, mid_pow))
    for E in Es:
        t0 = time.time()
        cl, info = build(k, E, mid_scale_pow=mid_pow)
        pts = [p for B in cl for p in B]
        S = set(pts)
        sym = all((-x, -y) in S for (x, y) in pts)
        rep = check(cl, k, xs)
        if len(S) < len(pts) or not rep['H0'] or not rep['GP']:
            print("  E=%-6d degenerate (coincident points / equal x / collinear): H0=%s GP=%s distinct=%s"
                  % (E, rep['H0'], rep['GP'], len(S) == len(pts)))
            continue
        m1, w1 = max_convex_cupcap(pts)
        m2 = max_convex_angular(pts)
        wit_ok = convex_position_bf(w1) and len(w1) == m1
        extra = ""
        if count:
            extra = " counts=%s" % count_convex_cupcap(pts)
        fails = [h for h in ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'GP'] if not rep[h]]
        print("  E=%-6d N=%d (2^%d=%d) sym=%s 0notin=%s | fails=%s | H3 cnt=%d H4 cnt=%d (zero-sum skipped %d)"
              " | maxconvex cupcap=%d angular=%d witness_ok=%s%s  [%.1fs]"
              % (E, len(pts), k - 2, 2 ** (k - 2), sym, (0, 0) not in S, fails or "none",
                 rep['H3_count'], rep['H4_count'], rep['H4_zero_sum_skipped'], m1, m2, wit_ok, extra,
                 time.time() - t0))
        sys.stdout.flush()


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "ingredients":
        for k in (6, 8, 10):
            ingredients(k)
    elif which == "scan6":
        scan(6, [1, 2, 4, 8, 16, 32, 64, 128, 1024, 10 ** 6], count=True)
    elif which == "scan8":
        scan(8, [int(v) for v in sys.argv[2].split(",")], count=(len(sys.argv) > 3))
