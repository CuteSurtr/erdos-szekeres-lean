#!/usr/bin/env python3
"""Independent necessary five-label Grassmann-Pluecker sign checks."""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource

HERE=Path(__file__).resolve().parent
CASE=Path('/home/jay/research/data/delta3-codex-20261113/extension/terminal7-a/m15')


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def load_signs():
    known={}
    with (CASE/'solve/cadical.log').open() as f:
        for line in f:
            if line.startswith('v '):
                for z in map(int,line.split()[1:]):
                    if 0<abs(z)<=455:
                        assert abs(z) not in known or known[abs(z)]==(1 if z>0 else -1)
                        known[abs(z)]=1 if z>0 else -1
    assert set(known)==set(range(1,456))
    return {t:known[i] for i,t in enumerate(combinations(range(15),3),1)}


def alternating(signs,t):
    parity=sum(t[i]>t[j] for i in range(3) for j in range(i+1,3))%2
    return signs[tuple(sorted(t))]*(-1 if parity else 1)


def check(signs,m):
    count=0;failures=[]
    for five in combinations(range(m),5):
        for a in five:
            b,c,d,e=[v for v in five if v!=a]
            terms=(alternating(signs,(a,b,c))*alternating(signs,(a,d,e)),
                   -alternating(signs,(a,b,d))*alternating(signs,(a,c,e)),
                   alternating(signs,(a,b,e))*alternating(signs,(a,c,d)))
            count+=1
            if len(set(terms))==1:
                failures.append({'five':five,'pivot':a,'terms':terms})
    return count,failures


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    signs=load_signs();count,bad=check(signs,15)
    # Exact real controls verify the determinant identity and the signs.
    P=[(i,i*i) for i in range(7)]
    def determinant(a,b,c):
        x,y=P[a];u,v=P[b];w,z=P[c]
        return (u-x)*(z-y)-(v-y)*(w-x)
    real={t:1 if determinant(*t)>0 else -1 for t in combinations(range(7),3)}
    controls,failures=check(real,7);assert not failures
    for five in combinations(range(7),5):
        for a in five:
            b,c,d,e=[v for v in five if v!=a]
            assert determinant(a,b,c)*determinant(a,d,e)-determinant(a,b,d)*determinant(a,c,e)+determinant(a,b,e)*determinant(a,c,d)==0
    out={'label':'COMPUTED exact necessary realizability check','status':'GP_FAIL' if bad else 'GP_PASS',
         'm':15,'identities_checked':count,'failures':bad,'real_control_identities':controls,
         'conclusion':'NOT REALIZABLE: necessary sign relation fails' if bad else 'Necessary condition only; real realizability UNKNOWN',
         'signs':''.join('+' if s>0 else '-' for s in signs.values()),
         'cnf_sha256':sha(CASE/'input.cnf'),'model_log_sha256':sha(CASE/'solve/cadical.log'),
         'script_sha256':sha(Path(__file__))}
    (HERE/'data').mkdir(exist_ok=True)
    with (HERE/'data/gp.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('signs','failures')} | {'failure_count':len(bad),'first_failures':bad[:3]}))


if __name__=='__main__':main()
