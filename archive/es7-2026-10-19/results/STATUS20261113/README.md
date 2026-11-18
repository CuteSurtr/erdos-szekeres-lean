# STATUS20261113: handoff at 22:10 KST, Friday 13 November 2026

> **Update 14 Nov, 01:45 KST.** ES(8) ≤ 309 now has three independent routes, all uncommitted:
> 1. **N66 ≤ 56 + slices 18, 19 over the Lean rows alone.**
>    - N66 ≤ 56: CERTIFIED at 23:43, confirmed by Codex in VERIFY309N20261113/followup56.
>    - Slices 18 and 19: independently replayed (VERIFY_LO).
> 2. **N66 ≤ 57 + slices 18–20:** audited by Codex (VERIFY309N20261113); written up in ES309N20261113.
> 3. **N5 ≤ 65 + N66 ≤ 59 + slices 19–22** (FASTBB20261113 §1.5).
>    - Both inputs are independently confirmed.
>    - Slice 22: 32,328,319 nodes, minimum margin 1. Slices 21 and 22 were each replayed twice within the track but
>      not yet by another track.
>    - All 755 coupled rows were re-certified with their proofs kept.
>
> Still running until about 06:00: slice 23 (unit `nov13c-g-chain9`) and N66 level 14 (N66 ≤ 55; with budget-34
> trees this is a possible route to ES(8) ≤ 308).
>
> **Repository reorganization (owner decisions, 14 Nov ~00:55):**
> - A fresh single-commit `main` is being built in an isolated clone; the old history goes to a `history` branch
>   and tag.
> - **The 13 Nov records stay out of the public snapshot** until the owner releases ES(8) ≤ 309. They must first be
>   scrubbed of machine paths and tool names.
> - Plan and logs: `/home/jay/research/data/reorg-20261113/`. No push without the owner's OK.

> **Update 22:25 KST: slice 21 is CLOSED (EXACT TREE).**
> - Pair (63, 58); C++ `fastbb` with the slice rule.
> - Size and replay: 19,333,541 nodes, 9,666,771 leaves, minimum margin 1. The only pending leaf is "state 0
>   missing". The whole tree was replayed piecewise by `check_tree`: 8,175 of 8,175 contexts.
> - Rows: 645 extra rows (643 cake_lpr-certified coupled rows plus the two capacity rows). 11 witnesses were killed
>   on the way with 29 newly certified rows.
> - Inputs: `extra.json` SHA-256 `7e7fc843…`, master `63ea1915…`, contexts digest `07157632…`.
> - Files: `/home/jay/research/data/fastbb-20261113/p2/runs/s21/DONE.json`.
> - A second replay with a different wrapper (`replay2.json`) runs automatically. The chain then continues with
>   slice 22 and then slice 20 as an independent second tree (unit `nov13c-g-chain6`; log `p2/runs/chain.log`).
> - **Consequence:** slices 18–21 are closed, so **N66 ≤ 58 ⇒ ES(8) ≤ 309** as well. This is a second route next to
>   N66 ≤ 57 with slices 18–20; both N66 certificates are CERTIFIED, neither is independently checked yet.
> - **If slice 22 closes**, the independently verified N66 ≤ 59 and N5 ≤ 65 suffice (slices 19–22).
> - Not independently checked: slice 21's tree, and the residual coupled encoder (link (c) of §1.2), which slice 21
>   uses too.

Written by the Claude session of 13 November (Fable 16:40–19:40, cut off by a usage limit; Opus from 20:25) for
whoever continues. Read this page first, then the records it names. **Nothing of 13 November evening is
committed or pushed.** Every record below is an untracked directory in `cloud/es7-2026-10-19/results/` (R).

## 1. Headline: ES(8) ≤ 309 now follows from certified pieces, pending independent checks

Every link is in place, but two links have not been independently re-checked (§1.2). Do not announce, commit or
write the headline into README/math.md before they are checked and the owner agrees.

### 1.1 The chain

