"""Rebuild the CNF certified for 'every FL(a,b)-signotope on n points has one of the listed partitions as a
valid strong split' from the list of partitions alone, and compare its SHA-256 with the certified CNF.
CNF = fls.FL(a,b,n) + for every listed S1 (S2 = complement) the clause
      OR [S1 contains an (a-1)-cap] OR [S1 contains an ((a-2)-cap,(b-1)-cup)-gon]
      OR [S2 contains a (b-1)-cup] OR [S2 contains an ((a-1)-cap,(b-2)-cup)-gon]
with one-directional auxiliary variables (aux -> the triples of the chain have the required sign).
usage: regen_split_cnf.py a b n"""
import sys, os, json, itertools, hashlib
import fls
a, b, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
weak = len(sys.argv) > 4 and sys.argv[4] == 'weak'   # one-sided variant: S2 only has to be free of (b-1)-cups
tag = 'weak' if weak else 'split'
HERE = os.path.dirname(os.path.abspath(__file__))
parts = json.load(open(os.path.join(HERE, 'cert', f'{tag}_{a}_{b}_{n}_partitions.json')))['partitions_S1']
w = fls.FL(a, b, n); extra = []; aux = {}
def chainvar(sgn, idx):
    key = (sgn, idx)
    if key not in aux:
        v = w.new(); aux[key] = v
        for i in range(len(idx) - 2): extra.append([-v, sgn * w.o[idx[i], idx[i + 1], idx[i + 2]]])
    return aux[key]
def gonvar(capidx, cupidx):
    key = ('g', capidx, cupidx)
    if key not in aux:
        g = w.new(); aux[key] = g
        for (sgn, idx) in ((-1, capidx), (1, cupidx)):
            if len(idx) >= 3: extra.append([-g, chainvar(sgn, idx)])
    return aux[key]
def gons(S, lc, lu):
    out = []; ic, iu = lc - 2, lu - 2
    for ui in range(len(S)):
        for vi in range(ui + 1, len(S)):
            mid = S[ui + 1:vi]
            if len(mid) < ic + iu: continue
            for cs in itertools.combinations(mid, ic):
                rest = [p for p in mid if p not in cs]
                for us in itertools.combinations(rest, iu):
                    capidx = (S[ui],) + cs + (S[vi],); cupidx = (S[ui],) + us + (S[vi],)
                    if ic == 0 and iu == 0: continue
                    out.append(gonvar(capidx, cupidx))
    return out
for S1 in parts:
    S1 = sorted(S1); S2 = [p for p in range(n) if p not in set(S1)]; lits = []
    for idx in itertools.combinations(S1, a - 1): lits.append(chainvar(-1, idx))
    lits += gons(S1, a - 2, b - 1)
    for idx in itertools.combinations(S2, b - 1): lits.append(chainvar(1, idx))
    if not weak: lits += gons(S2, a - 1, b - 2)
    extra.append(lits)
cl = w.cl + extra
txt = 'p cnf %d %d\n' % (w.nv, len(cl)) + ''.join(' '.join(map(str, c)) + ' 0\n' for c in cl)
h = hashlib.sha256(txt.encode()).hexdigest()
h0 = hashlib.sha256(open(os.path.join(HERE, 'cert', f'{tag}_{a}_{b}_{n}.cnf'), 'rb').read()).hexdigest()
print(f'FL({a},{b}) n={n} [{tag}]: {len(parts)} partitions, {len(cl)} clauses, regenerated sha256 {h[:16]}…, certified file {h0[:16]}…, equal: {h == h0}')
