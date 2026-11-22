# ae33-lean: radius 1 around AE33 in Lean, modulo the 203 cake_lpr verdicts (formalization wave, 22 Nov 2026)

Item `ae33-lean`, slot `lae` (units `esr-ag-lae-<job>`). Work directory, the only place this agent writes:
`/home/jay/research/data/formalize-20261122/ae33-lean`. Nothing in the git repository is edited; no git writes.

Source record: `archive/es7-2026-10-19/results/ROADMAP20261115/LOWERBOUND_RUN_1118_AE33R1.md` (REC; CERTIFIED + PROVED
soundness, 203/203 pairs), with `VERIFY_AE33R1.md`, `VERIFY_AE33R1_REBUILD.md`, `VERIFY_AE33R1_SOUNDNESS.md`. Encoder
`l2enc.cpp` (`171a3e7c…`, copy in `ref/`), data `/home/jay/research/data/roadmap-20261115/pm1115/l1118` (L18) and
`/home/jay/research/data/lower-20261121/ae33` (hash table `hashes_203.tsv`, copy in `ref/`).

## 1. Headline (22 Nov 2026, 19:15 KST)

**Both statements of REC §1 (and radius 0) compile in Lean 4.24.0 / Mathlib `f897ebcf` with axioms [propext,
Classical.choice, Quot.sound]. The 203 verdicts enter as one hypothesis, `TextsUnsat203`.** Statements, the
definitions in them and the axiom lines are pinned by `#guard_msgs` in `lean/AE33Geo/Audit.lean`.

```lean
AE33Geo.ae33_pair : TextsUnsat203 → ∀ (i : Fin 203) (P : Fin 31 → Point),
    Realizes (baseOf ↑i) P ∨ RealizesMirror (baseOf ↑i) P → ∀ (p q : Point),
    GeneralPosition (insert p (insert q (Finset.image P Finset.univ))) →
    (insert p (insert q (Finset.image P Finset.univ))).card = 33 →
    ConvexNGonThrough 7 (insert p (insert q (Finset.image P Finset.univ))) p ∨
      ConvexNGonThrough 7 (insert p (insert q (Finset.image P Finset.univ))) q
AE33Geo.ae33_radius1 : TextsUnsat203 → ∀ (S : Finset Point), GeneralPosition S → S.card = 33 →
    ∀ (u v : ℕ), u < 33 → v < 33 → u ≠ v → ∀ (φ : ℕ → Point), (∀ w < 33, w ≠ u → w ≠ v → φ w ∈ S) →
    (∀ (a b : ℕ), a < 33 → b < 33 → a ≠ u → a ≠ v → b ≠ u → b ≠ v → φ a = φ b → a = b) →
    OTEmb φ u v ∨ OTEmbMirror φ u v → HasConvexNGon 7 S
AE33Geo.ae33_radius0  -- the same for a 32-point subset of type AE33 − {w} (an instance of ae33_radius1)
```

