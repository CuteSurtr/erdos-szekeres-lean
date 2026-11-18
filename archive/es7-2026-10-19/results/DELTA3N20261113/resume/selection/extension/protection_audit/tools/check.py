#!/usr/bin/env python3
"""Independent streamed reconstruction; no parent or previous checker import."""
import argparse
import collections
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import resource

ROOT=Path('/home/jay/research/lean/erdos-szekeres-lean')
SEL=ROOT/'cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection'
RECORD=SEL/'extension/protection_audit'
SCRATCH=Path('/home/jay/research/data/delta3-codex-20261113/extension/protection-audit')
BLOCKS=[(0,0),(1,-1),(2,-3),(3,-6),(10,500),(11,600),(12,699),(13,797)]
TWO=[(0,0),(1,1),(2,0),(3,4),(4,-3),(5,10),(6,-2),(7,5)]

def need(ok,msg):
    if not ok: raise ValueError(msg)

def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def verts(s): return tuple(i for i in range(s.bit_length()) if s&(1<<i))
def mask(t): return sum(1<<i for i in t)
def comb(s,k): return (mask(t) for t in itertools.combinations(verts(s),k))

class Geometry:
    def __init__(self,p,n,variant):
        self.p=p;self.n=n;self.variant=variant;self.m=len(p);self.full=(1<<self.m)-1
        need(all(p[i][0]<p[i+1][0] for i in range(self.m-1)),'x_order')
        self.sign={s:self.det(*verts(s)) for s in comb(self.full,3)}
        need(all(self.sign.values()),'collinear')
        self.cap4={s for s in comb(self.full,4) if self.cap(s)}
        self.end={verts(s)[-2:] for s in self.cap4}
        self.non4=set()
        for s in comb(self.full,4):
            for q in verts(s):
                a,b,c=verts(s^(1<<q))
                d=(self.det(a,b,q),self.det(b,c,q),self.det(c,a,q))
                if all(x>0 for x in d) or all(x<0 for x in d): self.non4.add(s);break
        self.targets={s for s in comb(self.full,n-1) if self.convex(s)}
        self.covered={q:any(self.protect(q,t) for t in self.end) for q in itertools.combinations(range(self.m),2)}
        self.bad={s for s in comb(self.full,3) if self.cap(s) and not self.covered[verts(s)[-2:]]}
        self.D=self.up(self.cap4|self.bad);self.T=self.up(self.targets)
        need(not any(self.cap(s) for s in comb(self.full,5)),'five_cap')
        need(not any(self.convex(s) for s in comb(self.full,n)),'n_gon')
    def det(self,a,b,c):
        p,q,r=self.p[a],self.p[b],self.p[c]
        return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    def cap(self,s): return all(self.sign[t]<0 for t in comb(s,3))
    def cup(self,s): return all(self.sign[t]>0 for t in comb(s,3))
    def convex(self,s): return all(t not in self.non4 for t in comb(s,4))
    def up(self,seeds):
        a=bytearray(1<<self.m)
        for s in seeds:a[s]=1
        for i in range(self.m):
            for s in range(1<<self.m):
                if s&(1<<i):a[s]|=a[s^(1<<i)]
        return a
    def difference(self,query,support,x):
        # Direct line difference with positive common denominator; no orientation predicate.
        b,c=query;u,v=support;p=self.p
        dx=p[c][0]-p[b][0];ex=p[v][0]-p[u][0]
        qy=p[b][1]*dx+(p[c][1]-p[b][1])*(x-p[b][0])
        sy=p[u][1]*ex+(p[v][1]-p[u][1])*(x-p[u][0])
        return sy*dx-qy*ex
    def endpoint(self,q,t):
        if q==t:return True
        endpoints=q+t
        left=self.difference(q,t,self.p[min(endpoints)][0])
        right=self.difference(q,t,self.p[max(endpoints)][0])
        return left<=0<=right and (left<0 or right>0)
    def protect(self,q,t):
        if q==t:return True
        if self.variant=='cup':
            return t[0]>=q[0] and t[1]>=q[1] and self.cup(mask(set(q+t)))
        return self.endpoint(q,t)
    def value(self,kind,s):
        v=verts(s)
        if kind=='orientation':return self.sign[s]>0
        if kind=='convex':return self.convex(s)
        if kind=='terminal_fourcap':return s in self.cap4
        if kind=='terminal_fourcup':return self.cup(s)
        if kind=='end_fourcap':return v in self.end
        if kind.startswith('cup_support_'):
            u,w=map(int,kind.split('_')[2:]);return (u,w) in self.end and self.cup(s)
        if kind.startswith('forced_support_'):
            b,c,u,w=map(int,kind.split('_')[2:]);return (u,w) in self.end and self.endpoint((b,c),(u,w))
        if kind=='covered_pair':return self.covered[v]
        if kind=='uncovered_cap_triple':return s in self.bad
        if kind=='bad_contains':return bool(self.D[s])
        if kind=='target_contains':return bool(self.T[s])
        raise ValueError('unknown_kind_'+kind)

