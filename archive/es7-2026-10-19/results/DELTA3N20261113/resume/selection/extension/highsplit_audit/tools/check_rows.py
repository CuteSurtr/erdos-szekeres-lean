#!/usr/bin/env python3
"""Independent streaming m14 map, containment, and high-split row audit.

Only Python's standard library is used. No producer or earlier checker is
imported or executed. The accepted generic geometry is an explicit dependency.
"""
import collections
import hashlib
import itertools as it
import json
from pathlib import Path
import resource
import sys

ROOT = Path('/home/jay/research/lean/erdos-szekeres-lean')
E = ROOT / 'cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension'
REC = E / 'highsplit_audit'
W = Path('/home/jay/research/data/delta3-codex-20261113/extension')
RUN = sys.argv[1] if len(sys.argv)>1 else 'rows-run02'
need_run_name = RUN.replace('-','').isalnum()
if not need_run_name:
    raise ValueError('invalid run directory name')
DATA = REC / 'data' / RUN
WORK = W / 'highsplit-audit' / RUN
BASE = W / 'terminal7-a/m14/input.cnf'
MAP = Path(str(BASE)+'.map')
EXACT = W / 'n7m14-exact.cnf'
CUT = W / 'n7m14-indecomp.cnf'
V2 = W / 'n7m14-indecomp-v2.cnf'
M, N = 14, 7

def need(ok, message):
    if not ok:
        raise ValueError(message)

