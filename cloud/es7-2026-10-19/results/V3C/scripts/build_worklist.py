#!/usr/bin/env python3
"""Work list for a later acceptance pass of mirror sub-case (ii).

usage: build_worklist.py REPO Z Z0 OUTDIR
  REPO  a clone that has commits Z and Z0
  Z     the commit whose wave results are to be checked
  Z0    the input commit of the earlier pass (V3B: 066eaa9)

At each of Z and Z0, the wave directories are exported with `git archive`, and the manifest is built
exactly as V3B step 2 does it (verify/v3 at bdf319c: v3_jsonl_leaves.py on every results/WAVEk that
exists into jtreek, then v3_manifest.py over the pairs in order).  The work list holds every record
of the manifest at Z whose key (case, json.dumps(lits)) is neither in the manifest at Z0 (those leaves
belong to the earlier pass) nor a VERIFIED leaf record of results/V3T/**/*.jsonl or
results/V3[ABC]/*/out.jsonl at Z.  Records keep the manifest's fields; idx is renumbered 0..n-1.
Writes OUTDIR/M_Z.jsonl, OUTDIR/M_Z0.jsonl, OUTDIR/worklist.jsonl and prints counts and sha256s."""
import glob, hashlib, io, json, os, subprocess, sys, tarfile

REPO, Z, Z0, OUT = sys.argv[1:5]
B = 'cloud/es7-2026-10-19'
os.makedirs(OUT, exist_ok=True)


def git(*a, **k):
    return subprocess.run(['git', '-C', REPO, *a], capture_output=True, check=True, **k).stdout


def exists(commit, path):
    return subprocess.run(['git', '-C', REPO, 'cat-file', '-e', f'{commit}:{path}'], capture_output=True).returncode == 0


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


v3 = os.path.join(OUT, 'v3src')
os.makedirs(v3, exist_ok=True)
for f in ('v3_jsonl_leaves.py', 'v3_manifest.py'):
    open(os.path.join(v3, f), 'wb').write(git('show', f'bdf319c:{B}/verify/v3/{f}'))


def manifest(commit, tag):
    dest = os.path.join(OUT, 'tree_' + tag)
    subprocess.run(['rm', '-rf', dest])
    os.makedirs(dest)
    parts = ['Mii-S', 'WAVE1', 'WAVE2', 'WAVE3', 'WAVE4', 'V3T', 'V3A', 'V3B', 'V3C']
    paths = [f'{B}/results/{p}' for p in parts if exists(commit, f'{B}/results/{p}')]
    tarfile.open(fileobj=io.BytesIO(git('archive', '--format=tar', commit, *paths))).extractall(dest)
    root = os.path.join(dest, B)
    pairs = []
    for k in (1, 2, 3, 4):
        if os.path.isdir(os.path.join(root, f'results/WAVE{k}')):
            r = subprocess.run(['python3', os.path.join(v3, 'v3_jsonl_leaves.py'), root, f'results/WAVE{k}', f'jtree{k}'],
                               capture_output=True, text=True, check=True)
            print(tag, f'WAVE{k}:', r.stdout.strip())
            if os.path.isdir(os.path.join(root, f'jtree{k}')):   # no jtree when the wave has no leaves.jsonl yet
                pairs += [f'results/WAVE{k}', f'jtree{k}']
    M = os.path.join(OUT, f'M_{tag}.jsonl')
    r = subprocess.run(['python3', os.path.join(v3, 'v3_manifest.py'), root, M, os.path.join(OUT, f'C_{tag}.jsonl'), *pairs],
                       capture_output=True, text=True)
    print(tag, 'manifest:', r.stdout.strip()[-300:], r.stderr.strip()[-300:], 'exit', r.returncode)
    print(tag, 'M sha256', sha(M), 'lines', sum(1 for _ in open(M)))
    return root, M


rootZ, MZ = manifest(Z, 'Z')
_, MZ0 = manifest(Z0, 'Z0')
key = lambda r: (r['case'], json.dumps(r['lits']))
old = {key(json.loads(l)) for l in open(MZ0)}
files = sorted(glob.glob(rootZ + '/results/V3T/**/*.jsonl', recursive=True))
for g in ('V3A', 'V3B', 'V3C'):
    files += sorted(glob.glob(rootZ + f'/results/{g}/*/out.jsonl'))
ver = set()
for f in files:
    for l in open(f):
        try:
            o = json.loads(l)
        except ValueError:
            continue
        if o.get('kind') == 'leaf' and o.get('verdict') == 'VERIFIED' and 'lits' in o:
            ver.add((o['case'], json.dumps(o['lits'])))
recs = [json.loads(l) for l in open(MZ)]
new = [r for r in recs if key(r) not in old]
work = [r for r in new if key(r) not in ver]
W = os.path.join(OUT, 'worklist.jsonl')
with open(W, 'w') as f:
    for i, r in enumerate(work):
        r = dict(r)
        r['idx'] = i
        f.write(json.dumps(r) + '\n')
print('verified keys at Z', len(ver), 'from', len(files), 'files')
print('manifest at Z', len(recs), '| not in manifest at Z0', len(new), '| of those without a VERIFIED record', len(work))
print('worklist sha256', sha(W))
