"""Write the exact sign table for refdp.c, validate refdp.c against the Python DPs, and run k=10."""
import struct, subprocess, sys, random, os
from fractions import Fraction
from rg import orient, sgn, max_convex_cupcap, max_convex_angular, count_convex_cupcap

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "refdp")


def write_table(pts, path):
    P = sorted(pts)
    n = len(P)
    order = sorted(range(n), key=lambda i: (P[i][1], P[i][0]))
    yr = [0] * n
    for r, i in enumerate(order):
        yr[i] = r
    buf = bytearray(n * n * n)
    for i in range(n):
        pi = P[i]
        for j in range(n):
            if j == i:
                continue
            pj = P[j]
            ax = pj[0] - pi[0]; ay = pj[1] - pi[1]
            base = (i * n + j) * n
            for l in range(n):
                if l == i or l == j:
                    continue
                pl = P[l]
                v = ax * (pl[1] - pi[1]) - ay * (pl[0] - pi[0])
                buf[base + l] = 1 if v > 0 else (255 if v < 0 else 0)
    with open(path, "wb") as f:
        f.write(struct.pack("<i", n))
        f.write(struct.pack("<%di" % n, *yr))
        f.write(bytes(buf))


def run_c(pts, path, counts=False):
    write_table(pts, path)
    out = subprocess.run([EXE, path, "1" if counts else "0"], capture_output=True, text=True, check=True).stdout
    return out.strip()


def validate(trials, seed):
    from test_rg import rand_set
    rng = random.Random(seed)
    bad = 0
    tmp = os.path.join(HERE, "tmp_tab.bin")
    for t in range(trials):
        n = rng.randint(5, 26)
        pts = rand_set(rng, n, t % 3)
        out = run_c(pts, tmp, counts=True)
        m1, _ = max_convex_cupcap(pts)
        m2 = max_convex_angular(pts)
        cd = count_convex_cupcap(pts)
        exp = "N=%d max_cupcap=%d max_angular=%d counts:%s" % (n, m1, m2, "".join(" %d:%d" % (s, c) for s, c in cd.items()))
        if out != exp:
            bad += 1
            print("MISMATCH", out, "|", exp)
    print("refdp.c validation: trials=%d mismatches=%d" % (trials, bad))


if __name__ == "__main__":
    if sys.argv[1] == "validate":
        validate(int(sys.argv[2]), int(sys.argv[3]))
    elif sys.argv[1] == "k10":
        from rconstruct import build, base_abscissae
        from rhyp import check
        k = 10
        for E in [int(v) for v in sys.argv[2].split(",")]:
            cl, info = build(k, E)
            pts = [p for B in cl for p in B]
            S = set(pts)
            rep = check(cl, k, base_abscissae(k))
            print("k=10 E=%d N=%d sym=%s 0notin=%s fails=%s H3cnt=%d H4cnt=%d" % (
                E, len(pts), all((-x, -y) in S for (x, y) in pts), (0, 0) not in S,
                [h for h in ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'GP'] if not rep[h]] or 'none',
                rep['H3_count'], rep['H4_count']))
            sys.stdout.flush()
            if rep['H0'] and rep['GP']:
                print("   ", run_c(pts, os.path.join(HERE, "k10_tab.bin"), counts=(len(sys.argv) > 3)))
            sys.stdout.flush()
