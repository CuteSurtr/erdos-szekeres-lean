# DESIGN (M0): encoder B for the sevenfold octagon case in Lean, modulo the cake_lpr verdict

Item `sevenfold-encoder`, 22 Nov 2026. Pattern: ENCBLEAN (sixfold, m = 6) — read its `DESIGN.md` §1.4 for trust items
E1-E6, which are reused here with the instance (7,8,10) in place of (6,8,11) and one monolithic CNF in place of 64
cubes.

## 1. Target theorem and trust base

```lean
-- src/Geo7/Main7.lean (Mathlib side)
theorem EncB.Geo7.sevenfold_es8_of_text
    (h : ∀ nv G, EncB.parseDimacs (EncB.cnfText (EncB.encode 7 8 10) []) = some (nv, G) → ¬ EncB.DimacsSatisfiable G)
    (S : Finset Point) (c : Point) (hgp : GeneralPosition S)
    (hinv : Invariant (rotAbout c (2 * Real.pi / 7)) S) (hcard : 65 ≤ S.card) : HasConvexNGon 8 S
```

- Proof chain: `sevenfold_octagon` (LAYERLEAN, vendored in ENCBLEAN `geo/ES8Geo/Capstone2.lean:1144`) applied to
  `sevenfold70_of_no_modelO (no_modelO_7810_of_text h)` (with `geo7Bridge` inside); `no_modelO_7810_of_text` is M3-odd
  (`encB_satisfiable_7810`) composed with the round trip `parseDimacs_base7810` (M9, ENCBLEAN's
  `parseDimacs_cnfText`).
- **Reached** (22 Nov 06:31): `Geo7Bridge` is proved (`geo7Bridge`), so the only hypothesis is `h`, which
  `text7810_iff` shows equivalent to `¬ DimacsSatisfiable (encB 7 8 10)`.
- Trust items (ENCBLEAN DESIGN §1.4, instantiated):
  - **E1** the text `cnfText (encode 7 8 10) []`, printed by `encb_dimacs twin-base 7 8 10` (exe `3d43fa8b…`), has
    SHA-256 `b4d29017…` = the certified file (`logs/hash7810.log`, 22 Nov, which also checks the CNF hash, proof
    hash and verdict of the record `C6C7REVIEW/replay.json` B7 and the single `s VERIFIED UNSAT` line of both cake
    logs; also ENCBLEAN `m9_review_fix_hash_binding.log:97`, 6 Nov).
  - **E2** cake_lpr printed `s VERIFIED UNSAT` on (`b4d29017…`, proof `75f9bd35…`): `C7UPPER/logs/cake_B.out`,
    `C6C7REVIEW/logs/cake_B7.log` (cake_lpr `2fee767a…`). The proof was produced by CaDiCaL 3.0.1 (not the 2.1.3 of
    es-research §2), and neither CNF nor proof is on this machine: a fresh hash-bound re-solve (ENCBLEAN
    `scripts/resolve.sh` pattern; CaDiCaL ~800 s, proof 1.6 GB, cake_lpr ~8.4 GB RSS at heap 8000) needs a unit
    above this slot's 3.5 GB cap and the owner's OK.
  - **E3** cake_lpr reads the text as `parseDimacs` does and its verdict means `¬ DimacsSatisfiable`.
  - **E4** the compiled exe prints the kernel term (Lean compiler/runtime).
  - **E5** kernel, Mathlib `f897ebcf`, and the definitions (`Point`, `GeneralPosition`, `HasConvexNGon`, `orient`,
    `rotAbout`, `Invariant`, `Sevenfold70`) — vendored in ENCBLEAN `geo/`, byte-pinned there.
  - **E6** SHA-256.

## 2. Clause families of encoder B for odd m and their soundness obligations

gen_b2.py (= `EncB.gen` = `EncB.encB`, ENCBLEAN M1/M2) at odd m. All families except the angular one are identical
to the even case; the odd angular family has H premises and half-sector cells.

| family | gen_b2.py | obligation (under the intended assignment) | discharged by |
|---|---|---|---|
| ψ-order transitivity | 79-81 | `psiLt` is a strict order | `transCl_soundO` (copy of ENCBLEAN proof) |
| angular, odd: patterns (ranks × H bits), unit or conditional | 83-141 | a pattern whose Y premises match ψ and H premises match `hb` gives a true literal | `angCl_soundO` + `patternSpecO` |
| — key step | 104-119 | the encoder's odd objects `J = (2k+h) mod 2m`, `(J+m) mod 2m` equal ENCBLEAN's even objects at `2m` of the lifted labels `(i, 2k + hbit i)` | `RulesO.objsOdd_eq`; then ENCBLEAN `Rules.sortSix`, `wordSpec` at `2m` (unchanged) |
| nesting units | 143-150 | `chi (i,0) (i,1) (j,k)` | `nestLits_soundO` |
| chains (base, extension, closing) | 154-190 | no 7-chain about any pivot | `chainCl_soundO` |

