#!/usr/bin/env python3
"""Independent exact controls; no imports from any finder or prior checker.

The finder used monotone hulls, all-triple cap tests and cup edge DP. Here
convexity uses triangle containment, chains use consecutive turns, and cup
ranks are found by enumerating all cup subsets. Only the frozen small inputs
and three explicit synthetic configurations are used; this is not a search.
"""
import hashlib
import itertools as it
import json
from fractions import Fraction as F
from pathlib import Path
import resource
import time

resource.setrlimit(resource.RLIMIT_AS, (384 * 1024**2,) * 2)
resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
START = time.monotonic()
HERE = Path(__file__).resolve().parent


def bit(vs):
    return sum(1 << v for v in vs)


def vertices(a):
    return [v for v in range(a.bit_length()) if a >> v & 1]


def det(P, a, b, c):
    ax, ay = P[a]; bx, by = P[b]; cx, cy = P[c]
    return ax*(by-cy) + bx*(cy-ay) + cx*(ay-by)


def inside(P, p, abc):
    a,b,c = abc
    ds = [det(P,a,b,p),det(P,b,c,p),det(P,c,a,p)]
    return all(d>0 for d in ds) or all(d<0 for d in ds)


def data(P, n):
    m = len(P)
    assert all(P[i][0] < P[i+1][0] for i in range(m-1))
    determinants = [det(P,*q) for q in it.combinations(range(m),3)]
    assert all(determinants)
    nonconvex = [bit(q) for q in it.combinations(range(m),4)
                 if any(inside(P,p,tuple(v for v in q if v != p)) for p in q)]
    def convex(q):
        a = bit(q)
        return not any(a & w == w for w in nonconvex)
    def cap(q):
        return all(det(P,*q[j:j+3])<0 for j in range(len(q)-2))
    def cup(q):
        return all(det(P,*q[j:j+3])>0 for j in range(len(q)-2))
    caps = {j:[bit(q) for q in it.combinations(range(m),j) if cap(q)]
            for j in (3,4,5)}
    cups = [bit(q) for j in range(1,m+1) for q in it.combinations(range(m),j) if cup(q)]
    beta = [max(a.bit_count() for a in cups if a.bit_length()-1 == v) for v in range(m)]
    gons = {j:[bit(q) for q in it.combinations(range(m),j) if convex(q)] for j in (n-1,n)}
    assert not caps[5]
    return dict(P=P,n=n,m=m,caps=caps,cups=cups,beta=beta,gons=gons,
                nonconvex=nonconvex,min_det=min(abs(d) for d in determinants))


def good(d, a):
    return (not any(a & q == q for q in d['caps'][4])
            and all(a & h for h in d['gons'][d['n']-1]))


def terminal_safe(d, a):
    tails = {tuple(vertices(q)[-2:]) for q in d['caps'][4]}
    return (not any(a & q == q for q in d['caps'][4])
            and all(tuple(vertices(q)[-2:]) in tails for q in d['caps'][3] if a & q == q))


def rank_control(d):
    beta = d['beta']
    tails = {tuple(vertices(q)[-2:]) for q in d['caps'][4]}
    bad = [q for q in d['caps'][3] if tuple(vertices(q)[-2:]) not in tails]
    for q in bad:
        a,b,c = vertices(q)
        assert beta[a] < beta[b]
    for lev in set(beta):
        assert terminal_safe(d,bit(v for v in range(d['m']) if beta[v]==lev))
    return dict(rank3_triples=len(bad),levels_checked=len(set(beta)))


def extreme_control(P, n):
    assert len(P)<=2*n-3
    d = data(P,n); u=data(P[:-1],n)
    r = len(P)-1
    long = [c for c in u['cups'] if c.bit_count()==n-2]
    if long:
        a = min(long)
        branch='cup complement'
    else:
        a = bit(sorted({h.bit_length()-1 for h in u['gons'][n-1]}))
        branch='terminal endpoint level'
    assert good(u,a) and terminal_safe(u,a) and good(d,a | 1 << r)
    return dict(n=n,m=len(P),branch=branch,old_targets=len(u['gons'][n-1]),
                old_max_cup=max(u['beta']),A=vertices(a),root=r,
                full_ngons=len(d['gons'][n]))


