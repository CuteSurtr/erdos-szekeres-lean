#!/usr/bin/env python3
"""Stream-check every model literal, semantic flag, formula row and subset.

No parent encoder/checker or earlier audit implementation is imported.
"""
from array import array
from collections import Counter
from itertools import combinations, zip_longest
import json
from pathlib import Path
import resource
import time
import traceback

from geometry import bits, vertices, upwards, digest

HERE=Path(__file__).resolve().parent
CASE=Path('/home/jay/research/data/delta3-codex-20261113/extension/terminal7-a/m15')
M,N,K=15,7,10
FULL=(1<<M)-1


def masks(k):return (bits(t) for t in combinations(range(M),k))


def mapping_order():
    for s in masks(3):yield 'orientation',s
    for k in (4,5,6):
        for s in masks(k):yield 'convex',s
    for s in masks(4):yield 'terminal_fourcap',s
    for s in masks(3):yield 'terminal_bad_triple',s
    for s in range(FULL+1):
        if 4<=s.bit_count()<=K:yield 'bad_contains',s
    for s in range(FULL+1):
        if s.bit_count()>=N:yield 'target_contains',s


def load():
    with (CASE/'input.cnf').open() as f:
        head=f.readline().split();assert head[:2]==['p','cnf']
        nv,nc=map(int,head[2:])
    assignment=bytearray([2])*(nv+1);occurrences=0;statuses=[]
    with (CASE/'solve/cadical.log').open() as f:
        for line in f:
            if line.startswith('s '):statuses.append(line.strip())
            if line.startswith('v '):
                for literal in map(int,line.split()[1:]):
                    if not literal:continue
                    i=abs(literal);v=int(literal>0)
                    assert 1<=i<=nv and assignment[i] in (2,v)
                    assignment[i]=v;occurrences+=1
    assert statuses==['s SATISFIABLE'] and 2 not in assignment[1:]
    kinds=('orientation','convex','terminal_fourcap','terminal_bad_triple','bad_contains','target_contains')
    ids={kind:array('I',[0])*(FULL+1) for kind in kinds}
    count=0
    with (CASE/'input.cnf.map').open() as f:
        entries=(line.split() for line in f if not line.startswith('#') and line.strip())
        for i,(expected,entry) in enumerate(zip_longest(mapping_order(),entries),1):
            assert expected is not None and entry is not None
            kind,s=expected
            assert entry==[str(i),kind,str(s)],(i,expected,entry)
            ids[kind][s]=i;count+=1
    assert count==nv
    return nv,nc,assignment,ids,occurrences


