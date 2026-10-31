import sys,json,hashlib,collections,itertools
sys.path.insert(0,'/opt/a5'); import mk
M=[json.loads(l) for l in open('/opt/work/M.jsonl')]
L=collections.defaultdict(list)
for m in M: L[m['case']].append(m['lits'])
print('empty-lits leaves',sum(1 for m in M if m['lits']==[]), 'cases where only leaf is empty',sum(1 for c,v in L.items() if v==[[]]),'cases with empty + others',sum(1 for c,v in L.items() if [] in v and len(v)>1))
cov={}
for l in open('/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/V3Z/covers.jsonl'):
    r=json.loads(l); cov[r['key']]=r
def variants(case):
    cube=mk.cubes[case]; leaves=L[case]
    for nvname,nv in (('47002',mk.nv),('maxvar',max([abs(x) for x in cube]+[abs(x) for lf in leaves for x in lf]))):
        for order in ('manifest','sorted'):
            lv=leaves if order=='manifest' else sorted(leaves)
            for neg_first in (False,True):
                cl=[[u] for u in cube]; nl=[[-x for x in lf] for lf in lv]
                cls=nl+cl if neg_first else cl+nl
                yield (nvname,order,neg_first), ('p cnf %d %d\n'%(nv,len(cls))+''.join(' '.join(map(str,c))+' 0\n' for c in cls)).encode()
def lsha(case):
    out={}
    for order in ('manifest','sorted'):
        lv=L[case] if order=='manifest' else sorted(L[case])
        out[order+'-lines']=hashlib.sha256(''.join(' '.join(map(str,lf))+' 0\n' for lf in lv).encode()).hexdigest()
        out[order+'-a']=hashlib.sha256(''.join('a '+' '.join(map(str,lf))+(' ' if lf else '')+'0\n' for lf in lv).encode()).hexdigest()
        out[order+'-json']=hashlib.sha256(json.dumps(lv).encode()).hexdigest()
    return out
if __name__=='__main__':
    for case in ('U10_L2','U10_L5'):
        r=cov[case]; print(case,len(L[case]),r['nleaves'])
        for k,d in variants(case):
            if hashlib.sha256(d).hexdigest()==r['cnf_sha256']: print(' cnf match',k)
        for k,h in lsha(case).items():
            if h==r['leaves_sha256']: print(' leaves_sha match',k)
