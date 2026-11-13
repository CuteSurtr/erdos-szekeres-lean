#!/usr/bin/env python3
"""Full SHA-256 list of every k9 cube with a cake_lpr verdict: name, verdict lines, cube CNF, LRAT, proof.lrat.zst."""
import os, re
C = '/home/jay/research/data/satopen-20261113/k9/cubes'
print('# k9 cubes with result.txt (cake_lpr). Columns: cube  VERIFIED_LINES  cube.cnf-sha256  proof.lrat-sha256  proof.lrat.zst-sha256')
for n in sorted(os.listdir(C)):
    r = os.path.join(C, n, 'result.txt')
    if not os.path.exists(r) or os.path.exists(os.path.join(C, n, 'noproof')): continue
    t = open(r).read(); v = re.search(r'VERIFIED_LINES (\d+)', t)
    hs = re.findall(r'^([0-9a-f]{64})\s', t, re.M)
    print(n, v.group(1) if v else '?', *(hs + ['-'] * (3 - len(hs)))[:3])
