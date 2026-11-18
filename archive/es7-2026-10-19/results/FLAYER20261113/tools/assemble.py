"""Copy tools and small data into the record directory and write SHA256SUMS (run at the end)."""
import os, shutil, glob, json, hashlib, sys
W = os.path.dirname(os.path.abspath(__file__))
R = '/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/FLAYER20261113'
for d in ('tools', 'data', 'data/cex', 'data/logs', 'data/split_partitions'): os.makedirs(os.path.join(R, d), exist_ok=True)
def cp(src, dst):
    if os.path.exists(src): shutil.copy2(src, dst); return True
    return False
tools = [f for f in glob.glob(os.path.join(W, '*.py')) + glob.glob(os.path.join(W, '*.sh')) + [os.path.join(W, 'esgeo.c')]
         if os.path.basename(f) not in ('t0.py', 't1.py', 't2.py', 't3.py', 't4.py', 'geom.py')]
for f in tools: cp(f, os.path.join(R, 'tools', os.path.basename(f)))
data = ['etv668.json', 'pool_etv.jsonl', 'pool_compose.jsonl', 'pool_sub64.jsonl', 'pool_size.jsonl', 'sets_pE.jsonl', 'sets_pX.jsonl',
        'sets_pEuA.jsonl', 'sets_pZ.jsonl', 'sets_etvwalk.jsonl', 'sets_fl55_E.jsonl', 'sets_fl55_EuA.jsonl', 'singles.jsonl', 'pairs.jsonl',
        'singles_real.jsonl', 'pairs_real.jsonl', 'samples_E26.jsonl', 'samples_lvl.jsonl', 'samples_50.jsonl', 'maximal_4_4_4.json',
        'maximal_4_5_7.json', 'maximal_5_5_14.json', 'circuits_4_4_4.json', 'circuits_4_5_7.json', 'circuits_5_5_14.json',
        'small_table_5_5.json', 'toplevel.jsonl', 'cert_split.log', 'regen.log', 'regen_weak.log', 'nosplit_more.jsonl', 'cyc_base_A4B4.json']
for f in data: cp(os.path.join(W, f), os.path.join(R, 'data', f))
cp(os.path.join(W, 'cert', 'certified.jsonl'), os.path.join(R, 'data', 'certified.jsonl'))
cp(os.path.join(W, 'cert', 'certified_cnf.jsonl'), os.path.join(R, 'data', 'certified_cnf.jsonl'))
for f in glob.glob(os.path.join(W, 'cert', '*_partitions.json')): cp(f, os.path.join(R, 'data', 'split_partitions', os.path.basename(f)))
for f in glob.glob(os.path.join(W, '*.log')): cp(f, os.path.join(R, 'data', 'logs', os.path.basename(f)))
for f in glob.glob(os.path.join(W, 'MEMGUARD_STOPPED_*.txt')): cp(f, os.path.join(R, 'data', 'logs', os.path.basename(f)))
# counterexample files
cp(os.path.join(W, 'split_counterexample_5_5_14.json'), os.path.join(R, 'data', 'cex', 'split_counterexample_5_5_14.json'))
for f in glob.glob(os.path.join(W, 'nosplit_best_*.json')): cp(f, os.path.join(R, 'data', 'cex', os.path.basename(f)))
for f in glob.glob(os.path.join(W, 'real_nosplit_*.json')): cp(f, os.path.join(R, 'data', 'cex', os.path.basename(f)))
cp(os.path.join(W, 'nosplit_sample_real.jsonl'), os.path.join(R, 'data', 'cex', 'real_nosplit_5_5_14.jsonl'))
for f in ('nosplit_sample.jsonl', 'nosplit_sample_bfp.jsonl', 'nosplit_more_bfp.jsonl', 'split_counterexample_5_5_14_bfp.jsonl', 'bfp_control.jsonl',
          'bfp_control_bfp.jsonl', 'nosplit_check40.jsonl', 'init_E25.json'):
    cp(os.path.join(W, f), os.path.join(R, 'data', f))
import gzip
if os.path.exists(os.path.join(W, 'nosplit_all.jsonl')):
    with open(os.path.join(W, 'nosplit_all.jsonl'), 'rb') as fi, gzip.GzipFile(os.path.join(R, 'data', 'nosplit_all.jsonl.gz'), 'wb', mtime=0) as fo: fo.write(fi.read())
sys.path.insert(0, W)
import fl, an1
for line in open(os.path.join(W, 'pool_size.jsonl')):
    P = [tuple(p) for p in json.loads(line)['P']]; S = fl.Set66(P)
    E = [S.P[v] for v in range(S.n) if S.in_f[v][0] == 4]
    if an1.has_gon(E, 4, 5):
        json.dump({'claim': 'E (ends of 5-cups) contains a (4-cap,5-cup)-gon', 'n': S.n, 'E_size': len(E), 'P': S.P},
                  open(os.path.join(R, 'data', 'cex', 'E_has_45_gon_n%d.json' % S.n), 'w')); break
best = None
for line in open(os.path.join(W, 'sets_pX.jsonl')):
    r = json.loads(line); S = fl.Set66([tuple(p) for p in r['P']])
    x = sum(1 for f in S.in_f if f[0] == 4 and f[3] >= 1)
    if best is None or x > best[0]: best = (x, S.P)
json.dump({'claim': '|X| = %d' % best[0], 'n': len(best[1]), 'P': best[1]}, open(os.path.join(R, 'data', 'cex', 'X_%d_n%d.json' % (best[0], len(best[1]))), 'w'))
Pb = json.load(open(os.path.join(W, 'init_Ebest.json'))); Sb = fl.Set66([tuple(p) for p in Pb])
eb = sum(1 for f in Sb.in_f if f[0] == 4); ab = sum(1 for f in Sb.in_f if f[3] >= 1); xb = sum(1 for f in Sb.in_f if f[0] == 4 and f[3] >= 1)
json.dump({'claim': '|E| = %d, |A| = %d, |X| = %d, |E u A| = %d' % (eb, ab, xb, eb + ab - xb), 'n': Sb.n, 'P': Sb.P}, open(os.path.join(R, 'data', 'cex', 'E_%d_n%d.json' % (eb, Sb.n)), 'w'))
# hashes
lines = []
for sub in ('tools', 'data'):
    for root, dirs, files in os.walk(os.path.join(R, sub)):
        for fn in sorted(files):
            if fn == 'SHA256SUMS': continue
            p = os.path.join(root, fn); h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
            lines.append(f'{h}  {os.path.relpath(p, R)}')
open(os.path.join(R, 'SHA256SUMS'), 'w').write('\n'.join(sorted(lines, key=lambda l: l.split('  ')[1])) + '\n')
print('copied', len(tools), 'tools;', len(lines), 'files hashed')
