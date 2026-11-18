"""Only test A=L4 union B, B subset L5, on four fixed real fixtures."""
from fractions import Fraction as F
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback
from verify_structure2 import (signs_of, convex, ranks_by_subsets, four_caps,
                               maxgon, line, certificate, serial)


def mask(vertices):return sum(1<<i for i in vertices)


def exposed(q,ambient):
    lo=F(0);hi=None
    for r in ambient.values():
        d,e=q[0]-r[0],q[1]-r[1]
        if d==0:
            if e<=0:return None
        elif d>0:lo=max(lo,-e/d)
        elif hi is None:hi=-e/d
        else:hi=min(hi,-e/d)
    if hi is not None and lo>=hi:return None
    t=lo+1 if hi is None else (lo+hi)/2
    assert t>0 and all(q[0]*t+q[1]>r[0]*t+r[1] for r in ambient.values())
    return t


def analyze(p):
    vertices=list(range(len(p)));s=signs_of(p)
    six_cups=[t for t in combinations(vertices,6) if all(s[a]>0 for a in combinations(t,3))]
    if six_cups:
        # Keep this input as a negative premise control; do not apply an n7
        # maxcup-five rank argument to the parent's other real obstruction.
        beta={i:1 for i in vertices}
        for k in range(2,len(p)+1):
            for t in combinations(vertices,k):
                if all(s[a]>0 for a in combinations(t,3)):beta[t[-1]]=max(beta[t[-1]],k)
        return dict(status='OUTSIDE_HYPOTHESES',P=p,beta=[beta[v] for v in vertices],
                    maxcup=max(beta.values()),six_cups=six_cups,selection_tested=False)
    beta=ranks_by_subsets(s,vertices);caps=four_caps(s,vertices)
    assert max(beta.values())==5 and maxgon(s,vertices)==6
    L4=[v for v in vertices if beta[v]==4];L5=[v for v in vertices if beta[v]==5]
    T=sorted(L4+L5);Tmask=mask(T);fixed=mask(L4)
    assert len(L5)<=16
    hs=[t for t in combinations(vertices,6) if convex(p,t)]
    ambient={cap[-2:]:line(p,*cap[-2:]) for cap in caps}
    protection={};cap_triples=[t for t in combinations(T,3) if s[t]<0]
    for b,c in sorted({t[-2:] for t in cap_triples}):
        direct=[uv for uv in ambient if uv[0]>=b and uv[1]>=c and
                all(s[t]>0 for t in combinations(sorted(set((b,c)+uv)),3))]
        closure=[(u,v) for u,v in ambient if u>=b and v>=c and
                 (v==c or s[b,c,v]>0) and (u==b or s[b,u,v]>0)]
        cert=certificate(line(p,b,c),ambient);witness=exposed(line(p,b,c),ambient)
        assert (cert is None)==(witness is not None)
        assert not direct or closure
        assert not closure or cert
        protection[b,c]=dict(terminal=(b,c) in ambient,direct=bool(direct),
             closure=bool(closure),uniform=cert is not None,direct_pairs=direct,
             closure_pairs=closure,uniform_certificate=cert,exposed_t=witness)
    rows=[dict(kind='target',vertices=t,positive=True) for t in hs if not fixed&mask(t)]
    rows.extend(dict(kind='fourcap',vertices=t,positive=False) for t in caps if mask(t)&Tmask==mask(t))
    selections={mode:[] for mode in ('ordinary','terminal','direct','closure','uniform')}
    choices=[]
    for bits in range(1<<len(L5)):
        B=[v for j,v in enumerate(L5) if bits>>j&1];A=sorted(L4+B);am=mask(A)
        if any((not am&mask(row['vertices'])) if row['positive'] else
               (am&mask(row['vertices'])==mask(row['vertices'])) for row in rows):continue
        selections['ordinary'].append(A)
        for mode in ('terminal','direct','closure','uniform'):
            if all(protection[t[-2:]][mode] for t in cap_triples if am&mask(t)==mask(t)):
                selections[mode].append(A)
        choices.append(dict(A=A,selected_cap_triples=[t for t in cap_triples if am&mask(t)==mask(t)]))
    # An irreducible finite row core, if ordinary or uniform existence fails.
    cores={}
    for mode in ('ordinary','uniform'):
        if selections[mode]:continue
        current=list(rows)
        if mode=='uniform':
            current.extend(dict(kind='exposed_triple',vertices=t,positive=False,
                         exposed_t=protection[t[-2:]]['exposed_t'])
                         for t in cap_triples if not protection[t[-2:]]['uniform'])
        assignments=[fixed|mask([v for j,v in enumerate(L5) if bits>>j&1]) for bits in range(1<<len(L5))]
        def has_choice(constraints):
            return any(all(bool(a&mask(row['vertices'])) if row['positive'] else
                           a&mask(row['vertices'])!=mask(row['vertices'])
                           for row in constraints) for a in assignments)
        assert not has_choice(current)
        for row in list(current):
            rest=[r for r in current if r is not row]
            if not has_choice(rest):current=rest
        cores[mode]=current
    return dict(P=p,beta=[beta[v] for v in vertices],L4=L4,L5=L5,
        maxcap=4 if caps else 3,maxcup=5,maxgon=6,hexagon_count=len(hs),
        assignments=1<<len(L5),counts={k:len(v) for k,v in selections.items()},
        minimum={k:min(v,key=lambda a:(len(a),a)) if v else None for k,v in selections.items()},
        all_uniform=selections['uniform'],protection=protection,failed_row_cores=cores,
        missed_by_L4=[t for t in hs if not fixed&mask(t)])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists()
    root=Path(__file__).resolve().parents[1];start=time.monotonic();result={}
    inputs={}
    try:
        old=root/'data/initial_profiles.json';inputs[str(old)]=hashlib.sha256(old.read_bytes()).hexdigest()
        fixtures={k:v['P'] for k,v in json.loads(old.read_text())['fixtures'].items()}
        nine=root/'data/closure_examples_replay.json';inputs[str(nine)]=hashlib.sha256(nine.read_bytes()).hexdigest()
        fixtures['closure9']=json.loads(nine.read_text())['closure9']['P']
        fifteen=root.parent/'model15_audit/data/real15.coordinates.json'
        inputs[str(fifteen)]=hashlib.sha256(fifteen.read_bytes()).hexdigest()
        fixtures['real15']=json.loads(fifteen.read_text())['P']
        result['fixtures']={}
        for name,p in fixtures.items():
            r=analyze(p);result['fixtures'][name]=r
            if r.get('status')=='OUTSIDE_HYPOTHESES':
                print(json.dumps(dict(name=name,**r)),flush=True);continue
            print(json.dumps(dict(name=name,beta=r['beta'],L4=r['L4'],L5=r['L5'],
                 counts=r['counts'],minimum=r['minimum'],failed_row_cores=serial(r['failed_row_cores']))),flush=True)
        result['status']='PASS'
        result['label']='COMPUTED exact fixed-fixture candidate tests; not a general theorem'
    except Exception:
        result['status']='FAIL';result['traceback']=traceback.format_exc();raise
    finally:
        result['inputs']=inputs;result['elapsed_seconds']=time.monotonic()-start
        result['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        result['helper_sha256']=hashlib.sha256(Path(__file__).with_name('verify_structure2.py').read_bytes()).hexdigest()
        args.out.write_text(json.dumps(serial(result),indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k not in ('fixtures','inputs')}))


if __name__=='__main__':main()
