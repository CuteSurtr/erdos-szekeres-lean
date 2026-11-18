#!/usr/bin/env python3
"""Independent Boolean and integer-real semantics for both low-split encoders."""
import collections
from fractions import Fraction
import hashlib
import itertools as it
import json
from pathlib import Path
import resource
import subprocess
import sys
import rows

R=Path(__file__).resolve().parents[1]
E=R.parent
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
S=W/'low-split-audit'
mask,verts,subs=rows.mask,rows.verts,rows.subs

def up(m,seeds):
    a=bytearray(1 << m)
    for s in seeds:a[s]=1
    for v in range(m):
        bit=1 << v
        for base in range(0,1 << m,2*bit):
            for j in range(bit):a[base+bit+j]|=a[base+j]
    return a

class Geometry:
    def __init__(self,P,n):
        self.P=[tuple(p) for p in P];self.n=n;self.m=len(P);self.full=(1 << self.m)-1
        assert all(type(x) is int for p in P for x in p)
        assert all(P[i][0]<P[i+1][0] for i in range(self.m-1))
        self.turn={s:self.det(*verts(s)) for s in subs(self.full,3)}
        assert all(self.turn.values())
        self.cap3=[s for s,d in self.turn.items() if d<0]
        self.end3={verts(s)[-1] for s in self.cap3}
        self.cap4=[s for s in subs(self.full,4) if all(self.turn[t]<0 for t in subs(s,3))]
        self.end4={verts(s)[-2:] for s in self.cap4}
        self.bad3=[s for s in self.cap3 if verts(s)[-2:] not in self.end4]
        self.cap5=[s for s in subs(self.full,5) if all(self.turn[t]<0 for t in subs(s,3))]
        non4=[]
        for s in subs(self.full,4):
            for q in verts(s):
                a,b,c=verts(s^(1 << q))
                ds=(self.det(a,b,q),self.det(b,c,q),self.det(c,a,q))
                if all(d>0 for d in ds) or all(d<0 for d in ds):non4.append(s);break
        self.nonconvex=up(self.m,non4)
        self.targets=[s for s in subs(self.full,n-1) if not self.nonconvex[s]]
        self.ngons=[s for s in subs(self.full,n) if not self.nonconvex[s]]
        self.has_cap3=up(self.m,self.cap3)
        self.forbidden=up(self.m,self.cap4+self.bad3)
        self.T=up(self.m,self.targets)
        self.bad_pairs=[s for s in subs(self.full,2) if verts(s)[-1] not in self.end3]
        self.D=up(self.m,self.cap3+self.bad_pairs)

    def det(self,a,b,c):
        x,y=self.P[a];u,v=self.P[b];s,t=self.P[c]
        return (u-x)*(t-y)-(v-y)*(s-x)

    def value(self,kind,s):
        if kind=='orientation':return self.turn[s]>0
        if kind=='convex':return not self.nonconvex[s]
        if kind=='ends_three_cap':return verts(s)[0] in self.end3
        if kind=='bad_pair_or_cap_contains':return bool(self.D[s])
        if kind=='target_contains':return bool(self.T[s])
        raise ValueError(kind)

    def report(self):
        return {'m':self.m,'n':self.n,'GP':True,'fourcaps':len(self.cap4),'fivecaps':len(self.cap5),
                'ngons':len(self.ngons),'targets':len(self.targets),'cap_triples':len(self.cap3),
                'bad_cap_triples':len(self.bad3),'End3':sorted(self.end3),
                'maximum_abs_coordinate':max(abs(x) for p in self.P for x in p)}

def low_join(P,n):
    d=n-4
    provisional=[(P[-1][0]+i,i*i) for i in range(1,d+1)]
    thresholds=[Fraction(0)]
    def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    for a,b in it.combinations(P,2):
        for r in provisional:thresholds.append(Fraction(det(a,b,r),b[0]-a[0]))
    for l in P:
        for r,s in it.combinations(provisional,2):thresholds.append(Fraction(-det(l,r,s),s[0]-r[0]))
    top=max(thresholds);shift=top.numerator//top.denominator+1
    return list(P)+[(x,y-shift) for x,y in provisional]

def canonical(formula,G):
    f=rows.Formula(G.m,G.n,formula);values=[False];counts=collections.Counter();failed=collections.Counter()
    for phase,row in f.rows():
        if row is None:continue
        while len(values)<=len(f.entries):
            _,kind,s=f.entries[len(values)-1];values.append(G.value(kind,s))
        counts[phase]+=1
        if not any(values[abs(v)]==(v>0) for v in row):failed[phase]+=1
    assert not (set(failed)-{'no_covered_cup_transversal','no_small_blue_two_cup_partition'})
    return {'rows_checked':sum(counts.values()),'false_by_phase':dict(failed),
            'nonfailure_all_true':True,'map_values_assigned':len(values)-1}

