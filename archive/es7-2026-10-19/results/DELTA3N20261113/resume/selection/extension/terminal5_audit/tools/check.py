#!/usr/bin/env python3
"""New n5 instance audit, reusing the accepted independent checker read-only.

The n5 pure geometry base is separately rebuilt here. No parent producer or
solver is imported or run. No frozen output path is used by this wrapper.
"""
import collections
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import resource
import sys

E = Path(__file__).resolve().parents[2]
R = E/'terminal5_audit'
W = Path('/home/jay/research/data/delta3-codex-20261113/extension')
S = W/'terminal5-audit'
OLD = E/'audit/check.py'
BLOCKS = [(0,0),(1,-1),(2,-3),(3,-6),(10,500),(11,600),(12,699),(13,797)]

def sha(path):
    h=hashlib.sha256()
    a=path.stat()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1 << 20),b''):
            h.update(block)
    b=path.stat()
    assert (a.st_ino,a.st_size,a.st_mtime_ns)==(b.st_ino,b.st_size,b.st_mtime_ns)
    return h.hexdigest()

def save(path,obj):
    with path.open('x') as f:
        json.dump(obj,f,indent=2)
        f.write('\n')

def load_independent():
    spec=importlib.util.spec_from_file_location('accepted_independent_terminal_audit',OLD)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def clause(row):
    return (' '.join(map(str,(*row,0)))+'\n').encode()

def base9(lib,path,mapfile):
    # n5 requires only exact convex4 flags; no larger-convex recurrence exists.
    entries=[]
    for kind,size in [('orientation',3),('convex',4)]:
        entries.extend((kind,lib.mask(t)) for t in it.combinations(range(9),size))
    ids={(kind,s):v for v,(kind,s) in enumerate(entries,1)}
    mapbytes=b'# id kind mask; indices are zero based in increasing x order\n'+b''.join(
        f'{v} {kind} {s}\n'.encode() for v,(kind,s) in enumerate(entries,1))
    assert mapbytes==mapfile.read_bytes()
    out=S/'base9-rebuilt.map'
    with out.open('xb') as f:f.write(mapbytes)
    triples=lambda t:[ids['orientation',lib.mask(q)] for q in it.combinations(t,3)]
    phases=collections.OrderedDict((p,[]) for p in
        ('signotope','no5cap','convex4_equivalence','convex_larger_equivalence','no_ngon','fixed_signs'))
    for t in it.combinations(range(9),4):
        vs=triples(t)
        for a,b,c in it.combinations(vs,3):
            phases['signotope'].extend([(-a,b,-c),(a,-b,c)])
    for t in it.combinations(range(9),5):
        phases['no5cap'].append(tuple(ids['orientation',lib.mask(t[j:j+3])] for j in range(3)))
    for t in it.combinations(range(9),4):
        a,b,c,d=triples(t)
        z=ids['convex',lib.mask(t)]
        phases['convex4_equivalence'].extend([
            (-z,-a,b),(-z,a,-b),(-z,-c,d),(-z,c,-d),
            (z,a,d),(z,-a,-d),(z,b,-c),(z,-b,c)])
    for t in it.combinations(range(9),5):
        # Each deletion gives a four-subset; express the five children directly.
        phases['no_ngon'].append(tuple(-ids['convex',lib.mask(set(t)-{v})] for v in t))
    count=sum(map(len,phases.values()))
    rebuilt=S/'base9-rebuilt.cnf'
    with path.open('rb') as original,rebuilt.open('xb') as out:
        header=(f'p cnf {len(entries)} {count}'.ljust(95)+'\n').encode()
        assert original.readline()==header
        out.write(header)
        for name,rows in phases.items():
            comment=f'c phase {name}\n'.encode()
            assert original.readline()==comment
            out.write(comment)
            for row in rows:
                expected=clause(row)
                assert original.readline()==expected,(name,row)
                out.write(expected)
        assert not original.read(1)
    assert sha(rebuilt)==sha(path)
    return {'m':9,'n':5,'variables':len(entries),'clauses':count,
            'literals':sum(len(row) for rows in phases.values() for row in rows),
            'phases':{p:len(rows) for p,rows in phases.items()},
            'pure_geometry_only':True,'map_and_body_byte_identical':True,
            'rebuilt_sha256':sha(rebuilt)}

