# VERIFY_ES307_FINAL: final independent read of claim es307-final-1118 (verifier VR, 18 November 2026, 11:52-12:04 KST)

**Verdict: CONFIRMED at the claimed label.** ES(8) ≤ 307 is PROVED, computer-assisted: a written chain over PROVED,
CERTIFIED and EXACT TREE inputs, at the trust level of the 308 chain. It is not Lean-checked as a whole and not refereed.
- The chain arithmetic is right.
- Every evidence file named in §5 of the record says what the record says.
- VR's own run of the rebuilt `tcheck_b35` reproduces EXACT TREE on `bb-s1`.
- The split of context 4782 into 8065-8080 is clean.

VR found no discrepancy that touches the bound. The wording problems in §6 are minor; one of them (W1) qualifies the
record's "every item passed".

Work folder (not in Git): `/home/jay/research/data/roadmap-20261115/pm1115/vr1118/` (V). W = `/home/jay/research/data/es308-20261114`.
VR wrote nothing into W or into the packet.

## 1. Chain (re-derived by VR)

- **Setting** (bridge §2-4, ROUTE307 §1.1): |S| ≤ 1 + |H| + |R|, |H| ≤ 187, |R| + h(C) = 154, C = F ⊔ Lo with |F| = 84
  and |Lo| = 70, and h_0 = 0.
- **h(F) ≥ 18:** nine rows of demand 6 on 28-state supports in F cover each F state exactly 3 times (9 · 28 = 252 =
  3 · 84). So 3 h(F) ≥ 54.
- **h(Lo) ≥ 15:** Lemma A gives h(Lo) ≥ 70 − N66, and N66 ≤ 55.
- **The 308 chain** gives h(C) ≥ 35.
- **Budget 35:** h(C) = 35 means h(F) + h(Lo) = 35. Then h(F) ∈ [18, 35 − 15] = [18, 20], so the cases are exactly
  **(18,17), (19,16), (20,15)**.
  - A slice tree with capacity rows (F, T) and (Lo, 35 − T) excludes every row-satisfying H with |H| ≤ 35 and 0 ∉ H,
    h(F) ≥ T and h(Lo) ≥ 35 − T. Each case meets its own slice's hypotheses.
  - (21,14) is ruled out by h(Lo) ≥ 15, and (17,18) by h(F) ≥ 18.
- **Hence** h(C) ≥ 36, |R| = 154 − h(C) ≤ 118 and |S| ≤ 1 + 187 + 118 = 306.
- **Forcing in Lean:** VR read the signatures in `ErdosSzekeres/Omission/PopulationBounds.lean`.
  `forces_of_population_bounds` gives `ForcesConvexNGon (B + R + 2) 8` = 307 for B = 187 and R = 118, and
  `avoiding_card_le_of_population_bounds` gives |S| ≤ B + R + 1 = 306.
- **Equality case** (record §5): 306 ≤ 1 + |H| + |R| ≤ 306 forces |H| = 187, |R| = 118 and h(C) = 36. This is right.
- **Scope of the record:** it claims exactly this and nothing stronger. It keeps N5-free, the lower bound 65 and the
  label caveats ("not Lean-checked as a whole, unrefereed").

## 2. Evidence (record §5, row by row)

