#!/usr/bin/env python3
"""Bounded exact projection comparison. Use installed venv; no downloads.

Each --m/--n invocation is a separate <30s probe. No frontier SAT.
Reports are written incrementally; an exception is a failed control.
"""
import argparse
from collections import defaultdict
from itertools import combinations
import json
import os
from pathlib import Path
import subprocess
import time

os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
from pysat.solvers import Glucose4

HERE = Path(__file__).resolve().parent
WORK = Path('/home/jay/research/data/delta3-codex-20261113/resume/compact')
OLD = Path('/home/jay/research/data/delta3-codex-20261113/encoder/delta_cnf')
NEW = WORK/'compact_cnf'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_cnf(path):
    phases = defaultdict(list)
    phase, clauses, nv = 'unlabelled', [], None
    for line in path.read_text().splitlines():
        w = line.split()
        if not w:
            continue
        if w[0] == 'p':
            nv, nc = map(int, w[2:])
        elif w[0] == 'c':
            if w[1:2] == ['phase']:
                phase = w[2]
        else:
            row = list(map(int, w))
            require(row[-1] == 0 and 0 not in row[:-1], 'bad clause')
            clauses.append(row[:-1])
            phases[phase].append(row[:-1])
    require(len(clauses) == nc, 'clause count mismatch')
    return nv, clauses, phases


def write_cnf(path, nv, clauses):
    with path.open('w') as f:
        f.write(f'p cnf {nv} {len(clauses)}\n')
        for c in clauses:
            f.write(' '.join(map(str, [*c, 0]))+'\n')


def generate(folder, m, n, conv, pool, containment):
    folder.mkdir(parents=True, exist_ok=False)
    opts = ['--m', str(m), '--n', str(n)]
    p = subprocess.run([str(NEW), *opts, '--convex', conv, '--pool', pool,
                        '--containment', containment, '--out', str(folder/'new.cnf'),
                        '--map', str(folder/'new.map')], capture_output=True, text=True, timeout=3)
    (folder/'new.encode.log').write_text(p.stdout+p.stderr)
    require(p.returncode == 0, 'new generation failed')
    p = subprocess.run([str(OLD), *opts, '--mode', 'weak', '--sym', 'none',
                        '--pool', 'lattice', '--out', str(folder/'old.cnf')],
                       capture_output=True, text=True, timeout=3)
    (folder/'old.encode.log').write_text(p.stdout+p.stderr)
    require(p.returncode == 0, 'old generation failed')
    nn, new, phases = read_cnf(folder/'new.cnf')
    on, old, _ = read_cnf(folder/'old.cnf')
    newpool = phases.pop('forall_delta')
    newdefs = [c for rows in phases.values() for c in rows]
    olddefs, oldpool = old[:-(1 << m)], old[-(1 << m):]
    qdefs = [c for name in ('signotope', 'convex4_equivalence', 'convex_larger_equivalence')
             for c in phases[name]]
    qm = [(int(row.split()[0]), int(row.split()[2]))
          for row in (folder/'new.map').read_text().splitlines()
          if row and not row.startswith('#') and row.split()[1] == 'convex']
    return nn, newdefs, newpool, on, olddefs, oldpool, qdefs, qm


def configurations(m):
    ts = list(combinations(range(m), 3))
    tid = {t:i+1 for i,t in enumerate(ts)}
    clauses = []
    # Independent truth-table packet clauses, not the new ternary family.
    for s in combinations(range(m), 4):
        v = [tid[t] for t in combinations(s, 3)]
        for bits in range(16):
            b = [(bits >> i) & 1 for i in range(4)]
            if sum(x != y for x,y in zip(b,b[1:])) > 1:
                clauses.append([-v[i] if b[i] else v[i] for i in range(4)])
    with Glucose4(bootstrap_with=clauses) as solver:
        while solver.solve():
            model = {abs(x): x > 0 for x in solver.get_model()}
            literals = [i if model[i] else -i for i in range(1, len(ts)+1)]
            yield literals, {t:model[i] for t,i in tid.items()}
            solver.add_clause([-x for x in literals])


def semantics(t, m, n):
    full = (1 << m)-1
    ids = lambda s: tuple(i for i in range(m) if s >> i & 1)
    mask = lambda s: sum(1 << i for i in s)
    convex = lambda s: all(t[a,b,c] == t[a,b,d] and t[a,c,d] == t[b,c,d]
                           for a,b,c,d in combinations(ids(s), 4))
    cap = lambda s: all(not t[q] for q in combinations(s, 3))
    caps = [mask(s) for s in combinations(range(m), 4) if cap(s)]
    targets = [mask(s) for s in combinations(range(m), n-1) if convex(mask(s))]
    valid = (not any(cap(s) for s in combinations(range(m), 5)) and
             not any(convex(mask(s)) for s in combinations(range(m), n)))
    fail = [any(k & d == k for k in caps) or any(k & d == 0 for k in targets)
            for d in range(full+1)]
    return valid, fail, convex


