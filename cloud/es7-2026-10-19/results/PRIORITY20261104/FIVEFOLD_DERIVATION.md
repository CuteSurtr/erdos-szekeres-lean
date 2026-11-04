# Elementary derivation of the eight-area pentagon obstruction

4 November 2026. **Written proof plus exact computation — independently
checked, not refereed.** This derivation is part of the current review. It is
not attributed to an earlier publication and does not settle priority.

Put `s=sqrt(5)`, `phi=(1+s)/2`, and let `R` be counterclockwise rotation
by 72 degrees about the origin. Write `y_j=R^j y`, and
`[x,y,z]=det(x,y)+det(y,z)+det(z,x)` for doubled oriented triangle area.

The retained witness uses `A=13-3s`, `B=13s-15` and `C=5s-1`.
Exactly, `B=A*s` and `C=A*phi`. Since `A>0`, division by A preserves the
sign contradiction.

The rotation satisfies

```text
I + R + phi R^3 = 0,
I - R^4 + R - R^2 = -s R^3,
I + R^2 + phi R = s R.
```

These follow from the fifth-root-of-unity relation. They can also be verified
in the positively oriented basis `(1, exp(2 pi i/5))`, where

```text
R = [0  -1]
    [1  (s-1)/2].
```

Define `P(x;y)=[x,y_0,y_4]+[x,y_1,y_2]`. Its internal determinants
`det(y_0,y_4)` and `det(y_1,y_2)` cancel. The second rotation identity gives

```text
P(x;y) = det(x,y_0-y_4+y_1-y_2) = -s det(x,y_3).
```

Define

```text
Q(a;c,d) = [a,c_0,d_0] + [a,c_1,d_2] + phi [a,c_3,d_1].
```

The terms involving `a,c` vanish by the first rotation identity. The terms
involving `c,d` vanish by the same identity, because
`det(c_1,d_2)=det(c_0,d_1)` and
`det(c_3,d_1)=det(c_0,d_3)`. The remaining terms give

```text
Q(a;c,d) = det(d_0+d_2+phi d_1,a) = -s det(a,d_1).
```

Set `a=5`, `b_j=35+j`, `c_j=40+j`, and `d_j=45+j` in the retained
point labels. The normalized eight-term expression is

```text
-P(a;b) - P(b_0;d) - s [a,b_3,d_1] + Q(a;c,d)
= -[5,35,39] - [5,36,37] + [5,40,45] + [5,41,47]
  -[35,45,49] - [35,46,47] - s[5,38,46] + phi[5,43,46].
```

Expand the middle triangle and use
`det(b_3,d_1)=det(b_0,d_3)`. Every term cancels, proving the identity.
The prescribed signs in the retained source make every displayed signed term
strictly positive, so those signs cannot hold for four concentric regular
pentagon orbits. The existing campaign verifies this binding to the source;
this follow-up checks the algebraic derivation independently.

## Exact check and scope

Run `python3 -I -B check_fivefold.py`. The checker directly expands the eight
actual triangles in eight independent formal seed coordinates, using rational
pairs for `Q(sqrt(5))`. It separately checks all three rotation identities,
`R^5=I`, the coefficient normalizations, both P expressions, Q, and determinant
invariance. All eleven checks pass. No numerical solver is used.

This derivation does not show that the eight-literal sign clause follows
logically from the earlier three- or five-area clause families. It supplies a
short algebraic explanation of the retained eight-term witness. It uses the
prescribed geometric C5 action and makes no claim about arbitrary asymmetric
realizations of the abstract order type.
