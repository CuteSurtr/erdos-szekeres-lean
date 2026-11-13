"""Write mutant copies of gen_b2.py into scratch/ (each replacement must occur exactly once).
Usage: python3 -I make_mutants.py <path to gen_b2.py>"""
import sys
src = open(sys.argv[1]).read()
muts = {
 "M1_permsign_const": ("                    s = -s\n", "                    s = s\n"),
 "M2_olit_sign_flip": ("                return v if sg > 0 else -v\n", "                return v if sg < 0 else -v\n"),
 "M3_olit_sort_unrotated": ("order = sorted(range(3), key=lambda r: rt[r])", "order = sorted(range(3), key=lambda r: tri[r])"),
 "M4_canon_max": ("if best is None or rt < best:", "if best is None or rt > best:"),
 "M5_canon_wrong_dir": ("    def canon(tri):              # tri: list of (i,k)\n        best = None\n        for (i0, k0) in tri:\n            s = (-k0) % m",
                        "    def canon(tri):              # tri: list of (i,k)\n        best = None\n        for (i0, k0) in tri:\n            s = (k0) % m"),
 "M6_angular_PAPAPA_flip": ("lit = v if sg > 0 else -v                          # orient", "lit = -v if sg > 0 else v                          # orient"),
 "M7_PPP_layer_cond": ("if b[0] <= a[0] and b[0] <= cc[0]:", "if b[0] >= a[0] and b[0] >= cc[0]:"),
}
for name, (a, b) in muts.items():
    assert src.count(a) == 1, (name, src.count(a))
    open(f"scratch/{name}.py", "w").write(src.replace(a, b))
print("ok", len(muts))