| item | file read | finding |
|---|---|---|
| data/ | `data/SHA256SUMS` | `sha256sum -c`: 10/10 OK |
| live inputs | W files | the SHA-256 of master.json `71993a47…`, contexts.json `1923b8ee…`, master.txt `d2ccbbba…`, extra.json `de4bcceb…`, rows.txt `68fda5ef…` and the catalog `8c7fe9ef…` equal record §7. No file in `bb-s1` is newer than its `fastbb.log.jsonl` (09:30:49). No finder is running |
| C1 | `claims/p307-chain.verdict.json` | VS, CONFIRMED, 2026-11-16 18:42 (see W1) |
| C2 / L10 | `claims/p307v-l10-pycheck.verdict.json` | VB, CONFIRMED 03:08, with VB's own fourth implementation |
| N1 | `data/n66_cover_final.json` | COVER COMPLETE, 132 accepted, 0 rejected, 0 of 16,384 uncovered, 14 split states, deep |
| N2 | `VERIFY_N66CUBES_1118.md`, `_ALL.md` | "Four-check verified cover (own code): 100.00 % = COMPLETE"; the _ALL pass at 05:13 has 132 of 132 (see W4) |
| N3 | `VERIFY_N66LE55_FINAL.md` (VS), `_VN.md`, both verdict JSONs | both CONFIRMED at the claimed label. VN: exact partition with 0 doubly covered; cert.cnf = F_c + the cube's units byte for byte on all 132; trim ⊆ F_c ∪ units; fresh cake_lpr on `hooooo` and on one random cube |
| T1 | own `prep_rows.py` run (`V/prep-b35s20-v169.json`) | ok true: (F, 20), (Lo, 15), supports F (84) / Lo (70), the other 1,990 extra rows rhs 1, 4,642 rows. The rows file is byte-identical to the 09:31 run's |
| T2 | `data/rows_stated_v169.json` | ok, 4,642 rows, base 1,020 + 970 appended rows over 69 rounds (v101-v169; VR re-summed it to 970) from 111 folders, no problems |
| T3 | `audit/cuts-v1xx*/summary.json`, recounted by VR | 111 batch audits, all CERTIFIED. In each, rows = own-encoder matches = fresh cake acceptances = rows cutting the witness; 970 rows in all |
| T4 | `data/lrat_recheck_v169_summary.json` = `p307v/lrat-b35s20-v169/lrat-summary.json` (`f80a720e…`), and its `lrat-results.tsv` | 1,990/1,990 rows certified, 1,994 jobs (4 rows have two candidates), all ACCEPTED, 0 hash mismatches. VR checked every rhs-1 row of the **v169** extra.json against the TSV: each has an ACCEPTED job with CNF and LRAT hashes equal, the cake line, and the same support. All 1,994 `cake/*.out` contain the exact line `s VERIFIED UNSAT` |
| T5/T6 | `data/final_tree_check_verdict_v169.json`, `steps.log`, `p307v/final-b35s20-v169/compare.txt` | EXACT TREE (tcheck_b35 + pycheck_b35), 8,080 contexts, 238,116,145 nodes, 119,054,033 leaves, min margin 1, 0 differences |
| T7 | `audit/fresh-b35s20-v169-bbs1/summary.json` (`85566fc3…` ✓) | EXACT TREE (fresh full replay), 8,080/8,080, 238,116,145 nodes, 119,054,034 leaves, min margin 1, global pending 1. Master and extra hashes as above. Checker `35cb3050…` = `scripts/omission_tree.py`; tool `466aa324…` = `fresh_replay_v3.py`. Ran 09:57:08-10:51:21. The tool asserts master pending = contexts + 1 (the state-0 branch) and no internal pending |
| T8 | `VERIFY307/data/mutation_tests_b35.log` | 24 OK, "ALL CONTROLS BEHAVED AS EXPECTED" (see W2) |
| T9/T10 | below (§3, §4) | ok |

Tool hashes checked: `prepare_successor_b35.py` `10fad935…` (also in SUCCESSOR.json), `fresh_replay_v3.py` `466aa324…`
and `omission_tree.py` `35cb3050…`.

## 3. VR's own run of the tree check (rebuild, not new code)

- **Build:** `g++ -O2 -std=c++17 -o V/bin/tcheck_b35 VERIFY307/tools/tcheck_b35.cpp -lz -pthread`. The binary's SHA-256 is
  `a8c4f810a753e4f5e68f4a893a8259bd24c470e6f653cd47405ceacd02aff84c`, the same as the record's.
- **Rows:** `prep_rows.py` gave rc 0 (§2 T1).
- **Run:** unit `esr-vf-reader-tc` (CPUQuota 600 %, MemoryMax 8G, MemorySwapMax 0, RuntimeMaxSec 3600, nice 10), 6 threads,
  11:54:12-11:55:50 (1 min 37 s wall, 9 min 38 s CPU), rc 0.
  - systemd reports an "8G memory peak", which includes page cache from reading 32 GB.
  - memguard (anon + swap) lifted the kernel limit at 11:54:13, logged a total of 1,100 MB at 11:54:27 and never
    stopped the unit. There was no OOM event.
- **Result** (`V/tc-b35s20-v169.summary.json`, `d78e362b…`):
  - **EXACT TREE**: 8,080 contexts and 8,080 ctx files; master 16,347 nodes with 94 leaves;
  - **238,116,145 nodes**, 119,054,033 leaves (all weighted);
  - **min margin 1**, with 13,215,994 leaves at the minimum;
  - pending 0, over-budget 0, errors 0.
- **Comparisons** (own code `V/vr_checks.py`, output `V/vr_checks.json`):
  - The per-context TSV and the summary are byte-identical to the 09:31 final run's.
  - Per context, nodes, leaves and min margin equal T7's `contexts.jsonl` (0 differences of 8,080) and pycheck's
    `py.tsv` (0 differences; pycheck total 238,116,145).
  - The largest context is 4274 (640,843 nodes).
- This run is a re-run of the record's own C++ checker, not an independent implementation. The second and third
  implementations (pycheck_b35, check_tree) were not re-run by VR; VR only compared their outputs.

## 4. Split integrity (own code `V/split_check.py`, output `V/split_check.json`)

- **Master:** VR walked `bb/master.json` (8,065 contexts, labels 0-8064) and `bb-s1/master.json` (8,080) side by side.
  They are equal node for node, except at placeholder 4782.
  - In `bb-s1`, that position holds a subtree of branches only, with exactly the contexts **8065-8080** as leaves and
    no other leaf.
  - `bb-s1` has **no context 4782**.
  - Each new context extends 4782's (M, O) by 4 decisions.
