#!/usr/bin/env python3
"""Chord lemma clause family (radius-free orientation rules) for C7UPPER/gen.py Enc(6,8,10).

LEMMA (written proof).  Let q1 = (j,k1), q2 = (j,k2) be two vertices of the same layer j (regular hexagon of
radius rho about O), with ccw angular separation phi = 60*((k2-k1) mod 6) in {60,120,180} degrees, and let n be the
unit normal of the line q1q2 pointing away from O (for phi = 180 deg: the normal on the clockwise side, n = rotation of
q1/|q1| by -90 deg).  The line is {x : x.n = rho*cos(phi/2)}, and O is on the side x.n < rho*cos(phi/2), which is the
LEFT side of the directed segment q1->q2 (for phi < 180).  Hence for any point p with p.n <= 0 (and p not on the line):
orient(q1,q2,p) = +.  For phi = 180 deg the line passes through O, orient(q1,-q1,p) = -2 det(q1,p), so with n the clockwise normal
orient = sign(p.n) exactly.
p.n <= 0 iff the direction of p makes an angle >= 90 deg with n.  Directions: (i,l) has angle theta_i + 60 l with
theta_0 = 0 and theta_i in (0,60) for i >= 1 (generic, pairwise distinct).  The angle between p = (i,l) and n is
  delta + 60*(l - k1) - (phi/2 - 90) ... computed below exactly as an interval in delta = theta_i - theta_j,
and the sign of delta is the phase literal (Y(j,i) / Y(i,j), or fixed when a layer is 0, or 0 when i = j).
A rule is emitted only when the condition holds for EVERY delta in the open interval allowed by the phase literal,
so each clause is: (phase literal false) OR (orientation literal).  No radius assumption is used at all.
"""
import importlib.util, itertools, json, sys, math, random
import os, pathlib
R=os.environ.get('ES_RESULTS', str(pathlib.Path(__file__).resolve().parents[2]))
s=importlib.util.spec_from_file_location('g', R+'/C7UPPER/gen.py'); G=importlib.util.module_from_spec(s); s.loader.exec_module(G)
E=G.Enc(6,8,10); NL=10
def ylit_lt(i,j):
    """literal (or True/False) for theta_i < theta_j, layers i != j"""
    return E.ylit(i,j)   # gen.py: psi_i < psi_j ; psi = theta for even m
def rules():
    out=[]   # (orientation literal, condition literal or None)
    for j in range(NL):
        for d in (1,2,3):
            phi=60*d
            for k1 in range(6):
                q1=6*j+k1; q2=6*j+(k1+d)%6
                # outward normal direction of chord q1->q2 (ccw): bisector angle + 0 for phi<180;  for phi=180 the
                # clockwise normal: angle(q1) - 90.  bisector of q1,q2 = theta_j + 60*k1 + phi/2
                for i in range(NL):
                    for l in range(6):
                        p=6*i+l
                        if p in (q1,q2): continue
                        # angle(p) - angle(n) = (theta_i - theta_j) + 60*l - 60*k1 - phi/2  (phi < 180)
                        #                     = (theta_i - theta_j) + 60*l - 60*k1 + 90     (phi = 180)
                        base = 60*l - 60*k1 - (phi/2 if d<3 else -90)
                        # delta range by phase literal
                        cases=[]
                        if i==j: cases=[(None,(0.0,0.0))]
                        elif j==0: cases=[(None,(0.0,60.0))] if True else []      # theta_i in (0,60), theta_0 = 0
                        elif i==0: cases=[(None,(-60.0,0.0))]
                        else:
                            lt=ylit_lt(i,j)   # theta_i < theta_j  -> delta in (-60,0)
                            cases=[(lt,(-60.0,0.0)),(-lt,(0.0,60.0))]
                        for cond,(lo,hi) in cases:
                            a_lo=base+lo; a_hi=base+hi   # open interval of the angle (closed if lo==hi)
                            # normalise to (-180,180]
                            def inside_ge90(a1,a2):
                                # True if every angle in [a1,a2] has cos <= 0 (|angle| >= 90 mod 360)
                                for sh in range(-3,4):
                                    lo2,hi2=a1+360*sh,a2+360*sh
                                    if 90<=lo2 and hi2<=270: return True
                                return False
                            def inside_lt90(a1,a2):
                                for sh in range(-3,4):
                                    lo2,hi2=a1+360*sh,a2+360*sh
                                    if -90<=lo2 and hi2<=90 and not (lo2==-90 or hi2==90 and lo==hi): return True
                                return False
                            oriented=E.o(q1,q2,p)
                            if d<3:
                                if inside_ge90(a_lo,a_hi): out.append((oriented,cond))       # p.n <= 0: O's side
                            else:   # diameter q1 -> -q1, n = clockwise normal: orient = + iff p.n > 0
                                if inside_lt90(a_lo,a_hi): out.append((oriented,cond))
                                elif inside_ge90(a_lo,a_hi): out.append((-oriented,cond))
    return out
def clauses():
    cl=set()
    for lit,cond in rules():
        if cond is None: c=(lit,)
        elif cond is True: c=(lit,)
        elif cond is False: continue
        else: c=tuple(sorted((lit,-cond),key=abs))
        cl.add(c)
    # a rule that holds under both phase orders is unconditional: merge (L or y), (L or -y) into the unit (L)
    units={c[0] for c in cl if len(c)==1}
    for c in list(cl):
        if len(c)==2:
            L=[x for x in c if abs(x)<=E.ntriplevars][0]; y=[x for x in c if abs(x)>E.ntriplevars][0]
            if tuple(sorted((L,-y),key=abs)) in cl: units.add(L)
    cl={c for c in cl if len(c)==1 or not any(x in units for x in c)} | {(u,) for u in units}
    return sorted(cl,key=lambda c:[abs(x) for x in c])
if __name__=='__main__':
    C=clauses()
    units=[c for c in C if len(c)==1]; bins=[c for c in C if len(c)==2]
    print('clauses', len(C), 'units', len(units), 'binary', len(bins))
    # contradiction check: a unit and its negation?
    U=set(c[0] for c in units); print('conflicting units:', sum(1 for u in U if -u in U))
    # compare with the encoder's own unit clauses (its forced literals)
    with open(sys.argv[1] if len(sys.argv)>1 else '/dev/null','w') as f:
        for c in C: f.write(' '.join(map(str,c))+' 0\n')
