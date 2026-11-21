# Exact basic solution from the HiGHS simplex basis (Fractions), then exact feasibility check.
from fractions import Fraction as Fr
from lp_slices import *
flat=[i for i,s in enumerate(S) if s[0]==s[1]==s[2]==s[3] and s[0]>=1]
second=[S.index(t) for t in [(1,0,0,0),(1,1,0,0),(1,1,1,0),(1,1,1,1)]]
R=base+extra
def solve_exact(rows_ge, rows_le):
    h=highspy.Highs(); h.setOptionValue('output_flag',False); h.setOptionValue('solver','simplex'); inf=highspy.kHighsInf
    for i in range(N):
        h.addVar(0.0, 0.0 if i==0 else 1.0); h.changeColCost(i,1.0)
    allrows=[(rhs,sup,'ge') for rhs,sup in rows_ge]+[(ub,sup,'le') for ub,sup in rows_le]
    for rhs,sup,t in allrows:
        if t=='ge': h.addRow(float(rhs),inf,len(sup),np.array(sup,dtype=np.int32),np.ones(len(sup)))
        else: h.addRow(-inf,float(rhs),len(sup),np.array(sup,dtype=np.int32),np.ones(len(sup)))
    h.run(); B=h.getBasis(); x=h.getSolution().col_value
    BS=highspy.HighsBasisStatus
    basic=[j for j in range(N) if B.col_status[j]==BS.kBasic]
    fixed={}
    for j in range(N):
        if B.col_status[j]!=BS.kBasic:
            fixed[j]=Fr(0) if B.col_status[j]==BS.kLower or j==0 else Fr(1)
            if B.col_status[j]==BS.kZero: fixed[j]=Fr(0)
    tight=[r for r in range(len(allrows)) if B.row_status[r]!=BS.kBasic]
    assert len(tight)==len(basic), (len(tight),len(basic))
    # build system: for each tight row, sum_{j in basic∩sup} x_j = rhs - sum fixed
    idx={j:k for k,j in enumerate(basic)}; m=len(basic)
    M=[[Fr(0)]*(m+1) for _ in range(m)]
    for k,r in enumerate(tight):
        rhs,sup,t=allrows[r]; s=Fr(rhs)
        for j in sup:
            if j in idx: M[k][idx[j]]+=1
            else: s-=fixed[j]
        M[k][m]=s
    # Gauss-Jordan
    for c in range(m):
        p=next(r for r in range(c,m) if M[r][c]!=0); M[c],M[p]=M[p],M[c]
        pv=M[c][c]; M[c]=[v/pv for v in M[c]]
        for r in range(m):
            if r!=c and M[r][c]!=0:
                f=M[r][c]; M[r]=[a-f*b for a,b in zip(M[r],M[c])]
    q=dict(fixed)
    for j,k in idx.items(): q[j]=M[k][m]
    q=[q[j] for j in range(N)]
    ok=all(0<=v<=1 for v in q) and q[0]==0 and all(sum(q[i] for i in sup)>=rhs for rhs,sup in rows_ge) and all(sum(q[i] for i in sup)<=ub for ub,sup in rows_le)
    return sum(q), ok, max(v.denominator for v in q)
for T in (19,20,21):
    print('slice',(T,36-T), 'with endpoint rows: exact vertex sum, feasible, maxden =', solve_exact(R+[(T,F),(36-T,Lo)], [(5,flat),(3,second)]))
