#!/usr/bin/env python3
"""Compare local rule sets semantically (per orbit/sign: set of covered phase total orders) and syntactically
(subsumption); count model violations of the new clauses."""
import sys, os, json, itertools, glob, random
from collections import defaultdict, Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lr_core as C
from lr_scan import total_orders
E = C.E; D = os.path.dirname(os.path.abspath(__file__)); B = os.path.dirname(D)
YINV = {v: k for k, v in E.Y.items()}


def load(f):
    return [tuple(map(int, l.split()))[:-1] for l in open(f) if l.strip() and not l.startswith(('c', 'p'))]


def coverage(cls):
    """(var, s) -> set of covered total orders (frozenset of items); plus list of non-local clauses"""
    cov = defaultdict(set); nonlocal_ = 0
    for c in cls:
        tl = [l for l in c if abs(l) <= C.NT]; yl = [l for l in c if abs(l) > C.NT]
        if len(tl) != 1:
            nonlocal_ += 1; continue
        v = abs(tl[0]); s = -1 if tl[0] > 0 else 1        # clause literal -(s*var)
        L = sorted({x // 6 for x in C.INV[v]})
        cond = {}
        ok = True
        for y in yl:
            a, b = YINV[abs(y)]
            if a not in L or b not in L:
                ok = False; break
            cond[(a, b)] = 1 if y < 0 else -1          # clause has -Y => condition Y true (theta_a < theta_b)
        if not ok:
            nonlocal_ += 1; continue
        for o in total_orders(L):
            if all(o[p] == x for p, x in cond.items()):
                cov[(v, s)].add(frozenset(o.items()))
    return cov, nonlocal_


def subsumed(c, S):
    for k in range(1, len(c) + 1):
        for sub in itertools.combinations(sorted(c, key=abs), k):
            if tuple(sorted(sub, key=abs)) in S:
                return True
    return False


def implied(c, cov):
    """semantic: is local clause c implied by coverage cov (with Y transitivity)?"""
    one, _ = coverage([c])
    return all(o <= cov.get(k, set()) for k, o in one.items()) and one


def main():
    mine = load(D + '/local_rules.clauses')
    base = load(D + '/base_local.clauses'); chord = load(B + '/main/chord_rules.clauses')
    facial = load(D + '/facial_rules_snapshot.clauses')
    norm = lambda cls: set(tuple(sorted(c, key=abs)) for c in cls)
    Sb, Sc, Sf = norm(base), norm(chord), norm(facial)
    cov_m, nl_m = coverage(mine); cov_b, nl_b = coverage(base); cov_c, _ = coverage(chord); cov_f, nl_f = coverage(facial)
    cov_bc = defaultdict(set)
    for cv in (cov_b, cov_c):
        for k, v in cv.items():
            cov_bc[k] |= v
    cov_bcf = defaultdict(set)
    for k, v in cov_bc.items():
        cov_bcf[k] |= v
    for k, v in cov_f.items():
        cov_bcf[k] |= v
    rep = {'mine_clauses': len(mine), 'base_local_clauses': len(base), 'base_nonlocal(Y-only etc)': nl_b,
           'facial_clauses': len(facial), 'facial_nonlocal': nl_f}
    # syntactic novelty
    new_bc = [c for c in mine if not subsumed(c, Sb | Sc)]
    new_bcf = [c for c in mine if not subsumed(c, Sb | Sc | Sf)]
    rep['mine_not_subsumed_by_base_or_chord'] = len(new_bc)
    rep['mine_not_subsumed_by_base_chord_facial'] = len(new_bcf)
    # semantic novelty
    sem_new_bc = [c for c in mine if not implied(c, cov_bc)]
    sem_new_bcf = [c for c in mine if not implied(c, cov_bcf)]
    rep['mine_not_implied_by_base_or_chord(semantic, with Y transitivity)'] = len(sem_new_bc)
    rep['mine_not_implied_by_base_chord_facial(semantic)'] = len(sem_new_bcf)
    rep['new_by_length'] = dict(Counter(len(c) for c in new_bc))
    # forced (var, sign, order) triples
    cnt = lambda cv: sum(len(v) for v in cv.values())
    rep['forced_sign_order_triples'] = {'mine': cnt(cov_m), 'base': cnt(cov_b), 'chord': cnt(cov_c), 'facial': cnt(cov_f),
                                        'base+chord': cnt(cov_bc)}
    miss_in_mine_from = {}
    for name, cv in (('base', cov_b), ('chord', cov_c), ('facial', cov_f)):
        miss = [(k, o) for k, v in cv.items() for o in v if o not in cov_m.get(k, set())]
        miss_in_mine_from[name] = len(miss)
        rep['examples_%s_not_in_mine' % name] = [[k[0], k[1], sorted(o)] for k, o in miss[:8]]
        rep['orbits_%s_not_in_mine' % name] = len({k for k, _ in miss})
    rep['covered_by_other_but_not_mine'] = miss_in_mine_from
    fac_extra = [(k, o) for k, v in cov_m.items() for o in v if o not in cov_f.get(k, set())]
    rep['mine_not_in_facial_triples'] = len(fac_extra); rep['mine_not_in_facial_orbits'] = len({k[0] for k, _ in fac_extra})
    fac_extra_bc = [(k, o) for k, o in fac_extra if o not in cov_bc.get(k, set())]
    rep['mine_not_in_facial_nor_base_chord_triples'] = len(fac_extra_bc)
    rep['mine_not_in_facial_nor_base_chord_orbit_signs'] = len({k for k, _ in fac_extra_bc})
    # facial clauses not reproduced (not implied by mine)
    fac_not = [c for c in facial if not implied(c, cov_m)]
    rep['facial_clauses_not_implied_by_mine'] = len(fac_not); rep['facial_not_implied_examples'] = [list(c) for c in fac_not[:10]]
    # by layer count of novel clauses
    lay = lambda c: len({x // 6 for x in C.INV[abs([l for l in c if abs(l) <= C.NT][0])]})
    rep['new_bc_by_nlayers'] = dict(Counter(lay(c) for c in new_bc))
    rep['new_bcf_by_nlayers'] = dict(Counter(lay(c) for c in new_bcf))
    with open(D + '/local_rules_new.clauses', 'w') as f:
        for c in new_bc:
            f.write(' '.join(map(str, c)) + ' 0\n')
    with open(D + '/local_rules_new_vs_facial.clauses', 'w') as f:
        for c in new_bcf:
            f.write(' '.join(map(str, c)) + ' 0\n')
    # model violations
    hard = sorted(glob.glob(B + '/models/*.json'))
    cm = sorted(glob.glob(B + '/cegar/runs/**/model*.json', recursive=True))
    samp = [l.strip() for l in open(D + '/cegar_sample400.txt') if l.strip()]   # frozen sample (runs dir grows)
    def viol(files, cls):
        nv = 0; per = Counter()
        for fn in files:
            T = set(json.load(open(fn)))
            bad = [c for c in cls if not any((l > 0) == (abs(l) in T) for l in c)]
            if bad:
                nv += 1
            for c in bad:
                per[c] += 1
        return nv, per
    for name, files in (('hard101', hard), ('cegar400', samp)):
        for tag, cls in (('new_vs_base_chord', new_bc), ('new_vs_base_chord_facial', new_bcf), ('facial', facial), ('chord_rules', chord), ('all_local_rules', mine)):
            nv, per = viol(files, cls)
            rep['%s_models_violating_%s' % (name, tag)] = '%d/%d' % (nv, len(files))
            if tag == 'new_vs_base_chord_facial':
                rep['%s_distinct_violated_%s' % (name, tag)] = len(per)
    rep['cegar_models_total'] = len(cm)
    json.dump(rep, open(D + '/compare_summary.json', 'w'), indent=1)
    print(json.dumps(rep, indent=1))


if __name__ == '__main__':
    main()
