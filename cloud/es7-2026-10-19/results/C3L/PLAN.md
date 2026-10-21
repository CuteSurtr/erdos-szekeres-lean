# C3L plan: the 3-fold base CNF in Lean

Source of truth: `results/C3a/c3cnf.py` (`C3Enc(m, k)` with the defaults `sb = True`,
`xsig = False`, `gon = "chain"`, `acy = False`), called by `results/C3-S/tools/gen_case.py m k none`.
For ES(7) on 33 points: m = 11, n = 3m = 33, k = 7, header `p cnf 168399 4154921`.

Set-up (from the c3cnf.py docstring and `C3-S/soundness.md`): S is R-invariant, R = rotation by
+120° about the centre c (the origin), c ∉ S. A line l through c avoiding S is the y-axis.
φ(x, y) = (y/x, 1/x) maps S to S'. Labels 0..n-1 by increasing X' = y/x; then R(i) = (i − m) mod n
and σ_i = [x_i < 0] satisfies σ_{r+m} = 1 − σ_r, σ_{r+2m} = σ_r.

## Variables (in allocation order) and their Lean definitions

All in `C3Encoding/Gen.lean`, namespace `C3`. `rot m i = (i + 2m) % 3m` is R, `eps m i` is ε_i.

| Python | meaning | count (m=11,k=7) | Lean |
|---|---|---|---|
| `C[t]` | χ'(t), orientation of S' on sorted triples; one var per R-orbit, `C(R t) = parity · ε_iε_jε_k · C(t)` | 1826 | `orbits m true 0`, `Tables.C`, `Tables.Cl` |
| `s[r]`, r < m | σ_r; `sig(i)` = ±s[i mod m] (negated iff i div m = 1) | 11 | `Tables.s`, `Tables.sig` |
| `inv[i,j]`, i<j | Y'_i > Y'_j | 528 | `Tables.inv`, `Tables.invv` |
| `B[i,j]`, i<j | i left of j in S (`B(p,q) = −B(q,p)`) | 528 | `Tables.Bv`, `Tables.Bvv`, `Tables.B` |
| `T[t]` | χ_S(t) (true = ccw) per R-orbit, factor 1 | 1826 | `orbits m false _`, `Tables.T`, `Tables.Tl`, `Tables.ccw` |
| `Y[x,b,c]` | c right of x and (x,b,c) ccw | n(n−1)(n−2) = 32736 | `chainVars` (first component) |
| `W[r][x,a,b]`, 2 ≤ r ≤ k−2 | a chain x ∣ p1..pr ending a,b, angularly increasing about x, left turns inside | 4 · 32736 | `chainVars` (second component) |

Total 1826 + 11 + 528 + 528 + 1826 + 5 · 32736 = 168399 (`C3.numVars 11 7`).
Literal tables are arrays indexed by `key3 n i j k = (i n + j) n + k`; `orbits` follows
`_orbits` exactly (a new variable at the lexicographically first unseen triple, then three steps
of R, only unset entries written), so the variable numbers are Python's.

## Clause families (in file order) and their Lean definitions

Every clause goes through `addCl` = `C3Enc.add` (tautologies dropped, distinct literals sorted by
|·|); `push` appends it.

| section | clauses | count (m=11,k=7) | Lean |
|---|---|---|---|
| `sig` | signotope axioms on χ': for every 4-set, the 4 triple literals s0..s3 and every p<q<r of 0..3, `[-sp, sq, -sr]`, `[sp, -sq, sr]`; a clause equal (as a sorted tuple) to an earlier one is skipped | ≤ 8 · C(33,4) | `secSig` |
| `sb` | `¬σ_0` | 1 | `secSb` |
| `prefix` | for i<j<k with c = C(ijk), a,b,d = inv(ij), inv(ik), inv(jk): `[-c,-b,a] [-c,-d,b] [c,-b,d] [c,-a,b]` | 4 · C(33,3) | `secPrefix` |
| `forced` | `[σi, ¬σj, inv]`, `[¬σi, σj, ¬inv]` | 2 · C(33,2) | `secForced` |
| `xorB` | XOR(B_ij, inv_ij, σ_i, σ_j) = 0 via `xor0` | ≤ 8 per pair | `secXorB`, `xor0` |
| `xorT` | XOR(T, C, σ_i, σ_j, σ_k) = 0, once per T-variable at its orbit representative | ≤ 16 per orbit | `secXorT` |
| `Y` | `[¬B(x,c), ¬ccw(x,b,c), Y(x,b,c)]` | 32736 | `secChain` (1st loop) |
| `W` | `[¬B(x,a), ¬Y(x,a,b), W2(x,a,b)]`; then for 2 ≤ r ≤ k−3: `[¬Wr(x,a,b), ¬Y(x,b,c), ¬ccw(a,b,c), W(r+1)(x,b,c)]` | | `secChain` (2nd, 3rd loops) |
| `gon` | `[¬W(k−2)(x,a,b), ¬Y(x,b,c), ¬ccw(a,b,c)]`, collected during `W`, written last | | `secChain` (last loop) |

`xor0` reproduces the Python dict order (first occurrence of each |literal|, cancelling repeated
variables, e.g. σ_i and σ_{i+m}) and the `itertools.product` order (first variable most
significant). `baseClauses m k` is the composition of the sections; `Emit.lean` only formats.

