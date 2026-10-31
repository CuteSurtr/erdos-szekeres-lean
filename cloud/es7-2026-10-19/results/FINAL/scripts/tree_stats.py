#!/usr/bin/env python3
"""Per-case cube tree from all wave directories at REF (run in the es7wt worktree).
usage: tree_stats.py REF OUT.json
Root children = top cubes that are not split children of another cube. A node is: an exact leaf (its
literal sequence was closed with cake_lpr VERIFIED), split (children = node + sub for one SPLIT record),
subsumed (a closed cube whose literal set is a proper subset, or the same set in another order, covers it),
or open. Reports per case: nodes, exact leaves, subsumed, open, conflicting SPLIT records, max depth."""
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
per = collections.defaultdict(lambda: {'top': set(), 'closed': set(), 'subs': {}, 'conflict': 0, 'whole': False})
for d in dirs:
    recs = []
    for l in show(d + '/leaves.jsonl').splitlines():
        l = l.strip()
        if l.startswith('{'):
            try: recs.append(json.loads(l))
            except ValueError: pass
    case = dircase(d, recs)
    if case is None: continue
    P = per[case]
    P['top'] |= set(cubes(show(d + '/top.icnf')))
    for c in cubes(show(d + '/leaves.icnf')):
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
        elif st == 'SPLIT' and 'subs' in r:
            subs = r['subs']
            if isinstance(subs, str): subs = json.loads(subs)
            subs = tuple(tuple(s) for s in subs)
            if c in P['subs'] and P['subs'][c] != subs: P['conflict'] += 1
            P['subs'].setdefault(c, subs)
res, tot = {}, collections.Counter()
for case, P in sorted(per.items()):
    if P['whole']:
        res[case] = {'whole': True}; tot['whole'] += 1; continue
    children = {c + s for c, subs in P['subs'].items() for s in subs}
    roots = sorted(t for t in P['top'] if t not in children)
    closed_sets = collections.defaultdict(list)
    for k in P['closed']:
        for l in k: closed_sets[l].append(frozenset(k))
    def subsumed(c):
        s = frozenset(c)
        return any(k <= s for l in c for k in closed_sets.get(l, ()))
    st = collections.Counter(); maxd = 0
    stack = [(r, 1) for r in roots]
    seen = set()
    while stack:
        c, dep = stack.pop()
        if c in seen: st['dup'] += 1; continue
        seen.add(c); maxd = max(maxd, dep)
        if c in P['closed']: st['leaf'] += 1
        elif c in P['subs']:
            st['split'] += 1; stack.extend((c + s, dep + 1) for s in P['subs'][c])
        elif subsumed(c): st['subsumed'] += 1
        else: st['open'] += 1
    res[case] = {'roots': len(roots), **st, 'conflict': P['conflict'], 'maxdepth': maxd,
                 'closed_records': len(P['closed']), 'unused_closed': len(P['closed'] - seen)}
    for k, v in st.items(): tot[k] += v
    tot['conflict'] += P['conflict']; tot['unused_closed'] += len(P['closed'] - seen)
json.dump(res, open(OUT, 'w'), indent=0)
print('totals', dict(tot))
for case, r in sorted(res.items(), key=lambda kv: -kv[1].get('leaf', 0))[:12]:
    print(case, r)
print('cases with subsumed nodes:', sum(1 for r in res.values() if r.get('subsumed')), ' with open:', sum(1 for r in res.values() if r.get('open')),
      ' with conflicts:', sum(1 for r in res.values() if r.get('conflict')), ' roots != 128 (non-whole):',
      collections.Counter(r['roots'] for r in res.values() if not r.get('whole')).most_common(8))
