# Exact acceptance and possible algebraic obstruction

No obstruction or realization is asserted by this methods file.

## Integer-coordinate acceptance

The target signs are indexed by the 560 increasing triples of labels
0 through 15, in lexicographic order. A candidate is accepted only when
its x coordinates increase strictly and all determinants

`(x_j-x_i)(y_k-y_i) - (y_j-y_i)(x_k-x_i)`

are nonzero and have exactly the prescribed signs. Positive, separate
integer scalings of the two axes preserve every determinant sign.
`verify.py` repeats this test with the expanded shoelace expression,
without importing a finder or numerical package.

For the direct algebraic search, the normalization p0=(0,0), p15=(1,0)
loses no x-ordered realization: translate and positively scale x, then
subtract the affine line through these two points from y. Since
`det(p0,p1,p15)=-y1`, general position makes y1 nonzero. A further positive
y scaling sets y1 to minus the requested sign of (0,1,15).
The search imposes no bounds on the other y coordinates.
An unsuccessful Z3 run is not used as a nonrealizability certificate.

## Strict product inequalities

Write `[a b c]` for the real determinant of three homogeneous point
coordinates, retaining the order of the labels. For five distinct labels,
the exact Grassmann--Pluecker identity is

`[a b c][a d e] - [a b d][a c e] + [a b e][a c d] = 0`.

All bracket factors are nonzero for a realization of the prescribed
uniform orientation model. Include the displayed minus sign in the sign
of the middle term. If exactly one of the three signed terms has one sign
and the other two have the opposite sign, the magnitude of that unique
term equals the sum of the other two magnitudes. Consequently its product
of bracket magnitudes is strictly larger than each of the other products.

`product_obstruction.py` enumerates these implications for every common
label and every four-element subset of the other labels. It seeks positive
integer powers of some of these inequalities whose bracket exponents
cancel exactly. An LP is used only to propose the powers. Rational
reconstruction and integer exponent summation must succeed before the
finder writes a certificate.

If the left and right exponents cancel, multiplying the selected strict
inequalities gives `X > X`, where X is a positive product of nonzero
bracket magnitudes. This is an explicit algebraic contradiction to any
real realization. It does not depend on x order, terminal selectors, or
any floating-point or optimization verdict.

`verify_product.py` imports no finder code. It reconstructs the ordered
bracket signs using its own permutation routine, checks the unique-sign
condition in each identity, checks that every power is a positive integer,
and accumulates all exponents independently. Only exact zero cancellation
accepts. Claimed coefficient arrays in the finder certificate are ignored
by this checker. Failure to find such a certificate leaves realizability
unresolved; this certificate class is not a complete decision method.
