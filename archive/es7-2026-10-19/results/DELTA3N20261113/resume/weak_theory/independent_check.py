#!/usr/bin/env python3
"""Independent exact audit: no imports from probe/refine or previous code.

Convexity uses four-subset triangle containment, caps use consecutive turns.
The finder used monotone hulls and all-triple cap tests. No solver is used.
"""
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import resource
import time

resource.setrlimit(resource.RLIMIT_AS, (384 * 1024**2,) * 2)
resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
START = time.monotonic()
HERE = Path(__file__).resolve().parent


def orient(P, a, b, c):
    ax, ay = P[a]
    bx, by = P[b]
    cx, cy = P[c]
    return ax*(by-cy)+bx*(cy-ay)+cx*(ay-by)


def bits(V):
    return sum(2**v for v in V)


def vertices(B):
    return [i for i in range(B.bit_length()) if B & 2**i]


def inside(P, p, a, b, c):
    v = [orient(P,a,b,p),orient(P,b,c,p),orient(P,c,a,p)]
    return all(x>0 for x in v) or all(x<0 for x in v)


def geometric_data(P, n):
    m = len(P)
    assert all(P[i][0]<P[i+1][0] for i in range(m-1))
    determinants = [orient(P,*C) for C in itertools.combinations(range(m),3)]
    assert all(determinants)
    concave4 = []
    for Q in itertools.combinations(range(m),4):
        if any(inside(P,q,*(p for p in Q if p!=q)) for q in Q):
            concave4.append(bits(Q))
    def convex(C):
        B = bits(C)
        return not any(B & Q == Q for Q in concave4)
    def cap(C):
        return all(orient(P,*C[j:j+3])<0 for j in range(len(C)-2))
    caps = {size:[bits(C) for C in itertools.combinations(range(m),size) if cap(C)]
            for size in (3,4,5)}
    gons = {size:[bits(C) for C in itertools.combinations(range(m),size) if convex(C)]
            for size in (n-1,n)}
    assert not caps[5] and not gons[n]
    return caps,gons,min(abs(d) for d in determinants)


def threshold_audit(P, n):
    caps,gons,_ = geometric_data(P,n)
    r = len(P)-1
    old3 = [K for K in caps[3] if not K & 2**r]
    old4 = [K for K in caps[4] if not K & 2**r]
    oldH = [H for H in gons[n-1] if not H & 2**r]
    X,Y = P[r]
    def height(pair):
        b,c = pair
        slope = Fraction(P[c][1]-P[b][1],P[c][0]-P[b][0])
        return P[c][1]+slope*(X-P[c][0])
    tails4 = {tuple(vertices(K)[-2:]) for K in old4}
    f4 = max((height(pair) for pair in tails4),default=None)
    assert f4 is None or Y>f4
    totals = dict(old_deltas=0, terminal_pair_safe=0, threshold_safe=0,
                  actual_red_extensions=0, rank3_blockers=0,
                  noncup_terminal_safe=0, weak_only_terminal_safe=0,
                  exact_deletion_tests=0)
    weak_only = None
    for A in range(2**r):
        if any(A & K == K for K in old4) or not all(A & H for H in oldH):
            continue
        totals['old_deltas'] += 1
        active = [K for K in old3 if A & K == K]
        f3 = max((height(vertices(K)[-2:]) for K in active),default=None)
        terminal = all(tuple(vertices(K)[-2:]) in tails4 for K in active)
        envelope = f3 is None or f4 is not None and f3<=f4
        direct = f3 is None or Y>f3
        fullA = A | 2**r
        assert direct == (not any(fullA & K == K for K in caps[4]))
        assert not terminal or envelope
        assert not envelope or direct
        totals['terminal_pair_safe'] += terminal
        totals['threshold_safe'] += envelope
        totals['actual_red_extensions'] += direct
        totals['noncup_terminal_safe'] += bool(terminal and active)
        if direct:
            assert all(fullA & H for H in gons[n-1])
        for K in active:
            if Y < height(vertices(K)[-2:]):
                totals['rank3_blockers'] += 1
                assert tuple(vertices(K)[-2:]) not in tails4
        if terminal:
            for H in oldH:
                vs=vertices(H)
                lower = bits([vs[0],vs[-1]]+[p for p in vs[1:-1]
                              if orient(P,vs[0],p,vs[-1])>0])
                if not A & lower:
                    totals['weak_only_terminal_safe'] += 1
                    if weak_only is None:
                        weak_only=dict(A=vertices(A),polygon=vs,lower=vertices(lower))
                    break
        # Independent direct comparison of the exact deletion criterion.
        blocker = [K ^ 2**r for K in caps[4] if K & 2**r and fullA & K == K]
        C=A
        while True:
            R=A^C
            criterion = all(R & K for K in blocker) and all(C & H for H in oldH)
            D=C|2**r
            actual = not any(D & K==K for K in caps[4]) and all(D & H for H in gons[n-1])
            assert criterion == actual
            totals['exact_deletion_tests'] += 1
            if not C:
                break
            C=(C-1)&A
    return dict(counts=totals, weak_only_terminal_safe_example=weak_only)


