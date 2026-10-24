#!/usr/bin/env python3
"""Global per-case frontier over all directories of results/WAVE1, WAVE2 and WAVE3 on a git ref.

For each case: created = union over dirs of (top cubes of that dir's shard, or the dir's --top share)
plus, for every SPLIT record, parent+sub for each sub; closed = union of UNSAT records whose cake_lpr is
exactly 's VERIFIED UNSAT' (a cube [] closes the whole case); a created cube is open if it was not split
anywhere and no closed cube's literal set is a subset of its literal set. Cases closed directly (Haudit
t5_all172) or vacuous are not wave cases; we report only the cases that have at least one wave directory
or are in the open_cases list.
Usage: gfrontier.py REF OUT.json"""
import subprocess, json, sys, collections
REF, OUT = sys.argv[1], sys.argv[2]
B = 'cloud/es7-2026-10-19/results/'
def git(*a): return subprocess.run(['git', *a], capture_output=True, text=True).stdout
def show(p): return git('show', f'{REF}:{p}')
cases = [json.loads(l) for l in show(B + 'Mii-S/cases.jsonl').splitlines() if l.strip()]
sha2case = {c['cnf_sha256']: c['case'] for c in cases}
names = sorted((c['case'] for c in cases), key=len, reverse=True)
files = git('ls-tree', '-r', '--name-only', REF, B + 'WAVE1', B + 'WAVE2', B + 'WAVE3', B + 'WAVE4').split()
dirs = sorted({f.rsplit('/', 1)[0] for f in files if f.endswith('/leaves.jsonl') or f.endswith('/top.icnf') or f.endswith('/leaves.icnf')})
def dircase(d, recs):
    for r in recs:
        if r.get('case_sha256') in sha2case: return sha2case[r['case_sha256']]
    base = d.rsplit('/', 1)[1]
    for n in names:
        rest = base[len(n):]
        if base == n or (base.startswith(n) and not rest[:1].isdigit() and not (rest[:1] == '-' and rest[1:2].isdigit())):
            return n
    return None
def cubes(text): return [tuple(map(int, l.split()[1:-1])) for l in text.splitlines() if l.startswith('a ')]
per = collections.defaultdict(lambda: {'created': set(), 'closed': set(), 'split': set(), 'whole': False, 'dirs': []})
for d in dirs:
    recs = []
    for l in show(d + '/leaves.jsonl').splitlines():
        l = l.strip()
        if l.startswith('{'):
            try: recs.append(json.loads(l))
            except ValueError: pass
    case = dircase(d, recs)
    if case is None: continue
    P = per[case]; P['dirs'].append(d.split('results/')[1])
    top = cubes(show(d + '/top.icnf'))
    shard, nsh = 0, 1
    for r in recs:
        if r.get('top') and 'nshards' in r: shard, nsh = r.get('shard', 0), r['nshards']
    P['created'].add(())                      # the whole case is a cube; a top.icnf splits it
    if top:
        P['split'].add(()); P['created'] |= set(top)   # all top cubes, whatever the shard (robust to missing shard dirs)
    for c in cubes(show(d + '/leaves.icnf')):   # leaves.icnf lines are verified leaves by the wave contract
        if c == (): P['whole'] = True
        P['closed'].add(c)
    for r in recs:
        cube = r.get('cube')
        if isinstance(cube, str): cube = json.loads(cube)
        if not isinstance(cube, list): continue
        c = tuple(cube); st = r.get('status')
        if st == 'UNSAT' and r.get('cake_lpr') == 's VERIFIED UNSAT':
            if not c: P['whole'] = True
            P['closed'].add(c)
        elif st == 'SPLIT':
            P['split'].add(c); subs = r.get('subs', [])
            if isinstance(subs, str): subs = json.loads(subs)
            for s in subs: P['created'].add(c + tuple(s))
res = {}
for case, P in sorted(per.items()):
    if P['whole']:
        res[case] = {'open': [], 'closed': len(P['closed']), 'dirs': P['dirs'], 'whole': True}; continue
    closed_sets = [frozenset(k) for k in P['closed']]
    by_lit = collections.defaultdict(list)
    for k in closed_sets:
        for l in k: by_lit[l].append(k)
        if not k: by_lit[None].append(k)
    def covered(c):
        s = frozenset(c)
        for l in c:
            for k in by_lit.get(l, ()):
                if k <= s: return True
        return False
    opn = sorted(c for c in P['created'] if c not in P['split'] and c not in P['closed'] and not covered(c))
    res[case] = {'open': [list(c) for c in opn], 'closed': len(P['closed']), 'nsplit': len(P['split']), 'dirs': P['dirs'], 'whole': False}
json.dump(res, open(OUT, 'w'))
tot = 0
for case, r in sorted(res.items(), key=lambda kv: -len(kv[1]['open'])):
    if r['open']:
        tot += len(r['open'])
        depth = collections.Counter(len(c) for c in r['open'])
        print(f"{case:10s} open={len(r['open']):5d} closed={r['closed']:5d} depths={dict(sorted(depth.items()))} dirs={len(r['dirs'])}")
print('cases with wave dirs:', len(res), 'closed (no open cube):', sum(1 for r in res.values() if not r['open']), 'open cubes total:', tot)
