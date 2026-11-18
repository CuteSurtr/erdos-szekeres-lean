#!/usr/bin/env python3
"""owner_check.py -- positive control: evaluate every clause of an owner-model CNF under the exact
semantic assignment of a real point set (integer coordinates).  Usage:
   owner_check.py points.json model.cnf [--mirror]
The CNF must have been written with --names.  Exit status 0 iff no clause is violated."""
import sys, pickle, itertools, json
sys.path.insert(0, '.')
import geom, states as st_mod, cat_common


def semantic(P, CA, CB, names, N, rows=None, S=None):
    n = len(P)
    if S is None:
        S = geom.orient(P)
    E = st_mod.labels(P, S)
    assert max(E[-1].values(), default=2) <= CA + 1 and max(E[1].values(), default=2) <= CB + 1, 'cap/cup too long'
    states, cells, capH, cupH, D = cat_common.make(CA, CB)
    NS = len(states)
    prof = st_mod.states(P, CA, CB, S)
    idx = {s: i for i, s in enumerate(states)}
    owner = {}
    for v, f in enumerate(prof):
        assert idx[f] not in owner, 'states not injective'
        owner[idx[f]] = v
    assert n >= N, 'point set smaller than N'
    lab = {(u, v): (E[-1][(u, v)] - 1, E[1][(u, v)] - 1) for u in range(n) for v in range(u + 1, n)}

    def Pv(s, t):
        return s in owner and t in owner and owner[s] < owner[t]

    def sg(a, b, c):   # orientation sign of points a,b,c in the given order
        t = tuple(sorted((a, b, c)))
        inv = (a > b) + (a > c) + (b > c)
        return S[t] if inv % 2 == 0 else -S[t]
    # chains anchored at their first point
    reach = {1: {}, -1: {}}
    for sgn in (1, -1):
        cur = {(s, j, k) for (s, j, k) in itertools.combinations(range(n), 3) if S[(s, j, k)] == sgn}
        reach[sgn][3] = cur
        top = (CB if sgn == 1 else CA) + 1
        for b in range(4, top + 2):
            nxt = set()
            for (s, i, j) in cur:
                for k in range(j + 1, n):
                    if S[(i, j, k)] == sgn:
                        nxt.add((s, j, k))
            reach[sgn][b] = nxt
            cur = nxt
        assert not reach[sgn][top + 1]
    span = {1: {}, -1: {}}
    for sgn in (1, -1):
        for b, R in reach[sgn].items():
            span[sgn][b] = {(s, k) for (s, j, k) in R}
    holes_prefix = [0]
    for i in range(NS):
        holes_prefix.append(holes_prefix[-1] + (0 if i in owner else 1))
    val = {}
    for name, v in names.items():
        k = name[0]
        if k == 'occ':
            x = name[1] in owner
        elif k == 'P':
            x = Pv(name[1], name[2])
        elif k == 'Lab':
            s, t, z = name[1:]
            x = Pv(s, t) and lab[(owner[s], owner[t])] == z
        elif k in ('cupge', 'capge'):
            s, t, kk = name[1:]
            x = Pv(s, t) and lab[(owner[s], owner[t])][1 if k == 'cupge' else 0] >= kk
        elif k == 'ori':
            s, t, r = name[1:]
            x = s in owner and t in owner and r in owner and sg(owner[s], owner[t], owner[r]) > 0
        elif k in ('Wu', 'Wc'):
            t, a, b = name[1:]
            c = 1 if k == 'Wu' else 0
            x = (Pv(t, a) and Pv(a, b) and sg(owner[t], owner[a], owner[b]) == (1 if c else -1)
                 and lab[(owner[t], owner[a])][c] + 1 == lab[(owner[a], owner[b])][c])
        elif k in ('SU', 'SC'):
            b, s, j, kk = name[1:]
            x = Pv(s, j) and Pv(j, kk) and (owner[s], owner[j], owner[kk]) in reach[1 if k == 'SU' else -1][b]
        elif k in ('U', 'K'):
            b, s, t = name[1:]
            x = Pv(s, t) and (owner[s], owner[t]) in span[1 if k == 'U' else -1][b]
        elif k == 'cnt':
            i, j = name[1:]
            x = holes_prefix[i] >= j
        elif k == 'rc':
            fam, _K = rows[name[1]]
            i, j = name[2:]
            x = sum(1 for s in fam[:i] if s in owner) >= j
        else:
            raise ValueError(name)
        val[v] = bool(x)
    return val, owner


def check(points_path, cnf_path, mirror=False, coloring=False):
    meta = pickle.load(open(cnf_path + '.names.pkl', 'rb'))
    if coloring:
        # abstract 2-colouring of the triples of 0..n-1 (not necessarily a signotope):
        # JSON {"n": n, "triples_positive": [[i,j,k],...]}; valid only for CNFs without family S
        d = json.load(open(points_path))
        n = d['n']
        pos = {tuple(t) for t in d['triples_positive']}
        S = {t: (1 if t in pos else -1) for t in itertools.combinations(range(n), 3)}
        P = list(range(n))
        val, owner = semantic(P, meta['CA'], meta['CB'], meta['names'], meta['N'], meta.get('rows'), S=S)
    else:
        P = geom.load(points_path)
        if mirror:
            P = geom.mirror(P)
        val, owner = semantic(P, meta['CA'], meta['CB'], meta['names'], meta['N'], meta.get('rows'))
    bad = 0
    tot = 0
    with open(cnf_path) as f:
        hdr = f.readline().split()
        assert hdr[0] == 'p'
        nv = int(hdr[2])
        assert nv == len(val), (nv, len(val))
        for line in f:
            tot += 1
            ok = False
            for tok in line.split():
                l = int(tok)
                if l == 0:
                    break
                if val[l] if l > 0 else not val[-l]:
                    ok = True
                    break
            if not ok:
                bad += 1
                if bad <= 5:
                    inv = {v: k for k, v in meta['names'].items()}
                    print('VIOLATED', [(('+' if int(t) > 0 else '-'), inv[abs(int(t))]) for t in line.split()[:-1]])
        assert tot == int(hdr[3])
    print(json.dumps({'points': points_path, 'mirror': mirror, 'n': len(P), 'occupied': len(owner),
                      'cnf': cnf_path, 'clauses': tot, 'violated': bad}))
    return bad


if __name__ == '__main__':
    sys.exit(1 if check(sys.argv[1], sys.argv[2], '--mirror' in sys.argv, '--coloring' in sys.argv) else 0)
