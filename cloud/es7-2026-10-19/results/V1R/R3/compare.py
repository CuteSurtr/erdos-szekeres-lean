import json, glob, sys
B = '/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results'
old = {}
for f in glob.glob(B + '/V1-[0-3]/leaves_cake.jsonl'):
    for l in open(f):
        r = json.loads(l); r['i'] = r.get('i', r.get('line')); old.setdefault(r['i'], []).append((f.split('/')[-2], r))
mine = {}
for l in open(sys.argv[1]):
    r = json.loads(l)
    if r['i'] not in mine or r.get('ok'): mine[r['i']] = r
diffs = []
for i, r in sorted(mine.items()):
    o = old.get(i)
    if not o: diffs.append(f'i={i}: no earlier record'); continue
    for src, x in o:
        if x['cube'] != r['cube']: diffs.append(f'i={i}: cube differs from {src}')
        if x['solver_exit'] != r['solver_exit']: diffs.append(f'i={i}: solver_exit {r["solver_exit"]} vs {x["solver_exit"]} ({src})')
        if ('VERIFIED UNSAT' in str(x.get('cake_lpr'))) != (r['cake_lpr'] == 's VERIFIED UNSAT'): diffs.append(f'i={i}: cake_lpr verdict {r["cake_lpr"]!r} vs {x.get("cake_lpr")!r} ({src})')
        if x.get('proof_bytes') != r['proof_bytes']: diffs.append(f'i={i}: proof_bytes {r["proof_bytes"]} vs {x.get("proof_bytes")} ({src}) [informational]')
ok = sum(r['ok'] for r in mine.values())
print('records', len(mine), 'verified', ok, 'solve_s', round(sum(r['solve_s'] for r in mine.values()), 1), 'check_s', round(sum(r['check_s'] for r in mine.values()), 1))
big = max(mine.values(), key=lambda r: r['solve_s'], default=None)
if big: print('largest(solve)', big['i'], big['solve_s'], big['proof_bytes'])
bigp = max(mine.values(), key=lambda r: r['proof_bytes'], default=None)
if bigp: print('largest(proof)', bigp['i'], bigp['solve_s'], bigp['proof_bytes'])
print('n_old_shards_per_i', sorted(set(len(v) for v in old.values())), 'old_total', len(old))
for d in diffs: print(d)
