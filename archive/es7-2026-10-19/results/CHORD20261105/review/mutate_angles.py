#!/usr/bin/env python3
"""Mutation test of check_angles.analyse: negating the orientation literal must always be rejected; dropping or
flipping the Y literal of a binary clause is expected to be rejected (else the clause would be a unit); random
orientation units over all 5710 orbits must be accepted exactly for the orbits whose sign is forced radius-free."""
import sys, json, random
from check_angles import analyse
from indep_enc import NTRIP, TRIPLE_OF

cls = []
for line in open(sys.argv[1]):
    l = list(map(int, line.split()))[:-1]
    cls.append(l)
neg_acc = drop_acc = flip_acc = 0; nb = 0
for c in cls:
    L = [x for x in c if abs(x) <= NTRIP][0]
    c2 = [(-x if x == L else x) for x in c]
    if analyse(c2)[0]:
        neg_acc += 1; print('NEGATED ACCEPTED', c, c2)
    if len(c) == 2:
        nb += 1
        y = [x for x in c if abs(x) > NTRIP][0]
        if analyse([L])[0]:
            drop_acc += 1; print('DROP-Y ACCEPTED', c)
        if analyse([L, -y])[0]:
            flip_acc += 1; print('FLIP-Y ACCEPTED', c)
print(json.dumps({'clauses': len(cls), 'negated_accepted': neg_acc, 'binary': nb,
                  'dropY_accepted': drop_acc, 'flipY_accepted': flip_acc}))
