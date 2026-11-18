"""Exact structural support audit and small-cell cup-selector enumeration."""
import argparse
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations as C
import json
from pathlib import Path
from probe import protection
from exact import determinant,line
from search import dump,sha
from verify import replay


def signed(z):return 1 if z>0 else -1 if z<0 else 0


def relative(p,query,ambient):
    q,e=line(p,query),line(p,ambient);ids=sorted(set(query+ambient));M=p[-1][0]
    def diff(i):
        t=p[i][0]-M
        return (e[0]*t+e[1])*q[2]-(q[0]*t+q[1])*e[2]
    slope=e[0]*q[2]-q[0]*e[2];height=e[1]*q[2]-q[1]*e[2]
    left,right=diff(ids[0]),diff(ids[-1])
    if len(ids)==4:
        assert left and right
        category='forced_dominance_after_R' if left<0<right else 'fails_whole_ray_from_R' if right<0 else 'four_point_signs_undetermined'
    else:category='shared_endpoint'
    return {'ambient_pair':list(ambient),'vertices':ids,'triple_determinants':[{'triple':list(t),'value':determinant(p,*t)} for t in C(ids,3)],'sign_pattern':''.join('+' if determinant(p,*t)>0 else '-' for t in C(ids,3)),'slope_difference':str(Q(slope,e[2]*q[2])),'height_difference_at_M':str(Q(height,e[2]*q[2])),'dominates_after_M':slope>=0 and height>=0,'d_at_L_sign':signed(left),'d_at_R_sign':signed(right),'orientation_only_category':category}


def four_point_table():
    triples=list(C(range(4),3));patterns=['++++','+++-','++--','+---','----','---+','--++','-+++'];rows=[]
    for pattern in patterns:
        signs={t:1 if s=='+' else -1 for t,s in zip(triples,pattern)}
        def orientation(t):
            inversions=sum(t[i]>t[j] for i in range(3) for j in range(i+1,3))
            return signs[tuple(sorted(t))]*(-1 if inversions%2 else 1)
        for query in C(range(4),2):
            ambient=tuple(i for i in range(4) if i not in query)
            ds=[]
            for v in range(4):
                ds.append(-orientation(ambient+(v,)) if v in query else orientation(query+(v,)))
            category='forced_dominance_after_R' if ds[0]<0<ds[-1] else 'fails_whole_ray_from_R' if ds[-1]<0 else 'four_point_signs_undetermined'
            rows.append({'orientations_012_013_023_123':pattern,'query_positions':query,'ambient_positions':ambient,'d_endpoint_signs':ds,'classification':category})
    # Check every row against many exact real four-point controls, and show
    # both possibilities for each ambiguous row using parallel/tilted lines.
    seen=set()
    for y1 in range(-6,7):
        for y2 in range(-6,7):
            for y3 in range(-6,7):
                p=[[0,0],[1,y1],[2,y2],[3,y3]]
                if any(determinant(p,*t)==0 for t in triples):continue
                pat=''.join('+' if determinant(p,*t)>0 else '-' for t in triples);assert pat in patterns
                for query in C(range(4),2):
                    ambient=tuple(i for i in range(4) if i not in query);r=relative(p,query,ambient)
                    expected=next(z for z in rows if z['orientations_012_013_023_123']==pat and z['query_positions']==query)
                    assert r['orientation_only_category']==expected['classification'];seen.add((pat,query))
                    if expected['classification']=='forced_dominance_after_R':assert r['dominates_after_M']
                    if expected['classification']=='fails_whole_ray_from_R':assert not r['dominates_after_M']
    assert len(seen)==48
    for r in rows:
        if r['classification']!='four_point_signs_undetermined':continue
        examples=[]
        for slope in (-1,0,1):
            p=[[i,0 if i in r['query_positions'] else 10+slope*i] for i in range(4)]
            pattern=''.join('+' if determinant(p,*t)>0 else '-' for t in triples)
            assert pattern==r['orientations_012_013_023_123'];z=relative(p,r['query_positions'],r['ambient_positions'])
            assert z['dominates_after_M']==(slope>=0);examples.append({'P':p,'dominates_after_R':z['dominates_after_M']})
        r['opposite_realizations']=examples
    return {'rows':rows,'class_counts':dict(Counter(r['classification'] for r in rows)),'controls_cover_all_48_rows':True,'scope':'Whole ray from the rightmost of these four endpoints; later M can differ.'}


