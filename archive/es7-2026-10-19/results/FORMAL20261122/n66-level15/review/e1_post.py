"""Reviewer's own post-processing of the own E1 re-run (slot lrv3). Read-only; writes review/e1_summary.json."""
import collections, json, re

RV = '/home/jay/research/data/formalize-20261122/n66-level15/review/'
W = '/home/jay/research/data/n66-20261113/'
FROZEN = '63d7fc9913fc1d80c423512470370644c62643c7ea785343ddb27426cb35a229'
cubes = json.load(open(W + 'p2/c15/campaign_status.json'))['cubes']
vfy = {e['id']: e for e in json.load(open(W + 'vfy15/summary.json'))}
lm = [l.rstrip('\n').split('\t') for l in open(RV + 'leafmap15.tsv') if l.strip()]
rows = [l.rstrip('\n').split('\t') for l in open(RV + 'e1_runs.tsv')][1:]
out = {'runs': len(rows)}
bad = []
seen = []
hashes = collections.defaultdict(list)
maxrss = 0
for r in rows:
    i, cid, exe, rc, rss, wall, ps, pb, fs, fb, c, err = r
    i = int(i)
    seen.append(i)
    v = cubes[cid]
    lits = ' '.join(f'{s}:{b}' for s, b in v['lits'])
    m = re.fullmatch(r'leaf (\d+) \[(.*)\] clauses (\d+) ?', err)
    ok = (exe == FROZEN and rc == '0' and c == '0' and ps == fs == v['trim_cnf_sha256'] == vfy[cid]['trim_cnf_sha']
          and pb == fb and int(pb) > 0 and m is not None and int(m.group(1)) == i and m.group(2) == lits
          and int(m.group(3)) == v['trim_cnf_clauses'] and lm[i][1] == cid)
    if not ok:
        bad.append(r)
    hashes[ps].append(cid)
    maxrss = max(maxrss, int(rss))
out['indices_exactly_0_to_104'] = seen == list(range(105))
out['match'] = len(rows) - len(bad)
out['bad'] = bad
out['distinct_printed_texts'] = len(hashes)
out['shared_texts'] = {h: ids for h, ids in hashes.items() if len(ids) > 1}
up = sorted(k for k, v in cubes.items() if v['status'] == 'certified' and v.get('up_refuted'))
out['up_refuted_share_one_text'] = any(sorted(ids) == up for ids in hashes.values())
out['total_bytes'] = sum(int(r[7]) for r in rows)
out['max_exe_rss_kb'] = maxrss
# exe `leaves` mode (compiled code) vs the olean dump (interpreter)
exe_leaves = [l.split(' ', 1) for l in open(RV + 'e1_exe_leaves.txt').read().splitlines() if l.strip()]
dump = [l for l in open(RV + 'dump_leaves105.txt').read().splitlines() if l.strip()]
out['exe_leaves_eq_dump'] = [int(a) for a, _ in exe_leaves] == list(range(105)) and [b for _, b in exe_leaves] == dump
out['controls'] = open(RV + 'e1_controls.txt').read().splitlines()
out['exe_hash_log'] = open(RV + 'e1_exe_hashes.txt').read().splitlines()
out['verdict'] = 'PASS' if (not bad and out['indices_exactly_0_to_104'] and out['exe_leaves_eq_dump']) else 'FAIL'
json.dump(out, open(RV + 'e1_summary.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != 'shared_texts'}, indent=1))
print('shared texts:', {h[:12]: ids for h, ids in out['shared_texts'].items()})
