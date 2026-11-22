# Reviewer's own check of the gate export: manifests vs sources (sha256), oleans present, leaf sums vs T7,
# per-module logs (lean_rc, whole standard axiom lines, CPU), sampled memory, bytes per leaf.  No worker code used.
import json, hashlib, os, re, sys
G = '/home/jay/research/data/formalize-20261122/s3520-gate'
T7 = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113/budget34/audit/fresh-b35s20-v169-bbs1/contexts.jsonl'
t7 = {}
for line in open(T7):
    d = json.loads(line); t7[d['context']] = d
STD = "depends on axioms: [propext, Classical.choice, Quot.sound]"
tot = dict(leaves=0, src=0, olean=0, cpu=0.0, mods=0)
per_mod = []
problems = []
axt = []          # (module, target) from the sources
for u in ('0161', '1793', '2080'):
    man = json.load(open(f'{G}/export/3520/ctx/ctx-{u}.json'))
    leaves = sum(md['leaves'] for md in man['modules'])
    ut = dict(leaves=0, src=0, olean=0, cpu=0.0)
    if leaves != man['leaves_expected']: problems.append(f'unit {u}: module leaves {leaves} != leaves_expected {man["leaves_expected"]}')
    for md in man['modules']:
        stem = md['module'].split('.')[-1]
        src = f'{G}/export/3520/{md["file"]}'
        b = open(src, 'rb').read()
        if hashlib.sha256(b).hexdigest() != md['sha256']: problems.append(f'{stem}: source sha256 differs from manifest')
        if len(b) != md['source_bytes']: problems.append(f'{stem}: source bytes differ')
        if md['min_margin'] < 1 or md['corrupted']: problems.append(f'{stem}: margin {md["min_margin"]} corrupted {md["corrupted"]}')
        ol = f'{G}/olean/RS3520/{stem}.olean'
        osz = os.path.getsize(ol) if os.path.exists(ol) else None
        if osz is None: problems.append(f'{stem}: no olean')
        log = open(f'{G}/logs/RS3520_{stem}.log', errors='replace').read()
        rc = re.findall(r'^lean_rc=(\d+)$', log, re.M)
        if rc != ['0']: problems.append(f'{stem}: lean_rc lines {rc}')
        ut_ = float(re.search(r'User time \(seconds\): ([\d.]+)', log).group(1))
        st_ = float(re.search(r'System time \(seconds\): ([\d.]+)', log).group(1))
        rss = int(re.search(r'Maximum resident set size \(kbytes\): (\d+)', log).group(1))
        targets = re.findall(r'^#print axioms (\S+)$', b.decode(), re.M)
        roots = ['ex%d' % r[0] for r in md['subtree_roots']]
        if targets != roots: problems.append(f'{stem}: #print axioms targets {targets} != manifest roots {roots}')
        whole = []
        for t in targets:
            full = f"'{md['module']}.{t}' {STD}"
            ok = any(line.strip() == full for line in log.split('\n'))
            whole.append(ok); axt.append((md['module'], t, ok))
        mem = open(f'{G}/logs/RS3520_{stem}.mem').read()
        anon = int(re.search(r'anon_shmem_max_mb=(\d+)', mem).group(1))
        cpu = ut_ + st_
        per_mod.append((stem, md['leaves'], cpu / md['leaves'], len(b) / md['leaves'], (osz or 0) / md['leaves'], anon, rss // 1024, sum(whole), len(targets)))
        for k, v in (('leaves', md['leaves']), ('src', len(b)), ('olean', osz or 0), ('cpu', cpu)):
            ut[k] += v; tot[k] += v
        tot['mods'] += 1
    t7note = ''
    if u == '2080': t7note = f"T7 ctx-4274 leaves {t7[4274]['leaves']}"
    if u == '0161': t7note = f"T7 ctx-169 leaves {t7[169]['leaves']}"
    print(f"unit {u}: modules {len(man['modules'])}, leaves {ut['leaves']} (expected {man['leaves_expected']}; {t7note}), "
          f"CPU {ut['cpu']:.1f} s = {ut['cpu']/ut['leaves']:.5f} s/leaf, source {ut['src']/ut['leaves']:.0f} B/leaf, olean {ut['olean']/ut['leaves']:.0f} B/leaf, base_path {man['base_path'] if u=='2080' else '-'}")
print(f"ALL: modules {tot['mods']}, leaves {tot['leaves']}, CPU {tot['cpu']:.1f} s = {tot['cpu']/tot['leaves']:.5f} s/leaf, source {tot['src']/tot['leaves']:.0f} B/leaf, olean {tot['olean']/tot['leaves']:.0f} B/leaf")
r = [p[2] for p in per_mod]; print(f"per-module s/leaf min {min(r):.4f} max {max(r):.4f}; source B/leaf {min(p[3] for p in per_mod):.0f}-{max(p[3] for p in per_mod):.0f}; olean B/leaf {min(p[4] for p in per_mod):.0f}-{max(p[4] for p in per_mod):.0f}")
mx = max(per_mod, key=lambda p: p[5]); print(f"max sampled anon+shmem {mx[5]} MB ({mx[0]}, {mx[1]} leaves); max RSS {max(p[6] for p in per_mod)} MB")
print(f"axiom targets {len(axt)}, whole standard lines {sum(1 for a in axt if a[2])}; not whole: {[(a[0], a[1]) for a in axt if not a[2]]}")
print('problems:', problems if problems else 'none')
json.dump([list(a) for a in axt], open(sys.argv[1], 'w'))
