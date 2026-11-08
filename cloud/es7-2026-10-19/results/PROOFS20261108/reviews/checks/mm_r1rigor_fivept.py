def orient(a,b,c): return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
P=[(-18,-62),(1,66),(-88,-82),(37,-76),(-7,49)]
n=len(P)
print('turns:',[orient(P[i-1],P[i],P[(i+1)%n]) for i in range(n)])
A,B,C=(-88,-82),(37,-76),(1,66); x=(-18,-62)
print('inside triangle signs:',orient(A,B,x),orient(B,C,x),orient(C,A,x))
