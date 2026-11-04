#!/usr/bin/env python3
"""Exact stdlib checker for 3-term Grassmann-Pluecker (GP) clauses on the sixfold 10-layer encoding (Enc(6,8,10)).

Semantics (independent re-implementation of C7UPPER/gen.py's orbit variables): points x = 6*i + k, rotation
R(x) = 6*(x//6) + (x%6+1)%6.  For a triple T of distinct points, its canonical form is the lexicographically least
sorted image of T under the 6 rotations; var(T) = 1 + index of the canonical form in the sorted list of all canonical
forms (5710 of them).  orient(T) = parity(T -> sorted rotated image) * (+1 if var true else -1).

Certificate line format (JSON per line): {"quintuple": [a,b,c,d,e], "clause": [lits]}.
Check: the clause's variables are exactly the variables of the 6 brackets abc, ade, abd, ace, abe, acd; under the
unique assignment falsifying the clause, the three terms [abc][ade], -[abd][ace], [abe][acd] all have the same sign.
Since [abc][ade] - [abd][ace] + [abe][acd] = 0 identically (verified symbolically by --selftest), no real
configuration with the sixfold rotation and generic (nonzero) orientations falsifies the clause.
Optional --model: also check that the model (JSON list of true vars) falsifies every clause.
"""
import sys, json, itertools
N, M = 60, 6
def rot(x, s): return (x // M) * M + (x % M + s) % M
def sortpar(t):
    a = list(t); p = 1
    for i in range(len(a)):
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]: a[j], a[j + 1] = a[j + 1], a[j]; p = -p
    return tuple(a), p
CANON = {}
for T in itertools.combinations(range(N), 3):
    best = None
    for s in range(M):
        srt, par = sortpar([rot(x, s) for x in T])
        if best is None or srt < best[0]: best = (srt, par)
    CANON[T] = best
VARS = {C: i + 1 for i, C in enumerate(sorted({c for c, _ in CANON.values()}))}
assert len(VARS) == 5710
def var_par(t):
    srt, p1 = sortpar(t); C, p2 = CANON[srt]
    return VARS[C], p1 * p2
def check_line(q, clause, model=None):
    a, b, c, d, e = q
    if len(set(q)) != 5 or not all(0 <= x < N for x in q): return 'bad quintuple'
    terms = [((a, b, c), (a, d, e), 1), ((a, b, d), (a, c, e), -1), ((a, b, e), (a, c, d), 1)]
    vs = {abs(l) for l in clause}
    if len(vs) != len(clause): return 'repeated variable in clause'
    need = {var_par(t)[0] for x, y, _ in terms for t in (x, y)}
    if vs != need: return 'clause variables differ from bracket variables'
    val = {abs(l): (l < 0) for l in clause}   # falsifying assignment: var true iff its literal is negative
    def o(t):
        v, p = var_par(t); return p * (1 if val[v] else -1)
    s = [co * o(x) * o(y) for x, y, co in terms]
    if not (s[0] == s[1] == s[2]): return 'terms not of equal sign'
    if model is not None:
        if any((l > 0) == (abs(l) in model) for l in clause): return 'model does not falsify clause'
    return None
def selftest():
    import sympy
    X = sympy.symbols('x0:5'); Y = sympy.symbols('y0:5')
    def br(i, j, k): return sympy.Matrix([[X[i], Y[i], 1], [X[j], Y[j], 1], [X[k], Y[k], 1]]).det()
    expr = sympy.expand(br(0,1,2)*br(0,3,4) - br(0,1,3)*br(0,2,4) + br(0,1,4)*br(0,2,3))
    assert expr == 0
    # independent orbit map vs reference encoder
    import importlib.util, os
    sp = importlib.util.spec_from_file_location('gen', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools', 'gen.py'))
    G = importlib.util.module_from_spec(sp); sp.loader.exec_module(G); E = G.Enc(6, 8, 10)
    for T in itertools.permutations(range(0, 60, 7), 3):
        v, p = var_par(T); r = E.o(*T); assert abs(r) == v and (1 if r > 0 else -1) == p
    print('selftest: GP identity symbolic zero; orbit map agrees with gen.py')
if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0] == '--selftest': selftest(); sys.exit(0)
    model = None
    if '--model' in args:
        i = args.index('--model'); model = set(json.load(open(args[i + 1]))); del args[i:i + 2]
    bad = 0; n = 0
    for line in open(args[0]):
        if not line.strip(): continue
        r = json.loads(line); n += 1
        err = check_line(tuple(r['quintuple']), r['clause'], model)
        if err: bad += 1; print('REJECT line', n, err)
    print(json.dumps({'lines': n, 'rejected': bad, 'ok': bad == 0 and n > 0}))
    sys.exit(0 if bad == 0 and n > 0 else 1)
