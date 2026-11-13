# ES(8) upper bound: decision memo (5 Nov 2026)

Paths are relative to `<repo>`. ES8S stands for `cloud/es7-2026-10-19/results/ES8SLACK`. The CPU-h figures were measured on the arm64 Mac; none has been re-timed on this Linux host. The probabilities are my judgement, not measurements.

## 1. State of the art

**The project's best result is ES(8) ≤ 311.**
- It is the theorem `forces_convex_octagon_311` in `experiments/omission-final311-2026-10-14/Final311/Final.lean`. The Lean kernel checked it, and the axiom audit shows only propext, Classical.choice and Quot.sound (`final-audit.out:1-4`).
- The lrat-check defect does not affect it (`cloud/es7-2026-10-19/results/LRATCHECK20261105/AUDIT.md:25,38`).

**How the proof works.**
- It follows Schroeder's omission scheme: a projective chart, then a split into a balanced part and a residual part.
- The bound is T = 406 − b_B − b_R, where b_B and b_R are the largest hole budgets excluded over each catalog (`experiments/omission-global-assembly-2026-10-10/README.md:221`).
  - The balanced catalog has 3,131 rows over 252 states.
  - The residual catalog has 2,650 rows over 154 states, with state 0 occupied.
- The current pair (63, 32) gives 406 − 63 − 32 = 311, which is 408 − 97 (ES8S/README.md:83-84).

**Published comparison.**
- The best published bound is 408 (Mojarrad–Vlachos).
- Schroeder's 319 is an unreviewed preprint.
- No newer small-n bound was found (`docs/RELATED_WORK_2026-10-14.md:46-80`), but that search is three weeks old and had no direct arXiv access.
- The lower bound is ES(8) ≥ 65, proved in Lean.

**Where slack remains.**
- **Residual side: no slack left.** The integer optimum over the present rows is exactly 33 holes. The lower bound is Lean-checked and four witnesses were re-checked exactly. So b_R cannot move without new geometric rows (ES8S/README.md:112-159).
- **Balanced side: optimum known only to lie in [64, 72]** (ES8S/README.md:161-192). Budget 64, which would give 310, is pure arithmetic over rows already proved. Whether it is true is unknown.
- **Ceiling of the present catalogs:** 375 − h_B^min, where h_B^min is that balanced optimum. This lies in [303, 311] (ES8S/proofs.md:118-140).
- **Floor of the additive scheme:** 114. It comes from Schroeder's floors, which are in an unreviewed preprint (RELATED_WORK:812-814, 1401-1405).

**Caveat on verification.** The 311 proof was kernel-checked only on the Mac, and its roughly 500 GB of compiled parts were deleted. Re-certifying it on this host with the current pipeline costs about 300 CPU-h.

*Note added 6 November 2026:* this caveat is out of date. The compact checker re-checked ES(8) ≤ 311 end to end on this host in about 10 CPU-hours (7.3 for the 352 certificate modules, about 2.7 for the geometric chain), with 6.5 GB (6.0 GiB) of compiled certificate modules. `assemble_final311.sh` verified `forces_convex_octagon_311 : ErdosSzekeres.ForcesConvexNGon 311 8` with propext, Classical.choice and Quot.sound (`experiments/omission-compact-checker-2026-11-05/README.md`, section "6 November 2026: the compact recheck is complete"). This is a second complete Lean check, a reproduction with the same certificate trees, catalogs and kernel; the geometric-chain sources are pinned to the 11 October bridge record, so their link to the 19 October check is by source hash only. It is not an independent proof and not a new bound.

## 2. Routes to ≤ 310 and beyond, ranked

