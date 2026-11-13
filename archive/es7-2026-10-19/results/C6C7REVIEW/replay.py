#!/usr/bin/env python3
"""Regenerate formulas, verify covers, and replay a preselected proof sample.

Usage: python3 -I replay.py --scratch DIR --archives DIR --archive DIR --bin DIR
The first archive root contains the historical C6/C7 archives. The second is a
fresh durable destination. No solver is invoked. Checkers run sequentially.
"""
import argparse, hashlib, json, os, pathlib, random, re, secrets, subprocess, sys, time

P = pathlib.Path
p = argparse.ArgumentParser()
p.add_argument('--resume', action='store_true')
p.add_argument('--seed', type=int, help='repeat the recorded random sample')
for arg in ('scratch', 'archives', 'archive', 'bin'):
    p.add_argument('--' + arg, required=True, type=P)
a = p.parse_args()
here = P(__file__).resolve().parent
results = here.parent
scratch = a.scratch.resolve(); scratch.mkdir(parents=True, exist_ok=True)
logs = here / 'logs'; logs.mkdir(exist_ok=True)
archive = a.archive.resolve(); archive.mkdir(parents=True, exist_ok=True)
ledger = {'rigor': 'exact computation; certificate only for successfully replayed proofs',
          'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
          'commands': [], 'files': [], 'proofs': [], 'memory_samples_gb': []}
if a.resume:
    ledger = json.loads((here / 'replay.json').read_text())
def save():
    text = json.dumps(ledger, indent=2).replace(sys.executable, '$PYTHON')
    (here / 'replay.json').write_text(text + '\n')
def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(8 << 20), b''): h.update(b)
    return h.hexdigest()
def clean(s):
    for path, tag in sorted([(str(results), '$RESULTS'), (str(scratch), '$SCRATCH'),
          (str(a.archives), '$ARCHIVES'), (str(archive), '$ARCHIVE'), (str(a.bin), '$BIN'),
          (sys.executable, '$PYTHON')],
          key=lambda x: -len(x[0])):
        s = s.replace(path, tag)
    return s
def memory():
    s = subprocess.check_output(['vm_stat'], text=True)
    size = int(re.search(r'page size of (\d+) bytes', s)[1])
    vals = dict((k, int(v)) for k, v in re.findall(r'^([^:\n]+):\s+(\d+)', s, re.M))
    return size * sum(vals[k] for k in ('Pages active', 'Pages wired down', 'Pages occupied by compressor')) / 1e9
def run(cmd, name, timeout=1200, stdout_file=None):
    print(name, flush=True)
    start = time.monotonic()
    raw = scratch / (name + '.rawlog')
    with open(raw, 'wb') as f:
        proc = subprocess.Popen([str(x) for x in cmd], stdout=stdout_file or f, stderr=f)
        try:
            while proc.poll() is None:
                mem = memory(); ledger['memory_samples_gb'].append(round(mem, 3))
                if mem > 30.0: raise RuntimeError('total memory exceeds 30 GB')
                if time.monotonic() - start > timeout: raise TimeoutError(name)
                time.sleep(2)
        finally:
            if proc.poll() is None:
                proc.terminate()
                try: proc.wait(timeout=10)
                except subprocess.TimeoutExpired: proc.kill(); proc.wait()
    text = clean(raw.read_text(errors='replace'))
    (logs / (name + '.log')).write_text(text)
    record = {'name': name, 'argv': [clean(str(x)) for x in cmd],
              'exit': proc.returncode, 'seconds': round(time.monotonic()-start, 3)}
    ledger['commands'].append(record); save(); raw.unlink()
    if proc.returncode != 0: raise RuntimeError(record)
    return text
def checked(path, expected, label):
    actual = sha(path)
    assert actual == expected, (label, actual, expected)
    ledger['files'].append({'file':label,'sha256':actual,'expected_match':True,'bytes':path.stat().st_size}); save()
def persist(path, label):
    dest = archive / (label + '.zst'); dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['zstd', '-q', '-1', '-T1', '-f', str(path), '-o', str(dest)], check=True)
    h = hashlib.sha256()
    proc = subprocess.Popen(['zstd', '-q', '-dc', str(dest)], stdout=subprocess.PIPE)
    for b in iter(lambda: proc.stdout.read(8 << 20), b''): h.update(b)
    assert proc.wait() == 0 and h.hexdigest() == sha(path)
    rec={'file': label, 'raw_sha256':h.hexdigest(),'zst_sha256':sha(dest),'roundtrip':True}
    with open(archive / 'manifest.jsonl', 'a') as f: f.write(json.dumps(rec)+'\n')

