# s3520-gate: launch gate for the last Res118 slice, s35_20 (22 Nov 2026)

## 1. Headline (status; updated after every milestone)

- **21:20 KST: plan and pre-registration written (§2, §3). No 3520 command has run yet.** Nothing is claimed.
- Item `s35_20-gate` of the Lean wave (owner: "lean verify everything"). This is a **gate**, not the campaign: the
  campaign (about 119 M leaves) is **not** launched here. Track `s20`, slot `g`, units `esr-s20-g-<job>`.
- Work directory (the only place written): `/home/jay/research/data/formalize-20261122/s3520-gate`.
  `res-slices-fv` (driver `esr-fvr-drv` running s35_19) is read-only for this item.

## 2. Plan (milestones)

| # | milestone | state |
|---|---|---|
| M0 | README with plan and the s35_20 pre-registration (§3) | done 21:20 |
| M1 | patched tools as new files in `tools/` with diffs in `diffs/`: `slice_export_v3.py` (context-id fix, streamed pre-pass, streamed compact context loader, lean unit export writing each module as it is built), `slice_export_w13fix.py` (reference: `slice_export_w13.py` + the id fix only), `compile.sh` (own `D`), `drive_v3.py` | |
| M2 | byte-identity controls: v3 vs reference on 3318 unit 0 and on one small real 3520 unit (module sha256 and manifest stats); tool hashes frozen afterwards | |
| M3 | streamed pre-pass of s35_20 (all 8,080 contexts): acceptance in §3 | |
| M4 | memory ladder: export a 40,000–60,000-leaf context, extrapolate, then export ctx-4274 (largest, 320,422 leaves) under MemoryMax ≤ 6G; anon + shmem sampled from the unit's own memory.stat | |
| M5 | compile every chunk module of the ctx-4274 unit (one or two at a time, gated loop units), same checker, catalog and parameters as the campaign (unit 40,000, chunk 8,000, block 64, 16 entries per word, profiler on) | |
| M6 | context-level sub-root theorem for the ctx-4274 unit; axiom lines checked with `res-slices-fv/tools/axlines.py` (unmodified, through a view directory) | |
| M7 | negative control: one corrupted chunk (separate `--out` and olean dir) rejected by Lean | |
| M8 | `LAUNCH_PLAN.md`: re-calibrated cost (HEURISTIC), wall time at 3/6/12 compiles, disk, swap-in commands for drive v3, pre-launch checks | |

## 3. PRE-REGISTRATION of s35_20 (tag 3520), written 21:20 KST before any 3520 file was generated

- **Lean statement**, Res118's hypothesis copied verbatim from
  `/home/jay/research/data/formalize-20261122/res118/lean/Res118/Final.lean` (sha256
  `7f9198b7660c2ff6329fe5ac3a640b1efa0e09d68f60b65c263cb3cc2713d83b`, namespace `Res118`):
  `(s35_20 : ResSliceExcludes (rowsP ++ rowsQ ++ rowsA) 35 20)`.
  The campaign's theorem will be
  `theorem s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20`, proved as
  `Res118.slice_of_root RS.cat3520_ok`, then
  `rw [List.length_append, List.length_append, Res118.rows_lengths.1, Res118.rows_lengths.2.1, Res118.rows_lengths.2.2.2]`
  (copied from `res-slices-fv/lean/RS/FinalTest3520.lean`, which compiled with lean_rc 0 at 20:07), then
  `exact RS3520.root`, where
  `RS3520.root : ¬ ∃ holes : Fin 154 → ℕ, FFeas fcatS3520 4642 154 35 (pmask (zerosF 154) [(0, 2)]) holes`.
  The Res118 specialisation then takes `RS.s35_20` as its argument `s35_20` (Lean checks the match).
- **Tree** (read-only): `/home/jay/research/data/es308-20261114/runs/b35s20/bb-s1`, `master.json` sha256
  `71993a47f134ff06afa1d0029f39b7f6feceaf23bfee17b945e32329498e9dea` (hashed 21:16; equals the T7 fresh replay
  summary `LO33N20261113/budget34/audit/fresh-b35s20-v169-bbs1/summary.json` and res118 README); budget 35, root 0,
  16,347 master nodes (8,173 branch, 8,080 context placeholders, 94 weighted leaves), `contexts: 8080`; context ids
  0..8080 with **4782 absent** (read 21:16).
- **Expected leaf count: 119,054,033** = T7's 119,054,034 (fresh_replay_v3) minus the pending "state 0 missing" leaf,
  which the mask `[(0, 2)]` excludes; it equals the T5/T6 count (tcheck_b35 + pycheck_b35, ES307 README T6:
  238,116,145 nodes, 119,054,033 leaves, minimum margin 1). The exporter's `skeleton.json` `total_leaves` must equal it.
- **Rows**: `/home/jay/research/data/es308-20261114/inputs/b35s20-v169/extra.json` sha256
  `de4bcceba6d0c80ce6f63cbef15822cac8300780607c738569999a7d94b81916`: 1,992 rows, row 0 = (F, 20), row 1 = (Lo, 15),
  1,990 unit rows of demand 1. Catalog rows m = 2,650 + 1,992 = 4,642 (13 bits: the w13 exporter, J = K << 13).
- **Catalog and bridge** (built by res-slices-fv at 20:06–20:08; used read-only): `RS.Cat3520` chain
  `Cat3520_p0..p5`, `Cat3520` (olean sha256 `f7904232…`, `53624fc2…`, `1e4d334e…`, `d5b3ddc3…`, `5ce3953c…`,
  `c66baffd…`, `247855f5…`), `RS.Bridge3520` olean `11dfffa7d302b60e32700d9c1a6eb5492d9499a9c82bb6f247a0704a3da93193`
  (= res-slices-fv README §7), `RS.cat3520_ok : Res118.SliceCatalog fcatS3520 (rowsP ++ rowsQ ++ rowsA) 35 20`.
- **Gate unit**: context 4274, the largest (T7 `contexts.jsonl`: 640,843 nodes, 320,422 leaves, minimum margin 1,
  max used row 4520). A placeholder is never split, so it is one unit by itself, and its unit-top theorem is the
  context-level theorem
  `¬ ∃ holes : Fin 154 → ℕ, FFeas fcatS3520 4642 154 35 (pmask (zerosF 154) P) holes`, with P = the context's master
  path (innermost first) followed by `(0, 2)`.
- **Gate acceptance** (all required; not accepted on any Python output alone):
  1. pre-pass: 8,080 contexts, id 4782 absent; leaves = branches + 1 in every context; every context's leaf count
     (and gz sha256, if the T7 field is the gz hash) equals T7 `contexts.jsonl`; `total_leaves` = 119,054,033;
  2. export of the ctx-4274 unit: manifest leaves 320,422, minimum margin ≥ 1, 0 leaf-test failures, exporter anon
     peak well under 4 GB;
  3. every chunk module of the unit: log ends `lean_rc=0` and has a whole line
     `'<module>.ex<s>' depends on axioms: [propext, Classical.choice, Quot.sound]` for each subtree root (axlines);
  4. the sub-root theorem compiles with lean_rc 0 and the standard axiom line;
  5. the corrupted chunk is rejected ("decide proved that the proposition … is false"), rc ≠ 0, no olean.

## 4. Progress log (KST)

- 21:16 orientation; master read (ids, 4782 gap); memory guard `esr-memguard-1122f` active with track `s20=8000`.
