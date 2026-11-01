import random, collections, sys
from adversarial import sample
from rhyp import check
from rconstruct import base_abscissae
k = int(sys.argv[1]); N = int(sys.argv[2])
rng = random.Random(int(sys.argv[3]))
xs = base_abscissae(k)
c = collections.Counter(); sizes = collections.Counter(); asym = 0; offc = 0; tot_pass = 0; full_chain = 0
for it in range(N):
    cl, info = sample(rng, k, 10 ** 15, tune_h4=(it % 2 == 0))
    rep = check(cl, k, xs)
    if rep['ALL']:
        tot_pass += 1
        c[(info['sym_mode'], info['mmode'])] += 1
        sizes[tuple(len(B) for B in cl)] += 1
        n = k - 2
        S = set(p for B in cl for p in B)
        if not all((-x, -y) in S for B in cl for (x, y) in B): asym += 1
        if info['off'] != (0, 0): offc += 1
        lc = rep['H5_detail'][n // 2 - 1][1]; lk = rep['H5_detail'][n // 2 + 1][2]
        if lc == n // 2 and lk == n // 2: full_chain += 1
print("passing samples:", tot_pass, "of", N)
print("by (outer symmetry mode, middle mode):", dict(c))
print("not centrally symmetric:", asym, " middle off-centre:", offc, " full cup in B_{n/2-1} AND full cap in B_{n/2+1}:", full_chain)
print("distinct cluster-size vectors:", len(sizes), " examples:", list(sizes.items())[:8])