`ModelO m K t` (src/EncBO/ModelO.lean) = ENCBLEAN's `Model` fields + `hb : ℕ → Bool` (`hb i` ⇔ θ_i < π/m),
`hb_zero`, and the two angular rules restated **at `2m` on lifted labels**:
`ruleA : … AltCCW (2*m) psiLt (liftO hb a) (liftO hb b) (liftO hb d) → chi a b d = true` (ruleB likewise).
`ψ` here is the phase modulo `π/m` (P1 Def. k8s:def:phase, u = π/m for odd m).

## 3. Lemma map (as built, Std-only)

- `ModelO.lean`: `ModelO`, `tauOfO`, `holds_yO/hO/orbO/fO`, `chi_perm3O`, `chi_rotByO`, `olitSpecO`, lift facts.
- `SoundO.lean`: `transCl_soundO`, `nestLits_soundO`, `Chain.base_soundO`, `Chain.ext_soundO`, `chainCl_soundO`.
- `RulesO.lean`: `objsOdd`, `patternLit_odd_fst`, `objsOdd_eq`, `getD_liftO`, `patternSpecO`.
- `AngO.lean`: `hOf`, `hPremOf`, `mem_angOuts_odd(')`, `mem_bitTuples`, `hbits_of_prem`, `exists_hbits`,
  `rkMono_of_premO`, `exists_rkMonoO`, `angCl_soundO`.
- `SatisfiableO.lean`: `genCoded_soundO`, **`encB_satisfiable_odd`**, `encB_satisfiable_7810`.
- `Compose7.lean`: `parseDimacs_base7810`, `encB7810_unsat_of_text`, **`no_modelO_7810_of_text`**, `_of_bytes`,
  `text7810_iff`.

No declaration that mentions `7 8 10` contains a tactic (they are terms); the numerals are in `seven_odd`.

## 4. The geometric half for odd m: `Geo7Bridge` (as built, all proved)

`Geo7Bridge : ∀ T c, GeneralPosition T → c ∉ T → Invariant (rotAbout c (2π/7)) T → T.card = 70 →
¬ HasConvexNGon 8 T → Nonempty (ModelO 7 8 10)` — **proved** (`Geo7.geo7Bridge`, from
`modelO_of_counterexample` at m = 7, K = 8, t = 10; that theorem holds for every m ≥ 3, 4 ≤ K ≤ 2m).

Why ENCBLEAN's M5/M6 do not apply: they need `Even m` (a) for `ψ_inj` (`phase_ne_of_distinct_layers`) and (b) in
ArcBridge (`antipode_even`). For odd m a counterexample need not be generic (P1 Lemma generic(b)).

| step | as built | file |
|---|---|---|
| G-A layer data | `LayerLab` = `PolarLabelling` minus `ψ_pos`, `ψ_inj`; `layerLab_of_counterexample` = ENCBLEAN M5 minus the even steps (uses `Lab.exists_layer_polar`, `dist2_le_of_later`) | Geo7/LayerLab.lean |
| G-B chi fields | `lab_P_rot`, `lab_P_injOn`, `lab_orient_ne_zero`, `lab_chi_rot/cycle/swap`, `lab_nest`, `lab_noChain`: ModelBasic renamed (`tools/gen_layerbasic.py`) | Geo7/LayerBasic.lean |
| G-C perturbation | `Pη η (i,k) = polar c rᵢ ((φ + ψᵢ + k·2π/m) + i·η)`; `exists_perturbation`: η > 0 with (C1) `0 < orient(Pη…) ↔ 0 < orient(P…)` on all valid distinct triples, (C2) `θ'ᵢ − θ'ⱼ ≠ k·π/m` (i ≠ j), (C3) `θ'ᵢ < 2π/m` | Geo7/Perturb.lean |
| G-D rules at 2m | `PolarData` = `PolarLabelling` minus `T`, `mem_layer`; ArcBridge renamed (`tools/gen_arcdata.py`) gives `polar_ruleA/B` | Geo7/PolarData.lean, ArcData.lean |
| assembly | `hbP i = [θ'ᵢ < π/m]`, `psiP i = θ'ᵢ − hbitᵢ·π/m`, `polarDataP : PolarData (2m) t c`, `P_liftO : P'(liftO a) = Pη a`, `chi_of_perturbed`, `modelO_of_counterexample` | Geo7/ModelOfLab.lean |

Compared with P1's proof of Lemma generic(b), the perturbed set is never shown to be a counterexample with the same
layers (no convpos lemma, no second application of the layer lemma): `chi` is the original orientation table, and
only `psiLt`/`hb` come from the perturbation, linked to the original signs by (C1).

## 5. Risks

| # | risk | status |
|---|---|---|
| R1 | `ModelO` unsatisfiable by real configurations (then `Geo7Bridge` is unprovable; no unsoundness) | closed: `Geo7Bridge` is proved |
| R2 | ArcBridge secretly uses `mem_layer` | closed: the copy over `PolarData` (no `mem_layer`) compiles unchanged |
| R3 | E2 provenance: CaDiCaL 3.0.1, files not on Linux | stated; re-solve needs owner OK (memory) |
| R4 | olean provenance | closed: all 32 reused modules rebuilt here from verbatim sources, byte-identical to ENCBLEAN's oleans; the final build uses only Mathlib's prebuilt oleans (geo checkout `f897ebcf`) |