class Audit:
    def __init__(self,path,m,n,variant,tag,geometry=None,baseline=None):
        self.path=Path(path);self.map_path=Path(str(path)+'.map');self.m=m;self.n=n;self.variant=variant
        self.full=(1<<m)-1;self.amax=m-n+2;self.tag=tag;self.geometry=geometry
        self.before={str(p):sha(p) for p in (self.path,self.map_path)}
        self.f=self.path.open();self.mapping=self.map_path.open();self.header=self.f.readline()
        h=self.header.split();need(h[:2]==['p','cnf'] and len(h)==4,'header')
        self.nv,self.nc=map(int,h[2:]);self.v=0;self.count=0;self.lits=0;self.phase=None;self.pending=None
        self.ids={};self.values=[False];self.kind_counts=collections.Counter();self.counts=collections.Counter()
        self.false=collections.Counter();self.records=[];self.end_empty=0;self.support_reuses=0
        self.body=(SCRATCH/(tag+'.rebuilt.cnf')).open('x');self.body.write(self.header)
        self.mapout=(SCRATCH/(tag+'.rebuilt.map')).open('x')
        comment='# id kind mask; indices are zero based in increasing x order\n'
        need(self.mapping.readline()==comment,'map_header');self.mapout.write(comment)
        for s in comb(self.full,3): self.fresh('orientation',s)
        for k in range(4,n):
            for s in comb(self.full,k): self.fresh('convex',s)
        self.geometry_variables=self.v
        prefix=[]
        first='c phase '+('fourcap_and_fourcup_equivalence' if variant=='cup' else 'fourcap_equivalence')+'\n'
        allowed={'signotope','no5cap','convex4_equivalence','convex_larger_equivalence','no_ngon'}
        while True:
            line=self.f.readline();need(bool(line),'missing_new_phase')
            if line==first:self.pending=line;break
            prefix.append(line);self.body.write(line)
            if line.startswith('c phase '):
                self.phase=line.split()[2];need(self.phase in allowed,'extra_geometric_phase')
            else:self.observe(line)
        self.prefix=''.join(prefix).encode();self.prefix_sha=hashlib.sha256(self.prefix).hexdigest()
        if baseline:
            old=[]
            with Path(baseline).open() as f:
                f.readline()
                for line in f:
                    if line=='c phase terminal_fourcap_equivalence\n':break
                    old.append(line)
            need(''.join(old).encode()==self.prefix,'geometry_prefix_changed')
        self.baseline=str(baseline) if baseline else None
        self.geometry_clauses=self.count
    def fresh(self,kind,s):
        self.v+=1;key=(kind,s);need(key not in self.ids,'duplicate_map_key')
        self.ids[key]=self.v;self.kind_counts[kind.split('_support_')[0]+'_support' if '_support_' in kind else kind]+=1
        row=f'{self.v} {kind} {s}\n'
        need(self.mapping.readline()==row,f'map_mismatch_{self.v}_{kind}_{s}')
        self.mapout.write(row)
        if self.geometry:self.values.append(self.geometry.value(kind,s))
        return self.v
    def get(self,kind,s):return self.ids[kind,s]
    def orientation(self,*t):
        need(len(set(t))==3,'degenerate_orientation')
        inv=sum(t[i]>t[j] for i in range(3) for j in range(i+1,3))
        return (-1 if inv%2 else 1)*self.get('orientation',mask(t))
    def take(self):
        if self.pending is not None:x=self.pending;self.pending=None;return x
        return self.f.readline()
    def phase_start(self,phase):
        line=f'c phase {phase}\n';need(self.take()==line,'phase_mismatch_'+phase)
        self.body.write(line);self.phase=phase
    def observe(self,line):
        a=list(map(int,line.split()));need(a and a[-1]==0 and all(0<abs(v)<=self.nv for v in a[:-1]),'bad_DIMACS')
        clause=tuple(a[:-1]);self.count+=1;self.lits+=len(clause);self.counts[self.phase]+=1
        if self.geometry:
            ok=any(self.values[abs(v)]==(v>0) for v in clause)
            if not ok:self.false[self.phase]+=1
            if self.phase not in {'signotope','no5cap','convex4_equivalence','convex_larger_equivalence','no_ngon'}:
                self.records.append((self.phase,clause))
    def row(self,c):
        line=' '.join(map(str,(*c,0)))+'\n';actual=self.take()
        need(actual==line,f'clause_mismatch_{self.count+1}_{self.phase}: {actual.strip()} != {line.strip()}')
        self.body.write(line);self.observe(line)
    def conjunction(self,z,xs):
        for x in xs:self.row((-z,x))
        self.row((z,*[-x for x in xs]))
    def exact_or(self,z,xs):
        self.row((-z,*xs))
        for x in xs:self.row((-x,z))
    def generate(self):
        cap={};cup={};end={};covered={};A={};B={}
        pairs=list(itertools.combinations(range(self.m),2))
        self.phase_start('fourcap_and_fourcup_equivalence' if self.variant=='cup' else 'fourcap_equivalence')
        for s in comb(self.full,4):
            cap[s]=self.fresh('terminal_fourcap',s)
            if self.variant=='cup':cup[s]=self.fresh('terminal_fourcup',s)
            signs=[self.get('orientation',t) for t in comb(s,3)]
            self.conjunction(cap[s],[-x for x in signs])
            if self.variant=='cup':self.conjunction(cup[s],signs)
        self.phase_start('ambient_terminal_pair_equivalence')
        for b,c in pairs:
            end[b,c]=self.fresh('end_fourcap',mask((b,c)))
            xs=[cap[mask((u,v,b,c))] for u,v in itertools.combinations(range(b),2)]
            self.end_empty+=not xs;self.exact_or(end[b,c],xs)
        self.phase_start('cup_domination_equivalence' if self.variant=='cup' else 'forced_domination_equivalence')
        cache={}
        for b,c in pairs:
            xs=[end[b,c]]
            # Reconstruct candidate relations from all ordered pairs, rather
            # than copying the encoder's nested endpoint loops.
            candidates=[(u,v) for u,v in pairs if v>=c and (u,v)!=(b,c) and u>=2 and v>=3
                        and (self.variant=='forced' or u>=b)]
            candidates.sort(key=(lambda t:(t[1],t[0])) if self.variant=='forced' else (lambda t:t))
            for u,v in candidates:
                union=mask(set((b,c,u,v)))
                if self.variant=='cup':
                    cp=self.get('orientation',union) if union.bit_count()==3 else cup[union]
                    key=(end[u,v],cp)
                    if key in cache:z=cache[key];self.support_reuses+=1
                    else:
                        z=self.fresh(f'cup_support_{u}_{v}',union);self.conjunction(z,key);cache[key]=z
                else:
                    z=self.fresh(f'forced_support_{b}_{c}_{u}_{v}',union)
                    condition=[end[u,v]]
                    # d(v)>=0 and d(min(b,u))<=0, converted by permutation
                    # signs of determinants. Shared endpoints give equality.
                    if v>c:condition.append(self.orientation(b,c,v))
                    if u>b:condition.append(self.orientation(u,v,b))
                    elif u<b:condition.append(-self.orientation(b,c,u))
                    self.conjunction(z,condition)
                xs.append(z)
            covered[b,c]=self.fresh('covered_pair',mask((b,c)));self.exact_or(covered[b,c],xs)
        self.phase_start('uncovered_cap_triple_equivalence')
        for s in comb(self.full,3):
            a,b,c=verts(s);z=self.fresh('uncovered_cap_triple',s)
            if self.amax>=3:A[s]=z
            self.conjunction(z,[-self.orientation(a,b,c),-covered[b,c]])
        self.phase_start('bad_triple_or_fourcap_containment')
        for s in range(1<<self.m):
            k=s.bit_count()
            if 4<=k<=self.amax:
                A[s]=self.fresh('bad_contains',s)
                xs=[A[s^(1<<v)] for v in verts(s)[:4 if k==4 else 5]]
                if k==4:xs.append(cap[s])
                self.row((-A[s],*xs))
        self.phase_start('target_containment')
        for s in range(1<<self.m):
            k=s.bit_count()
            if k==self.n-1:B[s]=self.get('convex',s)
            elif k>=self.n:
                B[s]=self.fresh('target_contains',s)
                self.row((-B[s],*[B[s^(1<<v)] for v in verts(s)[:self.n]]))
        self.phase_start('forall_'+self.variant+'_protected_delta')
        for s in range(1<<self.m):
            if s.bit_count()<=self.amax:self.row(tuple(v for v in (A.get(s),B.get(self.full^s)) if v))
        self.phase_start('fixed_signs')
        need(self.take()=='','extra_CNF_data');need(self.mapping.readline()=='','extra_map_data')
        need(self.v==self.nv and self.count==self.nc,'header_count_mismatch')
        self.body.close();self.mapout.close();self.f.close();self.mapping.close()
        need(sha(SCRATCH/(self.tag+'.rebuilt.cnf'))==sha(self.path),'rebuilt_CNF_hash')
        need(sha(SCRATCH/(self.tag+'.rebuilt.map'))==sha(self.map_path),'rebuilt_map_hash')
        need(self.before=={str(p):sha(p) for p in (self.path,self.map_path)},'input_changed')
        need(set(self.false)<= {'forall_'+self.variant+'_protected_delta'},'canonical_nonfailure_rejected')
        return dict(status='PASS',label='COMPUTED',variant=self.variant,m=self.m,n=self.n,variables=self.v,
            clauses=self.count,literals=self.lits,geometry_variables=self.geometry_variables,geometry_clauses=self.geometry_clauses,
            new_clauses=self.count-self.geometry_clauses,geometry_prefix_sha256=self.prefix_sha,
            geometry_reference=self.baseline,map_kind_counts=dict(self.kind_counts),phase_counts=dict(self.counts),
            empty_End4_ORs=self.end_empty,cup_support_cache_reuses=self.support_reuses,
            canonical_geometry_checked=self.geometry is not None,false_failure_rows=dict(self.false),
            input_hashes=self.before,streamed_rows_and_map_byte_identical=True)