Case units (`C3Encoding/Case.lean`): `parseLayers` = `parse_layers`, `layerOrder` = `layer_order`,
`layerUnits` = `layer_clauses` (σ units for two-orbit layers with r ≠ 0, then `ccw(u,v,w)` for every
consecutive pair (u,v) of the layer and every w not in an earlier layer, w ∉ {u,v}). The node CNF
of `close_node.py`/`compose.py` is the base file with these literals appended as unit clauses and
the header count increased.

## Status

* Done: `baseClauses` / `c3_dimacs base m k` byte-identical to `gen_case.py m k none` for
  m = 2..5 × k = 5..8, (6,7), (7,7), (11,7) (`logs/compare_base.log`).
* Done: `c3_dimacs node 11 7 DIR NAME…` matches `cnf_sha256` of `C3-S/manifest_depth2.tsv` for
  all 1641 nodes (`logs/compare_nodes.log`: 40 nodes with unit counts;
  `logs/compare_all_nodes.log`: every node).

## Next: the soundness statement

To prove (Mathlib side, in a separate module so the generator stays Mathlib-free):

```lean
/-- Every 3-fold-symmetric 33-point set in general position without a convex 7-gon, labelled as
in `C3-S/soundness.md` (Lemma 2: l = y-axis avoids S, labels by increasing y/x, σ_0 = 0),
satisfies the base CNF. -/
theorem c3_base_sound (P : ℕ → Point)
    (hR   : ∀ i < 33, P (C3.rot 11 i) = rot120 (P i))     -- R acts on labels as i ↦ i − m
    (hx   : ∀ i < 33, P i 0 ≠ 0)                          -- l avoids S (and c ∉ S)
    (hlab : ∀ i j, i < j → j < 33 → P i 1 / P i 0 < P j 1 / P j 0)
    (hsb  : 0 < P 0 0)                                    -- σ_0 = 0
    (hgp  : GeneralPosition (ptSet P 33))
    (hno  : ¬ HasConvexNGon 7 (ptSet P 33)) :
    DimacsSatisfiable (C3.baseClauses 11 7).toList
```

with the witness ν = "true value" of each variable (decoded through `orbits`/`chainVars`; the
needed facts are that each variable number has a unique preimage, proved once for the tables,
in the style of `numberMap_getD`/`decode_numberMap` in `results/H/ETVEncoding/Dimacs.lean`).
Lemma list, by family:

1. Tables: `orbits` is consistent on every orbit, i.e. `Cl (R t) = parity · ε · Cl t` and
   `Tl (R t) = parity · Tl t` (by `decide` on m = 11, or a general proof), and the true χ', χ_S
   satisfy these identities (R is a rotation: χ_S is R-invariant; φ∘R vs R: the ε factor).
2. `sig`: S' = φ(S) is x-sorted by X', so χ' is a signotope — `isSignotope_sigOf`
   (`H/ETVEncoding/Points.lean`) with `XSorted`; the clause shapes are `sig4`/`tri3`
   (`H/ETVEncoding/Clauses.lean`), and dedup/`addCl` only remove clauses.
3. `sb`: hypothesis `hsb`; the WLOG is Lemma 2(b) (point reflection), cf. `reflY`,
   `orient_reflY` (`H/ETVEncoding/Hull.lean`) for the reflection pattern.
4. `prefix`: the inversion pattern of a triple of an x-sorted set vs. its orientation (new,
   elementary: for X'_i < X'_j < X'_k the sign of χ' decides which inversion patterns occur).
5. `forced`, `xorB`, `xorT`: sign identities. `orient(φp, φq, φr) = orient(p,q,r)/(x_p x_q x_r)`
   (rows (1, y/x, 1/x) = (1/x)(x, y, 1), a cyclic column permutation), which gives T = C ⊕ σ's;
   B_ij = inv_ij ⊕ σ_i ⊕ σ_j similarly from 1/x. `xor0` correctness: a generic lemma
   "ν satisfies `xor0 lits` iff the parity of `lits` under ν is even" (by `decide` on the ≤ 5
   variables after cancellation).
6. `Y`, `W`: Horn definitions — set ν(Y), ν(W r) to the true chain predicates; each clause is
   an implication that holds by construction.
7. `gon`: a chain x ∣ p1..p(k−1) right of x, angularly increasing about x with left turns, is a
   convex k-gon. Reuse `orient_proj`, `orient_from`, `HullFrame`, `hasConvexNGon_of_hasGon'`,
   `HasGon.vertices`, `gon_middle` (`H/ETVEncoding/Hull.lean`, `Gon.lean`): projecting from x
   (as `HullFrame` does from the hull point 0) turns the chain into a cup of the x-sorted
   projected set; `exists_hullFrame_at` (`H3/MirrorEncoding/Frame.lean`) for the frame at x.
8. Glue: `DimacsSat`/`DimacsSatisfiable` from `H/ETVEncoding/Dimacs.lean`; for the node CNFs
   (`layerUnits`), Lemma 3 of `C3-S/soundness.md` (hull edges ⇒ `ccw` units) on top of
   `layerOrder` = angular order (Lemma 1), and `V2-L`-style `withUnits` to attach units.
