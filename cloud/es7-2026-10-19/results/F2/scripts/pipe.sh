#!/bin/bash
# pipe.sh NAME : verify a grown 26-set, build 32-sets, abstract checks (x and rot90)
cd /tmp/claude-0/-home-user-erdos-szekeres-lean/7d9c6ca0-022c-5e66-8370-d636a42cff9f/scratchpad
S=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/F2/scripts
N=$1
python3 $S/verify26.py ./brute ggs/$N.pts >> verify26.jsonl
python3 $S/process26.py --nocompress new32 ggs/$N.pts >> process26.jsonl
python3 $S/check32.py ./satc ./ext_solve ./brute_kgon base33.cnf new32wd $(ls new32/${N}_d*.pts | grep -v small) > new32_check_$N.jsonl
python3 -c "
import glob,os
for f in glob.glob('new32/${N}_d*.pts'):
    if 'small' in f: continue
    P=[tuple(map(int,l.split())) for l in open(f)]
    open('new32r/'+os.path.basename(f)[:-4]+'_rot90.pts','w').write(''.join(f'{-y} {x}\n' for x,y in P))
"
python3 $S/check32.py ./satc ./ext_solve ./brute_kgon base33.cnf new32rwd $(ls new32r/${N}_d*.pts) > new32r_check_$N.jsonl
python3 -c "
import json
for fn in ('new32_check_$N.jsonl','new32r_check_$N.jsonl'):
    L=[json.loads(l) for l in open(fn)]
    print(fn, len(L), 'abs_sat', sum(r['abstract_saturated'] for r in L), 'ok7free', sum(r['largest_convex_subset']==6 and r['general_position'] and 'convex_K_subsets=0' in r['brute_kgon'] for r in L), 'SAT', [r['ext_sat'] for r in L if r['ext_sat']], 'UNK', [r['ext_unknown'] for r in L if r['ext_unknown']])"
