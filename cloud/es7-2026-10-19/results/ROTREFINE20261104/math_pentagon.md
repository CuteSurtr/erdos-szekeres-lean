# Independent check of the pentagon parallel-chord identity

4 November 2026 (KST).

**Written proof (reviewed, not refereed).** Let `b0,b1,b2,b3,b4` be the consecutive vertices of a regular pentagon, in either rotational direction, and let `a` be any point. Put `phi=(1+sqrt(5))/2`. Then

```
b3-b0 = phi*(b2-b1).
```

For example, write the vertices as `c+z*zeta^j`, where `zeta^5=1` is a primitive fifth root corresponding to a 72-degree rotation. Since `phi=1+zeta+zeta^4`, direct multiplication gives

```
phi*(zeta^2-zeta) = zeta^3-1.
```

The same equation holds for the conjugate root, so reversing the rotational direction does not change the positive factor.

Using `[pqr]=det(q-p,r-p)`, the elementary four-point area identity and the chord relation give

```
[a,b0,b3]+[b0,b1,b3]
  = [a,b1,b3]+[a,b0,b1]
  = det(b1-a,b3-b0)
  = phi*[a,b1,b2].
```

Because `(5-sqrt(5))*phi=2*sqrt(5)`, this is precisely

```
(5-sqrt(5))*[a,b0,b3]
-2*sqrt(5)*[a,b1,b2]
+(5-sqrt(5))*[b0,b1,b3] = 0.
```

Both coefficient magnitudes are strictly positive. Thus the three required signs `+,-,+` are impossible in general position: all three displayed signed terms would be positive, but their sum is zero. Their simultaneous reversal is impossible for the same reason. No nesting, phase-order assumption, or radius ordering is used.

For the quoted fivefold labels, substitute `a=0` and `(b0,b1,b2,b3)=(50,51,52,53)`. This note independently checks the mathematical identity and its sign implication. The numerical variable-map binding, exact certified 56-point tests, and emitted clause-family hashes belong to the separate fivefold verification records.
