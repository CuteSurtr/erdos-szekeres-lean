#!/usr/bin/env python3
"""Parent replay of the theory worker's eight-point exposure example."""
from fractions import Fraction as Q
from itertools import combinations as C
from pathlib import Path
import hashlib,importlib.util,json,resource
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('parent_geometry',HERE.parent/'boundary/check_envelope.py');G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G)
def main():
 resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20));resource.setrlimit(resource.RLIMIT_CPU,(18,18))
 P5=[(0,0),(1,1),(2,0),(3,4),(4,-3),(5,10),(6,-2),(7,5)];P3=P5[:-1]+[(7,3)];A=(0,3,6);records=[]
 dets=[]
 for t in C(range(8),3):
  lo=G.det(P3,*t);hi=G.det(P5,*t);assert lo*hi>0;dets.append({'triple':t,'h3':lo,'h5':hi})
 for h,P in [(3,P3),(5,P5)]:
  caps=[t for t in C(range(8),4) if G.cap(P,t)];assert caps==[(0,1,2,4),(2,3,5,6),(2,3,5,7)]
  full=G.maxima(P,range(8));blue=G.maxima(P,[i for i in range(8) if i not in A]);assert full==(4,4,6) and blue[2]<6
  q=G.line(P,(3,6));assert q==(Q(-2),Q(-4));lines=[G.line(P,K[-2:]) for K in caps]
  records.append({'h':h,'full_maxima':full,'complement_maxima':blue,'fourcaps':caps,'q':list(map(str,q)),'ambient_lines':[list(map(str,l)) for l in lines]})
  if h==5:
   assert tuple((lines[0][i]+lines[2][i])/2 for i in [0,1])==(q[0],q[1]+Q(11,4))
   for ell,t in zip(lines,[Q(1),Q(1),Q(19)]):assert q[0]*t+q[1]>ell[0]*t+ell[1]
  else:
   lower=Q(0);upper=None
   for u,w in lines:
    s,z=q
    if s==u:assert z>w
    elif s>u:lower=max(lower,(w-z)/(s-u))
    else:upper=(w-z)/(s-u) if upper is None else min(upper,(w-z)/(s-u))
   assert (lower,upper)==(Q(14,3),Q(7))
   assert q[0]*6+q[1]==-16 and max(u*6+w for u,w in lines)==Q(-33,2)
 # Scale the insertion coordinates to integers before checking all geometry.
 S=[(4*x,4*y) for x,y in P3]+[(52,-65)];full=G.maxima(S,range(9));assert full==(4,4,6)
 assert G.cap(S,(0,3,6,8))
 blue=G.maxima(S,[i for i in range(9) if i not in A]);assert blue[2]<6
 # Every old determinant is affine in the only varying y-coordinate.
 # Equal strict endpoint signs therefore establish orientation invariance on [3,5].
 out={'label':'COMPUTED independent exact geometry and arithmetic replay','verdict':'PASS','cases':records,'determinants':dets,'orientation_family':'All determinants are affine in h and have equal nonzero signs at h=3,5; hence signs stay fixed for 3<=h<=5.','insertion_scaled_integer_points':S,'insertion_full_maxima':full,'unchanged_A_complement_maxima':blue,'A_plus_r_has_fourcap':True,'unchanged_A_still_weak_Delta':True,'scope':'Individual specified Delta uniform-extension property changes. Neither global uniform-selection failure nor monotone weak-Delta failure is asserted.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'geometry_sha256':hashlib.sha256((HERE.parent/'boundary/check_envelope.py').read_bytes()).hexdigest()}
 dest=HERE/'data/line_example_parent.json';dest.parent.mkdir(exist_ok=True);assert not dest.exists();dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'verdict':'PASS','orientation_triples':len(dets),'full_maxima':full}))
if __name__=='__main__':main()
