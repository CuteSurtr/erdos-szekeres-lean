# sevenfold-encoder (slot lenc7): the sevenfold octagon case in Lean, modulo the cake_lpr verdict

Work directory of the formalization wave of 22 Nov 2026 (item `sevenfold-encoder`). Nothing here is in git; nothing
in the repository was edited (read-only use of ENCBLEAN's sources, oleans and exe). Labels follow es-research §2.
Not refereed; no independent person or agent has re-run this yet.

## 1. Headline (22 Nov 2026, 06:40 KST)

**D2 (every 7-fold rotationally symmetric set of ≥ 65 points in general position has a convex octagon) is
Lean-checked modulo the cake_lpr verdict recorded in C6C7REVIEW (CNF `b4d29017…`, proof `75f9bd35…` made by
CaDiCaL 3.0.1, cake_lpr `2fee767a…`; `replay.json` entry B7 and `logs/cake_B7.log`) and ENCBLEAN's trust items
E1, E3–E6.** The Lean side is at the level of the sixfold case (ENCBLEAN `sixfold_es8_of_texts`); the **E2
provenance is weaker than for m = 6** (see the caveat below). Lean 4.24.0, Mathlib `f897ebcf`; every module built
here from verbatim sources against Mathlib only (45 modules, rc 0, no error or warning, final run `build_all`
06:41–06:43, `logs/build.log`); statements and axioms of the main theorems pinned by `#guard_msgs` (axioms
[propext, Classical.choice, Quot.sound]).

```
EncB.Geo7.sevenfold_es8_of_text
  (h : ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 7 8 10) []) = some (nv, G) → ¬EncB.DimacsSatisfiable G)
  (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
  (hinv : Invariant (rotAbout c (2 * Real.pi / 7)) S) (hcard : 65 ≤ S.card) : HasConvexNGon 8 S
EncB.Geo7.sevenfold_es8_order7_of_text : the same for invariance under rotAbout c (2π·j/7), 1 ≤ j ≤ 6
EncB.Geo7.sevenfold70_of_unsat (h : ¬EncB.DimacsSatisfiable (EncB.encB 7 8 10)) : Sevenfold70
EncB.Geo7.sevenfold_es8 : ¬DimacsSatisfiable (encB 7 8 10) → (the conclusion above)
EncB.text7810_iff : (the hypothesis h) ↔ ¬DimacsSatisfiable (encB 7 8 10)          -- h is not vacuous
```

- `h` is what cake_lpr's `s VERIFIED UNSAT` on the hash-bound file is taken to mean (E3). The file is the C7UPPER
  encoder-B CNF `cnfb/m7K8t10.cnf`. E1 was re-run today (`logs/hash7810.log`, PASS): the pinned exe copy
  `3d43fa8b…` prints `cnfText (encode 7 8 10) []` with SHA-256 `b4d29017…`, 67,820,434 bytes,
  `p cnf 80080 2748538`; this equals three hash records **and** the CNF hash of the verdict record
  (`C6C7REVIEW/replay.json` B7: proof `75f9bd35…` = `C7UPPER/logs/check_B_full.log`, verdict
  `replayed VERIFIED UNSAT`, `complete: true`), and both cake logs (`C6C7REVIEW/logs/cake_B7.log`,
  `C7UPPER/logs/cake_B.out`) have exactly one `s ` line, `s VERIFIED UNSAT`.
- **E2 caveat (weaker than m = 6).** The sixfold E2 is CaDiCaL 2.1.3 proofs, the pinned Linux cake_lpr
  `c14ff498…` and hash-bound `results.tsv` rows. Here: (1) the proof `75f9bd35…` was made by CaDiCaL **3.0.1**, so
  the CNF is not CERTIFIED in es-research §2's wording (which names CaDiCaL 2.1.3; cake_lpr is the trusted step
  either way); (2) the checker was the macOS binary `2fee767a…` (C6C7REVIEW, 3 Nov), whose build provenance was not
  checked here; `C7UPPER/logs/cake_B.out` carries no hashes. Neither the CNF nor the proof is on this Linux machine.
  A hash-bound Linux re-solve (CaDiCaL 2.1.3 + cake_lpr `c14ff498…`, ENCBLEAN `scripts/resolve.sh` pattern) needs
  about 8.4 GB for cake_lpr (heap 8000), above this slot's 3.5 GB cap: **owner decision**.
