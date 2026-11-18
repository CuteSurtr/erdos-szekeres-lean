# VERIFY_P307_CHAIN: claim `p307-chain` (verifier VS, 16 Nov 2026, 18:39-18:50 KST)

**Verdict: CONFIRMED.** The written chain in ROUTE307_1116.md §1.2-1.4 is correct arithmetic over its labelled inputs,
and every input it calls closed is on record with the stated label. Label: **PROVED** (conditional), as claimed. It is
computer-assisted, not Lean-checked as a whole, and unrefereed. **No bound changes: ES(8) ≤ 307 still needs L11 + L13,
or L11 + L12, or L14.** Two wording notes, neither changing the verdict:
1. The N5 forms of item (4) also use the F half of Lemma A, h(F) ≥ 84 − N5 (bridge/README.md §2, eq. (A)). The
   input list's L5 names only the Lo half. Also, h(C) = h(F) + h(Lo) holds with equality, because C = F ⊔ Lo.
2. For the budget-35 trees (L10) I checked the packet inputs (below), not the trees. The trees rest on the project's
   fresh replay plus VERIFY308's `tcheck_b35`, as the claim says; `pycheck` was not run on them.

## What I checked (own code: `/home/jay/research/data/roadmap-20261115/pm1115/vs1116/p307-chain/`)

`vs_p307.py` (sha256 `d69d3206…`, output `vs_p307.json` `67a9990f…`) reads the catalog and packet files directly. All
its asserts pass.
- **Catalog** (`W/inputs/source-2650.json.gz`): 154 states. F = {f1 ≥ 5} has 84 states and Lo = {f1 ≤ 4} has 70; they
  partition C, and state 0 is in Lo.
- **h(F) ≥ 18.** Rows 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186 and 2315 each have rhs 6 and a support of 28
  distinct states inside F. Every F state is covered exactly 3 times, so 3h(F) = Σ_j h(B_j) ≥ 54.
- **Packets** (the master.json `budget` field; the extra path; extra[0] = (F, T) and extra[1] = (Lo, B − T) with the
  supports equal to F and Lo exactly; every other extra row has rhs 1; the number of ctx files equals the `contexts`
  field):

| packet | B | (F, Lo) | rows | contexts = ctx files |
|---|---|---|---|---|
| runs/s18/bb | 34 | (18, 16) | 3,672 | 4,296 |
| runs/s19/bb | 34 | (19, 15) | 3,464 | 3,643 |
| runs/s20/bb-s2 | 34 | (20, 14) | 3,672 | 4,289 |
| runs/b35s18/bb | 35 | (18, 17) | 3,672 | 4,838 |
| runs/b35s19/bb | 35 | (19, 16) | 3,707 | 7,170 |

  The master SHA-256 values of s18, s19 and s20 equal those in VERIFY308 §5. The context counts of b35s18 and b35s19
  equal the claim and the VERIFY308 addendum (`verify308-20261114/b35/out-b35s1{8,9}.summary.json`: EXACT TREE,
  416,935 and 15,533,581 nodes, minimum margin 1, 0 errors).
- **Rows of the budget-35 packets** (`vs_p307_rows.py`, `3998789b…`):
  - the 1,020 coupled rows of b35s18-v13, and the first 1,020 of b35s19-v16, are identical and in the same order as
    s20-v13's, which VERIFY308 re-certified 1,020/1,020 with cake_lpr;
  - the other 35 rows of b35s19-v16 equal, as a multiset, the 11 + 13 + 11 rows of audits `cuts-v14/15/16`. Each of
    those audits has label CERTIFIED, own encoder = CNF hash and a fresh cake_lpr acceptance for every row.
- **Case enumeration.** With h(F) ≥ 18, h(Lo) ≥ 70 − N66 and h(F) + h(Lo) = h(C):
  - budget 33 gives {(18,15), (19,14)};
  - budget 34 gives {(18,16), (19,15), (20,14)};
  - budget 35 gives {(18,17), (19,16), (20,15), (21,14)} for N66 ≤ 56, the first three for N66 ≤ 55, and the first
    two for N66 ≤ 54;
  - N66 ≤ 52 leaves no case at budgets 33-35.

  This gives (A), (B) and (C). h(C) ≥ 36 then gives |R| ≤ 118, |S| ≤ 306, and the threshold
  `forces_of_population_bounds` with B = 187, R = 118 (`ForcesConvexNGon (B + R + 2) 8`, premise 1 ≤ B + R; the
  statement was read in `ErdosSzekeres/Omission/PopulationBounds.lean` l. 29) is 307.
- **Equality case.** The only (|H|, |R|) with 307 ≤ 1 + |H| + |R|, |H| ≤ 187 and |R| ≤ 119 is (187, 119). Then
  h(C) = 35, and the cases left after (18,17) and (19,16) give the owner pairs (84 − 20, 70 − 15) = (64, 55) and
  (63, 56).
- **Capacity-only forms.**
  - N66 ≤ 52: 18 + 18 = 36.
  - N5 ≤ 62: (84 − 62) + 14 = 36.
  - N5 ≤ 63 and N66 ≤ 55: 21 + 15 = 36.

  As a control, the unclaimed N5 ≤ 63 with N66 ≤ 56 gives only 35, so the stated hypotheses are needed.
- **Records.**
  - L7 (VERIFY_LO l. 35/37: 3,815 and 186,077 nodes) is confirmed.
  - L6 (VERIFY309N20261113/followup56) is "INDEPENDENTLY CONFIRMED".
  - L9 (VERIFY308 §1, §5: tcheck + pycheck, all three slices) is confirmed.
  - The 308 links are confirmed 10/10 in CHAIN_REVIEW.md.
  - Lemma A in its written form is in THEORY310N20261113 and VERIFY_N66_56 l. 34/65.
- **(5) N5-free.** It holds for (1)-(3): h(F) ≥ 18 comes from Lean rows only, and the budget-34 case (18,16) has its
  own tree. Only the capacity-only forms in (4) use N5, and the claim states them as conditionals.

No solver, no tree replay, no unit; three single-threaded Python runs of under a few seconds each. No file outside this
verify file and VS's work directory was written.
