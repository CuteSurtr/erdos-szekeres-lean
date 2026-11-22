# VERIFY ae33-lean: statement-fidelity review (slot lrv3, 22 Nov 2026, 19:20-19:45 KST; final text 19:45)

**Verdict: all five theorems of the worker result are CONFIRMED on statement fidelity.** Each says exactly what REC §1
(or REC §2, for `cnf_sat`) states. The verdict hypothesis is bound to the certified files, the hypotheses can be met,
and the axioms are the standard ones. The label stays as the worker gave it:

> **Lean-checked modulo `TextsUnsat203` (the 203 cake_lpr verdicts) and trust items E1–E6.** Unrefereed.

- No record label changes: REC stays CERTIFIED + PROVED soundness. This review checks statements and binding only. I
  re-proved nothing; my rebuild re-ran the kernel on the worker's proofs.
- I wrote only under `review/`.

| key (worker result) | verdict | basis |
|---|---|---|
| `AE33Geo.ae33_pair` | **confirmed** | The statement is REC §1 Theorem (§1.1). RS1 restates it with every definition unfolded and RS4 for an explicit pair u < v meeting H; both compile. Binding §2; non-vacuous §3; axioms [propext, Classical.choice, Quot.sound] |
| `AE33Geo.ae33_radius1` | **confirmed** | The statement is REC §1 Corollary in contrapositive form (§1.2). RS2 unfolds it and RS5 gives the set form (T ⊆ S plus a bijection); both compile. Same binding, witness and axioms |
| `AE33Geo.ae33_radius0` | **confirmed** | The statement is REC's "Radius 0 follows" (§1.3). It is **not pinned** in `Audit.lean`; my `#check @` prints it. RS3 states it with each "≠ w" hypothesis once and compiles. Same binding, witness and axioms |
| `AE33Geo.cnf_sat` | **confirmed** | `Ctx B pt → DimacsSatisfiable (cnf B)` is REC §2's soundness claim. `Ctx` is implied by REC's premises (§1.4). No verdict hypothesis. `Ctx` can be met (§3). Standard axioms |
| `AE33.texts_iff_cnfs` | **confirmed** | `TextsUnsat203 ↔ CnfsUnsat203`, with both sides printed. It needs no hypothesis. Axioms [propext, Quot.sound], a subset of the three; the worker reported it as such |

## 0. What I did

**Read:**
- SKILL.md §1–§5 and LEAN_STATUS_20261122.md (it holds no ae33 entry; I used its ENCBLEAN-pattern definition of E1–E6);
- REC = `ROADMAP20261115/LOWERBOUND_RUN_1118_AE33R1.md` §1–§6, and VERIFY_AE33R1_SOUNDNESS §0, §1 and §5;
- the worker's README.md and DESIGN.md;
- every theorem-side Lean file: `AE33Enc/{Basic,Clause,Gen,Data,Bridge,Main}`, and `AE33Geo/{Sem,Pair,Radius1,Audit}` in full;
- `Slot`/`Sound`: the definitions and statements only, not the proofs;
- ENCBLEAN `EncB/Dimacs.lean` (semantics) and the definitions of `Render.lean` (`render`, `parseDimacs`, `parseDimacs_render`);
- the library's `ErdosSzekeres/Definitions.lean` and `orient`;
- the worker's tools: hash_binding, freeze_check, cake_spot, rebuild_all, mutants, gate, closure and static audit;
- L18's `run_e72.sh` and `certify_cnf.sh`, and the fresh run's `run_pairs.sh`.

**Own code, all in `review/`:**
- `tools/own_checks.py` reads only. It covers the data, the pair set and the binding chain over all 203 pairs, against
  five independent records.
- `src/Fidelity.lean` has no `open`, sets `autoImplicit false` and `pp.fullNames true`, and holds my restatements
  RS1–RS5.
- `tools/run_review.sh` is the one compile job.

