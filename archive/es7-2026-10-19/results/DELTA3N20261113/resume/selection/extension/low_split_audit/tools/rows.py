#!/usr/bin/env python3
"""Independent streamed low-split map and row reconstruction.

No producer or other checker import. Geometry is the inherited generic
family, also rebuilt here; all new predicate clauses are reconstructed.
"""
import argparse
import collections
import hashlib
import itertools as it
import json
from pathlib import Path
import resource

R=Path(__file__).resolve().parents[1]
E=R.parent
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
S=W/'low-split-audit'

def need(ok,why):
    if not ok:raise ValueError(why)

def mask(vs):return sum(1 << v for v in vs)
def verts(s):return tuple(v for v in range(s.bit_length()) if s & (1 << v))
def subs(s,k):return (mask(vs) for vs in it.combinations(verts(s),k))

def sha(p):
    a=p.stat();h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1 << 20),b''):h.update(block)
    b=p.stat()
    need((a.st_ino,a.st_size,a.st_mtime_ns)==(b.st_ino,b.st_size,b.st_mtime_ns),'unstable hash input')
    return h.hexdigest()

def save(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')

class Formula:
    def __init__(self,m,n,variant):
        need(6<=n<=8 and n-1<=m<=16 and variant in ('direct','compact'),'unsupported domain')
        self.m,self.n,self.variant=m,n,variant
        self.full=(1 << m)-1;self.limit=m-n+2
        self.entries=[];self.ids={};self.Q={};self.D={};self.T={};self.ends={}
        for s in subs(self.full,3):self.fresh('orientation',s)

    def fresh(self,kind,s):
        need((kind,s) not in self.ids,'duplicate map key')
        v=len(self.entries)+1;self.entries.append((v,kind,s));self.ids[kind,s]=v
        return v

    def t(self,*vs):return self.ids['orientation',mask(vs)]

    def children(self,s,table,count):
        return tuple(table[s^(1 << v)] for v in verts(s)[:count])

    @staticmethod
    def exact_or(z,terms):
        yield (-z,*terms)
        for v in terms:yield (z,-v)

    def geometry(self):
        phase='signotope';yield phase,None
        for s in subs(self.full,4):
            signs=[self.ids['orientation',t] for t in subs(s,3)]
            for a,b,c in it.combinations(signs,3):
                yield phase,(-a,b,-c);yield phase,(a,-b,c)
        phase='no5cap';yield phase,None
        for s in subs(self.full,5):
            v=verts(s);yield phase,tuple(self.t(*v[j:j+3]) for j in range(3))
        phase='convex4_equivalence';yield phase,None
        for s in subs(self.full,4):
            z=self.Q[s]=self.fresh('convex',s)
            a,b,c,d=[self.ids['orientation',t] for t in subs(s,3)]
            for row in [(-z,-a,b),(-z,a,-b),(-z,-c,d),(-z,c,-d),
                        (z,a,d),(z,-a,-d),(z,b,-c),(z,-b,c)]:yield phase,row
        phase='convex_larger_equivalence';yield phase,None
        for k in range(5,self.n):
            for s in subs(self.full,k):
                z=self.Q[s]=self.fresh('convex',s)
                terms=self.children(s,self.Q,5)
                for v in terms:yield phase,(-z,v)
                yield phase,(z,*[-v for v in terms])
        phase='no_ngon';yield phase,None
        for s in subs(self.full,self.n):
            yield phase,tuple(-v for v in self.children(s,self.Q,5))

    def rows(self):
        yield from self.geometry()
        phase='left_has_no_fourcap';yield phase,None
        for s in subs(self.full,4):yield phase,tuple(self.ids['orientation',t] for t in subs(s,3))
        phase='ends_three_cap_equivalence';yield phase,None
        for b in range(self.m):
            z=self.ends[b]=self.fresh('ends_three_cap',1 << b)
            terms=tuple(-self.t(a,c,b) for a,c in it.combinations(range(b),2))
            if self.variant=='direct':
                for v in terms:yield phase,(z,-v)
                yield phase,(-z,*terms)
            else:
                for row in self.exact_or(z,terms):yield phase,row
        if self.variant=='compact':
            phase='bad_pair_or_cap_exact_containment';yield phase,None
            for s in subs(self.full,2):self.D[s]=-self.ends[verts(s)[-1]]
            for s in subs(self.full,3):
                a,b,c=verts(s)
                z=self.D[s]=self.fresh('bad_pair_or_cap_contains',s)
                for row in self.exact_or(z,(-self.t(a,b,c),-self.ends[b],-self.ends[c])):yield phase,row
            for s in range(self.full+1):
                if 4<=s.bit_count()<=self.limit:
                    z=self.D[s]=self.fresh('bad_pair_or_cap_contains',s)
                    for row in self.exact_or(z,self.children(s,self.D,4)):yield phase,row
            phase='target_exact_containment';yield phase,None
            for s in range(self.full+1):
                if s.bit_count()==self.n-1:self.T[s]=self.Q[s]
                elif s.bit_count()>=self.n:
                    z=self.T[s]=self.fresh('target_contains',s)
                    for row in self.exact_or(z,self.children(s,self.T,self.n)):yield phase,row
        phase='no_covered_cup_transversal';yield phase,None
        for s in range(self.full+1):
            if s.bit_count()>self.limit:continue
            if self.variant=='direct':
                row=[-self.ids['orientation',t] for t in subs(s,3)]
                row.extend(-self.ends[v] for v in verts(s)[1:])
                row.extend(self.Q[t] for t in subs(self.full^s,self.n-1))
            else:
                row=[v for v in (self.D.get(s,0),self.T.get(self.full^s,0)) if v]
            yield phase,tuple(row)
        phase='no_small_blue_two_cup_partition';yield phase,None
        for s in range(self.full+1):
            blue=self.full^s
            if s.bit_count()<=self.n-1 and blue.bit_count()<=self.n-2:
                yield phase,tuple(-self.ids['orientation',t] for part in (s,blue) for t in subs(part,3))

def check(path,m,n,variant,tag):
    path=Path(path);mp=Path(str(path)+'.map')
    before={str(p):sha(p) for p in (path,mp)}
    f=Formula(m,n,variant)
    counts=collections.Counter();literals=collections.Counter();widths=collections.Counter()
    rebuilt=S/(tag+'.rebuilt.cnf');rebuilt_map=S/(tag+'.rebuilt.map')
    with path.open('rb') as original,rebuilt.open('xb') as out:
        header=original.readline();h=header.split()
        need(len(h)==4 and h[:2]==[b'p',b'cnf'],'DIMACS header')
        nv,nc=map(int,h[2:]);out.write(header)
        for phase,row in f.rows():
            if row is None:
                expected=f'c phase {phase}\n'.encode()
            else:
                expected=(' '.join(map(str,(*row,0)))+'\n').encode()
                need(all(0<abs(v)<=nv for v in row),'literal outside header')
                counts[phase]+=1;literals[phase]+=len(row);widths[phase]=max(widths[phase],len(row))
            need(original.readline()==expected,f'row mismatch {phase} {sum(counts.values())}')
            out.write(expected)
        need(not original.read(1),'extra CNF bytes')
        need(len(f.entries)==nv and sum(counts.values())==nc,'header counts')
    with mp.open('rb') as original,rebuilt_map.open('xb') as out:
        first=b'# id kind mask; indices are zero based in increasing x order\n'
        need(original.readline()==first,'map header');out.write(first)
        for v,kind,s in f.entries:
            line=f'{v} {kind} {s}\n'.encode()
            need(original.readline()==line,'map entry '+str(v));out.write(line)
        need(not original.read(1),'extra map entry')
    need(sha(rebuilt)==before[str(path)] and sha(rebuilt_map)==before[str(mp)],'full hash mismatch')
    need(before=={str(p):sha(p) for p in (path,mp)},'inputs changed')
    return {'status':'PASS','label':'COMPUTED','left_m':m,'right_m':n-4,'n':n,'variant':variant,
            'variables':nv,'clauses':nc,'literals':sum(literals.values()),
            'phase_rows':dict(counts),'phase_literals':dict(literals),'phase_max_width':dict(widths),
            'map_counts':dict(collections.Counter(kind for _,kind,_ in f.entries)),
            'cnf_map_byte_identical_rebuild':True,'hashes':before,
            'empty_End3_count':2,'option2_rows':counts['no_small_blue_two_cup_partition']}

def main():
    resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
    ap=argparse.ArgumentParser()
    ap.add_argument('path',type=Path);ap.add_argument('m',type=int);ap.add_argument('n',type=int)
    ap.add_argument('variant',choices=['direct','compact']);ap.add_argument('tag')
    a=ap.parse_args()
    (R/'data').mkdir(exist_ok=True);S.mkdir(exist_ok=True)
    result=check(a.path,a.m,a.n,a.variant,a.tag)
    result['peak_rss_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result['resource_limits']={'AS_MiB':300,'CPU_count':1,'wall_seconds':20,'CPU_seconds':19}
    save(R/'data'/(a.tag+'.json'),result)
    print(json.dumps(result))

if __name__=='__main__':main()
