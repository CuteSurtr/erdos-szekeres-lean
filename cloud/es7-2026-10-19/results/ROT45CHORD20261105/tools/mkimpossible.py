import sys, itertools, json, importlib.util, os
R='<results-dir>'
s=importlib.util.spec_from_file_location('g', R+'/C7UPPER/gen.py'); G=importlib.util.module_from_spec(s); s.loader.exec_module(G)
m,t,base,chord,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3],sys.argv[4],sys.argv[5]
E=G.Enc(m,8,t); os.makedirs(out,exist_ok=True)
body=open(base).read(); first=body.index('\n'); hdr=body[:first].split(); nv,nc=int(hdr[2]),int(hdr[3]); body=body[first+1:]
ch=open(chord).read(); nch=ch.count('\n')
pairs=list(itertools.combinations([1,2,3,4],2)); sym=[E.H[1]] if m%2 else [E.Y[(1,2)]]
cons=set()
for perm in itertools.permutations([1,2,3,4]):
    pos={L:r for r,L in enumerate(perm)}; cons.add(tuple(pos[i]<pos[j] for i,j in pairs))
n=0; allpat=[]
for bits in itertools.product([True,False],repeat=6):
    if m%2==0 and not bits[0]: continue          # Y(1,2) is the symmetry unit for even m
    allpat.append(bits)
    if bits in cons: continue
    units=sym+[E.Y[p] if b else -E.Y[p] for p,b in zip(pairs,bits)]
    name='x'+''.join('1' if b else '0' for b in bits)
    with open(os.path.join(out,name+'.cnf'),'w') as f:
        f.write('p cnf %d %d\n'%(nv,nc+nch+len(units))); f.write(body); f.write(ch)
        for u in units: f.write('%d 0\n'%u)
    n+=1
print('patterns (after symmetry unit)', len(allpat), 'consistent', sum(1 for b in allpat if b in cons), 'impossible cubes written', n)
