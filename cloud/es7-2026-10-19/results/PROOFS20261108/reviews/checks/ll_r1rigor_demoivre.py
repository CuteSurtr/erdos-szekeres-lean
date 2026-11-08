import sympy as sp, random
al = sp.symbols('alpha', real=True); I = sp.I
for j in range(0, 9):
    e1 = sp.powsimp(sp.exp(I*al)**j - sp.exp(I*j*al), force=True)
    lhs = sp.expand((sp.cos(al) + I*sp.sin(al))**j)
    rhs = sp.expand_trig(sp.cos(j*al) + I*sp.sin(j*al))
    d = sp.simplify(sp.expand(lhs - rhs).rewrite(sp.exp))
    nums = [abs(complex(((sp.cos(x)+I*sp.sin(x))**j - (sp.cos(j*x)+I*sp.sin(j*x))).evalf())) for x in [random.uniform(-7,7) for _ in range(5)]]
    print(j, 'exp-form residual', e1, '| trig residual', d, '| max numeric', max(nums))
