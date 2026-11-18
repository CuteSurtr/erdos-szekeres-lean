"""Small fixed exact controls. Run with the outer one-CPU/AS/time limits."""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess

from exact_envelope import (cap, convex, convex_certificate, exposure,
                            finite_test, model, serial, upper_hull, value)

HERE = Path(__file__).resolve().parents[1]
SELECTION = HERE.parents[1]
POOL = Path('/home/jay/research/data/delta3-codex-20261113/selection/rooted')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pool_points(path):
    words = path.read_text().split()
    assert words[:2] == ['D3POOL', '1']
    pos, result = 3, []
    for _ in range(int(words[2])):
        m = int(words[pos]); pos += 1
        p = [list(map(int, words[pos+2*j:pos+2*j+2])) for j in range(m)]
        pos += 2*m
        result.append(p)
    assert pos == len(words)
    return result


def freeze(path):
    inputs = []
    for n in (6, 7, 8):
        src = HERE.parent/'data'/f'n{n}-boundary.json'
        p = json.loads(src.read_text())['P'][:-1]
        inputs.append(dict(name=f'boundary-n{n}-old', n=n, P=p,
                           source=str(src), source_sha256=digest(src),
                           operation='remove rightmost point'))
    src = SELECTION/'terminal/data/witness.json'
    p = json.loads(src.read_text())['P']
    inputs.append(dict(name='terminal18', n=7, P=p, source=str(src),
                       source_sha256=digest(src), known_A=[0,5,6,7,8]))
    for n in (7, 8):
        src = POOL/f'full-n{n}.pool'
        ps = pool_points(src)
        # A fixed modest sample: the two smallest records, ties by pool index.
        for i in sorted(range(len(ps)), key=lambda i:(len(ps[i]), i))[:2]:
            inputs.append(dict(name=f'pool-n{n}-index{i}', n=n, P=ps[i],
                               source=str(src), source_sha256=digest(src),
                               zero_based_index=i))
    path.write_text(json.dumps(inputs, indent=2)+'\n')
    print(json.dumps([dict(name=r['name'],m=len(r['P'])) for r in inputs]))


def sat(clauses, m, path):
    body = f'p cnf {m} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)
    path.write_text(body)
    try:
        proc = subprocess.run(['/usr/bin/cadical', '-q', str(path)],
                              text=True, capture_output=True, timeout=2)
        path.with_suffix('.finder.log').write_text(proc.stdout+proc.stderr)
    except subprocess.TimeoutExpired as e:
        path.with_suffix('.finder.log').write_bytes((e.stdout or b'')+(e.stderr or b'')+b'\nTIMEOUT\n')
        return dict(outcome='UNKNOWN_TIMEOUT')
    if proc.returncode != 10:
        return dict(outcome='UNSAT_UNCERTIFIED' if proc.returncode == 20 else 'UNKNOWN',
                    exit_code=proc.returncode)
    lits = [int(t) for row in proc.stdout.splitlines() if row.startswith('v ')
            for t in row[2:].split() if t!='0']
    positive = {l for l in lits if l>0}
    assert all(any((l>0)==(abs(l) in positive) for l in c) for c in clauses)
    return dict(outcome='SAT_EXACT_MODEL_CHECKED', A=sorted(i-1 for i in positive),
                exit_code=proc.returncode)


def certificates(g, A):
    rows = []
    for t in g['caps3']:
        if not set(t)<=set(A):
            continue
        s = g['states'][t[-2:]]
        assert s['safe']
        support = []
        for l,w in s['certificate']:
            pair = next(pair for pair,q in g['ambient'].items() if q==l)
            support.append(dict(pair=pair, ambient_fourcap=g['pair_caps'][pair],
                                weight=w, line=l))
        rows.append(dict(triple=t, line=s['line'], supports=support))
    return rows


