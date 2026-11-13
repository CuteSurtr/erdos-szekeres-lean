"""Independent re-check of a row subset: every row must be (a) a cycle row (a list order passing the six-order
test exists, demand = len - 7), (b) a Baek block row (all pairwise refined domains use only two cap coordinates,
demand = len - 22), or (c) a demand-one coupled row whose own CNF was certified by cake_lpr ('s VERIFIED UNSAT'
in certified.jsonl, CNF hash re-derived from the uncached builder for a sample).
usage: final_check.py <subset.json> [certified.jsonl] [hash_sample]"""
import json, sys, hashlib, random, itertools
import etv_common as ec
from cycle_order import order, check_list
import coupled5
sub = json.load(open(sys.argv[1])); cert_file = sys.argv[2] if len(sys.argv) > 2 else 'certified.jsonl'
sample = int(sys.argv[3]) if len(sys.argv) > 3 else 20
import glob
cert = {}
for fn in sorted(glob.glob(cert_file)):
    for line in open(fn):
        r = json.loads(line)
        if r['verdict'] == 's VERIFIED UNSAT': cert[tuple(r['support'])] = r['cnf_sha256']
def block_ok(S):
    for K in itertools.combinations(range(1, ec.A + 1), 2):
        if all(z[0] in K for s, t in itertools.permutations(S, 2) for z in ec.DREF[s][t]): return True
    return False
kinds = {'cycle': 0, 'block': 0, 'coupled': 0}; bad = []; coupled_rows = []
for S, d in sub:
    S = sorted(S); T = tuple(S)
    if len(set(S)) != len(S) or any(not (0 <= x < ec.N) for x in S): bad.append((S, d, 'malformed')); continue
    if d == len(S) - 7 and (lambda L: L is not None and check_list(L))(order(S)): kinds['cycle'] += 1; continue
    if len(S) >= 23 and d == len(S) - 22 and block_ok(S): kinds['block'] += 1; continue
    if d == 1 and T in cert: kinds['coupled'] += 1; coupled_rows.append(T); continue
    bad.append((S, d, 'unjustified'))
rng = random.Random(7); hb = 0
for T in rng.sample(coupled_rows, min(sample, len(coupled_rows))):
    h = hashlib.sha256(coupled5.CNF(list(T)).dimacs().encode()).hexdigest()
    if h != cert[T]: bad.append((list(T), 1, 'cnf hash mismatch'))
    hb += 1
print(json.dumps({'rows': len(sub), 'kinds': kinds, 'cnf_hash_rechecked': hb, 'bad': len(bad), 'first_bad': bad[:3],
                  'subset_sha256': hashlib.sha256(open(sys.argv[1], 'rb').read()).hexdigest()}))
