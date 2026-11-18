#!/usr/bin/env python3
"""witness_kill.py of phase 1 (FASTBB20261113/tools) with one addition (track G2, phase 2): the transported images of
NEW cores found by probing are persisted in KILLDIR/newrows_g2.json and are part of the pooled candidates of later
calls, so a later witness of the same kind is killed by certifying pooled rows instead of probing again.
Nothing else changes: a row is appended to EXTRA.json only after its own coupled CNF was solved by CaDiCaL (--lrat)
and cake_lpr printed "s VERIFIED UNSAT" (certify.certify in KILLDIR), recorded in KILLDIR/certified.jsonl.

Usage: witness_kill2.py KILLDIR EXTRA.json OUTDIR      (exit 0: every witness refuted; 1: STUCK)
"""
import glob, json, os, random, sys


def main():
    killdir, extra_path, outdir = os.path.abspath(sys.argv[1]), sys.argv[2], sys.argv[3]
    sys.path.insert(0, killdir)
    from common import N, ROWS
    import certify, coupled, shrink_tests
    from probe_vec import candidates, minimize
    extra = json.load(open(extra_path))
    have = {tuple(sorted(r['support'])) for r in extra}
    pool = [r['support'] for r in json.load(open(os.path.join(killdir, 'newrows.json')))]
    fp = os.path.join(killdir, 'fnewrows.json')
    if os.path.exists(fp):
        pool += [r['support'] for r in json.load(open(fp))]
    gp = os.path.join(killdir, 'newrows_g2.json')
    g2 = json.load(open(gp)) if os.path.exists(gp) else []
    pool += [r['support'] for r in g2]

    def cert(S):
        S = sorted(S)
        r = certify.certify(S)
        with open(os.path.join(killdir, 'certified.jsonl'), 'a') as f:
            f.write(json.dumps(r) + '\n')
        return r['verdict'] == 's VERIFIED UNSAT'

    def refuted(H):
        hs = set(H)
        return len(hs) > 33 or 0 in hs or any(len(hs & set(s)) < d for s, d in ROWS) or \
            any(len(hs & set(r['support'])) < r['rhs'] for r in extra)

    files = sorted(set(glob.glob(os.path.join(outdir, 'WITNESS.json')) + glob.glob(os.path.join(outdir, 'witness-ctx-*.json'))))
    stuck = 0
    for wf in files:
        H = json.load(open(wf))['holes']
        if refuted(H):
            print(json.dumps({'file': os.path.basename(wf), 'status': 'already_refuted'}), flush=True)
            continue
        occ = set(range(N)) - set(H)
        viol = [S for S in pool if set(S) <= occ]
        new = []
        for S in viol[:12]:
            if tuple(sorted(S)) in have or cert(S):
                new.append(sorted(S))
        how = 'pooled'
        transported = 0
        if not new:
            how = 'probe'
            cands, nf = candidates(H, [(tuple(s), d) for s, d in ROWS], random.Random(sum(H)), limit=2500)
            found = []
            for S in cands:
                if coupled.fast_solve(S, seconds=30) == 'unsat':
                    found.append(S)
                    if len(found) >= 4:
                        break
            for core in {tuple(sorted(minimize(S))) for S in found}:
                if cert(list(core)):
                    new.append(list(core))
                try:
                    tr = shrink_tests.run(list(core), transport_seconds=60)
                    if tr:
                        sups = [sorted(s) for s in tr['supports']]
                        pool += sups
                        g2 += [{'support': s, 'kind': 'transport', 'core': sorted(core)} for s in sups]
                        transported += len(sups)
                except Exception as e:  # transport is optional
                    print(json.dumps({'transport_error': repr(e)}), flush=True)
            if transported:
                tmp = gp + f'.{os.getpid()}'
                json.dump(g2, open(tmp, 'w'), separators=(',', ':'))
                os.replace(tmp, gp)
        added = 0
        for S in new:
            if tuple(S) not in have:
                extra.append({'support': S, 'rhs': 1}); have.add(tuple(S)); added += 1
        ok = refuted(H)
        print(json.dumps({'file': os.path.basename(wf), 'status': 'killed' if ok else 'STUCK', 'how': how,
                          'pooled_violations': len(viol), 'rows_appended': added, 'transported_saved': transported,
                          'holes': H}), flush=True)
        stuck += not ok
    tmp = extra_path + '.tmp'
    json.dump(extra, open(tmp, 'w'))
    os.replace(tmp, extra_path)
    print(json.dumps({'extra_rows': len(extra), 'stuck': stuck}))
    sys.exit(1 if stuck else 0)


if __name__ == '__main__':
    main()
