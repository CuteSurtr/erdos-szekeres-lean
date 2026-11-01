import sys, os, random, subprocess, math, itertools
OUT=sys.argv[1]; TMP=os.path.join(OUT,'tmp_test'); os.makedirs(TMP,exist_ok=True)
rng=random.Random(777)
def orient_int(P,a,b,c):
    (x1,y1),(x2,y2),(x3,y3)=P[a],P[b],P[c]; d=(x2-x1)*(y3-y1)-(y2-y1)*(x3-x1); return (d>0)-(d<0)
fails=0; hist={}
for trial in range(150):
    n=rng.randint(10,17)
    while True:
        pts=set()
        while len(pts)<n:
            t=rng.random()*2*math.pi; r=1000*(1 if rng.random()<0.6 else rng.random())
            if trial%2: pts.add((rng.randint(-1000,1000),rng.randint(-1000,1000)))
            else: pts.add((round(r*math.cos(t)),round(r*math.sin(t))))
        P=list(pts)
        if all(orient_int(P,a,b,c)!=0 for a,b,c in itertools.combinations(range(n),3)): break
    path=os.path.join(TMP,'e.otab')
    with open(path,'wb') as f:
        f.write(('%d\n'%n).encode()); f.write(bytes((orient_int(P,a,b,c)&0xFF) for a in range(n) for b in range(n) for c in range(n)))
    K=10
    e=subprocess.run([os.path.join(OUT,'cvxenum'),path,str(K)],capture_output=True,text=True).stdout
    b=subprocess.run([os.path.join(OUT,'bf'),path,str(K)],capture_output=True,text=True).stdout
    E={int(l.split()[2].split('-')[0]):int(l.split()[3]) for l in e.splitlines()}
    B={int(l.split()[2].split('-')[0]):int(l.split()[3]) for l in b.splitlines()}
    mk=max([k for k in B if B[k]] or [0]); hist[mk]=hist.get(mk,0)+1
    if E!=B: fails+=1; print('MISMATCH',E,B)
print('enum vs bf: 150 sets, mismatches',fails,'largest-convex histogram',sorted(hist.items()))