def run_case(r, out):
    p, n = r['P'], r['n']
    m = len(p)
    g = model(p)
    assert not any(cap(p, c) for c in combinations(range(m), 5))
    assert not any(convex(p, h) for h in combinations(range(m), n))
    targets = [h for h in combinations(range(m),n-1) if convex(p,h)]
    clauses = [[i+1 for i in h] for h in targets]
    clauses += [[-i-1 for i in c] for c in g['caps4']]
    clauses += [[-i-1 for i in t] for t in g['bad']]
    cnf = out/f"{r['name']}.cnf"
    result = sat(clauses, m, cnf)
    report = dict(name=r['name'], m=m, n=n, label='COMPUTED',
                  no_fivecap=True, no_ngon=True, targets=len(targets),
                  fourcaps=len(g['caps4']), exposed_triples=len(g['bad']),
                  ambient_lines=len(g['ambient']),
                  right_breaks=[t for _,t in g['hull'] if t is not None and t>0],
                  formula_variables=m, formula_clauses=len(clauses),
                  cnf_sha256=digest(cnf), result=result)
    if result['outcome']=='SAT_EXACT_MODEL_CHECKED':
        A = result['A']
        assert not any(cap(p,c) for c in combinations(A,4))
        assert all(set(h)&set(A) for h in targets)
        report['all_X_certificates'] = certificates(g,A)
    if 'known_A' in r:
        A = r['known_A']
        assert not any(cap(p,c) for c in combinations(A,4))
        assert all(set(h)&set(A) for h in targets)
        report['known_A_certificates'] = certificates(g,A)
    report['exposures'] = [dict(pair=pair, line=s['line'], interval=s['interval'])
                           for pair,s in g['states'].items() if not s['safe']]
    return report


def small_controls():
    lines = [(Q(0),Q(2)), (Q(2),Q(-2))]
    tests = [((Q(1),Q(0)), True), ((Q(1),Q(1)), False),
             ((Q(2),Q(-1)), False), ((Q(3),Q(-100)), False),
             ((Q(0),Q(3)), False), ((Q(0),Q(2)), True)]
    rows = []
    for q, expected in tests:
        safe = finite_test(q, upper_hull(lines))
        exp = exposure(q,lines)
        cert = convex_certificate(q,lines)
        assert safe==expected==(exp is None)==(cert is not None)
        if exp is not None:
            a,b=exp; t=a+1 if b is None else (a+b)/2
            assert t>0 and all(value(q,t)>value(l,t) for l in lines)
        rows.append(dict(q=q,safe=safe,exposure=exp,certificate=cert))
    assert len(rows[0]['certificate'])==2
    assert exposure((Q(0),Q(0)),[]) == (Q(0),None)
    assert finite_test((Q(0),Q(0)),upper_hull([(Q(1),Q(0))]))
    cup = [(i,i*i) for i in range(6)]
    cg = model(cup)
    assert not cg['caps3'] and not cg['caps4'] and convex(cup,tuple(range(6)))
    p = [(0,0),(1,3),(2,5),(3,6),(4,100),(5,120),(6,130)]
    g = model(p)
    assert not any(cap(p,c) for c in combinations(range(7),5))
    assert not any(convex(p,c) for c in combinations(range(7),6))
    A4 = [0,1,2,3]
    assert cap(p,A4)
    assert all(g['states'][t[-2:]]['safe'] for t in combinations(A4,3))
    targets = [h for h in combinations(range(7),5) if convex(p,h)]
    A, R = {0,4,5}, {4}
    badA = [t for t in g['bad'] if set(t)<=A]
    assert targets and badA
    assert min(len(A & set(h)) for h in targets)>=2
    assert all(R & set(t) for t in badA)
    assert all((A-R) & set(h) for h in targets)
    assert all(not set(t)<=A-R for t in g['bad'])
    return dict(label='COMPUTED', algebra_lines=lines, algebra_cases=rows,
                caveat='Algebra line examples are not claimed cap-realizable.',
                empty_ambient_cup=dict(P=cup,n=7,A=[0],target_count=1),
                fourcap_clauses_needed=dict(P=p,A=A4,certificates=certificates(g,A4)),
                uniform_repair=dict(P=p,n=6,A=sorted(A),R=sorted(R),
                                    repaired_A=sorted(A-R),targets=targets,
                                    bad_triples_in_A=badA,
                                    minimum_hits=min(len(A&set(h)) for h in targets)))


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--freeze',type=Path)
    ap.add_argument('--inputs',type=Path)
    ap.add_argument('--out',type=Path)
    ap.add_argument('--first',type=int,default=0)
    ap.add_argument('--last',type=int,default=100)
    ap.add_argument('--small',action='store_true')
    args=ap.parse_args()
    if args.freeze:
        freeze(args.freeze)
    else:
        args.out.mkdir(parents=True,exist_ok=True)
        if args.small:
            r=small_controls()
            (args.out/'small_controls.json').write_text(json.dumps(serial(r),indent=2)+'\n')
            print('small exact controls passed')
        if args.inputs:
            records=json.loads(args.inputs.read_text())[args.first:args.last]
            for r in records:
                report=run_case(r,args.out)
                (args.out/(r['name']+'.json')).write_text(json.dumps(serial(report),indent=2)+'\n')
                print(json.dumps({k:report[k] for k in ('name','m','n','targets','fourcaps','exposed_triples','right_breaks','result')},default=str),flush=True)
