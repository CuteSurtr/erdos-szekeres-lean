# Task G: hull-size case split pilot (ES(7), N = 33)

Run on 19 October 2026, 21:14 to about 01:10 KST. No case at k = 7 was closed, and nothing
here is a theorem.

## Bottom line

- **The split is sound and exhaustive.** Each case is "the hull-frame CNF plus a hull-size
  constraint". Every model of the base CNF satisfies exactly one case. The proof is in
  [proof_notes.md](proof_notes.md), and point sets and brute force check it independently.
- **k = 6 calibration passes.** At N = 17, every hull case is UNSAT, and every UNSAT run is
  LRAT-checked. At N = 16, cases h = 3, 4 and 5 are all SAT, and brute force verifies each
  model. Times per hull size are in the table below. The largest hull size, h = 5, is the
  cheapest case, at 36 s against 217 s for the unsplit CNF. Summed over all hull sizes, the
  split costs 1.9 times the unsplit CNF.
- **k = 7, N = 33: no hull case closed.** Shallowest-first cube-and-conquer ran for about
  3 hours on h = 6 and on h = 5. No cube at depth 8 or less closed within 20,000 conflicts.
  Closed weight is exactly 0 for both runs.
- **Estimated tree sizes.** Random dives with the same solver and split rule only close
  cubes at depth about 30 to 40. A single-path Knuth estimate therefore puts each hull case
  at about 2^30 to 2^40 leaves, which is roughly 10^10 to 10^12 CPU-seconds. That is not
  pilot-tractable, so even h = 6 is out of reach with this encoding and driver.
- **The optional lemmas are not used at k = 7.** The cup–cap cardinality lemmas passed the
  k = 6 controls but slowed k = 6 down by 1.3 to 1.7 times. Every k = 7 run is therefore
  lemma-free.

Details, tables and caveats follow. The machine was shared with other heavy jobs, so wall
times are inflated, and CPU times are the figures that matter.

PLACEHOLDER_BODY
