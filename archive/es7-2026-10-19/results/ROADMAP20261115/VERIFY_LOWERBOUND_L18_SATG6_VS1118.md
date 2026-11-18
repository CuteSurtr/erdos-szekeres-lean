# VERIFY_LOWERBOUND_L18_SATG6_VS1118: verdict on claim lb-l18-sat14-realdep (verifier VS, 18 November 2026, 03:43-03:45 KST)

(The claim names VERIFY_LOWERBOUND_L18_SATG6.md, which already holds another verifier's text; hence the suffix
_VS1118.)

**Verdict: CONFIRMED at the claimed labels.** For the 14-point hexagon-saturated set S =
`l1118/sat14/r_g2_m7_f0_k6_s13.txt`:
- (i) l1enc(S, 6) has **exactly 56 models**. CERTIFIED, and VS's own enumeration finds the same 56.
- (ii) **Each of the 56 models is realized**: an integer realization S′ of S's labelled order type, with the same
  x-order, plus a point p whose signs are the model, such that S′ + p is in general position with no convex hexagon.
  EXACT.

Moreover, every clause of l1enc(S, 6) is justified by VS's own code as valid for every realization of S's order type.
So the 56 models are exactly the sign vectors that a sound order-type-level encoding allows, and every one of them is
geometric.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/l18-sat14/`; L = `l1118/sat14/`)

1. **Hashes.** The 8 sat14 entries of `l1118/logs/satsmall_sha256.txt` all pass.
2. **Base CNF** (`V/satcheck14.out`, `V/ot14.out`, with the code of VERIFY_LOWERBOUND_L18_SATG7.md at k = 6).
   - S is in general position with largest convex subset 5.
   - l1enc(S, 6) has 91 variables and 2,514 clauses, all with 3 literals: **302 are clauses of VS's own exact hexagon
     encoding G** (all of G present), and **2,212 forbid empty patterns**.
   - The empty ones are 364 = C(14,3) triangle clauses and 1,848 concurrent-line clauses, all decided from S's
     orientation signs alone (0 failures). There are 0 unexplained clauses.
3. **(i) Model count** (`V/vs_sat14.py` → `V/vs_sat14.json`).
   - `enum/e14_blocking.cnf` is the base clauses as a verbatim prefix, followed by exactly 56 clauses, which as sets are
     the negations of the 56 listed models (`enum/e14_models.txt`, over all 91 variables).
   - The listed models are pairwise distinct and satisfy every base clause.
   - **VS's own pysat enumeration of the base finds exactly 56 models, the same set.**
   - **Fresh cake_lpr by VS** (unit `esr-agv-vs-sat14cake`, heap 200) on `e14_blocking.cnf` (e50a34d7…) with the kept
     LRAT (886ab5bd…): exactly one line `s VERIFIED UNSAT`.
4. **(ii) Realizations** (`V/vs_sat14.py`). Each of the 56 files `enum/realall/m<i>_t<t>_Sp.txt` (14 points of S′ in
   S's label order, then p) was checked:
   - all 364 triples of S′ have S's orientation sign;
   - S′ sorts by x in the same order as S, with distinct x;
   - p's 91 signs, X(a,b) = [orient(a,b,p) > 0] in lexicographic pair order, equal model i;
   - the 15 points are in general position;
   - **the largest convex subset has 5 points, so no convex hexagon** (VS's convk, after an orientation-preserving shear).

   **56/56 files pass, covering all 56 models.**

## Not checked

- `realize_sig.py`, which is a search tool only.
- The literature comparisons (DDSZ; the k = 7 and k = 8 analogues are VS/VB CONFIRMED claims).
