# v182-lean: chi_rainbow(G) = 6 for the 182-vertex omission-layer graph, in Lean modulo the 4,404 piece verdicts

Item `v182-lean` (#810), slot `l182` (units `esr-ag-l182-<job>`). Work directory (the only place this agent writes):
`/home/jay/research/data/formalize-20261122/v182-lean`. Nothing in the git repository is edited; no git writes.

Source of the result: `/home/jay/research/data/e810-linux-20261121/v182-recheck` (README, verify/ with both VERIFY
files) and wave 1 `/home/jay/research/data/e810-linux-20261121/a-t34-sat182` (README 3.3: reduction, base CNF
`a2/g182_k5_st_sb2.cnf` sha256 c3ae5224…7074, Y1/Y2 cube split, certify.jsonl). Pattern: ENCBLEAN (Lean-defined CNF,
printed text hashed against the certified files, cake_lpr verdicts as the one trusted step; trust items E1-E6), as
in `formalize-20261122/n66enc`.

## 1. Headline (22 Nov 2026, ~18:40 KST)

**All milestones done; final clean rebuild PASS.**

- `V182Geo.rainbowColorable_six : RainbowColorable 6` — **Lean-checked** (no hypothesis; axioms
  [propext, Classical.choice, Quot.sound]).
- `V182Geo.not_rainbowColorable_five : PieceVerdicts → ¬ RainbowColorable 5` and
  `V182Geo.chiRainbow_eq_six : PieceVerdicts → chiRainbow = 6` — **Lean-checked modulo `PieceVerdicts`**, i.e. the
  4,404 cake_lpr verdicts (`s VERIFIED UNSAT`, CERTIFIED in the records), carried into Lean by the hash binding M9
  under trust items E1-E6 (DESIGN.md §4). Axioms [propext, Classical.choice, Quot.sound] (`#guard_msgs` in
  `lean/V182Geo/End.lean`).
- In Lean: the definition of G and of rainbow colourings; the base CNF B as a Lean generator whose printed text is
  byte-identical to the certified file; soundness of every clause family; the 10-unit symmetry breaking
  (normalisation); the cube cover (84 direct + 36 × 120, shape also kernel-checked); the six-colouring.
- Outside Lean: E1 (printer output = certified bytes; M9 COMPUTED evidence: 4,404/4,404 SHA-256 matches), E2 (the
  verdicts), E3 (cake_lpr's DIMACS reading = `EncB.parseDimacs`), E4 (Lean compiler/runtime of the printer), E5
  (kernel, Mathlib, definitions), E6 (SHA-256).

Unrefereed. No new mathematical claim: this formalizes the existing result `chi_rainbow(G) = 6` (CERTIFIED pieces +
exact cover + PROVED reduction in the records). Labels of the records are unchanged.

<!-- STATUS -->
- 22 Nov ~18:45 KST: ENCBLEAN closure tied to its sources (`logs/encb_check.log`: IR C and oleans byte-identical
  for Gen, Dimacs, Coded, Cover, Render). Record fixes after the final review (§4, §6a, §8; DESIGN §3.3).
- 22 Nov ~18:40 KST: **final clean rebuild PASS** (unit esr-ag-l182-rb2, `tools/rebuild_all.sh`,
  `logs/rebuild_all.log`): all 15 modules recompiled from source into `build_clean/` (75.6 s, peak RSS 2.12 GB = 61 %
  of MemoryMax); End's axiom guards pass; the relinked printer is byte-identical to the M9 exe (b0b270cb…1c5d), Gen's
  IR C identical, `base` reprints B (c3ae5224…7074). Source audit PASS (`logs/audit.log`). Printer sources unchanged
  since M9 (`logs/m9_freeze.sha256` vs `logs/final_manifest.sha256`).
- 22 Nov ~18:35 KST: **M6 done**: `V182Geo/End.lean` compiles: `chiRainbow_eq_six`, `chiRainbow_eq_six'` (hypothesis
  unfolded), `pieces_shape` (kernel: 4,404 pieces, 84 direct, `splitSet` 36 distinct indices < 120); `#guard_msgs`
  axiom guards for all four theorems (`logs/e3.log`). Control `V182Ctl/WalkMut.lean`: the walk check passes on the
  table at start masks 14, 15 and fails at both when edge 0 is recoloured 5 → 0 (`logs/c1.log`).
- 22 Nov ~18:31 KST: **M5 done**: `rainbowColorable_six` (`V182Geo/Six.lean`, `logs/s7.log`) with the kernel walk
  check in 23 chunks (`V182Chk/WalkA.lean` 22.8 s / 1.87 GB, `WalkB.lean` 19.7 s / 1.68 GB). Incident: the first
  attempt (walk check inside the Mathlib module) was stopped cleanly by the memory guard at 3,373 MB
  (`MEMGUARD_STOPPED_esr-ag-l182-s1.txt`, no OOM kill); a single Std-only module then peaked at 3.09 GB (88 % of
  MemoryMax, above the 80 % sizing rule); split into two chunk modules since.
- 22 Nov ~18:22 KST: **M4 done**: `normalize` and `not_rainbowColorable_five` (`V182Geo/Norm.lean`, `logs/g9.log`).
- 22 Nov ~18:18 KST: **M3 done**: `exists_piece`, `no_normal_colouring` (`V182Geo/Cover.lean`, `logs/g6.log`).
- 22 Nov ~18:13 KST: **M2 done**: `baseCnf_sat`, `baseCnf_wf`, `pieceCube_wf`, `piece_unsat` (`V182Geo/Sound.lean`);
  bridge `cyc_bridge`, `conflict_ne` (`V182Geo/Masks.lean`).
- 22 Nov ~18:05 KST: **M9 PASS** (unit esr-ag-l182-m9a, 36 s, 51 MB; `tools/hash_binding.py`,
  `logs/m9_hash_binding.tsv` + `.summary.json`), details §5.
- 22 Nov ~18:01 KST: **M1 PASS**: `v182print base` prints B byte-identically (sha256 c3ae5224…7074).
- 22 Nov ~17:57 KST: M0 DESIGN.md written.
- 22 Nov 17:45 KST: work directory created; orientation done; README written.
<!-- /STATUS -->

## 2. Statement (`lean/V182Geo/Defs.lean`, printed in `logs/e3.log`)

- `V := {s : Finset (Fin 8) // 3 ≤ s.card ∧ s.card ≤ 5}`; `G : SimpleGraph V`,
  `G.Adj u v ↔ (u ⊆ v ∧ |v| = |u| + 1) ∨ (v ⊆ u ∧ |u| = |v| + 1)` (inclusions between consecutive sizes only).
- `IsFourCycle a b c d`: pairwise distinct, `a~b`, `b~c`, `c~d`, `d~a` (chords allowed by the definition).
- `IsRainbow (col : G.edgeSet → α)`: the four edge colours of every 4-cycle subgraph are pairwise distinct (no
  properness required). `RainbowColorable k := ∃ col : G.edgeSet → Fin k, IsRainbow col`;
  `chiRainbow := sInf {k | RainbowColorable k}`.
- `PieceVerdicts := ∀ q ∈ V182Enc.pieces, ∀ nv F, EncB.parseDimacs (V182Enc.pieceText q) = some (nv, F) →
  ¬ EncB.DimacsSatisfiable F`, where `pieceText q` is exactly the expression the printer writes for piece `q`.

## 3. Model and soundness (DESIGN.md §2-§3)

- **CNF** (`lean/V182Enc/Gen.lean`, Std-only): `baseCnf = ALO ++ CONF ++ AMO ++ STAR ++ UNITS` in rainbow.py's file
  order; `conflict e f` = distinct edges in a common structural 4-cycle `cyc X p q`. Byte identity with the certified
  B (M1) also shows that this conflict relation equals Python's.
- **Bridge** (`Masks`): each `cyc X p q` is a 4-cycle subgraph of G edge by edge, so a rainbow colouring separates
  conflicting edges.
- **Soundness** (`Sound`): the indicator `ind ψ` of a rainbow 5-colouring `ψ` that satisfies the units satisfies
  every clause of B; all literals are nonzero with `|l| ≤ 2800`, so `EncB.parseDimacs_renderCube` turns
  `PieceVerdicts` into `¬ DimacsSatisfiable (cubeCnf baseCnf (pieceCube q))` for each listed piece.
- **Cover** (`Cover`): the colours on the Y1 star (5 pairwise conflicting edges) are some lexicographic permutation
  `π_n` (`mem_permsOf`), and likewise on the Y2 star; the piece `(n, none)` or `(n, some m)` is in `pieces`.
- **Normalisation** (`Norm`, wave-1 README 3.3): a colour map makes `σ_X0(x) = x − 3`; then `norm_finite` (kernel,
  over the 120 permutations of the normalised `τ_Y0`) supplies a map `σ` of `{0..7}` fixing 3, 4 and preserving
  `{0,1,2}`, `{5,6,7}`, and a colour map, that reach the normal form `τ_Y0 = (0,1,4,2,3)`. Relabelling preserves
  rainbowness (`isRainbowS_transform`, generic `Finset.map` argument).
- **Six-colouring** (`Six`, `V182Chk/*`): adjacent vertices' masks differ in one bit, so every 4-cycle subgraph is a
  closed bit-toggle walk; the kernel checks all of them (4,480 qualify) on the notes' table.
- **χ = 6**: monotonicity in `k` and `Nat.sInf`.

## 4. Method and build

- Lean 4.24.0 binary `/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean`, bare `lean -j1 -R lean`,
  read-only LEAN_PATH over the repository's Mathlib package oleans (f897ebcf) and ENCBLEAN's oleans
  (`EncB.Render`, `EncB.Cover`, `EncB.Dimacs`); outputs only in `build/`, `build_clean/`. No lake anywhere.
- Std-only printer `v182print` (`lean/V182Enc/{Gen,Main}.lean`; linked with ENCBLEAN's IR C for Gen, Dimacs, Coded,
  Cover, Render by `tools/link.sh`). Modes: `stats`, `base`, `list`, `piece I`, `all DIR`, control `cube N M`.
- Theorem modules: `V182Geo/{Defs,Masks,Sound,Cover,Norm,SixData,Six,End}.lean`, `V182Chk/{WalkDefs,WalkA,WalkB,
  Walk}.lean` (Std-only kernel chunks), control `V182Ctl/WalkMut.lean`.
- Kernel checks (`decide +kernel`, never `native_decide`): `card_ofMask_eq_pc` (256 masks), `cycX`/`cycY`/`cycXY`,
  the 10 unit edges, `norm_finite`, `perms5_length`, `y1Star_conf`/`y2Star_conf`, `isV_spec`, `onebit_shl`,
  `walk_c0..22`, `pieces_shape`. Nothing evaluates `baseCnf` or `confCls` in the kernel.
- Compiles ran in units `esr-ag-l182-*` (CPUQuota 100 %, MemoryMax 3500M, MemorySwapMax 0, RuntimeMaxSec 7200,
  nice 10) after `tools/gate.sh` (no YIELD, Tctl < 86 C, agent pool anon < 4,500 MB), one at a time, with the one
  exception listed in §6a.
- ENCBLEAN's oleans and IR C used here are tied to its sources: `tools/encb_check.sh` (unit esr-ag-l182-encb,
  7 s, `logs/encb_check.log`) recompiled copies of `EncB/{Gen,Dimacs,Coded,Cover,Render}.lean` (sha256 equal to the
  record's files, `ref/encb/`) and got byte-identical IR C and oleans for all five.

## 5. Results

| module | compile (final clean rebuild) | content |
|---|---|---|
| V182Enc/Gen, Main | 0.47 s, 0.33 s | generator, printer |
| V182Geo/Defs | 1.36 s, 1.55 GB | statement, monotonicity, automorphisms |
| V182Geo/Masks | 3.10 s, 1.72 GB | bits, numbered edges, bridge |
| V182Geo/Sound | 1.57 s, 1.56 GB | family soundness, bounds, verdict transfer |
| V182Geo/Cover | 4.26 s, 1.97 GB | permutations, cover |
| V182Geo/Norm | 5.07 s, 2.12 GB | normalisation, `not_rainbowColorable_five` |
| V182Chk/WalkA, WalkB | 21.4 s / 1.75 GB, 19.5 s / 1.64 GB | kernel walk chunks |
| V182Geo/Six | 1.55 s, 1.64 GB | `rainbowColorable_six` |
| V182Geo/End | 3.07 s, 1.86 GB | `chiRainbow_eq_six`, axiom guards |

**M9 (hash binding, `logs/m9_hash_binding.summary.json`, ALL_OK true).** The piece list comes from the exe
(`v182print list`): 4,404 pieces = 84 direct + 36 × 120, distinct tags. For every piece the SHA-256 of the printed
`pieceText` equals the campaign certify.jsonl `cnf_sha256` and the campaign CNF file on disk; the campaign cake
output has the exact line `s VERIFIED UNSAT`; and an independent cake_lpr re-run with the same CNF sha, the campaign
LRAT sha and the exact line exists (wave-1 verifier 1,623 pieces, recheck 2,781, rebuild lens 2,781). Exe
b0b270cb…1c5d.

## 6. Controls (each can fail)

- M9: the unlisted cube (36, -) prints a text whose record is the abandoned timeout → FAIL as intended; piece 0's
  hash against piece 1's record → FAIL; `piece 0` output = `all` output; the exact-line test rejects a trailing space
  and a `c ` prefix.
- Six-colouring: recolouring edge 0 (5 → 0) makes the kernel walk check fail at start masks 14 and 15
  (`V182Ctl.ctl_mut`), while the true table passes there (`ctl_orig`). Python simulation of the same check
  (`tools/gen_six.py`): 4,480 walks, 0 bad; failing masks under the mutation 14, 15, 30, 31, 142, 143.
- The six-colour table (wave 1's `col6_mine.json`) equals my own decoding of `notes_src/diamond-colors.txt`
  (`tools/gen_six.py`).
- Compile errors met on the way (kept in `logs/g3.log`, `g5.log`, `g7.log`, `g8.log`, `s6.log`, `e2.log`) were tactic
  or name errors, each fixed in the source; none was worked around with a weaker statement.

## 6a. Incidents and rule deviations (no effect on any result)

- The Main rebuild and relink that produced the M9 exe (`logs/m1b2.log`, about 2 s) ran in the foreground after
  `tools/gate.sh`, not in a unit. The final clean rebuild rb2, run in a unit, reproduced that exe byte for byte.
- Foreground runs of a few seconds outside units: `v182print stats` and `base` (6.5-6.8 s each, 18 MB),
  `tools/gen_six.py`, `tools/gen_walk.py`, the Python control simulation and `tools/audit.sh` (each under 2 s).
- Unit esr-ag-l182-s1 (the walk check inside the Mathlib module Six) was stopped cleanly by the memory guard at
  3,373 MB of 3,500 MB (`MEMGUARD_STOPPED_esr-ag-l182-s1.txt`; no kernel OOM kill). Unit s2 (the walk check as one
  Std-only module) finished but peaked at 3.09 GB, 88 % of its MemoryMax, above the 80 % sizing rule. Both fixed by
  moving the check into Std-only chunk modules (`V182Chk/WalkA`, `WalkB`: 1.75 / 1.64 GB in the final rebuild).
- Waiting: after starting units g3-g9 I used a fixed `sleep` of 20-40 s before reading the log, and later
  until-loops polling every 5-10 s for my own units (the 60-s poll of rule 3 applies to the start gates, which
  `tools/gate.sh` follows).

## 7. Files and hashes (full list: `logs/final_manifest.sha256`, 46 entries)

- `lean/V182Enc/Gen.lean` 6d03f39a3214c7a40da903b879e61a07f27014a33c8a7c31cd5cf214a4a3bab7 (frozen since M9)
- `lean/V182Enc/Main.lean` e418a316a8de004375e69c93589739ea7a99591b913f547417ee3b8ed1bc285b (frozen since M9)
- `build/bin/v182print` = `build_clean/bin/v182print` b0b270cb5840bb92151900b77eb76ff8be1b71efd3dee93dbfe198ed6a531c5d
- `ref/rainbow.py` a6c33ef9…05d8, `ref/cubes.py` 0f45686c…c3b0 (= the wave-1 files; `ref/SHA256SUMS.ref`)
- Inputs read: B c3ae5224…7074; campaign certify.jsonl, cube CNFs and cake outputs under `a-t34-sat182/a2/`;
  `a-t34-sat182/verify/cake/{results.jsonl,out/}`; `v182-recheck/{status.jsonl,out/}`,
  `v182-recheck/verify/{vcake_status.jsonl,out/}`; `verify/a2/col6_mine.json` 22cee12c…1578;
  `notes_src/diamond-colors.txt`.

## 8. What remains / caveats

- The verdicts stay outside Lean (E2), as do E1, E4, E6 and E3: it is trusted that cake_lpr reads each piece file as
  the clause list `EncB.parseDimacs` returns for it (ENCBLEAN's parser is not modelled on cake_lpr's source; its
  evidence concerns its own texts). This run adds no new E3 evidence. A kernel replay of the 64 GB of LRAT is not
  attempted.
- Only the direction "a rainbow 5-colouring gives a satisfying assignment of some listed piece" is formalized
  (that is all the theorem needs). The converse "B SAT iff a rainbow 5-colouring exists" of wave-1 README 3.3 is not
  formalized, nor is the classification of the 84 Y1 cubes as trivial.
- The 1,623 wave-1 pieces have one independent cake re-run, the 2,781 others two (records; not re-run here).
- Possible next steps: none needed for this item. The proofs' `.lrat.zst` files remain the owner's decision.

## 9. Resume / re-run

From this directory: `tools/gate.sh` then
- full clean rebuild: `systemd-run --user --unit=esr-ag-l182-<job> -p CPUQuota=100% -p MemoryMax=3500M
  -p MemorySwapMax=0 -p RuntimeMaxSec=7200 --nice=10 --working-directory=$PWD /bin/bash -c
  "/usr/bin/time -v tools/rebuild_all.sh > logs/rebuild_all.log 2>&1"` (about 76 s);
- hash binding: the same unit template with `tools/m9.sh` (about 36 s; writes and deletes 1.4 GB in `tmp_m9/`);
- one module: `tools/run_mod.sh <job> V182Geo/<Mod>`; audit: `tools/audit.sh`.
