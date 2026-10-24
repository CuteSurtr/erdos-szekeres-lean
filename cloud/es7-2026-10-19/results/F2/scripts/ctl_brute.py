import sys, itertools, random, subprocess
sys.path.insert(0, "/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/tools/realizer")
from chiro import largest_convex_subset
def bits(pts):
    pts = sorted(pts); n = len(pts)
    return "".join("1" if (pts[b][0]-pts[a][0])*(pts[c][1]-pts[a][1])-(pts[b][1]-pts[a][1])*(pts[c][0]-pts[a][0])>0 else "0" for a,b,c in itertools.combinations(range(n),3))
def capcup(pts):
    pts=sorted(pts); n=len(pts); best={1:2,-1:2}
    L={}
    for j in range(n):
        for k in range(j+1,n):
            for s in (1,-1):
                v=2
                for i in range(j):
                    d=(pts[j][0]-pts[i][0])*(pts[k][1]-pts[i][1])-(pts[j][1]-pts[i][1])*(pts[k][0]-pts[i][0])
                    if (d>0)==(s>0): v=max(v,L[(i,j,s)]+1)
                L[(j,k,s)]=v; best[s]=max(best[s],v)
    return best[-1], best[1]
sets=[]
lines=open("/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/inputs/distinct_K7.txt").readlines()
random.seed(1)
for l in random.sample(lines,5):
    t=l.split(); t=t[t.index("32"):]; n=int(t[0]); v=list(map(int,t[1:1+2*n])); pts=[(v[2*i],v[2*i+1]) for i in range(n)]
    L=2*max(abs(y) for x,y in pts)+1; pts=[(L*x+y,y) for x,y in pts]; sets.append(pts[:26])
for k in range(5):
    sets.append([(random.randint(0,10**6),random.randint(0,10**6)) for _ in range(26)])
inp="\n".join(bits(p) for p in sets)+"\n"
out=subprocess.run(["./brute","26","40"],input=inp,capture_output=True,text=True).stdout.split("\n")
for p,o in zip(sets,out):
    print(o, "| python cap,cup,lcs:", capcup(p), largest_convex_subset(p))
