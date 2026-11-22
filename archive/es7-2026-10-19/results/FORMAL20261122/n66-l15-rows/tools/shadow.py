"""Providers per module on a LEAN_PATH (own code): every module name with more than one .olean on the path, and
whether those files are byte-identical. usage: LEAN_PATH=... python3 -I shadow.py"""
import os, hashlib, collections
prov = collections.defaultdict(list)
for d in os.environ['LEAN_PATH'].split(':'):
    for root, _, files in os.walk(d):
        for f in files:
            if f.endswith('.olean'):
                prov[os.path.relpath(os.path.join(root, f), d)[:-6].replace('/', '.')].append(os.path.join(root, f))
dup = {m: p for m, p in prov.items() if len(p) > 1}
def h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
bad = 0
for m, ps in sorted(dup.items()):
    same = len({h(p) for p in ps}) == 1
    bad += not same
    print(('IDENTICAL ' if same else 'DIFFERENT ') + m + ' ' + ' '.join(ps))
print(f'modules {len(prov)} with >1 provider {len(dup)} of which different {bad}')