def enumerate_case(case,out):
    inp=json.loads((case/'input.json').read_text());p=inp['P'];g=json.loads((case/'geometry.json').read_text());n=inp['n'];m=len(p)
    assert m<=18
    support=protection(p,g);caps=[sum(1<<v for v in t) for t in g['caps4']];targets=[sum(1<<v for v in t) for t in g['targets']]
    bad=[sum(1<<v for v in t) for t in g['caps3'] if not support[tuple(t[-2:])]['protected']]
    ordinary=[];good=[]
    for A in range(1<<m):
        if any(A&c==c for c in caps) or any(not A&h for h in targets):continue
        ordinary.append(A)
        if all(A&b!=b for b in bad):good.append(A)
    best=min(good,key=lambda a:(a.bit_count(),a));A=[i for i in range(m) if best>>i&1];cert=[];cup_rows=[]
    for t in g['caps3']:
        if all(best>>i&1 for i in t):
            s=support[tuple(t[-2:])];cert.append({'triple':t,'supports':[{'fourcap':s['ambient_fourcap'],'weight':'1'}]});cup_rows.append({'triple':t,**s})
    checked=replay(p,n,A,cert)
    report={'label':'COMPUTED exact finite enumeration','source_case':str(case),'source_input_sha256':sha(case/'input.json'),'P':p,'m':m,'n':n,'assignments_checked':1<<m,'ordinary_count':len(ordinary),'cup_protected_count':len(good),'minimum_cup_protected_size':len(A),'minimum_A':A,'minimum_cardinality_count':sum(z.bit_count()==len(A) for z in good),'support_witnesses':cup_rows,'certificates':cert,'positive_replay':checked,'consequence':'Every listed cup-protected Delta persists under every realization with the same ordered triple orientations, by the written cup-domination proof.'}
    dump(out,report);return report


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--known-case',type=Path,required=True);ap.add_argument('--case15',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    p=json.loads((args.known_case/'input.json').read_text())['P'];g=json.loads((args.known_case/'geometry.json').read_text());A=[0,5,6,7,8];supports=protection(p,g)
    ambient=sorted({tuple(c[-2:]) for c in g['caps4']});caps=[t for t in C(A,3) if determinant(p,*t)<0];rows=[]
    for t in caps:
        q=t[-2:];comparisons=[relative(p,q,uv) for uv in ambient];dom=[r for r in comparisons if r['dominates_after_M']]
        rows.append({'triple':t,'query_pair':q,'cup_protected':supports[q]['protected'],'shared_endpoint_dominating_pairs':[r['ambient_pair'] for r in dom if len(r['vertices'])<4],'dominating_pairs':dom,'all_pair_comparisons':comparisons})
    dump(args.out/'old_known_A.json',{'P':p,'A':A,'rows':rows,'scope':'The old known A, not the different cup-protected selector.'})
    dump(args.out/'four_point_classes.json',four_point_table())
    old=enumerate_case(args.known_case,args.out/'known18_exact_counts.json');new=enumerate_case(args.case15,args.out/'real15_exact_counts.json')
    print(json.dumps({'old_A_cap_triples':caps,'old_A_actual_dominating_pair_counts':[len(r['dominating_pairs']) for r in rows],'old_A_cup_protection':[r['cup_protected'] for r in rows],'known18':{k:old[k] for k in ('ordinary_count','cup_protected_count','minimum_cup_protected_size','minimum_A')},'real15':{k:new[k] for k in ('ordinary_count','cup_protected_count','minimum_cup_protected_size','minimum_A')}}))
if __name__=='__main__':main()
