#!/usr/bin/env python3
"""Work list for a later acceptance pass (V3E, ...) of mirror sub-case (ii).

usage: build_worklist_e.py REPO Z OUTDIR [--skip-b SHARDS] [--skip LIST:SHARDS:N ...]

  Z         the commit whose wave results are to be checked (all of results/WAVE1..4 that have leaves)
  --skip-b  V3B shards (of the 16) whose machines are still running: their records of the V3B list
            Mt (066eaa9, sha256 605e39d2...) are left out, since those machines are checking them
  --skip     LIST:SHARDS:N, e.g. results/V3D/worklist.jsonl:3,7:24 -- the records of that work list
            (at Z) with idx mod N in SHARDS are left out, since running machines are checking them
            (repeatable)

The manifest at Z is built exactly as V3B step 2 does it (verify/v3 at bdf319c). The work list is every
record of it whose key (case, json.dumps(lits)) has no VERIFIED leaf record in results/V3T/**/*.jsonl or
results/V3[A-E]/*/out.jsonl at Z, minus the records left out above. idx is renumbered 0..n-1.
Mt is rebuilt from the 066eaa9 manifest and the VERIFIED records at 066eaa9 exactly as V3B step 3 does it,
and its sha256 is checked."""
import argparse, glob, hashlib, io, json, os, subprocess, sys, tarfile

ap = argparse.ArgumentParser()
ap.add_argument('repo'); ap.add_argument('z'); ap.add_argument('out')
ap.add_argument('--skip-b', default='')
ap.add_argument('--skip', action='append', default=[])
a = ap.parse_args()
B = 'cloud/es7-2026-10-19'
MT_SHA = '605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7'
os.makedirs(a.out, exist_ok=True)


def git(*x):
    return subprocess.run(['git', '-C', a.repo, *x], capture_output=True, check=True).stdout


def exists(commit, path):
    return subprocess.run(['git', '-C', a.repo, 'cat-file', '-e', f'{commit}:{path}'], capture_output=True).returncode == 0


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


v3 = os.path.join(a.out, 'v3src')
os.makedirs(v3, exist_ok=True)
for f in ('v3_jsonl_leaves.py', 'v3_manifest.py'):
    open(os.path.join(v3, f), 'wb').write(git('show', f'bdf319c:{B}/verify/v3/{f}'))


def tree(commit, tag):
    dest = os.path.join(a.out, 'tree_' + tag)
    subprocess.run(['rm', '-rf', dest]); os.makedirs(dest)
    parts = ['Mii-S', 'WAVE1', 'WAVE2', 'WAVE3', 'WAVE4', 'V3T', 'V3A', 'V3B', 'V3C', 'V3D', 'V3E']
    paths = [f'{B}/results/{p}' for p in parts if exists(commit, f'{B}/results/{p}')]
    tarfile.open(fileobj=io.BytesIO(git('archive', '--format=tar', commit, *paths))).extractall(dest)
    return os.path.join(dest, B)


def manifest(root, tag):
    pairs = []
    for k in (1, 2, 3, 4):
        if os.path.isdir(os.path.join(root, f'results/WAVE{k}')):
            r = subprocess.run(['python3', os.path.join(v3, 'v3_jsonl_leaves.py'), root, f'results/WAVE{k}', f'jtree{k}'],
                               capture_output=True, text=True, check=True)
            print(tag, f'WAVE{k}:', r.stdout.strip())
            if os.path.isdir(os.path.join(root, f'jtree{k}')):
                pairs += [f'results/WAVE{k}', f'jtree{k}']
    M = os.path.join(a.out, f'M_{tag}.jsonl')
    r = subprocess.run(['python3', os.path.join(v3, 'v3_manifest.py'), root, M, os.path.join(a.out, f'C_{tag}.jsonl'), *pairs],
                       capture_output=True, text=True)
    print(tag, 'manifest:', r.stdout.strip()[-300:], r.stderr.strip()[-300:], 'exit', r.returncode)
    print(tag, 'M sha256', sha(M), 'lines', sum(1 for _ in open(M)))
    return M


def verified(root, groups):
    files = sorted(glob.glob(root + '/results/V3T/**/*.jsonl', recursive=True))
    for g in groups:
        files += sorted(glob.glob(root + f'/results/{g}/*/out.jsonl'))
    ver = set()
    for f in files:
        for l in open(f):
            try:
                o = json.loads(l)
            except ValueError:
                continue
            if o.get('kind') == 'leaf' and o.get('verdict') == 'VERIFIED' and 'lits' in o:
                ver.add((o['case'], json.dumps(o['lits'])))
    return ver, len(files)


key = lambda r: (r['case'], json.dumps(r['lits']))
# V3B's Mt at 066eaa9
r066 = tree('066eaa9', '066')
M066 = manifest(r066, '066')
ver066, _ = verified(r066, ('V3A', 'V3B'))
mt = [r for r in map(json.loads, open(M066)) if key(r) not in ver066]
MT = os.path.join(a.out, 'Mt066.jsonl')
with open(MT, 'w') as f:
    for i, r in enumerate(mt):
        r = dict(r); r['idx'] = i; f.write(json.dumps(r) + '\n')
assert sha(MT) == MT_SHA, ('Mt mismatch', sha(MT))
skipb = {int(s) for s in a.skip_b.split(',') if s.strip()}
left_out = {key(r) for i, r in enumerate(mt) if i % 16 in skipb}

rz = tree(a.z, 'Z')
MZ = manifest(rz, 'Z')
ver, nf = verified(rz, ('V3A', 'V3B', 'V3C', 'V3D', 'V3E'))
for spec in a.skip:
    path, shards, n = spec.rsplit(':', 2)
    n = int(n)
    sk = {int(x) for x in shards.split(',') if x.strip()}
    wl = [json.loads(l) for l in open(os.path.join(rz, path))]
    lo = {key(r) for r in wl if r['idx'] % n in sk}
    print('skip', path, 'shards', sorted(sk), 'of', n, ':', len(lo), 'records')
    left_out |= lo
recs = [json.loads(l) for l in open(MZ)]
unver = [r for r in recs if key(r) not in ver]
work = [r for r in unver if key(r) not in left_out]
W = os.path.join(a.out, 'worklist.jsonl')
with open(W, 'w') as f:
    for i, r in enumerate(work):
        r = dict(r); r['idx'] = i; f.write(json.dumps(r) + '\n')
print('verified keys at Z', len(ver), 'from', nf, 'files')
print('manifest at Z', len(recs), '| without VERIFIED', len(unver), '| left out (running machines)', len(unver) - len(work),
      '| work list', len(work))
print('worklist sha256', sha(W))
