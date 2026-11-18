**Verdict: CONFIRMED** (claim `root7-m17-nonreal-1`, verifier V2, 15 November 2026, 14:07-14:09 KST). Label EXACT
is correct. Every part of the statement holds.

# Independent check: T3's abstract ROOT(7) counterexample root7_m17_s1 has no x-sorted real realization

**Claim (filed by R7, 14:08).** The 680-character sign string `root7_m17_s1` (SHA-256 `72a678a9…a19f5f`) has no
x-sorted real realization. The reason given is a biquadratic final polynomial (BFP) certificate with 27 three-term
Grassmann–Plücker inequalities, all multipliers 1, on the 9-point sub-signotope [6,7,8,9,10,11,12,14,16] together with
the vertical point at infinity V. A second certificate on all 17 points + V has 486 inequalities. Non-realizability
without V is explicitly not claimed.

**Scope.** This check concerns only the realizability of the sign string. Whether the abstract ROOT(7) counterexample
itself is right is claim `root7-m17-abstract`, which is a separate verification.

## Definitions used

As in the claim, and the same as in [VERIFY_ROOT6_M15_NONREAL.md](VERIFY_ROOT6_M15_NONREAL.md):
- points p_i = (1, x_i, y_i) and V = (0,0,1);
- [abc] = orient(a,b,c) for points, and [a,b,V] = x_b − x_a > 0 for a < b;
- lexicographic signs, `+` = cup, with the parity rule for unsorted brackets;
- the 3-term GP identity, giving log|T_odd| > log|T_other| whenever T_odd's sign is opposite to both other terms;
- a positive integer combination that is identically zero gives 0 > 0.

In an x-sorted realization in general position every bracket is nonzero, including [a,b,V]. Any x-sorted realization
of the 17 points would restrict to one of the 9 points, so the certificate on the 9 points + V suffices.

## What was checked, and how (own code, integers only)

The script is `/home/jay/research/data/roadmap-20261115/pm1115/v2/root7-m17-nonreal-1/check_root7_nonreal_v2.py`
(`3eb1a1c2bd55245e22c694af450a96f5cc5bee84327b70d84cd6cc24a3fd9c01`). It uses `bfp_v2core.py`, which is a byte copy of
V2's validated checker from `root6-m15-main-nonrealizable` (`645ccfaba67c24515f4c9afbaa121244181cefe03198c7a95bb4b8df7adada9a`),
and `v2lib.py` (`7c8b1ee090252ef50435ece7e82346e3af466cf56a8a210f3317c8693fa2fea5`). It ran in about 3 s on one thread.
R7's `certcheck.py` was read only afterwards.

1. **Identity.**
   - T3's `t3/models/root7_m17_s1.json` and R7's copy `r7/root7_m17_s1.json` are byte-identical
     (`8d6bedc1…f9efebd`).
   - The sign string's SHA-256 is `72a678a9c704fc635b9fa393fecd08a2bd88bba93afbd23a16438296d9a19f5f`, as stated.
   - T3's CaDiCaL log `t3/runs/r7m17_s1.log` (`ef88d01d…22a20`) says `s SATISFIABLE`. My own decoding of its `v` lines
     (variable t = the t-th lexicographic triple, true = `+`) equals the sign string.
   - The 17-point string is a signotope: 0 of the 2,380 four-tuples violate the axiom.
2. **cert_min** (`r7/bfp/s1_min.json`, `0cc6d86a…a230fd`).
   - The header has n = 10, pts = [6,7,8,9,10,11,12,14,16] and withV = true; model_sha equals the string hash.
   - I rebuilt the sub-signature from the model's signs and appended `+` for every triple containing sub-index 9 (V).
     It equals the file's 120-character `sig`. The 9-point restriction is a signotope (0 violations).
   - The certificate has **27 items, all multipliers 1**, touching 51 brackets. In every item the stated odd term has
     the sign opposite to both other terms, and odd ≠ other. **All bracket totals are 0. Accepted.**
   - V occurs in the certificate, so it is a statement about x-sorted realizations only, as claimed.
   - The same 27 items, re-labelled into the full 17 points + V chirotope, are also accepted.
3. **cert_full** (`r7/bfp/s1_full_withV.json`, `c2a86067…8e8263`). The header has n = 18, and its `sig` equals the
   model plus V (index 17). It has **486 items**, multipliers up to 809,691,278,645,088,737. **All totals are 0.
   Accepted.**

## Controls (all PASS)

- The GP identity holds exactly on 2,000 random integer 5-tuples of vectors, some containing (0,0,1).
- The bracket conventions hold: [abc] = orient and [a,b,V] = x_b − x_a.
- The derived inequalities |T_odd| > |T_other| hold, in exact integers, for 12,716 odd-term instances in 30 random real
  x-sorted sets with V adjoined.
- **Negative controls.** Each of these corrupted inputs is rejected:
  - drop item 0;
  - set item 0's multiplier to 2;
  - swap odd and other in item 0;
  - flip the sign of a bracket the certificate uses, (0,1,8);
  - drop the last item of cert_full.

## Comparison with the filer's checker (read after my check)

`r7/tools/certcheck.py` (`a9ac06f4e7b966494e1e9135b60ac1e60da63ffc24e99a001dfa5138aed790d8`) rebuilds the
sub-chirotope from the model and applies the same rule:
- the same three terms and coefficients (1, −1, 1);
- the same parity rule;
- the same ±mult accumulation over sorted triples;
- the same range and positivity checks, although it accepts a bool multiplier.

It agrees with my result. I did not run it.

## Files

- Output: `/home/jay/research/data/roadmap-20261115/pm1115/v2/root7-m17-nonreal-1/check_root7_nonreal_v2.out.json`
  (`f9a09e88ae86a5bdadc638b3a9506cde704d063e4f6df0f04ce735e425d686cb`).
- Rerun:

```bash
cd /home/jay/research/data/roadmap-20261115/pm1115/v2/root7-m17-nonreal-1
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python check_root7_nonreal_v2.py   # exit 0, "verdict": "PASS"
```
