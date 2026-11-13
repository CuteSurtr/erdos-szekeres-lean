#!/usr/bin/env python3
"""Post-processing of scan.jsonl:
  local_certs.jsonl        every exact certificate (clause = negated record literals, checker format)
  local_rules.clauses      effective rule set: nesting literals (false by the base-CNF units of rule (B)) dropped,
                           then per (orbit, sign) the minimal phase conditions covered by the certified total orders
                           (resolution with the Y-transitivity clauses; a rule valid under every order is a unit)
  local_rules_raw.clauses  the certificate clauses themselves (one per certificate)
  uncertified.jsonl        numeric-feasible conditions with no exact certificate
  post_summary.json"""
import sys, os, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lr_core as C
from lr_scan import total_orders, consistent
E = C.E
D = os.path.dirname(os.path.abspath(__file__))

NEST = set()
for i in range(10):
    for j in range(i + 1, 10):
        for k in range(6):
            for l in range(6):
                NEST.add(E.o(6 * i + k, 6 * i + (k + 1) % 6, 6 * j + l))


def parse_cond(c):
    return {tuple(map(int, k.split(','))): v for k, v in c.items()}


def cond_clause_lits(cond):
    out = []
    for (a, b), sg in cond.items():
        y = E.Y[(a, b)]; out.append(-y if sg == 1 else y)
    return out


def main():
    rows = [json.loads(l) for l in open(D + '/scan.jsonl')]
    certs = {}; unc = []; merged = set(); stats = {'orbits': len(rows), 'both_signs_conflict': 0, 'certs': 0,
                                                   'certs_using_nesting': 0, 'uncertified_conditions': 0}
    per_orbit = {}
    for r in rows:
        t = tuple(r['t']); var = r['var']; L = r['layers']; TO = total_orders(L)
        pairs = [(a, b) for a, b in itertools.combinations(L, 2) if a != 0]
        cov_by_sign = {}
        for s_str, v in r['signs'].items():
            s = int(s_str)
            conds = []
            for c, cert in v['found']:
                key = tuple(cert['clause'])
                if key not in certs:
                    certs[key] = cert
                conds.append(parse_cond(c))
                if any(rr['kind'] == 'triple' and rr['var'] != var for rr in cert['records']):
                    stats['certs_using_nesting'] += 1
            for c, info in v['uncertified']:
                unc.append({'t': list(t), 'var': var, 'sign': s, 'cond': c, 'info': info})
            covered = [o for o in TO if any(all(o[p] == x for p, x in c.items()) for c in conds)]
            cov_by_sign[s] = covered
            # minimal covered partial conditions
            kept = []
            for k in range(0, len(pairs) + 1):
                for P in itertools.combinations(pairs, k):
                    for sg in itertools.product((1, -1), repeat=k):
                        c = dict(zip(P, sg))
                        if not consistent(c, L):
                            continue
                        if any(all(c.get(p) == x for p, x in kc.items()) for kc in kept):
                            continue
                        ext = [o for o in TO if all(o[p] == x for p, x in c.items())]
                        if ext and all(o in covered for o in ext):
                            kept.append(c)
            for c in kept:
                merged.add(tuple(sorted([-s * var] + cond_clause_lits(c), key=abs)))
        both = [o for o in cov_by_sign.get(1, []) if o in cov_by_sign.get(-1, [])]
        if both:
            stats['both_signs_conflict'] += 1; print('CONFLICT', t, both)
        per_orbit[var] = {str(s): len(cov) for s, cov in cov_by_sign.items()}
    stats['certs'] = len(certs); stats['uncertified_conditions'] = len(unc)
    with open(D + '/local_certs.jsonl', 'w') as f:
        for key in sorted(certs, key=lambda c: [abs(x) for x in c]):
            f.write(json.dumps(certs[key]) + '\n')
    with open(D + '/local_rules_raw.clauses', 'w') as f:
        for key in sorted(certs, key=lambda c: [abs(x) for x in c]):
            f.write(' '.join(map(str, key)) + ' 0\n')
    # effective: drop nesting literals; a certificate clause with only nesting literals removed is implied by
    # resolution with base-CNF units (B).  merged already uses conditions only (no nesting literals).
    eff = set()
    for key in certs:
        eff.add(tuple(x for x in key if -x not in NEST))
    # sanity: every effective clause is implied by (subsumed by) some merged clause
    ms = set(merged)
    def subsumed(c, S):
        cs = set(c)
        for k in range(1, len(c) + 1):
            for sub in itertools.combinations(sorted(cs, key=abs), k):
                if tuple(sorted(sub, key=abs)) in S:
                    return True
        return False
    stats['effective_not_subsumed_by_merged'] = sum(1 for c in eff if not subsumed(c, ms))
    merged = sorted(merged, key=lambda c: (len(c), [abs(x) for x in c]))
    with open(D + '/local_rules.clauses', 'w') as f:
        for c in merged:
            f.write(' '.join(map(str, c)) + ' 0\n')
    with open(D + '/uncertified.jsonl', 'w') as f:
        for u in unc:
            f.write(json.dumps(u) + '\n')
    from collections import Counter
    stats['merged_clauses'] = len(merged)
    stats['merged_by_length'] = dict(Counter(len(c) for c in merged))
    stats['merged_derived_not_directly_certified'] = sum(1 for c in merged if c not in eff)
    json.dump(stats, open(D + '/post_summary.json', 'w'), indent=1)
    print(json.dumps(stats))


if __name__ == '__main__':
    main()
