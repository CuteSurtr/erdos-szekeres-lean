"""Adversarial exact controls for the no-cup-bound high-split reduction.

No selector search except exhaustive tests of the conditional lift on
named left blocks of at most seven points. All larger selections are
prescribed by the theorem or previously fixed controls.
"""
from collections import Counter
from itertools import combinations, product
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback
from verify_structure2 import determinant, signs_of, maxgon, convex, serial


def chain_ranks(s,vertices,positive):
    vertices=sorted(vertices);rank={v:1 for v in vertices};last={}
    for j,b in enumerate(vertices):
        for i,a in enumerate(vertices[:j]):
            last[a,b]=max([2]+[last[z,a]+1 for z in vertices[:i] if (s[z,a,b]>0)==positive])
            rank[b]=max(rank[b],last[a,b])
    return rank


def caps4(s,ids):
    return [t for t in combinations(ids,4) if all(s[u]<0 for u in combinations(t,3))]


def verify_selection(s,ids,A,n,ambient):
    A=set(A);ends={t[-2:] for t in ambient}
    assert not any(A.issuperset(t) for t in ambient)
    triples=[t for t in combinations(sorted(A),3) if s[t]<0]
    assert all(t[-2:] in ends for t in triples)
    assert maxgon(s,[v for v in ids if v not in A])<n-1
    return dict(A=sorted(A),selected_cap_triples=triples,
                terminal_certificates={str(t):next(c for c in ambient if c[-2:]==t[-2:]) for t in triples},
                complement_maxgon=maxgon(s,[v for v in ids if v not in A]))


