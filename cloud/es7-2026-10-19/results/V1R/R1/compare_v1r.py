import json, glob, sys
R = '/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/'
old = {}
for f in sorted(glob.glob(R + 'V1-[0-3]/leaves_cake.jsonl')):
    for l in open(f):
        r = json.loads(l); r['i'] = r['i'] if 'i' in r else r['line']; old.setdefault(r['i'], []).append((f.split('/')[-2], r))
mine = [json.loads(l) for l in open(R + 'V1R/R1/out.jsonl')]
diffs = []
for r in sorted(mine, key=lambda r: r['i']):
    o = old.get(r['i'])
    if not o: diffs.append(f"i={r['i']}: no earlier record"); continue
    for src, x in o:
        if x['cube'] != r['cube']: diffs.append(f"i={r['i']} ({src}): cube differs {x['cube']} vs {r['cube']}")
        if x.get('solver_exit') != r['solver_exit']: diffs.append(f"i={r['i']} ({src}): solver_exit {x.get('solver_exit')} vs {r['solver_exit']}")
        if x.get('cake_lpr') != r['cake_lpr'] and not (src == 'V1-1' and x.get('cake_lpr') == 'VERIFIED UNSAT' and r['cake_lpr'] == 's VERIFIED UNSAT'): diffs.append(f"i={r['i']} ({src}): cake_lpr {x.get('cake_lpr')!r} vs {r['cake_lpr']!r}")
    if len(o) > 1: diffs.append(f"i={r['i']}: {len(o)} earlier records ({[s for s,_ in o]})")
n = len(mine); v = sum(r['verified'] for r in mine)
print(f"records {n}, verified {v}, solve_s {sum(r['solve_s'] for r in mine):.1f}, check_s {sum(r['check_s'] or 0 for r in mine):.1f}")
if mine:
    b = max(mine, key=lambda r: r['proof_bytes']); s = max(mine, key=lambda r: r['solve_s'])
    print(f"largest proof: i={b['i']} {b['proof_bytes']} bytes, solve {b['solve_s']} s; slowest solve: i={s['i']} {s['solve_s']} s")
print('earlier records with i in this shard:', sum(1 for i in old if i % 4 == 1))
print('differences:', len(diffs)); print('\n'.join(diffs))
