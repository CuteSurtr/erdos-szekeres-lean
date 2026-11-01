#!/usr/bin/env python3
"""Self-test of check_even_sector.py: each mutation must make it fail (an AssertionError)."""
import os, sys, platform
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_even_sector as M

orig_pattern, orig_sector, orig_label = M.encoder_pattern, M.in_open_sector, M.label


def run(name):
    try:
        M.main()
    except AssertionError as e:
        print(f"mutation {name}: caught (AssertionError {str(e)[:80]!r})")
        return True
    print(f"mutation {name}: NOT caught")
    return False


ok = True
# 1. flipped sector pattern
M.encoder_pattern = lambda m: [-s for s in orig_pattern(m)]
ok &= run("flipped pattern")
M.encoder_pattern = orig_pattern
# 2. closed sector (boundary rays admitted): must break the grid equivalence (4) or (1b)
M.in_open_sector = lambda p, O0, m: (M.det(M.C, O0[0], p) >= 0) if m == 2 else (M.det(M.C, O0[0], p) >= 0 and M.det(M.C, p, O0[1]) > 0)
ok &= run("half-open sector")
M.in_open_sector = orig_sector
# 3. clockwise labelling of the inner orbits (R^-1) -> encoder units must be violated
def label_cw(orbs, o0, i0, m, pat, order):
    lab = orig_label(orbs, o0, i0, m, pat, order)
    t = len(lab) // m
    out = lab[:m]
    for o in range(1, t):
        blk = lab[o * m:(o + 1) * m]
        out.extend([blk[0]] + blk[1:][::-1])
    return out
M.label = label_cw
ok &= run("clockwise inner orbits")
M.label = orig_label
print("python", platform.python_version(), "| all mutations caught:", ok)
# 4. pattern_ok with the j = 0 sign flipped (bypasses check 1a): must break (1b)
orig_pok = M.pattern_ok
M.pattern_ok = lambda p, O0, m, pat: orig_pok(p, O0, m, [-pat[0]] + pat[1:])
ok &= run("pattern_ok j=0 flipped")
M.pattern_ok = orig_pok
print("python", platform.python_version(), "| all mutations caught (incl. 4):", ok)
