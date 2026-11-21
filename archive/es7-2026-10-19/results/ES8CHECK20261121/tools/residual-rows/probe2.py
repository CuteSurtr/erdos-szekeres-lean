from lp_slices import *
import itertools
R=base+extra
def maxface(rows, Y, T):
    h=highspy.Highs(); h.setOptionValue('output_flag',False); inf=highspy.kHighsInf
    Ys=set(Y)
    for i in range(N):
        h.addVar(0.0, 0.0 if i==0 else 1.0); h.changeColCost(i, -1.0 if i in Ys else 0.0)
    for rhs,sup in rows: h.addRow(float(rhs),inf,len(sup),np.array(sup,dtype=np.int32),np.ones(len(sup)))
    h.addRow(float(T),float(T),len(F),np.array(F,dtype=np.int32),np.ones(len(F)))
    h.addRow(float(36-T),float(36-T),len(Lo),np.array(Lo,dtype=np.int32),np.ones(len(Lo)))
    h.run(); st=h.getModelStatus()
    return -h.getInfo().objective_function_value, str(st)
fams={}
for j in range(0,7):
    fams[f'f1>=5,f2>={j}']=[i for i,s in enumerate(S) if s[0]>=5 and s[1]>=j]
    fams[f'f1>=5,f3>={j}']=[i for i,s in enumerate(S) if s[0]>=5 and s[2]>=j]
    fams[f'f1>=5,f4>={j}']=[i for i,s in enumerate(S) if s[0]>=5 and s[3]>=j]
    fams[f'f1<=4,f4>={j}']=[i for i,s in enumerate(S) if s[0]<=4 and s[3]>=j]
    fams[f'f1<=4,f2>={j}']=[i for i,s in enumerate(S) if s[0]<=4 and s[1]>=j]
    fams[f'f1<=4,f4<={j}']=[i for i,s in enumerate(S) if s[0]<=4 and s[3]<=j]
    fams[f'f1>=5,f4<={j}']=[i for i,s in enumerate(S) if s[0]>=5 and s[3]<=j]
fams['f1=6']=[i for i,s in enumerate(S) if s[0]==6]
fams['f1=5']=[i for i,s in enumerate(S) if s[0]==5]
fams['f4>=2 (A2)']=[i for i,s in enumerate(S) if s[3]>=2]
fams['f4>=1 (A1)']=[i for i,s in enumerate(S) if s[3]>=1]
fams['f4=0']=[i for i,s in enumerate(S) if s[3]==0]
seen=set()
for T in (19,20,21):
    print('=== slice',(T,36-T))
    for nm,Y in fams.items():
        key=tuple(Y)
        if len(Y)==0: continue
        m,st=maxface(R,Y,T)
        print(f'  {nm:16s} |Y|={len(Y):3d} max_PT h(Y)={m:7.3f}  need demand >= {int(np.floor(m+1e-9))+1}  (|Y|-demand cap = {len(Y)-int(np.floor(m+1e-9))-1})')
