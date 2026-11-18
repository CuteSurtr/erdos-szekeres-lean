#!/usr/bin/env python3
"""Exact independent crossing-sign audit of the fixed real obstructions."""
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource

resource.setrlimit(resource.RLIMIT_AS, (150 << 20, 150 << 20))
E = Path(__file__).resolve().parent
inputs = ['terminal12/uniform/result.json', 'terminal15/data/balanced.json']
results = []
for relative in inputs:
    source = E/relative
    pts = json.loads(source.read_text())['P']
    assert all(pts[i][0] < pts[i+1][0] for i in range(len(pts)-1))
    signs = {}
    for i,j,k in combinations(range(len(pts)),3):
        a,b,c = pts[i],pts[j],pts[k]
        value = a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1])
        assert value
        signs[i,j,k] = 1 if value > 0 else -1
    cuts = []
    for cut in range(1,len(pts)):
        llr = [(t,s) for t,s in signs.items() if t[1]<cut<=t[2]]
        lrr = [(t,s) for t,s in signs.items() if t[0]<cut<=t[1]]
        patterns = {}
        for name, a, b in [('high',1,-1),('low',-1,1),('all_cup',1,1),('all_cap',-1,-1)]:
            violations = [list(t) for t,s in llr if s!=a]+[list(t) for t,s in lrr if s!=b]
            patterns[name] = {'holds':not violations, 'violation_count':len(violations),
                              'first_violation':violations[0] if violations else None}
        cuts.append({'left_size':cut,'patterns':patterns})
    results.append({'source':relative,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                    'm':len(pts),'all_determinants_nonzero':True,'cuts':cuts,
                    'holding_cuts':{name:[r['left_size'] for r in cuts if r['patterns'][name]['holds']]
                                    for name in ['high','low','all_cup','all_cap']}})
out={'label':'COMPUTED exact fixed-coordinate crossing-sign audit',
     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'results':results,
     'scope':'Fixed examples only. No new general decomposition lemma is inferred.'}
(E/'data/obstruction-cuts.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps([{'m':r['m'],'holding_cuts':r['holding_cuts']} for r in results]))
