**Verdict: CONFIRMED** (claim `root7-m17-t3-nonrealizable`, verifier V1, 15 November 2026, 14:11 KST). Label EXACT is
supported: both certificates are valid exact biquadratic-final-polynomial certificates, so T3's signotope root7_m17_s1
has no x-sorted real realization. (V2 confirmed a similarly worded claim, `root7-m17-nonreal-1`, in
`VERIFY_ROOT7_M17_NONREAL1.md`; this file is V1's separate check of T1's claim.)

# VERIFY_ROOT7_M17_NONREAL: T3's abstract ROOT(7) counterexample is not realizable with its x-order

## Claim checked (filed by T1)

The sub-signotope of root7_m17_s1 on the points 6, 7, 8, 9, 10, 11, 13, 14, 16, with the vertical point at infinity V
(χ(a,b,V) = + for a < b), has a biquadratic-final-polynomial (BFP) certificate of 27 three-term Grassmann-Plücker
inequalities, all with multiplier 1; the full 18-element configuration (17 points + V) has one with 486 inequalities. So
the model is not the signotope of any real point set, and gives no real counterexample to ROOT(7). (Without V no
certificate was found; that is information, not claimed.)

## Why such a certificate proves non-realizability (checked)

Write p_i = (1, x_i, y_i) and V = (0, 0, 1); [abc] = det. Then [a b c] = orient(a,b,c) for points, and
[a b V] = x_b − x_a, which is > 0 for a < b in an x-sorted realization. The three-term relation
[abc][ade] − [abd][ace] + [abe][acd] = 0 holds for all vectors of R^3 (fix a; it is the 2-D Plücker identity in
R^3/⟨a⟩). In a realization in general position all brackets are nonzero, so if term T_odd has the sign opposite to the
other two, |T_odd| = |T_x| + |T_y| > |T_other|. Multiplying the stated inequalities with their positive integer
exponents gives a strict inequality between two monomials in the |brackets|; if every bracket's exponent cancels, the
two monomials are equal, a contradiction. Restricting an x-sorted realization of the 17 points to 9 of them keeps it
x-sorted, so the 10-element certificate already suffices.

## Method (own code `v1_bfp_check.py`, written before reading T1's `t1lib.check_cert`)

1. `t1/models/r7m17_t3.json` is byte-identical to `t3/models/root7_m17_s1.json` (file SHA-256 `8d6bedc1…`); its
   680-character sign string has SHA-256 `72a678a9c704fc635b9fa393fecd08a2bd88bba93afbd23a16438296d9a19f5f`, as stated.
2. `sub_signs` of `r7m17_t3_sub_cert.json` (`0b7b7945…`) equals the model restricted to [6,7,8,9,10,11,13,14,16],
   re-indexed 0..8, with element 9 = V and '+' on every bracket containing it: **match**.
3. For each certificate item (a,b,c,d,e, odd, other; mult): the five elements are distinct, mult is a positive integer,
   odd ≠ other; the signs of T0 = [abc][ade], T1 = −[abd][ace], T2 = [abe][acd] are computed from the chirotope (an
   unsorted bracket gets the sign of the sorted one times the permutation parity); T_odd must differ in sign from both
   others; then +mult is added to the two brackets of T_odd and −mult to the two of T_other, as unordered triples.
4. The same for `r7m17_t3_bfp_withV.json` (`26f9309b…`, n = 18): its `sig` restricted to 0..16 equals the model and is
   '+' on every triple containing 17 = V.
5. Self-tests: the GP identity holds exactly on 2,000 random integer 5-tuples of Z^3, and [a,b,V] = x_b − x_a.
6. Negative control: 200 random x-sorted integer 9-point sets + V and 50 random 17-point sets + V (realizable by
   construction) are run through the same certificates; each must fail some sign condition.

## Results (`v1_bfp_check.out`, SHA-256 `73500683578718a17b4fa571db134eaa612676dfc1ec1bfac1d167796d26524a`)

| certificate | elements | items | sign conditions | exponents cancel | multipliers |
|---|---|---|---|---|---|
| sub (points 6-11, 13, 14, 16 + V) | 10 | 27 | **all hold** | **yes** | all 1 |
| full (17 points + V) | 18 | 486 | **all hold** | **yes** | positive integers from 1,745,184,192,451,300 to 809,691,278,645,088,737 |

Negative control: **0 of 250** realizable configurations pass a certificate, as required.

So root7_m17_s1 has no x-sorted real realization; this abstract counterexample (`VERIFY_ROOT7_M17.md`) does not give a
real counterexample to ROOT(7). Whether a real 17-point counterexample exists is open.

## Comparison (after the check)

`t1/tools/t1lib.py` `check_cert` applies the same rule (sign of the odd term, positive integer multipliers, exponent
totals zero); results agree.

## Not checked

- The informational remark that no certificate was found without V (a search result, not a claim).
- Realizability of the order type with a different x-direction (not claimed).

Code: `/home/jay/research/data/roadmap-20261115/pm1115/v1/root7-m17-t3-nonrealizable/v1_bfp_check.py`
(SHA-256 `34f45ffe38251543a699f26e3554e796936b3367752ec321ef23f5407d25936a`). Rerun (0.2 s):
`python3 -I v1_bfp_check.py t1/models/r7m17_t3.json t1/models/r7m17_t3_sub_cert.json t1/models/r7m17_t3_bfp_withV.json`.
No git action, no unit, no other repository file written.
