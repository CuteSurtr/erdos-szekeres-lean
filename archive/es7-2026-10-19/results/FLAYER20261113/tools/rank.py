"""Exact hole minimum of the 70-state system: cycle rows + candidate capacity rows (CP-SAT, COMPUTED)."""
import sys, json
import fl
from fl import *
from ortools.sat.python import cp_model
BASE = json.load(open('cyc_base_A4B4.json'))['rows']
def fam(pred): return [i for i, f in enumerate(STATES) if eval(pred, {'f': f})]
def solve(extra, base=BASE, tlim=60):
    m = cp_model.CpModel(); h = [m.NewBoolVar(f'h{i}') for i in range(N)]
    for i in ec.FIXED_OCC: m.Add(h[i] == 0)
    for s, d in list(base) + list(extra): m.Add(sum(h[i] for i in s) >= d)
    m.Minimize(sum(h))
    so = cp_model.CpSolver(); so.parameters.num_workers = 1; so.parameters.max_time_in_seconds = tlim
    st = so.Solve(m)
    return so.StatusName(st), int(round(so.ObjectiveValue())), so.BestObjectiveBound(), [i for i in range(N) if so.Value(h[i])]
if __name__ == '__main__':
    E = fam('f[0]==4'); A = fam('f[3]>=1'); X = fam('f[0]==4 and f[3]>=1'); EA = fam('f[0]==4 or f[3]>=1')
    cands = {
      'base (cycle rows only)': [],
      '|E|<=25': [(E, 10)], '|E|<=25 and |A|<=25': [(E, 10), (A, 10)],
      '|E u A|<=30': [(EA, 20)], '|E u A|<=32': [(EA, 18)], '|E u A|<=35': [(EA, 15)],
      '|X|<=16': [(X, 4)], '|X|<=14': [(X, 6)],
      '|E|<=25,|A|<=25,|X|<=16': [(E, 10), (A, 10), (X, 4)],
      '|E|<=26 and |A|<=26': [(E, 9), (A, 9)], '|E|<=28 and |A|<=28': [(E, 7), (A, 7)], '|E|<=30 and |A|<=30': [(E, 5), (A, 5)],
    }
    for nm, extra in cands.items():
        st, v, bd, H = solve(extra)
        print('%-32s %s holes %d (bound %.1f) -> N66 <= %d' % (nm, st, v, bd, N - v), flush=True)
