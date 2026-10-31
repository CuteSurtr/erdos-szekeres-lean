#!/usr/bin/env python3
"""Markdown tables from summ2.py outputs. usage: tables.py RUN.json [RUN.json ...]"""
import json
import sys

print("| Run | r | Bases | Deletion sets | Answers | SAT | UNSAT | UNKNOWN | Conflicts mean / max | ms mean / max | Wall s |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for fn in sys.argv[1:]:
    d = json.load(open(fn))
    a, r = d["per_group"]["ALL|ALL|ALL"], d["run"]
    print(f"| {fn.split('/')[-1][:-5]} | {r['R']} | {r['bases']} | {a['deletion_sets']:,} | {a['answers']:,} | {a['SAT']} | "
          f"{a['UNSAT']:,} | {a['UNKNOWN']} | {a['conflicts_mean']} / {a['conflicts_max']:,} | {a['ms_mean']} / "
          f"{a['ms_max']:,} | {r['wall_s']} |")
print()
print("| Run | Kind | Mode | Deletion sets | Answers | SAT | UNSAT | UNKNOWN | Conflicts mean / max |")
print("|---|---|---|---|---|---|---|---|---|")
for fn in sys.argv[1:]:
    d = json.load(open(fn))
    for k, a in d["per_group"].items():
        g, kind, mode = k.split('|')
        if g == 'ALL' and kind != 'ALL':
            print(f"| {fn.split('/')[-1][:-5]} | {kind} | {mode} | {a['deletion_sets']:,} | {a['answers']:,} | {a['SAT']} | "
                  f"{a['UNSAT']:,} | {a['UNKNOWN']} | {a['conflicts_mean']} / {a['conflicts_max']:,} |")
print()
print("| Run | Source group | Deletion sets | Answers | SAT | UNKNOWN |")
print("|---|---|---|---|---|---|")
for fn in sys.argv[1:]:
    d = json.load(open(fn))
    for k, a in sorted(d["per_group"].items()):
        if k.startswith('src:'):
            print(f"| {fn.split('/')[-1][:-5]} | {k[4:].split('|')[0]} | {a['deletion_sets']:,} | {a['answers']:,} | {a['SAT']} | {a['UNKNOWN']} |")
