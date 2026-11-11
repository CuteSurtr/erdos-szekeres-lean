# LEANLB20261111: the symmetric lower-bound sets for k = 8, Lean-checked

Lean 4 (v4.24.0), Mathlib `f897ebcf`, 11–12 November 2026 (KST). Not committed.

**Status.** Seven point sets of `ES8SYM`/`SIX60` are now Lean-checked (kernel evaluation with `decide +kernel`,
no `native_decide`, no `sorry`, no new axioms; every theorem below has axioms
`[propext, Classical.choice, Quot.sound]`, enforced at build time by `#guard_msgs` in `LeanLB/Audit.lean`):

| theorem (`LeanLB.`) | file (results/) | symmetry | n | before |
|---|---|---|---|---|
| `sixfold60` | `SIX60/sets/c6_60pts_D.pts` | rotation by 2π/6 | 60 | exact computation |
| `fourfold52` | `ES8SYM/sets/c4_52pts_13layers.pts` | rotation by 2π/4 | 52 | exact computation |
| `halfturn64` | `ES8SYM/sets/c2_64points_k8.txt` | rotation by π | 64 | exact computation |
| `mirror46` | `ES8SYM/sets/mirror_46points_k8.txt` | reflection in x = 0 | 46 | exact computation |
| `threefold61` | `ES8SYM/sets4/c3_61pts_centre.txt` | rotation by 2π/3 | 61 | exact computation |
| `sevenfold64` | `ES8SYM/sets/c7_64pts_small.pts` | rotation by 2π/7 | 64 | exact computation |
| `fivefold56` | `ES8SYM/sets3/c5_56pts_11layers_centre.pts` | rotation by 2π/5 | 56 | exact computation |

So the lower bounds of the 6-fold value **60** (P1), the 7-fold value **64** and the mirror value **46** are
Lean-checked, and so are the lower bounds 64, 61, 56 and 52 of the half-turn, 3-, 5- and 4-fold rows of the `ES8SYM`
table. Each theorem is about the set defined from the rows of the repository's file, read as in `ES8SYM/README.md`
§2; `scripts/gen_data.py --check` regenerates the Lean data files from the set files byte for byte, and their
SHA-256 equal the repository's `SHA256SUMS` entries (`scripts/audit.sh`).

## 1. The statements

All seven have the same form; for the 6-fold set (`LeanLB/Main.lean`):

```lean
theorem LeanLB.sixfold60 :
    setC6N60.card = 60 ∧ GeneralPosition setC6N60 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 6)) setC6N60 ∧ ¬ HasConvexNGon 8 setC6N60
theorem LeanLB.exists_sixfold60 : ∃ S : Finset Point, S.card = 60 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 6)) S ∧ ¬ HasConvexNGon 8 S
```

The others: `fourfold52` (`card = 52`, `rotAbout 0 (2 * Real.pi / 4)`), `halfturn64` (`64`, `2 * Real.pi / 2`),
`mirror46` (`46`, `Invariant (lineRefl 1 0 0)`), `threefold61` (`61`, `2 * Real.pi / 3`), `sevenfold64` (`64`,
`2 * Real.pi / 7`), `fivefold56` (`56`, `2 * Real.pi / 5`), each with `¬ HasConvexNGon 8` and an `exists_` form.

**What the words mean** (the trusted part; nothing else needs to be read to understand the statements):
- `Point`, `GeneralPosition`, `ConvexPosition`, `HasConvexNGon` are the repository's definitions
  (`ErdosSzekeres/Definitions.lean`, copied verbatim): `Point := Fin 2 → ℝ`; general position is "no three distinct
  points collinear" (Mathlib `Collinear`); `HasConvexNGon n s` is "some `t ⊆ s` with `t.card = n` is in convex
  position" (Mathlib `ConvexIndependent`). So `¬ HasConvexNGon 8 S` says that no 8 points of `S` are in convex
  position.
