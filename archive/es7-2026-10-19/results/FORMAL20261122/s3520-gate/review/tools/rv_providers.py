# Reviewer: one-provider audit of the closure printed by my compile (MODULE lines), over the LEAN_PATH it used;
# plus pins: CompactChecker oleans vs the verified 311 record, RS catalog/bridge oleans vs res-slices-fv records.
import os, sys, json, hashlib, re
RV = '/home/jay/research/data/formalize-20261122/s3520-gate/review'
lp = open(RV + '/logs/rv_lean_path.txt').read().strip().split(':')
mods = [l[7:].strip() for l in open(RV + '/logs/RV3520.log') if l.startswith('MODULE ')]
H = {}
def sha(p):
    if p not in H: H[p] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return H[p]
multi, missing, by_dir = [], [], {}
prov = {}
for m in mods:
    rel = m.replace('.', '/') + '.olean'
    hits = [d for d in lp if os.path.exists(os.path.join(d, rel))]
    if not hits: missing.append(m); continue
    prov[m] = os.path.join(hits[0], rel)
    by_dir[hits[0]] = by_dir.get(hits[0], 0) + 1
    if len(hits) > 1:
        real = {os.path.realpath(os.path.join(d, rel)) for d in hits}
        contents = {sha(os.path.join(d, rel)) for d in hits}
        multi.append((m, hits, len(real), len(contents)))
print('modules in closure', len(mods), '| missing', missing)
for d, n in by_dir.items(): print(f'  {n:6d} from {d}')
print('modules found in more than one LEAN_PATH dir:', len(multi))
for m, hits, nr, nc in multi: print('  ', m, 'dirs', len(hits), 'distinct realpaths', nr, 'distinct contents', nc)
# RS3520 modules must come from the gate's olean dir
g = '/home/jay/research/data/formalize-20261122/s3520-gate/olean'
bad = [m for m in mods if m.startswith('RS3520.') and not prov[m].startswith(g + '/')]
print('RS3520.* modules', sum(1 for m in mods if m.startswith('RS3520.')), 'not from the gate olean dir:', bad)
# pins
rec = open('/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05/logs/es311/final311-compact.json').read()
for m in sorted(x for x in mods if x.startswith('CompactChecker.')):
    h = sha(prov[m]); ok = h in rec
    print(f'  pin {m}: {h[:16]} in final311-compact.json: {ok} (provider {os.path.realpath(prov[m])})')
cat = json.load(open('/home/jay/research/data/formalize-20261122/res-slices-fv/data/cat3520.json'))
cs = json.dumps(cat)
for m in sorted(x for x in mods if x.startswith('RS.')):
    h = sha(prov[m]); print(f'  RS olean {m}: {h[:16]} listed in res-slices-fv data/cat3520.json: {h in cs}')
