#!/usr/bin/env python3
"""Cube files for the m-fold threshold instance with the chord-lemma clauses.
Each cube = base CNF + chord_new clauses + symmetry unit (H(1) for odd m, Y(1,2) for even m, as in C7UPPER/ROT456/C6UPPER)
+ the phase-order literals Y(i,j), 1<=i<j<=4, of one total order of psi_1..psi_4 (consistent with the unit).
The cover: for odd m every order of layers 1..4 (24); for even m every order with psi_1 < psi_2 (12).  Orders that violate
transitivity are omitted here; they are refuted by the base CNF's transitivity clauses (C6UPPER/ROT456 checked this)."""
import sys, itertools, json, importlib.util, os
R='<results-dir>'
s=importlib.util.spec_from_file_location('g', R+'/C7UPPER/gen.py'); G=importlib.util.module_from_spec(s); s.loader.exec_module(G)
m,t,base,chord,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],sys.argv[4],sys.argv[5]
E=G.Enc(m,8,t); os.makedirs(out,exist_ok=True)
hdr=None; body=open(base).read(); first=body.index('\n'); hdr=body[:first].split(); nv,nc=int(hdr[2]),int(hdr[3]); body=body[first+1:]
ch=open(chord).read(); nch=ch.count('\n')
sym=[E.H[1]] if m%2 else [E.Y[(1,2)]]
man=[]
for perm in itertools.permutations([1,2,3,4]):
    pos={L:r for r,L in enumerate(perm)}
    if m%2==0 and pos[1]>pos[2]: continue
    lits=[E.Y[(i,j)] if pos[i]<pos[j] else -E.Y[(i,j)] for i,j in itertools.combinations([1,2,3,4],2)]
    name='o'+''.join(map(str,perm))
    units=sym+lits
    with open(os.path.join(out,name+'.cnf'),'w') as f:
        f.write('p cnf %d %d\n' % (nv, nc+nch+len(units))); f.write(body); f.write(ch)
        for u in units: f.write('%d 0\n' % u)
    man.append({'cube':name,'order':list(perm),'units':units})
json.dump({'m':m,'t':t,'base':base,'chord':chord,'cubes':man},open(os.path.join(out,'manifest.json'),'w'),indent=1)
print('cubes', len(man))