- What is new in Lean (relative to C7UPPER's written proof and ENCBLEAN, which covered even m only):
  1. **M3 for odd m** (Std-only): `encB_satisfiable_odd : m % 2 = 1 → 2 ≤ m → ModelO m K t → DimacsSatisfiable (encB m K t)`
     (P1's code-to-clause gap G1 for m = 7, H premises and half-sector cells included).
  2. **The geometric half for odd m**: `modelO_of_counterexample` (any m ≥ 3): layers without genericity, a
     perturbation lemma that **replaces P1 Lemma generic(b)** (only the phase order is read off the perturbed
     set; the orientation signs are the original ones), and rules A/B on the half-sector grid at 2m.
  3. The composition with `sevenfold_octagon` (LAYERLEAN/Capstone2) and an order-7 corollary.

## 2. Statement and model (short; DESIGN.md has the lemma map)

`ModelO m K t` = ENCBLEAN's `Model` fields + half-sector bits `hb` (`hb i` ⇔ θᵢ < π/m) + `hb_zero`, with rules
A/B stated at `2m` on lifted labels `liftO hb (i,k) = (i, 2k + hbitᵢ)`. Key identity (`RulesO.objsOdd_eq`): the
encoder's odd objects (`J = (2k+h) mod 2m`, antipode `(J+m) mod 2m`) are ENCBLEAN's even objects at `2m` of the
lifted labels, so ENCBLEAN's `sortSix` and `wordSpec` apply unchanged.

## 3. Method / provenance

- ENCBLEAN's 16 EncB modules and 16 geo modules (10 vendored repository modules + Capstone2, KeyOrder, Orbit,
  OrbitConsistency, Interface, Labelling) are verbatim copies (= repository files; `logs/*_vendor.sha256`); built
  here from source, all 32 oleans are **byte-identical** to ENCBLEAN's prebuilt ones (`logs/olean_compare.log`).
- `Geo7/ArcData.lean` and `Geo7/LayerBasic.lean` are mechanical renames of ENCBLEAN's ArcBridge and ModelBasic
  (`tools/gen_arcdata.py`, `tools/gen_layerbasic.py`; no proof text changed) over structures without `mem_layer`
  resp. without `ψ_pos`/`ψ_inj`. `EncBO/SoundO.lean` and parts of `ModelO`/`AngO` are copies of ENCBLEAN proofs with
  `Model` → `ModelO`.
- Static audit `tools/audit.py` (PASS, `logs/audit.log`; self-test with planted violations FAIL as expected,
  `logs/audit_selftest.log`): vendored hashes, no forbidden token (sorry, native_decide, axiom, set_option, …) in
  the 13 own files, the 13 declarations that mention the instance (`7 8 10`, `(m := 7)`, `Geo7Bridge`,
  `Sevenfold70`) are terms, every module's last build rc 0 with its source unchanged since. The audit is
  regex-based (a local abbreviation for the numerals would evade check 3; the elaboration times, 0.3–5 s per file,
  show that nothing evaluates `encB 7 8 10`).
- Mutation tests (`tools/mutants.sh`, `logs/mutants.log`): 7 of 7 mutants killed (rules at m instead of 2m,
  swapped H bit, no `hb_zero`, rule B without the outer-layer condition, shifted nesting, wrong H threshold in the
  geometry, uniform perturbation), 1 docstring-only control survived as expected. Some kills are at the
  arity/rewrite level, not the semantic step.

## 4. Milestones

| milestone | content | status |
|---|---|---|
| M0 | DESIGN.md | done |
| M1 | Lean definition byte-identical to the certified CNF | ENCBLEAN's `encB 7 8 10`; E1 re-run PASS |
| M2-M3 | `ModelO`, `encB_satisfiable_odd`, `encB_satisfiable_7810` | **done** |
| M4-M7 | `layerLab_of_counterexample`, `lab_*` fields, `exists_perturbation`, `polar_ruleA/B`, `modelO_of_counterexample` | **done** |
| M8 | `geo7Bridge`, `sevenfold70_of_unsat`, `sevenfold_es8(_of_text)`, `sevenfold_es8_order7_of_text` | **done** |
| M9 | `parseDimacs_base7810`, `no_modelO_7810_of_text(_bytes)`, `text7810_iff`, E1 hash run | **done** |

## 5. Files

| file | content |
|---|---|
| `src/EncB/*.lean`, `src/ErdosSzekeres/**`, `src/ES8Geo/*.lean` | verbatim ENCBLEAN sources (hashes in `logs/encb_vendor.sha256`, `logs/geo_vendor.sha256`) |
| `src/EncBO/ModelO.lean` | `hbit`, `liftO`, `ModelO`, `tauOfO`, literal semantics, `chi_perm3O`, `olitSpecO` |
| `src/EncBO/SoundO.lean` | transitivity, nesting, chain families under `ModelO` |
| `src/EncBO/RulesO.lean` | `objsOdd`, `objsOdd_eq`, `patternSpecO` |
| `src/EncBO/AngO.lean` | odd angular family: H premises, bit tuples, `angCl_soundO` |
| `src/EncBO/SatisfiableO.lean` | `encB_satisfiable_odd`, `encB_satisfiable_7810` |
| `src/EncBO/Compose7.lean` | M9 Lean side for (7,8,10) |
| `src/Geo7/PolarData.lean`, `ArcData.lean` | polar data without a point set; ArcBridge copy (`polar_ruleA/B`) |
| `src/Geo7/LayerLab.lean`, `LayerBasic.lean` | layer data without genericity; ModelBasic copy (`lab_*`) |
| `src/Geo7/Perturb.lean` | `exists_perturbation` (C1 signs, C2 genericity, C3 range) |
| `src/Geo7/ModelOfLab.lean` | `polarDataP`, `P_liftO`, `modelO_of_counterexample` |
| `src/Geo7/Main7.lean` | `geo7Bridge`, final theorems, pins |
| `tools/` | `env.sh`, `lc.sh`, `build_std.sh`, `build_self.sh`, `build_all.sh`, `gate.sh`, `run.sh`, `hash7810.sh`, `audit.py`, `mutant(s).sh`, generators |
| `logs/` | `build.log`, `hash7810.log`, `audit.log`, `audit_selftest.log`, `mutants.log`, `olean_compare.log`, manifests |

## 6. What remains

- **E2 on Linux** (owner decision, memory): re-solve the text with the pinned CaDiCaL 2.1.3 and check with the
  pinned cake_lpr, hash-bound (would also meet §2's CERTIFIED wording); E3 evidence for this text (cake_lpr's
  parse-and-print mode, ~4 GB).
- An independent re-run of `tools/build_all.sh` and review of the copies (DESIGN.md §3-4).
- A record in the repository (e.g. a `C7UPPER` section or a new record) and P1's rigor line for m = 7 — owner only.
- Out of scope: encoder A, the lower bound (64-point sets), affine symmetries (SYMLEAN).

## 7. Resume

```
cd /home/jay/research/data/formalize-20261122/sevenfold
tools/run.sh all  $PWD/tools/build_all.sh     # everything from source + audit, ~2 min, 0.6 GB cgroup peak
tools/run.sh hash $PWD/tools/hash7810.sh      # E1, ~13 s, 0.7 GB
tools/run.sh mut  $PWD/tools/mutants.sh       # mutation tests, ~75 s
```
