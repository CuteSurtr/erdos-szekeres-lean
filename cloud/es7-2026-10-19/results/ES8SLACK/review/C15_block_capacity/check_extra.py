"""Extra owner-only necessary conditions NOT in the C15 list (derived from the rank definitions).

FCW (forward cap witness): a(u,v) = 6 - F_-(u,v). If a(u,v) <= 3 then F_-(u,v) >= 3, so the attaining
  cap continues u,v,w,... ; rank growth gives F_-(v,w) = F_-(u,v)-1, i.e. a(v,w) = a(u,v)+1, and Lemma 2.1
  (d(v,w) not in I(v)) with b(v,w) <= 6 gives  f_{a(u,v)+1}(state v) <= 5.
  (Lean: ResidualRanks.StartingPath.step, rank_growth, StateInterface.incoming_admissible, label_bounds.)
BCW (backward cup witness): b(u,v) = E_+(u,v)-1. If b(u,v) >= 2 then the attaining cup ends t,u,v; growth
  gives b(t,u) = b(u,v)-1, and d(t,u) in I(u) gives f_1(state u) >= b(u,v)-1.
Reports violations for owner pairs of a witness. Usage: check_extra.py witness.json
"""
import sys, json
w = json.load(open(sys.argv[1]))
n = w['n']
st = [tuple(s) for s in w['states']]
lab = {tuple(map(int, k.split(','))): tuple(v) for k, v in w['labels'].items()}
fcw = [(p, q, lab[(p, q)], st[q]) for (p, q) in lab if lab[(p, q)][0] <= 3 and st[q][lab[(p, q)][0]] >= 6]
bcw = [(p, q, lab[(p, q)], st[p]) for (p, q) in lab if lab[(p, q)][1] >= 2 and st[p][0] < lab[(p, q)][1] - 1]
print(json.dumps({'row': w['row'], 'FCW_violations': len(fcw), 'FCW_examples': fcw[:6],
                  'BCW_violations': len(bcw), 'BCW_examples': bcw[:6]}))
