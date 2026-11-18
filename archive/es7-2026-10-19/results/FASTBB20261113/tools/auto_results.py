#!/usr/bin/env python3
"""Write R/FASTBB20261113/data/AUTO_RESULTS.md from the run files of the slice chain (track G2, 13-14 Nov 2026).

Called by run_chain6.sh after every step, so that results arriving after the G2 session ended (02:00 KST) are in the
record without anybody editing README.md.  It only READS the run files and copies small result files (DONE.json,
STUCK.json, replay2_compare.json, the final extra-row file, witnesses.jsonl, proofs/summary.json) into data/.
Labels: a slice is reported CLOSED (EXACT TREE) only if DONE.json says so (verify_slice.py replay complete); the
second replay is reported separately.  Nothing here is a new proof; it is a summary of the files named.
"""
import hashlib, json, os, shutil, time

P2 = '/home/jay/research/data/fastbb-20261113/p2'
R = '/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/FASTBB20261113'
D = os.path.join(R, 'data')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def load(p):
    try:
        return json.load(open(p))
    except Exception:
        return None


def main():
    lines = ['# AUTO_RESULTS: slice runs of track G2 (generated file)', '',
             f'Generated {time.strftime("%F %T")} KST by `tools/auto_results.py` from the run files in '
             '`/home/jay/research/data/fastbb-20261113/p2/runs/` (see README §8). It summarizes those files; it adds no '
             'new argument. A slice is CLOSED (EXACT TREE) only if its DONE.json says so (complete piecewise replay by '
             '`tools/verify_slice.py` with the semantic row checks); "replay 2" is the second replay by '
             '`tools/replay_split.py`.', '',
             '| slice t | pair | state | nodes | leaves | min margin | pending | contexts | extra rows | witnesses killed | rows appended | replay 2 | extra SHA-256 | contexts digest |',
             '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for T in (21, 22, 20, 23):
        sd = os.path.join(P2, 'runs', f's{T}')
        if not os.path.isdir(sd):
            lines.append(f'| {T} | ({84 - T}, {37 + T}) | not started | | | | | | | | | | | |')
            continue
        st = load(os.path.join(sd, 'status.json')) or {}
        done = load(os.path.join(sd, 'DONE.json'))
        stuck = load(os.path.join(sd, 'STUCK.json'))
        r2 = load(os.path.join(sd, 'replay2_compare.json'))
        if done:
            rp = done['replay']
            state = 'CLOSED (EXACT TREE)' if rp.get('contexts_missing') == 0 and rp.get('pending') == 1 else 'see DONE.json'
            r2s = ('agree' if r2 and r2.get('agree') else ('DISAGREE' if r2 else 'pending'))
            lines.append(f"| {T} | ({84 - T}, {37 + T}) | {state} | {rp['nodes']:,} | {rp['leaves']:,} | {rp['minimum_margin']} | "
                         f"{rp['pending']} | {rp['contexts_total']:,} | {rp['extra_rows']} | {done.get('witnesses_killed')} | "
                         f"{done.get('rows_appended')} | {r2s} | `{rp['extra_sha256']}` | `{rp['contexts_digest_sha256']}` |")
            for name in ('DONE.json', 'replay2_compare.json', 'extra.json', 'witnesses.jsonl'):
                src = os.path.join(sd, name)
                if os.path.exists(src):
                    shutil.copyfile(src, os.path.join(D, f's{T}_{name}'))
        elif stuck:
            lines.append(f"| {T} | ({84 - T}, {37 + T}) | **STUCK** (obstruction: a 33-hole vector no certified row kills) | | | | | | "
                         f"{stuck.get('extra_rows')} | {st.get('witnesses_killed')} | {st.get('rows_appended')} | | | |")
            shutil.copyfile(os.path.join(sd, 'STUCK.json'), os.path.join(D, f's{T}_STUCK.json'))
        else:
            ncl = len([f for f in os.listdir(os.path.join(sd, 'bb')) if f.startswith('ctx-') and f.endswith('.json.gz')]) if os.path.isdir(os.path.join(sd, 'bb')) else 0
            lines.append(f"| {T} | ({84 - T}, {37 + T}) | open ({st.get('state', '?')}; {ncl:,} contexts closed; updated {st.get('updated', '?')}) | | | | | | "
                         f"{st.get('extra_rows', '')} | {st.get('witnesses_killed', '')} | {st.get('rows_appended', '')} | | | |")
    ps = load(os.path.join(P2, 'proofs', 'summary.json'))
    lines += ['', '## Re-certification with kept proofs (`tools/recert_keep.py`, output `W/p2/proofs/`)', '']
    if ps:
        lines.append(f"- {ps['records_total']} rows re-certified ({ps['finished']}): {ps['verified_total']} cake_lpr `s VERIFIED UNSAT`, "
                     f"{ps['cnf_hash_matches_record_total']} regenerated CNF hashes equal to the record, "
                     f"{ps['lrat_hash_matches_record_total']} LRAT hashes equal to the record; not verified: {ps['not_verified']}; "
                     f"{ps['skipped_proof_already_kept']} rows skipped because their proofs were already kept when certified "
                     '(`W/killtools/proofs/`).')
        shutil.copyfile(os.path.join(P2, 'proofs', 'summary.json'), os.path.join(D, 'recert_summary.json'))
    else:
        lines.append('- not run yet.')
    lines += ['', 'Chain log: `W/p2/runs/chain.log`. Conclusions are drawn in README §1.5 only for slices whose state above is '
              'CLOSED (EXACT TREE); for slice 22 see README §1.5 (pair (65, 59) with the verified N66 ≤ 59).', '']
    out = os.path.join(D, 'AUTO_RESULTS.md')
    tmp = out + '.tmp'
    open(tmp, 'w').write('\n'.join(lines))
    os.replace(tmp, out)
    print('AUTO_RESULTS.md written')


if __name__ == '__main__':
    main()
