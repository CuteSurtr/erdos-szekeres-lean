#!/usr/bin/env python3
"""Independent audit of the m13/n7 reverse-containment augmentation.

No parent or prior checker is imported. The full geometric base is inherited;
only its map, containment interface and preserved bytes are reconstructed.
"""
import collections
import datetime
import hashlib
import itertools
import json
import math
from pathlib import Path
import resource
import sys

ROOT = Path('/home/jay/research/lean/erdos-szekeres-lean')
SELECTION = ROOT / 'cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection'
RECORD = SELECTION / 'extension/exact_audit'
DATA = RECORD / 'data'
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/extension/exact-audit')
EXT = SCRATCH.parent
BASE = EXT / 'terminal7-a/m13/input.cnf'
MAP = Path(str(BASE) + '.map')
AUG = EXT / 'n7m13-exact.cnf'
SOURCE = SELECTION / 'extension/augment_exact.py'
M, N = 13, 7

def require(ok, text):
    if not ok:
        raise ValueError(text)

def sha(path):
    h = hashlib.sha256()
    before = path.stat()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    after = path.stat()
    require((before.st_size, before.st_mtime_ns, before.st_ino) ==
            (after.st_size, after.st_mtime_ns, after.st_ino), 'unstable_hash_input')
    return dict(sha256=h.hexdigest(), bytes=after.st_size, mtime_ns=after.st_mtime_ns)

def save(name, obj):
    with (DATA / name).open('x') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')

def bits(s):
    return tuple(i for i in range(s.bit_length()) if s & (1 << i))

def mask(vertices):
    return sum(1 << i for i in vertices)

def subsets(s, k):
    return (mask(v) for v in itertools.combinations(bits(s), k))

def expected_map(m=M, n=N):
    universe = (1 << m)-1
    order = []
    for k, kind in [(3, 'orientation'), *[(k, 'convex') for k in range(4,n)],
                    (4, 'terminal_fourcap'), (3, 'terminal_bad_triple')]:
        order.extend((kind, s) for s in subsets(universe, k))
    order.extend(('bad_contains', s) for s in range(1 << m) if 4 <= s.bit_count() <= m-n+2)
    order.extend(('target_contains', s) for s in range(1 << m) if s.bit_count() >= n)
    return [(i, kind, s) for i, (kind, s) in enumerate(order, 1)]

def read_map(path):
    rows = []
    for line in path.open():
        if line.startswith('#'):
            continue
        v, kind, s = line.split()
        rows.append((int(v),kind,int(s)))
    return rows

def verify_map(rows, expected):
    require(len(rows)==len(expected), 'map_length')
    for position,(got,want) in enumerate(zip(rows,expected),1):
        require(got==want, f'map_row_{position}: {got} != {want}')
    require(len({(kind,s) for _,kind,s in rows})==len(rows), 'map_duplicate_key')

def families(mapping, n=N):
    ids = {(kind,s):v for v,kind,s in mapping}
    parents = []
    forward = collections.defaultdict(list)
    reverse = []
    for p, kind, s in mapping:
        if kind not in ('bad_contains','target_contains'):
            continue
        leaf_size, leaf_kind = (3,'terminal_bad_triple') if kind=='bad_contains' else (n-1,'convex')
        deleted = bits(s)[:leaf_size+1]
        require(len(deleted)==leaf_size+1, 'short_parent')
        children = []
        child_masks = []
        for v in deleted:
            child_set = s - (1 << v)
            child_kind = leaf_kind if child_set.bit_count()==leaf_size else kind
            c = ids[child_kind,child_set]
            require(0<c<p, 'not_acyclic')
            require(child_set != s and child_set & s == child_set, 'not_proper_subset')
            children.append(c)
            child_masks.append(child_set)
            reverse.append((-c,p))
        phase = 'bad_triple_containment' if kind=='bad_contains' else 'target_containment'
        forward[phase].append(tuple([-p,*children]))
        parents.append(dict(id=p,kind=kind,mask=s,children=children,child_masks=child_masks,
                            deleted=deleted,leaf_size=leaf_size))
    return ids, parents, dict(forward), reverse

