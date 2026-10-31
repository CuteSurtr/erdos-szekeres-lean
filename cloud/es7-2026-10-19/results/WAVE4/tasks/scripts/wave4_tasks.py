#!/usr/bin/env python3
"""WAVE4 helper task lists.  usage: wave4_tasks.py REF GF3.json NOW_EPOCH OUTDIR CASE:K[,CASE:K...] [PREFIX]

For each CASE, the open cubes come from GF3.json (gfrontier3.py at REF).  For every directory of the case
whose machine is still running (env.txt present, no README.md), model that driver's queue: the frontier at
its last "resume" record (DFS order, as close_march.py rebuilds it), followed by the children of the SPLIT
records written after that resume record, in record order (the driver appends them FIFO).  Keep the cubes
still open and reserve the first R = 0.8 * rate * minutes_left of them for that driver (rate = cubes finished
since the resume record per minute; minutes_left = env.txt start + 165 min - now).  The helpers get every
other open cube: first the cubes in no running queue, then the unreserved tails of the running queues from
their far end, interleaved.  Position p of that list goes to helper p mod K.  Prints the plan."""
import subprocess, json, sys, os, re, collections, calendar, time

REF, GF, NOW, OUT, SPEC = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5]
PREFIX = sys.argv[6] if len(sys.argv) > 6 else 'H'
B = 'cloud/es7-2026-10-19/results/'
def git(*a): return subprocess.run(['git', *a], capture_output=True, text=True).stdout
def show(p): return git('show', f'{REF}:{p}')
gf = json.load(open(GF))
files = git('ls-tree', '-r', '--name-only', REF, B + 'WAVE1', B + 'WAVE2', B + 'WAVE3', B + 'WAVE4').split()
fset = set(files)
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
    """d = results/<WAVE>/<VM>/<dir>; returns (queue of cubes in processing order, rate per min, minutes left) or None."""
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
    ri = max(i for i, r in enumerate(recs) if r.get('resume'))
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
    left = max(0.0, (start + 165 * 60 - NOW) / 60)
    return q, rate, left

plan = {}
helpers = []
for item in SPEC.split(','):
    case, k = item.split(':'); k = int(k)
    opn = [tuple(c) for c in gf[case]['open']]
    oset = set(opn)
    used = set(); tails = []; reserved_total = 0; notes = []
    for d in gf[case]['dirs']:
        rq = running_queue(d)
        if rq is None: continue
        q, rate, left = rq
        q = [tuple(c) for c in q if tuple(c) in oset and tuple(c) not in used]
        R = int(0.8 * rate * left)
        used |= set(q)
        tails.append(list(reversed(q[R:])))
        reserved_total += min(R, len(q))
        notes.append(f"{d.split('/')[1]}: queue {len(q)} rate {rate:.1f}/min left {left:.0f} min reserve {min(R, len(q))}")
    orphans = [c for c in opn if c not in used]
    merged = list(orphans)
    for i in range(max((len(t) for t in tails), default=0)):
        for t in tails:
            if i < len(t): merged.append(t[i])
    assert len(set(merged)) == len(merged)
    for j in range(k):
        name = f'{PREFIX}{len(helpers) + 1:02d}'
        part = [list(c) for c in merged[j::k]]
        helpers.append((name, case, part))
    plan[case] = {'open': len(opn), 'orphans': len(orphans), 'reserved_for_running': reserved_total,
                  'to_helpers': len(merged), 'helpers': k, 'running': notes}
    print(case, json.dumps(plan[case]))
os.makedirs(OUT, exist_ok=True)
for name, case, part in helpers:
    json.dump({case: part}, open(os.path.join(OUT, f'{name}.json'), 'w'))
    depth = collections.Counter(len(c) for c in part)
    print(name, case, len(part), dict(sorted(depth.items())))
json.dump(plan, open(os.path.join(OUT, 'plan.json'), 'w'), indent=1)
