#!/usr/bin/env python3
"""Independent fixed n6 geometry/membership audit and generic10/11 rows."""
import collections
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import resource

E=Path(__file__).resolve().parents[2]
R=E/'terminal12_audit'
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
S=W/'terminal12-audit'

def sha(p):
    h=hashlib.sha256();a=p.stat()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1 << 20),b''):h.update(block)
    b=p.stat()
    assert (a.st_ino,a.st_size,a.st_mtime_ns)==(b.st_ino,b.st_size,b.st_mtime_ns)
    return h.hexdigest()

def save(p,v):
    with p.open('x') as f:json.dump(v,f,indent=2);f.write('\n')

def mask(vs):return sum(1 << v for v in vs)
def verts(s):return tuple(v for v in range(s.bit_length()) if s & (1 << v))

def up(m,seeds):
    a=bytearray(1 << m)
    for s in seeds:a[s]=1
    for v in range(m):
        bit=1 << v
        for base in range(0,1 << m,2*bit):
            for j in range(bit):a[base+bit+j]|=a[base+j]
    return a

class Geometry:
    def __init__(self,P,n):
        assert n==6
        self.P,self.n,self.m=P,n,len(P)
        self.full=(1 << self.m)-1
        assert all(type(v) is int for p in P for v in p)
        assert all(P[i][0]<P[i+1][0] for i in range(self.m-1))
        self.detvalues={mask(t):self.det(*t) for t in it.combinations(range(self.m),3)}
        assert all(self.detvalues.values())
        self.sign={s:d>0 for s,d in self.detvalues.items()}
        self.cap3=[s for s,d in self.detvalues.items() if d<0]
        self.cap4=[mask(t) for t in it.combinations(range(self.m),4) if self.chain(t,-1)]
        ends={verts(s)[-2:] for s in self.cap4}
        self.bad=[s for s in self.cap3 if verts(s)[-2:] not in ends]
        self.cap5=[mask(t) for t in it.combinations(range(self.m),5) if self.chain(t,-1)]
        self.non4=[]
        for t in it.combinations(range(self.m),4):
            inside=False
            for q in t:
                a,b,c=[v for v in t if v!=q]
                ds=[self.det(a,b,q),self.det(b,c,q),self.det(c,a,q)]
                inside |= all(d>0 for d in ds) or all(d<0 for d in ds)
            if inside:self.non4.append(mask(t))
        self.nonconvex=up(self.m,self.non4)
        self.targets=[mask(t) for t in it.combinations(range(self.m),n-1) if not self.nonconvex[mask(t)]]
        self.ngons=[mask(t) for t in it.combinations(range(self.m),n) if not self.nonconvex[mask(t)]]
        self.cap_inside=up(self.m,self.cap4)
        self.bad_inside=up(self.m,self.bad)
        self.target_inside=up(self.m,self.targets)
        self.weak=[s for s in range(self.full+1) if not self.cap_inside[s] and not self.target_inside[self.full^s]]
        self.good=[s for s in self.weak if not self.bad_inside[s]]
        if not self.cap5:
            assert all(self.bad_inside[s] or not self.cap_inside[s] for s in range(self.full+1))

    def det(self,a,b,c):
        x,y=self.P[a];u,v=self.P[b];s,t=self.P[c]
        return (u-x)*(t-y)-(v-y)*(s-x)

    def chain(self,t,sign):return all(sign*self.detvalues[mask(q)]>0 for q in it.combinations(t,3))
    def prepare_values(self):pass
    def value(self,kind,s):
        if kind=='orientation':return self.sign[s]
        if kind=='convex':return not self.nonconvex[s]
        if kind=='terminal_fourcap':return s in self.cap4
        if kind=='terminal_bad_triple':return s in self.bad
        if kind=='bad_contains':return bool(self.bad_inside[s])
        if kind=='target_contains':return bool(self.target_inside[s])
        raise ValueError(kind)

    def report(self):
        maxima=[0,0,0]
        for s in range(1,self.full+1):
            v=verts(s);k=len(v)
            if self.chain(v,-1):maxima[0]=max(maxima[0],k)
            if self.chain(v,1):maxima[1]=max(maxima[1],k)
            if not self.nonconvex[s]:maxima[2]=max(maxima[2],k)
        minimum=min(map(int.bit_count,self.weak)) if self.weak else None
        return {'m':self.m,'n':self.n,'P':self.P,'general_position':True,'maxima_cap_cup_gon':maxima,
                'minimum_absolute_determinant':min(abs(d) for d in self.detvalues.values()),
                'maximum_absolute_determinant':max(abs(d) for d in self.detvalues.values()),
                'fourcaps':len(self.cap4),'bad_triples':len(self.bad),'targets':len(self.targets),
                'fivecaps':len(self.cap5),'ngons':len(self.ngons),'assignments':self.full+1,
                'ordinary_weak_deltas':len(self.weak),'terminal_deltas':len(self.good),
                'minimum_weak_size':minimum,
                'weak_by_size':dict(sorted(collections.Counter(s.bit_count() for s in self.weak).items())),
                'terminal_by_size':dict(sorted(collections.Counter(s.bit_count() for s in self.good).items())),
                'first_minimum_weak':list(verts(next(s for s in self.weak if s.bit_count()==minimum))) if self.weak else None,
                'first_terminal':list(verts(self.good[0])) if self.good else None}

