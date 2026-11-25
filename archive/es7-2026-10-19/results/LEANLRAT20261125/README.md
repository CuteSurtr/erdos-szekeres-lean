# LEANLRAT20261125: a second verified LRAT checker on the kept proofs of ES(8) <= 302

25 Nov 2026, KST, Linux. Work directory `~/research/data/lrat-lean-20261125`. Built and run inside the project only; not
reviewed by anyone else.

## 1. Result

Every one of the **2,654 kept LRAT proofs** behind two verdict hypotheses of the end theorem of ES(8) <= 302 was
accepted by **Lean core's verified LRAT checker** `Std.Tactic.BVDecide.LRAT.check` (Lean 4.24.0), each on the text
printed by the frozen Lean printer of the hypothesis:

| hypothesis | texts | printer (frozen exe) | accepted |
|---|---|---|---|
| H-ROWS (rows P/Q/U/A of Res118) | 2,025 (812 + 208 + 35 + 970) | `rowprint row B i` (`eabe3791…`) | 2,025 |
| H-N66R (N66 level-15 row certificates) | 629 (421 T + 208 C) | `r15rowprint t/c k` (`6b9af2c6…`); T 208: `st 208 trim208.idx` | 629 |

`data/results.jsonl` (one line per text: text SHA-256, proof file and its SHA-256, sizes, time, the checker's `s` line),
`data/summary.json` (2,654 items, 2,653 ACCEPT in the campaign, 1 SPECIAL), `data/special_t208.json` (T 208).
Checker time 4,016 s in total (largest: 22 s, a 144 MB text with a 69 MB proof); peak 4.7 GB.

**What this adds.** These verdicts were CERTIFIED by cake_lpr (CakeML, verified in HOL4). They are now also accepted
by a checker whose soundness is proved in Lean: `LRAT.check_sound : check proof cnf = true → cnf.Unsat` (core,
`Std/Tactic/BVDecide/LRAT/Checker.lean`). Each verdict therefore rests on two independently verified checkers. The
labels do not change: cake_lpr's line stays the certificate (es-research §2), this is a second check (E2).

**Not covered:** the 105 N66 cube leaves (H-N66C): their proofs were deleted on 24 Nov; the re-solve of
`n66-resolve-20261125` keeps the new ones, but at about 10 GB each they exceed this driver's memory (it loads a whole
proof). The fivefold verdict of FORMAL20261122/fivefold was checked the same way (`../FORMAL20261122/fivefold/lrat-lean`).

## 2. Method and trust

- `tools/LeanLrat.lean` (strict) and `tools/LeanLrat2.lean` (header-tolerant): parse the DIMACS text into core's
  `CNF Nat` (DIMACS variable `i` is `i - 1`, as core's printer adds 1), load the proof with core's
  `LRAT.loadLRATProof`, and print `s VERIFIED UNSAT (Std.Tactic.BVDecide.LRAT.check; sound by LRAT.check_sound)` only if
  `LRAT.check` returns `true` **and** the parse is validated: the strict form requires core's printer
  `Std.Sat.CNF.dimacs` to reproduce the input text byte for byte; the tolerant form requires the clause lines to be
  byte-identical to core's printer output and the header to be exactly `p cnf NV NC` with `NC` the clause count and `NV`
  at least the largest variable used. Compiled with `lean -c` + `leanc` (binaries `leanlrat` `c92230f0…`, `leanlrat2`
  `43465533…`; sources `5006a0c4…`, `57e20e0c…`); run natively, so the trust is core's proof plus the Lean compiler and
  runtime (E4), not the kernel; the DIMACS reader is not verified but checked per text.
- `tools/second_check.py`: for each text, prints it with the pinned printer, requires its SHA-256 = the hash bound by
  the M9 tables (`res118-rowblocks/logs/m9_binding.tsv`, `n66-l15-rows/logs/m9rows.tsv`), takes the proof the T4
  re-check tables (`p307v/lrat-b35s20-v169`, `lrat-b35s19-v16`) or VB's job record (`n66-20261113/vfy15/rows/jobs`)
  names, requires its SHA-256 = the recorded one, and runs `leanlrat`. 2,653 texts passed the strict form.
- **T 208** (its certified CNF is the trimmed text `349b6c6c…` that `st 208 trim208.idx` prints; its header declares
  30,247 variables, more than the trimmed clauses use) fails the strict byte round trip by design and was accepted by
  `leanlrat2` (`data/special_t208.json`; proof `d0e97e74…` = the record).
- Controls (`test/`): PHP(4,3) and its CaDiCaL proof accepted; rejected with `s NOT VERIFIED`: the satisfiable PHP(4,3)
  minus one clause with the same proof, a final step whose hint is a missing clause id, the proof with its first lemma
  dropped; removing one hint of the final step is accepted (correctly: the remaining hints still give the conflict).
  For `leanlrat2` also: a header declaring more variables is accepted, one declaring fewer than used is refused
  (`s NOT CHECKED`). Both binaries give the same verdicts on all common controls.

## 3. Deviations and incidents (all on 25 Nov)

- The first run used `zstd` on every proof, but the 1,213 Q/U/A proofs live in `es308-20261114/cuts-*` either
  uncompressed (`system.lrat`) or compressed later (`system.lrat.zst`, the T4 table still names `system.lrat`): 760
  items reported `zstd failed` (no checker run). The driver was fixed (read uncompressed proofs in place, never delete
  them; fall back to `.zst`), the 760 lines removed from `results.jsonl` (the first run is kept in
  `data/results.first-run-with-zstd-bug.jsonl`) and the items re-run.
- The memory guard stopped the run at 22:07 when one certificate check reached the unit's 3 GB limit
  (`data/memguard_stop_2207_esr-ll2-c302.txt`; no kernel OOM); the remaining certificates ran in a 6 GB unit (peak 4.7 GB).
- A first try of T 208 was stopped by the memory guard (its printer needs 2.9 GB); re-run in a larger unit.
