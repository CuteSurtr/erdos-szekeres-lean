#!/usr/bin/env python3
"""Stream-compare the two solved fivefold CNFs (angle form P1, layer form L1) line by line.

Reports: header differences, the length of the common clause prefix, and the clauses after it in each file,
decoded into chirotope statements chi(a,b,c) = +/- with points written as (orbit,index) or c (the centre).
Never holds a CNF in memory (only the short tails).

usage: diff_cnf.py A.cnf A.json B.cnf B.json
"""
import json
import sys


def load_map(path):
    with open(path) as f:
        info = json.load(f)
    # variable v with sign s means chi(a,b,c) = s * v  (a<b<c)
    inv = {}
    for a, b, c, v, s in info["triples"]:
        inv.setdefault(v, []).append((a, b, c, s))
    return info, inv


def name(i, info):
    if i == info["center_index"]:
        return "c"
    o, r = divmod(i, info["m"])
    return f"({o},{r})"


def decode(lit, info, inv):
    v = abs(lit)
    if v > info["X_vars"]:
        return f"aux var {lit}"
    # representative triple of the orbit with sign
    reps = inv[v]
    a, b, c, s = min(reps)
    sign = (1 if lit > 0 else -1) * s
    return f"chi({name(a, info)},{name(b, info)},{name(c, info)})={'+' if sign > 0 else '-'}"


def main():
    fa, ja, fb, jb = sys.argv[1:5]
    ia, inva = load_map(ja)
    ib, invb = load_map(jb)
    same_triples = ia["triples"] == ib["triples"]
    print("variable maps (triple -> var, sign) identical:", same_triples)
    for k in ("vars", "X_vars", "clauses", "center_index", "setpts"):
        print(f"  {k}: A={ia[k] if k != 'setpts' else len(ia[k])}  B={ib[k] if k != 'setpts' else len(ib[k])}")
    with open(fa) as A, open(fb) as B:
        # headers: comment lines and p line
        ha, hb = [], []
        for F, H in ((A, ha), (B, hb)):
            while True:
                line = F.readline()
                H.append(line.rstrip("\n"))
                if line.startswith("p cnf"):
                    break
        print("header A:", ha)
        print("header B:", hb)
        n_common = 0
        la = lb = None
        while True:
            la = A.readline()
            lb = B.readline()
            if not la or not lb or la != lb:
                break
            n_common += 1
        tail_a = ([la] if la else []) + A.readlines()  # small: only the tail after the first difference
        tail_b = ([lb] if lb else []) + B.readlines()
    print(f"identical clause lines in common prefix: {n_common}")
    print(f"remaining clauses: A {len(tail_a)}, B {len(tail_b)}")
    # also check whether any tail clause of A appears in B's tail (would be common but out of order)
    sa = {l for l in tail_a}
    sb = {l for l in tail_b}
    print(f"tail clauses common to both tails (as sets): {len(sa & sb)}")
    for lab, tail, info, inv in (("A", tail_a, ia, inva), ("B", tail_b, ib, invb)):
        print(f"--- tail of {lab} ---")
        for l in tail:
            lits = [int(x) for x in l.split()[:-1]]
            print("  ", l.strip(), "  =>  ", " OR ".join(decode(x, info, inv) for x in lits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
