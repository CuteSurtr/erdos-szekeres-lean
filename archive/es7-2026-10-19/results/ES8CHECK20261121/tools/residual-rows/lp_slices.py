import gzip, json, sys
import numpy as np, highspy
ESB='<repo>'
SRC=ESB+'/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
ROWS=ESB+'/archive/es7-2026-10-19/results/LO33N20261113/budget34/data/frozen-inputs/s20-v5/rows.txt'
d=json.load(gzip.open(SRC)); S=[tuple(s[:4]) for s in d['states']]; N=len(S)
base=[(c['rhs'],list(c['support'])) for c in d['constraints']]
def read_rows(p):
    out=[]; started=False
    for line in open(p):
        t=line.split()
        if not t: continue
        if t[0]=='rows': started=True; continue
        if not started: continue
        rhs=int(t[0]); k=int(t[1]); sup=list(map(int,t[2:2+k])); assert len(sup)==k
        out.append((rhs,sup))
    return out
allrows=read_rows(ROWS)
assert [tuple(r) for r in allrows[:2650]]==[(a,tuple(b)) for a,b in base] or all(allrows[i][0]==base[i][0] and sorted(allrows[i][1])==sorted(base[i][1]) for i in range(2650))
F=[i for i,s in enumerate(S) if s[0]>=5]; Lo=[i for i,s in enumerate(S) if s[0]<=4]
extra=[r for r in allrows[2650:] if sorted(r[1]) not in (sorted(F),sorted(Lo))]
caps=[r for r in allrows[2650:] if sorted(r[1]) in (sorted(F),sorted(Lo))]
def lp(rows, fix0=True, extra_le=(), retx=False):
    h=highspy.Highs(); h.setOptionValue('output_flag',False)
    inf=highspy.kHighsInf
    for i in range(N):
        lb=0.0; ub=0.0 if (fix0 and i==0) else 1.0
        h.addVar(lb,ub); h.changeColCost(i,1.0)
    for rhs,sup in rows:
        h.addRow(float(rhs),inf,len(sup),np.array(sup,dtype=np.int32),np.ones(len(sup)))
    for ub,sup in extra_le:
        h.addRow(-inf,float(ub),len(sup),np.array(sup,dtype=np.int32),np.ones(len(sup)))
    h.run(); v=h.getInfo().objective_function_value
    if retx: return v, np.array(h.getSolution().col_value)
    return v
if __name__=='__main__':
    print('states',N,'F',len(F),'Lo',len(Lo),'base',len(base),'extra(noncap)',len(extra),'caps',[(r[0],len(r[1])) for r in caps])
    print('LP base2650', lp(base))
    print('LP base+extra', lp(base+extra))
    for T in (18,19,20,21):
        L=36-T
        for name,rows in (('2650',base),('2650+extra',base+extra)):
            print('slice',(T,L),name, lp(rows+[(T,F),(L,Lo)]))
