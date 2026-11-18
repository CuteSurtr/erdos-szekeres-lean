**Verdict: CONFIRMED** (claim `env6-real-14-15`, filed by T4; verifier V3, 15 November 2026, 13:47-13:52 KST).
- The labels are correct: EXACT for the 0 counts, PROVED for the two corollaries (given the CONFIRMED claim root6-real-15).
- **ENV#(6) is false for real point sets with 14 and with 15 points.**

# Independent check: ENV#(6) fails on the real 15-point ROOT(6) counterexamples

**Claim.** The claim concerns the 21 distinct real 15-point sets of claim root6-real-15: `t1/root6_real15.json`, which is the
same point set as `m15_it8_real.json`, and the 20 further files `t1/real/m15_it*_real.json`. For each set:
- neither U = S nor U = S − r has an ENV# Δ;
- by corollary, VE(6) and condition (U) fail at U = S − r;
- the least failing size of ENV#(6) is not determined.

**Definitions used.** From ROUND6.md, "Definitions used below", and METHODS_SWEEP.md §3.1, with n = 6.
- P4(U): the pairs (c,d) that end a 4-cap (a,b,c,d) of U.
- The order ⊑ is generated, for each triple i<j<k of U, by:
  - (j,k) ⊑ (i,k) ⊑ (i,j) when the triple is a cup;
  - (i,j) ⊑ (i,k) ⊑ (j,k) when it is a cap.
- ↑P4(U): every q with p ⊑ q for some p ∈ P4, computed as reachability along the generating steps.
- ENV# Δ of U: a 4-cap-free A that meets every convex pentagon of U and has (b,c) ∈ ↑P4(U) for every 3-cap a<b<c inside A.
- Computation: everything comes from the integer coordinates, with exact orient. Convex position is tested directly
  on each k-set: no point strictly inside a triangle of three others.

## Results (own code, run before reading T4's code or output)

**Positive control** (the three real 13-point sets of VERIFY_ATN_MAIN.md, `round6/mainsession/cts6real/*_real_s1.json`).
My ENV# counts for S / S − r reproduce the published table exactly:

| set | S | S − r |
|---|---|---|
| lattice-nohyp | 1,437 | 508 |
| lattice-hyp | 719 | 208 |
| flat-hyp | 1,431 | 467 |

**The 22 files** (21 distinct point sets and 21 distinct order types; root6_real15.json and m15_it8_real.json have
identical P):

| quantity | U = S (15 points) | U = S − r (14 points) |
|---|---|---|
| (5,6)-valid (0 five-caps, 0 convex hexagons) | 22/22 | 22/22 (subsets) |
| 4-caps | 78-88 | 49 |
| \|↑P4\| out of the 105 or 91 pairs | 33-39 | 20 |
| 3-caps with (b,c) ∉ ↑P4 | 31-42 | 54-55 |
| convex pentagons | 289-317 | 254 or 262 |
| weak Δs | 409-600 | 992 or 990 |
| **ENV# Δs, exhaustive over 2^15 and 2^14 subsets** | **0 in all 22** | **0 in all 22** |

- The 21 sets of S − r fall into only **2 distinct 14-point order types**, which are the two profiles 254 / 992 and
  262 / 990. So the 14-point failure has 2 distinct witnesses, and the 15-point failure has 21.
- The S − r part also follows from root6-real-15 by itself. An ENV# Δ A of U has A + r 4-cap-free for every 5-cap-free
  right extension r, because the cap set of r is a ⊑-down-set disjoint from P4, hence from ↑P4. I re-derived this
  from the 4-tuple axiom. So my count of 0 rooted weak Δs for the same sets (VERIFY_ROOT6_REAL15.md) forces 0 here, and
  my direct count agrees. The 15-point part (U = S) is independent of that.

**Corollaries (PROVED, re-derived from the definitions).**
- **VE(6)** (METHODS_SWEEP §3.1: ENV# with r ranging only over valid real insertions). The actual r is a real point to
  the right of U = S − r, and U + r = S is (5,6)-valid. A VE solution would therefore be a weak Δ of U with A + r
  4-cap-free, and root6-real-15 (CONFIRMED by V3) says none exists.
- **(U)** (VERIFICATION.md P1: A ∪ {r} must be a weak Δ of U ∪ {r} for every real r to the right of U with U ∪ {r} in
  general position and 5-cap-free). The same r qualifies, and the same contradiction follows.
- Both corollaries hold for the 14-point real U = S − r.

**"The least failing size is not determined."**
- The records and work folders contain no ENV#(6) certification at any size. A grep of all records and of `round6/`
  and `pm1115/` finds only ENV#(7) CNFs and proofs (|U| ≤ 13) and per-set checks of ENV#(6).
- The implication ENV# at |U| = m ⟹ ROOT at |S| = m + 1 does not run backwards, so the CERTIFIED ROOT(6) for |S| ≤ 14
  says nothing about ENV#(6) at |U| ≤ 13.
- The smallest failing size is therefore somewhere at or below 14, and not known. Correct as stated.

**Comparison (read after my run).**
- T4's `real15/envS.jsonl` gives env_S = 0 and env_U = 0 and valid_S = true for all 22 files, the same as mine.
- T4's `t4lib.py` `up_P4` (`97ad9fb6…941`) states the same order and up-closure; `envS.py` is `7307a534…629`.
- No difference to explain.

**Scope.** ENV#(6) is refuted at 14 and 15 real points. Nothing is claimed or checked here about ENV#(7), ENV#(8),
weak D(5,n) or any ES bound.

## Code and outputs (`/home/jay/research/data/roadmap-20261115/pm1115/v3/env6-real-14-15/`)

| file | SHA-256 |
|---|---|
| `v3_env6_check.py` (14 s for the 22 files, single thread) | `5b9dcd6006eb621a21b494f9ccefaf9691dd44dd29e2b70ef2296575fab60939` |
| `env6.out.jsonl` (per file: file SHA-256, P and sign hashes, all counts) | `d1847dff1363390b54d9a14813789ad04f920c7f7efd9f29801d649215654570` |
| `control.out.jsonl` | `059d49edcfbd28c668fcb35f2cca6a80e5350c20dcf85ec8fd1bb73432282205` |

The input SHA-256s equal `t4/real15/inputs.sha256` (22/22 OK at 13:49).

Re-run: `python3 -I v3_env6_check.py $T1/root6_real15.json $T1/real/m15_it*_real.json`, with `T1=/home/jay/research/data/roadmap-20261115/pm1115/t1`.
