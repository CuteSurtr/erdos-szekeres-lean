import sys, json, collections
recs = [json.loads(l) for f in sys.argv[1:] for l in open(f)]
acc = [r for r in recs if not r['status'].startswith('reject')]
rej = collections.Counter((r['kind'], r['status']) for r in recs if r['status'].startswith('reject'))
print("accepted sets:", len(acc), "rejected (not in general position / axis on hull):", dict(rej))
by = collections.defaultdict(collections.Counter)
for r in acc:
    k = r['kind'] + ('/' + r['sub'] if r.get('sub') else '')
    by[k]['n'] += 1; by[k]['fail'] += r['status'] == 'FAIL'
    by[k]['hull<=6'] += r['hull_size'] <= 6; by[k]['hull>=8'] += r['hull_size'] >= 8
    by[k]['yflip'] += r['yflip']; by[k]['heptagon'] += r['heptagon']
    if 'angular_check' in r: by[k]['angular_checked'] += 1
for k in sorted(by): print(f"{k:22s}", dict(by[k]))
cases = collections.Counter(r['case'] for r in acc if r.get('case'))
print("distinct cases hit:", len(cases), " 4-gon cases hit:", sum(1 for c in cases if c.count('-') == 0 and (c.startswith('U_') or c.endswith('_L')) ), )
print("hull size distribution:", dict(collections.Counter(r['hull_size'] for r in acc)))
print("FAILURES:", [r for r in acc if r['status'] == 'FAIL'])
import itertools
P = range(2, 17); allc = set()
for a in P:
    allc |= {f"U{a}_L", f"U_L{a}"}
    for b in P:
        if a < b: allc |= {f"U{a}-{b}_L", f"U_L{a}-{b}"}
        if a != b: allc.add(f"U{a}_L{b}")
print("cases never hit:", len(allc - set(cases)))
print("never-hit cases containing -X(1,2,3) (U2.. or L3.. pairs; vacuous under the y-flip):",
      len([c for c in allc - set(cases) if ('U2' in c.split('_')[0].split('-')[0] or c.split('_')[1].split('-')[0] == 'L3' or c.split('_')[1] == 'L3')]))
