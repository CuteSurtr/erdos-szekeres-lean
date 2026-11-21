import json, gzip, hashlib, os, sys
A = '<scratch>/agents/lean-rebuild'
L = A + '/esb/experiments/omission-compact-checker-2026-11-05/logs/es311/chain311-library.json.gz'
d = json.load(gzip.open(L))
roots = d['roots']
PK = A + '/esb/.lake/packages'
OUT = A + '/olean'
TC = '<home>/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean'
def local_root(r):
    # map a Linux root to the local one
    if '/.lake/packages/' in r:
        pkg = r.split('/.lake/packages/')[1].split('/')[0]
        return PK + '/' + pkg + '/.lake/build/lib/lean'
    if 'toolchains' in r: return TC
    if r.endswith('/.lake/build/lib/lean'): return OUT   # main library -> our rebuild
    return None
stats = {}
mism = []
for mod, (ri, h) in d['modules'].items():
    r = roots[ri]; lr = local_root(r)
    grp = 'ErdosSzekeres(rebuilt here)' if lr == OUT else ('toolchain' if lr == TC else r.split('/.lake/packages/')[-1].split('/')[0] if '/.lake/packages/' in r else r)
    p = os.path.join(lr, *mod.split('.')) + '.olean' if lr else None
    if not p or not os.path.exists(p):
        st = 'absent'
    else:
        hh = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        st = 'match' if hh == h else 'MISMATCH'
        if st == 'MISMATCH': mism.append((mod, hh, h))
    stats.setdefault(grp, {}).setdefault(st, 0); stats[grp][st] += 1
print('roots:'); [print('  ', i, r) for i, r in enumerate(roots)]
for g, s in sorted(stats.items()): print(g, s)
print('mismatches:', len(mism))
for m in mism[:20]: print('  ', m)