- **contexts.json:** in both packets every entry equals the master path (branch `zero` = h_v 0 = occupied). The 8,064
  shared contexts are unchanged in path and entry. bb's masters still have the hashes in SUCCESSOR.json
  (`6afb7046…`, `04157a9d…`, `6912bb8b…`).
- **Negative control:** with the packets swapped, the check is rejected (exception, exit ≠ 0).
- **SUCCESSOR.json:** source `runs/b35s20/bb`, 8,064 contexts hard-linked (labels 0-8064 without 4782).
- **Spot check of 20 inherited files:** the 3 largest (4274 at 86.1 MB, 132 at 82.8 MB, 6254 at 76.7 MB) and 17 seeded
  random ones. Each is the same inode as in `bb` (nlink 2) and its SHA-256 equals SUCCESSOR.json: 20/20.
  - In addition, all 8,064 hashes that T7 recorded equal SUCCESSOR.json.
  - The 16 new files have nlink 1.
- **`bb-s1/fastbb.log.jsonl`** has exactly 16 `closed` events: one finder run, the split. There are no stray `.tmp`
  files.
- **`diff prepare_successor.py prepare_successor_b35.py`:** only line 2 (docstring) and line 17 (`RUN = …/runs/s20` →
  `…/runs/b35s20`, plus a trailing comment) differ.

## 5. Chain links that VR read as a second reviewer

- Link 1 (composition, 118 → 307, Lean signatures).
- Link 2 (same catalog `8c7fe9ef…`; walk from O = {0}; the only excluded branch is state 0 missing).
- Link 4 (budget-35 case list).

VR did not re-read links 3 (Lemma A, N66 model and SB soundness) and 5 (encoder soundness of the 1,990 rows). They rest
on unchanged written arguments, VS/VN's confirmations and the CERTIFIED CNFs.

## 6. Wording problems in the record (not edited)

- **W1.** §1 and the claim say "every item of VERIFY307 §1 has passed", but VERIFY307's C1 cell and §6a say "two
  reviewers per link, as for 308, remain to be assigned". The record's C1 row cites only VS's `p307-chain`. This read is a
  second review of links 1, 2 and 4 only (§5).
- **W2.** §6 says "24 single defects, each rejected by both T5 and T6". The log has 24 controls:
  - 21 single defects, rejected as expected;
  - 3 expected passes: `positive_control`, `rows_F_demand_minus_1` and `rows_F_demand_plus_1_still_valid`.

  §5 T8's "24/24 as expected" is right.
- **W3.** §8 says "the forcing step and the rows are Lean-checked". Only the 2,650 catalog rows are. The 1,020 coupled and
  970 appended rows are CERTIFIED per CNF and rest on the written encoder argument. In the same way, §1.1 L11 could
  name these rows' label, as ROUTE307 §1.5 does.
- **W4.** The N2 cell calls `VERIFY_N66CUBES_1118.md` "VB's full pass". That file is VB's round-17 record (27 cubes,
  04:34). The single pass over all 132 cubes is `VERIFY_N66CUBES_1118_ALL.md` (05:13). The conclusion is the same.
- **W5.** §4 and §7 say `prepare_successor_b35.py` "differs only in the packet path". The docstring and a comment also
  differ; there is no code difference.
- **W6.** §4 lists `hc169a` and `hc169b` without saying how they ended. `hc169a` exited with −6 (abort) after 10 of 28
  contexts, and `hc169b` exited with 4. Both are finder receipts (COMPUTED); the final replays cover every file.
- **W7.** Trivial:
  - N3 gives VN's time as 08:31, but VN's file and verdict say 08:32.
  - T9's "the 8,064 original labels without 4782" should read "the original labels 0-8064 except 4782 (8,064)".
- **W8.** In the linked checklist (not the record), VERIFY307's header ("NOT REACHED", 04:45) and its T1-T10 status
  cells are stale. The final results are only in the record's §5.

## 7. Not checked by VR

- **Not re-run:** pycheck_b35, fresh_replay_v3, cake_lpr on any row or N66 cube, the batch audits (counted only), the
  mutation controls (log read only), and the N66 cover checkers.
- **Not re-derived:**
  - Lemma A and the N66 model and SB soundness;
  - the encoder soundness of the coupled and appended rows;
  - the 308 chain inputs L1-L9, including the 86 `pending_kernel` catalog rows (VERIFY308 follow-up) and the Lean
    proofs themselves (signatures read only).
- **Not verified:** the finder history (progress times, "no cube SAT"), and the literature or novelty statement.
- **The tree check is a byte-identical re-run** of the record's C++ checker plus own comparison code, not an
  independent leaf-rule implementation.
