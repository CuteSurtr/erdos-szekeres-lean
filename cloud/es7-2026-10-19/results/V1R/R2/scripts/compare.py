#!/usr/bin/env python3
"""Compare out.jsonl with results/V1-0..V1-3 leaves_cake.jsonl (same i, same cube) and the leaf file."""
import glob, json, sys
here, res, leaves, J = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
lines = [[int(x) for x in l.split()[1:-1]] for l in open(leaves)]
old = {}
for f in sorted(glob.glob(f'{res}/V1-[0-3]/leaves_cake.jsonl')):
    for l in open(f):
        r = json.loads(l)
        k = r['i'] if 'i' in r else r['line']  # V1-1/V1-3 call it 'line'; base checked below
        r['_idx'] = k; old.setdefault(k, []).append((f.split('/')[-2], r))
# earlier verdict fields differ in wording ('s VERIFIED UNSAT' or 'VERIFIED UNSAT')
def old_ok(x): return x['solver_exit'] == 20 and x['cake_lpr'].strip() in ('s VERIFIED UNSAT', 'VERIFIED UNSAT')
base = {}
for k, recs in old.items():
    for src, x in recs:
        b = 0 if k < len(lines) and lines[k] == x['cube'] else (1 if 0 < k <= len(lines) and lines[k-1] == x['cube'] else None)
        base.setdefault(src, set()).add(b)
print('index base of earlier records (0 = 0-based):', {s: sorted(map(str, b)) for s, b in base.items()})
mine = {}
for l in open(f'{here}/out.jsonl'):
    r = json.loads(l); mine.setdefault(r['i'], []).append(r)
share = [i for i in range(len(lines)) if i % 4 == J]
diffs = []
for i in share:
    if i not in mine: diffs.append(f'i={i}: not run here'); continue
    r = mine[i][-1]
    if r['cube'] != lines[i]: diffs.append(f'i={i}: cube differs from hull_leaves.icnf line')
    ok = r['solver_exit'] == 20 and r['cake_lpr'] == 's VERIFIED UNSAT'
    if not ok: diffs.append(f'i={i}: here exit {r["solver_exit"]}, cake_lpr {r["cake_lpr"]!r}')
    o = old.get(i, [])
    if not o: diffs.append(f'i={i}: no earlier record'); continue
    okold = [x for x in o if old_ok(x[1])]
    if not okold: diffs.append(f'i={i}: earlier record not verified')
    for src, x in o:
        if x['cube'] != r['cube']: diffs.append(f'i={i}: cube differs from {src}')
        elif x['solver_exit'] != r['solver_exit']: diffs.append(f'i={i}: solver exit differs from {src}')
extra = [i for i in mine if i % 4 != J]
nver = sum(1 for i in share if i in mine and mine[i][-1]['solver_exit'] == 20 and mine[i][-1]['cake_lpr'] == 's VERIFIED UNSAT')
print(f'share {len(share)}, run {len([i for i in share if i in mine])}, verified {nver}, earlier records for share {sum(1 for i in share if i in old)}')
print(f'solve_s total {sum(m[-1]["solve_s"] for m in mine.values()):.1f}, check_s total {sum(m[-1]["check_s"] for m in mine.values()):.1f}')
big = max((m[-1] for m in mine.values()), key=lambda r: r['proof_bytes'], default=None)
slow = max((m[-1] for m in mine.values()), key=lambda r: r['solve_s'], default=None)
if big: print(f'largest proof: i={big["i"]} {big["proof_bytes"]} bytes, solve {big["solve_s"]} s; slowest solve: i={slow["i"]} {slow["solve_s"]} s')
print('differences:' if diffs else 'differences: none'); [print(' ', d) for d in diffs]
