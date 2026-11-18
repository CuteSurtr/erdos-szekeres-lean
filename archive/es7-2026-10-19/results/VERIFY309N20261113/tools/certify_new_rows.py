"""Fresh independent encodings and LRAT checks for the 272 additional row certificates.
The 349 identical CNFs already checked in VERIFY_N66 are explicitly inherited.
Full proof hints select a sub-CNF; only a fresh cake_lpr-accepted subproof is evidence.
"""
import collections, gzip, hashlib, json, pathlib, shutil, subprocess, time
from rows66 import D
from coupled66_independent import Model,clause,line
ROOT=pathlib.Path(__file__).resolve().parents[5]
V=pathlib.Path('/home/jay/research/data/verify309-codex-20261113/rows'); V.mkdir(parents=True,exist_ok=True)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
old=ROOT/'cloud/es7-2026-10-19/results/N66N20261113/data/cert59'
prior=[('tmpl',json.loads(l)) for l in gzip.open(old/'template_certs11.jsonl.gz','rt')]+[('core',json.loads(l)) for l in (old/'core_certs11.jsonl').open()]
size=lambda x:len(x[1]['core'] if x[0]=='tmpl' else x[1]['support'])
prior.sort(key=size)
P=pathlib.Path('/home/jay/research/data/verify-N66-20261113')
covered=set()
for i,l in enumerate((P/'recert.jsonl').open()):
    x=json.loads(l); kind,r=prior[i]
    assert (x['kind'],x['id'],x['n'])==(kind,r.get('id'),size(prior[i]))
    if x['ALL_OK']: covered.add(i)
for l in (P/'recert_sub.jsonl').open():
    x=json.loads(l); i=x['idx']; kind,r=prior[i]
    assert x['ALL_OK'] and (x['kind'],x['id'],x['n'])==(kind,r.get('id'),size(prior[i]))
    covered.add(i)
assert len(covered)==349==len(prior)
inherited={prior[i][1]['cnf_sha256'] for i in covered}
items=[('tmpl',json.loads(l)) for l in (D/'tcert/template_certs.jsonl').open()]+[('core',json.loads(l)) for l in (D/'tcert/core_certs.jsonl').open()]
items.sort(key=size)
out=V/'certificates.jsonl'; done={json.loads(l)['full_sha256'] for l in out.open()} if out.exists() else set()
static={}
for kind,r in items:
    h=r['cnf_sha256']
    if h in done: continue
    rec={'kind':kind,'id':r.get('id'),'support':r.get('support'),'n':size((kind,r)),'full_sha256':h}
    if h in inherited:
        rec.update(result='INHERITED independently verified identical CNF',evidence='N66N20261113/VERIFY_N66.md')
    else:
        t=time.time(); n=rec['n']; full='octs' not in r; model=Model(n); key=(n,full)
        if key not in static:
            body=V/f'static_{n}_{int(full)}.body'; nc=0
            with body.open('wb') as f:
                for lits in model.static(full):
                    c=clause(lits)
                    if c is not None: f.write(line(c)); nc+=1
            static[key]=(body,nc)
            print(json.dumps({'static':key,'clauses':nc,'sha256':sha(body)}),flush=True)
        body,nc=static[key]; extra=[]
        if 'octs' in r:
            for q in r['octs']:
                assert len(q)==len(set(q))==8 and all(0<=i<n for i in q)
                extra.append(clause(model.oct(q)))
        support=r['core'] if kind=='tmpl' else r['support']
        keep={tuple(t) for t in r['tests']} if kind=='tmpl' else None
        for lits,tag in model.dynamic(support):
            if keep is None or tag in keep:
                c=clause(lits)
                if c is not None: extra.append(c)
        cnf=V/'current.cnf'; proof=V/'current.lrat'
        with cnf.open('wb') as f:
            f.write(f'p cnf {model.nv} {nc+len(extra)}\n'.encode())
            with body.open('rb') as g: shutil.copyfileobj(g,f,1<<20)
            for c in extra: f.write(line(c))
        assert sha(cnf)==h,('independent encoder hash differs',kind,rec['id'],n,sha(cnf),h)
        with (V/'current.cadical.log').open('w') as f:
            rc=subprocess.run(['/usr/bin/cadical','-q','--lrat=true','--binary=false',str(cnf),str(proof)],stdout=f,stderr=subprocess.STDOUT).returncode
        assert rc==20,(rec,rc)
        # Superset of all original clauses cited in the proof, not a trusted proof checker.
        used=set(); m=nc+len(extra)
        with proof.open() as f:
            for l in f:
                q=l.split()
                if len(q)<2 or q[1]=='d': continue
                z=q.index('0',1)
                used.update(abs(int(v)) for v in q[z+1:-1] if 0<abs(int(v))<=m)
        sub=V/(h+'.cnf'); spr=V/(h+'.lrat')
        with cnf.open('rb') as f,sub.open('wb') as g:
            next(f); g.write(f'p cnf {model.nv} {len(used)}\n'.encode()); count=0
            for i,l in enumerate(f,1):
                if i in used: g.write(l); count+=1
        assert count==len(used)
        with (V/(h+'.cadical.log')).open('w') as f:
            rc=subprocess.run(['/usr/bin/cadical','-q','--lrat=true','--binary=false',str(sub),str(spr)],stdout=f,stderr=subprocess.STDOUT).returncode
        assert rc==20
        cake=V/(h+'.cake.log')
        with cake.open('w') as f:
            subprocess.run(['/home/jay/.local/bin/cake_lpr','--CML_HEAP_SIZE=700','--CML_STACK_SIZE=100',str(sub),str(spr)],stdout=f,stderr=subprocess.STDOUT)
        assert 's VERIFIED UNSAT' in cake.read_text().splitlines(),(rec,cake.read_text()[-500:])
        rec.update(result='CERTIFIED',sub_clauses=count,sub_sha256=sha(sub),lrat_sha256=sha(spr),seconds=round(time.time()-t,2))
    with out.open('a') as f: f.write(json.dumps(rec)+'\n')
    done.add(h); print(json.dumps(rec),flush=True)
assert len(done)==len({r['cnf_sha256'] for _,r in items})
print(json.dumps({'result':'ALL ROW CERTIFICATES COVERED','records':len(items),'distinct_cnfs':len(done)}),flush=True)
