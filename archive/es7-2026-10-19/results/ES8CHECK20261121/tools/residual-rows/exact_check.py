# Rationalize HiGHS LP optima and verify feasibility exactly (Fractions): slice LP = 36 even with the endpoint rows.
from fractions import Fraction as Fr
from lp_slices import *
flat=[i for i,s in enumerate(S) if s[0]==s[1]==s[2]==s[3] and s[0]>=1]
second=[S.index(t) for t in [(1,0,0,0),(1,1,0,0),(1,1,1,0),(1,1,1,1)]]
R=base+extra
for T in (19,20,21):
    rows=R+[(T,F),(36-T,Lo)]
    v,x=lp(rows,extra_le=[(5,flat),(3,second)],retx=True)
    q=[Fr(float(xi)).limit_denominator(1000) for xi in x]
    ok=all(0<=qi<=1 for qi in q) and q[0]==0
    ok&=all(sum(q[i] for i in sup)>=rhs for rhs,sup in rows)
    ok&=sum(q[i] for i in flat)<=5 and sum(q[i] for i in second)<=3
    print('slice',(T,36-T),'float LP',round(v,9),'rational point sum',sum(q),'exactly feasible',ok, 'max denom',max(qi.denominator for qi in q))