1. **Composition (Lean-checked, existing).** An octagon-free set S has |S| ≤ 1 + n_H + n_R with n_H ≤ 187
   (`Final310Compact`, balanced population 187) and n_R = 154 − Σh, where h is the residual hole vector
   (h₀ = 0 by `zero_mem_residualOccupied`). ES(8) ≤ 310 used Σh ≥ 33 (`Excludes2650Zero 32`). **309 needs Σh ≥ 34.**
2. **Lemma A** (R/THEORY310N20261113 §2; written proof). The owners of the 70 residual states Lo = {f₁ ≤ 4} form
   a set with no 6-cap, no 6-cup and no convex octagon, so h(Lo) ≥ 70 − N66. The verifier of LO33N confirmed this
   use (VERIFY_LO.md).
3. **N66 ≤ 57** (R/N66N20261113; **CERTIFIED** 21:43 by cake_lpr). Every set with no 6-cap, no 6-cup and no
   convex octagon has at most 57 points. Cup–cap gives 70; the ETV value is 50; this was 64 at 16:43.
   - Proof object: a trimmed monolithic sub-CNF "≤ 12 holes" with 206,705 clauses (CNF SHA-256 `80b55b0c…`, LRAT
     `3971e63f…`). It uses 7,913 rows, each justified: 3,769 transported, 3,891 mirror, 203 cores and 50 cycle rows.
   - Directory: `/home/jay/research/data/n66-20261113/p2/b12/it1`. Status file:
     `/home/jay/research/data/phase2-20261113/n66_certified.json`.
   - **NOT independently verified.** Of this record, only the 18:11 certificate N66 ≤ 59 was independently
     confirmed (VERIFY_N66.md); N66 ≤ 58 (20:56) and N66 ≤ 57 (21:43) were not.
4. **Lemma S** (R/LO33N20261113 §2; written; **independently confirmed**, VERIFY_LO.md). From Σh ≥ 33 (Lean) and
   h(F) ≥ 18 (nine Baek rows), a 33-hole vector with h(Lo) ≥ 13 lies in a slice t = h(F) ∈ {18, 19, 20}.
5. **Slices 18, 19, 20 closed** by exact trees: the 2,650 Lean rows, 578 cake_lpr-certified coupled rows and the
   slice's two capacity rows, every leaf margin recomputed in exact integers by `scripts/omission_tree.check_tree`.
   - Slices 18 and 19: also closed over the Lean rows alone, and **independently replayed** (VERIFY_LO.md).
   - Slice 20 (pair (64, 57)): closed 20:28; 3,468,657 nodes, 1,734,329 leaves, minimum margin 1, one pending leaf
     (state 0).
     - Replayed twice by the record's own `verify_stream.py`; **not independently replayed**.
     - Tree: `/home/jay/research/data/lo33-20261113/bb_64_57`; log `logs/tree_64_57.log`. Hashes: extra rows
       `d12f624f…`, master `15cd5892…`, contexts digest `709a345e…`.
6. Hence Σh ≥ 34, n_R ≤ 120, |S| ≤ 308 for octagon-free S, so **ES(8) ≤ 309**.

### 1.2 What must be checked before any claim

- **(a) The N66 ≤ 57 certificate.**
  - Read the soundness section of the monolithic CNF (`mono66.py`; README of N66N, written by the phase-2 agent).
  - Regenerate the trimmed CNF, re-run cake_lpr, and re-justify the 7,913 used rows with your own code.
  - Test real (6,6,8)-sets against every used row.
  - VERIFY_N66.md shows how this was done for N66 ≤ 59.
- **(b) The slice-20 tree.** Replay it yourself with `check_tree` (piecewise), check that the capacity rows are
  exactly (F, 20) and (Lo, 13), and check that every other extra row has a cake_lpr verdict.
- **(c) The residual coupled encoder.** Slice 20 uses 578 certified *residual* coupled rows (RES33N's `coupled.py`).
  Their validity rests on that encoder's soundness, which no verifier has examined (VERIFY_LO.md lists it as an
  inherited assumption). There are two ways to remove this dependency:
  - close slice 20 over the Lean rows alone (`repair.py`, LO33N §6); or
  - wait for **N66 ≤ 56** (level 13, running, §2). With it, slices 18 and 19 over the Lean rows alone suffice. That
    is the cleanest chain: Lean rows, Lemma A, Lemma S and one certified CNF family (the (6,6,8) model).
