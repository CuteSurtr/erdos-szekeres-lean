import math
from fractions import Fraction as F
from check import *

def normalize(P):
    xs=[p[0] for p in P]; ys=[p[1] for p in P]
    x0,x1=min(xs),max(xs); y0=min(ys)
    if len(P)==1: return [(F(0),F(0))]
    w=x1-x0
    Q=[((x-x0)/w,(y-y0)/w) for x,y in P]
    ms=max(abs((b[1]-a[1])/(b[0]-a[0])) for a,b in itertools.combinations(Q,2))
    if ms>1: Q=[(x,y/ms) for x,y in Q]
    return Q

def Pau(a,u):
    if a==2 or u==2: return [(F(0),F(0))]
    L=normalize(Pau(a,u-1)); R=normalize(Pau(a-1,u))
    pts=L+[(x+2,y+10) for x,y in R]
    return normalize(pts)

def ES(k,delta=F(1,1000)):
    pts=[]
    for i in range(2,k+1):
        C=normalize(Pau(k-i+2,i))
        cx,cy=F(i),F(i*i)
        pts+= [(cx+delta*x, cy+delta*y) for x,y in C]
    return pts

s5=math.sin(2*math.pi/5); c5=math.cos(2*math.pi/5)
def r5(p,k):
    x,y=p
    for _ in range(k): x,y=x*c5-y*s5, x*s5+y*c5
    return (x,y)
five=[r5((-12,-17),4),(-12,-17),r5((-12,-17),1),r5((-12,-17),2),r5((-12,-17),3),
      (-15,2),r5((-15,2),1),r5((-15,2),2),r5((-15,2),3),r5((-15,2),4),
      (-13,0),r5((-13,0),1),r5((-13,0),2),r5((-13,0),3),r5((-13,0),4),(0.0,0.0)]
four=[(-30,0),(0,-30),(30,0),(0,30),(-20,-3.5),(3.5,-20),(20,3.5),(-3.5,20),(-13,-6),(6,-13),(13,6),(-6,13),(-1.9,-1.2),(1.2,-1.9),(1.9,1.2),(-1.2,1.9)]
