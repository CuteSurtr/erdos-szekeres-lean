import json,collections,statistics
man={}
for l in open('/opt/work/Mr.jsonl'):
    r=json.loads(l); man[r['idx']]=r
mine=[i for i in man if i%16==4]
cases=sorted({r['case'] for r in man.values()}); mycases=[c for k,c in enumerate(cases) if k%16==4]
lv=collections.Counter(); cv=collections.Counter(); bad=[]; done=set(); S=[];C=[]
for l in open('/opt/work/out/out.jsonl'):
    try: r=json.loads(l)
    except: continue
    if r['kind']=='leaf':
        lv[r['verdict']]+=1
        if r['verdict']=='VERIFIED': done.add(r['key'])
        if 'solve_s' in r: S.append(r['solve_s'])
        if 'check_s' in r: C.append(r['check_s'])
    else: cv[r['verdict']]+=1
    if r['verdict']!='VERIFIED':
        m=man.get(r['key']) if r['kind']=='leaf' else None
        bad.append((r, m['sources'] if m else None))
print("my leaves",len(mine),"my cases (covers)",len(mycases),mycases)
print("leaf verdicts",dict(lv)); print("cover verdicts",dict(cv))
print("leaves still without VERIFIED record",len(set(mine)-done))
f=lambda x:(round(sum(x),1),round(statistics.median(x),2),round(max(x),2)) if x else None
print("solve_s (sum,median,max)",f(S),"n",len(S)); print("check_s (sum,median,max)",f(C),"n",len(C))
print("non-VERIFIED:",bad)