**One unit:** `esr-ag-lrv3-fid`, run after the gate (YIELD absent, Tctl 83 °C, agent pool anon 1,504 MB).
- Settings: CPUQuota 100 %, MemoryMax 3500M, MemorySwapMax 0, RuntimeMaxSec 7200, nice 10.
- It ran 19:34:30–19:36:07: 1 min 36 s CPU, cgroup peak 1,537 MB. The largest `/usr/bin/time` maxrss was 4.2 GB, but that
  count includes the shared, mmapped Mathlib oleans, which are not charged to the unit.
- Steps:
  1. rebuild the ten theorem modules from a snapshot `review/src/` (hashes equal the worker's `final_manifest.sha256`)
     into my own olean store. The worker's `build/olean` was not on the path;
  2. compile `Fidelity.lean` against that store;
  3. compare the oleans;
  4. run the exe on three pairs and compare its output with L18's kept CNFs.
- I deleted my olean store afterwards: it was byte-identical to `build/olean`, and a second store with the same module
  names invites path mix-ups. The hashes are in `logs/run_review.log`.
- **Deviation from "ONE compile".** The single unit ran eleven `lean` invocations: the ten-module rebuild plus
  `Fidelity.lean`. It also ran the exe three times.
  - Why: importing an olean does not re-run the kernel. Without the rebuild, the axiom lines would only describe
    oleans the worker produced, not the sources I read.
  - Cost: one unit, 96 s of CPU, 1,537 MB cgroup peak.

## 1. Statements against the record

All statements below are the elaborated forms printed by my compile (`logs/fidelity.out`). They contain only
`ErdosSzekeres.{Point, orient, GeneralPosition, ConvexPosition, HasConvexNGon}`, `EncB.{parseDimacs, render,
DimacsSatisfiable}` and `AE33`/`AE33Geo` definitions.
- **Printed from the olean** by my compile: `TextsUnsat203`, `CnfsUnsat203`, `cnfText`, `cnf`, `clauseB`, `numVars`,
  `numVarsN`, `n2`, `baseOf`, `pairOfIdx`, `base`, `keepIdx`, `hept`, `iorient`, `Pt`, `Realizes`, `RealizesMirror`,
  `ConvexNGonThrough`, `OTEmb`, `OTEmbMirror`, `Ctx`, `Realizes31`, `PosChain`, the five `ErdosSzekeres` notions,
  `DimacsSatisfiable`, `DimacsSat`, `parseDimacs`, `render`.
- **Read in source only:** `gen`, `clauseOf` and the data constants `ae33` and `pairs203`. My rebuild compiled that
  source into byte-identical oleans.

- **No auto-bound binders.** None appears in the three end statements. `cnf_sat` binds `{B} {pt}` through
  `variable` (Sound.lean:63).
- **Nothing that changes elaboration.** A grep of all ten theorem files for `instance`, `notation`/`infix`,
  `macro(_rules)`, `syntax`, `attribute`, `local`, `scoped`, `set_option`, `include`, `export`, `elab`, `opaque`,
  `partial`, `implemented_by`, `extern`, `csimp`, `unsafe`, `axiom`, `sorry`, `native_decide` and `ofReduceBool` finds only:
  - `deriving Inhabited` (Desc) and `deriving Inhabited, BEq, Repr, DecidableEq` (Term);
  - one `variable {B : Array Pt} {pt : ℕ → Point}`;
  - `@[irreducible]` on the two data constants.

### 1.1 `ae33_pair` vs REC §1 Theorem

The REC Theorem:
> For each of the 203 pairs {u, v} that meet H, let B′ be any realization of the labelled order type of B (or of its
> mirror image), and let p, q be points with B′ ∪ {p, q} in general position. Then B′ ∪ {p, q} contains a convex 7-gon
> through p or q.

How each part matches:
- **The 203 pairs.** `i : Fin 203` indexes `pairs203`. Own check: `pairs203` (Data.lean) equals the (u, v) columns of
  `hashes_203.tsv` row by row (`90cbb85d…`). As a set it is exactly {u < v < 33 : u ∈ H or v ∈ H}, all 203 of them.
  `hept` = REC's H, in REC's ccw order.
  - RS4 removes the indexing. Its hypothesis is "u < v < 33 with u ∈ hept ∨ v ∈ hept", with `base u v` in place of
    `baseOf i`, and it follows from `ae33_pair` through `pairs_cover`.
- **B.** `baseOf i = base u v` = `ae33.getD` mapped over `keepIdx u v` = (range 33).filter(≠ u, ≠ v). This is AE33 − {u, v}
  in file order, labels 0..30, matching REC.
  - Own check: the 33 pairs of integers of `ae33` (Data.lean) equal `L18/e72/ae33.txt` (`cb6a5327…`, REC's file),
    point by point.
  - My rebuild compiled that source into an olean byte-identical to the worker's, so the theorem's constant is that
    source.
- **Labelled order type.** `Realizes B P`: ∀ i j k : Fin 31, 0 < orient(P i, P j, P k) ↔ 0 < iorient(B_i, B_j, B_k).
  - For distinct indices both sides are nonzero: B is in general position (own exact check of all 5,456 triples), and
    P is injective by `hcard`. So this is sign equality on every triple.
  - On repeated indices both sides are 0.
  - So it is exactly "P realizes B's labelled order type".
- **Mirror.** `RealizesMirror`: 0 < orient(P…) ↔ iorient(B…) < 0, which is sign(P) = −sign(B), the labelled order type of B
  reflected. This matches REC.
- **General position.** `GeneralPosition (insert p (insert q (image P)))` plus `card = 33`. REC's "B′ ∪ {p, q} in general
  position" is a 33-point configuration. A `Finset` drops duplicates, so `card = 33` is what makes p and q new and
  distinct. §3 shows it cannot be dropped, so it is part of the premise, not a weakening.
- **Conclusion.** `ConvexNGonThrough 7 S x` := ∃ t ⊆ S, t.card = 7 ∧ ConvexPosition t ∧ x ∈ t. That is a convex 7-gon of
  S, not necessarily empty (the ES convention, VERIFY_AE33R1_SOUNDNESS §1), through x, for x = p or x = q. This matches REC.
- **RS1 restates the whole theorem** with `Realizes`, `RealizesMirror` and `ConvexNGonThrough` unfolded by hand. Its
  proof is `fun … => AE33Geo.ae33_pair …`, pure definitional unfolding, and it compiles.

### 1.2 `ae33_radius1` vs REC §1 Corollary

The REC Corollary:
> No 33-point set in general position without a convex 7-gon contains a 31-point subset with the order type (or mirror
> order type) of any 31-point subset of AE33.

The Lean statement is the contrapositive, for all S with `GeneralPosition S` and `S.card = 33`, all labels
u ≠ v < 33, and all maps φ with three properties:
- the 31 labels ≠ u, v map into S (`hS`);
- φ is injective on them (`hinj`), so they are a 31-point subset;
- φ preserves (`OTEmb`) or reverses (`OTEmbMirror`) every orientation sign of AE33 on those labels.

Under these, `HasConvexNGon 7 S` holds.
- **φ is an order-type isomorphism.** Positivity-iff is sign equality here: S and AE33 are in general position, and φ
  is injective.
- **φ is arbitrary,** so this is "∃ a labelling" = "has the order type". "Any 31-point subset of AE33" = AE33 − {u, v};
  AE33 has 33 distinct points (own check).
- **RS2** unfolds `OTEmb` and `HasConvexNGon`; pure defeq, compiles.
- **RS5** is the set form, written independently of the worker's labelling device. A subset T ⊆ S and an `Equiv` σ
  from the labels {w < 33, w ≠ u, v} onto T preserve or reverse all signs, so S has a convex 7-gon. It compiles and
  follows from `ae33_radius1`.
- **`hinj` is no restriction.** It follows from `OTEmb` together with general position of S and of AE33: if
  φ a = φ b with a ≠ b, the real orientation is 0, which forces iorient(a, b, c) = 0. It is the record's "31-point
  subset".

### 1.3 `ae33_radius0` vs REC

REC: "Radius 0 follows. A 32-point subset with the order type of AE33 − w contains a 31-point subset with the order
type of AE33 − {w, t}."

Lean: S with general position and `S.card = 33`, φ injective on the 32 labels ≠ w, those labels mapped into S, and
`OTEmb φ w w ∨ OTEmbMirror φ w w`. Then `HasConvexNGon 7 S`.
- `OTEmb φ w w` lists each "≠ w" hypothesis twice. That is harmless: RS3 states the natural form (each once) and derives it.
- This statement was not pinned in `Audit.lean`, and the worker's JSON paraphrases it. The form above is the one my
  compile printed.

### 1.4 `cnf_sat` (REC §2) and `texts_iff_cnfs`

**`cnf_sat`** is `∀ {B pt}, Ctx B pt → EncB.DimacsSatisfiable (cnf B)`. `Ctx` has four fields:
- `B.size = 31`;
- `Realizes31` (positivity-iff on indices < 31);
- nonzero orientation for distinct indices < 33;
- `no7`: no list of seven indices < 33 forms a positive chain (`PosChain`: all increasing triples positive) through
  31 or 32.

REC §2's premises imply `Ctx`. A positive 7-chain is seven distinct points in convex position
(`posChain_card_convex`), so "no convex 7-gon through p or q" gives `no7`. The conclusion is the existence of a model,
which is all that UNSAT ⇒ Theorem needs.

**`texts_iff_cnfs`**: `TextsUnsat203 ↔ CnfsUnsat203` with
- `TextsUnsat203 := ∀ i < 203, ∀ nv F, EncB.parseDimacs (cnfText i) = some (nv, F) → ¬ DimacsSatisfiable F`;
- `CnfsUnsat203 := ∀ i < 203, ¬ DimacsSatisfiable (cnf (baseOf i))`;
- `cnfText i = EncB.render (numVars (baseOf i)) (cnf (baseOf i))`.

`parse_cnfText` (printed) shows that the parse always exists, so the text hypothesis has content.

## 2. Binding of `TextsUnsat203` to the files cake_lpr certified

**The exe.** `build/bin/ae33print`, SHA-256 `22e05743…`.
- The journal shows it was linked by unit `esr-ag-lae-build2` (18:06:08–18:06:18) from `build/obj`. Those objects were
  compiled in the same unit from:
  - `build/ir/AE33Enc/{Basic,Clause,Gen,Data,Main}.c`, emitted by `lean -c` together with the oleans;
  - ENCBLEAN's `.lake/build/ir/EncB/{Gen,Dimacs,Coded,Cover,Render}.c`.
- The exe's mtime is 18:06:18. The first M9 unit (`esr-ag-lae-m9`) started at 18:07:30, and no later unit ran
  `build.sh` or `link.sh` (journal of all `esr-ag-lae-*` units).
- The hash is the same in `link2.log`, at the start and end of M9's last segment, in `freeze_check.log`, in
  `final_manifest.sha256`, and at the start and end of my unit.
- So all four M9 segments used this exe. That closes the gap that M9 logged the exe hash only around its last
  segment.

**Frozen?**
- **Not by permissions:** the file is writable.
- **By hash and sources:** yes.
  - `sha256sum -c logs/final_manifest.sha256` passes for all 44 entries except `DESIGN.md`. That file was edited at
    19:13, after the 19:12 manifest; it is documentation only.
  - The worker's freeze check regenerated the IR of the five linked modules from the current sources, byte-identical
    to `build/ir`. All linked `.c` files are older than the exe.
  - My rebuild from the same sources gives oleans byte-identical to the worker's for all ten theorem modules. So the
    theorem's `cnfText`, `cnf` and `gen` come from the source files that produced the exe's IR.
  - I did not re-link the exe or regenerate the IR myself.

**Bytes.** Three independent lines of evidence:
- **M9 (worker):** 203/203 pairs where SHA-256(exe output) = `hashes_203.tsv` = L18 `certify.jsonl` = L18 `summary.jsonl`,
  with header `p cnf 961 <clauses>` equal to the recorded count. The exe groups the pairs into 194 distinct CNFs
  exactly as the record does (9 pairs of pairs share bytes, e.g. ae_d14_26/27).
- **Own chain (`own_checks.py`, all 203 rows, 0 bad).** Every link was checked:
  - M9 TSV = the table;
  - table = `certify.jsonl` (one entry per name, verdict field) = `summary.jsonl` (clauses, verdict_lines 1);
  - table = the fresh run's `results.jsonl` `cnf_sha256_regen`. Per `run_pairs.sh`, that is the hash of the very
    file the fresh cake_lpr read; `cnf_all4_equal` and `lrat_equal` are true;
  - `.lrat.zst` on disk = table.
- **Own byte comparison (my unit):** `cmp` of `ae33print cnf i` against `zstd -dc` of L18's kept `cnf/<name>.cnf.zst`.
  Identical for i = 109 (ae_d14_26), 110 (ae_d14_27; same bytes as 109, the duplicate group) and 202 (ae_d31_32).

**Verdicts.**
- L18 `cert/<name>.cake.out` has exactly one line `s VERIFIED UNSAT` for all 203.
- The fresh run's `cake/<name>.cake.out` is exactly that one line for all 203 (own check).
- L18's `certify_cnf.sh` hashes the same path it passes to cake_lpr. The worker's `cake_spot.log` adds cake_lpr
  accepting the exact exe output for 5 pairs, with 4 cross-pair controls rejected.

**Remaining trust:**
- E2: cake_lpr;
- E3: cake_lpr's DIMACS reading = `EncB.parseDimacs`. Inherited from ENCBLEAN; the same renderer is used here;
- E4: compiler and runtime. This includes `Std.HashSet` hashing, `@[csimp]` mergeSort and core's `implemented_by`.
  It also includes **ENCBLEAN's IR `.c` files against its oleans**: nobody checked those here. The worker compared
  ENCBLEAN oleans only, with sevenfold's rebuild. Inherited;
- E6: SHA-256.

## 3. Non-vacuity

- **`ae33_pair`.** The witness for every i is AE33 itself: P = the 31 points of B (integers cast to ℝ), p = AE33_u,
  q = AE33_v.
  - `Realizes` holds, because `orient` of the cast is the cast of `iorient`.
  - General position and card 33 hold (own exact check: 33 distinct points, no collinear triple).
  - The conclusion holds through H (REC §4).
- **`ae33_radius1` and `ae33_radius0`.** S = AE33 cast to ℝ, φ = the cast labelling. All hypotheses hold for every
  u ≠ v (resp. w).
- **`cnf_sat`.** `Ctx` holds for B = AE33 − {u, v} with u, v ∉ H, pt = file order, then u, then v.
  - H is AE33's only convex 7-gon: REC, and VERIFY_AE33R1_SOUNDNESS §3.4, deduced from convex7 = 0 in the 203 bases.
  - H avoids p and q, so no positive 7-chain passes through 31 or 32.
- **`TextsUnsat203`** is not vacuously true: the parse exists (`parse_cnfText`). It is supported by the verdicts
  through E1–E3 (§2).
- **`hcard` is necessary.** Without it, take P = B cast and p = q = P 0. Then S = B′ has 31 points in general position,
  and the conclusion would ask for a convex 7-gon in B′. But every base has convex7 = 0 (encoder stats; REC §4's own
  counts, 203/203), and convex position is an order-type property. So that statement would be false.
- **`hinj`** follows from the other hypotheses (§1.2).

## 4. Axioms (my compile, own olean store)

Lines from `logs/fidelity.out` and from my rebuild logs (`logs/build_*.log`):
- `ae33_pair`, `ae33_radius1`, `ae33_radius0`, `cnf_sat`, `clauseOf_sound`, `pair_of_unsat`: **[propext,
  Classical.choice, Quot.sound]**;
- `texts_iff_cnfs`, `parse_cnfText`, `pairs_cover`, `mem_of_any`: [propext, Quot.sound];
- `pairOfIdx_of_mem`: [propext];
- my RS1–RS5: [propext, Classical.choice, Quot.sound].

Every module compiled with rc 0. By `grep -c` on the build logs, all 21 warnings are "This simp argument is unused"
linter lines: 19 in Sem.lean and 2 in Sound.lean. `Fidelity.lean` emitted no warning. No `sorry`.

My oleans equal the worker's `build/olean` byte for byte for all ten modules: Basic `9940a5c5…`, Clause `a88ea673…`,
Gen `ad866846…`, Data `46e0d161…`, Bridge `d1795b4b…`, Slot `aebdfe94…`, Sem `c19528c7…`, Sound `a756fe58…`, Pair
`f28d7fc0…`, Radius1 `1438d902…`.

Imported stores, read only:
- Mathlib and the repo library as on `geo_env.sh`. The worker's closure audit found 4,693 oleans equal to their pins;
  I did not re-run it;
- ENCBLEAN `.lake/build`.

## 5. Findings that do not change a verdict

1. **`ae33_radius0` is not pinned** by `#guard_msgs` in `Audit.lean` (only `ae33_pair` and `ae33_radius1` are). Add it.
2. **The static audit's token list** (`tools/audit.py`) lacks `instance`, `notation`/`infix`, `attribute`, `local`,
   `scoped`, `variable`, `macro_rules`, `syntax`, `include`. My grep found none of concern (§1), but the audit should
   list them.
3. **`autoImplicit`** is on: bare `lean` uses core's defaults, and `set_option` is banned by the worker's audit.
   Nothing slipped through (§1), but a stray identifier in a future statement would become a silent binder. A
   `#check @` pin catches that.
4. **M9 logged the exe hash** only around its last segment. The journal and the mtime close the gap (§2); a
   per-segment log line would be cleaner.
5. **E4 inherits ENCBLEAN's IR files unchecked** against ENCBLEAN's oleans (§2).

## 6. Not checked

- I did not re-run cake_lpr (E2). I rely on the two recorded runs per pair and the worker's 5-pair spot check.
- I did not regenerate the IR, re-link the exe or run the full 203-pair hash binding myself: 3 byte comparisons only.
- I did not re-run the closure audit or the mutants.
- I did not read the proofs in Slot.lean and Sound.lean. They are kernel-checked, and fidelity does not depend on them.
- I did not independently check that H is AE33's only convex 7-gon; I rely on REC and VERIFY_AE33R1_SOUNDNESS §3.4. It
  matters only for `cnf_sat`'s non-vacuity witness.

## 7. Files (`review/`) and resume

- `VERIFY_ae33-lean_fidelity.md` (this file).
- `tools/own_checks.py` → `logs/own_checks.json` (PASS).
- `tools/run_review.sh` → `logs/run_review.log`, `logs/build_*.log`, `logs/fidelity.out`, `logs/time_v.txt`.
- `src/` holds the snapshot of the ten theorem files (`logs/src_snapshot.sha256`, equal to the worker's manifest) and
  `src/Fidelity.lean`.
- `SHA256SUMS` covers all of the above.

Resume, about 2 min:

```
D=/home/jay/research/data/formalize-20261122/ae33-lean
bash $D/tools/gate.sh && systemd-run --user --unit=esr-ag-lrv3-fid -p CPUQuota=100% -p MemoryMax=3500M \
  -p MemorySwapMax=0 -p RuntimeMaxSec=7200 --nice=10 --working-directory=$D/review \
  /bin/bash -c "/usr/bin/time -v -o logs/time_v.txt /bin/bash tools/run_review.sh > logs/run_review.log 2>&1"
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I $D/review/tools/own_checks.py
```
