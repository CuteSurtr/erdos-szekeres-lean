**Verdict: CONFIRMED** (claim `lp0-7-w19-nonreal`, verifier V1, 15 November 2026, 17:39 KST). Label EXACT is supported:
the certificate is a valid exact biquadratic-final-polynomial (BFP) certificate for the plain 19-point chirotope of W, so
W is not realizable by any configuration of 19 points in the plane (x-sorted or not).

# VERIFY_LP0_7_W19_NONREAL: P2's LP0(7) counterexample W is not realizable

## Claim checked (filed by R7)

W (claim `lp0-7-false-abstract`; `pm1115/p2/lp0cex/w19_real17_oonn.json`, key `signs`, 969 characters, sign-string
SHA-256 `a0e6cecd…4e4d8d`) carries a BFP certificate of 686 three-term Grassmann-Plücker inequalities with positive integer
multipliers (largest 6079363803590194724270684251130) whose weighted sum is the zero linear form, with no point at
infinity; hence no planar realization exists.

## Why the certificate proves it (checked)

For any realization p_i = (1, x_i, y_i) (or any vectors of R^3) the brackets [ijk] = det(p_i,p_j,p_k) have the signs of
the chirotope and are nonzero; the three-term relation [abc][ade] − [abd][ace] + [abe][acd] = 0 holds for all five
vectors. If one term has the sign opposite to the other two, its absolute value is the sum of theirs, so strictly larger
than each: log|T_odd| > log|T_other|. A positive integer combination of these strict inequalities whose bracket exponents
cancel says 0 > 0. No V is used, so this excludes every point configuration with this chirotope; and since each term is a
product of two brackets, it also excludes the mirror image (all signs reversed).

## Method (own code `v1_bfp_generic.py`, a generic form of V1's earlier `v1_bfp_check.py`; written before reading R7's `certcheck.py`)

- Input hashes equal the claim: `w19_real17_oonn.json` `834da5f8…a7e7`; R7's copy `r7/lp0/w19_real17_oonn_in.json`
  `1ac51532…0e01` has the same sign string; certificate `r7/lp0/bfp_oonn_full_noV.json` `8b7257fa…56b7`.
- The 969-character string gives 19 points; its SHA-256 is
  `a0e6cecd0ea8d58728a3b7565d7f587ce7c9c486e4cbc6642f3c7fa3c34e4d8d` as stated; the certificate has n = 19,
  withV = false, and its `sig` equals the model's string (the check itself uses the model's string).
- Per item: five distinct indices, odd ≠ other, positive integer multiplier; the signs of T0 = [abc][ade],
  T1 = −[abd][ace], T2 = [abe][acd] from the string (unsorted bracket = sorted sign × permutation parity); T_odd must
  differ from both others; +mult on the two brackets of T_odd, −mult on the two of T_other (unordered triples).
- Self-test: the GP identity holds exactly on 2,000 random integer 5-tuples of Z^3.
- Negative control: 60 random integer 19-point sets in general position (any order; realizable by construction) must
  each fail some sign condition of the certificate.

## Results (`v1_bfp_generic.out`, SHA-256 `985f1aabda1cc4756bb2997095804dced51e7add01b14962c218729e42303c00`)

| items | sign failures | bracket exponents | brackets involved | largest multiplier | realizable controls passing |
|---|---|---|---|---|---|
| 686 | **0** | **all cancel** | 724 | 6079363803590194724270684251130 | **0 of 60** |

## Comparison (after the check)

`r7/tools/certcheck.py` rebuilds the chirotope from the model and applies the same rule (sign of the odd term, positive
integer multipliers, exponent totals zero). Results agree. (`lp0-7-false-abstract` itself has a CONFIRMED verdict.)

## Not checked

The search context in the claim (LP slack of the cells, `realize_sig.py` run) is information only.

Code: `/home/jay/research/data/roadmap-20261115/pm1115/v1/lp0-7-w19-nonreal/v1_bfp_generic.py` (SHA-256
`14911622e1dd7f0e30f44ad72a3d7068f6ba6c5c6372431ed0c512588283ab3e`). Rerun (0.3 s):
`python3 -I v1_bfp_generic.py p2/lp0cex/w19_real17_oonn.json r7/lp0/bfp_oonn_full_noV.json`. No git action, no unit, no
other repository file written.
