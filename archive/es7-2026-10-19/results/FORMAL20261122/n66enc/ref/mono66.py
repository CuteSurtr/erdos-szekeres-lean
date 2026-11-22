"""Monolithic CNF for the (4,4) internal catalog: "some real (6,6,8)-set has at most L holes".
All 70 states are potential owners; sel_i = "state i is occupied".  Every geometric clause is guarded by the
selectors of the owners it mentions.  Clause families (README section 2.6):
  dynamic clauses of coupled5 (empty / domain / positive, refined domains D')            [guards: their owners]
  threshold monotonicity, order transitivity, cap/cup growth with the ceilings, signotope packets
       (only for chronological orders not excluded by the empty units; the omitted clauses are implied)
  chain atoms C_k(p,u,v), U_k(p,u,v), k = 3,4,5:  C_3(p,u,v) <- p<u<v, (p,u,v) cap;
       C_{k+1}(p,u,v) <- C_k(p,t,u), u<v, (t,u,v) cap;  CE(p,q) <- C_5(p,u,q);  UE likewise;
       not CE(p,q) or not UE(p,q)        (a 5-cap and a 5-cup on common endpoints form a convex octagon)
  sel_0, sel_1 (the first two points own the empty diagram and the single cell)
  optional: known demand-one rows as clauses over the selectors (hints; each must be justified separately)
  at most L of the 68 other selectors are false (sequential counter)
UNSAT => every (6,6,8)-set with at least 2 points has at least L+1 holes.
usage: mono66.py <out.cnf> <L> [rows.json|none]      (writes out.cnf and out.cnf.info.json)"""
import itertools, json, os, sys, time, hashlib
import etv_common as ec, coupled5
from coupled5 import BAD4, MAXK
N = ec.N

def generate(emit, S=None):
    """Calls emit(clause, owners) for every geometric clause; returns (cnf, sel, top, C, U, CE, UE)."""
    S = list(range(N)) if S is None else list(S); n = len(S)
    cnf = coupled5.CNF(S, static=False)
    top = cnf.nv
    sel = [top + 1 + i for i in range(n)]; top += n
    can = [[bool(ec.DREF[S[u]][S[v]]) for v in range(n)] for u in range(n)]
    for c, t in zip(cnf.clauses, cnf.tags):
        emit(list(c), t[1:4] if t[0] == 'positive' else t[1:3])
    bef = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j: bef[i][j] = cnf.before(i, j)
    ge = cnf.ge
    ori = {}
    for a, b, c in itertools.permutations(range(n), 3): ori[(a, b, c)] = cnf.orient((a, b, c))
    for i, j in itertools.combinations(range(n), 2):
        for typ in ('cap', 'cup'):
            for k in range(2, MAXK[typ]): emit([-ge(typ, i, j, k + 1), ge(typ, i, j, k)], (i, j))
    C = {}; U = {}
    def newvar():
        nonlocal top; top += 1; return top
    for a, b, c in itertools.permutations(range(n), 3):
        if not (can[a][b] and can[b][c]): continue
        emit([-bef[a][b], -bef[b][c], bef[a][c]], (a, b, c))
        if not can[a][c]: continue
        o = ori[(a, b, c)]
        for typ, color in (('cap', False), ('cup', True)):
            gate = [-bef[a][b], -bef[b][c], -o if color else o]
            for k in range(1, MAXK[typ] + 1):
                x = ge(typ, a, b, k); y = ge(typ, b, c, k + 1)
                if x is False or y is True: continue
                emit(gate + ([] if x is True else [-x]) + ([] if y is False else [y]), (a, b, c))
        for k in (3, 4, 5):
            C[(k, a, b, c)] = newvar(); U[(k, a, b, c)] = newvar()
        emit([-bef[a][b], -bef[b][c], o, C[(3, a, b, c)]], (a, b, c))
        emit([-bef[a][b], -bef[b][c], -o, U[(3, a, b, c)]], (a, b, c))
    CE = {}; UE = {}
    for (k, p, u, q), v in C.items():
        if k == 5:
            if (p, q) not in CE:
                CE[(p, q)] = newvar(); UE[(p, q)] = newvar(); emit([-CE[(p, q)], -UE[(p, q)]], (p, q))
            emit([-v, CE[(p, q)]], (p, u, q)); emit([-U[(5, p, u, q)], UE[(p, q)]], (p, u, q))
    PERM4 = list(itertools.permutations(range(4)))
    for quad in itertools.combinations(range(n), 4):
        for pm in PERM4:
            a, b, c, d = quad[pm[0]], quad[pm[1]], quad[pm[2]], quad[pm[3]]
            if not (can[a][b] and can[b][c] and can[c][d] and can[a][c] and can[b][d] and can[a][d]): continue
            order = [-bef[a][b], -bef[b][c], -bef[c][d]]
            tr = (ori[(a, b, c)], ori[(a, b, d)], ori[(a, c, d)], ori[(b, c, d)])
            for bits in BAD4:
                emit(order + [-t if bit else t for t, bit in zip(tr, bits)], quad)
            o = tr[3]
            for k in (3, 4):
                emit([-C[(k, a, b, c)], -bef[c][d], o, C[(k + 1, a, c, d)]], quad)
                emit([-U[(k, a, b, c)], -bef[c][d], -o, U[(k + 1, a, c, d)]], quad)
    return cnf, sel, top, C, U, CE, UE

