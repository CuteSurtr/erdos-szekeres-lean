#!/usr/bin/env python3
"""Supplemental controls using only this audit's own implementation."""
import argparse
from collections import Counter
from itertools import combinations, product, zip_longest
import json
from pathlib import Path
import resource
import subprocess
import time
import traceback

from check import (BIN, COMPACT, DATA, EXT, SCRATCH, Geometry, Reconstruction,
                   clauses, det, frozen, mask, sha, subsets, upclosure, verts)

ROOT = SCRATCH.parent


def filtered(m,n,k,path):
    parent = ROOT/f'terminal{n}-a/m{m}/input.cnf'
    e = Reconstruction(m,n,str(parent)+'.map')
    selected = iter(s for s in range(1<<m) if s.bit_count()<=m-n+2)
    count, retained, phases = 0, [], Counter()
    actual = iter(clauses(path))
    for phase,row in e.rows():
        if phase=='forall_terminal_delta':
            s = next(selected)
            if s.bit_count()>k:
                continue
            retained.append(s)
        assert next(actual,None)==(phase,row)
        count += 1;phases[phase] += 1
    assert next(selected,None) is None and next(actual,None) is None
    header = Path(path).open().readline().split()
    assert (int(header[2]),int(header[3]))==(e.nv,count)
    # An independent cardinality enumeration checks the index-to-mask range.
    from math import comb
    assert len(retained)==sum(comb(m,j) for j in range(min(k,m-n+2)+1))
    return {'m':m,'n':n,'k':k,'variables':e.nv,'clauses':count,
            'selection_rows':len(retained),'selection_counts':dict(Counter(s.bit_count() for s in retained)),
            'all_other_families_unchanged':True,'parent_sha256':sha(parent),
            'map_sha256':sha(str(parent)+'.map'),'filtered_sha256':sha(path)}


def filters():
    cases = [(7,11,2),(7,11,3),(7,12,3),(7,12,4),(8,13,3),(8,13,4)]
    results = []
    for n,m,k in cases:
        case = ROOT/f'small-delta/n{n}m{m}k{k}'
        r = filtered(m,n,k,case/'input.cnf')
        receipt = json.loads((case/'solve/result.json').read_text())
        r['parent_status'] = receipt['status']
        r['result_sha256'] = sha(case/'solve/result.json')
        results.append(r)
    return {'cases':results,'filter_source_sha256':sha(EXT/'small_delta.py'),
            'scope':'SAT excludes only selections up to k; UNKNOWN proves nothing.'}


def domain():
    directory = SCRATCH/'domain'
    directory.mkdir(exist_ok=False)
    records = []
    for n in range(5,9):
        for m in range(n-1,n+2):
            path = directory/f'm{m}n{n}.cnf'
            p = subprocess.run([str(BIN),str(m),str(n),str(path)],text=True,
                               capture_output=True,timeout=18)
            assert p.returncode==0
            from check import check_formula
            report = check_formula(path,m,n)
            # k<=2 forces actual empty clauses; k=3 does not justify dropping smaller rows.
            empty = sum(not row for _,row in clauses(path))
            if m<=n:
                assert empty>0
            report['empty_clauses']=empty
            records.append(report)
    rejected = []
    for m,n in ((3,5),(4,6),(6,8),(21,7),(9,4),(9,9)):
        p = subprocess.run([str(BIN),str(m),str(n),'--stats'],text=True,
                           capture_output=True,timeout=18)
        assert p.returncode!=0 and 'bad_parameters' in p.stderr
        rejected.append({'m':m,'n':n,'returncode':p.returncode,'stderr':p.stderr.strip()})
    return {'supported_edge_cases':records,'rejected_out_of_domain':rejected}


def mutants():
    f = next(x for x in frozen() if x['name']=='n6-root-old')
    g = Geometry(f['P'],6)
    e = Reconstruction(9,6,geometry=g)
    rows = list(e.rows())
    assignment = e.assignment
    mapping = [line.split() for line in (SCRATCH/'m9n6/input.cnf.map').read_text().splitlines()
               if not line.startswith('#')]
    exact = {int(i):kind for i,kind,s in mapping if kind in
             ('convex','terminal_fourcap','terminal_bad_triple')}
    definitions = [(phase,row) for phase,row in rows if 'equivalence' in phase]
    involved = {}
    for phase,row in definitions:
        for var in {abs(x) for x in row} & exact.keys():
            involved.setdefault(var,[]).append(row)
    rejected = Counter()
    for var,kind in exact.items():
        assignment[var] ^= 1
        bad = any(not any(bool(assignment[abs(x)])==(x>0) for x in row) for row in involved[var])
        assignment[var] ^= 1
        assert bad
        rejected[kind] += 1
    false_internal = bytearray(assignment)
    changed = 0
    for i,kind,s in mapping:
        if kind in ('bad_contains','target_contains'):
            changed += bool(false_internal[int(i)])
            false_internal[int(i)] = 0
    assert changed
    assert all(any(bool(false_internal[abs(x)])==(x>0) for x in row)
               for phase,row in rows if phase!='forall_terminal_delta')
    # Independently exhaust all leaf truth sets and auxiliary assignments of
    # the 3-witness/4-deletion lattice on five vertices, with its root true.
    leaves = list(subsets(5,3));nodes = list(subsets(5,4))+[31]
    projection_cases = 0
    for leafbits in range(1<<len(leaves)):
        truth = dict(zip(leaves,((leafbits>>i)&1 for i in range(len(leaves)))))
        can_assert_root = False
        for bits in range(1<<(len(nodes)-1)):
            values = {**truth,31:1}
            values.update((s,(bits>>i)&1) for i,s in enumerate(nodes[:-1]))
            valid = all(not values[s] or any(values[s^(1<<i)] for i in verts(s)[:4]) for s in nodes)
            if valid:
                can_assert_root = True
                break
        assert can_assert_root == bool(leafbits)
        projection_cases += 1
    return {'mutated_exact_flags_rejected':dict(rejected),
            'genuine_internal_witnesses_allowed_false':changed,
            'bad_lattice_exhaustive_leaf_projection_cases':projection_cases}


