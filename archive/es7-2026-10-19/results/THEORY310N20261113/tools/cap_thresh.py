import sys
sys.argv=[sys.argv[0]]
from cap_lp import *
RS, RC = res['states'], res['constraints']; BS, BC = bal['states'], bal['constraints']
F=fam(RS,lambda s:s[0]>=5); Lo=fam(RS,lambda s:s[0]<=4)
Hi=fam(BS,lambda s:s[0]==5); Him=fam(BS,lambda s:s[4]>=1); BLo=fam(BS,lambda s:s[0]<=4); Lom=fam(BS,lambda s:s[4]==0)
def resLP(cF=None,cLo=None):
    ex=[]
    if cF is not None: ex.append({'support':F,'rhs':len(F)-cF})
    if cLo is not None: ex.append({'support':Lo,'rhs':len(Lo)-cLo})
    return lp(RS,RC,ex,True)[0]
def balLP(c, fams):
    return lp(BS,BC,[{'support':X,'rhs':len(X)-c} for X in fams],False)[0]
print('residual F only:')
for c in range(54,63): print('  c',c,'LP %.4f'%resLP(cF=c))
print('residual F with Lo at ETV 50 / cup-cap 70:')
for c in range(54,66,2): print('  c',c,'LP %.4f / %.4f'%(resLP(cF=c,cLo=50),resLP(cF=c,cLo=70)))
print('balanced Hi only:')
for c in range(72,80): print('  c',c,'LP %.4f'%balLP(c,[Hi]))
print('balanced Hi+Lo (both halves of H_6 split, same capacity by reflection):')
for c in range(76,96,2): print('  c',c,'LP %.4f'%balLP(c,[Hi,BLo]))
print('balanced Hi+Him+Lo+Lom:')
for c in range(80,100,2): print('  c',c,'LP %.4f'%balLP(c,[Hi,Him,BLo,Lom]))
