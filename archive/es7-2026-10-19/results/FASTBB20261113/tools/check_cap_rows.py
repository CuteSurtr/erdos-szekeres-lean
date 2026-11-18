#!/usr/bin/env python3
"""Semantic check of a capacity extra-row file (track G2): exactly one row is h(F) >= 84 - C (F = the 84 states with
f1 >= 5) and every other row has demand 1 and a support carrying a cake_lpr 's VERIFIED UNSAT' record in one of the
given certified files.   Usage: check_cap_rows.py EXTRA.json C CERTFILE [CERTFILE ...]"""
import gzip, hashlib, json, sys

SRC = '/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'


def main():
    extra, C, files = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
    states = json.load(gzip.open(SRC))['states']
    F = sorted(i for i, s in enumerate(states) if s[0] >= 5)
    rows = json.load(open(extra))
    cert = set()
    for f in files:
        if f.endswith('.jsonl'):
            for line in open(f):
                r = json.loads(line)
                if r.get('verdict') == 's VERIFIED UNSAT':
                    cert.add(tuple(sorted(r['support'])))
        else:
            for r in json.load(open(f)):
                if r.get('cnf_sha256'):
                    cert.add(tuple(sorted(r['support'])))
    caps = [k for k, r in enumerate(rows) if sorted(r['support']) == F]
    ok_cap = len(caps) == 1 and rows[caps[0]]['rhs'] == 84 - C
    others = [r for k, r in enumerate(rows) if k not in caps]
    bad = [r['support'] for r in others if r['rhs'] != 1 or tuple(sorted(r['support'])) not in cert]
    out = {'extra': extra, 'sha256': hashlib.sha256(open(extra, 'rb').read()).hexdigest(), 'rows': len(rows),
           'capacity_row_index': caps, 'capacity_row_ok': ok_cap, 'coupled_rows': len(others), 'uncertified': len(bad),
           'ok': ok_cap and not bad}
    print(json.dumps(out))
    sys.exit(0 if out['ok'] else 1)


if __name__ == '__main__':
    main()
