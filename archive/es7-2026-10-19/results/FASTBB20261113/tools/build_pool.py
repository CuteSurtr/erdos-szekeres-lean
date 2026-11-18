#!/usr/bin/env python3
"""Row pool for the slice trees (track G2, phase 2, 13 Nov 2026).

Union of the cake_lpr-verified demand-one coupled rows of the given certified.jsonl files (read-only),
in a STABLE order: file order of the first file, then rows first seen in the second file, and so on.

A support is kept only if
  (a) at least one record for it carries the verdict "s VERIFIED UNSAT" (cake_lpr's line), and
  (b) its support matches the record: the coupled CNF regenerated from the support by the unchanged encoder
      (killtools/coupled.py, byte-identical to res33's except for work paths) has exactly the SHA-256 that the
      verified record states (cnf_sha256), so the verdict is for the CNF of this very support.
Every row that fails (a) or (b) is listed in the manifest and left out.

Usage: build_pool.py OUT_POOL.json OUT_MANIFEST.json certified1.jsonl [certified2.jsonl ...]
"""
import hashlib, json, os, sys, time

KILL = '/home/jay/research/data/fastbb-20261113/killtools'
sys.path.insert(0, KILL)


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def main():
    out_pool, out_man, files = sys.argv[1], sys.argv[2], sys.argv[3:]
    import coupled
    order, recs = [], {}
    inputs = []
    for f in files:
        inputs.append({'file': f, 'sha256': sha(f), 'lines': sum(1 for _ in open(f))})
        for line in open(f):
            try:
                r = json.loads(line)
            except Exception:
                continue
            s = tuple(sorted(r['support']))
            if s not in recs:
                recs[s] = []
                order.append(s)
            recs[s].append({'file': os.path.basename(os.path.dirname(f)) + '/' + os.path.basename(f),
                            'verdict': r.get('verdict'), 'cnf_sha256': r.get('cnf_sha256'),
                            'lrat_sha256': r.get('lrat_sha256')})
    pool, rejected = [], []
    t0 = time.time()
    for k, s in enumerate(order):
        ver = [x for x in recs[s] if x['verdict'] == 's VERIFIED UNSAT']
        if not ver:
            rejected.append({'support': list(s), 'why': 'no verified record'})
            continue
        txt = coupled.CNF(list(s)).dimacs()
        h = hashlib.sha256(txt.encode()).hexdigest()
        good = [x for x in ver if x['cnf_sha256'] == h]
        if not good:
            rejected.append({'support': list(s), 'why': 'regenerated CNF hash differs', 'regenerated': h})
            continue
        pool.append({'support': list(s), 'rhs': 1, 'cnf_sha256': h, 'lrat_sha256': good[0]['lrat_sha256'],
                     'record': good[0]['file']})
        if (k + 1) % 50 == 0:
            print(json.dumps({'done': k + 1, 'of': len(order), 'kept': len(pool), 'seconds': round(time.time() - t0)}), flush=True)
    tmp = out_pool + '.tmp'
    json.dump(pool, open(tmp, 'w'))
    os.replace(tmp, out_pool)
    man = {'inputs': inputs, 'distinct_supports': len(order), 'kept': len(pool), 'rejected': rejected,
           'pool_file': out_pool, 'pool_sha256': sha(out_pool),
           'encoder': os.path.join(KILL, 'coupled.py'), 'encoder_sha256': sha(os.path.join(KILL, 'coupled.py')),
           'check': 'verdict "s VERIFIED UNSAT" and sha256(coupled.CNF(support).dimacs()) == recorded cnf_sha256',
           'seconds': round(time.time() - t0, 1), 'finished': time.strftime('%F %T')}
    json.dump(man, open(out_man, 'w'), indent=1)
    print(json.dumps({k: v for k, v in man.items() if k != 'rejected'} | {'rejected': len(rejected)}))


if __name__ == '__main__':
    main()
