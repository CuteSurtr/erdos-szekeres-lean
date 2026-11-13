from sympy import symbols, Integer
from sympy.solvers.simplex import lpmax, InfeasibleLPError
a,b,d,tt=symbols('a b d tt',real=True)
cons=[a-b+tt<=0, b-d+tt<=0, d-a-2+tt<=0, 1-(d-a)+tt<=0, b-a-1+tt<=0, a+1-b<=0, tt<=1]
print(cons)
v,pt=lpmax(tt,cons); print(v,pt)
print([c.subs(pt) for c in cons])
# shift variables to be nonnegative to test whether free variables are the problem
A,B,Dv,T=symbols('A B D T',nonnegative=True)
M=10
sub={a:A-M,b:B-M,d:Dv-M,tt:T-M}
cons2=[c.subs(sub) for c in cons]+[A>=0,B>=0,Dv>=0,T>=0]
try:
    v2,pt2=lpmax(T-M,cons2); print('shifted',v2,pt2)
except InfeasibleLPError: print('shifted infeasible')
