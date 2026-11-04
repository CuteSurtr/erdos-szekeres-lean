#!/usr/bin/env python3
"""Compare chord clauses with the base encoding encA_6_8_10.cnf:
 (a) no chord unit is the negation of a base unit;
 (b) unit propagation over (all base clauses restricted to variables <= 5746) + chord clauses: no conflict;
 (c) which chord clauses are already base clauses / subsumed by base clauses (to confirm the 524 'new' split)."""
import sys, json
D = '<six10-work-dir>'
MAXV = 5746
base_units = set(); base_small = []; base_set = set(); nb = 0
with open(D + '/cegar/base/encA_6_8_10.cnf') as f:
    for line in f:
        if line[0] in 'cp':
            continue
        l = list(map(int, line.split()))[:-1]
        nb += 1
        if all(abs(x) <= MAXV for x in l):
            base_small.append(l)
            base_set.add(frozenset(l))
            if len(l) == 1:
                base_units.add(l[0])


def rd(fn):
    return [list(map(int, l.split()))[:-1] for l in open(fn) if l.strip()]


chord = rd(D + '/main/chord_rules.clauses')
new = rd(D + '/cegar/inbox/chord_lemma.clauses')
res = {'base_clauses_total': nb, 'base_clauses_vars_le_5746': len(base_small), 'base_units_le_5746': len(base_units)}
# (a)
res['chord_units_contradicting_base_units'] = [c for c in chord if len(c) == 1 and -c[0] in base_units]
res['chord_clauses_falsified_by_base_units'] = [c for c in chord if all(-x in base_units for x in c)]
# (b) unit propagation
def up(clauses):
    assign = {}
    changed = True
    while changed:
        changed = False
        for c in clauses:
            if any(assign.get(abs(x)) == (x > 0) for x in c):
                continue
            free = [x for x in c if abs(x) not in assign]
            if not free:
                return None, c
            if len(free) == 1:
                x = free[0]; assign[abs(x)] = x > 0; changed = True
    return assign, None
assign, confl = up(base_small + chord)
res['UP_base_small_plus_chord'] = 'conflict %s' % confl if assign is None else 'no conflict (%d vars fixed)' % len(assign)
assign0, _ = up(base_small)
res['UP_fixed_vars_base_only'] = len(assign0)
# (c)
def subsumed(c):
    s = frozenset(c)
    if s in base_set:
        return 'identical'
    if any(x in base_units for x in c):
        return 'subsumed-by-base-unit'
    for b in base_small:
        if len(b) <= len(c) and set(b) <= s:
            return 'subsumed'
    return None
newset = {frozenset(c) for c in new}
stat = {}
for c in chord:
    k = (frozenset(c) in newset, subsumed(c))
    stat[str(k)] = stat.get(str(k), 0) + 1
res['(in_new_file, base_relation)'] = stat
res['new_subset_of_chord'] = newset <= {frozenset(c) for c in chord}
# implied by base UP? (for 'new' clauses: is the clause already forced by base unit propagation?)
imp = 0
for c in new:
    if any(assign0.get(abs(x)) == (x > 0) for x in c):
        imp += 1
res['new_clauses_already_satisfied_by_base_UP'] = imp
print(json.dumps(res, indent=1))
