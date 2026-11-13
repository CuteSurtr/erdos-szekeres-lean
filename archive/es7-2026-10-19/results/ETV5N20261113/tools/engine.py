"""In-process incremental SAT helpers (pysat CaDiCaL 1.9.5) for core minimisation and test shrinking.
Discovery only: every row that is used in a claimed bound is re-solved from its full CNF with the CaDiCaL
2.1.3 binary and checked by cake_lpr (certify5.py).
Owner removal = switching off every clause that mentions the owner (selector literals); for the CNF
families of coupled5 this is the order-preserving re-indexing of CNF(S minus owner)."""
import itertools
from pysat.solvers import Solver
import coupled5

_ST = {}
def static_with_owners(n):
    if n in _ST: return _ST[n]
    cnf = coupled5.CNF(list(range(n)))
    vown = {}
    for key, v in cnf.ids.items():
        vown[v] = frozenset(x for x in key[1:] if isinstance(x, int)) if key[0] in ('before', 'orientation', 'convex_four') \
            else frozenset(key[1:3])
    stat = []; 
    for c, t in zip(cnf.clauses, cnf.tags):
        if t is None:
            stat.append((c, frozenset().union(*[vown[abs(l)] for l in c])))
    if n >= 17:   # large supports: do not keep the clause objects (memory)
        return (cnf.nv, stat, vown)
    _ST[n] = (cnf.nv, stat, vown)
    return _ST[n]

def dyn_clauses(S):
    d = coupled5.CNF(S, static=False)
    return list(zip(d.clauses, d.tags)), d

def minimize_fast(S, name='cadical195'):
    """Deletion-based owner minimisation with selector assumptions and core trimming."""
    n = len(S); nv, stat, vown = static_with_owners(n)
    dyn, d = dyn_clauses(S)
    assert d.nv == nv
    sel = [nv + 1 + i for i in range(n)]
    s = Solver(name=name)
    for c, own in stat:
        s.add_clause(c + [-sel[o] for o in own])
    for c, t in dyn:
        own = set(t[1:4]) if t[0] == 'positive' else set(t[1:3])
        s.add_clause(c + [-sel[o] for o in own])
    cur = list(range(n))
    if s.solve(assumptions=[sel[o] for o in cur]):
        s.delete(); return None
    core = set(s.get_core() or [])
    cur = [o for o in cur if sel[o] in core]
    i = 0
    while i < len(cur):
        trial = cur[:i] + cur[i + 1:]
        if not s.solve(assumptions=[sel[o] for o in trial]):
            core = set(s.get_core() or [])
            cur = [o for o in trial if sel[o] in core]
        else:
            i += 1
    s.delete()
    return sorted(S[o] for o in cur)

def shrink_fast(S, tests, name='cadical195'):
    """Keep a subset of the state-dependent tests (tags) such that static + kept clauses stay UNSAT."""
    n = len(S); nv, stat, vown = static_with_owners(n)
    dyn, d = dyn_clauses(S)
    tests = [tuple(t) for t in tests]
    tsel = {t: nv + 1 + k for k, t in enumerate(tests)}
    s = Solver(name=name)
    for c, own in stat: s.add_clause(c)
    for c, t in dyn:
        if t in tsel: s.add_clause(c + [-tsel[t]])
    cur = list(tests)
    if s.solve(assumptions=[tsel[t] for t in cur]):
        s.delete(); return None
    core = set(s.get_core() or []); cur = [t for t in cur if tsel[t] in core]
    i = 0
    while i < len(cur):
        trial = cur[:i] + cur[i + 1:]
        if not s.solve(assumptions=[tsel[t] for t in trial]):
            core = set(s.get_core() or []); cur = [t for t in trial if tsel[t] in core]
        else:
            i += 1
    s.delete()
    return [list(t) for t in cur]
