from math import comb
print("C(46,8)=",comb(46,8))
E=lambda n,a,b: sum(comb(n-2,i) for i in range(n-b,a-1))
print("E(2j,j,2j):",[E(2*j,j,2*j) for j in range(2,8)])
print("E(2j-1,j,2j-1):",[E(2*j-1,j,2*j-1) for j in range(2,8)])
L=lambda k: 2**(k-2) if k%2 else 2**(k-2)-comb(k-2,k//2-1)+2
print("L(k) k=3..14:",[L(k) for k in range(3,15)])
print("Baek N(n,4,n)=C(n-1,2)+1:",{n:comb(n-1,2)+1 for n in range(5,11)})
print("pascal 9:",comb(8,2)+1+comb(9,3)," 10:",comb(9,2)+1+comb(10,3)," no Baek:",2*comb(10,3),2*comb(11,3)+2)
print("E(7,5,6)=",E(7,5,6))
print("B(h):",[comb(2*h,h-1)-(comb(2*h,h-2) if h>=2 else 0) for h in range(1,8)])
print("(2^(m-1)-1)/m:",[(m,(2**(m-1)-1)/m) for m in (3,5,7,9,11,13,15)])
print("C(n,3):",comb(64,3),comb(120,3),comb(253,3),comb(991,3),comb(16,3),comb(256,3))
print("deep halves 2C(3j-4,j-2), j=4:",2*comb(8,2))
x=3  # central size identity for k=6+2x
for x in range(0,6):
    k=6+2*x
    lhs=2*sum(comb(2*x+4,l) for l in range(x+1))+2*comb(2*x+3,x)+4*comb(2*x+2,x)+8*comb(2*x+1,x)
    print(k,lhs,2**(k-2),lhs==2**(k-2))
# compat k list
def isprime(n):
    if n<2: return False
    i=2
    while i*i<=n:
        if n%i==0: return False
        i+=1
    return True
ks=[m+1 for m in range(2,700) if pow(2,m-1,m) in (0,1)]
print("compatible k<=700:",ks[:20],"... composites odd m:",[m for m in range(3,700,2) if pow(2,m-1,m)==1 and not isprime(m)])
print("9-fold:",[9*t+e for t in (28,) for e in (0,1)], "2^8 mod 9 =",pow(2,8,9), "32 mod 6=",32%6)
