import importlib.util, sys
from sympy import symbols, Integer
from sympy.solvers.simplex import lpmax, InfeasibleLPError
a,b,d,tt=symbols('a b d tt',real=True); P=Integer(1)
def lpcons(cons):
    lp=[]
    for e,rel in cons:
        if rel=='<': lp.append(e+tt<=0)
        elif rel=='<=': lp.append(e<=0)
        elif rel=='==': lp+= [e<=0,-e<=0]
    lp.append(tt<=1); return lp
lt=lambda l,r:(l-r,'<'); le=lambda l,r:(l-r,'<='); eq=lambda l,r:(l-r,'==')
order=[lt(a,b),lt(b,d),lt(d,a+2*P)]
h12=order+[lt(P,d-a)]
for nm,hyp,neg in [
 ('case1 first', h12+[lt(b-a,P)], [(-(b-(a+P)),'<=')]),
 ('case1 second', h12+[lt(b-a,P)], [(-((a+P)-d),'<=')]),
 ('case3 first', h12+[eq(b-a,P)], [(-(a-(d+P-2*P)),'<=')]),
 ('case3 second', h12+[eq(b-a,P)], [(-((d+P-2*P)-b),'<=')]),
 ('case1 hyps only', h12+[lt(b-a,P)], []),
 ('case3 hyps only', h12+[eq(b-a,P)], []),
]:
    lp=lpcons(hyp+neg)
    try:
        v=lpmax(tt,lp); print(nm,'->',v)
    except InfeasibleLPError as e:
        print(nm,'-> infeasible')
    except Exception as e:
        print(nm,'-> EXC',type(e).__name__,e)
