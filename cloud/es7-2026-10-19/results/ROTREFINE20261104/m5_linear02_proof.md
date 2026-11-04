# Shared-centre pentagon identity

4 November 2026 (KST).

**Written proof (reviewed, not refereed):** put `a=5`, `b_j=45+j`, `c_j=50+j`, and `tau=(sqrt(5)-1)/2`. Take the common rotation centre as the origin. Regular pentagons in either direction satisfy

```text
c_0 + tau*(c_2+c_3) = 0,
b_3-b_4-b_0+b_1 = sqrt(5)*b_2,
det(b_3,b_4) = det(b_0,b_1).
```

Write `b_j=b_0*zeta^j` and `c_j=c_0*zeta^j`, where `zeta=exp(+-2*pi*i/5)`. Then `tau=zeta+zeta^4`, `sqrt(5)=1+2*tau`, and `1+zeta+zeta^2+zeta^3+zeta^4=0` give `tau*(zeta^2+zeta^3)=-1` and `zeta^3-zeta^4-1+zeta=sqrt(5)*zeta^2`. These prove the first two vector identities. The third follows because a common rotation preserves determinants.

Consequently

```text
[a,b_3,b_4] - [a,b_0,b_1] = sqrt(5)*det(a,b_2),
[a,b_2,c_0] + tau*([a,b_2,c_2]+[a,b_2,c_3])
    = det(b_2-a,-sqrt(5)*a) = sqrt(5)*det(a,b_2).
```

Subtracting gives the five-row identity. In the source model the first four brackets `[a,b_0,b_1]`, `[a,b_2,c_0]`, `[a,b_2,c_2]`, `[a,b_2,c_3]` are negative while `[a,b_3,b_4]` is positive, contradicting the displayed equality with positive coefficients. Multiplying by `2*sqrt(5)-4` gives the witness weights, since `(7-3*sqrt(5))/(2*sqrt(5)-4)=tau`. This proof uses the common pentagon centre and neither layer ordering nor phase inequalities.

The source-variable binding, formal polynomial checks, and finite exact tests are recorded separately in `m5_linear02.json`, `m5_linear02_verified.json`, and [the campaign report](m5_REPORT.md). This geometric derivation does not depend on the linear-programming search.
