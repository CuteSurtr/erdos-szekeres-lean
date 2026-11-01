#!/usr/bin/env python3
"""Negative control for indexmaps.py: the actual relabelling maps are compared with the claimed maps and with
plausible wrong ones (off-by-one side rules, wrong class maps).  A wrong map must mismatch on (almost) every
labelling; the claimed maps must never mismatch."""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from indexmaps import T, hull, labelling, make_set, neg, point_of  # noqa: E402

PRED = {
    # name: (reflect, start: 'pa' or 'npa', class map f(i,a), side flip rule g(i,a))
    "A  (claimed)":            (False, "pa",  lambda i, a: (i - a) % T, lambda i, a: i < a),
    "A' (claimed, start -p_a)": (False, "npa", lambda i, a: (i - a) % T, lambda i, a: i >= a),
    "A  flips i<=a (wrong)":   (False, "pa",  lambda i, a: (i - a) % T, lambda i, a: i <= a),
    "A  no flips (wrong)":     (False, "pa",  lambda i, a: (i - a) % T, lambda i, a: False),
    "A  class a-i (wrong)":    (False, "pa",  lambda i, a: (a - i) % T, lambda i, a: i < a),
    "B  (claimed)":            (True,  "pa",  lambda i, a: (a - i) % T, lambda i, a: i > a),
    "B' (claimed, start -p_a)": (True,  "npa", lambda i, a: (a - i) % T, lambda i, a: i <= a),
    "B  flips i>=a (wrong)":   (True,  "pa",  lambda i, a: (a - i) % T, lambda i, a: i >= a),
    "B  flips i<a (wrong)":    (True,  "pa",  lambda i, a: (a - i) % T, lambda i, a: i < a),
    "B  class a+1-i (wrong)":  (True,  "pa",  lambda i, a: (a + 1 - i) % T, lambda i, a: i > a),
    "B  class i-a (wrong)":    (True,  "pa",  lambda i, a: (i - a) % T, lambda i, a: i > a),
    "B  class -i (wrong)":     (True,  "pa",  lambda i, a: (-i) % T, lambda i, a: i > a),
}


def main():
    nsets = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 99)
    mism = {k: 0 for k in PRED}
    total = 0
    sig = lambda p: (-p[0], p[1])
    done = 0
    while done < nsets:
        P = make_set(rng, rng.randint(1, 16), rng.choice([0, 2, 3]))
        if P is None:
            continue
        done += 1
        H = hull(P)
        for h in H:
            lab, reps = labelling(P, h)
            a = sorted({lab[p][0] for p in H})[1]
            pa = point_of(reps, (a, 0))
            total += 1
            for name, (refl, st, f, g) in PRED.items():
                start = pa if st == "pa" else neg(pa)
                if refl:
                    Q = [sig(p) for p in P]
                    lab2, _ = labelling(Q, sig(start))
                    img = lambda x: lab2[sig(x)]
                else:
                    lab2, _ = labelling(P, start)
                    img = lambda x: lab2[x]
                bad = any(img(x) != (f(lab[x][0], a), lab[x][1] ^ int(g(lab[x][0], a))) for x in P)
                mism[name] += bad
    print(f"labellings: {total}")
    for k, v in mism.items():
        print(f"  {k:28s} mismatched on {v:5d} of {total}")
    claimed_ok = all(mism[k] == 0 for k in PRED if "claimed" in k)
    wrong_caught = all(mism[k] > 0 for k in PRED if "wrong" in k)
    print("claimed maps never mismatch:", claimed_ok, "; every wrong map caught:", wrong_caught)
    return 0 if claimed_ok and wrong_caught else 1


if __name__ == "__main__":
    sys.exit(main())
