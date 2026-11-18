# VERIFY_LOWERBOUND_L18_OTSAT: claim `lb-l18-otsat-nonmax` (verifier VB, 18 Nov 2026, 03:09-03:20 KST)

**Verdict: CONFIRMED** for the six UNSAT certificates and their meaning, for the conversions, and for consequences
(i)-(iii) as stated.
- **sat_g(8) ≤ 51:** the 51-point integer set `c5_51.txt` has every property below and is therefore geometrically
  octagon-saturated in every realization of its labelled order type (CERTIFIED + PROVED soundness).
- **Not checked:** the side facts listed as "not claimed as new" (the SAT sets, and the non-saturated realizations of
  mirror46 and c3_27).
- Novelty is not judged here. The claim says "not found in this search" and makes no priority claim.

Own code throughout. `W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/lb-l18-otsat-nonmax/`

| set | k | n | conversion (own exact check) | collinear | convex j-sets, j = 4, 5, 6, 7 (own enumeration = brute force) | convex k-sets | own l1enc multiset = CNF (R2 / AC / OCT) | fresh cake_lpr (exactly one `s VERIFIED UNSAT`; LRAT stream SHA-256 = the claim's) | 200 random p: on a k-gon |
|---|---|---|---|---|---|---|---|---|---|
| c5_51 | 8 | 51 | Z[√5] signs = integer signs, 0 of 20,825 differ | 0 | 128,980 / 314,845 / 303,090 / 88,920 | **0** (all 636,763,050 8-subsets) | yes, 167,862 (119,952 / 20,825 / 27,085) | yes (`a770b703…`) | 200/200 |
| c4_52 | 8 | 52 | = (w0 − w2, w1 − w3) line by line | 0 | 141,809 / 269,804 / 196,770 / 45,220 | **0** (752,538,150) | yes, 170,380 (127,400 / 22,100 / 20,880) | yes (`d34b277f…`) | 200/200 |
| c3_55 | 8 | 55 | byte-identical to `ES8SYM/sets/c3_55points_k8.txt` | 0 | 191,739 / 568,611 / 671,808 / 244,887 | **0** (1,217,566,350) | yes, 218,741 (151,580 / 26,235 / 40,926) | yes (`af264558…`) | 200/200 |
| c4_28 | 7 | 28 | byte-identical to `SYMMAX/c4_28points.txt` | 0 | 10,911 / 10,484 / 3,050 / – | **0** (1,184,040) | yes, 25,492 (18,200 / 3,276 / 4,016) | yes (`ee1b2ec4…`) | 200/200 |
| c3_31 | 7 | 31 | byte-identical to `SYMMAX/c3_31points.txt` | 0 | 18,915 / 33,732 / 23,082 / – | **0** (2,629,575) | yes, 39,657 (25,172 / 4,495 / 9,990) | yes (`b788f422…`) | 200/200 |
| c5_31i | 7 | 31 | Z[√5] signs = integer signs, 0 of 4,495 differ | 0 | 17,005 / 22,546 / 8,445 / – | **0** (2,629,575) | yes, 37,022 (25,172 / 4,495 / 7,355) | yes (`e4a898e8…`) | 200/200 |

- The convex 4-set and 7-set counts of c3_55, c4_52 and c5_51 equal those that ES8SYM's README (§2) lists for the
  repository sets: 191,739 / 244,887, 141,809 / 45,220 and 128,980 / 88,920. Since the counts are order-type
  invariants, this also cross-checks the conversions.
- The CNF hashes equal the claim's: `538c8785…`, `6e01eae8…`, `b7795ba3…`, `1a6f5452…`, `0515c484…`, `e43a342c…`.

## 1. What was checked

The claim says the following for each of the six sets S (integer files `l1118/sym8/*.txt`, `l1118/absat_sym/*.txt`):
- S is in general position and k-gon-free;
- `l1enc(S, k)` is UNSAT (CERTIFIED);
- so, by the soundness of ABSAT8_INDEPENDENT §3 (k-generic), every realization of S's labelled order type, or of its
  mirror image, is geometrically k-gon-saturated;
- hence (i) sat_g(8) ≤ 51 (DDSZ's Thm 4 gives 56), (ii) c4_28 is saturated in every realization, and (iii) order-type
  saturation does not imply maximum size;
- the integer files have the labelled order types of the repository sets.

## 2. Method (own code)

- **`vb_conv.py`, conversions in exact arithmetic.**
  - 5-fold: a repository line c_0..c_{r−1} is the point Σ c_j ζ^j, ζ = e^{2πi/5}. orient(a,b,c) = sign Im(conj(b−a)(c−a)).
    With z = conj(u)v = Σ z_t ζ^t, Im z = sin 72°·((z₁ − z₄) + (z₂ − z₃)(√5 − 1)/2), so the sign is sign(A + B√5) with
    A = 2(z₁ − z₄) − (z₂ − z₃) and B = z₂ − z₃, decided exactly by comparing A² with 5B².
  - The formula agrees with a float evaluation on 220 well-separated triples, a sanity check only.
  - All labelled triples are compared with the integer file's determinant signs. No repository triple is collinear.
  - 4-fold `.pts`: w0 + w1·i − w2 − w3·i = (w0 − w2, w1 − w3), checked line by line.
  - The others: SHA-256 equality.
  - c3_55 and c3_31 are Eisenstein pairs a + bω read as Cartesian integers. That is a linear map with positive
    determinant, so the orientations agree (ES8SYM README §2).
- **`vb_otsat.py`.**
  - Exact orientation table and collinear-triple count.
  - Complete enumeration of all convex j-subsets: a convex set plus a larger index is convex iff every 4-subset
    through the new index is convex; bitmask candidate sets.
  - Own l1enc(S, k), whose encoder (from ABSAT8_INDEPENDENT §3) matched d28_h.cnf in claim `lb-ln-ddsz28-all34`:
    - R2 rotation clauses;
    - one AC clause per triangle;
    - OCT chain clauses of every convex (k−1)-gon in ccw order around its lexicographically smallest vertex,
      deduplicated.
  - Comparison with the claim's CNF as sorted clause multisets, plus the header.
  - Positive control: 200 random integer points p per set, every 4th far outside the hull, rejected if collinear with
    two points of S. Each p is tested exactly for a convex k-gon through p: some convex (k−1)-gon Q of S of which p
    sees exactly one edge, i.e. Q ∪ {p} is convex.
- **`bf.cpp`** (VB's brute force, `__int128` determinants): counts the convex j-subsets for j = 4..k by full enumeration of
  all j-subsets, independently of the bitmask method. For the k = 8 sets that includes all 8-subsets: 0.6-1.2·10⁹,
  2.9-4.5 s each.
- **Fresh cake_lpr** on each CNF with the kept LRAT, streamed from `<name>.lrat.zst` through a FIFO (`vb1118/bin/recake_vb.sh`;
  heap 1000 MB for k = 8 and 300 MB for k = 7; max RSS 46-358 MB). Stdout is exactly one line, `s VERIFIED UNSAT`.
  The stream SHA-256 equals `certify.jsonl`'s `lrat_sha256`, and the CNF SHA-256 equals the claim's.
- Unit `esr-agv-vb-otsat` (95 %, 2700M, under `vb1118/unit.lock`), under 1 min in all.

## 3. Soundness and consequences (read, agreed)

- ABSAT8_INDEPENDENT §3 proves the following for k = 8. If a real point p has S′ ∪ {p} in general position (S′ any
  realization of S's labelled order type) and no convex k-gon through p, then α_p satisfies R2, AC and OCT.
- The proof never uses k = 8 except as the size of the gon: the visibility and slot lemmas are about a convex
  (k−1)-gon Q. So UNSAT means that every such p lies on a convex k-gon. A mirror image changes no convex position.
- With S k-gon-free (checked above), S itself is geometrically k-gon-saturated. For c5_51 (51 points, k = 8) that gives
  **sat_g(8) ≤ 51**, under DDSZ's definition: an n-gon-free set in general position to which no point can be added in
  general position without creating a convex n-gon. DDSZ's Theorem 4 gives 56, as the claim says; the paper was not
  re-read here.
- (ii) holds for c4_28 at k = 7 (28 points).
- (iii) holds: 51, 52 and 55 < 64 and 28, 31 < 32. These are the sizes 2^{k−2} of the Erdős–Szekeres constructions
  without a convex k-gon, so k-gon-free sets larger than these saturated ones exist, and the saturated sets are not of
  maximum size. Whether 2^{k−2} is the maximum is not used.

## 4. Files (`W`; SHA-256 of everything in `W/SHA256SUMS`)

`vb_otsat.py` (`261ad77e…`), `vb_conv.py` (`5f0c8687…`), `bf.cpp` (`f51fcf89…`), `run.sh` (`7917f0fa…`), `conv.jsonl`,
`out/<set>.json|.out|.bf`, `cake/rerun.jsonl` and `cake/<set>.cake.out`. Re-run: `bash W/run.sh` (about 1 minute).