| # | Route → bound | What it needs | Compute + verification | Novelty | Main risk | P (my judgement) |
|---|---|---|---|---|---|---|
| 1 | **Balanced budget 64 over the existing 3,131 rows → 310**, i.e. (64, 32) | h_B^min ≥ 65; Bridge63 copied as Bridge64 (`exclusion_transfer` already works for any budget, Bridge63.lean:40-45); `(budget := 64)` in a new Final; a compact Lean checker; the residual budget-32 certificate (R32) rebuilt on this host | Search: 1,100–1,450 CPU-h, about 2–4 days wall on ~28 workers (ES8S/README.md:358-368). Lean with a compact checker: 250–540 CPU-h (my estimate, unmeasured). Lean with the current exporter: 1,320–1,740 CPU-h and 3.7–5 TB, which cannot fit in 641 GB free. R32 rebuild: 18–112 CPU-h. Total output under 20 GB with the compact checker | No new mathematics; days of Lean engineering | A 64-hole witness (detected, ends the route); node multiplier above 10 (estimates 8.3 / 8.8 / 9.9; a fresh budget-64 Knuth run gave 3.32e8 against the recorded 2.74e8); compact checker untested at scale | ≤ 3% within 48 h; 25–35% within 7 days; 35–50% within about 4 weeks |
| 2 | **Residual budget 33 via new rows → 310**, i.e. (63, 33) | Attainment axioms in Lean (contexts with existential owners outside the support); either a capacity-21 block lemma or cores from a whole-configuration coupled test on the 33-hole vectors W0–W3; a budget-33 certificate; the balanced budget-63 certificate (B63) re-exported on this host | Discovery: 100–600 CPU-h (estimate). Certificate: 1–3× the 313 tree if the LP reaches about 28.8, about 8× (around 3.5M leaves, which forces a compact checker) if the LP stays at 27. Lean infrastructure: 2–6 weeks | High: a new Baek-type capacity bound under attainment | Capacity 21 is false in the abstract model (22-owner models exist for rows 973, 1165 and 1186); even if proved, it shows only best vector 34 and dual bound 31; the last discovery round was 72 of 72 SAT; at least 15 optima with 33 holes are known and the total is unknown | 10–20% within 2–3 months |
| 3 | **Routes 1 and 2 together → 309**, i.e. (64, 33) | Both of the above | Sum of the two | High | Both risks compound | 5–8% |
| 4 | **Balanced budget 65 → 309**, i.e. (65, 32) | h_B^min ≥ 66 | Multiplier from 64 to 65 measured at 9.6 ± 12% (Knuth estimate). About 5,000–10,000 CPU-h even with the compact checker and symmetry, i.e. weeks of the whole machine. 28–49 TB with the current exporter | None | Truth of budget 65; cost | about 10%; decide only after route 1 |
| 5 | **New balanced rows** (cycle-family discovery, never run on the balanced side; a balanced coupled search for obstruction rows) | Port of the residual enumeration; a balanced analogue of CoupledSemantics | Discovery: 2–20 CPU-h. Coupled search: 2–6 weeks of engineering | Moderate | Every LP-tightening attempt so far left the balanced LP at 55.0 | 5–15% chance of any LP gain at deep nodes. It would speed up routes 1 and 4, or rescue them if a 64-hole witness turns up |
| 6 | **Joint balanced–residual rows, recovering the root's +1, or a direct bound on Q_8** | New structural mathematics; no worked example exists | Unknown | Very high | Unknown | < 5% in the near term. These are the only routes below 303 without new rows on either side, and the only routes below 114 at all |
| — | **Not viable** | Cup–cap recursion fed by Erdős–Tuza–Valtr (ETV) values (182 at best, and only if open cases are settled; those rungs would take about 2–3e5 core-hours of SAT); Norin–Yuditsky (no value at fixed n); HMPT (2^123); direct SAT (ES(7) = 33 is still open) | — | — | — | ≈ 0 |

**One prerequisite sits under every route: a compact, reflective Lean checker.**
- The design is one `decide +kernel` per chunk of leaves over a packed Nat/List encoding of the subtree.
- Its soundness lemma would be a list analogue of `CertificateTree.check_sound` (`ErdosSzekeres/OmissionCertificates.lean:210-261`).
- My estimate is 0.1–0.25 s and about 1 KB per leaf. Neither figure is measured. Today's pipeline uses 0.78 s and 0.64 MB per leaf.
- What it unlocks:
  - B64 can be checked on this machine at all.
  - R32 and B63 can be re-exported for whichever route is chosen.
  - 311 can be re-certified on Linux for about 50–85 CPU-h instead of about 300. *(6 Nov 2026: done, for about 10 CPU-h; see the note under §1.)*

## 3. Recommended next steps

**Now until 16:00 KST, one core.** At 14:12 KST the load was 31 on 32 threads, with 33 GB of RAM available and 641 GB of disk free. Mathlib and the core library are already built here.

1. **Start the compact checker.** It is on the critical path of every route.
   - Day-1 target: the Lean statement of the packed checker and its soundness lemma, plus an exporter for a 64-leaf chunk of `experiments/omission-final312-2026-10-13/certificate/tree-62.json.xz`. That file is here and is known to be good.
   - Gate G2, to pass before relying on the checker:
     - at most about 0.3 s of kernel time per leaf;
     - at most about 10 KB of compiled output per leaf;
     - checking time grows linearly from 64 to 1,000 to 10,000 leaves;
     - a corrupted leaf weight makes the check fail;
     - the axiom audit is clean.
   - No `native_decide`. Encode each leaf as a list of small Nats rather than shifting one huge literal.
