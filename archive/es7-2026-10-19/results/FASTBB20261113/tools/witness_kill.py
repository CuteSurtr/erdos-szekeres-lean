#!/usr/bin/env python3
"""Refute the WITNESS vectors of a fastbb run with cake_lpr-certified coupled rows (as capcegar.py does)
and APPEND those rows to the extra-row file, so that the run can be resumed.

Usage: witness_kill.py KILLDIR EXTRA.json OUTDIR

KILLDIR is a private copy of the certification tools of /home/jay/research/data/res33-20261113
(common.py certify.py coupled.py probe_vec.py shrink_tests.py transport.py hfind.py static/ newrows.json
fnewrows.json certified.jsonl); this script never touches the original directory.  certify.certify()
builds the coupled CNF of a support, solves it with CaDiCaL (--lrat) and accepts the row only on
cake_lpr's "s VERIFIED UNSAT" line.

For every witness file in OUTDIR (WITNESS.json, witness-ctx-*.json):
  1. skip it if the current rows already refute it;
  2. certify up to 12 pooled transported rows that are fully occupied in it;
  3. if none exists, probe its occupied set for new coupled cores, certify them (and transport them
     into the pool);
  4. append every newly certified support (demand 1) at the END of EXTRA.json.
Exit code 0: every witness is now refuted (resume the fastbb command).  Exit code 1: STUCK on a witness
(no certified row found): the vector is then a real 33-hole solution of the current relaxation and must
be reported.
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
                        pool += [sorted(s) for s in tr['supports']]
                except Exception as e:  # transport is optional
                    print(json.dumps({'transport_error': repr(e)}), flush=True)
        added = 0
        for S in new:
            if tuple(S) not in have:
                extra.append({'support': S, 'rhs': 1}); have.add(tuple(S)); added += 1
        ok = refuted(H)
        print(json.dumps({'file': os.path.basename(wf), 'status': 'killed' if ok else 'STUCK', 'how': how,
                          'pooled_violations': len(viol), 'rows_appended': added, 'holes': H}), flush=True)
        stuck += not ok
    tmp = extra_path + '.tmp'
    json.dump(extra, open(tmp, 'w'))
    os.replace(tmp, extra_path)
    print(json.dumps({'extra_rows': len(extra), 'stuck': stuck}))
    sys.exit(1 if stuck else 0)


if __name__ == '__main__':
    main()
