"""Baseline: sparse local certificates for every bad 5-layer subset of one model; distinct orbits used."""
import sys, json, re
from multiprocessing import Pool
sys.path.insert(0, '.')
import bfp_cegar2 as B, bfp_cegar3 as C
from modeltest import chi_from_model
if __name__ == '__main__':
    chi = chi_from_model(sys.argv[1])
    bad = [tuple(map(int, re.findall(r'\d+', l.split(')')[0]))) for l in open(sys.argv[2]) if l.startswith('bad')]
    res = []
    with Pool(3, initializer=B._init, initargs=(chi,)) as pool:
        for L, d, msg in pool.imap_unordered(C._cert_sparse, bad):
            if d is None: print('FAIL', L, msg, flush=True); continue
            orb = {B.ids[tuple(sorted(L[p // 4] * 4 + p % 4 for p in tr))] for tr, _ in d['used']}
            res.append((len(orb), L))
    res.sort()
    print('subsets', len(res), 'orbits used: min', res[0], 'median', res[len(res) // 2][0], 'max', res[-1][0], flush=True)
    json.dump(res, open(sys.argv[3], 'w'))