- **(d) Optional robustness.** If slices 21 and 22 close (slice 21 is running, §2), then the independently verified
  N66 ≤ 59 and N5 ≤ 65 already give 309 through slices 19–22.

Dependencies that are not Lean-checked in any variant: Lemma A, Lemma S, the cake_lpr certificates and their
encoders, and the Python tree checker. Nothing is refereed.

## 2. What is running now (systemd user units, 16-thread cap, 24 GB memory budget)

| unit | threads | what | result appears in | ends |
|---|---|---|---|---|
| `nov13c-g-chain6` | 5 | slice 21 (pair (63, 58)) with the C++ engine `fastbb` and its slice rule. At 22:04, 3,527 of 4,662 remaining contexts were closed (9.2 M nodes). 8 witnesses were killed by 20 newly certified rows; none is stuck. The driver replays the tree when it finishes. | `/home/jay/research/data/fastbb-20261113/p2/runs/s21/` (`DONE.json` or `STUCK.json`, `status.json`, `driver.log`) | ≤ 06:00 |
| `nov13c-n66-s13c1`, `-s13e1`, `-s13g`, driver `nov13c-n66-drv18` | 3 | level 13 (N66 ≤ 56) with the lazy monolithic engine. The driver certifies any UNSAT by itself and appends it to `n66_certified.json`. | `/home/jay/research/data/n66-20261113/p2/` (`driver.log`), `n66_certified.json` | ≤ 06:00 |
| `nov13c-vfy-E2-n37` | 1 | Independent re-check of ETV7SAT's N = 37 certificate, whose LRAT was deleted: CaDiCaL (~70 min from 21:38), then cake_lpr with a 4.2 GB heap. | `/home/jay/research/data/verify-E2-20261113/` (`status.jsonl`, `VERIFIED` / `FAILED`) | ~23:15 |
| `p2-watch-d1b` → `nov13c-vfy-D1b-m16` | 1 | After E2: re-check of DELTA2N's strong case (4,7) at m = 16 with a 4.5 GB heap (the verifier's 1.3 GB was too small). | `/home/jay/research/data/verify-D1b-20261113/` | after E2 |
| `memguard5-20261113` | – | Memory guard for `nov13c-*` units only. It lifts the kernel limit and stops a unit cleanly at 95% of its own MemoryMax, on swap, or over budget. Log: `/home/jay/research/data/memguard-20261113/memguard.log`. | – | until stopped |

- **Claude agents.** One Claude agent, G2, may still be waiting for slice 21. It will update
  R/FASTBB20261113/README.md and exit by 02:00 KST at the latest; avoid editing that file before then. All other
  Claude agents have finished.
- **Thread count.** `/home/jay/research/data/phase2-20261113/cpu_free.sh` prints the threads still free under the
  cap. It counts only `nov13c-*` units; start other jobs under that prefix too, or count them yourself.
- **At the end:** stop `memguard5-20261113` and `p2-watch-d1b` once no research job runs.

## 3. Results of the evening (all uncommitted)

