#!/usr/bin/env python3
"""Summarise ext_solve outputs.

usage: summarize.py main OUTDIR SIGFILE M OUT.json [PER_SET.tsv]
       summarize.py nbhd OUTDIR OUT.json
main : per-set SAT/UNSAT/UNKNOWN counts over positions 1..M; every set must have exactly M answers.
nbhd : counts per deletion set (label) and per R.
"""
import json
import sys
from collections import Counter, defaultdict
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigutil import parse_outputs  # noqa: E402


def stats(vals):
    vals = sorted(vals)
    if not vals:
        return {}
    q = lambda f: vals[min(len(vals) - 1, int(f * len(vals)))]
    return {"n": len(vals), "mean": round(sum(vals) / len(vals), 3), "median": q(0.5), "p99": q(0.99), "max": vals[-1]}


def main_mode(outdir, sigfile, M, out, tsv=None):
    meta = {}
    for l in open(sigfile):
        t = l.split()
        meta[t[0]] = (t[1], t[2], t[3])
    per = defaultdict(dict)
    conf, ms = [], []
    sat = []
    for rec in parse_outputs(outdir):
        if rec[0] == 'R':
            _, lab, tag, st, c, d, t = rec
            assert tag not in per[lab], (lab, tag)
            per[lab][tag] = st
            conf.append(c)
            ms.append(t)
        else:
            sat.append((rec[1], rec[2]))
    missing = [s for s in meta if len(per.get(s, {})) != M]
    tot = Counter()
    saturated = 0
    by_tag = defaultdict(Counter)
    rows = []
    for s, (tg, lab, h) in meta.items():
        c = Counter(per[s].values())
        tot.update(c)
        full = c.get('UNSAT', 0) == M
        saturated += full
        by_tag[tg]['sets'] += 1
        by_tag[tg]['abstractly_saturated'] += full
        for k, v in c.items():
            by_tag[tg][k] += v
        rows.append((s, tg, lab, h, c.get('SAT', 0), c.get('UNSAT', 0), c.get('UNKNOWN', 0)))
    res = {"sets": len(meta), "positions_per_set": M, "answers": sum(tot.values()), "status_totals": dict(tot),
           "sets_missing_answers": missing, "abstractly_saturated_sets": saturated,
           "by_source_tag": {k: dict(v) for k, v in sorted(by_tag.items())},
           "sat_answers": [{"set": a, "tag": b} for a, b in sat],
           "conflicts_per_solve": stats(conf), "wall_ms_per_solve": stats(ms)}
    json.dump(res, open(out, 'w'), indent=1)
    if tsv:
        with open(tsv, 'w') as f:
            f.write("id\tsource\tlabel\thash\tSAT\tUNSAT\tUNKNOWN\n")
            for r in rows:
                f.write("\t".join(map(str, r)) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k not in ('by_source_tag', 'sat_answers')}))


def nbhd_mode(outdir, out):
    per = defaultdict(Counter)
    conf, ms = [], []
    sat = []
    for rec in parse_outputs(outdir):
        if rec[0] == 'R':
            per[rec[1]][rec[3]] += 1
            conf.append(rec[4])
            ms.append(rec[6])
        else:
            sat.append((rec[1], rec[2]))
    tot = Counter()
    kinds = defaultdict(Counter)
    sets = set()
    for lab, c in per.items():
        tot.update(c)
        kinds[lab.split('_')[-2]].update(c)
        sets.add(lab.rsplit('_', 2)[0])
    res = {"deletion_sets": len(per), "base_sets": len(sets), "answers": sum(tot.values()), "status_totals": dict(tot),
           "by_kind": {k: dict(v) for k, v in kinds.items()},
           "sat_answers": [{"label": a, "tag": b} for a, b in sat],
           "conflicts_per_solve": stats(conf), "wall_ms_per_solve": stats(ms)}
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'sat_answers'}))


if __name__ == '__main__':
    if sys.argv[1] == 'main':
        main_mode(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], sys.argv[6] if len(sys.argv) > 6 else None)
    else:
        nbhd_mode(sys.argv[2], sys.argv[3])
