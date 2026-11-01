import json,pickle,collections,statistics,sys
I=pickle.load(open('/opt/a5/v3idx.pkl','rb'))
S0={json.loads(l)['case']:json.loads(l) for l in open('/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/Mii-S/cases.jsonl')}
for fn in sys.argv[1:]:
    R=[json.loads(l) for l in open(fn)]
    c=collections.Counter(r['verdict'] for r in R); m=collections.Counter()
    for r in R:
        if r['lits']==[] and r['idx']==-1:
            m['match Mii-S case sha' if r['cnf_sha256']==S0[r['case']]['cnf_sha256'] else 'MISMATCH Mii-S']+=1
        else:
            v=[x for x in I[(r['case'],json.dumps(r['lits']))] if x[0]=='VERIFIED']
            m['match V3 sha' if v and all(x[1]==r['cnf_sha256'] for x in v) else 'MISMATCH V3']+=1
    per=collections.Counter(r['case'] for r in R)
    t=[r['solve_s']+r.get('check_s',0) for r in R]
    print(fn,len(R),dict(c),dict(m),'cases',len(per),'U_L2/U3_L/U_L7',per['U_L2'],per['U3_L'],per['U_L7'],
      'solve+check s: sum %.0f median %.1f max %.1f'%(sum(t),statistics.median(t),max(t)),'max proof MB %.0f'%(max(r.get('proof_bytes',0) for r in R)/1e6))