def exhaustive(args):
    started = time.monotonic()
    tag = f'm{args.m}n{args.n}-{args.convex}-{args.pool}-{args.containment}'
    folder = WORK/('tiny-'+tag)
    nn, nd, np, on, od, op, qd, qm = generate(folder, args.m, args.n, args.convex,
                                             args.pool, args.containment)
    masklist = (list(range(1 << args.m)) if args.pool == 'all' else
                [d for d in range(1 << args.m) if 3 <= d.bit_count() <= args.m-args.n+2])
    require(len(np) == len(masklist) or (not masklist and np == [[]]), 'pool mask count')
    ng = [nn+1+i for i in range(len(np))]
    og = [on+1+i for i in range(1 << args.m)]
    report = dict(label='COMPUTED', status='RUNNING', m=args.m, n=args.n,
                  convex=args.convex, pool=args.pool, containment=args.containment,
                  configurations=0, valid=0, pool_queries=0, wrong_flag_queries=0,
                  base_queries=0, mismatches=0)
    dest = HERE/(tag+'.json')
    dest.write_text(json.dumps(report, indent=2)+'\n')
    with Glucose4(bootstrap_with=nd+[[ -g, *c] for g,c in zip(ng,np)]) as ns, \
         Glucose4(bootstrap_with=od+[[ -g, *c] for g,c in zip(og,op)]) as osolver, \
         Glucose4(bootstrap_with=qd) as qs:
        for literals,t in configurations(args.m):
            valid, fail, convex = semantics(t, args.m, args.n)
            require(ns.solve(assumptions=literals) == valid, 'new base mismatch')
            require(osolver.solve(assumptions=literals) == valid, 'old base mismatch')
            report['base_queries'] += 2
            report['configurations'] += 1
            report['valid'] += valid
            for ident, s in qm:
                wrong = -ident if convex(s) else ident
                require(not qs.solve(assumptions=literals+[wrong]), 'flag not an equivalence')
                report['wrong_flag_queries'] += 1
            if valid:
                for i,d in enumerate(masklist):
                    expected = fail[d]
                    require(ns.solve(assumptions=literals+[ng[i]]) == expected, 'new pool mismatch')
                    require(osolver.solve(assumptions=literals+[og[d]]) == expected, 'old pool mismatch')
                    report['pool_queries'] += 2
                # Check the omitted masks' mathematical coverage, separately.
                if args.pool == 'reduced':
                    reduced_fails = all(fail[d] for d in masklist) if masklist else False
                    require(reduced_fails == all(fail), 'reduced universal coverage mismatch')
    require(report['configurations'] == {4:8, 5:62, 6:908}[args.m], 'enumeration incomplete')
    report.update(status='PASS', seconds=round(time.monotonic()-started, 6), scratch=str(folder))
    dest.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report))


def retained_fixture():
    p = [[0,0],[1,3],[2,-2],[3,3],[4,0]]
    m, n = 5, 6
    def det(a,b,c):
        a,b,c = p[a],p[b],p[c]
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    ds = [det(*s) for s in combinations(range(m),3)]
    require(all(ds), 'fixture degeneracy')
    signs = [i+1 if x>0 else -i-1 for i,x in enumerate(ds)]
    folder = HERE/'tiny_examples'
    nn, nd, np, on, od, op, _, _ = generate(folder,m,n,'recurrence','all','witness')
    rows = []
    for name,d,expected in [('missed_gon',0,True), ('working_delta',1,False), ('fourcap_delta',27,True)]:
        for encoder,nv,defs,pool in [('new',nn,nd,np),('old',on,od,op)]:
            clauses = defs+[[x] for x in signs]+[pool[d]]
            path = folder/f'{name}-{encoder}.cnf'
            write_cnf(path,nv,clauses)
            with Glucose4(bootstrap_with=clauses) as solver:
                result = solver.solve()
                require(result == expected, 'real fixture projected-query mismatch')
                if result:
                    model = solver.get_model()
                    values = {abs(x): x > 0 for x in model}
                    require(all(any(values[abs(x)] == (x>0) for x in c) for c in clauses),
                            'SAT model fails emitted clause')
                    (folder/f'{name}-{encoder}.model').write_text(' '.join(map(str,model))+' 0\n')
                rows.append(dict(name=name, delta_mask=d, encoder=encoder, sat=result, cnf=str(path)))
    report = dict(label='COMPUTED', status='PASS', P=p, m=m, n=n,
                  statement='Individual Delta-failure queries, not full counterexample formulas',
                  signs=''.join('+' if x>0 else '-' for x in ds), results=rows)
    (folder/'controls.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(report))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m', type=int, choices=[4,5,6])
    ap.add_argument('--n', type=int)
    ap.add_argument('--convex', default='recurrence', choices=['recurrence','direct'])
    ap.add_argument('--pool', default='all', choices=['all','reduced'])
    ap.add_argument('--containment', default='witness', choices=['witness','exact'])
    ap.add_argument('--fixture', action='store_true')
    args = ap.parse_args()
    if args.fixture:
        retained_fixture()
    else:
        require(args.m is not None and args.n is not None, 'need m and n')
        exhaustive(args)


if __name__ == '__main__':
    main()
