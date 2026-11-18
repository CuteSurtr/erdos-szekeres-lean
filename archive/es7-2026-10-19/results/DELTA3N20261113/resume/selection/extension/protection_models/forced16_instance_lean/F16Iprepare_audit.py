#!/usr/bin/env python3
"""Independent integer preparation controls, separate from the Lean proof evidence."""
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE.parent / 'forced16_realization/data'
cert_bytes = (INPUT / 'certificate.json').read_bytes()
sign_bytes = (INPUT / 'orientation.signs').read_bytes()
cert = json.loads(cert_bytes)
signs = sign_bytes.decode().strip()
triples = list(itertools.combinations(range(16), 3))
index = {t:i for i,t in enumerate(triples)}
balance = [0]*560
controls = [[(i,i*i) for i in range(16)], [(i,i*i*i+2*i*i+1) for i in range(16)]]

def det(a,b,c):
    return a[0]*(b[1]-c[1])+b[0]*(c[1]-a[1])+c[0]*(a[1]-b[1])

def sign(t):
    inv = sum(t[i]>t[j] for i in range(3) for j in range(i+1,3))
    return (-1)**inv * (1 if signs[index[tuple(sorted(t))]] == '+' else -1)

selected_control_rows = [0,0]
for r in cert['rows']:
    a=r['root']; b,c,d,e=r['other']
    assert len({a,b,c,d,e})==5 and all(0<=i<16 for i in [a,b,c,d,e])
    pairs=[[(a,b,c),(a,d,e)],[(a,b,d),(a,c,e)],[(a,b,e),(a,c,d)]]
    term_signs=[(-1 if k==1 else 1)*math.prod(sign(t) for t in pair)
                for k,pair in enumerate(pairs)]
    L,S=r['large'],r['small']; O=3-L-S
    assert sorted([L,S,O])==[0,1,2] and r['weight']>0
    assert term_signs[L]==-term_signs[S]==-term_signs[O]
    for t in pairs[L]: balance[index[tuple(sorted(t))]]+=r['weight']
    for t in pairs[S]: balance[index[tuple(sorted(t))]]-=r['weight']
    for ci,points in enumerate(controls):
        terms=[(-1 if k==1 else 1)*math.prod(det(*(points[i] for i in t)) for t in pair)
               for k,pair in enumerate(pairs)]
        assert sum(terms)==0 and all(terms)
        if (terms[L]>0)!=(terms[S]>0) and (terms[L]>0)!=(terms[O]>0):
            assert abs(terms[S])<abs(terms[L])
            selected_control_rows[ci]+=1
assert not any(balance)
assert all(n<387 for n in selected_control_rows)
# Independent permutation-parity controls on every ordered distinct triple.
for points in controls:
    for t in itertools.permutations(range(16),3):
        inv=sum(t[i]>t[j] for i in range(3) for j in range(i+1,3))
        assert det(*(points[i] for i in t)) == (-1)**inv*det(*(points[i] for i in sorted(t)))
# Increasing the first weight by one changes at least one exponent total.
r=cert['rows'][0]; a=r['root'];b,c,d,e=r['other']
pairs=[[(a,b,c),(a,d,e)],[(a,b,d),(a,c,e)],[(a,b,e),(a,c,d)]]
corrupt=balance.copy()
for t in pairs[r['large']]:corrupt[index[tuple(sorted(t))]]+=1
for t in pairs[r['small']]:corrupt[index[tuple(sorted(t))]]-=1
assert any(corrupt)
record=dict(status='PASS exact Python controls; not Lean evidence',rows=387,variables=560,
    balanced_exponents=560,gp_identities_control=774,permutation_controls=6720,
    selected_control_rows=selected_control_rows,perturbed_weight_rejected=True,
    certificate_sha256=hashlib.sha256(cert_bytes).hexdigest(),
    signs_sha256=hashlib.sha256(sign_bytes).hexdigest(),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(HERE/'data/preparation-audit.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
