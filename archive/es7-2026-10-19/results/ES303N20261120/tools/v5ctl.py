# Controls for balz_assemble_v5.one_big against v4's one() (unchanged path) on contexts small enough for both.
import sys, os, json, gzip, hashlib, shutil
OCC = '/home/jay/research/data/bal186-20261119/zrow/b68zs/occ'
W = '/home/jay/research/data/bal186-20261119/zrow/b68zs/v5ctl'
sys.argv = ['balz_assemble_v5.py', '68', OCC, '-', W + '/outA', '1']
sys.path.insert(0, '/home/jay/research/data/bal186-20261119/zrow')
import balz_assemble_v5 as A
os.makedirs(W + '/outA', exist_ok=True); os.makedirs(W + '/outB', exist_ok=True)
items = A.descriptors(OCC, 0, 68)
byc = {it[2]: (k, it) for k, it in enumerate(items) if it[2] is not None}
sizes = sorted(((os.path.getsize(f'{OCC}/ctx-{c}.json.gz'), c) for c in byc), reverse=True)
mid = [c for s, c in sizes if 2e6 < s <= 9e6]
pick = sorted(set(mid[::max(1, len(mid) // 6)][:6] + [c for s, c in sizes if s <= 2e6][:2] + [2]))
out = {'pos': [], 'neg': []}
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
for c in pick:
    k, it = byc[c]
    A.OUT = W + '/outA'; ra = A.one((k,) + it)
    fa = sha(f'{W}/outA/ctx-{k}-zb68.json.gz')
    for sub in (30000, 1500, 97):
        A.SUB_NODES = sub; A.OUT = W + '/outB'
        rb = A.one_big((k,) + it)
        fb = sha(f'{W}/outB/ctx-{k}-zb68.json.gz')
        row = {'ctx': c, 'sub': sub, 'one': list(ra), 'one_big': list(rb), 'same_result': list(ra) == list(rb), 'same_file': fa == fb}
        out['pos'].append(row); print(json.dumps(row), flush=True)
# negative controls on ctx-2 (copied and modified in a scratch side dir)
k, it = byc[2]; path = it[0]
neg_dir = W + '/negside'; os.makedirs(neg_dir, exist_ok=True)
orig = json.loads(gzip.decompress(open(f'{OCC}/ctx-2.json.gz', 'rb').read()))
def run_mod(name, mod):
    d = json.loads(json.dumps(orig)); mod(d)
    open(f'{neg_dir}/ctx-2.json.gz', 'wb').write(gzip.compress(json.dumps(d, separators=(',', ':')).encode()))
    A.SUB_NODES = 1500; A.OUT = W + '/outB'
    try:
        r = A.one_big((k, path, neg_dir, 2, None)); res = 'returned ok=%s' % r[1]
    except Exception as e:
        res = 'raised %s: %s' % (type(e).__name__, str(e)[:80])
    row = {'neg': name, 'result': res}; out['neg'].append(row); print(json.dumps(row), flush=True)
leaf_ix = [i for i, nd in enumerate(orig['nodes']) if nd['type'] == 'weighted']
br_ix = [i for i, nd in enumerate(orig['nodes']) if nd['type'] == 'branch']
def n1(d): d['nodes'][leaf_ix[len(leaf_ix) // 2]]['capacity'] *= 1000          # margin <= 0
def n2(d): d['nodes'][br_ix[5]]['one'] = d['nodes'][br_ix[3]]['zero']            # node reached twice
def n3(d): d['nodes'].append({'type': 'over_budget'})                             # unreachable node
def n4(d): d['nodes'][leaf_ix[-1]] = {'type': 'pending'}                         # extra pending leaf
def n5(d): d['nodes'][br_ix[len(br_ix) // 2]]['vertex'] = 0                       # vertex already fixed
def n6(d): d['nodes'][br_ix[7]]['zero'] = True                                   # bool as a child index
def n7(d): d['nodes'][br_ix[9]]['vertex'] = True                                  # bool as a vertex
for nm, f in (('N1 capacity x1000 in one leaf', n1), ('N2 branch child reused', n2), ('N3 unreachable node', n3),
              ('N4 leaf replaced by pending', n4), ('N5 branch on fixed vertex 0', n5), ('N6 bool child index', n6),
              ('N7 bool vertex', n7)):
    run_mod(nm, f)
json.dump(out, open(W + '/ctl_result.json', 'w'), indent=1)
print('POS all equal:', all(r['same_result'] and r['same_file'] for r in out['pos']), 'n=', len(out['pos']))