def join(left,right):
    # Exact translation valid for arbitrary x spacings; not just a unit grid.
    dx=max(x for x,y in left)-min(x for x,y in right)+1
    p=list(left)+[(x+dx,y) for x,y in right];cut=len(left);height=0
    for a,b in combinations(range(cut),2):
        for c in range(cut,len(p)):
            height=max(height,(-determinant(p,a,b,c))//(p[b][0]-p[a][0])+1)
    for a in range(cut):
        for b,c in combinations(range(cut,len(p)),2):
            height=max(height,determinant(p,a,b,c)//(p[c][0]-p[b][0])+1)
    return list(left)+[(x+dx,y+height) for x,y in right]


def cup(k):return [(i,i*i) for i in range(k)]


def left_target(c):
    # c+2 hull vertices: a c-cup below and a four-cap above.
    return [(i,(c+3)**3 if i in (1,c) else i*i) for i in range(c+2)]


def right_target(k):
    # k+1 hull vertices: a k-cup below and a three-cap above.
    return [(i,(k+3)**3 if i==k//2 else i*i) for i in range(k+1)]


def check(p,cut,n,conditional_B=None,all_small_B=False):
    assert 0<cut<len(p);idx=list(range(len(p)));L=idx[:cut];R=idx[cut:]
    s=signs_of(p)
    assert all(value>0 if b<cut<=d else value<0 if a<cut<=b else True
               for (a,b,d),value in s.items())
    beta=chain_ranks(s,idx,True);bl=chain_ranks(s,L,True);ar=chain_ranks(s,R,False)
    alpha=chain_ranks(s,idx,False);assert max(alpha.values())<=4
    assert not any(all(s[t]<0 for t in combinations(q,3)) for q in combinations(idx,5))
    assert maxgon(s,idx)<n
    c=max(bl.values());assert 1<=c<=n-2 and max(ar.values())<=3
    ambient=caps4(s,idx);left_caps=caps4(s,L);out=dict(P=p,n=n,m=len(p),cut=cut,c=c,
        maxima=dict(cup=max(beta.values()),cap=max(alpha.values()),gon=maxgon(s,idx)),
        beta_left=[bl[v] for v in L],selected=[])
    if c<=n-4:
        out['case']='i';out['selected'].append(verify_selection(s,idx,R,n,ambient))
    elif c==n-3:
        out['case']='ii';assert max(ar.values())<=2 and len(R)<=n-1
        B=[v for v in L if bl[v]==n-3]
        for r in R:out['selected'].append(verify_selection(s,idx,B+[r],n,ambient))
    else:
        out['case']='iii';assert len(R)==1 and ambient==left_caps
        assert all(s[a,b,R[0]]>0 for a,b in combinations(L,2))
        choices=[]
        if conditional_B is not None:choices.append(conditional_B)
        if all_small_B:
            assert len(L)<=7
            ends={t[-2:] for t in left_caps}
            for bits in range(1<<len(L)):
                B=[v for i,v in enumerate(L) if bits>>i&1]
                if any(set(B).issuperset(t) for t in left_caps):continue
                if any(s[t]<0 and t[-2:] not in ends for t in combinations(B,3)):continue
                if maxgon(s,[v for v in L if v not in B])>=n-1:continue
                choices.append(B)
        for B in choices:
            verify_selection(s,L,B,n,left_caps)
            lifted=verify_selection(s,idx,sorted(B+R),n,ambient)
            assert lifted['selected_cap_triples']==[t for t in combinations(sorted(B),3) if s[t]<0]
            out['selected'].append(lifted)
        out['old_four_caps_unchanged']=True
        out['conditional_choices_checked']=len(choices)
        if not choices:out['scope']='Critical case is only a conditional reduction; no left selector asserted.'
    if len(p)<=10:
        for selection in out['selected']:
            A=set(selection['A'])
            assert all(A.intersection(t) for t in combinations(idx,n-1) if convex(p,t))
    return out


def named(root):
    out={}
    for n in (5,6,8):
        L=cup(n-4);R=right_target(n-2)
        out[f'n{n}_case_i_cap_R']=check(join(L,R),len(L),n)
        R=cup(n-1)
        out[f'n{n}_case_i_longcup_R']=check(join(L,R),len(L),n)
        L=left_target(n-3);R=cup(n-1)
        out[f'n{n}_case_ii_both_internal_targets']=check(join(L,R),len(L),n)
        L=right_target(n-2);R=[(0,0)]
        out[f'n{n}_case_iii_nonvacuous_left']=check(join(L,R),len(L),n,all_small_B=True)
        L=cup(n-2)
        out[f'n{n}_case_iii_empty_left_selection']=check(join(L,R),len(L),n,conditional_B=[])
    # Nontrivial rank-level cap triples in the middle and critical cases.
    old=json.loads((root/'data/separator_c3.json').read_text())
    L=old['P'];out['n7_case_iii_terminal_caps']=check(join(L,[(0,0)]),len(L),7,conditional_B=old['A'])
    split=json.loads((root/'data/separator_c4.json').read_text())
    L=split['P'][:split['cut']];R=cup(6)
    out['n7_case_ii_terminal_caps']=check(join(L,R),len(L),7)
    # A negative control against dropping the induction premise at the last cut.
    t18=root/'data/initial_profiles.json';L=json.loads(t18.read_text())['fixtures']['terminal18']['P']
    inherited=check(join(L,[(0,0)]),len(L),7)
    inherited['inherited_obstruction']='Terminal nonexistence inherited logically from the independently audited terminal18 record; no new SAT run here.'
    inherited['left_source_sha256']=hashlib.sha256(t18.read_bytes()).hexdigest()
    out['terminal18_plus_high_singleton']=inherited
    return dict(status='PASS',cases=out)


def grid():
    counts=Counter();branches=Counter();examples={};start=time.monotonic()
    for m in range(2,8):
        for ys in product(range(-3,4),repeat=m-2):
            if time.monotonic()-start>15:
                return dict(status='PARTIAL_TIME_BOUND',counts=dict(counts),branches=dict(branches),examples=examples)
            counts['attempted']+=1;p=list(enumerate((0,0)+ys));idx=list(range(m))
            s={t:determinant(p,*t) for t in combinations(idx,3)}
            if not all(s.values()):continue
            counts['general_position']+=1
            cuts=[cut for cut in range(1,m) if all(v>0 if b<cut<=d else v<0 if a<cut<=b else True
                                                  for (a,b,d),v in s.items())]
            if not cuts:continue
            counts['has_split']+=1
            if max(chain_ranks(s,idx,False).values())>=5 or maxgon(s,idx)>=5:continue
            counts['valid_sets']+=1
            for cut in cuts:
                r=check(p,cut,5,all_small_B=True)
                counts['checked_valid_splits']+=1;branches[r['case']]+=1
                if r['maxima']['cup']==4:counts['splits_with_fourcup']+=1
                if r['case']=='iii':
                    assert r['conditional_choices_checked']>0
                    counts['conditional_lifts_checked']+=r['conditional_choices_checked']
                examples.setdefault(r['case'],r)
    return dict(status='PASS_COMPLETE_GRID',counts=dict(counts),branches=dict(branches),examples=examples,
         scope='m=2,...,7; x_i=i; y0=y1=0; other y_i in [-3,3]; no cup exclusion; not all real order types')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['cases','grid'],required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();assert not args.out.exists()
    root=Path(__file__).resolve().parents[1];start=time.monotonic();result={}
    try:result=named(root) if args.mode=='cases' else grid()
    except Exception:result.update(status='FAIL',traceback=traceback.format_exc());raise
    finally:
        result['elapsed_seconds']=time.monotonic()-start
        result['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        result['helper_sha256']=hashlib.sha256(Path(__file__).with_name('verify_structure2.py').read_bytes()).hexdigest()
        args.out.write_text(json.dumps(serial(result),indent=2)+'\n')
        if 'cases' in result:
            print(json.dumps({name:dict(n=r['n'],m=r['m'],cut=r['cut'],c=r['c'],case=r['case'],
                maxima=r['maxima'],selections_checked=len(r['selected']),
                selected_cap_triples=max([0]+[len(a['selected_cap_triples']) for a in r['selected']]))
                for name,r in result['cases'].items()}))
        else:print(json.dumps({k:v for k,v in result.items() if k!='examples'}))


if __name__=='__main__':main()
