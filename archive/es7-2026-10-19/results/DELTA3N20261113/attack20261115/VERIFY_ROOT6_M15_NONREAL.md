**Verdict: CONFIRMED** (claim `root6-m15-main-nonrealizable`, verifier V2, 15 November 2026, 13:45-13:50 KST).
Label EXACT is correct. Every part of the statement holds: (i), (ii) and the consequence.

# Independent check: the main session's m = 15 ROOT(6) model has no real realization

**Claim (filed by T1, 13:45).** The sign string of the main session's abstract ROOT(6) counterexample `root6_m15`
(string SHA-256 `b99b6999…8dfe1`) has no x-sorted real realization:
- (i) its 15-point chirotope, with no point at infinity, carries a biquadratic final polynomial (BFP) certificate of
  288 three-term Grassmann–Plücker inequalities, so no point configuration realizes it;
- (ii) the 8-point sub-signotope on points 2, 3, 4, 6, 7, 8, 9, 12 plus the vertical point at infinity V carries one
  with 23 inequalities, all multipliers 1, so that 8-point signotope has no x-sorted realization;
- consequence: "every abstract signotope on ≤ 8 points is realizable" is false for x-sorted realizations.

## Definitions used (from the claim, not from the filer's code)

- Points are p_i = (1, x_i, y_i) and V = (0, 0, 1). The bracket [ijk] = det(p_i, p_j, p_k) equals orient(i,j,k) for
  points, and [a,b,V] = x_b − x_a, which is > 0 for a < b in an x-sorted set.
- Signs: lexicographic triples a < b < c, `+` = orient > 0 (cup). An unsorted bracket has the sorted sign times the
  permutation parity.
- For five distinct vectors: [abc][ade] − [abd][ace] + [abe][acd] = 0. Call the terms T0, T1, T2.
- If the signs force T_odd to be opposite to both other terms, then in any realization with all brackets nonzero
  |T_odd| = |T_x| + |T_y| > |T_other|. With L = log|·| (a function of the unordered triple), this reads
  L(odd brackets) − L(other brackets) > 0. A positive integer combination that is identically zero gives 0 > 0.
- All brackets are nonzero in a realization of a uniform chirotope, and [a,b,V] ≠ 0 because x is distinct.

I re-derived this argument by hand. It needs no other lemma.

## What was checked, and how

Own script `/home/jay/research/data/roadmap-20261115/pm1115/v2/root6-m15-main-nonrealizable/check_bfp_v2.py`
(SHA-256 `645ccfaba67c24515f4c9afbaa121244181cefe03198c7a95bb4b8df7adada9a`), with V2's helper `v2lib.py` in the
same folder (`7c8b1ee090252ef50435ece7e82346e3af466cf56a8a210f3317c8693fa2fea5`). Integers only. It ran in about 3 s
on one thread. The filer's `t1lib.check_cert` and `bfp.verify_certificate` were read only after this check was done.

1. **Identity of the object.**
   - `t1/models/m15_main.json` and `round6/mainsession/root15/root6_m15.json` have the same SHA-256
     `165b1b7e…d733fe`, as the claim says.
   - The SHA-256 of the 455-character sign string is `b99b699947453288ed38b9e08a66e78a75f8301f489920d46d15348dbd28dfe1`,
     as stated.
   - I decoded the `v` lines of `round6/mainsession/root6/cert15/root6_m15.cadical.log` myself: variable t = the t-th
     lexicographic triple, true = `+`. The result equals the sign string. So the certificates concern the actual
     CaDiCaL model.
   - The string is a signotope: 0 of the 1,365 four-tuples violate the axiom.
2. **Certificate checker.** For each item `tag = (a,b,c,d,e,odd,other)`, `mult`, the script checks:
   - a..e are five distinct elements in range;
   - odd and other are in {0,1,2} and differ;
   - mult is a positive integer, not a bool;
   - the sign of T_odd, computed from the sign string with permutation parity, is opposite to both other terms.

   It then adds mult to the two brackets of T_odd and subtracts it from the two brackets of T_other, keyed by
   unordered triple. It requires every total to be 0.
