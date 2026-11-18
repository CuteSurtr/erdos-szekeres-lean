#!/usr/bin/env python3
"""colcontrol.py CA CB G OWNERCNF nlist seeds -- positive control of the signotope-free owner model
on abstract 2-colourings of triples that are NOT signotopes.
Colourings are sampled with the original position-indexed encoder (etv_sat2.py) with its signotope
clauses removed (random seeds / phases), re-checked by the independent path checker of
decode_check.py, and then the semantic assignment of the owner model (computed from the colouring
alone) is evaluated on every clause of OWNERCNF (must be built with --nosig --names)."""
import sys, json, itertools, subprocess, os
from math import comb
sys.path.insert(0, '.')
import etv_sat2_orig, etv7, decode_check, owner_check

CA, CB, G = map(int, sys.argv[1:4])
cnf = sys.argv[4]
ns = [int(x) for x in sys.argv[5].split(',')]
seeds = [int(x) for x in sys.argv[6].split(',')]
os.makedirs('ctl/col', exist_ok=True)
tot = 0; bad = 0
for n in ns:
    base = f'ctl/col/pos_n{n}.cnf'
    etv_sat2_orig.build(n, CA + 1, CB + 1, base, G)
    L = open(base).read().split('\n')
    hdr = L[0].split(); k = 8 * comb(n, 4)
    rest = [x for x in L[1 + k:] if x.strip()]
    open(base, 'w').write(f'p cnf {hdr[2]} {len(rest)}\n' + '\n'.join(rest) + '\n')
    for sd in seeds:
        out = subprocess.run(['cadical', '-q', f'--seed={sd}', '--phase=%d' % (sd % 2), '--randec=1', '--randecinit=1', base],
                             capture_output=True, text=True).stdout
        if 's SATISFIABLE' not in out:
            # option names differ between versions: retry with the seed only
            out = subprocess.run(['cadical', '-q', f'--seed={sd}', '--phase=%d' % (sd % 2), base], capture_output=True, text=True).stdout
        if 's SATISFIABLE' not in out:
            print('n', n, 'seed', sd, 'no model:', out.split('\n')[0]); continue
        val = set()
        for line in out.split('\n'):
            if line.startswith('v'):
                for t in line.split()[1:]:
                    if int(t) > 0: val.add(int(t))
        col = {t: (1 if etv7.ovar(n, *t) in val else -1) for t in itertools.combinations(range(n), 3)}
        res = decode_check.check(n, col, G)
        assert res['longest_cap_path'] <= CA + 1 and res['longest_cup_path'] <= CB + 1 and not res['has_weak_G_gon'], res
        f = f'ctl/col/col_{CA}{CB}{G}_n{n}_s{sd}.json'
        json.dump({'n': n, 'G': G, 'triples_positive': [list(t) for t, v in sorted(col.items()) if v > 0], 'check': res}, open(f, 'w'))
        b = owner_check.check(f, cnf, coloring=True)
        tot += 1; bad += b
        print('n', n, 'seed', sd, 'signotope violations', res['signotope_violations'], 'owner-CNF violations', b, flush=True)
    os.remove(base)
print('TOTAL colourings', tot, 'owner-CNF violations', bad)
