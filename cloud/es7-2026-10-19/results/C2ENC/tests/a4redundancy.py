"""Is the interiority family (A4) implied by the other clauses of the rot m=2 encoding?

For a CNF produced by the mutant without A4, force, for a 4-element set {p,q,r,t} without zero triple and a sign s,
the pattern that A4 forbids (chi(t,q,r) = chi(p,t,r) = chi(p,q,t) = s, chi(p,q,r) = -s, a positive 4-circuit) as unit
clauses, and ask CaDiCaL whether the rest of the CNF still has a model.  SAT for some choice means the A4 family is
not redundant (the mutant has strictly more models); UNSAT for every choice means A4 is implied at that instance.

usage: a4redundancy.py CNF MAP [--all | --sample N]
"""
import itertools
import json
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import classes  # noqa: E402

CADICAL = os.environ.get("CADICAL", "cadical")   # CaDiCaL 3.0.1 binary (path or name on the PATH)


def main():
    cnf, mp = sys.argv[1], sys.argv[2]
    info = json.load(open(mp))
    tv = {(a, b, c): (v, s) for a, b, c, v, s in info["triples"]}
    N = info["N"]

    def L(a, b, c):
        T = (a, b, c)
        S = tuple(sorted(T))
        if S not in tv:
            return 0
        v, s = tv[S]
        return classes.perm_sign(T) * s * v
    body = open(cnf).read().split("\n")
    hdr = [i for i, l in enumerate(body) if l.startswith("p cnf")][0]
    _, _, nv, nc = body[hdr].split()
    choices = []
    for S in itertools.combinations(range(N + 1), 4):
        if any(tuple(sorted(T)) not in tv for T in itertools.combinations(S, 3)):
            continue
        for t in S:
            p, q, r = [x for x in S if x != t]
            for s in (1, -1):
                choices.append((S, t, s, [s * L(t, q, r), s * L(p, t, r), s * L(p, q, t), -s * L(p, q, r)]))
    if "--sample" in sys.argv:
        k = int(sys.argv[sys.argv.index("--sample") + 1])
        random.Random(5).shuffle(choices)
        choices = choices[:k]
    tmp = cnf + ".a4tmp.cnf"
    nsat = nuns = ntriv = 0
    examples = []
    for S, t, s, units in choices:
        if any(-u in units for u in units):
            ntriv += 1          # the pattern contradicts the variable identification itself
            continue
        with open(tmp, "w") as f:
            f.write("\n".join(body[:hdr]) + ("\n" if hdr else ""))
            f.write(f"p cnf {nv} {int(nc) + len(units)}\n")
            f.write("\n".join(body[hdr + 1:]).rstrip("\n") + "\n")
            for u in units:
                f.write(f"{u} 0\n")
        r = subprocess.run([CADICAL, "-q", "-t", "60", tmp], capture_output=True, text=True)
        if r.returncode == 10:
            nsat += 1
            if len(examples) < 5:
                examples.append((S, t, s))
        elif r.returncode == 20:
            nuns += 1
        else:
            print("unknown result", r.returncode)
    os.remove(tmp)
    print(f"{cnf}: {len(choices)} forced positive-circuit patterns: SAT {nsat}, UNSAT {nuns}, "
          f"contradicting the identification {ntriv}; examples SAT {examples}")


if __name__ == "__main__":
    main()
