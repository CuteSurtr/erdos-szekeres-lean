import json,statistics,sys
O='/opt/work/out/U_L2/'
rs=[json.loads(l) for l in open(O+'leaves.jsonl')]
for f in ('leaves.icnf','open.icnf','top.icnf'):
    assert all(l.startswith('a ') and l.endswith(' 0\n') for l in open(O+f)), f
top=[tuple(map(int,l.split()[1:-1])) for l in open(O+'top.icnf')]
leaves=[tuple(map(int,l.split()[1:-1])) for l in open(O+'leaves.icnf')]
ver=[r for r in rs if r.get('status')=='UNSAT' and r.get('cake_lpr')=='s VERIFIED UNSAT']
assert sorted(map(tuple,(r['cube'] for r in ver)))==sorted(leaves)
sys.setrecursionlimit(100000)
def covered(cubes):  # do the cubes (sets of literals) cover every assignment?
    if any(len(c)==0 for c in cubes): return True
    if not cubes: return False
    l=next(iter(cubes[0]))
    pos=[c-{l} for c in cubes if -l not in c]; neg=[c-{-l} for c in cubes if l not in c]
    return covered(pos) and covered(neg)
ls=[set(c) for c in leaves]; bad=0
for t in top:
    T=set(t); sub=[c-T for c in ls if not any(-x in T for x in c)]
    if not covered(sub): bad+=1
print('given',len(top),'verified leaves',len(leaves),'uncovered top cubes',bad)
c=lambda s: [r for r in rs if r.get('status')==s]
print({s:len(c(s)) for s in ('UNSAT','SPLIT','UNSAT_UNCHECKED','SAT','TIMEOUT','SKIP')})
print('top cubes that are themselves leaves',len(set(top)&set(leaves)))
sp=c('SPLIT'); print('splits: nsub',[r['nsub'] for r in sp],'split_s sum',round(sum(r['split_s'] for r in sp),1))
for k in ('solve_s','check_s'):
    v=[r[k] for r in ver]; print(k,'sum',round(sum(v),1),'median',round(statistics.median(v),2),'max',max(v))
v=[r['solve_s'] for r in sp]; print('solve_s of split cubes (timeouts) sum',round(sum(v),1))
v=[r['solve_s']+r.get('check_s',0)+r.get('split_s',0) for r in rs if 'cube' in r]; print('all wall per job sum',round(sum(v),1))
print('cake retries',sum(1 for r in rs if r.get('cake_retry')),'max proof MB',round(max(r['proof_bytes'] for r in ver)/1e6,1))
print('resume records',sum(1 for r in rs if r.get('resume')))