def tail_clauses(sel, top, L, rows=None):
    """Selector-only clauses: fixed states, rows (hints), at most L holes.  Returns (clauses, top)."""
    from pysat.card import CardEnc, EncType
    out = [[sel[i]] for i in ec.FIXED_OCC]
    for s, d in (rows or []):
        assert d == 1
        out.append([-sel[i] for i in s])
    enc = CardEnc.atmost(lits=[-sel[i] for i in range(N) if i not in ec.FIXED_OCC], bound=L, top_id=top, encoding=EncType.seqcounter)
    out += enc.clauses
    return out, max(top, enc.nv)

if __name__ == '__main__':
    out, L = sys.argv[1], int(sys.argv[2])
    rows = None
    if len(sys.argv) > 3 and sys.argv[3] != 'none':
        rows = [(s, d) for s, d in json.load(open(sys.argv[3])) if d == 1]
    t0 = time.time(); body = out + '.body'; nc = 0; buf = []
    f = open(body, 'w')
    sel_holder = {}
    def emit(c, own):
        global nc
        buf.append(' '.join(map(str, c)) + ''.join(' -%d' % sel_holder['sel'][o] for o in own) + ' 0\n'); nc += 1
        if len(buf) >= 200000: f.write(''.join(buf)); buf.clear()
    # selectors are numbered right after the coupled5 variables: nv+1..nv+70 (known before generation starts)
    probe = coupled5.CNF(list(range(N)), static=False); sel_holder['sel'] = [probe.nv + 1 + i for i in range(N)]; del probe
    cnf, sel, top, C, U, CE, UE = generate(emit)
    assert sel == sel_holder['sel']
    tail, top = tail_clauses(sel, top, L, rows)
    for c in tail: buf.append(' '.join(map(str, c)) + ' 0\n'); nc += 1
    f.write(''.join(buf)); f.close()
    with open(out, 'w') as g:
        g.write(f'p cnf {top} {nc}\n')
        with open(body) as b:
            while True:
                chunk = b.read(1 << 26)
                if not chunk: break
                g.write(chunk)
    os.remove(body)
    h = hashlib.sha256()
    with open(out, 'rb') as g:
        for chunk in iter(lambda: g.read(1 << 24), b''): h.update(chunk)
    info = {'file': out, 'L': L, 'vars': top, 'clauses': nc, 'rows': len(rows) if rows else 0, 'sha256': h.hexdigest(),
            'bytes': os.path.getsize(out), 'seconds': round(time.time() - t0, 1), 'selectors': [sel[0], sel[-1]]}
    json.dump(info, open(out + '.info.json', 'w')); print(json.dumps(info))
