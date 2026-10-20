#!/usr/bin/env python3
"""Mop-up task lists for the cubes no running machine will close.

usage: mopup_tasks.py REF GF3.json NOW_EPOCH TASKDIR OUTDIR FIRST_INDEX CASE:K[,CASE:K...]

Open cubes come from GF3.json (gfrontier3.py at REF).  A cube is claimed (left out) if
 - it is in the task list (TASKDIR/H*.json) of a WAVE4 machine that has not written README.md at REF
   (started or not), or extends such a cube (that machine closes the cubes it splits off), or
 - it is in the front of the queue of another running machine (env.txt, no README.md): the first
   0.8 * rate * minutes_left cubes, as in wave4_tasks.py.
Every other open cube of each CASE goes to K new machines named H<FIRST_INDEX>, ... (position p mod K,
in the order: cubes in no running queue first, then the unreserved queue tails from their far end)."""
import json, os, re, subprocess, sys, collections, calendar, time
sys.path.insert(0, os.path.dirname(__file__))
REF, GF, NOW, TASKDIR, OUT, FIRST, SPEC = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5], int(sys.argv[6]), sys.argv[7]
B = 'cloud/es7-2026-10-19/results/'
def git(*a): return subprocess.run(['git', *a], capture_output=True, text=True).stdout
def show(p): return git('show', f'{REF}:{p}')
gf = json.load(open(GF))
fset = set(git('ls-tree', '-r', '--name-only', REF, B).split())
VER = 's VERIFIED UNSAT'

def frontier(roots, closed, split):
    out, st = [], list(reversed(roots))
    while st:
        c = st.pop()
        if tuple(c) in closed: continue
        if tuple(c) in split: st.extend(reversed([c + s for s in split[tuple(c)]])); continue
        out.append(c)
    return out

def running_queue(d):
    vm = d.rsplit('/', 1)[0]
    if f'{B}{vm}/README.md' in fset or f'{B}{vm}/env.txt' not in fset: return None
    env = show(f'{B}{vm}/env.txt')
    m = re.search(r'(\w{3}) (\w{3}) +(\d+) (\d\d):(\d\d):(\d\d) UTC (\d{4})', env)
    start = calendar.timegm(time.strptime(' '.join(m.groups()), '%a %b %d %H %M %S %Y'))
    recs = []
    for l in show(f'{B}{d}/leaves.jsonl').splitlines():
        if l.startswith('{'):
            try: recs.append(json.loads(l))
            except ValueError: pass
    ri = max((i for i, r in enumerate(recs) if r.get('resume')), default=None)
    if ri is None: return None
    rtime = calendar.timegm(time.strptime(recs[ri]['time'], '%Y-%m-%dT%H:%M:%SZ'))
    closed, split = set(), {}
    for r in recs[:ri]:
        if 'cube' not in r: continue
        c = tuple(r['cube'])
        if r.get('status') == 'UNSAT' and r.get('cake_lpr') == VER: closed.add(c)
        elif r.get('status') == 'SKIP': closed.add(c)
        elif r.get('status') == 'SPLIT' and 'subs' in r: split[c] = r['subs']
    top = [list(map(int, l.split()[1:-1])) for l in show(f'{B}{d}/top.icnf').splitlines() if l.startswith('a ')]
    t = next((r for r in recs if r.get('top') and 'nshards' in r), {'shard': 0, 'nshards': 1})
    mine = [c for i, c in enumerate(top) if i % t['nshards'] == t.get('shard', 0)]
    q = frontier(mine, closed, split)
    done = 0
    for r in recs[ri + 1:]:
        if 'cube' not in r: continue
        if r.get('status') in ('UNSAT', 'SPLIT', 'UNSAT_UNCHECKED', 'SAT', 'SKIP', 'TIMEOUT'): done += 1
        if r.get('status') == 'SPLIT' and 'subs' in r: q += [r['cube'] + s for s in r['subs']]
    rate = done / max(1.0, (NOW - rtime) / 60)
    budget = 135 if '/WAVE4/' in '/' + d else 165
    left = max(0.0, (start + budget * 60 - NOW) / 60)
    if d.startswith('WAVE4/') and NOW - rtime < 30 * 60:
        rate = 0.0          # started less than 30 min ago: its rate is not yet meaningful, it keeps its list
    return q, rate, left

# WAVE4 claims: a machine without README whose case directory has no synced leaves.jsonl yet claims its whole list
w4claim = collections.defaultdict(set)
for f in sorted(os.listdir(TASKDIR)):
    if not re.match(r'H\d+\.json$', f): continue
    v = f[:-5]
    if f'{B}WAVE4/{v}/README.md' in fset: continue
    for case, cubes in json.load(open(os.path.join(TASKDIR, f))).items():
        if f'{B}WAVE4/{v}/{case}/leaves.jsonl' in fset: continue
        w4claim[case] |= {tuple(c) for c in cubes}

def claimed_by_w4(case, c):
    s = w4claim.get(case, ())
    return any(c[:k] in s for k in range(len(c), 0, -1))

plan, machines, idx = {}, [], FIRST
for item in SPEC.split(','):
    case, k = item.split(':'); k = int(k)
    opn = [tuple(c) for c in gf[case]['open']]
    opn = [c for c in opn if not claimed_by_w4(case, c)]
    oset = set(opn)
    used, tails, notes, reserved = set(), [], [], 0
    # WAVE4 machines first: a cube in a helper's queue is that helper's, even if an older queue lists it too
    for d in sorted(gf[case]['dirs'], key=lambda d: 0 if d.startswith('WAVE4/') else 1):
        rq = running_queue(d)
        if rq is None: continue
        q, rate, left = rq
        q = [tuple(c) for c in q if tuple(c) in oset and tuple(c) not in used]
        R = int(0.8 * rate * left)
        if d.startswith('WAVE4/') and rate == 0:
            R = len(q)          # just started: no rate yet, it keeps its whole list
        used |= set(q)
        tails.append(list(reversed(q[R:])))
        reserved += min(R, len(q))
        notes.append(f"{d.split('/')[1]}: queue {len(q)} rate {rate:.1f}/min left {left:.0f} min reserve {min(R, len(q))}")
    merged = [c for c in opn if c not in used]
    for i in range(max((len(t) for t in tails), default=0)):
        for t in tails:
            if i < len(t): merged.append(t[i])
    for j in range(k):
        part = [list(c) for c in merged[j::k]]
        if part:
            machines.append((f'H{idx:02d}', case, part)); idx += 1
    plan[case] = {'open': len(gf[case]['open']), 'claimed_by_wave4': len(gf[case]['open']) - len(opn),
                  'reserved_for_running': reserved, 'to_mopup': len(merged), 'machines': k, 'running': notes}
    print(case, json.dumps(plan[case]))
os.makedirs(OUT, exist_ok=True)
for name, case, part in machines:
    json.dump({case: part}, open(os.path.join(OUT, f'{name}.json'), 'w'))
    print(name, case, len(part), dict(sorted(collections.Counter(len(c) for c in part).items())))
json.dump(plan, open(os.path.join(OUT, 'plan_mopup.json'), 'w'), indent=1)