def terminal(lib,m):
    path=W/f'n5m{m}-terminal.cnf'
    report=lib.check_formula(path,m,5)
    G=lib.Geometry(BLOCKS[:m],5)
    assert not G.cap5 and not G.ngons and G.good
    control=lib.check_formula(path,m,5,geometry=G)
    # The inherited checker's hull calculation is cross-checked by a new
    # triangle-containment implementation on every four-subset of this P.
    convex4=[]
    for t in it.combinations(range(m),4):
        inside=False
        for v in t:
            a,b,c=[x for x in t if x!=v]
            turns=[lib.det(G.P,a,b,v),lib.det(G.P,b,c,v),lib.det(G.P,c,a,v)]
            inside |= all(x>0 for x in turns) or all(x<0 for x in turns)
        assert inside==bool(G.nonconvex[lib.mask(t)])
        if not inside:convex4.append(lib.mask(t))
    invalid_shortcut=None
    if m==7:
        A=lib.mask((0,1,2,4))
        assert not G.cap_inside[A] and not G.target_inside[G.full^A] and G.bad_inside[A]
        invalid_shortcut={'P':G.P,'A':[0,1,2,4],'no_fourcap':True,
            'hits_all_targets':True,'blue_size':3,'terminal_safe':False,
            'unprotected_triple':[0,1,2],
            'reason':'No ambient four-cap can end at pair(1,2), which has fewer than two earlier vertices.'}
    return {'formula':report,'real_control':G.report(),'canonical_rows':control,
            'four_subset_triangle_checks':len(list(it.combinations(range(m),4))),
            'withdrawn_m7_shortcut_counterexample':invalid_shortcut}

def main():
    resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
    (R/'data').mkdir(exist_ok=True)
    S.mkdir(exist_ok=True)
    lib=load_independent()
    compact=E.parents[1]/'compact/compact_cnf.cpp'
    source=E/'terminal_general.cpp'
    inputs=[Path(__file__),OLD,source,compact,E/'audit/VERIFY_EXTENSION.md']
    for m,tag in [(7,'terminal5m7-a'),(8,'terminal5m8-a'),(9,'base5m9-a')]:
        kind='base' if m==9 else 'terminal'
        p=W/f'n5m{m}-{kind}.cnf'
        inputs += [p,Path(str(p)+'.map'),W/tag/'input.cnf',W/tag/'result.json']
    before={str(p):sha(p) for p in inputs}
    save(R/'data/formula-inputs-before.json',before)
    assert sha(source)==sha(E/'audit/source/selection/extension/terminal_general.cpp')
    assert sha(compact)==sha(E/'audit/source/compact/compact_cnf.cpp')
    cases={}
    for m,tag in [(7,'terminal5m7-a'),(8,'terminal5m8-a'),(9,'base5m9-a')]:
        kind='base' if m==9 else 'terminal'
        path=W/f'n5m{m}-{kind}.cnf'
        assert sha(path)==sha(W/tag/'input.cnf'),'solver input differs from mapped input'
        parent=json.loads((W/tag/'result.json').read_text())
        assert parent['hashes']['input.cnf']==sha(path)
        assert parent['finished'] and parent['status']=='UNSAT_CERTIFIED'
        result=base9(lib,path,Path(str(path)+'.map')) if m==9 else terminal(lib,m)
        result['original_cnf_sha256']=sha(path)
        result['map_sha256']=sha(Path(str(path)+'.map'))
        result['solver_input_byte_identical']=path.read_bytes()==(W/tag/'input.cnf').read_bytes()
        assert result['solver_input_byte_identical']
        save(R/'data'/f'formula-m{m}.json',result)
        cases[str(m)]=result
    after={str(p):sha(p) for p in inputs}
    save(R/'data/formula-inputs-after.json',after)
    assert before==after
    out={'status':'PASS','label':'COMPUTED','cases':cases,
         'read_only_reused_checker':{'path':str(OLD),'sha256':sha(OLD)},
         'source_hashes':{str(p):sha(p) for p in (source,compact)},
         'all_inputs_stable':True,'prior_records_written':False,
         'resource_limits':{'AS_MiB':300,'CPUs':1,'wall_seconds':20,'CPU_seconds':19},
         'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    save(R/'data/formula-result.json',out)
    print(json.dumps({'status':'PASS','cases':list(cases),'peak_rss_KiB':out['peak_rss_KiB']}))

if __name__=='__main__':
    main()