def semantic(assignment,ids):
    signs={s:bool(assignment[ids['orientation'][s]]) for s in masks(3)}
    nonconvex4=[];cap4=[];packets=0
    for s in masks(4):
        p=[signs[bits(t)] for t in combinations(vertices(s),3)]
        assert sum(p[i]!=p[i+1] for i in range(3))<=1
        packets+=1
        if p[0]!=p[1] or p[2]!=p[3]:nonconvex4.append(s)
        if not any(p):cap4.append(s)
    cap5=[s for s in masks(5) if all(not signs[bits(t)] for t in combinations(vertices(s),3))]
    assert not cap5
    nonconvex=upwards(M,nonconvex4)
    targets=[s for s in masks(6) if not nonconvex[s]]
    ngons=[s for s in masks(7) if not nonconvex[s]];assert not ngons
    terminal_pairs={vertices(s)[-2:] for s in cap4}
    bad=[s for s,v in signs.items() if not v and vertices(s)[-2:] not in terminal_pairs]
    D,F,T=(upwards(M,seeds) for seeds in (bad,cap4,targets))
    capset,badset=set(cap4),set(bad)
    canonical=bytearray(len(assignment));flag_counts={}
    for kind,table in ids.items():
        counts=Counter()
        for s,i in enumerate(table):
            if not i:continue
            if kind=='orientation':v=signs[s]
            elif kind=='convex':v=not nonconvex[s]
            elif kind=='terminal_fourcap':v=s in capset
            elif kind=='terminal_bad_triple':v=s in badset
            elif kind=='bad_contains':v=bool(D[s])
            elif kind=='target_contains':v=bool(T[s])
            canonical[i]=int(v);counts['variables']+=1
            counts['model_true']+=bool(assignment[i]);counts['canonical_true']+=v
            if kind in ('bad_contains','target_contains'):
                assert not assignment[i] or v,(kind,s,'false positive containment')
                counts['true_witness_with_false_flag']+=bool(v and not assignment[i])
            else:assert bool(assignment[i])==v,(kind,s,'inexact leaf/convex flag')
        flag_counts[kind]=dict(counts)
    weak=[];terminal=[];failures=Counter();retained=Counter()
    for s in range(FULL+1):
        assert D[s] or not F[s]
        if not F[s] and not T[FULL^s]:weak.append(s)
        if not D[s] and not T[FULL^s]:terminal.append(s)
        reason='both' if D[s] and T[FULL^s] else 'bad_triple' if D[s] else 'missed_target' if T[FULL^s] else 'works'
        failures[reason]+=1
        if s.bit_count()<=K:retained[reason]+=1
    assert not terminal and weak
    rooted=[]
    for root in range(M):
        choices=[s for s in weak if s>>root&1]
        chosen=min(choices,key=lambda s:(s.bit_count(),s)) if choices else None
        rooted.append({'root':root,'minimum_size':chosen.bit_count() if chosen is not None else None,
                       'weak_delta':vertices(chosen) if chosen is not None else None})
    report={'signotope_packets':packets,'five_caps':len(cap5),'convex_seven_subsets':len(ngons),
            'four_caps':len(cap4),'bad_triples':len(bad),'convex_six_subsets':len(targets),
            'auxiliary_counts':flag_counts,'all_subsets_checked':FULL+1,
            'terminal_safe_deltas':len(terminal),'failure_reasons':dict(failures),
            'retained_failure_reasons':dict(retained),'weak_deltas':len(weak),
            'weak_delta_size_counts':dict(sorted(Counter(s.bit_count() for s in weak).items())),
            'rooted_weak_deltas':rooted,'signs':''.join('+' if v else '-' for v in signs.values())}
    # This compares independent abstract all-four-subset semantics with the
    # coordinate/hull replay, not auxiliary values from the SAT model.
    real=json.loads((HERE/'data/real15.geometry.json').read_text())['result']
    for key in ('five_caps','convex_seven_subsets','four_caps','bad_triples','convex_six_subsets',
                'all_subsets_checked','terminal_safe_deltas','failure_reasons','weak_deltas','signs'):
        assert real[key]==report[key],key
    assert real['weak_delta_size_counts']=={str(k):v for k,v in report['weak_delta_size_counts'].items()}
    assert real['rooted_weak_deltas']==[dict(r,weak_delta=list(r['weak_delta']) if r['weak_delta'] is not None else None) for r in rooted]
    return canonical,report