def cnf(path):
    phase = None
    rows = []
    header = None
    with path.open() as f:
        for lineno,line in enumerate(f,1):
            words = line.split()
            require(bool(words), f'blank_cnf_line_{lineno}')
            if words[0]=='p':
                require(header is None and lineno==1 and len(words)==4 and words[1]=='cnf','bad_header')
                header = (int(words[2]),int(words[3]))
            elif words[0]=='c':
                require(len(words)==3 and words[1]=='phase','unexpected_comment')
                phase = words[2]
            else:
                require(header is not None and phase is not None, 'missing_header_or_phase')
                row = tuple(map(int,words))
                require(row[-1]==0 and all(x and abs(x)<=header[0] for x in row[:-1]),'bad_clause')
                rows.append((phase,row[:-1]))
    require(header and len(rows)==header[1], 'header_clause_count')
    return header, rows

def verify_reverse(got, expected):
    require(len(got)==len(expected), 'reverse_count')
    for i,(a,b) in enumerate(zip(got,expected),1):
        require(a==b, f'reverse_row_{i}: {a} != {b}')

def truth(clause, values):
    return any(values[abs(v)] == (v>0) for v in clause)

def load():
    mapping = read_map(MAP)
    verify_map(mapping, expected_map())
    ids,parents,forward,reverse = families(mapping)
    base_header,base_rows = cnf(BASE)
    aug_header,aug_rows = cnf(AUG)
    require(base_header[0]==len(mapping)==aug_header[0], 'variable_count')
    require(aug_rows[:len(base_rows)]==base_rows,'old_clause_semantics_changed')
    added = aug_rows[len(base_rows):]
    require(all(phase=='reverse_containment_implications' for phase,_ in added),'extra_phase')
    verify_reverse([row for _,row in added], reverse)
    for phase,rows in forward.items():
        require([row for p,row in base_rows if p==phase]==rows,'old_forward_interface_'+phase)
    full=(1<<M)-1
    failure=[]
    for s in range(1<<M):
        if s.bit_count()>M-N+2:
            continue
        r=[]
        if s.bit_count()>=3:
            r.append(ids['terminal_bad_triple' if s.bit_count()==3 else 'bad_contains',s])
        t=full^s
        if t.bit_count()>=N-1:
            r.append(ids['convex' if t.bit_count()==N-1 else 'target_contains',t])
        failure.append(tuple(r))
    require([row for phase,row in base_rows if phase=='forall_terminal_delta']==failure,'failure_interface')
    internal={p['id'] for p in parents}
    for phase,row in base_rows:
        if phase not in forward and phase!='forall_terminal_delta':
            require(all(abs(v) not in internal for v in row),'internal_flag_used_elsewhere')
    require(not any(phase=='fixed_signs' for phase,_ in base_rows),'fixed_sign_units')
    return mapping,parents,reverse,base_header,base_rows,aug_header