- `LeanLB/Statement.lean` (77 lines): `Invariant f S := ∀ p ∈ S, f p ∈ S` and `rotAbout c θ` (verbatim from
  `LAYERLEAN/LayerLemma.lean`; the same text is used by `ENCBLEAN/geo`'s upper bound `sixfold_es8`); `lineRefl`
  (body verbatim from `SYMLEAN/mirror/ReductionThreeClasses.lean`, used by `mirror_eight_line`; `lineRefl 1 0 0` is
  `(x, y) ↦ (-x, y)`); `unitRoot m j = (cos(2πj/m), sin(2πj/m))`; `cycPoint m w = Σ_{j<m} w_j • unitRoot m j`;
  `intPoint [x, y] = (x, y)`; and the seven sets, e.g.
  `setC6N60 := (c6N60Rows.map (cycPoint 6)).toFinset`, `setC2N64 := (c2N64Rows.map intPoint).toFinset`.
- `LeanLB/Data/*.lean`: the `…Rows` lists are the rows of the files, verbatim (generated; checked as above).
  A `.pts` row `w_0 … w_{m-1}` is `Σ_j w_j ζ^j`, `ζ = e^{2πi/m}` (`cycPoint m`); a row `a b` of
  `c3_61pts_centre.txt` is `a + bω`, `ω = e^{2πi/3}` (`cycPoint 3 [a, b]`); a row `x y` of the other `.txt` files
  is `(x, y)` (`intPoint`). Every row has exactly `m` (or 2) entries (`LeanLB/Check/Rows.lean`).

Everything else in the data files (checker coordinates, approximations, translations) and every other module is
checked, not trusted.

## 2. How the proof goes

**The checker** (`LeanLB/Checker.lean`, 102 lines; generic copy `LeanLB/G/Checker.lean`). Points are pairs of
natural numbers. For each anchor `p`: keep the points above `p` in the order (y, x); sort them counterclockwise
around `p` by insertion; check that the sorted list is pairwise counterclockwise around `p`; then a dynamic
programme over the sorted list computes, for every pair `(x, y)`, the length of the longest chain `…, x, y` (in list
order) whose consecutive triples turn left, and fails if a value exceeds `B = 6`. Kernel evaluation uses only `Nat`
primitives (`Nat.mul`, `Nat.add`, `Nat.blt`, `Nat.ble`, `Nat.beq`, GMP-accelerated in the kernel), `Bool` and
structural recursion on lists. A general-position check tests all `C(n,3)` triples.

**Soundness** (`LeanLB/CheckerSound.lean`, `LeanLB/Bridge.lean`):
- `card_le_of_check`: if `checkAll B L = true`, every `U ⊆ L` satisfying the four-point condition `ConvexSigns`
  (if `b` lies counterclockwise between `a` and `c` around `p`, then `a, b, c` turn left) has at most `B + 1`
  points. Proof: take the lowest point `p` of `U`; the other points of `U`, in the anchor list's order, form a chain
  with left turns (by `ConvexSigns` and pairwise sortedness), so the programme's invariant bounds its length by `B`.
- `convexSigns_of_convexPosition`: a set in convex position satisfies `ConvexSigns` (otherwise `b` would lie in the
  triangle `p a c`; repository lemma `Suk.mem_triangle_iff_orient_products`).
- `lowerBound_of_check`: for any map `φ` from lattice points to the plane that multiplies every orientation
  determinant by one positive constant, `gpOK L` and `checkAll 6 L` give `card = L.length`, `GeneralPosition` and
  `¬ HasConvexNGon 8` for the image of `L`.

**The five lattice sets.** The rows are mapped to integer lattice coordinates (`LeanLB/Geometry.lean`): `Σ w_j i^j
= (w₀ − w₂) + (w₁ − w₃)i`; for `ζ = e^{iπ/3}`, `Σ w_j ζ^j = a + bζ` with `a = w₀ − w₂ − w₃ + w₅`,
`b = w₁ + w₂ − w₄ − w₅`; for `ω`, `a + bω`. The plane point is `embedZ A B (a, b) = a·A + b·B` with `A = (1, 0)`
and `B = (0, 1)`, `(1/2, √3/2)` or `(−1/2, √3/2)`, which scales orientations by `√3/2` or `1` (`embed_scaling`;
`cycPoint_four/six/three`, proved from the values of cos and sin at multiples of 2π/m). The symmetry is an integer
map on rows (cyclic shift, `(a, b) ↦ (−b, a − b)`, `(x, y) ↦ (−x, −y)` or `(−x, y)`), and the rotation acts on
`embedZ` accordingly (`rot_four`, `rot_six`, `rot_three`, `rot_two`, `refl_x`). The kernel checks that the rows are
closed under the integer map, that the checker's list is the translated lattice image of the rows, `gpOK` and
`checkAll 6` (`LeanLB/Check/*.lean`).

**The 5- and 7-fold sets** (`LeanLB/G/`). Here `Σ w_j ζ^j = (X(t)/2, s·Y(t))` with `t = 2cos(2π/m)`,
`s = sin(2π/m)` and `X, Y ∈ ℤ[t]` of degree ≤ 2 (`lat5`, `lat7`, `cycPoint_five`, `cycPoint_seven`; Lean proves
`t₅ = (√5 − 1)/2` from Mathlib's `cos(π/5)`, and `t₇³ + t₇² − 2t₇ − 1 = 0` from `cos 4x = cos 3x` at `x = 2π/7`).
Rational bounds `lo/D < t < (lo + 1)/D` (`D = 2⁸⁰` resp. `2⁶⁴`; `t5_bounds` from `√5`, `t7_bounds` from the cubic
and its monotonicity on [1, 2]) certify, for each point, integer approximations `Ũ, Ṽ` of `2^K·X(t), 2^K·Y(t)`
within 1 (`apxOK`, `certOK`; `K = 40` resp. `24`). With all translated approximations at most `Mx`, an
approximate orientation above `8·Mx + 8` certifies a positive orientation (`opA_sound`), and the order by
`Ṽ + Ũ` with margin 4 certifies `Y(t) + X(t)` increasing (`abA_sound`). The same checker then runs on the
approximations (`G.lowerBound`; its hypotheses are required for the points of the list only). The rotation by
`2π/m` is the cyclic shift of the coefficients for every `m` (`rot_cycPoint`, `LeanLB/G/Cyclo.lean`). The kernel
checks the certificates, that the exact coordinates are `lat5`/`lat7` of the rows, closure under the shift, `gpOK`
(every triple decided in one of its two orders, every pair ordered) and `checkAll 6`. The margins were chosen by
an exact computation beforehand (smallest approximate orientation / `E`: 3891 for the 7-fold set at `K = 24`; about
6·10¹⁴ for the 5-fold set at `K = 40`); Lean only checks them.

**Kernel work.** The anchor loop is split into ranges of anchors (`checkFrom`), one `decide +kernel` each, so that
the kernel's cache stays small; `checkFrom_trans` and `checkAll_of_checkFrom` recombine them.

| set | orientation tests in the programme | ranges | kernel module build | peak RSS |
|---|---:|---:|---:|---:|
| `c6_60pts_D` (60) | 487,635 | 19 | 96 s | 6.0 GiB |
| `c4_52pts_13layers` (52) | 270,725 | 10 | 54 s | 4.6 GiB |
| `c2_64points_k8` (64) | 635,376 | 22 | 123 s | 6.7 GiB |
| `mirror_46points_k8` (46) | 163,185 | 6 | 32 s | 4.0 GiB |
| `c3_61pts_centre` (61) | 521,855 | 20 | 93 s | 5.9 GiB |
| `c7_64pts_small` (64) | 635,376 | 24 | 146 s | 7.3 GiB |
| `c5_56pts_11layers_centre` (56) | 367,290 | 12 | 86 s | 5.5 GiB |

(Tests = `C(n, 4)`, the number of orientation tests of the programme over all anchors; the module time includes
the `gpOK` check of all `C(n, 3)` triples and, for the 5- and 7-fold sets, the certificates. Times are wall clock of
the clean build of 11 November, one module at a time, 2 CPUs; peak RSS of that step.)

## 3. Axiom audit

From the clean build (`logs/build_final.log`; the same lines are enforced by `#guard_msgs` in `LeanLB/Audit.lean`,
which is part of the default target, for the seven theorems, their seven `exists_` forms, `lowerBound_of_check`,
`card_le_of_check` and `G.lowerBound`):

```
info: LeanLB/Audit.lean:41:0: 'LeanLB.sixfold60' depends on axioms: [propext, Classical.choice, Quot.sound]
info: LeanLB/Audit.lean:42:0: 'LeanLB.fourfold52' depends on axioms: [propext, Classical.choice, Quot.sound]
info: LeanLB/Audit.lean:43:0: 'LeanLB.halfturn64' depends on axioms: [propext, Classical.choice, Quot.sound]
info: LeanLB/Audit.lean:44:0: 'LeanLB.mirror46' depends on axioms: [propext, Classical.choice, Quot.sound]
info: LeanLB/Audit.lean:45:0: 'LeanLB.threefold61' depends on axioms: [propext, Classical.choice, Quot.sound]
info: LeanLB/Audit.lean:46:0: 'LeanLB.sevenfold64' depends on axioms: [propext, Classical.choice, Quot.sound]
info: LeanLB/Audit.lean:47:0: 'LeanLB.fivefold56' depends on axioms: [propext, Classical.choice, Quot.sound]
```

`scripts/audit.sh` (`logs/audit.log`, **AUDIT PASS**, 11 November 22:41 KST): the 11 vendored modules verify and
equal the repository files; the 7 data files regenerate byte for byte and their sources' SHA-256 equal the
repository's `SHA256SUMS`; no `sorry`, `admit`, `native_decide`, `axiom`, `opaque`, `implemented_by`, `extern`,
`unsafe`, `ofReduceBool`, `ofReduceNat`, `skipKernelTC` or `maxHeartbeats` in the 41 Lean files (comments
stripped), and no `set_option` other than `maxRecDepth`; the seven axiom lines above are in the build log.
All computation on the data is by `decide +kernel` (kernel reduction; it adds no axiom, unlike `native_decide`).

**Rejection tests** (`tests/Reject.lean`, `logs/reject.log`): the checker with `B = 5` on the mirror set (which has
convex 7-gons), `gpOK` with three collinear points added, and a certificate with one approximation moved by 2 are all
rejected (`Tactic decide proved that the proposition ... is false`, three errors, as expected).

## 4. Build

The package is separate from the repository's Lake package (whose `.lake` is not touched). `.lake/packages` is a
copy of `ENCBLEAN/geo/.lake/packages` (Mathlib `f897ebcf` with its prebuilt oleans, same toolchain; nothing was
downloaded or rebuilt). Lake 5.0 has no job limit and each kernel-check module needs 4–8 GB, so the build is
staged, one module group at a time, each step in a scope of 2 CPUs and 12 GB at nice 10:

```
cd cloud/es7-2026-10-19/results/LEANLB20261111
scripts/build_all.sh --clean      # removes .lake/build only; log logs/build_final.log
scripts/audit.sh                  # log logs/audit.log
lake env lean tests/Reject.lean   # three expected failures; log logs/reject.log
```

Do not run a bare `lake build` on a stale tree: Lake would start all seven kernel-check modules at once.

**Second reading, 11 November 2026, 22:43–22:54 KST.** The statements were read against `Definitions.lean` and the
set files, `scripts/audit.sh` passed, and a second clean build (`scripts/build_all.sh --clean`, now
`logs/build_final.log`, **642 s** wall) re-ran every kernel check with exit 0; a separate `#print axioms` of the
seven `exists_*` theorems, run outside the package's own audit file, printed `[propext, Classical.choice,
Quot.sound]` for each. Not an independent review.

**Clean build, 11 November 2026, 22:29–22:40 KST** (`scripts/build_all.sh --clean`, log kept as
`logs/build_final.first.log`): **685 s** wall in all; the seven kernel-check modules 631 s of it (table in §2); the vendored modules 13 s; every
other module under 5 s. Peak RSS of any step 7.3 GiB (the 7-fold module); never more than one Lean process at a
time. Mathlib was not rebuilt. The first builds of the same modules (`logs/build_checks.log`, 21:59–22:27 KST)
gave the same times within 15%.

## 5. Files

| path | content |
|---|---|
| `LeanLB/Statement.lean` | **trusted**: `Invariant`, `rotAbout`, `lineRefl`, `unitRoot`, `cycPoint`, `intPoint`, the seven sets |
| `LeanLB/Data/*.lean` | **trusted rows** (`…Rows`, verbatim, generated by `scripts/gen_data.py`); the other lists are checked |
| `ErdosSzekeres/*.lean`, `ErdosSzekeres/Suk/*.lean` | 11 repository modules, verbatim (`VENDOR.sha256`; equal to the files at commit `408c0885`); `Definitions.lean` is trusted, the rest are proofs |
| `LeanLB/Checker.lean`, `CheckerSound.lean`, `Bridge.lean` | the `Nat` checker, its soundness, the bridge to the repository's definitions |
| `LeanLB/Geometry.lean` | lattice coordinates of the 2-, 3-, 4-, 6-fold and mirror rows, symmetries |
| `LeanLB/G/Checker.lean`, `Sound.lean`, `Bridge.lean` | the checker with the orientation test as a parameter, its soundness and bridge |
| `LeanLB/G/Approx.lean`, `Cyclo.lean`, `Five.lean`, `Seven.lean` | certified approximations; rotation = cyclic shift; `t = 2cos(2π/5)`, `2cos(2π/7)` |
| `LeanLB/Check/*.lean` | the kernel evaluations (generated by `scripts/gen_checks.py`); `Rows.lean`: row lengths |
| `LeanLB/Main.lean` | the seven theorems and their existential forms |
| `LeanLB/Audit.lean` | `#guard_msgs` axiom audit (part of the default build) |
| `tests/Reject.lean` | rejection tests (not built): three `decide +kernel` that must fail |
| `scripts/gen_data.py`, `gen_checks.py` | generators (standard library only); `--check` compares with the files on disk |
| `scripts/build_all.sh`, `build_checks.sh`, `audit.sh` | staged build under the resource cap; audit |
| `SOURCES.sha256`, `VENDOR.sha256` | hashes of every source and configuration file |
| `logs/` | `build_final.log` (second clean build), `build_final.first.log` (first clean build), `audit.log`, `reject.log`, `build_checks.log` (first builds) |

Key files (SHA-256; all files in `SOURCES.sha256` and `VENDOR.sha256`):

| file | SHA-256 |
|---|---|
| `LeanLB/Statement.lean` (trusted) | `b99dedd1588346d5fc71cb2287ce78acce273cd84b476c254bd498cad8b3e9df` |
| `ErdosSzekeres/Definitions.lean` (trusted, verbatim) | `2425500eefd181ad4ebc30dc4cb1542a17bfb3605e5ee0d25bbbf4843406710e` |
| `LeanLB/Main.lean` | `6cfdf944496cdf0b4d12f223a7cf2941328d97f42f1f287f48270ec36827719d` |
| `LeanLB/Checker.lean` | `d5fdb977812bb81e88fecd6f139819fae3d498422e5690942220a0cd774e8f12` |
| `LeanLB/CheckerSound.lean` | `21ddfe5e18ec157ef5c4ab04e17368b80f910afdae23b02af8dee0050ef90575` |
| `LeanLB/Bridge.lean` | `06ab6a44e26c1308bb7cc61951604878a0a9d9328011248ab16e362dce887f4e` |
| `lakefile.toml` / `lake-manifest.json` | `f9966939…` / `cd4888c5…` |

Data sources (SHA-256 as in the repository's `SHA256SUMS`; re-checked by `scripts/audit.sh`):

| file | SHA-256 |
|---|---|
| `SIX60/sets/c6_60pts_D.pts` | `e2eaceb9e6483b461a72fc330a5d05b0ad6d7e238bfc557f5eed412d95d133c2` |
| `ES8SYM/sets/c4_52pts_13layers.pts` | `dc4cf91396f8efe5e03b54ef8a4ff5d569385fcec7b9f5a016f72431c980c65b` |
| `ES8SYM/sets/c2_64points_k8.txt` | `25576cf253fb969b01777c2e8945dfbdecfef10fad8b8c15a3eb70b1c4a8811f` |
| `ES8SYM/sets/mirror_46points_k8.txt` | `bf3b8e95f20d61ffe605ac18d768be17d99677e4da9012160f933f7f7c6cd263` |
| `ES8SYM/sets4/c3_61pts_centre.txt` | `006a0cae53478c728d6bdfe5a31f2d06a882aa29adba613e0cab74f54f5a6e2f` |
| `ES8SYM/sets/c7_64pts_small.pts` | `ebe028f65c3856a9a7c6fa595a3e735eb49a362f833b76089eea1b9f35a0ecc3` |
| `ES8SYM/sets3/c5_56pts_11layers_centre.pts` | `4cdd24bbeaa56d437420b1d1f63ca5ecb0fba64482ceb78ba6f1f7a496cf3387` |

## 6. What is not done, and remarks

- **Second reading** (11 November, after the clean build): the trusted file `LeanLB/Statement.lean` was read again
  against `ES8SYM/README.md` §2 (formats) and the source files (`c3_61pts_centre.log`: its symmetry is
  `(a, b) ↦ (−b, a − b)`, i.e. multiplication by `ω` in `a + bω` coordinates, as used here); `Invariant` and
  `rotAbout` were compared with `LAYERLEAN/LayerLemma.lean` (identical text) and `lineRefl` with
  `SYMLEAN/mirror` (identical body). The 5- and 7-fold assembly was first rejected by the elaborator (a heartbeat
  time-out while inferring the checker's parameters); it now passes them explicitly. No other issue.

- Only one file per row is checked: order type D of `SIX60` (the others, A, B, C, C', and the other four 7-fold
  order types of `ES8SYM` §6, would each need only a data file and a generated check module; about 2 minutes of
  kernel time each).
- The upper bounds (`C6UPPER`, `C7UPPER`, `SYMLEAN/mirror`) are not touched; this package proves only the lower
  bounds. The statements use the same `Invariant` and `rotAbout` text as `ENCBLEAN/geo`'s `sixfold_es8`, so the
  two halves of "the 6-fold maximum is exactly 60" are stated in the same terms (but live in different packages).
- The checker exists twice: the `Nat` version (`Checker.lean`, `CheckerSound.lean`, `Bridge.lean`) used for the
  five lattice sets, and the version with the orientation test as a parameter (`G/Checker.lean`, `G/Sound.lean`,
  `G/Bridge.lean`) used for the 5- and 7-fold sets. Their programme is the same.
- The 5- and 7-fold proofs use a certified approximation, not exact signs: if a margin were too small, a kernel
  check would fail (it would not give a wrong theorem).
