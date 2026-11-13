#!/usr/bin/env python3
"""Is the midpoint clause implied? For each setting, 12 random instances (p, q, r): the base formula plus the units
chi(p,q,r), chi(p,q,-r), not chi(p,q,-p) (one violated midpoint clause). UNSAT means that instance is implied.
Settings: --sym with or without the centre axioms and with or without the no-7-gon clauses.
usage: implied.py   (expects cadical in ../../local/bin, as for closesgn.py)"""
import json, os, random, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # sgn.py is one level up
from sgn import Enc
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "local", "bin", "cadical")
random.seed(7)
for n, centre, kgon in [(10, False, False), (14, False, False), (20, False, False), (14, True, False),
                        (14, False, True), (14, True, True), (20, True, True)]:
    e = Enc(n, 7, True, centre); e.signotope()
    if centre: e.centre_axioms()
    if kgon: e.kgon()
    A = lambda x: n + 1 - x; res = {}
    for t in range(12):
        while True:
            p, q, r = random.sample(range(1, n + 1), 3)
            if q != A(p) and r not in (A(p), A(q)): break
        a, b, m = e.chi(p, q, r), e.chi(p, q, A(r)), e.chi(p, q, A(p))
        cl = list(e.cl) + [(a,), (b,), (-m,)]
        with tempfile.NamedTemporaryFile("w", suffix=".cnf", delete=False) as g:
            g.write(f"p cnf {e.nv} {len(cl)}\n"); g.writelines(" ".join(map(str, c)) + " 0\n" for c in cl)
        ec = subprocess.run([B, "-q", "-t", "60", g.name], stdout=subprocess.DEVNULL).returncode; os.remove(g.name)
        k = {10: "SAT", 20: "UNSAT"}.get(ec, str(ec)); res[k] = res.get(k, 0) + 1
    print(json.dumps({"n": n, "centre": centre, "no_7gon_clauses": kgon, "instances": res}), flush=True)