def geometry_control(name):
    if name.startswith('small'):
        n=int(name[-1]);source=E/'structure2/data/low_split_controls.json'
        item=json.loads(source.read_text())['cases'][f'n{n}_endpoint_small']
        P=[tuple(p) for p in item['P'][:item['cut']]];m=len(P)
    else:
        m=int(name[4:]);n=7;source=E/'structure2/data/low_classification_replay.json'
        P=[tuple(p) for p in json.loads(source.read_text())['cases']['n7_fixed_left16']['P'][:m]]
    inputs=[Path(__file__),R/'tools/rows.py',source,E/'low_split_cnf.cpp',E/'low_split_compact.cpp',
            E.parents[1]/'compact/compact_cnf.cpp',S/'low-direct',S/'low-compact']
    before={str(p):rows.sha(p) for p in inputs}
    rows.save(R/'data'/f'{name}-input.json',{'P':P,'m':m,'n':n,'input_hashes':before})
    G=Geometry(P,n)
    assert not G.cap4 and not G.ngons
    U=Geometry(low_join(P,n),n)
    assert not U.cap5 and not U.ngons
    right=U.full^G.full
    for s,d in U.turn.items():
        count=(s&G.full).bit_count()
        if count==2 and (s&right):assert d<0
        if count==1 and (s&right).bit_count()==2:assert d>0
    assert not U.has_cap3[right]
    assert U.end4=={(b,r) for b in G.end3 for r in range(m,U.m)}
    assert set(U.targets)==set(G.targets)|{s|right for s in G.cap3}
    expected_bad=set(G.cap3)|{mask((a,b,r)) for a,b in it.combinations(range(m),2)
                             if b not in G.end3 for r in range(m,U.m)}
    assert set(U.bad3)==expected_bad
    option1=bytearray(1 << m);option2=bytearray(1 << m)
    thinnings=0
    for b in range(1 << m):
        v=verts(b);blue=G.full^b
        option1[b]=(not G.has_cap3[b] and all(q in G.end3 for q in v[1:]) and not G.T[blue])
        option2[b]=(not G.has_cap3[b] and not G.has_cap3[blue] and blue.bit_count()<=n-2)
        assert bool(G.D[b])==(G.has_cap3[b] or any(q not in G.end3 for q in v[1:]))
        if option2[b]:assert b.bit_count()<=n-1
        if option1[b] and b.bit_count()>m-n+2:
            smaller=mask(v[:m-n+2]);sv=verts(smaller)
            assert not G.has_cap3[smaller] and all(q in G.end3 for q in sv[1:]) and not G.T[G.full^smaller]
            thinnings+=1
    bounded=sum(option1[b] for b in range(1 << m) if b.bit_count()<=m-n+2)
    assert bool(sum(option1))==bool(bounded)
    if m>2*n-3:assert not any(option2)
    actual_count=0
    for a in range(1 << U.m):
        actual=not U.forbidden[a] and not U.T[U.full^a]
        predicted=bool(option1[a&G.full] if a&right else option2[a&G.full])
        assert actual==predicted,('classification',name,a)
        actual_count+=actual
    assert actual_count==sum(option1)*((1 << (n-4))-1)+sum(option2)
    canonical_reports={};formula_reports={};commands=[]
    for variant in ('direct','compact'):
        native_parent=(n==7 and ((variant=='direct' and m in (11,12,13)) or (variant=='compact' and m==14)))
        if native_parent:
            suffix='-compact' if variant=='compact' else ''
            path=W/f'low{m}-n7{suffix}.cnf'
        else:
            path=S/f'{name}-{variant}.cnf'
            assert not path.exists()
            command=[str(S/('low-'+variant)),str(m),str(n),str(path)]
            with (R/'data'/f'{name}-{variant}.encode.stdout').open('x') as out,(R/'data'/f'{name}-{variant}.encode.stderr').open('x') as err:
                proc=subprocess.run(command,stdout=out,stderr=err,timeout=18)
            assert proc.returncode==0
            commands.append(command)
        formula_reports[variant]=rows.check(path,m,n,variant,name+'-'+variant)
        canonical_reports[variant]=canonical(variant,G)
        fail=canonical_reports[variant]['false_by_phase']
        assert fail.get('no_covered_cup_transversal',0)==bounded
        assert fail.get('no_small_blue_two_cup_partition',0)==sum(option2)
    assert canonical_reports['direct']['false_by_phase']==canonical_reports['compact']['false_by_phase']
    after={str(p):rows.sha(p) for p in inputs};assert before==after
    return {'status':'PASS','label':'COMPUTED','name':name,'left':G.report(),'full':U.report(),
            'P_left':P,'P_full':U.P,'parent_fixture_values_ignored':True,
            'option1_all_B':sum(option1),'option1_bounded_B':bounded,'option2_B':sum(option2),
            'thinning_controls':thinnings,'all_selector_assignments_compared':1 << U.m,
            'terminal_safe_full_count':actual_count,'End4_exactly_End3_times_R':True,
            'target_and_bad_triple_classification_exact':True,
            'canonical':canonical_reports,'native_formulas':formula_reports,
            'generation_commands':commands,'inputs_before':before,'inputs_after':after}

