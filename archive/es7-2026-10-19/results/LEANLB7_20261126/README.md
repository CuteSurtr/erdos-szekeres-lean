# LEANLB7_20261126: the symmetric lower-bound sets for k = 7, Lean-checked

Lean 4 (v4.24.0), Mathlib `f897ebcf`, 26 November 2026 (KST), Linux. Built and audited inside the project
only; not reviewed by anyone else.

**Status.** The six point sets behind the lower bounds of RESULTS.md row **C7** (largest symmetric sets without a
convex 7-gon) are now Lean-checked: kernel evaluation with `decide +kernel`, no `native_decide`, no `sorry`, no new
axioms. Every theorem below has axioms `[propext, Classical.choice, Quot.sound]`, enforced at build time by
`#guard_msgs` in `LeanLB/Audit7.lean`.

| theorem (`LeanLB.`) | file (results/) | symmetry | n | before |
|---|---|---|---|---|
| `threefold31` | `SYMMAX/c3_31points.txt` | rotation by 2π/3 | 31 | exact computation, two methods |
| `fourfold28` | `SYMMAX/c4_28points.txt` | rotation by 2π/4 | 28 | exact computation, two methods |
| `fivefold31` | `SYMMAX/c5_31points.txt` | rotation by 2π/5 | 31 | exact computation, two methods |
| `sixfold30` | `SYMMAX/c6_30points.txt` | rotation by 2π/6 | 30 | exact computation, two methods |
| `halfturn32` | `SYM2/sym7_32points.txt` | rotation by π | 32 | exact computation |
| `mirror32` | `SYMMAX/mirror_32points.txt` | reflection in x = 0 | 32 | exact computation, two methods |

("Two methods": `SYMMAX/verifyg.py` / `verify5.py` and the brute force `brute.c` over every 7-point subset,
SYMMAX "Verification".) So the lower bounds N(3-fold) ≥ 31, N(4-fold) ≥ 28, N(5-fold) ≥ 31, N(6-fold) ≥ 30,
N(half-turn) ≥ 32 and N(mirror) ≥ 32 of row C7 are Lean-checked. The 32-point half-turn and mirror sets show that
Theorem A (C1: every set of at least 33 points with a non-trivial isometry or affine symmetry has a convex 7-gon) is
sharp.

**ES(7) ≥ 33.** From the half-turn set, this record also proves `LeanLB.not_forcesConvexNGon_32_7 :
¬ ForcesConvexNGon 32 7` and `LeanLB.heptagon_lower_bound : ForcesConvexNGon N 7 → 33 ≤ N` (`ForcesConvexNGon N n`:
every set of at least `N` points in general position has `n` points in convex position; vendored
`Definitions.lean`). The library already had the same bound for every n ≥ 3 from the Erdős–Szekeres construction
(RESULTS.md row B3, `ErdosSzekeres/LowerBound/Construction.lean`): `not_forcesConvexNGon_two_pow 7` is
`¬ ForcesConvexNGon (2 ^ 5) 7` and `conjecturedBound_le_of_forces` gives `2 ^ 5 + 1 ≤ N`. The new proof checks one
explicit 32-point set by kernel evaluation instead.

**Not in this record:** the upper bounds of row C7 (C2–C6; the 5-fold one is Lean-checked modulo one CERTIFIED
verdict in `FORMAL20261122/fivefold`; for the mirror one, RESULTS.md row C8 says its upper side is Lean-checked for
k = 4, …, 8 with no SAT input, record `MIRRORETV`), and the further sets `c3_30points.txt`, `c3_27points.txt`
(3-fold) and `c5_30points.txt` (5-fold), which are not table values.

## 1. The statements

All six have the same form as in LEANLB20261111; for the 5-fold set (`LeanLB/Main7.lean`):

```lean
theorem LeanLB.fivefold31 :
    setC5N31.card = 31 ∧ GeneralPosition setC5N31 ∧
      Invariant (rotAbout 0 (2 * Real.pi / 5)) setC5N31 ∧ ¬ HasConvexNGon 7 setC5N31
theorem LeanLB.exists_fivefold31 : ∃ S : Finset Point, S.card = 31 ∧ GeneralPosition S ∧
    Invariant (rotAbout 0 (2 * Real.pi / 5)) S ∧ ¬ HasConvexNGon 7 S
```

The others: `threefold31` (`31`, `2 * Real.pi / 3`), `fourfold28` (`28`, `2 * Real.pi / 4`), `sixfold30` (`30`,
`2 * Real.pi / 6`), `halfturn32` (`32`, `2 * Real.pi / 2`), `mirror32` (`32`, `Invariant (lineRefl 1 0 0)`), each
with `¬ HasConvexNGon 7` and an `exists_` form.

