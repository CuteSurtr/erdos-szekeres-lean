from math import comb
def etv_baek(n, a, b):      # Baek: N(n,a,b) = sum_{i=n-b}^{a-2} C(n-2,i), a-cap, b-cup, n-gon
    return sum(comb(n-2, i) for i in range(n-b, a-1))
def etv_bv(a, u, k):        # Balko-Valtr: N(a,u,k) = sum_{i=k-a+2}^{u} C(k-2,i-2)
    return sum(comb(k-2, i-2) for i in range(k-a+2, u+1))
# conventions agree on all triplets 2<=a,b<=n<=a+b-2, n<=14
bad = [(n,a,b) for n in range(3,15) for a in range(2,n+1) for b in range(2,n+1)
       if n <= a+b-2 and etv_baek(n,a,b) != etv_bv(a,b,n)]
print("convention mismatches:", bad)
# symmetry in caps/cups
print("cap/cup symmetric:", all(etv_baek(n,a,b)==etv_baek(n,b,a) for n in range(3,15) for a in range(2,n+1) for b in range(2,n+1) if n<=a+b-2))
# trivial range n >= a+b-3 equals cups-caps C(a+b-4,a-2)
print("trivial range = cups-caps:", all(etv_baek(n,a,b)==comb(a+b-4,a-2) for n in range(3,15) for a in range(2,n+1) for b in range(2,n+1) if a+b-3<=n<=a+b-2))
# Baek case a=4,b=n: N = C(n-1,2)+1
print("N(n,4,n)=C(n-1,2)+1:", all(etv_baek(n,4,n)==comb(n-1,2)+1 for n in range(4,30)))
print("N(n,n,n)=2^(n-2):", all(etv_baek(n,n,n)==2**(n-2) for n in range(3,30)))
print()
print(" j  k=2j  r_j(ETV)  closed form  trivial(n>=a+b-3)?  cups-caps bound C(3j-4,j-2)  mirror conj 2r+2  2^(k-2)-C(k-2,k/2-1)+2  2^(k-2)")
for j in range(2, 9):
    k = 2*j
    r = etv_baek(k, j, k)
    closed = (2**(2*j-2) - comb(2*j-2, j-1))//2
    assert (2**(2*j-2) - comb(2*j-2, j-1)) % 2 == 0
    trivial = k >= j + k - 3
    cc = comb(j + k - 4, j - 2)
    m = 2*r + 2
    f = 2**(k-2) - comb(k-2, k//2-1) + 2
    print(f"{j:2d} {k:4d} {r:8d} {closed:11d} {str(trivial):>18s} {cc:24d} {m:16d} {f:22d} {2**(k-2):8d}")
print()
print("Balko-Valtr Prop 3.2 bound N(4,k,k) <= C(k,2)-1 at k=7,8:", comb(7,2)-1, comb(8,2)-1)
print("ETV values cited: (7,5,6)=",etv_baek(7,5,6)," (7,5,7)=",etv_baek(7,5,7)," (7,4,7)=",etv_baek(7,4,7)," (9,4,9)=",etv_baek(9,4,9))
print("Mojarrad-Vlachos ES(10) bound C(15,8)-C(12,7)+2 =", comb(15,8)-comb(12,7)+2)
print("r_5 threshold for mirror sets below 2^(k-2) at k=10: need 2r+2 < 256 -> r <= ", (256-3)//2)
