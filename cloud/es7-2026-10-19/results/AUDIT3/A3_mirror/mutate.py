#!/usr/bin/env python3
"""Sensitivity of myeval.py: build mutated copies of zcnf.py (in this audit directory only), generate a small mirror
instance with each, and run myeval.py.  Unsound mutations must be flagged; the sound weakening (M8) must pass."""
import os, subprocess, sys, json

O = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.environ.get("ES7_RESULTS", "."), "SYMZ/zcnf.py")
MUT = {
    "M1_pair_identity_reversed": ("base = (right, left)      # chi(Z,p,q) = chi(right, left, q) for both points of the pair",
                                  "base = (left, right)"),
    "M2_Z_group_sign": ("self.gsign = (-1, 1)", "self.gsign = (-1, -1)"),
    "M3_point_group_sign": ("self.gsign = (-1, 1)", "self.gsign = (1, 1)"),
    "M4_sb_reversed": ("u.append(self.lit(Z, self.pt(o, 0), self.pt(o2, 0)))\n            if self.axis == 2",
                       "u.append(self.lit(Z, self.pt(o2, 0), self.pt(o, 0)))\n            if self.axis == 2"),
    "M5_a4_sign": ("cl = [-s * self.lit(t, q, r), -s * self.lit(p, t, r), -s * self.lit(p, q, t), s * self.lit(p, q, r)]",
                   "cl = [-s * self.lit(t, q, r), -s * self.lit(p, t, r), s * self.lit(p, q, t), s * self.lit(p, q, r)]"),
    "M6_gp_middle_sign": ("((y[0], y[2]), (y[1], y[3]), -1)", "((y[0], y[2]), (y[1], y[3]), 1)"),
    "M7_axis_not_fixed": ("if i >= self.NP:                      # axis points and Z are fixed\n            return i",
                          "if i >= self.NP + self.axis:\n            return i\n        if i >= self.NP:\n            return self.NP + (self.axis - 1 - (i - self.NP))"),
    "M8_sound_weakening_no_axis_identity": ("            for q in range(self.N):\n                if q in (p, tp):",
                                            "            for q in range(self.NP):\n                if q in (p, tp):"),
    "M9_convex4_pattern_too_wide": ("if n_in == 0:\n            convex.append(pat)\n    assert len(convex) == 6",
                                    "if n_in <= 1:\n            convex.append(pat)\n    assert len(convex) >= 6"),
}


def main():
    os.makedirs(f"{O}/mut", exist_ok=True)
    src = open(SRC).read()
    out = {}
    for name, (old, new) in MUT.items():
        assert src.count(old) == 1, (name, src.count(old))
        path = f"{O}/mut/{name}.py"
        open(path, "w").write(src.replace(old, new))
        res = []
        for t, K, axis in ((6, 7, 1), (6, 6, 2), (6, 7, 0)):
            f = f"{O}/mut/{name}_t{t}k{K}a{axis}"
            g = subprocess.run([sys.executable, path, "mirror", str(t), str(K), "--axis", str(axis), "-o", f + ".cnf",
                                "--map", f + ".json"], capture_output=True, text=True)
            if g.returncode != 0:
                res.append(f"t{t}K{K}a{axis}: generator error: {g.stderr.strip().splitlines()[-1][:120]}")
                continue
            e = subprocess.run([sys.executable, f"{O}/myeval.py", f + ".cnf", f + ".json", str(t), str(K), str(axis),
                                "40", "11"], capture_output=True, text=True)
            first = e.stdout.strip().splitlines()[0] if e.stdout.strip() else "{}"
            try:
                fails = json.loads(first).get("failures")
            except Exception:
                fails = None
            res.append(f"t{t}K{K}a{axis}: evaluator exit {e.returncode}, failures {fails}"
                       + (f" ({e.stderr.strip().splitlines()[0][:110]})" if e.returncode and e.stderr.strip() else ""))
            os.remove(f + ".cnf")
        out[name] = res
        print(name)
        for r in res:
            print("   ", r)


if __name__ == "__main__":
    main()