3. **(i), 15 points, no V** (`m15_main_bfp_noV.json`). The certificate's `sig` equals the model. It has **288 items**,
   all valid, multipliers 1 to 23,003,671,369, touching 308 brackets. **All totals are 0. Accepted.**
4. **(ii), 8 points + V** (`m15_main_sub8V_cert.json`).
   - `points` = [2,3,4,6,7,8,9,12].
   - `sub8_signs` equals my restriction of the model to these points, re-indexed 0..7. It is a signotope (0 violations).
   - `sub8V_signs` equals that restriction plus element 8 = V with `+` on every triple (a,b,8).
   - The certificate has **23 items, all multipliers 1**, touching 40 brackets. **All totals are 0. Accepted.**
5. **For information:** `m15_main_bfp_withV.json` (15 points + V). Its `sig` equals the model plus V, and its
   398 items are also accepted.
6. **Consequence.** By (ii), and because the 8-point restriction is a genuine signotope, some 8-point signotope has
   no x-sorted realization. The consequence follows. The record's further remark that every signotope on ≤ 7 points is
   realizable rests on Goodman–Pollack (literature), and I did not check it.

## Controls (all PASS)

- The GP identity holds exactly on 2,000 random integer 5-tuples of vectors, about 30 % of them containing (0,0,1).
- [abc] = orient(a,b,c) for (1,x,y) vectors, and [a,b,V] = x_b − x_a, on 500 random cases.
- **Soundness of the derived inequalities on real data.** I used 30 random integer x-sorted sets of 6-8 points with V
  adjoined:
  - the chirotope built by my code (`+` on (a,b,V)) equals the exact determinant signs;
  - for 12,716 sampled ordered 5-tuples where the signs make a term odd, the exact values satisfy |T_odd| > |T_other|
    for both other terms.
- **Negative controls.** Each of these corrupted inputs is rejected:
  - drop the first item;
  - change one multiplier;
  - swap odd and other;
  - flip the sign of a bracket the certificate uses, (0,2,V);
  - drop the last item of the 288;
  - add 1 to one large multiplier.

## Comparison with the filer's checkers (read after my check)

`t1/tools/t1lib.py` `check_cert` (`933953f7…`) and `t1/tools/bfp.py` `verify_certificate` (`147b3690…`) use the same
term definitions, parity rule and accumulation as mine, and they reach the same accept verdicts. There are two minor
differences, neither of which matters for these files:
- theirs accept a bool multiplier, and mine rejects one;
- theirs reject out-of-range elements only through a KeyError.

The filer's self-test covers points only. Mine also covers brackets with V.

## Scope

- This check proves non-realizability of this one sign string (and of its 8-point restriction for x-sorted sets).
- It says nothing about the other 21 models T1 realized, or about the claim `root6-real-15`.
- Global sign convention: each GP term is a product of two brackets, so reflecting all signs (including V, i.e.
  V = (0,0,−1)) leaves every term sign unchanged. The certificates therefore also refute the mirror image.

## Files

- Output: `/home/jay/research/data/roadmap-20261115/pm1115/v2/root6-m15-main-nonrealizable/check_bfp_v2.out.json`
  (`c8e2b7a24b35ee6b3becb14df71edf80aefce1a26c3aa8a8c4fca9391a5be0dd`).
- Inputs (SHA-256):
  - `m15_main.json` `165b1b7ec1958cd373aaddd2676c46a0be0e6f835482169fab06295c57d733fe`;
  - `m15_main_bfp_noV.json` `4d219796e23d927b8f39f8df513ab24f2ffcff542da2b163d0a3b758afad2382`;
  - `m15_main_sub8V_cert.json` `9335f5538284cc1b6651c72db3803d3ec018f1525922c42ccfe59b47948c049d`;
  - `m15_main_bfp_withV.json` `a30f2d03c1d444bd4cb853f2dbda08805784f802a5b49e130abc651ac4618586`;
  - `root6_m15.cadical.log` `6641f3519e3c6eccd97ae32970ccfecf4607db3b9bad2d036df5a9934b14a0ea`.
- Rerun:

```bash
cd /home/jay/research/data/roadmap-20261115/pm1115/v2/root6-m15-main-nonrealizable
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python check_bfp_v2.py   # exit 0, "verdict": "PASS"
```