def arbitrary_control(P,n):
    assert len(P)<=2*n-4
    d=data(P,n)
    choices=[]
    for r in range(len(P)):
        old_gons=[h for h in d['gons'][n-1] if not h >> r & 1]
        if old_gons:
            a=next(c for c in d['cups'] if c.bit_count()==n-3 and not c >> r & 1
                   and c & old_gons[0]==c)
        else:
            a=0
        assert good(d,a | 1 << r)
        choices.append(dict(root=r,A=vertices(a)))
    return dict(n=n,m=len(P),full_ngons=len(d['gons'][n]),choices=choices)


def parent_control(P,n):
    assert len(P)<=n+3
    d=data(P,n)
    assert not d['gons'][n]
    out=[]
    for r in range(len(P)):
        if len(P)<=n+1:
            a=bit([r]+[v for v in range(len(P)) if v!=r][:2])
            w=0
        else:
            w=next(w for w in d['nonconvex'] if not w >> r & 1)
            available=[v for v in range(len(P)) if not w >> v & 1 and v!=r]
            if len(P)==n+2:
                a=bit([r]+available[:2])
            else:
                five=sorted([r]+available[:4])
                a=next(bit(q) for q in it.combinations(five,4)
                       if r in q and bit(q) not in d['caps'][4])
        assert good(d,a) and a >> r & 1 and not a & w
        out.append(dict(root=r,A=vertices(a),nonconvex_W=vertices(w)))
    return dict(n=n,m=len(P),choices=out)


def projective_control(P):
    r=len(P)-1
    Q=[(F(x-P[r][0]+1),F(y-P[r][1])) for x,y in P]
    den=[1-x for x,y in Q[:-1]]
    T=[(x/(1-x),y/(1-x)) for x,y in Q[:-1]]
    assert all(T[i][0]<T[i+1][0] for i in range(r-1))
    for abc in it.combinations(range(r),3):
        a,b,c=abc
        assert det(T,*abc)*den[a]*den[b]*den[c]==det(Q,*abc)
    positive=0
    for a,b in it.combinations(range(r),2):
        dy=T[b][1]-T[a][1]
        assert dy*den[a]*den[b]==-det(Q,a,b,r)
        assert dy != 0
        positive += dy>0
    cap4=0
    for q in it.combinations(range(r),4):
        if all(det(Q,*q[j:j+3])<0 for j in range(2)):
            cap4+=1
            assert T[q[-1]][1]<T[q[-2]][1]
    return dict(points=len(P),old_triples= len(list(it.combinations(range(r),3))),
                pairs=len(list(it.combinations(range(r),2))),
                positive_pairs=positive,old_four_caps_with_negative_tail=cap4)


def pure_cap_counterexample():
    P=[(0,0),(1,1),(2,0),(3,100),(4,99),(5,100),(6,-10)]
    d=data(P,6);u=data(P[:-1],6)
    assert not u['caps'][4] and not any(c.bit_count()==4 for c in u['cups'])
    assert not d['gons'][6]
    heights=[]
    for a,b in it.combinations(range(6),2):
        x,y=P[b]
        heights.append(y+F(P[b][1]-P[a][1],P[b][0]-P[a][0])*(6-x))
    assert min(heights)==-4
    failed=[]
    for old in it.combinations(range(6),4):
        a=bit(old)|64
        q=next(q for q in d['caps'][4] if a & q == q)
        failed.append(dict(five_set=vertices(a),four_cap=vertices(q)))
    maxima=max(a.bit_count() for a in range(128) if a & 64
               and not any(a & q == q for q in d['caps'][4]))
    assert maxima==4 and not any(bit([0,1,3,6]) & q == q for q in d['caps'][4])
    assert len(failed)==15
    return dict(P=P,root=6,caps4=len(d['caps'][4]),caps5=0,
                old_caps4=0,old_cups4=0,convex6=0,min_abs_det=d['min_det'],
                min_secant_height_at_root=str(min(heights)),root_y=-10,
                maximum_rooted_capfree_size=maxima,rooted_four=[0,1,3,6],
                all_fifteen_failures=failed,
                projective=projective_control(P))