| record | result | label | independent check |
|---|---|---|---|
| N66N20261113 | N66 ≤ 59 (18:11), ≤ 58 (20:56), ≤ 57 (21:43); level 13 running | CERTIFIED | 59 **confirmed** (VERIFY_N66.md); 58 and 57 not yet |
| LO33N20261113 | Lemma S. Slices 18, 19 (also over the Lean rows alone) and 20 closed. So N66 ≤ 57 ⇒ ES(8) ≤ 309, and N66 ≤ 56 ⇒ 309 over the Lean rows alone | EXACT TREE | Lemma S and slices 18, 19 **confirmed with corrections** (naming; archiving gaps); slice 20 not yet |
| ETV5N20261113 (morning, committed) | N5 ≤ 65 | CERTIFIED | **confirmed** (VERIFY_N5.md); a write-up must compare with 78, which follows from printed results |
| FASTBB20261113 | C++ `fastbb`: capacity-58/59 trees reproduced, 20–70× faster; slice rule added | EXACT TREE | **confirmed with corrections** (labels; mutable input paths) |
| ETV7SAT20261113 | M(5;7) ≤ 36 (was 41) via a new owner-model CNF; Schroeder's M₇(5,6) ≤ 25 re-proved in one CNF | CERTIFIED (log only) | **not confirmed**: model sound, but the N = 37 LRAT had been deleted; re-check running (E2) |
| DELTA2N20261113 | Weak Conj(6) true for all point sets; no counterexample ≤ 15 points for weak Conj(7), (8); the "cup-side" sharper form survives everything | CERTIFIED | **confirmed with corrections** (wording; (4,7) m = 16 heap, re-check queued) |
| FLAYER20261113 | No new capacity row; N₁(5,5) = 14 (already known: MathOverflow 277192) | CERTIFIED | **confirmed with corrections** |
| LFR20261113 | Lazy full-support refuter (tool), superseded by N66N's lazy monolithic engine | COMPUTED / CERTIFIED cores | not checked |
| NOVELTY20261113B | Literature check: no ES(8) bound ≤ 310 anywhere; Schroeder still v1 (319); the strong decomposition form has public prior art and is false (15 and 16 points); concurrent public projects GLitchfield and gotrevor work on the same ETV cases | evidence | – |

The VERIFY files are `VERIFY_<KEY>.md` inside each record.

## 4. Rules that the owner has set (keep them)

- **Git.** No commit, push or branch change without asking the owner. Never add Co-Authored-By or tool-identity
  trailers to commits; the owner has stripped them from history twice.
- **Threads.** Hard cap of 16 of the 32 threads. Full load made the display blink on 7 November.
- **Memory.** Use RAM responsibly: at most 24 GB for all research jobs, and never let a job reach its own
  MemoryMax.
  - GNOME's `gsd-housekeeping` shows a "device memory is nearly full" alarm whenever the kernel OOM-kills a user
    unit, even one killed only at its own limit.
  - Estimate memory before launching. cake_lpr keeps its whole `--CML_HEAP_SIZE` resident when the proof needs
    it; CaDiCaL needs roughly 150–250 bytes per literal plus proof buffers.
  - Read `/home/jay/research/data/memguard-20261113/MEMORY_POLICY.txt`.
- **Evidence.**
  - Only cake_lpr's line `s VERIFIED UNSAT` certifies an LRAT proof (lrat-check is unsound here; cake_lpr exits 0
    even when it rejects).
  - HiGHS statuses are never evidence; it once reported a false optimum in this project.
  - Labels: PROVED / CERTIFIED / EXACT TREE / COMPUTED / HEURISTIC.
- **Ask the owner first** for: deleting large proof directories, e-mails to Schroeder or the
  Subercaseaux–Mackey–Qian–Heule group, pushing, raising the thread cap.
- **Tools.** Python venv: `/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python`. C/C++ are welcome
  where Python is slow (g++, cmake, zlib, gmp; no Rust).

## 5. Next steps (ranked)

1. **Checks (a)–(c) of §1.2.** If level 13 certifies N66 ≤ 56 tonight, verify that certificate instead and use the
   Lean-rows-only chain (slices 18, 19).
2. **Write-up for the owner.** Write an ES(8) ≤ 309 summary record (chain, hashes, what is not Lean-checked). Then
   update the README "Beyond 310" section and math.md only with the owner's agreement.
3. **Robustness.** Slice 21 (running) and slice 22 give the route through the verified N66 ≤ 59.
4. **Lean.**
   - Export the capacity statements as hypotheses, plus Lemma A (Lo part) and Lemma S, on top of
     `SlopePartition` / `ResidualStates`.
   - Export the slice trees with the compact checker.
   - The certified CNFs need an LRAT-to-Lean route (see NOVELTY20261113B §4.1: Szeider, arXiv:2607.00815).
5. **ES(8) ≤ 308** (budget 34). See LO33N §4d (pair (65, 55): 24 of 3,792 contexts done; resume command in §6).
   It needs N66 ≤ 54 trivially, or new trees.
6. **Side lines.**
   - M(5;7) ≤ 36: wait for E2; then try N = 36.
   - Δ-conjecture: prove the cup-side form (DELTA2N §4.2b).
   - Compare 65 with 78 for N5 in any write-up.
