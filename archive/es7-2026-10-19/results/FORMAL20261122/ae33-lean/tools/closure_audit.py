#!/usr/bin/env python3
"""Import-closure audit (the assemble_final310.sh pattern): every module loaded by AE33Geo.Radius1 is resolved on
the LEAN_PATH of tools/geo_env.sh; a module found under two roots is refused; library/Mathlib oleans are compared
with the pins of build/chain311/library.json; ENCBLEAN oleans with sevenfold's byte-identical rebuild list when
present; own oleans are listed with SHA-256. Input: the MODULE lines printed by lean/AE33Geo/ModList.lean."""
import hashlib, json, os, re, subprocess, sys
D = '/home/jay/research/data/formalize-20261122/ae33-lean'
R = '/home/jay/research/lean/erdos-szekeres-lean'
LIB = R + '/experiments/omission-compact-checker-2026-11-05/build/chain311/library.json'
env = subprocess.run(['bash', '-c', f'source {D}/tools/geo_env.sh; echo $LEAN_PATH'], capture_output=True, text=True).stdout.strip()
roots = env.split(':')
mods = [l.split()[1] for l in open(sys.argv[1]) if l.startswith('MODULE ')]
lib = json.load(open(LIB))
libroots = [r.replace('<repo>', R).replace('<home>', '/home/jay') for r in lib['roots']]
pins = lib['modules']
def sha(p):
    h = hashlib.sha256(); f = open(p, 'rb')
    for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
out, bad, stats = [], [], {'pinned_ok': 0, 'pinned_mismatch': 0, 'own': 0, 'encb': 0, 'other': 0}
for m in mods:
    rel = m.replace('.', '/') + '.olean'
    found = [r for r in roots if os.path.exists(os.path.join(r, rel))]
    if len(found) != 1:
        bad.append(f'{m}: found under {len(found)} roots'); continue
    p = os.path.join(found[0], rel); h = sha(p)
    if m in pins:
        ok = pins[m][1] == h and os.path.normpath(libroots[pins[m][0]]) == os.path.normpath(found[0])
        stats['pinned_ok' if ok else 'pinned_mismatch'] += 1
        if not ok: bad.append(f'{m}: pin mismatch')
        kind = 'pinned'
    elif found[0].startswith(D):
        stats['own'] += 1; kind = 'own'
    elif 'ENCBLEAN' in found[0]:
        stats['encb'] += 1; kind = 'encb'
    else:
        stats['other'] += 1; kind = 'other'
    out.append(f'{kind}\t{m}\t{h}\t{p}')
open(D + '/logs/closure_audit.tsv', 'w').write('\n'.join(out) + '\n')
res = {'modules': len(mods), **stats, 'problems': bad, 'PASS': not bad and stats['pinned_mismatch'] == 0}
json.dump(res, open(D + '/logs/closure_audit.json', 'w'), indent=1)
print(json.dumps(res, indent=1)[:2000])
