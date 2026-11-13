import json, sys, subprocess, os
G=sys.argv[1]; case=sys.argv[2]
given=json.load(open(G+'/../tasks/G4.json'))[case]
lines=open(f'{G}/{case}/leaves.icnf').read().split('\n')
assert lines[-1]==''
leaves=[]
for l in lines[:-1]:
    t=l.split(); assert t[0]=='a' and t[-1]=='0'; leaves.append(tuple(map(int,t[1:-1])))
rs=[json.loads(l) for l in open(f'{G}/{case}/leaves.jsonl')]
ver={tuple(r['cube']) for r in rs if r.get('status')=='UNSAT' and r.get('cake_lpr')=='s VERIFIED UNSAT'}
assert set(leaves)<=ver, 'unverified leaf'
ok=0
for c in given:
    S=set(c); res=[[l for l in L if l not in S] for L in leaves if not any(-x in S for x in L)]
    res=[r for r,L in zip(res,[L for L in leaves if not any(-x in S for x in L)]) if set(L)>=S or True]
    # residual cubes of leaves consistent with c; disjunction must be valid: clauses = negated cubes must be UNSAT
    if any(len(r)==0 for r in res): ok+=1; continue
    vs=sorted({abs(x) for r in res for x in r}); m={v:i+1 for i,v in enumerate(vs)}
    cnf=f'p cnf {len(vs)} {len(res)}\n'+''.join(' '.join(str(-x//abs(x)*m[abs(x)]) for x in r)+' 0\n' for r in res)
    open('/opt/work/cov.cnf','w').write(cnf)
    rc=subprocess.run(['/opt/bin/cadical','-q','/opt/work/cov.cnf'],capture_output=True).returncode
    ok+= rc==20
print(case,'given',len(given),'covered',ok,'leaves',len(leaves))
