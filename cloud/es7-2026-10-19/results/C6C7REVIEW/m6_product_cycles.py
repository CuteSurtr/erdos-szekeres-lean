#!/usr/bin/env python3
"""Exact rotation-quotiented GP product-cycle search; no SAT or numeric LP.

For each GP identity [abc][ade]-[abd][ace]+[abe][acd]=0 with nonzero
brackets, its uniquely signed term has absolute value strictly larger than
either other term. A graph edge goes from that larger product to a smaller
product. Rotation identifies absolute brackets. A directed cycle is a
strict product contradiction, valid for realizations with that rotation.
No cycle is only a failure of this restricted search, not realizability.

Input model is the positive-variable list saved by ROT456/tools/cegar_gp.py.
Triple IDs are reconstructed independently by sorted minimal rotated triples.
"""
import argparse
from array import array
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import resource
import sys
import time


def parity(xs):
    return -1 if sum(xs[i] > xs[j] for i in range(3) for j in range(i+1, 3)) % 2 else 1


def rotate(x, s, m):
    return (x // m) * m + (x % m + s) % m


def canonical(triple, m):
    images = [tuple(rotate(x, s, m) for x in triple) for s in range(m)]
    best = min(tuple(sorted(x)) for x in images)
    signs = {parity(x) for x in images if tuple(sorted(x)) == best}
    assert len(signs) == 1, ('odd stabilizer', triple)
    return best, signs.pop()


def terms(q):
    a,b,c,d,e = q
    return (((a,b,c),(a,d,e),1), ((a,b,d),(a,c,e),-1), ((a,b,e),(a,c,d),1))


def cycle(graph):
    """Return directed edges (source,target,witness) of one cycle, or None."""
    color = {}
    parent = {}
    for start in graph:
        if color.get(start, 0):
            continue
        color[start] = 1
        stack = [(start, iter(graph.get(start, {}).items()))]
        while stack:
            u, it = stack[-1]
            try:
                v, witness = next(it)
            except StopIteration:
                color[u] = 2
                stack.pop()
                continue
            state = color.get(v, 0)
            if state == 0:
                color[v] = 1
                parent[v] = (u, witness)
                stack.append((v, iter(graph.get(v, {}).items())))
            elif state == 1:
                found = [(u,v,witness)]
                x = u
                while x != v:
                    p, w = parent[x]
                    found.append((p,x,w))
                    x = p
                found.reverse()
                return found
    return None


def pack(q, other):
    value = other
    for x in q:
        value = value * 64 + x
    return value


def unpack(value):
    rev = []
    for _ in range(5):
        rev.append(value % 64)
        value //= 64
    return tuple(reversed(rev)), value


def selftest():
    assert cycle({1:{2:10},2:{3:11},3:{1:12}}) is not None
    assert cycle({1:{2:10,3:11},2:{3:12}}) is None
    assert cycle({1:{1:7}}) == [(1,1,7)]
    q=(3,12,22,45,59)
    for j in range(3):
        assert unpack(pack(q,j)) == (q,j)
    # Independent integer points verify the GP identity and strict comparison.
    pts=[(i,i*i+i**3) for i in range(7)]
    det=lambda t: ((pts[t[1]][0]-pts[t[0]][0])*(pts[t[2]][1]-pts[t[0]][1])
                   -(pts[t[1]][1]-pts[t[0]][1])*(pts[t[2]][0]-pts[t[0]][0]))
    checked=0
    for a in range(7):
        for rest in itertools.combinations([i for i in range(7) if i!=a],4):
            tt=terms((a,)+rest)
            vv=[det(x)*det(y)*sg for x,y,sg in tt]
            assert sum(vv)==0 and all(vv)
            mi=next(i for i in range(3) if sum((v>0)==(vv[i]>0) for v in vv)==1)
            assert all(abs(vv[mi])>abs(vv[j]) for j in range(3) if j!=mi)
            checked+=1
    return checked


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model',required=True,type=Path)
    ap.add_argument('--map',required=True,type=Path)
    ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--max-seconds',type=float,default=1100)
    ap.add_argument('--max-edges',type=int,default=2500000)
    ap.add_argument('--full',action='store_true',help='Try all-point identities after small restrictions')
    ap.add_argument('--max-layers',type=int,choices=(2,3),default=3)
    args=ap.parse_args()
    start=time.monotonic()
    deadline=start+args.max_seconds
    args.out.mkdir(parents=True,exist_ok=True)
    log=(args.out/'m6_cycles.log').open('w',buffering=1)
    def emit(obj):
        obj['seconds']=round(time.monotonic()-start,3)
        obj['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        line=json.dumps(obj,sort_keys=True)
        print(line,flush=True)
        log.write(line+'\n')
    emit({'event':'selftest','integer_gp_identities':selftest(),'passed':True})
    meta=json.loads(args.map.read_text())
    m,t=meta['m'],meta['t']; n=m*t
    assert n<64 and m==6 and t==10
    positive=set(json.loads(args.model.read_text()))
    triples=list(itertools.combinations(range(n),3))
    cmap={q:canonical(q,m) for q in triples}
    reps=sorted({x[0] for x in cmap.values()})
    ids={q:i+1 for i,q in enumerate(reps)}
    assert len(reps)==meta['ntriple']
    width=len(reps)+1
    oriented=array('h',[0])*(n*n*n)
    for q,(rep,sg) in cmap.items():
        v=ids[rep]
        for p in itertools.permutations(q):
            oriented[(p[0]*n+p[1])*n+p[2]]=sg*parity(p)*v
    def lit(q):
        return oriented[(q[0]*n+q[1])*n+q[2]]
    def sign(l):
        return (1 if abs(l) in positive else -1)*(1 if l>0 else -1)
    def product(x,y):
        x,y=abs(x),abs(y)
        return min(x,y)*width+max(x,y)
    def comparisons(layers):
        pts=[m*i+k for i in layers for k in range(m)]
        # A simultaneous rotation moves each anchor to phase zero, preserving
        # every absolute product. This covers all rotated GP identities.
        for layer in layers:
            a=m*layer
            rest=[x for x in pts if x!=a]
            for ii,(b,c,d,e) in enumerate(itertools.combinations(rest,4)):
                if ii%4096==0 and time.monotonic()>deadline:
                    raise TimeoutError
                q=(a,b,c,d,e)
                ll=[(lit(x),lit(y),co) for x,y,co in terms(q)]
                ss=[sign(x)*sign(y)*co for x,y,co in ll]
                if ss[0]==ss[1]==ss[2]:
                    raise ValueError(('GP sign violation',q,ss))
                mi=next(i for i in range(3) if ss.count(ss[i])==1)
                pp=[product(x,y) for x,y,_ in ll]
                yield q,[(pp[mi],pp[j],pack(q,j)) for j in range(3) if j!=mi]
    def verify(found):
        # Reconstruct each sign through canonical rotation independently of
        # the oriented lookup table and derive the minority term again.
        expo=Counter(); records=[]
        assert found and all(found[i][1]==found[(i+1)%len(found)][0] for i in range(len(found)))
        for u,v,w in found:
            q,j=unpack(w)
            tt=terms(q); ss=[]; pp=[]; used=[]
            for x,y,co in tt:
                rx,sx=canonical(x,m); ry,sy=canonical(y,m)
                ix,iy=ids[rx],ids[ry]
                ss.append(co*sx*sy*(1 if ix in positive else -1)*(1 if iy in positive else -1))
                pp.append(product(ix,iy)); used.append((rx,ry))
            mi=next(i for i in range(3) if ss.count(ss[i])==1)
            assert j!=mi and u==pp[mi] and v==pp[j]
            for r in used[mi]: expo[r]+=1
            for r in used[j]: expo[r]-=1
            records.append({'anchor_quintuple':q,'minority_term':mi,'other_term':j,
                            'term_signs':ss,'greater_orbits':used[mi],'lesser_orbits':used[j],'weight':1})
        assert all(v==0 for v in expo.values())
        return {'m':m,'t':t,'model_sha256':hashlib.sha256(args.model.read_bytes()).hexdigest(),
                'scope':'realizations invariant under the specified Euclidean rotation',
                'verified_exponent_cancellation':True,'comparisons':records}
    emit({'event':'input','model_sha256':hashlib.sha256(args.model.read_bytes()).hexdigest(),
          'map_sha256':hashlib.sha256(args.map.read_bytes()).hexdigest(),
          'm':m,'t':t,'triple_orbits':len(reps),'positive_variables':len(positive)})
    union={}; union_edges=0; union_complete=True; complete=0
    found=None
    try:
        for size in range(2,args.max_layers+1):
            for layers in itertools.combinations(range(t),size):
                graph={}; count=0
                for q,edges in comparisons(layers):
                    count+=1
                    for u,v,w in edges:
                        graph.setdefault(u,{})[v]=w
                        if union_complete:
                            row=union.setdefault(u,{})
                            if v not in row:
                                row[v]=w;union_edges+=1
                                if union_edges>args.max_edges:
                                    union_complete=False
                found=cycle(graph)
                complete+=1
                emit({'event':'restriction','layers':layers,'gp_identities':count,
                      'edges':sum(map(len,graph.values())),'cycle_length':len(found) if found else 0,
                      'union_edges':union_edges,'union_complete':union_complete})
                if found: break
            if found: break
        if not found:
            found=cycle(union)
            emit({'event':'small_restrictions_union','completed_restrictions':complete,
                  'edges':union_edges,'complete':union_complete,
                  'cycle_length':len(found) if found else 0})
        if not found and args.full and union_complete:
            count=0
            for q,edges in comparisons(range(t)):
                count+=1
                for u,v,w in edges:
                    row=union.setdefault(u,{})
                    if v not in row:
                        row[v]=w;union_edges+=1
                if count%100000==0:
                    found=cycle(union)
                    emit({'event':'full_progress','gp_identities':count,'edges':union_edges,
                          'cycle_length':len(found) if found else 0})
                    if found or union_edges>args.max_edges:
                        break
            if not found: found=cycle(union)
            emit({'event':'full_result','gp_identities':count,'edges':union_edges,
                  'complete':count==t*__import__('math').comb(n-1,4),
                  'cycle_length':len(found) if found else 0})
    except ValueError as exc:
        detail=exc.args[0]
        if not (isinstance(detail,tuple) and detail[0]=='GP sign violation'):
            raise
        _,q,sg=detail
        vv=sorted({abs(lit(x)) for x,y,_ in terms(q)} | {abs(lit(y)) for x,y,_ in terms(q)})
        violation={'anchor_quintuple':q,'term_signs':sg,'model_sha256':hashlib.sha256(args.model.read_bytes()).hexdigest(),
                   'candidate_clause':[-v if v in positive else v for v in vv]}
        (args.out/'gp_sign_violation.json').write_text(json.dumps(violation,indent=2)+'\n')
        emit({'event':'gp_sign_violation','anchor_quintuple':q,'candidate_clause':violation['candidate_clause']})
    except TimeoutError:
        emit({'event':'time_limit','completed_restrictions':complete,'edges':union_edges})
        found=cycle(union)
    if found:
        result=verify(found)
        p=args.out/'m6_cycle_witness.json'
        p.write_text(json.dumps(result,indent=2)+'\n')
        emit({'event':'certificate','comparisons':len(found),'independent_verify':True,
              'witness_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    else:
        emit({'event':'no_cycle','conclusion':'restricted search only; no realizability conclusion'})
    emit({'event':'stop'})
    log.close()

if __name__=='__main__':
    main()
