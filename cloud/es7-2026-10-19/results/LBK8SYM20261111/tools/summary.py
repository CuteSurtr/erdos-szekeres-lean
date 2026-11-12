#!/usr/bin/env python3
"""Summary of all runs of the work directory (for the record): annealing statistics per (m, t, centre), phase-fixed
CEGAR result counts per run directory, long-run decisions."""
import glob, re, collections, os, json
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
stats = collections.defaultdict(lambda: [0, 0, []])
for f in sorted(glob.glob('runs/*/log_*.txt')):
    txt = open(f).read()
    m = re.search(r"'m': (\d+), 't': (\d+), 'centre': (\w+)", txt)
    if not m:
        continue
    key = (int(m.group(1)), int(m.group(2)), m.group(3) == 'True')
    for line in txt.splitlines():
        mm = re.search(r'end restart \d+ (\S+) evals (\d+) best N8 (\d+)', line)
        if mm:
            stats[key][0] += 1; stats[key][1] += int(mm.group(2)); stats[key][2].append(int(mm.group(3)))
print('== annealing (completed restarts): (m, t, centre): restarts, evaluations, best N8 values')
for k, (n, ev, b) in sorted(stats.items()):
    print('  %s: %d restarts, %.1f M evaluations, best %s' % (k, n, ev / 1e6, sorted(b)[:8]))
print('== phase-fixed CEGAR result counts per run directory')
tot = collections.Counter()
for f in sorted(glob.glob('cegar/*/res_*.tsv')):
    c = collections.Counter()
    for line in open(f):
        for x in line.rstrip('\n').split('\t'):
            if x in ('UNSAT', 'UNSAT0', 'TIMEOUT', 'CAND', 'BUDGET', 'LPFAIL', 'NODUAL', 'DEGEN'):
                c[x] += 1
    if c:
        print('  %-40s %s' % (f, dict(c)))
        tot.update(c)
print('  total', dict(tot))
print('== long runs (RESULT lines with more than one iteration)')
for f in sorted(glob.glob('cegar/*/log_*.txt')):
    for line in open(f):
        if 'RESULT' in line:
            mm = re.search(r'RESULT (\S+) K (\S+) N8\(hint\) (\d+) -> (\S+) it (\d+) best (\S+) \(([\d.]+) s\)', line)
            if mm and int(mm.group(5)) > 1:
                print('  %s %s: %s after %s rounds, best margin %s, %s s' % (f.split('/')[1], mm.group(1), mm.group(4), mm.group(5), mm.group(6), mm.group(7)))