try:
    ledger['binaries'] = {x: sha(a.bin/x) for x in ('cadical','lrat-check','cake_lpr')}
    ledger['sources'] = {x:sha(results/x) for x in ('C7UPPER/gen.py','C7UPPER/gen_b.py',
       'C6UPPER/encb/gen_b2.py','C6UPPER/tools/mkcubes.py','C6UPPER/tools/verify_cover.py')}
    seed = secrets.randbits(64) if a.seed is None else a.seed
    rng = random.Random(seed)
    meaningful = ['c00000','c00001','c01001','c01011','c10000','c10100','c11000','c11001','c11011','c11100','c11110','c11111']
    if 'sampling' not in ledger:
        ledger['sampling'] = {'seed':seed,'method':'three uniformly selected without replacement from the 12 transitive phase-order cubes, independently for each encoder; selected before checking',
                             'A':rng.sample(meaningful,3),'B':rng.sample(meaningful,3)}
    save()
    cases=[('A6','C7UPPER/gen.py',6,11,'542c8a3a2c4484a7d60b5fdb8efc0f3506d782031fc4b4625604b360211ad51e'),
       ('B6','C6UPPER/encb/gen_b2.py',6,11,'479e31a9e8d58d752c86b9abf02fb799c10615a7e61a88f132c49734674f37fc'),
       ('A7','C7UPPER/gen.py',7,10,'1a7c0e706f2a7fb52b109ae20ca37d49c74940e01c1227fe152b46d742d5997f'),
       ('B7','C7UPPER/gen_b.py',7,10,'b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2'),
       ('B7extended','C6UPPER/encb/gen_b2.py',7,10,'b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2')]
    for name, generator, m, t, expected in cases:
        cnf=scratch/(name+'.cnf')
        if a.resume:
            checked(cnf,expected,name+'.cnf')
            continue
        run([sys.executable,'-I',results/generator,m,8,t,cnf],'generate_'+name)
        checked(cnf,expected,name+'.cnf'); persist(cnf,name+'.cnf')
        if m == 6:
            meta=P(str(cnf)+'.json')
            if name == 'B6':
                orig=json.loads(P(str(cnf)+'.map.json').read_text())
                meta.write_text(json.dumps({'Y':{f'{i},{j}':v for i,j,v in orig['Y']}}))
            cubes=scratch/(name+'_cubes'); cubes.mkdir(exist_ok=True)
            run([sys.executable,'-I',results/'C6UPPER/tools/mkcubes.py',cnf,meta,cubes],'cubes_'+name)
            run([sys.executable,'-I',results/'C6UPPER/tools/verify_cover.py',cnf,meta,cubes],'cover_'+name)
            for f in sorted(cubes.glob('*.cnf')): persist(f,name+'_cubes/'+f.name)
            persist(meta,name+'.meta.json')
    cnf=scratch/'A7.cnf'; meta=json.loads(P(str(cnf)+'.json').read_text())
    run([sys.executable,'-I',results/'C7UPPER/addunits.py',cnf,scratch/'A7_H1.cnf',meta['H']['1']], 'add_H1')
    checked(scratch/'A7_H1.cnf','fa297b5bd6608d29369fd56f8cab20d6d17ad9d335253352541a42e4c669fc49','A7_H1.cnf')
    persist(scratch/'A7_H1.cnf','A7_H1.cnf')
    jobs=[]
    c6=a.archives/'es8-c6-octagon-2026-11-03'
    for enc, folder, manifest in [('A','lrat',c6/'archived.txt'),('B','lrat_B',c6/'encb/archived_B.txt')]:
        records={}
        for line in manifest.read_text().splitlines():
            parts=line.split()
            if parts and re.fullmatch(r'c[01]{5}', parts[0]):
                records[parts[0]]=dict(x.split('=',1) for x in parts[1:] if '=' in x)
        for cube in ledger['sampling'][enc]:
            rec=records[cube]
            jobs.append((enc+'6_'+cube, scratch/(enc+'6_cubes')/(cube+'.cnf'), c6/folder/(cube+'.lrat.zst'),rec['raw'],rec['zst']))
    c7=a.archives/'es8-c7-octagon-2026-11-03'
    jobs += [('A7',scratch/'A7_H1.cnf',c7/'m7K8t10_H1.lrat.zst','c750a805a7a3dbdb4ba445c16fb75051a9fac623a3ddf93a5d864defe41039b2','4e2db40a6f86b8e1ab2449b8cdd58c6ad9a8be386dc9bfe4b4e976b74fac6dc4'),
             ('B7',scratch/'B7.cnf',c7/'B_full_m7K8t10.lrat.zst','75f9bd350186724a85e949b05315369d88ef887c9953e0048810b67e8172550e','6f41c33887e7f4d2091a826919b4fbe9d92205fe2fec52c904ebee52bfbbb56c')]
    for name,cnf,zst,rawhash,zsthash in jobs:
        if any(x['name'] == name for x in ledger['proofs']): continue
        checked(zst,zsthash,name+'.lrat.zst')
        proof=scratch/(name+'.lrat')
        with open(proof,'wb') as f: run(['zstd','-q','-dc',zst],'decompress_'+name,stdout_file=f)
        checked(proof,rawhash,name+'.lrat')
        out=run([a.bin/'lrat-check',cnf,proof],'lrat_'+name)
        assert 'c VERIFIED' in out
        out=run([a.bin/'cake_lpr','--CML_HEAP_SIZE=4000','--CML_STACK_SIZE=4000',cnf,proof],'cake_'+name)
        assert 's VERIFIED UNSAT' in out
        ledger['proofs'].append({'name':name,'cnf_sha256':sha(cnf),'raw_sha256':rawhash,'zst_sha256':zsthash,'lrat_check':'replayed VERIFIED','cake_lpr':'replayed VERIFIED UNSAT'})
        save(); proof.unlink()
    ledger['complete']=True
finally:
    ledger['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()); save()