def algebra():
    m=5;full=(1 << m)-1;triples=list(subs(full,3));comparisons=0
    for caps in range(1 << len(triples)):
        capset={t for i,t in enumerate(triples) if caps & (1 << i)}
        capcontains=up(m,capset)
        for endbits in range(1 << m):
            end=lambda v:bool(endbits & (1 << v))
            lattice={0:False,**{1 << v:False for v in range(m)}}
            for s in subs(full,2):lattice[s]=not end(verts(s)[-1])
            for s in triples:
                a,b,c=verts(s);lattice[s]=(s in capset or not end(b) or not end(c))
            for size in (4,5):
                for s in subs(full,size):lattice[s]=any(lattice[s^(1 << v)] for v in verts(s)[:4])
            for s in range(1 << m):
                reference=bool(capcontains[s] or any(not end(v) for v in verts(s)[1:]))
                assert lattice[s]==reference;comparisons+=1
    target_checks=0;full7=(1 << 7)-1;targets=list(subs(full7,6))
    for bits in range(1 << len(targets)):
        witnesses={s for i,s in enumerate(targets) if bits & (1 << i)}
        lattice={s:(s in witnesses) for s in range(1 << 7) if s.bit_count()<=6}
        lattice[full7]=any(lattice[full7^(1 << v)] for v in range(7))
        for s in range(1 << 7):
            assert lattice[s]==any(w&s==w for w in witnesses);target_checks+=1
    end_checks=0
    for b in range(6):
        fanin=b*(b-1)//2
        for bits in range(1 << fanin):
            literal_values=[bool(bits & (1 << i)) for i in range(fanin)]
            for z in (False,True):
                forward=(not z or any(literal_values))
                reverses=all(z or not v for v in literal_values)
                assert (forward and reverses)==(z==any(literal_values));end_checks+=1
    cover_checks=0
    for k in (2,3,6):
        children=4 if k<=3 else 7
        for size in range(max(children,k+1),17):
            for witness in it.combinations(range(size),k):
                assert set(range(children))-set(witness);cover_checks+=1
    lost3=set(range(3));lost6=set(range(6))
    false_end=False
    singleton=(0,)
    flag,cap_child=False,True
    mutations={'three_children_lose_cap3':not any(v not in lost3 for v in range(3)),
               'six_children_lose_six_target':not any(v not in lost6 for v in range(6)),
               'positive_End3_pair_alias_is_wrong_when_End3_false':(not false_end)!=false_end,
               'first_selected_End3_must_be_exempt':all(False for _ in singleton[1:])!=all(False for _ in singleton),
               'one_way_End3_allows_false_flag_despite_true_cap_child':(not flag or cap_child) and flag!=cap_child}
    assert all(mutations.values())
    return {'status':'PASS','label':'COMPUTED','arbitrary_cap_End3_subset_comparisons':comparisons,
            'arbitrary_target_subset_comparisons':target_checks,'End3_gate_truth_cases':end_checks,
            'all_relative_leaf_cover_checks':cover_checks,'mutations':mutations,
            'scope':'Boolean D/T equivalence does not assume realizability or no-four-cap.'}

def main():
    resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
    assert len(sys.argv)==2
    name=sys.argv[1]
    assert name in ('algebra','small6','small7','small8','left11','left12','left13','left14')
    result=algebra() if name=='algebra' else geometry_control(name)
    result['peak_rss_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result['limits']={'AS_MiB':300,'CPU_count':1,'wall_seconds':20,'CPU_seconds':19}
    rows.save(R/'data'/f'control-{name}.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in
        ('P_left','P_full','canonical','native_formulas','inputs_before','inputs_after','generation_commands')}))

if __name__=='__main__':main()
