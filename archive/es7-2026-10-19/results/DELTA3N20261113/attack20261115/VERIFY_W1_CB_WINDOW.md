**Verdict: CONFIRMED, except one sentence** (claim `w1-cb-window`, filed by W1; verifier V3, 15 November 2026,
17:07-17:12 KST).
- Confirmed: (a), (b), the arithmetic, the open windows 16-58 (n = 8) and 14-31 (n = 7), the two quotations of (c), and
  (d).
- **Refuted as worded:** the first sentence of (c), "CB(8) is open at every size ≥ 16 and CB(7) at every size ≥ 14".
  - CB(n) at a size m above M(5;n) is vacuously true, because no (5,n)-valid set has m points.
  - With M(5;7) ≤ 36 (CERTIFIED, ETV7SAT; the claim's own input), **CB(7) is decided (true) at every size ≥ 37**.
  - CB(8) is likewise decided at every size above the best N5 bound: ≥ 66 if ETV5N's N5 ≤ 65 is accepted (its LRATs were
    deleted), and in any case above ES(8) − 1.
  - Suggested wording: "CB(8) is undecided at every size from 16 up to the largest possible (5,8)-valid size, and CB(7)
    at sizes 14-36. By (b), both reduce to the windows 16-58 and 14-31."

# Independent check: CB window lemma and the corrected open ranges

**Definitions.** CB(n) is from candidates.md K3: every (5,n)-valid S has a weak Δ with no (n−1)-cup. Weak Δ, gon and
validity are from THEORY_1115PM.md §0, and M(a;n) is defined as in LEDGER_1115PM.md §0.

**(a) Heredity: PROVED, re-derived.** Let D be a CB Δ of a valid W and T ⊆ W.
- D ∩ T ⊆ D is 4-cap-free and (n−1)-cup-free.
- Every gon G of T is a gon of W, so ∅ ≠ D ∩ G = (D ∩ T) ∩ G.
- T is valid.

So D ∩ T is a CB Δ of T.

**(b) Window lemma: PROVED from CERTIFIED inputs, re-derived.**
- By (a), failure of CB is upward closed. So every counterexample contains an inclusion-minimal one, which is
  vertex-critical.
- For a vertex-critical point set S and any p ∈ S, S − p has a CB Δ D′. That gives two bounds:
  - |D′| ≤ f(n−1, 4) = C(n−1, 2), by the Erdős–Szekeres cup-cap theorem (no (n−1)-cup and no 4-cap; LEDGER I7);
  - S − p − D′ has no 5-cap, and no gon, since D′ meets every gon of S − p. So |S − p − D′| ≤ M(5; n−1).
- Hence |S| ≤ 1 + C(n−1,2) + M(5;n−1).
- With M(5;7) ≤ 36 (I4: CERTIFIED modulo ETV7SAT §2's written arguments) and M(5;6) = 15 (I5), this gives 21 + 36 + 1 = 58
  and 15 + 15 + 1 = 31 (`v3_w1_arith.py`, asserts pass).
- With CB(8) ≤ 15 and CB(7) ≤ 13 (claim cb78-from-strong, CONFIRMED by V1), the windows that decide CB(8) and CB(7) are
  16-58 and 14-31. Correct.
- Caveat inherited from V1's verdict: CB(8) at |S| = 15 rests on the DELTA2N record only, because its proof was
  deleted and never re-run. Counting only re-run certificates, the n = 8 window starts at 15.

**(c) Wording correction.**
- Both quotations are exact:
  - `cb78-from-strong.claim.json` ends "CB(8) at 16-22... and CB(7) at 14-15 remain open."
  - VERIFY_CB78_FROM_STRONG.md line 76 reads "Open, as the claim says: CB(8) at 16-22 and CB(7) at 14-15".
- Both understate what is open, as W1 says.
- "No record decides CB(8) at 23-58 or CB(7) at 16-31": correct. A grep of all records and claims finds CB(7) and CB(8)
  decided only at ≤ 13 and ≤ 15. THEORY_1115PM.md line 371 lists the next sizes as untested.
- The broader sentence "open at every size ≥ 16 / ≥ 14" is wrong at the vacuous sizes, as explained in the verdict.

**(d) PROVED, re-derived.**
- If N5 ≤ 57, CB(8) at 58 is vacuous.
- Conversely, if CB(8) holds at 58 and S were a valid 58-point set, its CB Δ would give |S| ≤ 21 + 36 = 57, a
  contradiction. So CB(8) at 58 implies N5 ≤ 57.
- The master formula ES(8) ≤ 189 + N5 + N66 is LEDGER §0, from I1 (Lean |H| ≤ 187), I2 (THEORY310N Lemma A) and I3
  (N66 ≤ 56, CERTIFIED). With N66 ≤ 56 it gives 189 + 57 + 56 = 302.
- I checked the arithmetic and that the LEDGER states these inputs with their labels. I did not re-derive I1-I3.
- "Nothing here changes any bound": correct, since (d) is conditional on CB(8) at 58.

**Files.**
- `/home/jay/research/data/roadmap-20261115/pm1115/v3/w1-cb-window/v3_w1_arith.py`, SHA-256
  `c86b15ddc5a0679b094e0c5ad9fde76d1dd06f00fe805c2e07bd07911383990c`.
- Its output `v3_w1_arith.out`, SHA-256 `74f11754…b055`.
- W1's `ledger_calc.py` was not needed.
