#!/usr/bin/env python3
"""Reduce the two monotone obstructions; check terminal-edge sufficient tests."""
import itertools as it
import hashlib
import json
from fractions import Fraction
from pathlib import Path
import sys
import time

from probe import det, family, ids, mask

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/resume/weak_theory')


def line(P, b, c, X):
    return Fraction(P[b][1]*(P[c][0]-P[b][0])
                    +(P[c][1]-P[b][1])*(X-P[b][0]), P[c][0]-P[b][0])


def reduce_obstruction(n, name, Aids):
    source = ROOT.parent / 'DELTA2N20261113/data/cex' / name
    raw = json.loads(source.read_text())
    P = raw.get('P', raw.get('points'))
    m, A, r = len(P), mask(Aids), len(P)-1
    bit = 1 << r
    gons = family(P, n-1)
    private = {q: [H for H in gons if not H & bit and H & A == 1 << q] for q in Aids}
    missed = [H for H in gons if H & bit and not H & A]
    rest = [i for i in range(m) if not (A | bit) >> i & 1]
    ground = None
    for size in range(len(rest)+1):
        for B in it.combinations(rest, size):
            G = mask(B) | A | bit
            if any(H & G == H for H in missed) and all(any(H & G == H for H in private[q]) for q in Aids):
                ground = G
                break
        if ground is not None:
            break
    retained = ids(ground)
    ren = {q:i for i,q in enumerate(retained)}
    Q = [P[q] for q in retained]
    targets = family(Q, n-1)
    Anew = mask(ren[q] for q in Aids)
    rnew = ren[r]
    old = [H for H in targets if not H >> rnew & 1]
    assert all(Anew & H for H in old)
    full = next(D for D in range(1 << len(Q))
                if all(D & H for H in targets)
                and not any(D & K == K for K in family(Q,4,True)))
    return dict(n=n, P=Q, source=str(source), source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                source_indices=retained,
                r=rnew, A=ids(Anew), blocker=ids(Anew | (1 << rnew)),
                private_polygons={str(ren[q]):ids(next(H for H in old if H & Anew == 1 << ren[q])) for q in Aids},
                missed_polygon=ids(next(H for H in targets if not H & Anew)),
                full_delta=ids(full))


def thresholds(P, n, tag):
    m, r = len(P), len(P)-1
    assert all(det(P,*C) for C in it.combinations(range(m),3))
    X, Y = P[r]
    allcaps, gons = family(P,4,True), family(P,n-1)
    oldcaps = [K for K in allcaps if not K >> r & 1]
    oldgons = [H for H in gons if not H >> r & 1]
    oldtriples = [C for C in it.combinations(range(r),3) if det(P,*C) < 0]
    rank4pairs = {tuple(ids(K)[-2:]) for K in oldcaps}
    triples = [(mask(C), tuple(C[-2:]), line(P, *C[-2:], X)) for C in oldtriples]
    F4 = max((line(P,*pair,X) for pair in rank4pairs), default=None)
    counts = dict(old_deltas=0, terminal_pair_safe=0, threshold_safe=0,
                  actual_red_extensions=0, rank3_blockers=0)
    examples = {}
    for A in range(1 << r):
        if any(A & K == K for K in oldcaps) or not all(A & H for H in oldgons):
            continue
        counts['old_deltas'] += 1
        active = [(pair, height) for C,pair,height in triples if A & C == C]
        F3 = max((h for _,h in active), default=None)
        terminal_safe = all(pair in rank4pairs for pair,_ in active)
        threshold_safe = F3 is None or F4 is not None and F3 <= F4
        actualsafe = F3 is None or Y > F3
        counts['terminal_pair_safe'] += terminal_safe
        counts['threshold_safe'] += threshold_safe
        counts['actual_red_extensions'] += actualsafe
        fullA = A | (1 << r)
        exactsafe = not any(fullA & K == K for K in allcaps)
        assert exactsafe == actualsafe
        assert not terminal_safe or threshold_safe
        assert not threshold_safe or actualsafe
        for pair,height in active:
            if Y < height:
                counts['rank3_blockers'] += 1
                assert pair not in rank4pairs
        kind = None
        if terminal_safe and active:
            kind = 'noncup_terminal_safe'
        elif threshold_safe and not terminal_safe:
            kind = 'envelope_only_safe'
        elif actualsafe and not threshold_safe:
            kind = 'actual_height_only_safe'
        if kind and kind not in examples:
            examples[kind] = dict(A=ids(A), F3=str(F3), F4=str(F4), r_y=Y,
                                  full_delta=ids(fullA))
    return dict(tag=tag, n=n, m=m, counts=counts, examples=examples)


def main():
    started = time.monotonic()
    obstructions = [reduce_obstruction(7,'restr_ends_weak_a5_n7_m12_real.json',[7,9,10]),
                    reduce_obstruction(8,'restr_ends_weak_a5_n8_m13_real.json',[9,10,11])]
    out = dict(label='COMPUTED', obstructions=obstructions,
               threshold_checks=[thresholds(w['P'],w['n'],f"reduced-n{w['n']}") for w in obstructions])
    for n in (7,8):
        # Nonvacuous convex (n-1)-gon plus an extreme point hiding its old right endpoint.
        P = [(0,0),(1,-4),(2,8),(4,10),(5,-4),(6,0),(8,1)]
        if n == 8:
            P.insert(3,(3,-5))
        assert not family(P,5,True) and not family(P,n)
        out['threshold_checks'].append(thresholds(P,n,f'nonvacuous-upper4-n{n}'))
    out['failed_construction'] = {
        'status':'REFUTED BEFORE USE',
        'description':'Earlier cup, last blue point (-1,-20), followed by cap T=(0,0),(1,10),(2,18),(3,24).',
        'five_cap':[[-1,-20],[0,0],[1,10],[2,18],[3,24]],
        'reason':'Last blue point prepends to all four vertices of T, creating a forbidden five-cap.'}
    out['elapsed_seconds'] = time.monotonic()-started
    target = SCRATCH / 'refined.json'
    target.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__ == '__main__':
    main()