def parse_points(path):
    rows=[tuple(map(int,line.split())) for line in path.read_text().splitlines()]
    assert rows[0]==(12,6) and len(rows)==13 and all(len(t)==2 for t in rows)
    return rows[1:]

def fixed_case(case,original):
    directory=W/'descend15-a'/str(case)
    P=parse_points(directory/'points.txt')
    expected=json.loads((directory/'result.json').read_text())
    indices=[i for i in range(15) if i not in expected['removed_original_indices']]
    assert indices==expected['local_to_original']
    assert [tuple(original[i]) for i in indices]==P
    G=Geometry(P,6)
    assert not G.cap5 and not G.ngons
    rows=[tuple(-v-1 for v in verts(s)) for s in G.cap4+G.bad]
    rows.extend(tuple(v+1 for v in verts(s)) for s in G.targets)
    body=f'p cnf 12 {len(rows)}\n'.encode()+b''.join((' '.join(map(str,(*r,0)))+'\n').encode() for r in rows)
    cnf=directory/'terminal.cnf'
    assert cnf.read_bytes()==body
    rebuilt=S/f'case{case}-terminal.cnf'
    with rebuilt.open('xb') as f:f.write(body)
    sat=0
    for a in range(1 << 12):
        clause_sat=all(any(bool(a & (1 << (abs(v)-1)))==(v>0) for v in row) for row in rows)
        geometric=not G.cap_inside[a] and not G.bad_inside[a] and not G.target_inside[G.full^a]
        assert clause_sat==geometric
        sat+=clause_sat
    report=G.report()
    assert report['ordinary_weak_deltas']==expected['weak_delta_count']
    assert report['terminal_deltas']==expected['terminal_delta_count']==sat
    assert report['maxima_cap_cup_gon']==expected['maxima_cap_cup_gon']
    assert len(G.cap4)==expected['fourcaps'] and len(G.bad)==expected['bad_triples']
    assert len(G.targets)==expected['pentagons'] and report['minimum_weak_size']==expected['minimum_weak_size']
    report.update(status='PASS',label='COMPUTED',local_to_original=indices,
                  clauses=len(rows),membership_byte_identical=True,membership_truth_checks=4096,
                  cnf_sha256=sha(cnf),parent_result_sha256=sha(directory/'result.json'),
                  fourcap_masks=G.cap4,bad_triple_masks=G.bad,target_masks=G.targets)
    if case==3:
        assert report['ordinary_weak_deltas']==945 and not G.good and report['minimum_weak_size']==4
        assert (directory/'certificate/input.cnf').read_bytes()==body
        assert sha(cnf)=='25ca75a9eee359ca03ae7f96657128ab03693c03421b1e7e83627f529841890a'
        # Earlier independent C++ is a comparison only, never executed/imported.
        parsed=[tuple(map(int,line.split()[:-1])) for line in
                (directory/'independent.terminal.cnf').read_text().splitlines() if not line.startswith(('p','c'))]
        canonical=lambda rr:tuple(sorted(rr))
        assert collections.Counter(map(canonical,parsed))==collections.Counter(map(canonical,rows))
        report['old_cpp_clause_multiset_agrees']=True
    save(R/'data'/f'fixed-case{case}.json',report)
    return report