- `TextsUnsat203 := ∀ i < 203, ∀ nv F, EncB.parseDimacs (cnfText i) = some (nv, F) → ¬ EncB.DimacsSatisfiable F`.
  `cnfText i = EncB.render (numVars (baseOf i)) (cnf (baseOf i))` is the exact string `ae33print cnf i` writes.
  `texts_iff_cnfs : TextsUnsat203 ↔ CnfsUnsat203` holds with no runtime hypothesis (ENCBLEAN's `parseDimacs_render`).
- `Realizes B P`: every orientation sign of `P` equals that of the integer base `B` (labelled order type);
  `RealizesMirror`: every sign reversed. `OTEmb φ u v`: φ preserves every orientation sign of AE33 on the 31 labels
  ≠ u, v; `OTEmbMirror`: reverses them. `ConvexNGonThrough 7 S x`: a 7-subset of S in convex position containing x.
  `hcard = 33` makes p, q new and distinct; `hinj` says the 31 images are 31 points (a "31-point subset").
- **Label: Lean-checked modulo `TextsUnsat203` (the 203 cake_lpr verdicts) and trust items E1–E6** (DESIGN.md §4).
  Unrefereed; no independent agent has re-run this work. No bound and no label of any record changes; REC's
  result stays CERTIFIED + PROVED soundness, and this adds a Lean check of the soundness side and of the statement.
- **In Lean, kernel-checked:** soundness of every l2enc clause family (R2X/R2Y, ACX/ACY, RAD, GPA/GPP/GPQ, OCTX/OCTY,
  JK) for every realization (`clauseOf_sound`, `cnf_sat`); the slot lemma by three Grassmann–Plücker steps (replaces
  ABSAT8's normal-cone argument); rotation and insertion of positive chains; the mirror case; transfer of the R2
  cone signs and of the AC/GP constants through the realization; the variable decoding; the split of all 528 pairs
  into the 203 and 325 that miss H; H's 35 orientation signs on the AE33 integers.
- **E1 (printed bytes = certified bytes), M9 PASS** (`logs/m9_hash_binding.summary.json`, 19:11): for all 203 pairs the
  SHA-256 of `ae33print cnf i` equals `hashes_203.tsv`, L18's `cert/certify.jsonl` and `summary.jsonl`; header
  `p cnf 961 <clauses>` equals the recorded count; L18's `cert/<name>.cake.out` and the worker's fresh
  `cake/<name>.cake.out` each contain exactly one line `s VERIFIED UNSAT` (the latter nothing else); LRAT hash chain
  certify.jsonl = hashes table. `ae33print pts` = `ae33.txt` (`cb6a5327…`). Controls: refused indices print nothing;
  the exe hashes group the pairs exactly as the recorded hashes do (the record has **194 distinct CNFs for 203 pairs**:
  9 pairs of pairs share a CNF, e.g. ae_d15_26/ae_d15_27, ae_d9_14/ae_d9_15). Exe `22e05743…` unchanged throughout.
- **Exe ↔ theorem freeze PASS** (`logs/freeze_check.log`): the current sources regenerate byte-identical IR C for
  the five linked modules; the exe is newer than every linked `.c`; manifest `logs/final_manifest.sha256`.
- **Direct E1+E2 spot check** (`logs/cake_spot.log`): cake_lpr `c14ff498…` (heap 600) on the exact text the exe
  prints, with L18's kept LRAT: exactly one line `s VERIFIED UNSAT` for 5/5 pairs (ae_d14_15, ae_d14_16, ae_d0_14,
  ae_d5_32 = largest proof, ae_d1_32 = smallest); 4/4 cross-pair negative controls give 0 verdict lines. The other
  198 verdicts rest on the recorded cake outputs (two runs, M9 re-greps them).

## 2. Trust items (as ENCBLEAN / n66enc; DESIGN.md §4)

| item | content | evidence here |
|---|---|---|
| E1 | the bytes the exe prints for pair i are the bytes cake_lpr certified | M9 PASS 203/203; freeze check; 5 direct cake_lpr runs |
| E2 | cake_lpr's verdicts | recorded outputs (L18 + worker fresh run, 203 each), re-grepped; 5/203 re-run here |
| E3 | cake_lpr's DIMACS reading = every `EncB.parseDimacs` parse is unsatisfiable | inherited from ENCBLEAN (evidence only) |
| E4 | compiler and runtime: the exe computes the kernel value `cnfText i` | my package has no `partial`/`opaque`/`implemented_by`/`extern` (static audit). **Core code that `gen` and `render` use does**: `Array.foldlM` and `Array.forIn'` are `@[implemented_by …Unsafe]`, `Array.replicate`/`push`/`set!` and `String.push` are `@[extern]` runtime primitives, `List.mergeSort` is replaced via `@[csimp]` (a proved equation), Int arithmetic is GMP, `Std.HashSet` hashing is the runtime's (the kept descriptors are pure set membership, independent of the hash). All of this is E4. |
| E5 | kernel, Mathlib, definitions | axiom lines; closure audit: 4,708 modules, 4,693 oleans equal the `library.json` pins, 5 ENCBLEAN oleans equal sevenfold's source rebuild |
| E6 | SHA-256 | standard |
| data | the Lean constant `ae33` is ae33.txt | `ae33print pts` SHA-256 = `cb6a5327…`; REC: ae33.txt = JSON × 10^17 (EXACT) |

<!-- STATUS -->
- 22 Nov 19:12 KST: **freeze check PASS** and final manifest (`logs/freeze_check.log`, `logs/final_manifest.sha256`).
- 22 Nov 19:11 KST: **M9 PASS** (summary v2). Summary v1 (19:10, kept as `.summary.v1.json`) said PASS=false only
  because it demanded 203 distinct hashes; the record itself has 194. All 203 rows MATCH in both.
- 22 Nov 18:46 KST: **M10 done** (`esr-ag-lae-m10`): clean rebuild of all modules into a fresh store, rc 0, the 11
  pre-existing oleans byte-identical (`rebuild_all.log`; cgroup peak 1.53 GB), with `Audit.lean` (`#guard_msgs` on
  2 statements, 7 definitions, 14 axiom lines); static token audit PASS with self-test (`audit_static.log`); mutation
  controls 7/7 killed in the soundness proofs, doc-only control survived (`mutants.log`); cake_lpr spot check 5/5
  (`cake_spot.log`). 18:50: closure audit PASS (`closure_audit.json`; a first run mis-read `<home>` in the pin roots,
  fixed, all 4,693 pinned hashes were equal in both runs).
- 22 Nov 18:33–18:39 KST: **M8 done**: `Pair.lean` (`core`, `core_mirror`, `pair_of_unsat`, `ae33_pair`) and
  `Radius1.lean` (`ae33_radius1`, `ae33_radius0`) compile, standard axioms (`logs/geo7.log`, `geo9.log`, `geo10.log`).
- 22 Nov 18:23–18:27 KST: **M2–M4 done**: `Slot.lean`, `Sem.lean`, `Sound.lean` compile (`logs/geo2/4/6.log`).
- 22 Nov 18:00–18:06 KST: **M1 done**: Std-only port compiled (`logs/build1.log`), pilot 3/3 MATCH (`logs/pilot1.log`),
  exe relinked with `clauseB` (`logs/link2.log`, `22e05743…`); M9 started.
- 22 Nov before 18:00 KST: M0 DESIGN.md. Started about 17:35.
<!-- /STATUS -->

## 3. Milestones

| M | content | state |
|---|---|---|
| M0 | DESIGN.md: target theorem, family inventory with soundness and sources, trust list, lemma map | **done** (§7 as built) |
| M1 | Std-only port of l2enc: descriptor generator `gen`, validity-checking `clauseOf`, `cnf B = filterMap`, exe | **done** |
| M2 | literal semantics, real assignment, R2/AC/RAD/GP soundness | **done** |
| M3 | `mem_cnf`, `parse_cnfText`, `texts_iff_cnfs` | **done** |
| M4 | slot lemma, OCT/JK, rotation/insertion, polygon, mirror | **done** |
| M8 | `ae33_pair`, `ae33_radius1`, `ae33_radius0` | **done** |
| M9 | hash binding | **done, PASS** (203/203) |
| M10 | audit file, clean rebuild, closure audit, static audit, mutants, cake_lpr spot check, freeze check | **done** |

What remains (not done here): an independent re-run by another agent or person; fresh cake_lpr on the other 198
pairs (about 1 CPU-h with the exe; E2 rests on the recorded outputs for them); E3 is ENCBLEAN's. Optional: remove the
unused simp arguments flagged by the linter (cosmetic).

## 4. Files

- `DESIGN.md` (M0 + §7 as built), `README.md`.
- `lean/AE33Enc/` (Std-only; `tools/build.sh`, `tools/link.sh`): `Basic`, `Clause`, `Gen`, `Data` (generated by
  `tools/gen_data.py`), `Main` (exe), `Bridge`.
- `lean/AE33Geo/` (Mathlib side; `tools/build_geo.sh`, `tools/geo_env.sh`): `Slot`, `Sem`, `Sound`, `Pair`, `Radius1`,
  `Audit` (pinned); `Audit0`, `ModList` are print helpers, not imported by anything.
- `tools/`: `gate.sh`, `pilot.sh`, `hash_binding.py` (M9), `cake_spot.sh`, `mutants.sh`, `rebuild_all.sh`,
  `closure_audit.py`, `audit.py`, `freeze_check.sh`, `m10.sh`, `gen_data.py`.
- `ref/` pinned inputs (`SHA256SUMS.ref`); `logs/` (all logs above; `m9_notes.txt` has the pause/resume history and a
  count correction).
- `build/`: oleans, IR, objects, exe `build/bin/ae33print` (regenerable from the sources in about 2 min).

## 5. Resume / re-check

```
D=/home/jay/research/data/formalize-20261122/ae33-lean
U="-p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 -p RuntimeMaxSec=7200 --nice=10 --working-directory=$D"
$D/tools/gate.sh && systemd-run --user --unit=esr-ag-lae-<job> $U /bin/bash tools/rebuild_all.sh   # Lean, 1.5 min
# exe: tools/build.sh && tools/link.sh; hash binding (47 min, resumable; delete logs/m9_hash_binding.tsv for a fresh
#   run): .../venv.disk/bin/python -I tools/hash_binding.py; spot check: tools/cake_spot.sh <i>...
```

## 6. Rules followed

- Lean only with `/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean` (bare, `-R`), read-only LEAN_PATH
  over existing olean stores (ENCBLEAN `.lake/build`, repo `.lake/build` and `.lake/packages`), outputs only under
  this directory; never `lake`, never lean-lsp `lean_build`.
- Every compile and run in an `esr-ag-lae-*` unit (CPUQuota 100 %, MemoryMax 3500M, MemorySwapMax 0, RuntimeMaxSec
  ≤ 7200, nice 10), one at a time, after `tools/gate.sh` (no YIELD, Tctl < 86 C, agent pool anon < 4,500 MB).
  Largest cgroup peak 1.80 GB (cake spot check). M9 was paused three times to free the slot (resumable).
- Labels per es-research §2. Gaps are hypotheses, never axioms. No git, no web, no installs.
