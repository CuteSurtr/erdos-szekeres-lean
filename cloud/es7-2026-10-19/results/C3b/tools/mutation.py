#!/usr/bin/env python3
"""Mutation test: does validate.py detect deliberately broken encodings?
Each mutant is written to its own CNF dir and validated on m=3..7, k=5,6,7."""
import os
import subprocess
import sys
import gen_c3b as G

HERE = os.path.dirname(os.path.abspath(__file__))


def mut_inv(self, a, b, c):          # chi' sign flipped in the inv prefix rule only
    return -G.Enc.chip_orig(self, a, b, c)


MUTANTS = {}


def make(name, m, k, d):
    e = G.Enc(m, k)
    if name == "inv_sign":
        orig = e.chip
        import itertools
        # rebuild with flipped chi' only inside inv_cl: wrap build
        def build():
            G.Enc.build(e)
        e.build()
        # flip: rewrite INV clauses by negating the first literal of the 4 prefix clauses/triple
        g = [x for x in e.groups if x[0] == "INV"][0]
        n3 = (e.n * (e.n - 1) * (e.n - 2)) // 6 * 4
        for i in range(g[1], g[1] + n3):
            e.cls[i][0] = -e.cls[i][0]
    elif name == "no_leftturn":
        orig = e.chis
        e.build()
        g = [x for x in e.groups if x[0] == "KGON"][0]
        for i in range(g[1], g[1] + g[2]):
            cl = e.cls[i]
            if len(cl) >= 4 and cl[0] < 0 and abs(cl[0]) > e.nprim:
                e.cls[i] = [cl[0]] + cl[2:]
    elif name == "no_right":
        e.build()
        g = [x for x in e.groups if x[0] == "KGON"][0]
        for i in range(g[1], g[1] + g[2]):
            cl = e.cls[i]
            if abs(cl[0]) > e.nprim:
                e.cls[i] = cl[:3] + cl[4:]
    elif name == "xor_parity":
        e.sig = lambda i, e=e: (e.s[i % e.m], 1 if i // e.m == 2 else 0)
        e.build()
    elif name == "reflect_R":
        e.R = [(i + m) % e.n for i in range(e.n)]
        e2 = G.Enc.__new__(G.Enc)
        e.build()
    e.write(os.path.join(d, f"c3b_m{m}k{k}.cnf"), os.path.join(d, f"c3b_m{m}k{k}.json"))


def main():
    names = sys.argv[1:] or ["inv_sign", "no_leftturn", "no_right", "xor_parity"]
    for name in names:
        d = f"/tmp/claude-0/mut_{name}"
        os.makedirs(d, exist_ok=True)
        for m in range(3, 8):
            for k in (5, 6, 7):
                make(name, m, k, d)
        r = subprocess.run([sys.executable, os.path.join(HERE, "validate.py"), "60", "99",
                            "--mmax", "7"], env=dict(os.environ, C3B_CNFDIR=d),
                           capture_output=True, text=True)
        last = r.stdout.strip().splitlines()[-1]
        print(name, "detected" if r.returncode else "NOT DETECTED", last[:300], flush=True)


if __name__ == "__main__":
    main()
