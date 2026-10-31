#!/usr/bin/env python3
"""Summarize N2 runs: runs/<method>/<start>.json -> summary.json and a markdown table."""
import json, glob, os, statistics as st, sys
R = sys.argv[1] if len(sys.argv) > 1 else 'runs'
rows = []
for fn in sorted(glob.glob(f'{R}/*/*.json')):
    try: d = json.load(open(fn))
    except Exception: continue
    d['start'] = os.path.basename(fn)[:-5]
    d['family'] = 'near-miss' if d['start'].startswith('nm_') else d['start'].rsplit('_', 1)[0]
    rows.append(d)
def agg(rs):
    if not rs: return None
    t1 = [r['t_le1'] for r in rs if r['t_le1'] >= 0]
    return dict(runs=len(rs), cpu=round(sum(r['cpu'] for r in rs)), best_H_min=min(r['best_H'] for r in rs),
                best_H_median=st.median(r['best_H'] for r in rs), best_H_list=[r['best_H'] for r in rs],
                final_H_list=[r['final_H'] for r in rs],
                reached_le1=len(t1), t_le1_median=round(st.median(t1), 1) if t1 else None, t_le1_list=[round(x, 1) for x in t1],
                reached_zero=sum(r['t_zero'] >= 0 for r in rs), steps=sum(r['steps'] for r in rs), sweeps=sum(r['sweeps'] for r in rs),
                distinct_fp=sum(r['distinct_fp'] for r in rs), distinct_fp_per_cpu_h=round(sum(r['distinct_fp'] for r in rs) / (sum(r['cpu'] for r in rs) / 3600), 1),
                verify_mismatch=sum(r['verify_mismatch'] for r in rs), incomplete_sweeps=sum(r['incomplete_sweeps'] for r in rs),
                final_near_median=st.median(r['final_near'] for r in rs))
fams = sorted(set(r['family'] for r in rows))
S = {f: {m: agg([r for r in rows if r['family'] == f and r['method'] == m]) for m in ['tabu', 'lns', 'pen']} for f in fams}
S['all'] = {m: agg([r for r in rows if r['method'] == m]) for m in ['tabu', 'lns', 'pen']}
json.dump(dict(by_family=S, runs=rows), open('summary.json', 'w'), indent=1)
print('| family | method | runs | CPU-s | min best H | median best H | reached H<=1 | median t(H<=1) CPU-s | distinct fingerprints | per CPU-h | sweeps | mismatches |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|')
for f in fams + ['all']:
    for m in ['tabu', 'lns', 'pen']:
        a = S[f][m]
        if a: print(f"| {f} | {m} | {a['runs']} | {a['cpu']} | {a['best_H_min']} | {a['best_H_median']} | {a['reached_le1']}/{a['runs']} | {a['t_le1_median']} | {a['distinct_fp']} | {a['distinct_fp_per_cpu_h']} | {a['sweeps']} | {a['verify_mismatch']} |")
