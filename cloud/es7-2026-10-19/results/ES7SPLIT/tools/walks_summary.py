#!/usr/bin/env python3
"""Summary of logs/walks_analysis.jsonl (produces logs/walks_summary.txt).

This is the inline code that wrote the summary, saved as a script.
Usage: python3 tools/walks_summary.py [logs/walks_analysis.jsonl]
"""
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
fn = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "logs", "walks_analysis.jsonl")
recs = [json.loads(l) for l in open(fn)]
print("distinct order types (up to reflection):", len(recs))
print("all general position:", all(r['general_position'] for r in recs), "; largest convex subset:", dict(Counter(r['gon'] for r in recs)))
print("hull sizes:", dict(Counter(r['hull'] for r in recs)))
print("number of layers:", dict(Counter(len(r['layers']) for r in recs)))
print("sets with a nontrivial z-split:", [(r['file'], r['tag'], r['split_types']) for r in recs if r['n_splits'] > 0])
print("every hull vertex has a v-5-cap in S\\{v}:", all(all(c == 5 for c, u in r['vframe']) for r in recs))
print("every hull vertex has a v-6-cup in S\\{v}:", all(all(u == 6 for c, u in r['vframe']) for r in recs))
hx = [r for r in recs if r['ears'] is not None]
print("hexagonal-hull sets:", len(hx), "; all ears nested:", all(all(n for c, n in r['ears']) for r in hx), "; ear sizes:", [[c for c, n in r['ears']] for r in hx])
print("six-layer sets:", [(r['file'], r['layers']) for r in recs if len(r['layers']) == 6])
byfile = defaultdict(list)
for r in recs: byfile[r['file']].append(r)
for f, rs in byfile.items():
    print(f, len(rs), "hull", dict(Counter(r['hull'] for r in rs)), "layers", dict(Counter(len(r['layers']) for r in rs)))
