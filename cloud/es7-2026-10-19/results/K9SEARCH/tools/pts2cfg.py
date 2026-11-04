import sys, cmath, math
m=8; z=cmath.exp(2j*math.pi/m)
rows=[[int(v) for v in l.split()] for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
for o in range(len(rows)//m):
    w=rows[o*m]; p=sum(c*z**j for j,c in enumerate(w))
    print("%.17g %.17g"%(math.log(abs(p)), cmath.phase(p)))