def main():
    frozen=HERE/'probe_selection.json'
    records=json.loads(frozen.read_text())['results']
    out=dict(label='COMPUTED',status='PASS',
             scope='independent exact controls of frozen fixtures and explicit examples',
             inputs_sha256={str(frozen):hashlib.sha256(frozen.read_bytes()).hexdigest()},
             fixed_inputs=[],extreme_bound=[],arbitrary_bound=[],parent_lemma=[],projective=[])
    for rec in records:
        P=rec['P']; n=rec['n']; d=data(P,n)
        assert not d['gons'][n]
        assert d['beta']==rec['beta'] and len(d['caps'][4])==rec['caps4']
        assert len(d['gons'][n-1])==rec['targets']
        a=bit(rec['antichain_example'])
        assert good(d,a) and terminal_safe(d,a)
        assert all(d['beta'][x]>=d['beta'][y] for x,y in zip(vertices(a),vertices(a)[1:]))
        ranks=rank_control(d)
        assert ranks['rank3_triples']==rec['rank3_triples']
        for t,fail in rec['lex_failures_by_size'].items():
            a=bit(fail['A']); r=len(P)-1
            assert len(fail['A'])==int(t)
            assert all(a & h for h in d['gons'][n-1] if not h >> r & 1)
            assert not any(a & q==q for q in d['caps'][4])
            for q in fail['blocks']:
                assert bit(q) in d['caps'][4] and (a | 1<<r) & bit(q)==bit(q)
            assert not fail['missed_full'] and good(d,a)
        out['fixed_inputs'].append(dict(tag=rec['tag'],m=len(P),n=n,**ranks))
        out['projective'].append(projective_control(P))
        out['extreme_bound'].append(extreme_control(P[:2*n-3],n))
    # Nonvacuous short-cup branches, already used as exact controls in weak_theory.
    for n in (7,8):
        P=[(0,0),(1,-4),(2,8),(4,10),(5,-4),(6,0),(8,1)]
        if n==8:
            P.insert(3,(3,-5))
        result=extreme_control(P,n)
        assert result['branch']=='terminal endpoint level' and result['old_targets']>0
        out['extreme_bound'].append(result)
        # Convex controls deliberately have n-gons: Theorem 4 does not forbid them.
        convex=[(i,i*i) for i in range(2*n-3)]
        out['extreme_bound'].append(extreme_control(convex,n))
        out['arbitrary_bound'].append(arbitrary_control(convex[:-1],n))
        original=next(rec['P'] for rec in records if rec['n']==n and rec['m']>=n+3)
        out['parent_lemma'].append(parent_control(original[:n+3],n))
        out['parent_lemma'].append(parent_control(original[:n+2],n))
    out['pure_cap_counterexample']=pure_cap_counterexample()
    out['seconds']=time.monotonic()-START
    out['max_rss_KiB']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (HERE/'exact_controls.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status=out['status'],seconds=out['seconds'],max_rss_KiB=out['max_rss_KiB'],
                         fixed_inputs=len(out['fixed_inputs']),extreme_bound=out['extreme_bound'],
                         arbitrary_root_checks=sum(len(v['choices']) for v in out['arbitrary_bound']),
                         parent_root_checks=sum(len(v['choices']) for v in out['parent_lemma']),
                         pure_cap_four_caps=out['pure_cap_counterexample']['caps4'],
                         pure_cap_five_failures=15)))


if __name__=='__main__':
    main()