def check_obstruction(w):
    P,n,r,A = w['P'],w['n'],w['r'],bits(w['A'])
    caps,gons,minimum = geometric_data(P,n)
    m=len(P)
    assert r==m-1 and m==n+2 and A.bit_count()==3
    T=A|2**r
    B=(2**m-1)^T
    assert T in caps[4]
    assert all((B|2**t) in gons[n-1] for t in vertices(T))
    old=[H for H in gons[n-1] if not H & 2**r]
    assert all(H & A for H in old)
    assert not any(A & K==K for K in caps[4])
    assert all(H & bits(w['full_delta']) for H in gons[n-1])
    assert not any(bits(w['full_delta']) & K==K for K in caps[4])
    failures=[]
    for sub in range(8):
        C=bits(w['A'][i] for i in range(3) if sub & 2**i)
        for red_r in (False,True):
            D=C|(2**r if red_r else 0)
            K=next((K for K in caps[4] if D & K==K),None)
            H=next((H for H in gons[n-1] if not D & H),None)
            assert K is not None or H is not None
            failures.append(dict(red=vertices(D),violation_type='four_cap' if K else 'missed_polygon',
                                 witness=vertices(K if K else H)))
    result=dict(n=n,m=m,cap4=len(caps[4]),cap5=len(caps[5]),
                targets=len(gons[n-1]),ngons=len(gons[n]),min_abs_det=minimum,
                private_polygons=[vertices(B|2**t) for t in vertices(A)],
                missed_polygon=vertices(B|2**r),blocker=vertices(T),
                blocker_triple_determinants=[orient(P,*C) for C in itertools.combinations(vertices(T),3)],
                full_delta=w['full_delta'],all_16_monotone_failures=failures,
                threshold_audit=threshold_audit(P,n))
    # A rational instance of the lift; the denominator is chosen by exact checks,
    # then all coordinates are uniformly scaled to integers.
    b=P[0]
    M=min([Fraction(0)]+[Fraction(q[1]-b[1],q[0]-b[0]) for q in P[1:]])-1
    lift=None
    for exponent in range(1,12):
        eps=Fraction(1,10**exponent)
        l=(Fraction(b[0])-eps,Fraction(b[1])-M*eps)
        Q=[l]+[tuple(map(Fraction,p)) for p in P]
        if all(orient(Q,0,i+1,j+1)*orient(P,0,i,j)>0
               for i,j in itertools.combinations(range(1,m),2)):
            lift=Q
            break
    assert lift is not None
    from math import lcm
    scale=lcm(*(x.denominator for p in lift for x in p))
    Q=[[int(x*scale) for x in p] for p in lift]
    c2,g2,md2=geometric_data(Q,n+1)
    B2=(B<<1)|1
    T2=T<<1
    assert all((B2|2**t) in g2[n] for t in vertices(T2))
    assert T2 in c2[4]
    result['lift_control']=dict(n=n+1,m=len(Q),scale=scale,P=Q,
                               cap5=0,ngons=0,min_abs_det=md2,
                               common_blue=vertices(B2),four_cap=vertices(T2))
    return result


def main():
    source=HERE/'findings.json'
    data=json.loads(source.read_text())
    for w in data['obstructions']:
        raw=Path(w['source']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==w['source_sha256']
        original=json.loads(raw)
        original=original.get('P',original.get('points'))
        assert [original[i] for i in w['source_indices']]==w['P']
    report=dict(label='COMPUTED',status='PASS',findings_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                obstructions=[check_obstruction(w) for w in data['obstructions']],
                positive_controls=[])
    for n in (7,8):
        P=[(0,0),(1,-4),(2,8),(4,10),(5,-4),(6,0),(8,1)]
        if n==8:
            P.insert(3,(3,-5))
        report['positive_controls'].append(dict(n=n,P=P,threshold_audit=threshold_audit(P,n)))
    failed=data['failed_construction']['five_cap']
    assert all(orient(failed,i,i+1,i+2)<0 for i in range(3))
    report['failed_construction_confirmed']=True
    report['elapsed_seconds']=time.monotonic()-START
    report['max_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    target=HERE/'independent_check.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',seconds=report['elapsed_seconds'],max_rss_kib=report['max_rss_kib'],
                         obstructions=[{k:v for k,v in w.items() if k in ['n','m','cap4','targets','cap5','ngons','min_abs_det','threshold_audit']}
                                       for w in report['obstructions']],
                         positive_controls=[dict(n=w['n'],**w['threshold_audit']) for w in report['positive_controls']])))


if __name__=='__main__':
    main()
