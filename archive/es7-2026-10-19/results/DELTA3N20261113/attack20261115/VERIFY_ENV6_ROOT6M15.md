**Verdict: CONFIRMED** (claim `env6-fails-root6m15`, verifier V1, 15 November 2026, 13:32 KST). Label supported: EXACT,
for the abstract signotope root6_m15 only. Realizability of root6_m15 is not part of the claim and was not addressed.

# VERIFY_ENV6_ROOT6M15: ENV#(6) fails on the abstract 15-point signotope root6_m15

## Claim checked (filed by T3)

ENV#(6) fails for abstract (5,6)-valid signotopes at |U| = 15 and |U| = 14. Witness: S = root6_m15 and S − r (r = 14).
Neither has an ENV# Δ (4-cap-free, meets every convex pentagon of U, (b,c) ∈ ↑P4(U) for every 3-cap a < b < c in A).
Counts: U = S: 19 P4 pairs, 34 ↑P4 pairs, 329 pentagons, 467 weak Δs, 0 ENV# Δs; U = S − r: 9, 19, 292, 0 ENV# Δs. Side
facts: weak D(5,6) holds on S (467 weak Δs, e.g. {0,1,2,3,4,5,7}); l = 0 starts 26 four-caps; S − l has 231 weak Δs A
with A + l 4-cap-free and 206 initial-safe weak Δs; so the per-set left-or-right disjunction (rooted and terminal-safe)
holds on S although ROOT and CONJ-TS′ fail at r.

## Definitions used (from the records)

`ROUND6.md` "Definitions" and `METHODS_SWEEP.md` §3.1 (ENV#(n), P4, ⊑, ↑P4, weak Δ, gon); `CONJTS_TEST.md` §2
(terminal-safe); `VERIFY_ATN_MAIN.md` (mirror form; initial-safe = every 3-cap a < b < c of A has a 4-cap of S − l
starting with (a,b)); `DELTA2N20261113/README.md` §2 (signotope, k-cap, convex k-set by the 4-subset rule, weak gon).

## Method (own code, written before reading T3's scripts)

- Library `/home/jay/research/data/roadmap-20261115/pm1115/v1/lib/v1lib.py`
  (SHA-256 `bfeed7ee2837629d9f82a8069fb7023f0ac2a3c4ce967e19c65c8d3680d3d577`).
- Script `/home/jay/research/data/roadmap-20261115/pm1115/v1/env6-fails-root6m15/v1_env6_check.py`
  (SHA-256 `06c8bf206582e20f7f5825eb71686711d86c8d7985197cfa9349252d350e6a52`).
- Input `pm1115/t3/models/root6_m15.json`, SHA-256 `165b1b7ec1958cd373aaddd2676c46a0be0e6f835482169fab06295c57d733fe`,
  byte-identical to `round6/mainsession/root15/root6_m15.json` (the file of claim root6-m15-abstract, CONFIRMED by V3).

Steps:
1. decode the 455 signs over lexicographic triples of 0..14 ('+' = cup, '-' = cap); count signotope violations over all
   4-tuples;
2. k-caps by "every triple a cap", with the consecutive-triple form asserted equal on every subset examined; convex
   k-sets by the 4-subset rule, with the cap/cup-split (weak gon) form asserted equal on every subset examined;
3. validity: 5-caps and convex hexagons of S;
4. for U = S and U = S − r: P4(U) (also via a longest-cap dynamic program, asserted equal), the generating steps of ⊑ from
   every triple of U, the up-closure ↑P4(U), convex pentagons, all 2^|U| subsets for weak Δs, and the ENV# filter;
5. at r: 4-caps ending at r, rooted Δs (weak Δs A of S − r with A + r 4-cap-free), terminal-safe weak Δs;
6. mirror twice: directly on the original labels (4-caps starting at 0; weak Δs of S − 0; A + 0 4-cap-free;
   initial-safe), and by building the reflected order type s′(14−c, 14−b, 14−a) = s(a,b,c) and running the right-hand
   code (4-caps ending at r′, rooted, terminal-safe);
7. positive control: ENV# on the three real 13-point CONJ-TS′(6) sets (signs from exact integer coordinates, convexity
   also checked against an exact convex hull).

Runtime 0.5 s, one thread, foreground.

## Results (output `v1_env6_check.out`, SHA-256 `f539ef355120568b26e542d21d2785918742ea9ebb9c955e6a31c43b374ec44a`)

- S: 0 signotope violations, 0 five-caps, 0 convex hexagons, 98 four-caps, 43 ending at r = 14. S is a (5,6)-valid
  signotope (agrees with V3's VERIFY_ROOT6_M15.md).

| U | points | P4 pairs | ↑P4 pairs / all | 4-caps | convex pentagons | weak Δs | **ENV# Δs** |
|---|---|---|---|---|---|---|---|
| S | 15 | 19 | 34 / 105 | 98 | 329 | 467 | **0** |
| S − r | 14 | 9 | 19 / 91 | 55 | 292 | 709 | **0** |

- {0,1,2,3,4,5,7} is a weak Δ of S, so weak D(5,6) holds on S (467 weak Δs).
- At r: 0 rooted Δs and 0 terminal-safe weak Δs (ROOT and CONJ-TS′ fail at r, as claimed; 709 weak Δs of S − r equals
  V3's count).
- Mirror (l = 0): 26 four-caps start at l; S − l has 230 convex pentagons and 447 weak Δs, of which **231** have A + l
  4-cap-free and **206** are initial-safe. The reflected-order-type computation gives 26 / 447 / 231 / 206 as well.
- Controls: ENV# Δs (S / S − r) = 719 / 208 (lattice-hyp), 1,431 / 467 (flat-hyp), 1,437 / 508 (lattice-nohyp), equal to
  `VERIFY_ATN_MAIN.md` and to `VERIFY_CTS6_REAL.md`.

**Every number in the claim is reproduced exactly.** ENV#(6) fails for the abstract (5,6)-valid signotopes S (15 points)
and S − r (14 points); both are valid since S is. The left-or-right disjunction holds on S in both versions.

## Comparison with T3's code (read after the check above)

`pm1115/t3/tools/check_forms.py`, `t3lib.py`, output `pm1115/t3/runs/root6_m15.forms.json`
(SHA-256 `26aeef0f…a668b`). Same definitions. Differences in code path only: T3 adds all three relations of each triple's
chain to ⊑ directly, this check adds the two covering steps and closes; T3 computes h_U and the starting-pair lengths by
dynamic programs, this check enumerates 4-caps (with a DP cross-check for h_U); this check also runs the mirror on the
reflected order type. All counts agree, including T3's minimum weak Δ example and left-rooted count.

## Not checked / limits

- Abstract signotope only: whether root6_m15 is realizable by points is open here, so this does not refute ENV#(6) for
  real point sets.
- ENV#(6) for abstract U with |U| ≤ 13 was not examined here.

Rerun:

```bash
cd /home/jay/research/data/roadmap-20261115/pm1115/v1/env6-fails-root6m15
D=/home/jay/research/data/roadmap-20261115/round6/mainsession/cts6real
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I v1_env6_check.py \
  /home/jay/research/data/roadmap-20261115/pm1115/t3/models/root6_m15.json \
  $D/lattice-hyp_real_s1.json $D/flat-hyp_real_s1.json $D/lattice-nohyp_real_s1.json
```

No git action, no unit started, no other repository file written.
