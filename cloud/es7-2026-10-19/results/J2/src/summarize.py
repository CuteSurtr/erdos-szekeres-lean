#!/usr/bin/env python3
"""Summarize J2 logs (run from results/J2): per-generation tables and equal-CPU comparisons.
Writes summary.json and prints markdown tables."""
import json


def jl(p):
    try:
        return [json.loads(l) for l in open(p)]
    except FileNotFoundError:
        return []


def cpu(r):
    return r['cpu_self'] + r['cpu_children']


out = {}
v1 = jl('logs/v1/pb/generations.jsonl')
br = jl('logs/v1/base_random/timeline.jsonl')
bs = jl('logs/v1/base_seeds/timeline.jsonl')
print('### v1: unconditional generation (transformer) vs baselines\n')
print('| gen | CPU s | decoded E7 median | E7 after LS: min / q10 / median | E7<=1 | loss |')
print('|---|---|---|---|---|---|')
for r in v1:
    print('| %d | %.0f | %.0f | %d / %.0f / %.0f | %d | %.3f |' % (r['gen'], cpu(r), r['decoded_E7_med'], r['E7_min'],
                                                          r['E7_q10'], r['E7_med'], r['n_le1'], r['loss']))


def at_cpu(tl, c):
    best = None
    for r in tl:
        if r['cpu'] <= c:
            best = r
    return best


c_end = cpu(v1[-1]) if v1 else 0
print('\nEqual-CPU comparison at %.0f CPU s (v1 total):\n' % c_end)
print('| arm | starts | E7 min | E7<=1 found | distinct order types with E7<=1 |')
print('|---|---|---|---|---|')
print('| PatternBoost v1 | %d | %d | %d | %d |' % (sum(r['n'] for r in v1), min(r['E7_min'] for r in v1),
                                                sum(r['n_le1'] for r in v1), sum(r['distinct_ot_le1'] for r in v1)))
for name, tl in (('random starts', br), ('seeds + encoding noise (no model)', bs)):
    r = at_cpu(tl, c_end) or tl[-1]
    print('| %s (at %.0f CPU s) | %d | %d | %d | %d |' % (name, r['cpu'], r['starts'], r['E7_min_so_far'], r['n_le1_total'],
                                                         r['distinct_ot_le1']))
out['v1'] = dict(pb=v1, base_random_last=br[-1] if br else None, base_seeds_last=bs[-1] if bs else None)

arms = {a: jl('logs/%s/generations.jsonl' % a) for a in ('v2_gpt', 'v2_unigram')}
for a, g in arms.items():
    print('\n### %s\n' % a)
    print('| gen | CPU s | decoded E7 median | decoded E7<=1 | E7 min / median after LS | E7 hist 0/1/2/3 | E7<=1 (distinct OT) | pool new OT | best c6 (E7=1) |')
    print('|---|---|---|---|---|---|---|---|---|')
    for r in g:
        h = r['E7_hist']
        print('| %d | %.0f | %.0f | %d | %d / %.0f | %s/%s/%s/%s | %d (%d) | %d | %d |' % (
            r['gen'], cpu(r), r['decoded_E7_med'], r['decoded_le1'], r['E7_min'], r['E7_med'], h['0'], h['1'], h['2'], h['3'],
            r['n_le1'], r['distinct_ot_le1'], r['pool_new_vs_seeds'], r['pool_top_c6'][0]))
if all(arms.values()):
    c = min(cpu(arms[a][-1]) for a in arms)
    print('\nEqual-CPU comparison at %.0f CPU s:\n' % c)
    print('| arm | generations | samples | E7<=1 per 1000 samples | new order types with E7<=1 in pool | best c6 among E7=1 | E7=0 |')
    print('|---|---|---|---|---|---|---|')
    eq = {}
    for a, g in arms.items():
        gg = [r for r in g if cpu(r) <= c + 1]
        s = sum(r['n'] for r in gg)
        le1 = sum(r['n_le1'] for r in gg)
        eq[a] = dict(gens=len(gg), samples=s, le1=le1, pool_new=gg[-1]['pool_new_vs_seeds'], c6=gg[-1]['pool_top_c6'][0],
                     zero=sum(r['E7_hist']['0'] for r in gg))
        print('| %s | %d | %d | %.1f | %d | %d | %d |' % (a, len(gg), s, 1000.0 * le1 / s, eq[a]['pool_new'], eq[a]['c6'],
                                                         eq[a]['zero']))
    out['v2_equal_cpu'] = dict(cpu=c, arms=eq)
out['v2'] = arms
json.dump(out, open('summary.json', 'w'), indent=1)
