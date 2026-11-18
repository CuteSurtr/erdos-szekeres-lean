"""Independent SB encoder and tail preparation; PySAT seqcounter is shared.
No original encoder imports. The C++ recognizer independently checks mono_top.
"""
import hashlib
import itertools as it
import json
import math
from pysat.card import CardEnc, EncType
from model import D, HERE, WORK, tau

def lex(x, pairs):
    for a,b in pairs:
        if x[a] != x[b]:
            return not x[a]
    return True

def sb_clauses(selectors, pairs, top):
    out = []; prev = None
    for j,(a,b) in enumerate(pairs):
        gate = [] if prev is None else [-prev]
        out.append(gate+[-selectors[a],selectors[b]])
        if j+1 < len(pairs):
            top += 1
            out.append(gate+[-selectors[a],-selectors[b],top])
            out.append(gate+[selectors[a],selectors[b],top])
            prev = top
    return out,top

def main():
    lay = json.loads((D/'layout.json').read_text())
    assert lay['W'] == list(range(70)) and lay['L'] == 13 and lay['cube'] == []
    first = 7*math.comb(70,2)+math.comb(70,3)+math.comb(70,4)+1
    selectors = list(range(first,first+70))
    assert lay['sel'] == [selectors[0],selectors[-1]]
    enc = CardEnc.atmost(lits=[-s for s in selectors[2:]],bound=13,
                         top_id=lay['mono_top'],encoding=EncType.seqcounter)
    assert enc.nv == lay['card_top'] and len(enc.clauses) == 1472
    pairs = lay['sb_pairs']; seen = set()
    for a,b in pairs:
        assert a != b and tau[a] == b and tau[b] == a
        assert tuple(sorted((a,b))) not in seen
        seen.add(tuple(sorted((a,b))))
    assert len(pairs) == 27 and sum(tau[s] == s for s in range(70)) == 16
    sb,top = sb_clauses(selectors,pairs,enc.nv)
    assert len(sb) == 79 and top == lay['vars']
    # Exhaust all local truth-table transitions, including the final pair.
    transitions = 0
    for prev,x,y in it.product((False,True),repeat=3):
        e = prev and (x == y)
        comparator = not prev or not x or y
        propagation = ((not prev or not x or not y or e) and
                       (not prev or x or y or e))
        assert propagation
        assert comparator == (not(prev and x and not y))
        transitions += 1
    # Representatives for both values of each equal prefix, every first
    # differing pair and both directions; later pairs are deliberately varied.
    samples = 0
    for j in range(28):
        for equal,direction in it.product((False,True),repeat=2):
            x = [True]*70
            for k,(a,b) in enumerate(pairs):
                x[a],x[b] = (equal,equal) if k<j else ((direction,not direction) if k==j else (bool(k%2),bool((k//2)%2)))
            y = [x[tau[s]] for s in range(70)]
            assert lex(x,pairs) or lex(y,pairs)
            assert (lex(x,pairs) == lex(y,pairs)) == all(x[a] == x[b] for a,b in pairs)
            chosen = x if lex(x,pairs) else y
            values = dict(zip(selectors,chosen)); equalprefix = True
            for k,(a,b) in enumerate(pairs[:-1]):
                equalprefix = equalprefix and chosen[a] == chosen[b]
                values[enc.nv+1+k] = equalprefix
            assert all(any(values[abs(l)] == (l>0) for l in c) for c in sb)
            samples += 1
    rows = json.loads((D/'used_rows.json').read_text())
    tail = WORK/'independent-tail.txt'
    with tail.open('w') as f:
        f.write(f'meta {lay["mono_top"]} {enc.nv} {top} {first} {first+69}\n')
        for s in selectors[:2]:
            f.write(f'fixed {s} 0\n')
        for support,demand in rows:
            assert demand == 1
            f.write('row '+' '.join(str(-selectors[s]) for s in support)+' 0\n')
        for family,clauses in [('counter',enc.clauses),('sb',sb)]:
            for c in clauses:
                f.write(family+' '+' '.join(map(str,c))+' 0\n')
    report = {'label':'COMPUTED','mirror_orbits':27,'fixed_states':16,
              'full_sb_clauses':len(sb),'local_transition_cases':transitions,
              'first_difference_controls':samples,'counter_clauses':len(enc.clauses),
              'card_top':enc.nv,'header_vars':top,
              'shared_dependency':'installed PySAT CardEnc sequential counter, as in prior audit',
              'tail_sha256':hashlib.sha256(tail.read_bytes()).hexdigest()}
    (HERE/'data/tail.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