def structure():
    inputs=[SOURCE,BASE,MAP,AUG,Path(str(AUG)+'.json'),BASE.parent/'encode.json',
            SELECTION/'extension/audit/VERIFY_EXTENSION.md',
            SELECTION/'extension/terminal_general.cpp',
            SELECTION/'../compact/compact_cnf.cpp',RECORD/'tools/check_exact.py']
    before={str(p):sha(p) for p in inputs}
    save('inputs-before.json',before)
    mapping,parents,reverse,base_header,base_rows,aug_header=load()
    with BASE.open('rb') as f:
        f.readline()
        old_body=f.read()
    with AUG.open('rb') as f:
        f.readline()
        require(f.read(len(old_body))==old_body,'old_body_bytes_changed')
        tail=f.read()
    expected_tail=b'c phase reverse_containment_implications\n'+b''.join(
        f'{c} {p} 0\n'.encode() for c,p in reverse)
    require(tail==expected_tail,'tail_bytes_mismatch')
    rebuilt=SCRATCH/'independently-rebuilt.cnf'
    with rebuilt.open('xb') as f:
        f.write(f'p cnf {len(mapping)} {len(base_rows)+len(reverse)}\n'.encode())
        f.write(old_body)
        f.write(expected_tail)
    require(sha(rebuilt)['sha256']==sha(AUG)['sha256'],'full_rebuilt_hash_mismatch')
    rebuilt_map=SCRATCH/'independently-rebuilt.map'
    with rebuilt_map.open('x') as f:
        f.write('# id kind mask; indices are zero based in increasing x order\n')
        for v,kind,s in mapping:
            f.write(f'{v} {kind} {s}\n')
    require(sha(rebuilt_map)['sha256']==sha(MAP)['sha256'],'map_byte_mismatch')
    coverage=collections.Counter()
    for p in parents:
        for w in subsets(p['mask'],p['leaf_size']):
            require(any((w&child)==w for child in p['child_masks']),'witness_cover')
            coverage[p['kind']]+=1
    receipt=json.loads(Path(str(AUG)+'.json').read_text())
    require(receipt['n']==N and receipt['variables']==len(mapping),'receipt_parameters')
    require(receipt['old_clauses']==len(base_rows) and receipt['added_clauses']==len(reverse)
            and receipt['clauses']==aug_header[1],'receipt_counts')
    for key,path in [('base',BASE),('map',MAP),('output',AUG),('augmenter',SOURCE)]:
        require(receipt['hashes'][key]==before[str(path)]['sha256'],'receipt_hash_'+key)
    after={str(p):sha(p) for p in inputs}
    save('inputs-after.json',after)
    require(before==after,'inputs_changed')
    summary=dict(status='PASS',label='COMPUTED',m=M,n=N,variables=len(mapping),
        map_counts=dict(collections.Counter(kind for _,kind,_ in mapping)),
        map_counts_by_size={kind:{str(k):sum(1 for _,kind2,s in mapping if kind2==kind and s.bit_count()==k)
                                for k in range(M+1) if any(kind2==kind and s.bit_count()==k for _,kind2,s in mapping)}
                            for kind in sorted({kind for _,kind,_ in mapping})},
        old_clauses=len(base_rows),added_clauses=len(reverse),total_clauses=aug_header[1],
        added_by_family={kind:sum(len(p['children']) for p in parents if p['kind']==kind)
                         for kind in ('bad_contains','target_contains')},
        old_body_bytes=len(old_body),old_body_sha256=hashlib.sha256(old_body).hexdigest(),
        old_body_byte_identical=True,independent_rebuild_byte_identical=True,map_byte_identical=True,
        forward_interface_rows=sum(1 for phase,_ in base_rows if phase in ('bad_triple_containment','target_containment')),
        failure_interface_rows=sum(1 for phase,_ in base_rows if phase=='forall_terminal_delta'),
        internal_flags_have_no_other_uses=True,fixed_sign_units=0,witness_cover_checks=dict(coverage),
        duplicate_added_rows=len(reverse)-len(set(reverse)),new_variables=0,extra_geometric_clauses=0,
        elapsed_limit_seconds=20,as_mib=300,source_review='VERIFY_EXACT.md',certificate_replayed=False)
    save('structure.json',summary)
    print(json.dumps(summary))

