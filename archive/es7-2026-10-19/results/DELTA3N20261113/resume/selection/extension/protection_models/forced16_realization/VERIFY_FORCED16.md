# Verification of the fixed forced16 nonrealizability obstruction

**PROVED:** no sixteen real planar points in general position realize the
560 increasing-triple signs in `data/orientation.signs`, whose SHA-256 is
`b21664b06887c4019d75023025b1cd80582064a0b06f53698d2a70bc8fc49067`.
This is a written algebraic proof with independently replayed exact
arithmetic. It is not a Lean-kernel result or an LRAT certificate.

## Statement and conventions

Labels are 0 through 15. The signs are indexed by lexicographically ordered
increasing triples. For ordered labels a,b,c, write `[a b c]` for the
determinant of the rows `(x_a,y_a,1)`, `(x_b,y_b,1)`, `(x_c,y_c,1)`.
Reordering labels multiplies the sign by the permutation parity. Any
realization of these signs has every bracket nonzero.

The statement excludes arbitrary real coordinates, even without imposing
increasing x. It therefore excludes the requested x-ordered realization.
It makes no assertion about different sixteen-point orientation models.

## Algebraic proof

Assume such a real realization exists. For five distinct labels,

`T0 = [a b c][a d e]`,

`T1 = -[a b d][a c e]`,

`T2 = [a b e][a c d]`

satisfy `T0 + T1 + T2 = 0`. This follows by translating point a to the
origin and expanding the two-dimensional determinants; it is the
Grassmann--Pluecker relation with common label a.

Each of the 387 certificate rows supplies these five labels, a term L,
another term S, and a positive integer weight w. The independent replay
checks from the target signs that TL has the unique sign among the three
terms and TS has the opposite sign. Because the remaining term also has
the opposite sign and all terms are nonzero,

`abs(TL) = abs(TS) + abs(T_remaining) > abs(TS) > 0`.

Raise this inequality to w and multiply over all rows. Positivity of the
factors and weights gives a strict inequality between the products.
Each factor is an absolute bracket. The independent replay checks, in
integers, that every one of the 560 absolute-bracket exponents has net
contribution zero. The two products are therefore the same positive
quantity X. The resulting `X > X` is impossible. This proves the claim.

For example, the first certificate row uses `(a,b,c,d,e)=(0,1,4,11,14)`,
L=2 and S=1, so its checked implication is

`|[0 1 14][0 4 11]| > |[0 1 11][0 4 14]|`,

with positive weight 68,695,051,218,518. The complete list, including all
weights, is in `data/certificate.json`; the independently reconstructed
factor tuples are in `data/independent-replay.json`.

## Exact finite checks

`verify_product.py` uses only Python's standard library and integer
arithmetic. It imports no finder. It checks:

1. The target input contains exactly 560 valid signs and matches the
   certificate's SHA-256.
2. Every row has five distinct labels in 0 through 15.
3. An independently implemented permutation routine gives the signs of
   all six ordered bracket factors, including the minus in T1.
4. L has the unique sign, S has the opposite sign, and w is a strictly
   positive integer.
5. The sum of weighted exponents is exactly zero for every bracket.

The checker ignores the finder's claimed coefficient arrays and exponent
summary, rebuilding both from the raw labels and selected terms.

Receipt: **PASS**, 387 rows, weight sum 19,282,471,848,322,771, all exponents
cancel. All weights are positive; minimum 1,433,869,918,829, maximum
228,087,592,790,168, gcd 1. All sixteen labels occur. No claim that this
certificate or its label support is minimal is needed or made.

Exact reconstruction of the LP-proposed support had rank 386 and nullity
one. Sparse integer elimination and rational back substitution took
0.250 seconds with 56,556 KiB peak process RSS. The certificate's validity
does not depend on that reconstruction algorithm or on any solver status.

## Controls and retained failures

Two real sixteen-point controls use direct expanded determinants: the
parabola `(i,i^2)` and an asymmetric integer set retained in
`data/controls.json`. All determinants are nonzero. For each point set,
every common label and every quadruple of other labels is checked:
21,840 exact identities and 43,680 derived strict inequalities. Both sets
pass, giving 43,680 identities and 87,360 inequalities total.

Two deliberate corruptions of the accepted certificate are retained in
scratch. Increasing one weight by one is rejected by exponent
cancellation. Reversing one selected inequality is rejected by the
unique-sign check. Neither creates an accepted receipt.

Earlier coordinate searches found no witness. The LP-probe's initial
per-float rational reconstruction also failed. Those negative outcomes
remain archived. Neither those failures nor the Z3 `unknown` response
prove nonrealizability; only the algebraic contradiction above does.

## Artifact integrity and limits

- Certificate SHA-256:
  `cfe42cec6041709b2ed7ac18ee16b13e57f091239ac19b8e5257aac46d2a326d`.
- Independent replay SHA-256:
  `8ae4462877b5b0d0113de8e3f234f51b8a0f87038319fdb5757d900fe490849c`.
- Checker SHA-256:
  `3ae6b1b1d7bf1ae4b3714853788822630b6fed2bd7b2c54141fe284905d040ba`.

`data/manifest.json` records all archived data hashes. Sources and full
search logs remain in the owned record and scratch tree. The argument
does not alter the parent's checks of the abstract SAT model. A valid
abstract model can satisfy those checks while lacking real coordinates.
Other real configurations and the general selector question remain
outside this result.