def dump(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')

def sha(path):
    a = path.stat()
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    b = path.stat()
    need((a.st_ino,a.st_size,a.st_mtime_ns)==(b.st_ino,b.st_size,b.st_mtime_ns),
         'file changed during hash: '+str(path))
    return {'sha256':h.hexdigest(), 'bytes':b.st_size, 'mtime_ns':b.st_mtime_ns}

def mask(vertices):
    return sum(1 << v for v in vertices)

def vertices(s):
    return [v for v in range(s.bit_length()) if (s >> v)&1]

def clause(row):
    return (' '.join(map(str, row))+' 0\n').encode()

def mapping():
    result = []
    for k, kind in [(3,'orientation'), (4,'convex'), (5,'convex'), (6,'convex'),
                    (4,'terminal_fourcap'), (3,'terminal_bad_triple')]:
        result.extend((kind,mask(t)) for t in it.combinations(range(M),k))
    result.extend(('bad_contains',s) for s in range(1 << M) if 4<=s.bit_count()<=M-N+2)
    result.extend(('target_contains',s) for s in range(1 << M) if s.bit_count()>=N)
    return [(v,kind,s) for v,(kind,s) in enumerate(result,1)]

def children(kind,s,ids):
    k,leaf = (3,'terminal_bad_triple') if kind=='bad_contains' else (N-1,'convex')
    result = []
    for x in vertices(s)[:k+1]:
        child = s ^ (1 << x)
        result.append(ids[leaf if child.bit_count()==k else kind,child])
    need(len(result)==k+1 and len(set(result))==k+1, 'child coverage cardinality')
    return result

def forward(kind,rows,ids):
    for v,tag,s in rows:
        if tag==kind:
            yield (-v,*children(kind,s,ids))

def failure_rows(ids):
    for s in range(1 << M):
        if s.bit_count()>M-N+2:
            continue
        row = []
        if s.bit_count()>=3:
            row.append(ids['terminal_bad_triple' if s.bit_count()==3 else 'bad_contains',s])
        blue = ((1 << M)-1)^s
        if blue.bit_count()>=N-1:
            row.append(ids['convex' if blue.bit_count()==N-1 else 'target_contains',blue])
        yield tuple(row)

def reverse_rows(rows,ids):
    for p,kind,s in rows:
        if kind in ('bad_contains','target_contains'):
            for c in children(kind,s,ids):
                need(0<c<p,'containment ordering')
                yield (-c,p)

def cut_rows(orientations,m):
    # Count vertices on the left, independently of producer endpoint inequalities.
    for k in range(1,m):
        row = []
        for v,t in orientations:
            left = len(set(t) & set(range(k)))
            if left==2:
                row.append(-v)
            elif left==1:
                row.append(v)
        yield tuple(row)

def row_truth(row,values):
    return any(values[abs(v)]==(v>0) for v in row)

def split_truth(orientations,values,k):
    left, right = set(range(k)), set(range(k,1+max(max(t) for _,t in orientations)))
    for v,t in orientations:
        if len(left.intersection(t))==2 and len(right.intersection(t))==1 and not values[v]:
            return False
        if len(left.intersection(t))==1 and len(right.intersection(t))==2 and values[v]:
            return False
    return True

def logical_controls(orientations,cuts):
    total = {'mixed_single_flip':0,'pure_single_flip':0,'small_exhaustive':0,
             'canonical_split':0,'containment_leaf_covers':0}
    mutations = []
    for k,row in enumerate(cuts,1):
        assignment = {v:len(set(t)&set(range(k)))==2 for v,t in orientations}
        need(split_truth(orientations,assignment,k) and not row_truth(row,assignment),'canonical split')
        total['canonical_split']+=1
        mixed = {abs(v) for v in row}
        for v,_ in orientations:
            assignment[v] = not assignment[v]
            need(row_truth(row,assignment)==(v in mixed), 'single flip clause')
            need(split_truth(orientations,assignment,k)==(v not in mixed),'single flip predicate')
            total['mixed_single_flip' if v in mixed else 'pure_single_flip']+=1
            assignment[v] = not assignment[v]
        wrongsign = (-row[0],)+row[1:]
        need(row_truth(wrongsign,assignment), 'sign mutation escaped')
        missing = row[1:]
        changed = dict(assignment)
        changed[abs(row[0])] = not changed[abs(row[0])]
        need(row_truth(row,changed) and not row_truth(missing,changed),'omission mutation escaped')
        mutations.append({'cut':k,'flipped_literal':row[0], 'wrong_sign_accepts_highsplit':True,
                          'omission_rejects_one_violation':True,
                          'duplicate_rejected_by_exact_row_comparison':row+(row[0],)!=row})
    for m in (4,5):
        ori = list(enumerate(it.combinations(range(m),3),1))
        rows = list(cut_rows(ori,m))
        for bits in range(1 << len(ori)):
            a = {v:bool(bits & (1 << (v-1))) for v,_ in ori}
            for k,row in enumerate(rows,1):
                need(row_truth(row,a)==(not split_truth(ori,a,k)),'exhaustive split equivalence')
                total['small_exhaustive']+=1
    # All possible relative witness positions, independently of actual variable IDs.
    for k,maximum in ((3,M-N+2),(N-1,M)):
        for size in range(k+1,maximum+1):
            subchildren = [set(range(size))-{v} for v in range(k+1)]
            for witness in it.combinations(range(size),k):
                need(any(set(witness)<=child for child in subchildren),'leaf cover counterexample')
                total['containment_leaf_covers']+=1
    return total, mutations

def main():
    resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
    DATA.mkdir(exist_ok=False)
    WORK.mkdir(exist_ok=False)
    inputs = [BASE,MAP,EXACT,CUT,V2,E/'augment_exact.py',E/'augment_indecomposable.py',
              *(Path(str(p)+'.json') for p in (EXACT,CUT,V2)),
              E/'structure2/highsplit_reduction.md',E/'structure2/separated_theorem.md',
              E/'audit/VERIFY_EXTENSION.md',E/'exact_audit/VERIFY_EXACT.md',
              E/'exact_audit/replay13/data/result.json',Path(__file__)]
    before = {str(p):sha(p) for p in inputs}
    dump(DATA/'rows-inputs-before.json',before)
    rows = mapping()
    ids = {(kind,s):v for v,kind,s in rows}
    need(len(ids)==len(rows)==32086,'variable map uniqueness/count')
    rebuilt_map = WORK/'m14-independent.map'
    with MAP.open('rb') as source, rebuilt_map.open('xb') as out:
        header = b'# id kind mask; indices are zero based in increasing x order\n'
        need(source.readline()==header,'map header')
        out.write(header)
        for v,kind,s in rows:
            line = f'{v} {kind} {s}\n'.encode()
            need(source.readline()==line,f'map entry {v}')
            out.write(line)
        need(not source.read(1),'extra map rows')
    internal = {v for v,kind,_ in rows if kind in ('bad_contains','target_contains')}
    expected = {'bad_triple_containment':iter(forward('bad_contains',rows,ids)),
                'target_containment':iter(forward('target_contains',rows,ids)),
                'forall_terminal_delta':iter(failure_rows(ids))}
    phase_counts = collections.Counter()
    reverse_count = sum(4 if kind=='bad_contains' else 7 for _,kind,_ in rows if kind in ('bad_contains','target_contains'))
    need(reverse_count==127128,'reverse count')
    rebuilt_exact = WORK/'m14-independent-exact.cnf'
    bodyhash = hashlib.sha256()
    bodybytes = 0
    with BASE.open('rb') as base, EXACT.open('rb') as target, rebuilt_exact.open('xb') as out:
        need(base.readline().split()==[b'p',b'cnf',b'32086',b'104485'],'base header')
        header = b'p cnf 32086 231613\n'
        need(target.readline()==header,'exact header')
        out.write(header)
        phase = None
        for line in base:
            need(target.readline()==line,'old body changed')
            out.write(line)
            bodyhash.update(line)
            bodybytes += len(line)
            words = line.split()
            need(bool(words),'blank line in base')
            if words[0]==b'c':
                need(len(words)==3 and words[1]==b'phase','unknown base comment')
                phase = words[2].decode()
                continue
            rr = tuple(map(int,words))
            need(rr[-1]==0 and all(0<abs(x)<=len(rows) for x in rr[:-1]),'malformed base row')
            rr = rr[:-1]
            need(phase is not None,'missing phase')
            phase_counts[phase]+=1
            if phase in expected:
                need(next(expected[phase],None)==rr,'base interface row '+phase)
            else:
                need(not any(abs(v) in internal for v in rr),'containment variable escapes interface')
        need(sum(phase_counts.values())==104485,'base row count')
        need(phase_counts['fixed_signs']==0,'unexpected fixed-sign premise')
        for phase,gen in expected.items():
            need(next(gen,None) is None,'missing interface row '+phase)
        marker = b'c phase reverse_containment_implications\n'
        need(target.readline()==marker,'exact marker')
        out.write(marker)
        seen = 0
        for rr in reverse_rows(rows,ids):
            line = clause(rr)
            need(target.readline()==line,f'reverse row {seen+1}')
            out.write(line)
            seen+=1
        need(seen==reverse_count and not target.read(1),'extra/missing exact rows')
    orientations = [(v,tuple(vertices(s))) for v,kind,s in rows if kind=='orientation']
    cuts = list(cut_rows(orientations,M))
    lengths = [len(rr) for rr in cuts]
    need(lengths==[78,144,198,240,270,288,294,288,270,240,198,144,78],'cut row lengths')
    need(sum(lengths)==2730,'cut literal count')
    for k,row in enumerate(cuts,1):
        need(len(row)==len({abs(v) for v in row})==k*(M-k)*(M-2)//2,'cut duplicates/count')
    rebuilt_cut = WORK/'m14-independent-indecomp.cnf'
    with EXACT.open('rb') as base, CUT.open('rb') as target, V2.open('rb') as v2, rebuilt_cut.open('xb') as out:
        need(base.readline()==b'p cnf 32086 231613\n','exact header repeat')
        header = b'p cnf 32086 231626\n'
        need(target.readline()==v2.readline()==header,'cut headers')
        out.write(header)
        for line in base:
            need(target.readline()==v2.readline()==line,'exact prefix or v2 changed')
            out.write(line)
        marker = b'c conditional minimal-counterexample high-split exclusions\n'
        need(target.readline()==v2.readline()==marker,'cut marker')
        out.write(marker)
        for k,row in enumerate(cuts,1):
            line = clause(row)
            need(target.readline()==v2.readline()==line,f'cut row {k}')
            out.write(line)
        need(not target.read(1) and not v2.read(1),'extra conditional rows')
    for rebuilt,original in [(rebuilt_map,MAP),(rebuilt_exact,EXACT),(rebuilt_cut,CUT)]:
        need(sha(rebuilt)['sha256']==before[str(original)]['sha256'],'rebuilt full hash')
    receipts = {p.name:json.loads(Path(str(p)+'.json').read_text()) for p in (EXACT,CUT,V2)}
    for p in (EXACT,CUT,V2):
        receipt = receipts[p.name]
        need(receipt['variables']==len(rows),'receipt variables')
        need(receipt['hashes']['output']==before[str(p)]['sha256'],'receipt output')
        need(receipt['hashes']['map']==before[str(MAP)]['sha256'],'receipt map')
        need(receipt['hashes']['base']==before[str(BASE if p==EXACT else EXACT)]['sha256'],'receipt base')
        need(receipt['added_clauses']==(127128 if p==EXACT else 13),'receipt added')
        need(receipt['clauses']==(231613 if p==EXACT else 231626),'receipt total')
        need(receipt['old_clauses' if p==EXACT else 'base_clauses']==(104485 if p==EXACT else 231613),'receipt old')
    need(receipts[EXACT.name]['hashes']['augmenter']==before[str(E/'augment_exact.py')]['sha256'],'exact source receipt')
    need(receipts[V2.name]['hashes']['augmenter']==before[str(E/'augment_indecomposable.py')]['sha256'],'v2 source receipt')
    need(receipts[CUT.name]['hashes']['augmenter']!=receipts[V2.name]['hashes']['augmenter'],'expected source version change')
    for p in (CUT,V2):
        need(receipts[p.name]['m']==M and receipts[p.name]['n']==N,'conditional parameters')
        need(receipts[p.name]['cuts']==[{'cut':k,'literals':len(row)} for k,row in enumerate(cuts,1)],'cut receipt counts')
    controls,mutations = logical_controls(orientations,cuts)
    dump(DATA/'row-mutation-controls.json',mutations)
    after = {str(p):sha(p) for p in inputs}
    dump(DATA/'rows-inputs-after.json',after)
    need(before==after,'inputs changed across check')
    result = {'status':'PASS','label':'COMPUTED','m':M,'n':N,'variables':len(rows),
        'map_counts':dict(collections.Counter(kind for _,kind,_ in rows)),
        'base_phase_counts':dict(phase_counts),'base_clauses':104485,
        'reverse_clauses':127128,'reverse_by_family':{'bad_contains':57772,'target_contains':69356},
        'exact_clauses':231613,'cut_clauses':13,'cut_literals':sum(lengths),
        'cut_lengths':lengths,'conditional_clauses':231626,
        'old_body_bytes':bodybytes,'old_body_sha256':bodyhash.hexdigest(),
        'byte_identical_rebuilt_map':True,'byte_identical_rebuilt_exact':True,
        'byte_identical_rebuilt_conditional':True,'v1_v2_formula_byte_identical':True,
        'controls':controls,'source_version_note':'Current conditional producer matches v2 receipt; older receipt names another producer hash. Older producer bytes not independently recovered. Formula bytes independently rebuilt and equal in both versions.',
        'dependencies':'Geometry base audit; exact canonical projection proof; high-split real-geometry proof; exact size13 terminal-safe existence for cut13; accepted conditional CNF proof required for m14 existence.',
        'resource_limits':{'address_space_MiB':300,'cpu_seconds':19,'wall_seconds':20,'cpu_count':1},
        'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    dump(DATA/'rows-result.json',result)
    print(json.dumps(result))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        failure = {'status':'FAIL','type':type(exc).__name__,'message':str(exc)}
        failure_path = DATA/'rows-failure.json'
        if not failure_path.exists():
            dump(failure_path,failure)
        print(json.dumps(failure),file=sys.stderr)
        raise