def main():
    resource.setrlimit(resource.RLIMIT_AS,(300 << 20,300 << 20))
    S.mkdir(exist_ok=True);(R/'data').mkdir(exist_ok=True)
    boundary=E.parent/'boundary/audit'
    inputs=[Path(__file__),E/'audit/check.py',E/'terminal_general.cpp',
            E.parents[1]/'compact/compact_cnf.cpp',E/'terminal15/data/balanced.json',
            boundary/'VERIFY_BOUNDARY.md',boundary/'data/replay-n6.json',boundary/'data/replay-n6.log']
    for case in range(4):
        inputs.extend(W/'descend15-a'/str(case)/name for name in ('points.txt','result.json','terminal.cnf'))
    for m in (10,11):inputs.extend([W/f'n6m{m}-terminal.cnf',W/f'n6m{m}-terminal.cnf.map',W/f'terminal6m{m}-a/input.cnf'])
    before={str(p):sha(p) for p in inputs};save(R/'data/inputs-before.json',before)
    original=json.loads((E/'terminal15/data/balanced.json').read_text())['P']
    fixed={str(case):fixed_case(case,original) for case in range(4)}
    spec=importlib.util.spec_from_file_location('accepted_generic_terminal_audit',E/'audit/check.py')
    lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib)
    assert sha(E/'terminal_general.cpp')==sha(E/'audit/source/selection/extension/terminal_general.cpp')
    assert sha(E.parents[1]/'compact/compact_cnf.cpp')==sha(E/'audit/source/compact/compact_cnf.cpp')
    generic={}
    P=fixed['3']['P']
    for m in (10,11):
        path=W/f'n6m{m}-terminal.cnf';cnf=W/f'terminal6m{m}-a/input.cnf'
        assert path.read_bytes()==cnf.read_bytes()
        G=Geometry(P[:m],6)
        assert not G.cap5 and not G.ngons and G.good
        formula=lib.check_formula(path,m,6,G)
        result={'status':'PASS','formula':formula,'real_control':G.report(),
                'cnf_sha256':sha(cnf),'source_mapped_input_identical':True}
        save(R/'data'/f'generic-m{m}.json',result);generic[str(m)]=result
    prior=json.loads((boundary/'data/replay-n6.json').read_text())
    assert prior['label']=='CERTIFIED' and prior['exact_verdict_line'] and prior['stable']
    assert prior['input_hashes_before']==prior['input_hashes_after']
    assert 's VERIFIED UNSAT' in (boundary/'data/replay-n6.log').read_text().splitlines()
    assert sha(boundary/'data/replay-n6.log')==prior['log_sha256']
    after={str(p):sha(p) for p in inputs};save(R/'data/inputs-after.json',after);assert before==after
    result={'status':'PASS','label':'COMPUTED formula and exact geometry/membership audits',
            'fixed':fixed,'generic':generic,'through9':{'audit':str(boundary/'VERIFY_BOUNDARY.md'),
                'scope':'Every n6 admissible real set of size at most9; written smaller-size dichotomy plus boundary certificate.',
                'replay_receipt':prior,'fresh_replay_here':False},
            'limits':{'AS_MiB':300,'CPUs':1,'wall_seconds':20,'CPU_seconds':19},
            'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    save(R/'data/check-result.json',result)
    print(json.dumps({'status':'PASS','fixed_terminal_counts':[fixed[str(i)]['terminal_deltas'] for i in range(4)],
                      'fixed3_weak':fixed['3']['ordinary_weak_deltas'],'generic':[10,11],
                      'peak_rss_KiB':result['peak_rss_KiB']}))

if __name__=='__main__':main()
