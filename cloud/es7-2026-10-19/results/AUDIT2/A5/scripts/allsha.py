# compare A5 cnf_sha256 for every manifest leaf with V3 VERIFIED records
import sys,json,hashlib,pickle,collections
sys.path.insert(0,'/opt/a5'); import mk
F=open('/opt/work/F.cnf','rb').read(); body=F.split(b'\n',1)[1]
pre={}
def h(case,lits):
    units=mk.cubes[case]+list(lits); n=mk.nc+len(units)
    if n not in pre:
        x=hashlib.sha256(b'p cnf %d %d\n'%(mk.nv,n)); x.update(body); pre[n]=x
    x=pre[n].copy(); x.update(b''.join(b'%d 0\n'%u for u in units)); return x.hexdigest()
I=pickle.load(open('/opt/a5/v3idx.pkl','rb'))
c=collections.Counter(); bad=[]
for l in open('/opt/work/M.jsonl'):
    m=json.loads(l); recs=I.get((m['case'],json.dumps(m['lits'])),[])
    mine=h(m['case'],m['lits'])
    ver=[r for r in recs if r[0]=='VERIFIED']
    if not ver: c['no VERIFIED']+=1; bad.append(m['idx']); continue
    if all(r[1]==mine for r in ver): c['all VERIFIED sha match']+=1
    elif any(r[1]==mine for r in ver): c['some VERIFIED sha match']+=1
    else: c['no VERIFIED sha match']+=1; bad.append(m['idx'])
    if not all(r[4]=='s VERIFIED UNSAT' for r in ver): c['VERIFIED w/o exact cake line']+=1
    vs=collections.Counter(r[0] for r in recs)
    for k in vs:
        if k!='VERIFIED': c['also has '+k]+=1
    # leaf literal sanity
    L=m['lits']
    if len(set(map(abs,L)))!=len(L) or any(abs(x)>mk.nv or x==0 for x in L): c['bad lits']+=1
    if set(L)&{-u for u in mk.cubes[m['case']]}: c['leaf contradicts cube']+=1
    if set(L)&set(mk.cubes[m['case']]): c['leaf repeats cube lit']+=1
print(dict(c)); print('bad idx sample',bad[:20])
