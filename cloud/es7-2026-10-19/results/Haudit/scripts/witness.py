#!/usr/bin/env python3
"""Task 4 extra: every clause of F violated by the least model of the auxiliaries must be witnessed
by a real convex 7-gon (exact check).  Tests "no convex 7-gon => F satisfied" at n = 33, where
7-gon-free sets cannot be sampled.   usage: witness.py SEED NPER OUT.jsonl"""
import sys, json
SEED, WPER, OUTW = sys.argv[1], int(sys.argv[2]), sys.argv[3]
sys.argv = ['x', '/opt/work/F/m33k7int.sub.cnf', '/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/Mii-S/cases.icnf',
            '/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/inputs/distinct_K7.txt', SEED, '0', '/dev/null']
exec(open('/opt/audit/geotest.py').read())
INV = {v: ('V',) + k for k, v in VID.items()}; INV.update({v: ('E',) + k for k, v in EID.items()})
MEMO = {}
def chain(O, kind, x, a, b, r):
    key = (kind, x, a, b, r)
    if key in MEMO: return MEMO[key]
    MEMO[key] = res = _chain(O, kind, x, a, b, r); return res
def _chain(O, kind, x, a, b, r):
    good = (lambda t: O[t]) if kind == 'cup' else (lambda t: not O[t])
    if not good((x, a, b)): return None
    if r == 3: return [x, a, b]
    for w in range(x + 1, a):
        if good((w, a, b)):
            c = chain(O, kind, x, w, a, r - 1)
            if c: return c + [b]
    return None
def chain_xb(O, kind, x, b, r):
    for a in range(x + 1, b):
        c = chain(O, kind, x, a, b, r)
        if c: return c
    return None
def convex7(P, S):
    S = sorted(set(S))
    return len(S) == 7 and len(hull_idx([P[i - 1] for i in S])) == 7
src = open('/opt/audit/geotest.py').read()
body = src.split("def analyse(P, kind, extra):")[1].split("    ss, ls = clause_sat(Xv)")[0]
exec("def build(P, kind, extra):" + body + "    return Xv, P, O\n")
with open(OUTW, 'w') as out:
    for kind, g in GEN.items():
        got = 0
        while got < WPER:
            r = g()
            if r is None: continue
            P0, extra = r
            if not general_position(P0): continue
            Pn, _ = normalize(P0)
            if 16 in hull_idx(Pn): continue
            res = build(P0, kind, extra)
            if isinstance(res, dict): continue
            Xv, P, O = res; MEMO.clear()
            ss, ls = clause_sat(Xv)
            viol = np.nonzero(~ss)[0]; bad = []; kinds = {}
            for ci in viol:
                c = [int(l) for l in SH[ci]]; aux = sorted({abs(l) for l in c if abs(l) > NX})
                if len(aux) == 2:   # [-E_cap(x,b,r), -E_cup(x,b,s)]
                    e1, e2 = INV[aux[0]], INV[aux[1]]
                    assert e1[0] == 'E' and e2[0] == 'E' and e1[2:4] == e2[2:4]
                    S = chain_xb(O, e1[1], e1[2], e1[3], e1[4]) or []
                    T = chain_xb(O, e2[1], e2[2], e2[3], e2[4]) or []
                    W = S + T; kinds['cap+cup'] = kinds.get('cap+cup', 0) + 1
                else:               # [-V(kind,x,w,a,6), -lit(w,a,b)]
                    v = INV[aux[0]]; assert v[0] == 'V' and v[5] == 6
                    lit = [l for l in c if abs(l) <= NX][0]
                    # which b: orientation literal is the orbit rep of (w,a,b); find b consistent
                    _, kd, x, w, a, _r = v
                    W = []
                    for b in range(a + 1, 34):
                        if M.orb(w, a, b) == abs(lit):
                            ch = chain(O, kd, x, w, a, 6)
                            if ch and ((O[(w, a, b)]) == (kd == 'cup')): W = ch + [b]; break
                    kinds['7-chain'] = kinds.get('7-chain', 0) + 1
                if not convex7(P, W): bad.append((c, W))
            out.write(json.dumps({"kind": kind, "violated": int(len(viol)), "types": kinds, "unwitnessed": len(bad), "ex": bad[:2]}) + "\n"); out.flush()
            got += 1