def formula(ids):
    t,Q,F,B,A,T=(ids[k] for k in ('orientation','convex','terminal_fourcap','terminal_bad_triple','bad_contains','target_contains'))
    def conj(z,terms):
        for a in terms:yield (-z,a)
        yield (z,*(-a for a in terms))
    def bad(s):return B[s] if s.bit_count()==3 else A[s]
    def target(s):return Q[s] if s.bit_count()==6 else T[s]
    for s in masks(4):
        packet=[t[bits(q)] for q in combinations(vertices(s),3)]
        for a,b,c in combinations(packet,3):
            yield 'signotope',(-a,b,-c)
            yield 'signotope',(a,-b,c)
    for s in masks(5):
        v=vertices(s)
        yield 'no5cap',tuple(t[bits(v[i:i+3])] for i in range(3))
    for s in masks(4):
        z=Q[s];a,b,c,d=(t[bits(q)] for q in combinations(vertices(s),3))
        for row in ((-z,-a,b),(-z,a,-b),(-z,-c,d),(-z,c,-d),(z,a,d),(z,-a,-d),(z,b,-c),(z,-b,c)):
            yield 'convex4_equivalence',row
    for k in (5,6):
        for s in masks(k):
            for row in conj(Q[s],[Q[s^(1<<v)] for v in vertices(s)[:5]]):
                yield 'convex_larger_equivalence',row
    for s in masks(7):
        yield 'no_ngon',tuple(-Q[s^(1<<v)] for v in vertices(s)[:5])
    for s in masks(4):
        for row in conj(F[s],[-t[bits(q)] for q in combinations(vertices(s),3)]):
            yield 'terminal_fourcap_equivalence',row
    for s in masks(3):
        a,b,c=vertices(s)
        for row in conj(B[s],[-t[s]]+[-F[bits((u,v,b,c))] for u,v in combinations(range(b),2)]):
            yield 'terminal_bad_triple_equivalence',row
    for s in range(FULL+1):
        if 4<=s.bit_count()<=K:
            yield 'bad_triple_containment',(-A[s],*(bad(s^(1<<v)) for v in vertices(s)[:4]))
    for s in range(FULL+1):
        if s.bit_count()>=7:
            yield 'target_containment',(-T[s],*(target(s^(1<<v)) for v in vertices(s)[:7]))
    for s in range(FULL+1):
        if s.bit_count()<=K:
            yield 'forall_terminal_delta',tuple(z for z in (bad(s),target(FULL^s)) if z)


def rows():
    phase=None
    with (CASE/'input.cnf').open() as f:
        next(f)
        for line in f:
            fields=line.split()
            if not fields:continue
            if fields[:2]==['c','phase']:
                assert len(fields)==3;phase=fields[2];continue
            assert fields[0]!='c'
            row=tuple(map(int,fields));assert row[-1]==0 and 0 not in row[:-1]
            yield phase,row[:-1]


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    start=time.monotonic()
    paths=[CASE/'input.cnf',CASE/'input.cnf.map',CASE/'solve/cadical.log']
    before={str(p):digest(p) for p in paths}
    out={'label':'COMPUTED independent complete SAT/semantic audit','status':'IN_PROGRESS',
         'input_hashes':before,'script_sha256':digest(__file__),'own_geometry_source_sha256':digest(HERE/'geometry.py')}
    try:
        nv,nc,assignment,ids,occurrences=load()
        canonical,semantics=semantic(assignment,ids)
        counts=Counter();literals=0
        for lineno,(expected,actual) in enumerate(zip_longest(formula(ids),rows()),1):
            assert expected==actual,(lineno,expected,actual)
            phase,row=actual
            assert all(1<=abs(z)<=nv for z in row)
            assert any(bool(assignment[abs(z)])==(z>0) for z in row),(lineno,'SAT model clause failure')
            assert any(bool(canonical[abs(z)])==(z>0) for z in row),(lineno,'canonical clause failure')
            counts[phase]+=1;literals+=len(row)
        assert sum(counts.values())==nc
        assert before=={str(p):digest(p) for p in paths}
        out.update(status='PASS',variables=nv,clauses=nc,literals=literals,
                   assigned_variables=nv,model_literal_occurrences=occurrences,phase_counts=dict(counts),
                   model_and_canonical_assignments_satisfy_every_clause=True,
                   map_and_every_formula_row_match=True,semantic=semantics)
    except BaseException:
        out.update(status='FAIL',error=traceback.format_exc());raise
    finally:
        out.update(seconds=time.monotonic()-start,max_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        with (HERE/'data/model.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
        print(json.dumps({k:v for k,v in out.items() if k!='semantic'}))


if __name__=='__main__':main()
