"""Freeze the tested n7 witness and exact controls into this track only."""
from fractions import Fraction as Q
import hashlib
import itertools as it
import json
from pathlib import Path
import shutil
from check import verify,cap,convex,cross

HERE=Path(__file__).resolve().parent;DATA=HERE/'data';DATA.mkdir(exist_ok=True)
WORK=Path('/home/jay/research/data/delta3-codex-20261113/selection/terminal')
pre=WORK/'minimum-s0-final'
minimum=json.loads(Path(str(pre)+'.minimize.json').read_text());indices=minimum['indices']
source=json.loads((WORK/'hept-0075-n7.input.json').read_text())
g=json.loads(Path(str(pre)+'.geometry.json').read_text());p=minimum['P'];m=len(p);n=7
audit=verify(pre,colors=True)
envelope=json.loads(Path(str(pre)+'.envelope.json').read_text())
core=json.loads(Path(str(pre)+'.core.json').read_text())
assert audit['terminal_count']==0 and envelope['all_X_strictly_right']['count']==4057
fullclauses={tuple([-i-1 for i in t]) for t in g['fourcaps']+g['rank3_triples']}
fullclauses|={tuple([i+1 for i in t]) for t in g['polygons']}
clauses=[tuple(q['clause']) for q in core['candidate_core']]
assert set(clauses)<=fullclauses
neg=[sum(1<<(-l-1) for l in c) for c in clauses if c[0]<0]
pos=[sum(1<<(l-1) for l in c) for c in clauses if c[0]>0]
core_count=sum(all(a&z!=z for z in neg) and all(a&z for z in pos) for a in range(1<<m))
assert core_count==0
deletions=[]
for removed in indices:
    expected=[i for i in indices if i!=removed]
    h=next(h for h in minimum['history'] if h['indices']==expected)
    assert h['result']['terminal']['outcome']=='SAT'
    check=verify(WORK/h['stem'],colors=False)
    deletions.append(dict(removed_final_index=indices.index(removed),removed_source_index=removed,
                         terminal_A=h['result']['terminal']['A'],audit=check))

# A direct two-line proof of all-X dominance, independently of envelope construction.
A=audit['minimum_weak_A'];Aset=set(A);cap4=[6,7,14,17]
assert cap(p,cap4)
def line(a,b):
    slope=Q(p[b][1]-p[a][1],p[b][0]-p[a][0]);return slope,Q(p[a][1])-slope*p[a][0]
ambient=line(*cap4[-2:]);X=p[-1][0]
triples=[t for t in it.combinations(A,3) if cap(p,t)]
proof=[]
for t in triples:
    l=line(*t[-2:]);margin=(ambient[0]-l[0])*X+ambient[1]-l[1];slope_margin=ambient[0]-l[0]
    assert margin>0 and slope_margin>0
    proof.append(dict(triple=t,terminal_pair=t[-2:],slope_margin=str(slope_margin),margin_at_xmax=str(margin)))
assert not any(cap(p,t) for t in it.combinations(A,4))
assert all(set(t)&Aset for t in g['polygons'])
direct=dict(A=A,ambient_cap=cap4,ambient_terminal_pair=cap4[-2:],xmax=X,triples=proof,
            claim='For every X>xmax, every three-cap terminal line in A is strictly below this ambient four-cap terminal line, hence below F4(U;X).')

controls=[]
for stem in ['parent16-n7','star12-n7','restr_ends_weak_a5_n7_m12_real-n7',
             'target8-n8','restr_ends_weak_a5_n8_m13_real-n8']:
    controls.append(verify(WORK/stem,colors=True))

for suffix in ['points','geometry.json','terminal.cnf','weak.cnf','result.json','terminal.finder.log','weak.finder.log','core.cnf','envelope.json']:
    shutil.copyfile(Path(str(pre)+'.'+suffix),DATA/('witness.'+suffix))
packet=dict(label='COMPUTED',certificate_status='PENDING_PARENT_FRESH_LRAT_AND_CAKE',n=n,m=m,P=p,
            source=source,source_indices=indices,ordinary_weak_Delta=A,all_X_envelope_Delta=A,
            full_coloring_variables=m,full_coloring_clauses=len(g['fourcaps'])+len(g['rank3_triples'])+len(g['polygons']),
            core_variables=m,core_clauses=len(clauses),core_negative_rank3=len(neg),core_positive_polygons=len(pos),
            required_certificate='Fresh CaDiCaL LRAT plus cake_lpr s VERIFIED UNSAT for witness.core.cnf (or the full witness.terminal.cnf); independent coordinate/clause audit.',
            limitations=['Single-point-deletion irreducible, not globally smallest.',
                         'Terminal rank restriction fails; the weaker envelope condition holds for all rightward X.',
                         'No weak-Delta counterexample and no rooted-extension counterexample.'])
def put(name,value):(DATA/name).write_text(json.dumps(value,indent=2)+'\n')
put('witness.json',packet);put('exact_check.json',audit);put('deletion_controls.json',deletions)
put('positive_controls.json',controls);put('all_X_direct_proof.json',direct)
put('core.json',dict(label='COMPUTED',status='UNSAT_UNCERTIFIED',clauses=core['candidate_core'],
                     exhaustive_satisfying_assignments=core_count,all_assignments=1<<m,
                     complete_single_clause_deletion_pass=core['complete_single_clause_deletion_pass'],
                     source_trajectory=str(pre)+'.core.json',core_sha256=core['core_sha256']))
summary=[]
for path in sorted(WORK.glob('*.result.json')):
    if any(q in path.name for q in ('trial','minimum')):continue
    r=json.loads(path.read_text());summary.append(r)
put('probe_results.json',summary)
print(json.dumps(dict(m=m,n=n,full_clauses=packet['full_coloring_clauses'],core_clauses=len(clauses),
                     core_negative=len(neg),core_positive=len(pos),weak_Delta=A,
                     deletion_controls=len(deletions),positive_controls=len(controls),packet=str(DATA/'witness.json'))))