def exact_geometry(points):
    m=len(points); full=(1<<m)-1
    require(all(points[i][0]<points[i+1][0] for i in range(m-1)),'fixture_x_order')
    def det(i,j,k):
        a,b,c=points[i],points[j],points[k]
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    orient={s:det(*bits(s)) for s in subsets(full,3)}
    require(all(orient.values()),'fixture_collinear')
    def cap(s): return all(orient[t]<0 for t in subsets(s,3))
    nonconvex=set()
    for s in subsets(full,4):
        for q in bits(s):
            a,b,c=bits(s^(1<<q))
            turns=[det(a,b,q),det(b,c,q),det(c,a,q)]
            if all(t>0 for t in turns) or all(t<0 for t in turns):
                nonconvex.add(s); break
    def convex(s): return all(t not in nonconvex for t in subsets(s,4))
    c4={s for s in subsets(full,4) if cap(s)}
    bad=set()
    for s,d in orient.items():
        if d>0: continue
        a,b,c=bits(s)
        if not any(mask((u,v,b,c)) in c4 for u,v in itertools.combinations(range(b),2)):
            bad.add(s)
    hexagons={s for s in subsets(full,6) if convex(s)}
    def contains_table(seeds):
        table=bytearray(1<<m)
        for s in seeds: table[s]=1
        for b in range(m):
            for s in range(1<<m):
                if s&(1<<b): table[s]|=table[s^(1<<b)]
        return table
    D,T=contains_table(bad),contains_table(hexagons)
    require(not any(cap(s) for s in subsets(full,5)),'fixture_five_cap')
    require(not any(convex(s) for s in subsets(full,7)),'fixture_heptagon')
    return orient,convex,c4,bad,hexagons,D,T

def expect_rejection(name, action, prefix, payload):
    try:
        action()
    except ValueError as e:
        require(str(e).startswith(prefix),'wrong_negative_rejection')
        return dict(name=name,status='REJECTED_AS_EXPECTED',message=str(e),mutation=payload)
    raise ValueError('negative_control_accepted_'+name)

def lattice_control(m, k, patterns):
    # Fixed arbitrary leaf truths: compare every internal assignment, then
    # check that exact repair only changes false internals to true.
    full=(1<<m)-1
    leaves=list(subsets(full,k))
    internals=[s for s in range(1<<m) if s.bit_count()>k]
    where={s:i for i,s in enumerate(leaves+internals)}
    relations=[]
    for s in internals:
        p=where[s]; children=[where[s^(1<<v)] for v in bits(s)[:k+1]]
        relations.append((p,sum(1<<c for c in children)))
    old_total=new_total=checked=0
    for leaf_truth in patterns:
        canonical=leaf_truth
        for p,cs in relations:
            if canonical&cs: canonical|=1<<p
        matching=0
        for internal_truth in range(1<<len(internals)):
            v=leaf_truth|(internal_truth<<len(leaves));checked+=1
            if any(v&(1<<p) and not(v&cs) for p,cs in relations): continue
            old_total+=1
            require(v & ~canonical == 0,'repair_removes_a_true_flag')
            if any(v&cs and not(v&(1<<p)) for p,cs in relations): continue
            require(v==canonical,'noncanonical_exact_model')
            new_total+=1;matching+=1
        require(matching==1,'not_unique_exact_extension')
    return dict(m=m,witness_size=k,patterns=len(patterns),internal_flags=len(internals),
                assignments_checked=checked,old_models=old_total,exact_models=new_total,
                canonical_repair_preserves_all_true_flags=True)

