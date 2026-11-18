#!/usr/bin/env python3
"""mk_readme.py -- assemble the record README from readme_parts/ and the ladder logs."""
import re, glob, os, json
W = '/home/jay/research/data/etv7sat-20261113'
R = '/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/ETV7SAT20261113'
p1 = open(f'{W}/readme_parts/part1.md').read()
p2 = open(f'{W}/readme_parts/part2.md').read()
status = open(f'{W}/readme_parts/status.md').read()
nxt = open(f'{W}/readme_parts/next.md').read()
scaling = open(f'{W}/readme_parts/scaling.md').read()
colmax = open(f'{W}/readme_parts/colmax.txt').read().strip()

rows = []
def parse(line):
    d = {}
    m = re.match(r'N=(\d+)', line); d['N'] = int(m.group(1))
    m = re.search(r'flags=\[(.*?)\]', line); d['flags'] = m.group(1) if m else '--nosig'
    d['res'] = 'UNSAT' if 's UNSATISFIABLE' in line else ('SAT' if 's SATISFIABLE' in line else 'no verdict')
    m = re.search(r'cadical_wall=(\d+)', line); d['wall'] = int(m.group(1)) if m else None
    m = re.search(r'verified=(\d*)', line); d['ver'] = m.group(1) == '1'
    m = re.search(r'lrat_bytes=(\d+)', line); d['lrat'] = int(m.group(1)) if m else None
    m = re.search(r'cake_wall=(\d+)', line); d['cake'] = int(m.group(1)) if m else None
    m = re.search(r'conflicts=(\d+)', line); d['conf'] = int(m.group(1)) if m else None
    m = re.search(r'cnf_sha=([0-9a-f]+)', line); d['sha'] = m.group(1) if m else ''
    return d
seen = []
for f in sorted(glob.glob(f'{W}/run/ladder_*.log')):
    tag = os.path.basename(f)[7:-4]
    for line in open(f):
        if line.strip():
            d = parse(line); d['tag'] = tag
            # LRAT hash from the .cake file
            ck = f'{W}/run/lad_{tag}_N{d["N"]}.cake'
            d['lsha'] = ''
            if os.path.exists(ck):
                for l in open(ck):
                    if l.strip().endswith('.lrat'):
                        d['lsha'] = l.split()[0]
            gl = f'{W}/run/lad_{tag}_N{d["N"]}.gen.log'
            d['size'] = ''
            if os.path.exists(gl):
                m = re.search(r"vars (\d+) clauses (\d+)", open(gl).read())
                if m: d['size'] = f'{int(m.group(1)):,} / {int(m.group(2)):,}'
            seen.append(d)
seen.sort(key=lambda d: (-d['N'], d['flags']))
lines = ['| N | generator flags | variables / clauses | CaDiCaL 2.1.3 | conflicts | LRAT bytes | cake_lpr | status | SHA-256 CNF / LRAT |',
         '|---|---|---|---|---|---|---|---|---|']
for d in seen:
    if d['res'] == 'UNSAT' and d['ver']:
        st = f'**CERTIFIED**: M(5; 7) ≤ {d["N"]-1}'
        ck = f'`s VERIFIED UNSAT`, {d["cake"]} s'
    elif d['res'] == 'UNSAT':
        st = 'COMPUTED only (not checked)'; ck = '—'
    else:
        st = 'no verdict'; ck = '—'
    lr = f'{d["lrat"]:,}' if d['lrat'] else '—'
    cf = f'{d["conf"]:,}' if d['conf'] else '—'
    wall = f'{d["res"]}, {d["wall"]} s' if d['res'] != 'no verdict' else f'no verdict in {d["wall"]} s'
    sha = f'`{d["sha"]}` / `{d["lsha"]}`' if d['lsha'] else f'`{d["sha"]}`'
    lines.append(f'| {d["N"]} | `{d["flags"]}` | {d["size"]} | {wall} | {cf} | {lr} | {ck} | {st} | {sha} |')
ladder = '\n'.join(lines)
cl = ['| case | rows | CaDiCaL 2.1.3 | conflicts | LRAT bytes | cake_lpr | SHA-256 CNF / LRAT |', '|---|---|---|---|---|---|---|']
cubes_ok = 0
if os.path.exists(f'{W}/run/cubes.log'):
    for line in open(f'{W}/run/cubes.log'):
        if not line.strip(): continue
        nm = re.search(r'name=(\S+)', line).group(1)
        rw = re.search(r'rows=\[(.*?)\]', line).group(1)
        res = 'UNSAT' if 's UNSATISFIABLE' in line else ('SAT' if 's SATISFIABLE' in line else 'no verdict')
        wall = re.search(r'cadical_wall=(\d+)', line); wall = wall.group(1) if wall else '?'
        ver = re.search(r'verified=(\d+)', line).group(1) != '0'
        lr = re.search(r'lrat_bytes=(\d+)', line); lr = f'{int(lr.group(1)):,}' if lr else '—'
        ck = re.search(r'cake_wall=(\d+)', line); ck = ck.group(1) if ck else '?'
        cf = re.search(r'conflicts=(\d+)', line); cf = f'{int(cf.group(1)):,}' if cf else '—'
        sha = re.search(r'cnf_sha=([0-9a-f]+)', line).group(1)
        lsha = re.search(r'lrat_sha=([0-9a-f]*)', line); lsha = lsha.group(1) if lsha else ''
        cake = f'`s VERIFIED UNSAT`, {ck} s' if (res == 'UNSAT' and ver) else '—'
        if res == 'UNSAT' and ver: cubes_ok += 1
        cl.append(f'| `{nm}` | {rw} | {res}, {wall} s | {cf} | {lr} | {cake} | `{sha}`' + (f' / `{lsha}` |' if lsha else ' |'))
cubes = '\n'.join(cl) if len(cl) > 2 else '(both cases were still running at the time of writing; see the status block)'
out = (p1.replace('@@STATUS@@', status.strip()) +
       p2.replace('@@LADDER@@', ladder).replace('@@SCALING@@', scaling.strip()).replace('@@COLMAX@@', colmax).replace('@@NEXT@@', nxt.strip()).replace('@@CUBES@@', cubes))
n37 = open(f'{W}/readme_parts/n37.txt').read().strip() if os.path.exists(f'{W}/readme_parts/n37.txt') else 'still running'
mb = int(open(f'{W}/readme_parts/mbound.txt').read().strip())
out = out.replace('@@COLMAX@@', colmax).replace('@@N37@@', n37).replace('@@MB@@', str(mb)).replace('@@N5B@@', str(22 + mb))
rep = ''
for f in ('repro.log', 'extra_checks.log'):
    if os.path.exists(f'{W}/run/{f}'):
        rep += ''.join(l for l in open(f'{W}/run/{f}') if l.strip() and l.strip() != 'done')
out = out.replace('@@REPRO@@', rep.strip() or '(not finished at the time of writing)')
assert '@@' not in out, [l for l in out.split('\n') if '@@' in l][:3]
open(f'{R}/README.md', 'w').write(out)
json.dump(seen, open(f'{R}/data/ladder_table.json', 'w'), indent=1)
print('README written', len(out), 'bytes;', len(seen), 'ladder lines')
