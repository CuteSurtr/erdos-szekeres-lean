"""summarize.py - distributions of final counts from runs/*_runs.tsv. usage: summarize.py runs_dir"""
import sys, glob, os, collections
tot_s, tot_f = collections.Counter(), collections.Counter()
for fn in sorted(glob.glob(os.path.join(sys.argv[1], '*_runs.tsv'))):
    hdr = open(fn).readline().strip(); rows = [l.split('\t') for l in open(fn) if not l.startswith('#') and l.strip()]
    if not rows: continue
    s = collections.Counter(int(r[4]) for r in rows); f = collections.Counter(int(r[7]) for r in rows)
    ev = sum(int(r[9]) for r in rows); secs = sum(float(r[10]) for r in rows)
    print(f"{os.path.basename(fn)} {hdr} R={rows[0][1]} restarts={len(rows)} evals={ev} cpu_s={secs:.0f}")
    print("  symmetric-phase best c7:", dict(sorted(s.items())))
    print("  after free phase best c7:", dict(sorted(f.items())))
    print("  restarts where free phase improved:", sum(1 for r in rows if int(r[7]) < int(r[4])))
    if 'S1 0' not in hdr: tot_s += s; tot_f += f
print("ALL random-start restarts: symmetric best", dict(sorted(tot_s.items())))
print("ALL random-start restarts: free best", dict(sorted(tot_f.items())))