def named_geometry(name,n,variant):
    if name=='blocks':p=BLOCKS
    elif name=='two':p=TWO
    elif name=='first13':
        w=list(map(int,(SEL/'extension/subset_audit/data/ambient.points').read_text().split()))
        p=list(zip(w[2::2],w[3::2]))[:13]
    elif name=='none':return None
    else:raise ValueError('fixture_name')
    return Geometry(p,n,variant)

def semantic_controls():
    out={};schema=0
    for kind in ('or','and'):
        for width in range(8):
            for pattern in range(1<<width):
                leaves=[bool(pattern&(1<<i)) for i in range(width)]
                correct=any(leaves) if kind=='or' else all(leaves)
                for z in (False,True):
                    if kind=='or':ok=(not z or any(leaves)) and all(not x or z for x in leaves)
                    else:ok=all(not z or x for x in leaves) and (z or any(not x for x in leaves))
                    need(ok==(z==correct),'definition_schema');schema+=1
    for variant in ('cup','forced'):
        g=Geometry(BLOCKS,5,variant);first4=15;first5=31
        need(g.cap4=={15,240},'block_cap4_list')
        mixed=[t for t in comb(255,3) if (t&15) and (t&240)]
        need(all(g.sign[t]>0 for t in mixed),'mixed_not_cups')
        need(all(t not in g.bad for t in comb(first5,3)),'block_triple_unprotected')
        need(g.D[first4] and g.D[first5] and not g.T[255^first5],'old_cap_control')
        children=[first5^(1<<v) for v in verts(first5)]
        need(not any(g.D[c] for c in children[:4]) and g.D[children[4]],'five_children_control')
        q=Geometry(BLOCKS,7,variant)
        need(not q.T[255^first4] and not any(t in q.bad for t in comb(first4,3)),'n7_block_control')
        h=Geometry(TWO,7,variant);selection=mask((0,3,6))
        need(selection in h.bad and not h.covered[3,6],'two_support_not_bad')
        need(not h.T[255^selection] and not any(c&selection==c for c in h.cap4),'two_not_weak_delta')
        def line(t):
            a,b=t;s=Fraction(TWO[b][1]-TWO[a][1],TWO[b][0]-TWO[a][0])
            return s,Fraction(TWO[a][1])+s*(7-TWO[a][0])
        target=line((3,6));supports={str(t):line(t) for t in sorted(h.end)}
        need(all(not(s>=target[0] and y>=target[1]) for s,y in supports.values()),'single_support_exists')
        left,right=line((2,4)),line((5,7))
        need((left[0]+right[0])/2==target[0] and (left[1]+right[1])/2-target[1]==Fraction(11,4),'uniform_identity')
        out[variant]=dict(blocks=dict(points=BLOCKS,mixed_cup_triples=len(mixed),cap4_masks=sorted(g.cap4),
            no_five_cap=True,no_five_gon=True,n7_A15_hits_targets=True,n7_A15_all_cap_triples_protected=True,
            n5_A31_hits_targets=True,n5_A31_all_cap_triples_protected=True,old_cap_still_forbidden=True,
            canonical_A4=bool(g.D[15]),canonical_A5=bool(g.D[31]),four_child_mutation_would_fail=True),
            two_support=dict(points=TWO,A=selection,ordinary_weak_Delta=True,uniform_margin='11/4',
                single_line_dominator=False,covered_36=False,bad_036=True,
                target_line=list(map(str,target)),ambient_lines={k:list(map(str,v)) for k,v in supports.items()}))
    # Mixed witnesses of sizes three and four: every witness must survive
    # one of FIVE deletions; four deletions miss a four-element witness.
    covers=0
    for size in range(5,11):
        parent=(1<<size)-1;children=[parent^(1<<v) for v in range(5)]
        for k in (3,4):
            for witness in comb(parent,k):
                need(any(witness&c==witness for c in children),'mixed_cover');covers+=1
    out.update(status='PASS',label='COMPUTED',exact_gate_truth_assignments=schema,mixed_witness_cover_checks=covers,
               global_size_monotonicity_claim=False)
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['rows','semantics'])
    ap.add_argument('--variant',choices=['cup','forced']);ap.add_argument('--m',type=int);ap.add_argument('--n',type=int)
    ap.add_argument('--cnf',type=Path);ap.add_argument('--baseline',type=Path);ap.add_argument('--fixture',default='none');ap.add_argument('--tag',required=True)
    a=ap.parse_args();dest=RECORD/'data'/f'{a.tag}.json';need(not dest.exists(),'receipt_exists')
    if a.mode=='semantics':result=semantic_controls()
    else:
        g=named_geometry(a.fixture,a.n,a.variant)
        audit=Audit(a.cnf,a.m,a.n,a.variant,a.tag,g,a.baseline)
        result=audit.generate()
        if g:
            result['fixture']=dict(name=a.fixture,points=g.p,cap4=len(g.cap4),bad_triples=len(g.bad),targets=len(g.targets))
            # Check the actual emitted A4/A5 rows reject the missing-cap and
            # too-short-cover mutations on the supplied block geometry.
            if a.fixture=='blocks' and a.n==5:
                z4=audit.get('bad_contains',15);z5=audit.get('bad_contains',31);cap=audit.get('terminal_fourcap',15)
                rows={-c[0]:c for phase,c in audit.records if phase=='bad_triple_or_fourcap_containment'}
                r4=rows[z4];r5=rows[z5]
                def holds(c):return any(audit.values[abs(v)]==(v>0) for v in c)
                need(holds(r4) and holds(r5),'actual_canonical_A_rows')
                need(not holds(tuple(v for v in r4 if v!=cap)),'missing_cap_mutation_not_rejected')
                need(not holds(r5[:-1]),'four_children_mutation_not_rejected')
                result['actual_row_mutations']=dict(A4=list(r4),without_cap=[v for v in r4 if v!=cap],
                    A5=list(r5),four_children=list(r5[:-1]),both_mutations_rejected=True)
    dest.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('points','input_hashes')}))

if __name__=='__main__':
    resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20))
    main()