**What the words mean** (the trusted part): `ErdosSzekeres/Definitions.lean` (the repository's `Point`,
`GeneralPosition`, `HasConvexNGon`; vendored unchanged), the definitions `Invariant`, `rotAbout`, `lineRefl`,
`unitRoot`, `cycPoint`, `intPoint` of `LeanLB/Statement.lean` (unchanged from LEANLB20261111, where they are
explained), the six set definitions of `LeanLB/Statement7.lean`, and the rows in `LeanLB/Data/{C3N31, C6N30, C4N28,
C2N32, MirN32, C5N31}.lean`. The rows are read as in `SYMMAX/README.md`, "Coordinates":
- `c3_31points.txt`, `c6_30points.txt`: a row `a b` is `a + bω`, `ω = e^{2πi/3}` (`cycPoint 3 [a, b]`);
- `c5_31points.txt`: a row `c0 c1 c2 c3` is `c0 + c1 z + c2 z² + c3 z³`, `z = e^{2πi/5}` (`cycPoint 5`; the
  coefficient of `z⁴` is missing and counts as 0);
- `c4_28points.txt`, `mirror_32points.txt`, `SYM2/sym7_32points.txt`: a row `x y` is the point `(x, y)`
  (`intPoint`).

`scripts/gen_data7.py --check` regenerates the six data files from the set files byte for byte (it runs the k = 8
package's `gen_data.py`, copied unchanged, with only its table replaced); every row has the expected length
(`LeanLB/Check/Rows7.lean`).

## 2. How the proof goes

The checker, its soundness proof and the bridge to the plane are those of LEANLB20261111 (§2 there), **byte for
byte** (`scripts/audit7.sh` step 2 compares 23 files). The only parameter that changes is the chain bound: `checkAll 5`
(no anchor starts a chain of 6 left turns) instead of `checkAll 6`, and `lowerBound_of_check` / `G.lowerBound` give
`¬ HasConvexNGon (B + 2) = ¬ HasConvexNGon 7`. The kernel checks, per set (`LeanLB/Check/*.lean`, generated by
`scripts/gen_checks7.py`): the number of points, general position (`gpOK`: distinct points, every triple
non-collinear), the dynamic programme (`checkFrom` over 1–2 ranges of anchors), that the checker's list is the
translated lattice image of the rows (`_link`), and that the rows are closed under the symmetry (`_closed`). For the
5-fold set the coordinates lie in ℤ[t], t = 2cos(2π/5), and the checker runs on certified integer approximations
(`certOK`, `K = 40`, as for the k = 8 set `fivefold56`).

**New in this record** (`LeanLB/Geometry7.lean`, 3 row symmetries the k = 8 files did not need):
- `rot_six_eis`, `mulZeta3`: rotation by 60° of an Eisenstein row, `a + bω ↦ (a − b) + aω` (multiplication by
  `ζ = 1 + ω`; the k = 8 6-fold file used six coefficients instead);
- `rot90XY`: rotation by 90° of an integer row, `(x, y) ↦ (−y, x)` (with the k = 8 lemma `rot_four`);
- `G.mulZ5`, `G.rot_cycPoint_mulZ5`: rotation by 72° of a row in the basis `1, z, z², z³`, `w ↦ [w₄ − w₃, w₀ − w₃,
  w₁ − w₃, w₂ − w₃]` (multiplication by `z`, using `1 + z + z² + z³ + z⁴ = 0`; proved from the k = 8 lemmas
  `rot_cycPoint` and `cycPoint_five`). In this basis every point of ℤ[z] has one representation, so the file's rows
  are closed under the map exactly (checked by the kernel, `c5N31_closed`).

**Kernel work** (`logs/build_final.log`, clean `lake build` of 26 Nov, 2 CPUs): the six check modules took 5–10 s
each; the whole package 74 s wall, peak RSS 3.5 GB.

## 3. Audit and controls

- `scripts/audit7.sh` → `logs/audit7.log`: **AUDIT PASS** (vendored modules equal the repository's; 23 shared files
  equal LEANLB20261111; the six data files regenerate; each set file is tracked by git and unmodified against HEAD;
  no `sorry`/`admit`/`native_decide`/`axiom`/`implemented_by`/… in 48 Lean files; the axiom lines of the six
  theorems and the two ES(7) ≥ 33 corollaries; no error in the build log; the four controls rejected).
- `tests/Reject7.lean` → `logs/reject7.log`: each `decide +kernel` must fail and does (4 of 4): `checkAll 4` on the
  half-turn set (every 17 points in general position contain a convex hexagon, ES(6) = 17), three collinear points
  put in front of the list (`gpOK`), a wrong approximation (`certOK`), and `checkAll 4` on the 5-fold set. The k = 8
  record's control `checkAll 5` on its 46-point mirror set (which has convex 7-gons) also fails, so the bound
  `B = 5` is not vacuous.

## 4. Files

`LeanLB/` (sources; `Statement7`, `Geometry7`, `Main7`, `Audit7`, `Check/*`, `Data/*` of the six sets are new, the
rest is copied), `ErdosSzekeres/` (vendored, `VENDOR.sha256`), `scripts/` (`gen_data7.py`, `gen_checks7.py`,
`audit7.sh`; `gen_data.py` copied), `tests/Reject7.lean`, `logs/`, `SOURCES.sha256`. Reproduce: `lake build`
(Mathlib `f897ebcf` in `.lake/packages`, a copy of LEANLB20261111's), then `scripts/audit7.sh`.
