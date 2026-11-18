"""Independent replay: supporting edges, adjacent turns, endpoint values.

Imports neither the analysis driver nor any earlier research checker.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations
import json
import os
from pathlib import Path
import resource
import shutil
import time


def write(path,obj):
    with path.open('x') as f:
        json.dump(obj,f,indent=2,sort_keys=True);f.write('\n');f.flush();os.fsync(f.fileno())
        os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)


def orient(P,i,j,k):
    x,y=P[i];u,v=P[j];s,t=P[k]
    return x*(v-t)+u*(t-y)+s*(y-v)


def is_convex(P,S):
    edges=0
    for a,b in combinations(S,2):
        turns=[orient(P,a,b,c) for c in S if c!=a and c!=b]
        edges+=all(z>0 for z in turns) or all(z<0 for z in turns)
    return edges==len(S)


def chain(P,S,sign):
    return all(sign*orient(P,S[i],S[i+1],S[i+2])>0 for i in range(len(S)-2))


def bits(S):
    out=0
    for v in S:out|=1<<v
    return out


def vertices(mask):return [i for i in range(15) if mask&(1<<i)]


def upward_closure(seeds):
    result=bytearray(32768)
    for seed in seeds:result[seed]=1
    for i in range(15):
        b=1<<i
        for a in range(32768):
            if a&b:result[a]|=result[a^b]
    return result


def coefficients(P,pair):
    a,b=pair;x,y=P[a];u,v=P[b]
    # Global intercept before shifting X=M+t.
    slope=Fraction(v-y,u-x);intercept=Fraction(y*u-v*x,u-x)
    return slope,intercept+slope*P[-1][0]


def endpoint_forced(P,q,r):
    if q==r:return True
    b,c=q;u,v=r
    dx=P[c][0]-P[b][0];dy=P[c][1]-P[b][1]
    ex=P[v][0]-P[u][0];ey=P[v][1]-P[u][1]
    ordered=sorted(set(q+r))
    values=[]
    for i in ordered:
        x=P[i][0]
        values.append((P[u][1]*ex+ey*(x-P[u][0]))*dx
                      -(P[b][1]*dx+dy*(x-P[b][0]))*ex)
    last=values[-1]
    return last>=0 and any(z<=0 and (last>0 or z<0) for z in values[:-1])


def parse_cnf(path):
    clauses=[];pending=[];header=None
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith('c'):continue
        if line.startswith('p '):
            assert header is None
            p,cnf,n,m=line.split();assert p=='p' and cnf=='cnf';header=(int(n),int(m));continue
        for item in line.split():
            lit=int(item)
            if lit:pending.append(lit)
            else:clauses.append(tuple(sorted(pending)));pending=[]
    assert not pending and header is not None and header[1]==len(clauses)
    assert all(0<abs(v)<=header[0] for clause in clauses for v in clause)
    return header,Counter(clauses)


def expected_clauses(caps,targets,bad):
    return Counter(tuple(sorted(sgn*(v+1) for v in row))
                   for family,sgn in ((caps,-1),(targets,1),(bad,-1)) for row in family)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('run',type=Path)
    ap.add_argument('--parent-cnf',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    shutil.copy2(__file__,args.out/'replay.py')
    manifest=json.loads((args.run/'input_manifest.json').read_text())
    for name,row in manifest.items():
        assert hashlib.sha256((args.run/'inputs'/(name+'.json')).read_bytes()).hexdigest()==row['sha256']
    cases=[];recorded_sets={};pair_dicts={};cup_multiset=None;sign_reference=None
    for name in ('original','balanced'):
        source=json.loads((args.run/'inputs'/(name+'.json')).read_text());P=source['P'];directory=args.run/name
        assert len(P)==15 and all(type(z)is int for point in P for z in point)
        assert all(P[i][0]<P[i+1][0] for i in range(14))
        turns=[orient(P,*t) for t in combinations(range(15),3)];assert all(turns)
        signs=''.join('+' if z>0 else '-' for z in turns);assert signs==source['orientation_signs']
        if sign_reference is None:sign_reference=signs
        assert signs==sign_reference
        caps={k:[list(s) for s in combinations(range(15),k) if chain(P,s,-1)] for k in (3,4,5)}
        targets=[list(s) for s in combinations(range(15),6) if is_convex(P,s)]
        ngons=[list(s) for s in combinations(range(15),7) if is_convex(P,s)]
        assert not caps[5] and not ngons
        finder_geometry=json.loads((directory/'geometry.json').read_text())
        for k in (3,4,5):assert caps[k]==finder_geometry['caps'+str(k)]
        assert targets==finder_geometry['targets'] and ngons==finder_geometry['ngons']
        assert min(map(abs,turns))==finder_geometry['minimum_absolute_determinant']
        E={tuple(cap[-2:]) for cap in caps[4]};ambient={pair:coefficients(P,pair) for pair in E}
        checkpoints={Fraction(0)}
        for (s,z),(u,w) in combinations(ambient.values(),2):
            if s!=u and (w-z)/(s-u)>0:checkpoints.add((w-z)/(s-u))
        values={t:max(s*t+z for s,z in ambient.values()) for t in checkpoints}
        rows=json.loads((directory/'pairs.json').read_text())['pairs']
        assert [r['pair'] for r in rows]==[list(q) for q in combinations(range(15),2)]
        safe={};flags={};safe_count=unsafe_count=two_line=0;comparisons=0
        for row in rows:
            q=tuple(row['pair']);s,z=coefficients(P,q)
            assert Fraction(row['query_line']['slope'])==s and Fraction(row['query_line']['height_at_max_x'])==z
            cs={r for r in E if r==q or (r[0]>=q[0] and r[1]>=q[1] and chain(P,sorted(set(q+r)),1))}
            fs={r for r in E if endpoint_forced(P,q,r)};comparisons+=len(E)
            assert cs==set(map(tuple,row['cup_support_pairs'])) and fs==set(map(tuple,row['forced_support_pairs']))
            is_safe=s<=max(u for u,w in ambient.values()) and all(s*t+z<=h for t,h in values.items())
            assert is_safe==row['safe']
            actual={'terminal':q in E,'cup':bool(cs),'forced':bool(fs),'uniform':is_safe}
            assert row['protected']==actual;safe[q]=is_safe;flags[q]=actual
            assert row['cap_triples']==[t for t in caps[3] if t[-2:]==list(q)]
            if is_safe:
                total=ss=hh=Fraction(0)
                assert 1<=len(row['supports'])<=2
                for support in row['supports']:
                    c=support['fourcap'];r=tuple(support['tail_pair'])
                    assert c in caps[4] and c[-2:]==list(r)
                    weight=Fraction(support['weight']);assert weight>=0
                    u,w=coefficients(P,r)
                    assert str(u)==support['slope'] and str(w)==support['height_at_max_x']
                    total+=weight;ss+=weight*u;hh+=weight*w
                assert total==1 and ss>=s and hh>=z
                assert Fraction(row['slope_difference'])==ss-s and Fraction(row['height_difference'])==hh-z
                safe_count+=1;two_line+=len(row['supports'])==2
            else:
                t=Fraction(row['witness_t']);assert t>0 and all(s*t+z>u*t+w for u,w in ambient.values())
                lower=[Fraction(0)]+[(w-z)/(s-u) for u,w in ambient.values() if s>u]
                upper=[(w-z)/(s-u) for u,w in ambient.values() if s<u]
                assert all(z>w for u,w in ambient.values() if s==u)
                lo=max(lower);hi=min(upper) if upper else None
                assert row['exposure_interval']==[str(lo),None if hi is None else str(hi)]
                assert hi is None or lo<hi
                unsafe_count+=1
        bad={k:[t for t in caps[3] if not flags[tuple(t[-2:])][k]] for k in ('terminal','cup','forced','uniform')}
        assert bad==json.loads((directory/'bad_triples.json').read_text())
        # Independent full membership replay through upward-closure transforms.
        c_bad=upward_closure(map(bits,caps[4]));target_complement_bad=upward_closure(map(bits,targets))
        weak=[a for a in range(32768) if not c_bad[a] and not target_complement_bad[32767^a]]
        computed={'weak':weak}
        for k,triples in bad.items():
            closure=upward_closure(map(bits,triples))
            computed[k]=[a for a in weak if not closure[a]]
        recorded=json.loads((directory/'memberships.json').read_text());assert computed==recorded
        report=json.loads((directory/'report.json').read_text())
        for k,members in computed.items():
            histogram=dict(sorted(Counter(a.bit_count() for a in members).items()))
            minimum=min(histogram,default=None)
            row=report['families'][k]
            assert row['count']==len(members) and row['minimum']==minimum
            assert row['size_counts']=={str(k):v for k,v in histogram.items()}
            assert row['minimum_count']==histogram.get(minimum,0)
            assert row['minimum_masks']==[a for a in members if a.bit_count()==minimum]
        p=json.loads((directory/'positive.json').read_text())
        assert p['P']==P and p['A']==vertices(p['mask']) and p['mask'] in computed['uniform']
        assert len(p['A'])==min(a.bit_count() for a in computed['uniform'])
        selected=[t for t in caps[3] if set(t)<=set(p['A'])]
        assert [r['triple'] for r in p['certificates']]==selected
        by_pair={tuple(r['pair']):r for r in rows}
        for r in p['certificates']:assert r['line_certificate']==by_pair[tuple(r['triple'][-2:])]
        header,cnf=parse_cnf(directory/'uniform.cnf');expected=expected_clauses(caps[4],targets,bad['uniform'])
        assert header[0]==15 and cnf==expected
        assert all(any((lit>0)==bool(p['mask']&(1<<(abs(lit)-1))) for lit in clause) for clause in cnf)
        current_cup=expected_clauses(caps[4],targets,bad['cup'])
        if cup_multiset is None:cup_multiset=current_cup
        assert cup_multiset==current_cup
        recorded_sets[name]=set(computed['uniform']);pair_dicts[name]=by_pair
        cases.append({'name':name,'status':'PASS','orientations_checked':len(turns),'polygon_subsets_checked':11440,
                      'geometry_counts':{'caps3':len(caps[3]),'caps4':len(caps[4]),'caps5':len(caps[5]),'targets':len(targets),'ngons':len(ngons)},
                      'cup_support_comparisons':comparisons,'endpoint_forced_comparisons':comparisons,
                      'pair_certificates':len(rows),'safe_pairs':safe_count,'exposed_pairs':unsafe_count,'two_line_certificates':two_line,
                      'envelope_checkpoints':len(checkpoints),'family_counts':{k:len(v) for k,v in computed.items()},
                      'uniform_minimum':len(p['A']),'positive_A':p['A'],'positive_cap_triples':selected})
        for path in directory.iterdir():
            if path.is_file():
                with path.open('rb') as f:os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
    parent_bytes=args.parent_cnf.read_bytes();parent_hash=hashlib.sha256(parent_bytes).hexdigest()
    assert parent_hash=='47c738ec38449827573872fa0223e4c607649f8a38acb2e76a8daf59b365cd1f'
    header,parent_clauses=parse_cnf(args.parent_cnf)
    assert header==(15,211) and parent_clauses==cup_multiset
    (args.out/'parent_membership.cnf').write_bytes(parent_bytes)
    with (args.out/'reconstructed_cup.cnf').open('x') as f:
        f.write('p cnf 15 '+str(sum(cup_multiset.values()))+'\n')
        for clause,count in sorted(cup_multiset.items()):
            for _ in range(count):f.write(' '.join(map(str,clause))+' 0\n')
    write(args.out/'cup_clause_match.json',{'status':'PASS','source':str(args.parent_cnf),'input_sha256':parent_hash,
          'variables':15,'clauses':211,'complete_clause_multiset_equal':True,'family_rows':{'negative_fourcaps':47,'negative_unprotected_triples':94,'positive_convex_sixsets':70},
          'scope':'Reconstructed independently from each integer realization; duplicate clause multiplicities retained.'})
    original=recorded_sets['original'];balanced=recorded_sets['balanced']
    differences=json.loads((args.run/'differences.json').read_text())
    assert differences['common_uniform_count']==len(original&balanced)
    assert differences['original_only_uniform_masks']==sorted(original-balanced)
    assert differences['balanced_only_uniform_masks']==sorted(balanced-original)
    extra=sorted(balanced-original,key=lambda a:(a.bit_count(),a))
    if extra:
        a=extra[0];A=vertices(a)
        changed=[{'triple':list(t),'original':pair_dicts['original'][t[-2:]],'balanced':pair_dicts['balanced'][t[-2:]]}
                 for t in combinations(A,3) if t[-2:] in pair_dicts['original']
                 and list(t) in pair_dicts['original'][t[-2:]]['cap_triples']
                 and not pair_dicts['original'][t[-2:]]['safe'] and pair_dicts['balanced'][t[-2:]]['safe']]
        assert changed
        write(args.out/'metric_difference_witness.json',{'A':A,'mask':a,'ordinary_in_both':True,
             'original_uniform':False,'balanced_uniform':True,'changed_cap_triples':changed})
    summary={'status':'PASS','label':'COMPUTED independent exact replay','cases':cases,'cup_clause_multiset':'PASS',
             'uniform_family_comparison':'PASS','seconds':time.monotonic()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
             'scope':'Both fixed inputs only; no finder imports, solver call or coordinate search.'}
    write(args.out/'summary.json',summary);print(json.dumps(summary))


if __name__=='__main__':main()