def regeneration():
    records = []
    for n,m in ((7,11),(7,12),(8,13)):
        same = {}
        for suffix in ('','.map'):
            own = SCRATCH/f'm{m}n{n}/input.cnf{suffix}'
            parent = ROOT/f'terminal{n}-a/m{m}/input.cnf{suffix}'
            same[suffix or 'cnf'] = sha(own)
            assert sha(own)==sha(parent)
        records.append({'m':m,'n':n,'identical_sha256':same})
    return {'cases':records,'source_sha256':sha(EXT/'terminal_general.cpp'),
            'compact_sha256':sha(COMPACT),'binary_sha256':sha(BIN)}


def terminal18_facts():
    f = next(x for x in frozen() if x['name']=='terminal18')
    g = Geometry(f['P'],7)
    target_cups = [s for s in g.targets if all(g.sign[mask(t)] for t in combinations(verts(s),3))]
    cups5 = [s for s in subsets(18,5) if all(g.sign[mask(t)] for t in combinations(verts(s),3))]
    assert not target_cups and cups5 and not g.good
    assert g.caps4 and not g.cap5 and g.targets and not g.ngons
    return {'m':18,'n':7,'maximum_cap':4,'maximum_cup':5,'maximum_convex_subset':6,
            'six_cups':len(target_cups),'five_cups':len(cups5),
            'first_five_cup':verts(cups5[0]),'terminal_deltas':len(g.good),
            'consequence':'Forbidding an (n-1)-cup does not restore all-size terminal-safe selection.'}


def small_sat():
    case = ROOT/'small-delta/n7m11k2'
    cnf, log = case/'input.cnf', case/'solve/cadical.log'
    model = {}
    for line in log.read_text().splitlines():
        if line.startswith('v '):
            for v in map(int,line.split()[1:]):
                if v:
                    assert abs(v) not in model or model[abs(v)]==(v>0)
                    model[abs(v)]=v>0
    nv = int(cnf.open().readline().split()[2])
    assert set(model)==set(range(1,nv+1))
    checked = 0
    for phase,row in clauses(cnf):
        assert any(model[abs(v)]==(v>0) for v in row)
        checked += 1
    # Recover every semantic witness from orientation signs alone.
    m,n = 11,7
    signs = {s:model[i] for i,s in enumerate(subsets(m,3),1)}
    convex4 = []
    cap4 = []
    for s in subsets(m,4):
        p = [signs[mask(t)] for t in combinations(verts(s),3)]
        assert sum(p[i]!=p[i+1] for i in range(3))<=1
        if p[0]==p[1] and p[2]==p[3]:
            convex4.append(s)
        if not any(p):
            cap4.append(s)
    assert not any(all(not signs[mask(t)] for t in combinations(verts(s),3)) for s in subsets(m,5))
    nonconvex = upclosure(m,set(subsets(m,4))-set(convex4))
    assert all(nonconvex[s] for s in subsets(m,n))
    ends = {verts(s)[-2:] for s in cap4}
    bad = [s for s in signs if not signs[s] and verts(s)[-2:] not in ends]
    target = [s for s in subsets(m,n-1) if not nonconvex[s]]
    D,T = upclosure(m,bad),upclosure(m,target)
    good = [s for s in range(1<<m) if not D[s] and not T[((1<<m)-1)^s]]
    sizes = Counter(s.bit_count() for s in good)
    assert good and min(sizes)>2
    return {'status':'COMPUTED abstract SAT model checked','m':m,'n':n,'k':2,
            'clauses_checked':checked,'assigned_variables':nv,
            'terminal_deltas_by_size':dict(sorted(sizes.items())),
            'minimum_terminal_size':min(sizes),'first_delta':verts(good[0]),
            'real_realizability':'NOT CHECKED','cnf_sha256':sha(cnf),'model_log_sha256':sha(log)}


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    parser = argparse.ArgumentParser()
    parser.add_argument('mode',choices=['filters','domain','mutants','regeneration','terminal18_facts','small_sat'])
    parser.add_argument('--receipt',required=True)
    a = parser.parse_args()
    start = time.monotonic()
    out = {'label':'COMPUTED','mode':a.mode,'status':'IN_PROGRESS',
           'script_sha256':sha(__file__),'own_helper_sha256':sha(Path(__file__).with_name('check.py'))}
    try:
        result = globals()[a.mode]()
        out.update(status='PASS',result=result)
    except BaseException:
        out.update(status='FAIL',error=traceback.format_exc())
        raise
    finally:
        out.update(seconds=time.monotonic()-start,max_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        with (DATA/a.receipt).open('x') as f:
            json.dump(out,f,indent=2);f.write('\n')
        print(json.dumps({k:out[k] for k in ('mode','status','seconds','max_rss_KiB')}))


if __name__=='__main__':
    main()
