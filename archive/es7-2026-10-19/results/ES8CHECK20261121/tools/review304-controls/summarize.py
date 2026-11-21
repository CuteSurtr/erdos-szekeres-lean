import json, sys, os
D = '<scratch>/agents/review304-controls/'
tot = {}
for nm in ['main_random', 'main_greedy', 'main_struct', 'random_probe', 'random_probe2', 'greedy_probe', 'struct_probe']:
    p = D + nm + '.json'
    if not os.path.exists(p):
        print(nm, 'missing'); continue
    d = json.load(open(p))
    A = d['agg']; R = d['records']
    bal = [r for r in R if r.get('balanced_type')]
    of = [r for r in bal if r.get('octagon_free')]
    big = sorted(of, key=lambda r: -r['n'])[:3]
    print('==', nm, 'sets', A['sets'], 'balanced-type', A['balanced_type'], 'octfree', A['octfree'],
          'with_oct', A['with_oct'], 'fails a/b/c/d', A['a_fail'], A['b_fail'], A['c_fail'], A['d_fail'],
          'e_viol_octfree', A['e_viol_octfree'], 'viol_sets_with_oct', A['viol_with_oct_sets'])
    print('   max n balanced', A['max_n_balanced'], 'max n octfree', A['max_n_octfree_bal'],
          'max occupied octfree', A['max_occupied_octfree'], 'min slack octfree', A['min_slack_octfree'],
          'max tight rows', A['max_tight_octfree'], 'max Z owners', A['max_z_owners'], 'max Z* owners', A['max_zs_owners'],
          'wide f4=0 class has 6-chain', A['wide_has6'], 'elapsed', round(A.get('elapsed', 0), 1))
    print('   size hist (decades)', dict(sorted(A['sizes'].items(), key=lambda kv: int(kv[0]))))
    if of:
        n60 = sum(1 for r in of if r['n'] >= 60); n50 = sum(1 for r in of if r['n'] >= 50)
        print('   octfree sets with n>=50:', n50, ' n>=60:', n60,
              ' sets with >=1 tight row:', sum(1 for r in of if r.get('n_tight', 0) > 0))
        print('   top octfree:', [(r['n'], r['occupied'], r['min_slack'], r['n_tight'], r.get('base', r.get('mode'))) for r in big])
    for k in ['sets', 'balanced_type', 'octfree', 'with_oct', 'a_fail', 'b_fail', 'c_fail', 'd_fail', 'e_viol_octfree']:
        if nm.startswith('main'):
            tot[k] = tot.get(k, 0) + A[k]
print('MAIN TOTALS', tot)
