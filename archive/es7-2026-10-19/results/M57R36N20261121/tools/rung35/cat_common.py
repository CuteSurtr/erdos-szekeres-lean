"""cat_common.py -- internal state catalog for (CA, CB): cap coordinates 1..CA, cup coordinates 1..CB.
States = nonincreasing column heights f_1>=...>=f_CA, 0<=f_a<=CB (column a = cap coordinate a).
D(s->t)  = cells(t) minus cells(s)                     (state separation)
D'(s->t) = {(a,b) in D(s->t): a <= capH(s)+1, b <= cupH(s)+1}   (rank attainment, Lemma R)
"""
import itertools

def make(CA, CB):
    states = [f for f in itertools.product(range(CB + 1), repeat=CA)
              if all(f[i] >= f[i + 1] for i in range(CA - 1))]
    states.sort(key=lambda f: (sum(f), f))
    cells = [frozenset((a + 1, y) for a in range(CA) for y in range(1, f[a] + 1)) for f in states]
    capH = [sum(1 for x in f if x > 0) for f in states]
    cupH = [f[0] for f in states]
    N = len(states)
    dref = [[frozenset(z for z in cells[t] - cells[s] if z[0] <= capH[s] + 1 and z[1] <= cupH[s] + 1)
             if s != t else frozenset() for t in range(N)] for s in range(N)]
    return states, cells, capH, cupH, dref

def corners(cellset):
    """maximal cells of a down-set"""
    return [z for z in cellset if (z[0] + 1, z[1]) not in cellset and (z[0], z[1] + 1) not in cellset]