def controls():
    mapping,parents,reverse,base_header,base_rows,aug_header=load()
    frozen=SELECTION/'extension/subset_audit/data/ambient.points'
    w=list(map(int,frozen.read_text().split()))
    require(w[:2]==[23,7] and len(w)==48,'frozen_ambient_format')
    points=list(zip(w[2::2],w[3::2]))
    fixtures=[]
    for name,ix in [('first13',list(range(13))),('last13',list(range(10,23)))]:
        p=[points[i] for i in ix]
        orient,convex,c4,bad,hexagons,D,T=exact_geometry(p)
        values=[False]*(len(mapping)+1)
        for v,kind,s in mapping:
            values[v]=bool({'orientation':lambda:orient[s]>0,'convex':lambda:convex(s),
                'terminal_fourcap':lambda:s in c4,'terminal_bad_triple':lambda:s in bad,
                'bad_contains':lambda:D[s],'target_contains':lambda:T[s]}[kind]())
        false_base=collections.Counter(phase for phase,row in base_rows if not truth(row,values))
        require(set(false_base)<= {'forall_terminal_delta'},'canonical_nonpool_failure')
        require(all(truth(row,values) for row in reverse),'canonical_reverse_failure')
        all_false=values.copy()
        for parent in parents: all_false[parent['id']]=False
        require(all(truth(row,all_false) for phase,row in base_rows
                    if phase in ('bad_triple_containment','target_containment')),'one_way_control')
        rejected=sum(not truth(row,all_false) for row in reverse)
        require(rejected>0,'reverse_not_exercised')
        fixtures.append(dict(name=name,source_indices=ix,points=p,integer_GP=True,five_caps=0,
            heptagons=0,four_caps=len(c4),bad_triples=len(bad),hexagons=len(hexagons),
            added_rows_satisfied=len(reverse),all_nonfailure_base_rows_satisfied=True,
            false_failure_rows=false_base.get('forall_terminal_delta',0),
            false_internal_local_one_way_model_rejected_by_reverse_rows=rejected))
    mutations=[]
    for name,mutant in [('omit',reverse[:-1]),('duplicate',reverse+[reverse[0]]),
                        ('wrong_polarity',[(abs(reverse[0][0]),reverse[0][1]),*reverse[1:]]),
                        ('wrong_direction',[(reverse[0][1]*-1,-reverse[0][0]),*reverse[1:]]),
                        ('wrong_parent',[(reverse[0][0],reverse[0][1]+1),*reverse[1:]])]:
        mutations.append(expect_rejection(name,lambda v=mutant:verify_reverse(v,reverse),'reverse_',
            dict(length=len(mutant),first_row=mutant[0],last_row=mutant[-1])))
    wrong_map=mapping.copy(); a=wrong_map[5005];wrong_map[5005]=(a[0],a[1],a[2]+1)
    mutations.append(expect_rejection('wrong_map_mask',lambda:verify_map(wrong_map,expected_map()),
                     'map_row_',dict(row=5006,replacement=wrong_map[5005])))
    short_covers=[]
    for k in (3,6):
        s=(1<<(k+1))-1; chosen=bits(s)[:k]; witness=mask(chosen)
        require(not any(witness & (s^(1<<v)) == witness for v in chosen),'short_cover_not_detected')
        short_covers.append(dict(witness_size=k,parent=s,deleted=list(chosen),uncovered_witness=witness))
    # Exhaustive bad-triple leaf assignments on five points, including
    # every possible internal assignment (65,536 cases).
    small=lattice_control(5,3,list(range(1<<math.comb(5,3))))
    # Real n7 target width: all singleton/complement leaves and 32 fixed patterns.
    width=math.comb(8,6); top=(1<<width)-1
    patterns=sorted({0,top,*[1<<i for i in range(width)],*[top^(1<<i) for i in range(width)],
                     *[(i*2654435761)&top for i in range(32)]})
    target=lattice_control(8,6,patterns)
    result=dict(status='PASS',label='COMPUTED',real_fixtures=fixtures,
        negative_mutations=mutations,deliberately_short_covers=short_covers,
        exhaustive_bad_lattice=small,target_lattice=target,
        distinction='Local one-way assignments can be cut; exact canonical repair preserves the projection.',
        no_m15_audit=True,no_full_base_reconstruction=True)
    save('controls.json',result)
    print(json.dumps(dict(status='PASS',real_fixtures=len(fixtures),added_rows_tested=len(fixtures)*len(reverse),
        negative_mutations=len(mutations),lattice_assignments=small['assignments_checked']+target['assignments_checked'])))

if __name__=='__main__':
    resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20))
    require(len(sys.argv)==2 and sys.argv[1] in ('structure','controls'),'mode_required')
    try:
        globals()[sys.argv[1]]()
    except BaseException as e:
        save('failure-'+sys.argv[1]+'.json',dict(status='FAIL',error=repr(e),
             when=datetime.datetime.now(datetime.timezone.utc).isoformat()))
        raise
