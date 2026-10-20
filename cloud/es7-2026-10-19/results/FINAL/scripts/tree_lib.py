import subprocess, json, sys, collections
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