2. **Prepare the pilot** (under 1 CPU-h).
   - Extract the 4,096 depth-12 contexts and their budget-63 subtree sizes from the local `tree-63.json.xz.part-*` files. The scratchpad script `tree_ctx.py` already computes the sizes.
   - Choose 24–32 contexts stratified by size, including the top decile, which holds 23.5% of the leaves.
   - Write a small driver that runs `pbb_strong.py`'s expansion on a single given context with the production rule (K_TOP=40, K_LOW=12).
   - Solve one tiny context (about 12 leaves) at budget 63 to measure seconds per node on this machine.
3. **Calibrate Lean on this host.**
   - Build the balanced Catalog: 229 s and a 12.5 GB peak on the Mac. Skip it if memory gets tight.
   - Check that `Residual2650ZeroProof.Root`, `Final313.Match` and `Residual32Bridge2650.Rows` do not import `BalancedCover61FusedProof`.

**At 16:00 KST, about 30 threads.**
1. **Look for likely witnesses first.** Solve one budget-64 LP for each of the 4,096 contexts, which takes minutes. Add the 4 lowest-LP contexts to the pilot, since a 64-hole witness, if one exists, is most likely there.
2. **Run the pilot.**
   - Budget 64 on the 24–32 chosen contexts.
   - Budget 63 on about 8 of the same contexts. The pairing controls for the HiGHS version and machine speed.
   - Cost: about 10–20 CPU-h. Wall time is set by the heaviest context, about 1.5 CPU-h (estimate).
3. **On 2–4 threads, run a witness hunt** for balanced vectors with at most 64 holes, and separately at most 71. Run it for hours; the earlier runs had only 480–540 s. Install OR-Tools in the scratchpad venv for CP-SAT.
4. **Optional, on 1–2 threads, residual scouting.** Run what-if LP screens, aiming for a residual LP near 29. Run the abstract capacity-21 SAT test on the untested block rows (1166–1185, 2315 and the 24 general blocks). The result decides whether route 2 deserves weeks.

**Gate G1, tonight or tomorrow morning.**
- **A 64-hole witness, checked exactly:** stop route 1. The witness is itself a result: h_B^min = 64, so the present catalogs can never beat 311. Pivot to routes 2 and 5.
- **Node ratio from 63 to 64 at most about 10:** launch the full budget-64 search on about 28 workers, lowest-LP contexts first and then largest first, with a checkpoint after each context.
  - The trees are plain data, about 10–14 GB uncompressed, so they can wait for G2.
  - The search is worth running before the checker exists because it also settles whether budget 64 is true.
- **Ratio 10–15:** first A/B-test cheaper search nodes on the pilot contexts. Accept a change only if the tree does not grow.
- **Ratio above 15:** stop and reassess.

## 4. What not to do

- **Do not run a residual budget-33 exclusion over the present 2,650 rows.** Feasible 33-hole vectors are known, so it cannot succeed.
- **Do not export B64 or B65 with the current per-leaf exporter.** It needs 3.7–5 TB against 641 GB free. Making the Root hierarchical does not help on its own, because the final module still loads every compiled part.
- **Do not base a new Final on `Final313.Final`.** It pulls in the unused 61-hole balanced certificate.
- **Do not start budget 65 until budget 64 is settled.**
- **Do not spend compute on levers already measured to do nothing:** early-vertex constraints, root rank-1 cuts, symmetric images of cuts, two-column rows, divide-by-symmetry.
  - Do not change the branching rule in the middle of the campaign.
  - Defer symmetry: it is worth at most 2× with the early-vertex constraints and needs catalog changes.
- **Do not pursue any target below 303 with the present catalogs**, or asymptotic, direct-SAT or ETV-rung routes.
- **Do not use `native_decide` or the lrat-check build.** New coupled rows go through CoupledLrat / `fromLRATAux`.
- **Do not claim 310, or "309 is likely", before the actual Final is kernel-checked and the axiom audit is clean.**
  - Do not cite 404 or 324 as published bounds.
  - Label Schroeder's floors as coming from an unreviewed preprint.
  - Redo a dated 2026 literature check before any external claim.
- **Do not plan wall time from the Mac's CPU-h.** SMT threads on this machine deliver less than a full core each.
- **Fixing the record discrepancies is housekeeping only and changes no decision.** Examples: 312 is recorded as 58 CPU-h in the READMEs but 46.7 CPU-h in the kernel record, and the 313 part-time range is misstated.