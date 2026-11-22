#!/usr/bin/env python3
"""Bind every hypothesis of Res118 to its evidence files by sha256 (read-only; res118-lean, 22 Nov 2026).

Slices: packet master.json / contexts.json sha256, number of ctx files, the replay summary (label, counts,
extra/master sha256 equal to the packet), and a spot check of three ctx files against the replay receipts.
Blocks: P = inputs/pool812.json (order), certification summaries (sha256 and counts). Writes data/evidence.json.
"""
import hashlib, json, sys
from pathlib import Path

W = Path('/home/jay/research/data/es308-20261114')
REC = Path('/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results')
AUD = REC / 'LO33N20261113/budget34/audit'
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

out = {'slices': {}, 'blocks': {}}
PK = {  # slice: (packet, input folder, replay summary, replay receipts, receipt sha field)
    'b34s18': ('runs/s18/bb', 'inputs/s18-v13', AUD / 'fresh-s18-v13/summary.json', AUD / 'fresh-s18-v13/contexts.jsonl', 'sha256'),
    'b34s19': ('runs/s19/bb', 'inputs/s19', AUD / 's19-summary.json', AUD / 's19-contexts.jsonl', 'context_sha256'),
    'b35s18': ('runs/b35s18/bb', 'inputs/b35s18-v13', AUD / 'fresh-b35s18-v13/summary.json', AUD / 'fresh-b35s18-v13/contexts.jsonl', 'sha256'),
    'b35s19': ('runs/b35s19/bb', 'inputs/b35s19-v16', AUD / 'fresh-b35s19-v16/summary.json', AUD / 'fresh-b35s19-v16/contexts.jsonl', 'sha256'),
    'b35s20': ('runs/b35s20/bb-s1', 'inputs/b35s20-v169', AUD / 'fresh-b35s20-v169-bbs1/summary.json', AUD / 'fresh-b35s20-v169-bbs1/contexts.jsonl', 'sha256'),
}
for k, (pk, inp, summ, rec, fld) in PK.items():
    P = W / pk
    m = P / 'master.json'
    mj = json.loads(m.read_text())
    ctx = sorted(P.glob('ctx-*.json.gz'))
    s = json.loads(summ.read_text())
    r = {'packet': str(P), 'master_sha256': sha(m), 'contexts_json_sha256': sha(P / 'contexts.json'),
         'ctx_files': len(ctx), 'master_contexts': mj['contexts'], 'master_budget': mj['budget'],
         'master_extra': mj['extra'], 'extra_sha256': sha(W / inp / 'extra.json'),
         'replay_summary': str(summ), 'replay_summary_sha256': sha(summ), 'replay_receipts_sha256': sha(rec),
         'replay_label': s.get('label'), 'replay_nodes': s.get('nodes'), 'replay_leaves': s.get('leaves'),
         'replay_min_margin': s.get('minimum_margin'), 'replay_global_pending': s.get('global_pending')}
    if 'master_sha256' in s:
        r['replay_master_sha256_equal'] = s['master_sha256'] == r['master_sha256']
    if 'extra_sha256' in s:
        r['replay_extra_sha256_equal'] = s['extra_sha256'] == r['extra_sha256']
    if 'input_sha256' in s:
        r['replay_extra_sha256_equal'] = s['input_sha256'].get(str(W / inp / 'extra.json')) == r['extra_sha256']
    lines = [json.loads(x) for x in rec.read_text().splitlines() if x.strip()]
    r['receipt_contexts'] = len(lines)
    picks = [lines[0], lines[len(lines) // 2], lines[-1]]
    spot = []
    for x in picks:
        f = P / f"ctx-{x['context']}.json.gz"
        spot.append({'context': x['context'], 'equal': sha(f) == x[fld]})
    r['spot_check'] = spot
    out['slices'][k] = r
L = REC / 'LO33N20261113'
lr = {'repo_dir': str(L / 'data/cert_66_55_leanrows'), 'work_dir': '/home/jay/research/data/lo33-20261113/cert_66_55_leanrows'}
for f in ('contexts_66_55_leanrows.tar', 'extra_66_55_leanrows.json', 'verify_stream.out'):
    a, b = sha(L / 'data/cert_66_55_leanrows' / f), sha(Path(lr['work_dir']) / f)
    lr[f] = {'sha256': a, 'work_copy_equal': a == b}
lr['verify_stream_out'] = (L / 'data/cert_66_55_leanrows/verify_stream.out').read_text()
out['slices']['b33s18'] = lr
pool = json.loads((W / 'inputs/pool812.json').read_text())
s19 = json.loads((W / 'inputs/s19/extra.json').read_text())[2:]
def supp(x):
    return x['support'] if isinstance(x, dict) else x
out['blocks']['P_equals_pool812_in_order'] = [supp(x) for x in pool] == [x['support'] for x in s19]
out['blocks']['pool812_sha256'] = sha(W / 'inputs/pool812.json')
for name, p in {'pool_summary': AUD / 'pool_summary.json',
                'es307_t4_v169': REC / 'ES307N20261118/data/lrat_recheck_v169_summary.json',
                'verify307_t4_b35s19_v16': REC / 'LO33N20261113/budget34/VERIFY307/data/lrat-b35s19-v16/lrat-summary.json',
                'pool_inventory': AUD / 'pool_inventory.json'}.items():
    d = json.loads(p.read_text())
    keep = {k: d[k] for k in ('status', 'rows', 'rows_certified', 'jobs', 'job_status_counts', 'rows_not_certified',
                              'sha_mismatch_jobs', 'rejected_jobs', 'accepted_retained_lrats',
                              'independently_reconstructed_cnfs') if isinstance(d, dict) and k in d}
    out['blocks'][name] = {'path': str(p), 'sha256': sha(p), **keep}
json.dump(out, open(sys.argv[1], 'w'), indent=1)
bad = [k for k, v in out['slices'].items() if k != 'b33s18' and not (all(x['equal'] for x in v['spot_check'])
       and v.get('replay_extra_sha256_equal', True) and v.get('replay_master_sha256_equal', True)
       and v['ctx_files'] == v['master_contexts'] == v['receipt_contexts'])]
print('problems:', bad, ' P==pool812:', out['blocks']['P_equals_pool812_in_order'])
