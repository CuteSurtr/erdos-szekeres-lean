# Reviewer's own check of the s35_20 pre-pass against the independent T7 record (fresh full replay, 18 Nov).
# Mode "json": prepass.json / skeleton.json vs T7 contexts.jsonl + summary.json (seconds).
# Mode "gz": my own sha256 of every ctx-*.json.gz vs T7, and my own streamed type count of the listed contexts.
import json, hashlib, sys, zlib, os, re, time
G = '/home/jay/research/data/formalize-20261122/s3520-gate'
S = '/home/jay/research/data/es308-20261114/runs/b35s20/bb-s1'
A = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113/budget34/audit/fresh-b35s20-v169-bbs1'
t7 = {}
for line in open(A + '/contexts.jsonl'):
    d = json.loads(line); t7[d['context']] = d
summ = json.load(open(A + '/summary.json'))
master = json.load(open(S + '/master.json'))
ids = sorted(nd['context'] for nd in master['nodes'] if nd['type'] == 'context')
mode = sys.argv[1]
if mode == 'json':
    pp = json.load(open(G + '/export/3520/prepass.json')); sk = json.load(open(G + '/export/3520/skeleton.json'))
    bad = []
    assert sorted(t7) == ids, 'T7 context ids differ from the master placeholders'
    for k in ids:
        L, H, B = pp['leaves'][str(k)], pp['gz_sha256'][str(k)], pp['branches'][str(k)]
        d = t7[k]
        if (L, H, L + B) != (d['leaves'], d['sha256'], d['nodes']) or L != B + 1 or d['minimum_margin'] < 1: bad.append(k)
    ctx_leaves = sum(t7[k]['leaves'] for k in ids)
    ml = sum(1 for nd in master['nodes'] if nd['type'] not in ('branch', 'context'))
    dig = hashlib.sha256(''.join(f'{k} {t7[k]["sha256"]}\n' for k in ids).encode()).hexdigest()
    print('contexts', len(ids), 'T7', len(t7), 'summary contexts', summ['contexts'], '| prepass mismatches vs T7:', len(bad), bad[:5])
    print('T7 context leaves', ctx_leaves, '+ master leaves', ml, '=', ctx_leaves + ml, '| T7 summary leaves', summ['leaves'],
          '(includes the pending state-0-missing leaf:', summ['global_pending'], ') | skeleton total_leaves', sk['total_leaves'])
    print('T7 nodes: sum(context nodes)', sum(t7[k]['nodes'] for k in ids), '+ master nodes', len(master['nodes']), '- placeholders', len(ids),
          '=', sum(t7[k]['nodes'] for k in ids) + len(master['nodes']) - len(ids), '| summary nodes', summ['nodes'])
    print('contexts digest from T7 hashes', dig, '| skeleton', sk['contexts_digest'], '| prepass', pp['contexts_digest'])
    tops = sk['tops']; print('skeleton: units', len(tops), 'example top', {k: v for k, v in tops[2080].items() if k != 'path'} if isinstance(tops[2080], dict) else tops[2080])
    if isinstance(tops[0], dict) and 'leaves' in tops[0]:
        print('sum of unit leaves', sum(t['leaves'] for t in tops))
elif mode == 'gz':
    t0 = time.time(); bad = []
    for k in ids:
        h = hashlib.sha256()
        with open(f'{S}/ctx-{k}.json.gz', 'rb') as f:
            for blk in iter(lambda: f.read(1 << 22), b''): h.update(blk)
        if h.hexdigest() != t7[k]['sha256']: bad.append(k)
    print(f'gz sha256 of {len(ids)} context files vs T7: {len(bad)} mismatches {bad[:5]} ({time.time()-t0:.0f} s)', flush=True)
    pat = re.compile(rb'"type":"([a-z_]+)"')
    for k in map(int, sys.argv[2].split(',')):
        t0 = time.time(); z = zlib.decompressobj(16 + zlib.MAX_WBITS); cnt = {}; tail = b''
        with open(f'{S}/ctx-{k}.json.gz', 'rb') as f:
            for blk in iter(lambda: f.read(1 << 20), b''):
                buf = tail + z.decompress(blk)
                cut = max(0, len(buf) - 40)            # a token is < 40 bytes; count only matches that start before cut
                for mt in pat.finditer(buf):
                    if mt.start() < cut: cnt[mt.group(1).decode()] = cnt.get(mt.group(1).decode(), 0) + 1
                tail = buf[cut:]
            buf = tail + z.flush()
            for mt in pat.finditer(buf): cnt[mt.group(1).decode()] = cnt.get(mt.group(1).decode(), 0) + 1
        lv = sum(v for t, v in cnt.items() if t != 'branch')
        print(f'ctx-{k}: types {cnt}; leaves {lv}, nodes {sum(cnt.values())}; T7 leaves {t7[k]["leaves"]} nodes {t7[k]["nodes"]}; '
              f'equal: {lv == t7[k]["leaves"] and sum(cnt.values()) == t7[k]["nodes"]} ({time.time()-t0:.0f} s)', flush=True)
