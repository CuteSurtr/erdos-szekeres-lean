# combined part 3: FV302's tree and the slice s35_20 discharged (PRE-REGISTRATION, written 25 Nov 2026 16:02 KST)

Written before `E302ZZ.Final` (FV302) and `RS.Final3520` (res-slices-fv) exist: at 16:02 FV302 had 29,905 chunk
modules and 29 of 32 sub-roots compiled, s35_20 20,855 modules (no Root, no Final). Nothing here has been compiled.
No bound and no research label changes before §6 holds and the advisor has been consulted (es-research §7).

## 1. Gates (all must hold before the first compile)

1. **FV302 accepted**: `fv302-20261124/PLAN.md` acceptance items 1-4 pass and are logged there (item 3 via
   `tools/axiom_audit.py` over every module log).
2. **s35_20 accepted** by the res-slices-fv §9 finish recipe with tag 3520: `RS.s35_20` and `RS.residual_bound_118_fv`
   print [propext, Classical.choice, Quot.sound] with `lean_rc=0`; `audit.py 3520` reports `"problems": []` apart
   from split axiom lines, which `axlines.py 3520 --reprint` settles (`"n_problems": 0`); every unit manifest has
   `min_margin` 1 and `lean_test_failures` 0; the leaf sum is **119,054,034** (the pre-registered tree: 238,116,145
   nodes, REMAINS.md H-S3520); the six-slice specialisation is snapshotted in `data/spec-snapshots/`.
3. Both drivers (`esr-fv2-drv`, `esr-fvr-drv`) have exited; no YIELD file; Tctl < 86 C; `cpu_free.sh esr` >= 1.

## 2. Source and statement

- `src/Combined/ES302Final.lean`, sha256 `950be9327271e9799b1233d17a176805c2a8d8f9b5adc0e2a293c13d75acfee1`:
  `Combined.es302_verdicts`, `Combined.es304_verdicts`, `Combined.residual_bound_118_verdicts`, each the `_s3519`
  form of part 2 applied to `E302ZZ.Final.excludes_69` (302 only) and `RS.s35_20`.
- Expected `#check` of the end theorem (6 explicit hypotheses, all cake_lpr verdict props):
  `Combined.es302_verdicts (cubes : N66R15Enc.CubesUnsat105R) (certs : N66R15Geo.RowCertsUnsat)
  (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
  (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA) : ForcesConvexNGon 302 8`.
- Four `example`s pin the types mechanically: `excludes_69 : ExcludesHoleBudgetZZsN 16 69`,
  `forces_302_of_n54_res : N66Bound 54 → ResidualBound 118 → ForcesConvexNGon 302 8` (closes the 25 Nov review
  finding that FV302's acceptance checked axioms but not the elaborated statement), `RS.s35_20` with Res118's own
  arguments, and `es302_verdicts` as a plain implication.
- Three `#guard_msgs` axiom guards: exactly [propext, Classical.choice, Quot.sound].

## 3. LEAN_PATH

`tools/env2.sh` unchanged, plus two roots appended: `/home/jay/research/data/fv302-20261124/olean` (E302ZZ/*,
CompactChecker/FcatZZs16, BridgeZZs16) and `links3/` (file-level symlinks to res-slices-fv's `RS/Final3520`,
`RS/Bridge3520`, `RS/Cat3520*`, `RS3520/*` and the updated `RS/Res118FV` only if needed), built by a copy of
`tools/mklinks.py` for tag 3520 with the pins of `res-slices-fv/data/audit-3520.json`. The two-providers check over
the whole path must report no module file with two providers.

## 4. Control

`controls/Bad302.lean` (sha256 `2466006c9318b64261b99b5947ba56ff6fd1466e0aef365420271419c2124a03`) states
`ForcesConvexNGon 301 8` from the same proof term. It MUST fail with a type mismatch (compiled without `-o`).

## 5. Units and memory (HEURISTIC estimates marked)

- Units `esr-vfy-lcb3-<job>` (memguard track vfy, 20,000 MB), CPUQuota 100 %, MemorySwapMax 0, nice 10, one at a time,
  through `tools/unit_lean.sh` (anon+shmem sampler, SIGTERM at 80 % of MemoryMax).
- `ES302Final`: MemoryMax 12G (stop at 9,830 MB), RuntimeMaxSec 10800. HEURISTIC: anon+shmem 1-3 GB (FV304's Root and
  Final over 8,192 contexts used 429/451 MB; FV302 sub-roots 615-742 MB); wall 30-90 min (the axiom walks cover both
  trees' proof DAGs).
- `Bad302` control: MemoryMax 12G, RuntimeMaxSec 10800 (it imports the same closure).
- Import audit `audit3` (copy of `tools/audit2.py` with the two new roots and pins: FV302 olean sha256 recorded at
  FV302 acceptance, RS3520 oleans from `audit-3520.json`): MemoryMax 2G, O_DIRECT hashing.

## 6. Acceptance (all must hold)

1. `ES302Final` lean_rc 0; the three guards pass; the four `example`s elaborate; the `#check` lines equal §2.
2. `Bad302` fails with a type mismatch at `bad301` (and with nothing else).
3. `audit3` reports `"problems": []` (every closure module from exactly one root, every file hash equal to its pin).
4. The label then reads: **ES(8) ≤ 302, Lean-checked modulo the cake_lpr verdict propositions H-N66C (105), H-N66R
   (629) and H-ROWS (2,025), trust items E1-E6 (E3 tested, not proved)**. Stated in REMAINS.md and the records only
   after the advisor consult. Known limits to state with it: the 105 N66 cube proofs were deleted on 24 Nov (two
   recorded acceptances; a re-run needs a re-solve); no external review.
