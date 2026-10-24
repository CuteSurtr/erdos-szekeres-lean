import json,collections,statistics
recs=[]
for l in open('/opt/work/out/out.jsonl'):
    try: recs.append(json.loads(l))
    except: pass
M=[json.loads(l) for l in open('/opt/work/Mr.jsonl')]
mine=[r for r in M if r['idx']%16==2]
cases=sorted({r['case'] for r in M}); mycov=[c for i,c in enumerate(cases) if i%16==2]
leaf={};cov={}
for r in recs:
    (leaf if r['kind']=='leaf' else cov)[r['key']]=r
vc=collections.Counter(r['verdict'] for r in leaf.values())
cc=collections.Counter(r['verdict'] for r in cov.values())
ver={k for k,r in leaf.items() if r['verdict']=='VERIFIED'}
print('my leaves',len(mine),'leaf verdicts',dict(vc),'unchecked(no VERIFIED)',sum(1 for r in mine if r['idx'] not in ver))
print('my covers',len(mycov),mycov,'cover verdicts',dict(cc))
for k in ('solve_s','check_s'):
    xs=[r[k] for r in leaf.values() if r.get(k) is not None]
    if xs: print(k,'sum %.1f median %.2f max %.2f n %d'%(sum(xs),statistics.median(xs),max(xs),len(xs)))
byidx={r['idx']:r for r in M}
for k,r in list(leaf.items())+list(cov.items()):
    if r['verdict']!='VERIFIED':
        src=byidx[k]['sources'] if r['kind']=='leaf' else sorted({s for m in M if m['case']==k for s in m['sources']})
        print('NONVERIFIED',r['kind'],k,r.get('case',''),r['verdict'],r.get('lits',''),'nleaves',r.get('nleaves',''),'sources',src)
