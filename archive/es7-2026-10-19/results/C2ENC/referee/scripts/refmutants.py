"""Referee's additional mutants of zcnf.py (exact text replacements, each old string must occur exactly once).

Used two ways:
  python3 -I refmutants.py write OUTDIR       -> writes OUTDIR/<name>/zcnf_mut.py for every mutant below
  (the copied harness imports NEW_MUTANTS from here to extend mutate.MUTANTS)
"""
import os
import sys

NEW_MUTANTS = {
    "uf_compress": ("union-find path compression stores the x-to-root sign at every node of the path",
                    [("self.par[y] = (root, sy)", "self.par[y] = (root, s)")]),
    "gp_generic_polarity": ("GP generic path ignores literal polarity (affects 5-sets with a zero term, i.e. with c)",
                            [("v1 = 1 if (val[abs(l1)] == (l1 > 0)) else -1", "v1 = 1 if val[abs(l1)] else -1")]),
    "gp_fast_sign": ("GP fast path: one sign flipped in the first clause (forbids the valid product pattern +,-,+)",
                     [("self.sink.add([-s1 * l12, -s1 * l34, -s2 * l13, s2 * l24, -s3 * l14, -s3 * l23])",
                       "self.sink.add([-s1 * l12, -s1 * l34, -s2 * l13, -s2 * l24, -s3 * l14, -s3 * l23])")]),
    "hull_orient": ("hull clause uses chi(a,d,X0) instead of chi(d,a,X0)",
                    [("-s * self.lit(b, d, q), -s * self.lit(d, a, q)]",
                      "-s * self.lit(b, d, q), -s * self.lit(a, d, q)]")]),
    "parity": ("parity_sort counts only two of the three inversions",
               [("inv = (a > b) + (a > c) + (b > c)\n    return (tuple(sorted(t)), -1 if inv & 1 else 1)",
                 "inv = (a > b) + (b > c)\n    return (tuple(sorted(t)), -1 if inv & 1 else 1)")]),
    "identity_sign_p0": ("centre identity with the wrong sign for p = 0 only",
                         [("""                sp = 1
                base = (tp, p)            # chi(Z,p,q) = chi(tau p, p, q)""",
                           """                sp = -1 if p == 0 else 1
                base = (tp, p)            # chi(Z,p,q) = chi(tau p, p, q)""")]),
    "a4_sign_Z": ("interiority clause with the wrong sign, only on 4-sets containing c",
                  [("cl = [-s * self.lit(t, q, r), -s * self.lit(p, t, r), -s * self.lit(p, q, t), s * self.lit(p, q, r)]",
                    "cl = [-s * self.lit(t, q, r), -s * self.lit(p, t, r), -s * self.lit(p, q, t), "
                    "(-s if self.Z in S else s) * self.lit(p, q, r)]")]),
    # sound controls (must NOT be flagged by the semantic tests; the spec comparison may flag them)
    "ctl_hull_X1": ("sound control: hull clauses anchored at (0,1) = h(X0), also a hull vertex",
                    [("""        q = self.pt(0, 0)
        cnt = 0""", """        q = self.pt(0, 1)
        cnt = 0""")]),
    "ctl_hull_withZ": ("sound control: hull triangles may also use c as a vertex (X0 is an extreme point)",
                       [("for a, b, d in itertools.combinations([x for x in range(self.N) if x != q], 3):",
                         "for a, b, d in itertools.combinations([x for x in range(self.N + 1) if x != q], 3):")]),
}


def apply(src, name):
    for old, new in NEW_MUTANTS[name][1]:
        assert src.count(old) == 1, (name, old[:70], src.count(old))
        src = src.replace(old, new)
    return src


if __name__ == "__main__":
    assert sys.argv[1] == "write"
    out = sys.argv[2]
    orig = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tests", "zcnf_orig.py")
    src = open(orig).read()
    for name in NEW_MUTANTS:
        d = os.path.join(out, name)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "zcnf_mut.py"), "w") as f:
            f.write(apply(src, name))
        print("wrote", name)
