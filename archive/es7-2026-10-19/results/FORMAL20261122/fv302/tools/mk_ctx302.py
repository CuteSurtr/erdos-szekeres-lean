#!/usr/bin/env python3
"""FV302 (24 Nov 2026): contexts302.jsonl from the assembled budget-69 tree (zrow/b69zs54/files).

Every file is read whole: SHA-256 of the gz bytes and of the JSON, and the header fields (context, budget, path,
missing, occupied, status, root). Validated here: budget 69, status closed, root 0; path = root-first [[v, b]] with
b in {0, 1}, the first decision [0, 0] (state 0 occupied: zero side only), no vertex twice; missing/occupied equal the
path literals; the paths form one complete binary cover below the first decision: every internal node of the trie has
exactly two children (bits 0 and 1) and one branching vertex, no path is a prefix of another. ctx ids are assigned in
the order of the paths' bit strings (preorder of the trie), so siblings are adjacent.
Usage: python3 -I mk_ctx302.py FILES_DIR OUT.jsonl [--threads N]
"""
import gzip, hashlib, json, os, sys
from concurrent.futures import ProcessPoolExecutor

def one(args):
    D, name = args
    gz = open(os.path.join(D, name), 'rb').read()
    raw = gzip.decompress(gz)
    t = json.loads(raw)
    return dict(file=name, gz_sha256=hashlib.sha256(gz).hexdigest(), json_sha256=hashlib.sha256(raw).hexdigest(),
                file_k=t.get('context'), budget=t.get('budget'), status=t.get('status'), root=t.get('root'),
                path=t.get('path'), missing=t.get('missing'), occupied=t.get('occupied'), nodes=len(t.get('nodes', [])))


def main():
    D, OUT = sys.argv[1], sys.argv[2]
    T = int(sys.argv[sys.argv.index('--threads') + 1]) if '--threads' in sys.argv else 4
    names = sorted(n for n in os.listdir(D) if n.startswith('ctx-') and n.endswith('.json.gz'))
    with ProcessPoolExecutor(T) as ex: recs = list(ex.map(one, [(D, n) for n in names], chunksize=32))
    bad = []
    for r in recs:
        p = r['path']
        ok = (r['budget'] == 69 and r['status'] == 'closed' and r['root'] == 0 and isinstance(p, list) and len(p) >= 2
              and p[0] == [0, 0] and all(isinstance(x, list) and len(x) == 2 and x[1] in (0, 1) and 0 <= x[0] < 252 for x in p)
              and len({v for v, _ in p}) == len(p)
              and sorted(r['missing']) == sorted(v for v, b in p if b == 1)
              and sorted(r['occupied']) == sorted(v for v, b in p if b == 0))
        if not ok: bad.append(r['file'])
    assert not bad, ('bad headers', bad[:5])
    # the trie below the first decision
    leaves = {}
    for r in recs:
        key = tuple(b for _, b in r['path'][1:])
        assert key not in leaves, ('duplicate path', r['file'])
        leaves[key] = r
    vert = {}                                   # internal node (bit prefix) -> branching vertex
    for key, r in leaves.items():
        p = r['path'][1:]
        for d in range(len(key)):
            pre = key[:d]
            assert pre not in leaves, ('a path is a prefix of another', r['file'])
            v = p[d][0]
            assert vert.setdefault(pre, v) == v, ('two vertices at one node', pre, r['file'])
    for pre in vert:                            # both children of every internal node exist (as leaf or internal)
        for b in (0, 1):
            c = pre + (b,)
            assert c in leaves or c in vert, ('incomplete cover below', pre, b)
    order = sorted(leaves)                      # bit strings in lexicographic order = preorder of the trie
    with open(OUT + '.tmp', 'w') as f:
        for k, key in enumerate(order):
            r = leaves[key]
            f.write(json.dumps(dict(ctx=k, depth=len(r['path']), path=r['path'], missing=r['missing'], occupied=r['occupied'],
                                    file=r['file'], file_k=r['file_k'], gz_sha256=r['gz_sha256'], json_sha256=r['json_sha256'],
                                    nodes=r['nodes']), separators=(',', ':')) + '\n')
    os.replace(OUT + '.tmp', OUT)
    dep = {}
    for r in recs: dep[len(r['path'])] = dep.get(len(r['path']), 0) + 1
    print(json.dumps(dict(contexts=len(recs), internal_nodes=len(vert), depth_counts=dep, nodes_total=sum(r['nodes'] for r in recs),
                          sha256=hashlib.sha256(open(OUT, 'rb').read()).hexdigest())))


if __name__ == '__main__':
    main()
