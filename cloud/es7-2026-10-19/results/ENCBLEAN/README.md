# ENCBLEAN: encoder B in Lean (M0 design, M1 byte-identical port, M2 functional twin and numbering bridge)

- **M1.** `EncB.gen m K t` is a Lean definition of the CNF that `C6UPPER/encb/gen_b2.py m K t` writes (gen_b2.py
  SHA-256 `3d47459a9723b5f7344205f3f2d7463e0be00b41c5070155e5da8dbf78fd40ba`). It has the same variable numbering,
  clause order and literal order as Python, for both even and odd m.
- **M2.** `EncB.encB m K t` is a second definition of the same CNF, written with list functions and closed-form
  variable codes (`genCoded`), then renumbered in the order of Python's `new()` calls (`allCodes`, `numberMap`).
  The theorems are about `encB`: model transfer, well-formedness, code decoding, and the cube cover of the 64 cubes.
- `lake exe encb_dimacs` prints either one in gen_b2.py's DIMACS layout, and prints cubes in the layout of
  `C6UPPER/tools/mkcubes.py`. With `twin-cubes64` the cubes are taken from the Lean list `cubes64` itself.

**Status (2026-11-06, 16:25 KST).**
- **M0, M1 and M2 are done, and the three fixes of the M2 review are applied** (section "M2 review fixes" below).
  The design is in `DESIGN.md` (§3.1 is M2).
- **M2 in one paragraph.** `encB` is proved well formed (`encB_wf`). A model of the coded clauses transfers to a
  model of `encB` (`dimacsSat_of_holds`); membership of every code in the numbering holds by construction. The codes
  decode back to their variables (`decodeCode_code`). The 64 cubes cover all assignments, so the statement
  `(∀ c ∈ cubes64, ¬ DimacsSatisfiable (cubeCnf (encB 6 8 11) c)) → ¬ DimacsSatisfiable (encB 6 8 11)` is a
  theorem (`encB_unsat_of_cubes64`). `encB` equals `gen` and Python on everything tested: bytes on the 225-instance
  grid and the four recorded instances, Lean values on 229 instances, and kernel evaluation on 4 tiny instances,
  one of them, (4,5,1), with a two-level chain.
- **Nothing about what the clauses mean is proved yet.** That is M3 to M9 of `DESIGN.md`; see "What is NOT yet
  proved" below.
- **The package is Std-only:** no `[[require]]`, no Mathlib, toolchain `leanprover/lean4:v4.24.0` (Lean 4.24.0,
  commit `797c613e`).
- **No forbidden constructs and standard axioms:**
  - no `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `partial`, `axiom`, `opaque`,
    `set_option` or `ofReduceBool` (`scripts/audit.sh`);
  - no `decide`/`rfl`/`simp`/`omega`/`#eval`/`#reduce` anywhere in a declaration that mentions the (6,8,11) instance
    (`encB`, `gen`, `genCoded`, `numVars`, `allCodes`, `allCodesOf`, `encode` or `diagCoded` applied to 6 8 11, or
    `CubesUnsat64`);
  - every declaration of the package, 236 named ones (47 theorems written in the source) found by walking the
    environment, has axioms within {propext, Classical.choice, Quot.sound} (`logs/axioms.log`); 17 of them are
    also guarded at build time by `#guard_msgs`.
- No git commit was made.

## What exists

| file | lines | content |
|---|---|---|
| `DESIGN.md` | 645 | M0: target theorem (variant A: 64 cubes on Y12 Y13 Y14 Y23 Y24 Y34), trust list E1–E6, interfaces (`Model`, `PolarLabelling`), lemma map, milestones M0–M9, risks; revision notes for M2 and the M2 review fixes at the top |
| `EncB/Gen.lean` | 382 | M1: the port (`canon`, `olit`, `angOuts`, `patternLit`, `unitOf`, itertools orders, `gen`). Unchanged since M1 (`ec97b335…`) |
| `EncB/Dimacs.lean` | 220 | M2: `DimacsSat`, `DimacsSatisfiable`, `LitSat` (copied from H/H3); `numberMap` (an `Array`), `decode`, `numberMap_getD`, `decode_numberMap`; re-proofs of Mathlib's `List.idxOf_cons_ne` and `List.getElem_idxOf`; `dedupStep` with `mem_dedup_foldl` |
| `EncB/Coded.lean` | 460 | M2: `Var`, the codes and `decodeCode_code`; the twin `genCoded`, `allCodes`, `encB`, `numVars` (via `encode`); `mem_allCodes`, `dimacsSat_of_holds`, `encB_wf`; `diagCoded` (refusal flags for the emitter only) |
| `EncB/Cover.lean` | 121 | M2: `CubeSat`, `Covers`, `cubeCnf`, `not_dimacsSatisfiable_of_cover` (copied from H3); `signPatterns`, `covers_signPatterns`; `cubeVars64`, `cubes64`, `CubesUnsat64`, `encB_unsat_of_cubes64` |
| `EncB/KernelCheckB.lean` | 102 | M2: `decide +kernel` on `encB`/`numVars` at (3,4,1), (3,4,2), (6,4,1), (4,5,1), on `gen` at (4,5,1) and on `codesDecode` at (3,4,2); `#guard_msgs` axiom audit of the M2 theorems |
| `EncB/Emit.lean` | 301 | M1's modes unchanged; M2's `twin-*` modes; `bodyL`, `cubeBody`, `cubeBody_eq` (the printed cube text is the rendering of `cubeCnf F c`) |
| `EncB/KernelCheck.lean` | 35 | M1: `decide +kernel` on `gen` at (3,4,1), (3,4,2), (4,4,2) |
| `ref/make_ref.py`, `ref/hashes.tsv` | 80 | M1: the reference corpus (225 instances from gen_b2.py) |
| `scripts/compare_b.sh` | 34 | the 225 grid instances by SHA-256; second argument `gen` or `twin` |
| `scripts/twin_check.sh` | 25 | M2: `encB = gen` as Lean values (no printing) on the grid plus extra instances |
| `scripts/check_recorded.sh` | 127 | recorded instances; third argument `gen` or `twin`. Twin `big` = one emission of (6,8,11) with cubes from `cubes64`, the cube-variable check and the emitted-file check |
| `scripts/audit.sh` | 64 | static checks (forbidden tokens, Std-only, toolchain, no kernel evaluation of the (6,8,11) instance, checked per declaration) |
| `logs/` | | see "M2 results", "M2 review fixes" and "M1 results" below; `env.txt` has every source hash; `axioms_enum.lean.txt` and `axioms_query.lean.txt` are the two axiom queries |

Lines of Lean code written in M2, without blank and comment lines: Dimacs 154, Coded 285, Cover 73, KernelCheckB 40
(30 before the review fixes), plus 133 in Emit.lean (from 90 to 223 such lines; 132 to 301 lines in all). Scripts:
`twin_check.sh` is new; the other three gained a mode argument (+8, +48 and +10 lines). The review fixes rewrote
check 4 of `audit.sh` (35 to 64 lines).

## How to build and run

Every compile and every run goes at nice 10, one at a time, inside an 8 GB scope. `lake build` is run only in this
directory.

```
cd cloud/es7-2026-10-19/results/ENCBLEAN
export PATH=$HOME/.elan/bin:$PATH
CAP="systemd-run --user --scope -q -p MemoryMax=8G -p MemorySwapMax=0 nice -n 10"
$CAP lake build                                        # clean: 21 s wall, 2.1 GB peak (KernelCheckB 17-19 s, KernelCheck 11 s)
$CAP scripts/audit.sh
$CAP scripts/compare_b.sh ref/hashes.tsv twin          # 48 s; the 225 grid instances, encB
$CAP scripts/compare_b.sh ref/hashes.tsv gen           # 23 s; the same, gen (M1)
$CAP scripts/twin_check.sh ref/hashes.tsv '6 8 9' '7 8 9' '7 8 10'   # 110 s; encB = gen as values
$CAP scripts/check_recorded.sh SCRATCH small twin      # 33 s; (6,8,9), (7,8,9), (7,8,10)
$CAP scripts/check_recorded.sh SCRATCH big twin        # 16 s; (6,8,11) once, ~470 MB transient in SCRATCH, deleted
$CAP python3 ref/make_ref.py OUT.tsv                   # 59 s; regenerates the corpus from gen_b2.py
```

How to call the exe (the `twin-*` modes print `encB`, the others print `gen`):

```
.lake/build/bin/encb_dimacs twin-base 6 8 11 > B.cnf                    # encB 6 8 11
.lake/build/bin/encb_dimacs twin-cube 6 8 11 1 2 3 -10 11 18 > c.cnf    # cubeCnf (encB 6 8 11) [1, 2, 3, -10, 11, 18]
.lake/build/bin/encb_dimacs twin-cubes64 6 8 11 DIR [NAME ...]         # DIR/base.cnf + the cubes of cubes64 (all 64 if no NAME)
.lake/build/bin/encb_dimacs twin-check 6 8 11                           # encB = gen in memory, nothing written
.lake/build/bin/encb_dimacs twin-stats|twin-ymap|twin-profile M K T     # summary line / Y numbering / phase times
.lake/build/bin/encb_dimacs base|stats M K T, cube M K T U..., files M K T DIR NAME...   # gen, as in M1
```

- **Cube names.** `cBBBBB` is the cube whose first unit is +Y12, followed by the pattern on Y13 Y14 Y23 Y24 Y34,
  where bit 1 means a positive literal; these are mkcubes' 32 cubes. `nBBBBB` is the same pattern with −Y12 first;
  these are the cubes of the c6upper-noty12 run. `twin-cubes64` derives each name from the signs of the cube
  (`cubeName`, Emit.lean:84). It writes only cubes of `cubes64`, in list order.
- **Variable numbers.** At t = 11, Y12 Y13 Y14 Y23 Y24 Y34 are the variables 1, 2, 3, 10, 11 and 18
  (`cubeVars64`).
- **Refusal.** On an instance where gen_b2.py raises, the exe writes nothing and exits with 1. For the twin this is
  decided by `diagCoded`.

## M2: the functional twin and the numbering bridge

### What is proved (all Std-only; axioms in `logs/axioms.log`)

| statement | file:line | axioms |
|---|---|---|
| `numberMap_getD : v ∈ l → (numberMap l).getD v 0 = l.idxOf v + 1` | Dimacs.lean:147 | propext, choice, Quot.sound |
| `decode_numberMap : v ∈ l → decode l ((numberMap l).getD v 0) = v` | Dimacs.lean:162 | propext, choice, Quot.sound |
| `idxOf_cons_ne`, `getElem_idxOf` (Mathlib's, re-proved) | Dimacs.lean:38, 45 | propext / propext, choice, Quot.sound |
| `decodeCode_code : v.Valid m K t → decodeCode m K t (v.code m K t) = v` (layer < t, sector < m, pivot < t, level < FL; no hypothesis on K) | Coded.lean:127 | propext, Quot.sound |
| `mem_allCodes : cl ∈ genCoded m K t → x ∈ cl → x.natAbs ∈ allCodes m K t` | Coded.lean:365 | propext, Quot.sound |
| `dimacsSat_of_holds : (∀ cl ∈ genCoded m K t, ∃ x ∈ cl, CodeLitHolds (τ ∘ decodeCode m K t) x) → DimacsSat (encB m K t) (nuOf m K t τ)` | Coded.lean:381 | propext, choice, Quot.sound |
| `dimacsSatisfiable_of_holds` (the same, existential) | Coded.lean:404 | propext, choice, Quot.sound |
| `encB_wf : ∀ cl ∈ encB m K t, ∀ l ∈ cl, l ≠ 0 ∧ l.natAbs ≤ numVars m K t` | Coded.lean:410 | propext, choice, Quot.sound |
| `encB_eq`, `numVars_eq`, `allCodes_eq` (by `rfl`: `encB` is the renumbering of `genCoded`, `numVars` the length of `allCodes`) | Coded.lean:335-340 | none |
| `covers_signPatterns : (∀ v ∈ vs, v ≠ 0) → Covers (signPatterns vs)` | Cover.lean:58 | propext, choice, Quot.sound |
| `not_dimacsSatisfiable_of_cover` (H3 `Cover.lean:98`) | Cover.lean:82 | propext, Quot.sound |
| `length_cubes64 : cubes64.length = 64` | Cover.lean:105 | propext, Quot.sound |
| **`encB_unsat_of_cubes64 : (∀ c ∈ cubes64, ¬ DimacsSatisfiable (cubeCnf (encB 6 8 11) c)) → ¬ DimacsSatisfiable (encB 6 8 11)`** | Cover.lean:114 | propext, choice, Quot.sound |
| `cubeBody_eq : cubeBody (bodyL F) c = bodyL (cubeCnf F c)` (what the emitter prints for a cube) | Emit.lean:79 | propext, Quot.sound |

- **The definitions.** `genCoded`, `encB`, `numVars`, `allCodes` and `cubes64` use no axioms (`#print axioms`).
- **No kernel evaluation of (6,8,11).** `encB_unsat_of_cubes64` is
  `not_dimacsSatisfiable_of_cover (covers_signPatterns cubeVars64_ne_zero) h`. Its only `decide` is
  `cubeVars64_ne_zero` (six numerals ≠ 0), and Cover.lean builds in 0.27 s.
- **Model transfer needs no allocation lemma.** Every code of `genCoded` is in `allCodes` because `allCodes` is
  built from the codes of `genCoded` (`mem_allCodes`). That `allCodes` is exactly Python's `new()` order, so that
  the numbers agree, is checked only by bytes (D4 of `DESIGN.md`).

### How `encB` is built (Coded.lean)

- **Codes** (Coded.lean:55-65):
  - Y(i,j) ↦ 1 + i·t + j;
  - H(i) ↦ t² + 1 + i;
  - orb c ↦ oBase + triCode c;
  - F(piv,l,a,b) ↦ fBase + ((piv·FL + l)·N + ptCode a)·N + ptCode b, with N = t·m and FL = max (K−1) 3, as in
    `DESIGN.md` §3.1.
- **`genCoded`** (Coded.lean:281) = `transCl ++ angular ++ nesting ++ chains`, built only from `flatMap`,
  `filterMap`, `map` and `foldl`. It calls Gen's `canon`, `olit`, `angOuts`, `unitOf` and `triples` unchanged, with
  `orbVar := orbVarC` and `yv`, `hv` the closed-form codes:
  - the orbit list (first-seen order) is `orbList` (:187);
  - the chains per pivot are `okList` (:228), `extItems` (:242), `levelStep` (:268) and `chainCl` (:274). The key
    set of each level is an argument; it is only a filter.
- **`allCodes`** (:300): `prefixCodes` (Y, H, orbits), then the codes of `genCoded` in stream order, each kept once.
- **`encode`** (:320) computes `genCoded`, `allCodes` and `numberMap` once. `encB`, `numVars` and `allCodes` are
  its fields, so the emitter prints exactly `encB` and `numVars`.

**Deviations from `DESIGN.md` §3.1, and why:**

1. **`numberMap` is an `Array Nat` indexed by the code, not H's `Std.HashMap`.** The kernel cannot reduce a
   `HashMap`: its bucket index is a `USize`, and `USize.size` depends on an opaque platform constant. An array makes
   `decide +kernel` on `encB` possible. H's proofs carry over (`numberStep_foldl`, Dimacs.lean:101), because the
   array has `1 + (largest code)` entries.
2. **`orbVarC` returns a code only for three distinct valid labels**, not `some ∘ orbCode`. So `olit` fails
   exactly where Python raises `KeyError`, as Gen's `orbTab` lookup does, and every orbit literal of `genCoded`
   decodes to a valid triple.
3. **No `okpair` map.** In the extension step `(a, b) ∈ okpair` and `okpair[(a, b)]` are recomputed as
   `olit p a b = some lab` with `¬ is_false lab`. The literal in the clause is therefore `olit p a b` by
   definition, which M3 can use directly. This costs one extra `olit` per inner step (see the times below).
4. **`Var` has a fifth constructor, `other n`**, the image of codes outside every range; M3's τ maps it to `False`.
5. **The even kernel instance is (6,4,1), not (4,4,2).** `encB 4 4 2` in the kernel was OOM-killed at the 8 GB cap
   after 33 s. `allCodes 4 4 2` alone took 28 s and 5.5 GB: every step of its 903-entry seen-array is O(size) in
   the kernel. (6,4,1) took 7.5 s and 1.8 GB.
6. **`diagCoded`**, the refusal flags of the twin modes, does not recount failures of the extension `olit a b c`.
   Its three labels are pairwise distinct labels of Q, so `canon` of them is a key of `orb` and this `olit` cannot
   fail. This affects only the refusal, never `encB`. On the grid the twin refuses exactly the three rows where
   Python raises.
7. **The cube files render the list `cubeCnf F c` itself** (`cubeBody_eq`). For a non-empty F this is mkcubes'
   layout byte for byte. Only for an empty F would mkcubes add an extra newline.

### Evidence (exe `e9454996…`, built twice from clean with the same hash; load average about 30 on 32 cores)

**(a) Tiny grid, bytes: 225 of 225 agree, for `encB` and for `gen`.**
- `logs/compare_tiny_twin.log` (47.7 s): 222 byte-identical to gen_b2.py, and 3 refused where Python raises:
  (2,4,3) and (2,5,4) (`RuntimeError: conflict`) and (1,4,2) (`KeyError`).
- `logs/compare_tiny.log` (22.7 s): the same for `gen` with this exe (a regression check of M1).

**(b) `encB = gen` as Lean values: 228 of 228** (`logs/twin_check.log`, 110 s). `twin-check` compares
`encB m K t` with `(gen m K t).clauses.toList`, `numVars` with `nv`, and the refusal flags. It covers the 225 grid
rows (222 EQUAL, 3 BOTH-REFUSE) and (6,8,9), (7,8,9), (7,8,10). No printing is involved, so a bug in the text
renderer cannot hide a difference here.

**(c) Kernel** (`EncB/KernelCheckB.lean`, 19 s in the build). `decide +kernel` proves:
- `numVars 3 4 1 = 2 ∧ encB 3 4 1 = [[1], [2, -1]]`;
- the same for (3,4,2) (22 variables, 32 clauses) and (6,4,1) (20 variables, 48 clauses), against the gen_b2.py
  lists (for (6,4,1) a fresh gen_b2.py output whose SHA-256 equals the corpus row `dd42c2e8…`);
- the same for (4,5,1) (13 variables, 18 clauses), for `encB` and for `gen` (added by the review fixes; the only
  kernel instance with K > 4, see below);
- `codesDecode 3 4 2 (allCodes 3 4 2) = true`: every DIMACS variable decodes to a valid `Var` whose code it is.

**(d) Recorded instances, streamed into sha256sum: all MATCH** (`logs/check_recorded_small_twin.log`, the
hashes are read from the record files as in M1):

| instance | SHA-256 (encB = record) | encB wall / user / max RSS | gen (same exe) |
|---|---|---|---|
| (6,8,9) | `9f63854369a76998e13217e1f4208e365d0821b07f253decca2b9aed1ba1d350` | 6.29 s / 6.18 s / 211 MB | 2.65 s / 188 MB |
| (7,8,9) | `67cd613d024e36912e61aeae1bb582e1cd992659a6902dfa936ba1f1caa300aa` | 11.95 s / 11.85 s / 378 MB | 5.04 s / 348 MB |
| (7,8,10) | `b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2` | 14.29 s / 14.12 s / 550 MB | 7.72 s / 487 MB |

Every twin run also reports `"codesDecode": true`: all `numVars` DIMACS variables decode to valid variables.

**(e) (6,8,11): one emission from `encB`, 8 files, all MATCH** (`logs/check_recorded_big_twin.log`). The run
`twin-cubes64 6 8 11` took 15.26 s wall, 14.94 s user and 928 MB max RSS. That covers the generation plus writing
base and 7 cubes (8 × 58.6 MB) to the session scratchpad (`encblean/b6811`). The files were hashed and deleted.
- **Counts.** nv 78,059, ncl 2,387,083, `"codesDecode": true`.
- **Cube variables, checked by compiled code during the run, not by the kernel.** The exe's numbers of Y12 Y13 Y14
  Y23 Y24 Y34 are `[1, 2, 3, 10, 11, 18]`. That equals `cubeVars64` and the Y entries of gen_b2.py's map
  `C6UPPER/encb/B_m6K8t11.meta.json` (`68b43494…`). Decoding 1, 2, 3, 10, 11, 18 gives
  `Var.y 1 2, …, Var.y 3 4`, and every cube of `cubes64` is on these six variables.
- **Checked on the emitted file.** Clauses 1–4, 17–18 and 73–74 of the emitted `base.cnf` are the transitivity
  clauses of the triples (1,2,3), (1,2,4), (1,3,4) and (2,3,4) (gen_b2.py:79-81), written with exactly these
  numbers: `-1 -10 2 0`, `1 10 -2 0`, `-1 -11 3 0`, `1 11 -3 0`, `-2 -18 3 0`, `2 18 -3 0`, `-10 -18 11 0` and
  `10 18 -11 0`.

| file (from `cubes64`) | bytes | SHA-256 (encB = record) | record |
|---|---|---|---|
| base | 58,618,857 | `479e31a9e8d58d752c86b9abf02fb799c10615a7e61a88f132c49734674f37fc` | `C6UPPER/SHA256SUMS.txt:86` |
| c11111 | 58,618,884 | `0fa206f7b75f8653e8da78dd3b750294d3ddafd8b86da53a489d8cc63fa02a8e` | `C6UPPER/SHA256SUMS.txt` B/ |
| c11011 | 58,618,885 | `32bdbdc2a615a6a8b110de612f5a3138c74559ba8f45b6d2aecc055322f4ad45` | `C6UPPER/SHA256SUMS.txt` B/ |
| c10101 | 58,618,886 | `5bfddfed9e280468eb3d616d7844886235bc5321ae94d44b8de8019cd7f68ec3` | `C6UPPER/SHA256SUMS.txt` B/ |
| c00000 | 58,618,889 | `206f2b4f3ebfbcceb2ba5dc5eb6ec68bef51059a8ca734fac9d837567d19f396` | `C6UPPER/SHA256SUMS.txt` B/ |
| n11111 | 58,618,885 | `efdf4681b3cfe45c5e0999fdf74cbce426bf627c53e71720b6a30e993e697d2d` | noty12 `cubes.sha256` |
| n10100 | 58,618,888 | `96161b8ea82e6b365e6789294d19cf81ed7ce359aaf4025310e6410b5ea64ea7` | noty12 `cubes.sha256` |
| n00000 | 58,618,890 | `33894742a77ef9fc56af7411d05c089d179bc2f5eb091a758d9bf94ee34d19d0` | noty12 `cubes.sha256` |

**(f) (6,8,11) as Lean values** (`logs/twin_check_6811.log`). `twin-check 6 8 11` gives EQUAL:
`encB 6 8 11 = (gen 6 8 11).clauses.toList` and `numVars 6 8 11 = 78059 = nv`. It writes no file; this is the
second and last compiled evaluation of `encB 6 8 11`.
- `encode` took 11.0 s and `gen` 4.6 s.
- The whole run took 17.3 s and 748 MB max RSS.

**Time and memory of `encB`.**
- **About 2.4× `gen`.** At (6,8,11), `encode` alone takes 11.0 s and the emission with 8 files 15.3 s and 928 MB,
  against `gen`'s 4.6 s and M1's 6.2 s / 428 MB. That is well inside the 8 GB cap and the design's 10× allowance.
- **Where the time goes** (`twin-profile`, `logs/twin_profile.log`):

  | instance | diagCoded | genCoded | allCodesOf | renumber | bodyL | total |
  |---|---|---|---|---|---|---|
  | (6,8,9) | 0.1 s | 4.7 s | 0.3 s | 0.2 s | 0.8 s | 6.2 s, 211 MB |
  | (7,8,10) | 1.3 s | 13.4 s | 0.7 s | 0.7 s | 2.1 s | 18.3 s, 552 MB |

- **The cost is in `genCoded`,** mostly the extra `olit p a b` per extension step (deviation 3). An `okpair` table
  would remove it, at the price of a table lemma in M3. It is not needed at these sizes.

**(g) Audit** (`logs/audit.log`). `scripts/audit.sh` passes. Its check 4, as broadened by the review fixes, lists the
three declarations that mention the (6,8,11) instance (all in Cover.lean: `CubesUnsat64` and the two cover
theorems, statements and term proofs only). Six negative tests are in the log (see "M2 review fixes").

## M2 review fixes (2026-11-06, about 16:20 KST)

The review of M2 found no soundness, vacuity or byte-identity problem. It listed three minor fixes; each was checked
against the files, found real, and fixed. Only `EncB/KernelCheckB.lean`, `scripts/audit.sh`, the logs and the two
documents changed.

1. **No kernel instance had a chain of two levels.** Confirmed. Every kernel instance has K = 4: (3,4,1), (3,4,2),
   (6,4,1) here and (3,4,1), (3,4,2), (4,4,2) in `KernelCheck.lean`. At K = 4, `rng 2 (K - 1) = [2]` is one closing
   level. So neither the branch `lev + 1 < K - 1` of `extItems` (Gen: `lev + 1 < L`) nor the key set that
   `levelStep` passes to the next level was ever evaluated by the kernel.
   - **Fix:** two theorems in `KernelCheckB.lean`, both by `decide +kernel` and guarded by `#guard_msgs`:
     `encB_4_5_1 : numVars 4 5 1 = 13 ∧ encB 4 5 1 = […]` (no axioms) and `gen_4_5_1`, the same list for M1's
     `gen` ([propext]).
   - **The list:** gen_b2.py `3d47459a…` was rerun on (4,5,1). The output's SHA-256 `6b5cccde…` equals the corpus
     row, and the list equals the review's character for character.
   - **What it covers:** 6 base clauses (F₂ = variables 2–7), 6 extension clauses `[-F₂(b,c), -lab, -lt, F₃(a,b)]`
     (F₃ = variables 8–13), and 6 closing clauses `[-F₃(b,c), -lab, -lt]` on the key set of F₃.
   - **Cost:** both theorems together took 2.5 s and 750 MB in a scratch test. `KernelCheckB.lean` now builds in
     19 s (17 s before) with a 2.17 GB peak.
2. **Audit check 4 matched only the text `encB 6 8 11` on a single line.** Confirmed by negative tests. The M2
   audit passed all of these:
   - a `numVars 6 8 11` theorem with `decide` on the next line;
   - `(gen  6` / `8 11)` split over two lines and proved by `rfl`;
   - a `simp` proof of `CubesUnsat64`;
   - `set_option debug.skipKernelTC true`.

   **Fix:**
   - Check 4 now works per declaration: a column-0 command together with its continuation lines.
   - It matches `encB`, `gen`, `genCoded`, `numVars`, `allCodes`, `allCodesOf`, `encode` or `diagCoded` applied to
     `6 8 11` with any whitespace, and also `CubesUnsat64`. A declaration that matches fails the audit if it contains
     `decide`, `rfl`, `simp`, `simp_all`, `dsimp`, `omega`, `native_decide`, `of_decide_eq_true`, `example`,
     `run_cmd`, `#eval` or `#reduce` anywhere.
   - Check 1 now also forbids `set_option`, which covers `debug.skipKernelTC`, and `ofReduceBool`.
   - The header comment now names both `KernelCheck.lean` and `KernelCheckB.lean` as the build-time axiom guards.

   **Result:** the new audit passes the package and an unmodified copy, and fails on all five negative copies
   (`logs/audit.log`). It is still a text check, which indirection could evade. The real guard is the build itself:
   `Cover.lean`, which states the (6,8,11) theorems, builds in 0.27 s.
3. **`logs/axioms.log` listed 33 hand-picked names.** Confirmed: 15 M2 helper theorems (`div_mul_add`,
   `mem_dedup_clauses`, `mem_allCodesOf`, `numberMap_getD_le`, `dedupStep_spec`, …) and M1's three `gen_*` kernel
   theorems were missing. All 18 are within the three axioms. The review
   suggested appending its own list, but that would still be a list made by hand. Instead the log was regenerated
   from the environment by two queries:
   - **Query 1** (`logs/axioms_enum.lean.txt`) walks every constant declared in a module `EncB.*` and applies
     `Lean.collectAxioms`, the function behind `#print axioms`.
   - **Query 2** (`logs/axioms_query.lean.txt`) runs `#print axioms` on each of the 236 names that query 1 found.

   **Result:**
   - There are 236 named declarations: 71 theorems (47 written in the source, 24 generated, such as `injEq` and
     `sizeOf_spec`) and 165 definitions, inductives and constructors.
   - There are also 222 internal auxiliaries (`match_`, `proof_` and equation lemmas, recursors, private names).
   - All of them use only propext, Classical.choice and Quot.sound, and the two queries agree on every name.
   - The 47 source theorems are the review's 45 plus `encB_4_5_1` and `gen_4_5_1`.

**Reruns with the fixed package.** No source of the exe changed, and the exe is still `e9454996…`.
- **Build.** An incremental `lake build` returned 0 in 19.6 s with a 2.11 GB peak, rebuilding only `KernelCheckB`
  and `EncB`; the M2 clean builds already showed that the exe is reproducible. Every file was also recompiled from
  source with plain `lean` into scratch oleans. All 8 returned 0 with no message, so every `#guard_msgs` holds
  (`logs/build.log`).
- **Grid, by bytes.** `compare_b.sh twin`: 225/225 (222 MATCH, 3 REFUSED where Python raises) in 53.9 s.
  `compare_b.sh gen`: 225/225 in 25.4 s.
- **Values.** `twin_check.sh` on the grid plus (6,8,9), (7,8,9) and (7,8,10): 228/228 (225 EQUAL, 3 BOTH-REFUSE) in
  103.4 s.
- **Recorded instances.** `check_recorded.sh small twin` and `small gen`: (6,8,9), (7,8,9) and (7,8,10) all MATCH.
  The twin took 5.7 s, 11.2 s and 17.3 s.
- **(6,8,11) was not emitted again.** The exe is byte-identical to the one that made M2's emission (base and 7
  cubes, `logs/check_recorded_big_twin.log`). The review's own emission with the same exe matched the base and 7
  other cubes, but that run is not logged in this package.
- **For M3.** The review also named three lemmas that M3 needs first. They are listed under "What is NOT yet proved".

## M1 results (rerun 2026-11-06, 14:57–14:59 KST, exe `521dd64d…`)

The numbers in this section are M1's. In M2, `logs/compare_tiny.log` and `logs/check_recorded_small.log` were
rerun for `gen` with the M2 exe `e9454996…`, with the same results: 225/225 in 22.7 s, and three MATCHes at
2.65 s / 5.04 s / 7.72 s. `logs/check_recorded_big.log` and `logs/ref_regen.log` are still M1's.

The exe was rebuilt from scratch (`rm -rf .lake/build; lake build`). Its SHA-256 is
`521dd64d97cff63c4716ac6ac1cbf54863fdb3ac8d358868784a866fbdacddda`, identical to the M1 build, so the build is
reproducible. The load average was about 35 on 32 cores throughout, so all times are measured under contention.

**(a) Tiny grid: 225 of 225 agree** (`logs/compare_tiny.log`, 28.7 s).
- **Grid.** It covers every m in 3..8, K in 4..2m and t in 1..4 (192 instances), plus 33 extras:
  - K ≤ 3 and t = 0;
  - m ∈ {1, 2, 9, 10};
  - t = 5, 6 at K = 8 for m = 3..8;
  - t = 7, 8 at K = 8 for m = 6, 7.
- **222 are byte-identical** to gen_b2.py: 99 with odd m and 123 with even m.
- **On the other 3, Python raises and the exe refuses:** (2,4,3) and (2,5,4) (`RuntimeError: conflict`) and
  (1,4,2) (`KeyError`).
- **The corpus is not taken on faith.** `make_ref.py` was rerun from gen_b2.py `3d47459a…` into a scratch file in
  58.8 s. All 225 rows are identical to `ref/hashes.tsv` in every column except `seconds`; both give the column
  hash `5eba6a36…` (`logs/ref_regen.log`).

**(b) Recorded instances, streamed into sha256sum: all MATCH** (`logs/check_recorded_small.log`).

| instance | SHA-256 (Lean = record) | record read from, cross-checked against | Lean wall | max RSS |
|---|---|---|---|---|
| (6,8,9) | `9f63854369a76998e13217e1f4208e365d0821b07f253decca2b9aed1ba1d350` | `C6UPPER/logs/encb_gen.log:6` = `K8EXACT20261106/logs/regen_hashes.log:15` | 2.68 s | 188 MB |
| (7,8,9) | `67cd613d024e36912e61aeae1bb582e1cd992659a6902dfa936ba1f1caa300aa` | `K8EXACT20261106/logs/gen_m7K8t9.log` = `logs/exact_check.jsonl:2` | 5.12 s | 348 MB |
| (7,8,10) | `b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2` | `C7UPPER/SHA256SUMS.txt` (cnfb/m7K8t10.cnf) = `C6UPPER/logs/encb_gen.log:3` | 7.60 s | 488 MB |

- **Counts.** They equal Python's, e.g. (6,8,9): nv 42,728, ncl 1,040,348.
- **The (7,8,9) record is not independent.** It is gen_b2.py output of 2026-11-05 (`K8EXACT20261106/README.md`:
  "no earlier recorded hash exists"). For comparison, gen_b2.py on (7,8,10) took 18.1 s and 628 MB under the same
  load (M1 step).

**(c) (6,8,11): one generation, 8 files, all MATCH** (`logs/check_recorded_big.log`).
- **Cost.** `encb_dimacs files` took 6.21 s wall, 5.79 s user and 428 MB max RSS for the generation plus writing the
  8 files; with hashing, 6.7 s.
- **Counts.** nv 78,059, ncl 2,387,083, unit 2,347, cond 7,740, chain 2,376,426, equal to `C6UPPER/logs/encb_gen.log:8`.
- **Cleanup.** The files were written to the session scratchpad (`encblean/b6811`), hashed and deleted.

| file | bytes | SHA-256 (Lean = record) | record |
|---|---|---|---|
| base `B_m6K8t11` | 58,618,857 | `479e31a9e8d58d752c86b9abf02fb799c10615a7e61a88f132c49734674f37fc` | `C6UPPER/SHA256SUMS.txt:86` |
| `full_Y12` | 58,618,861 | `1b09c21076189717407dfb4e187bbaa41fd2174f8b7eb7a5d61f7e5af2153395` | `C6UPPER/SHA256SUMS.txt:87` |
| `c00000` | 58,618,889 | `206f2b4f3ebfbcceb2ba5dc5eb6ec68bef51059a8ca734fac9d837567d19f396` | `C6UPPER/SHA256SUMS.txt` B/ |
| `c11011` | 58,618,885 | `32bdbdc2a615a6a8b110de612f5a3138c74559ba8f45b6d2aecc055322f4ad45` | `C6UPPER/SHA256SUMS.txt` B/ |
| `c10101` | 58,618,886 | `5bfddfed9e280468eb3d616d7844886235bc5321ae94d44b8de8019cd7f68ec3` | `C6UPPER/SHA256SUMS.txt` B/ |
| `c11111` | 58,618,884 | `0fa206f7b75f8653e8da78dd3b750294d3ddafd8b86da53a489d8cc63fa02a8e` | `C6UPPER/SHA256SUMS.txt` B/ |
| `n11111` | 58,618,885 | `efdf4681b3cfe45c5e0999fdf74cbce426bf627c53e71720b6a30e993e697d2d` | noty12 `cubes.sha256` |
| `n00000` | 58,618,890 | `33894742a77ef9fc56af7411d05c089d179bc2f5eb091a758d9bf94ee34d19d0` | noty12 `cubes.sha256` |

The noty12 hash list is `/home/jay/research/data/c6upper-noty12-20261106/cubes.sha256`. It was only read; the
running unit `c6upper-noty12` was not touched. Its `results.tsv` had 8 of 32 ACCEPTED at 14:43. The other 57 cubes
differ only in their 6-unit tail, which is printed by the same code; all 64 are checked in M9.

**(d) Kernel check and audit.**
- **Build.** The clean `lake build` builds `EncB/KernelCheck.lean` in 12 s. That file holds three `decide +kernel`
  equalities (kernel evaluation of `gen` against gen_b2.py's lists) and `#guard_msgs` on `#print axioms`
  (`[propext]`).
- **Audit.** `scripts/audit.sh` passes (`logs/audit.log`). A negative test (an appended `sorry` in a scratch copy)
  makes it fail.

**Independent review (the skeptic step, before this fix).** Its files are in the session scratchpad,
`encb-skeptic/`. It found:
- 28 MATCH and 3 REFUSED on a 31-row sample;
- 30 of 30 fresh gen_b2.py runs equal to the exe, 19 of them outside the grid;
- interpreter runs (`lake env lean --run`) equal to the compiled exe;
- no embedded hashes or paths in the exe;
- branch coverage of gen_b2.py: no branch is reached at (6,8,11) that the m = 6 tiny rows do not reach.

## How the port `gen` mirrors gen_b2.py (M1)

Nothing in gen_b2.py uses floats. The angular configuration uses only integers (`J = 2k + h` or `J = k`, ranks, `%`,
`//`), and so does the port. Determinism holds for these reasons:
- **Dicts.** Every dict is an `Array` indexed by a code of the key that is injective on keys that occur; 0 means
  absent, and every stored value is nonzero. The two dicts that are iterated, `orb` and `okpair`, also keep an
  insertion-ordered array. Each key is inserted once, so insertion order is loop order.
- **Sets.** The only `set.pop()` (line 136) happens on a one-element set; it is `unitOf`.
- **Sorting.** `sorted` is a stable insertion sort, applied only to lists with distinct entries. The `objs` tuples
  `((J, r), kind, idx)` are compared on the full tuple, with `'A' < 'P'` encoded as 0 < 1.
- **itertools.** Its orders are reproduced exactly:
  - `pairs`/`triples` for combinations;
  - `perms` for lexicographic permutations;
  - `bitTuples` for `product`, last coordinate fastest.
- **Variable allocation.** `nv` is threaded through the loops, and `fv` is inlined at its two call sites, so chain
  variables are allocated in clause-stream order.
- **Failure cases.** Where Python raises (an `assert`, a `KeyError`, either `RuntimeError`), Lean drops the literal
  and counts `bad`, or sets `conflict`, and the exe refuses to print. `bad = 0` for every m ≥ 2.
- **Array bounds.** Every `setIfInBounds` index stays in range (checked by the review). `orbTab` has N³ entries,
  `F` has `max (K−1) 3 · N²`, and `forced` has nv + 1 and is indexed only by orbit literals.

| gen_b2.py | content | Gen.lean / Emit.lean |
|---|---|---|
| 28-34 | arguments, `odd`, `nv`/`new()` (`pid` at 30 is unused, so not ported) | `gen` 240-242 |
| 36-39 | `Yv`, lexicographic | 243-248 |
| 40 | `Hv`, odd m only | 249-254 |
| 42-49 | `canon` | `rotate` 98, `canon` 103-109 |
| 50-55 | `orb`, numbered in order of first appearance over `combinations(pts, 3)` | 259-275 (`orbTab` + `orbList`) |
| 56-62 | `perm_sign` | `permSign` 91-92 |
| 63-76 | `olit`: first matching rotation, then argsort sign | `olit` 114-125 |
| 79-81 | transitivity | 277-281 |
| 83-85 | `forced`, counters, loop over `orb.items()` | 282-290 |
| 86-87 | `Ls`, `free` | `angOuts` 187-189 |
| 89-94 | `permutations` × `product`, `rk`, `h` | `angOuts` 190-196 |
| 96-102 | premises (Y literals, then H literals) | `angOuts` 198-204 |
| 104-111 | keys of the points and antipodes | `patternLit` 144-153 |
| 112-117 | equal keys give no clause (`assert not odd`) | `patternLit` 154-156 |
| 118-119 | sort, `kinds` | `patternLit` 158-161 |
| 121-124 | rule A (`PAPAPA`/`APAPAP`) | `patternLit` 162-166 |
| 126-132 | rule B: `find('PPP')` as the first cyclic start in 0..5, middle point outermost | `patternLit` 167-181 |
| 134-137 | unit when every pattern gives the same non-`None` literal | `unitOf` 210-213, `gen` 291-296 |
| 138-141 | conditional clauses `[-prem] + [l]` | `gen` 297-304 |
| 143-150 | nesting units and the conflict check | 305-316 |
| 151-153 | `is_false` | 317-321 |
| 156-160 | `L`, pivot, `Q`, fresh `F` per pivot | 322-333 |
| 161-165 | `fv` | inlined at 349-353 and 371-375 |
| 166-172 | `okpair` | 334-345 |
| 174-175 | base clauses `[F2(a,b), -l]` | 346-355 |
| 176-190 | extension and closing clauses | 356-379 |
| 191-194 | DIMACS output | Emit.lean `pushClause` 26-30, `body` 32-33, `header` 35-36 |
| — (mkcubes.py:11-15) | cube layout | Emit.lean `cubeTail` 38-40, `cubeUnits` 42-55, `main` 82-131 |
| 195-200 | `.map.json` and summary line | summary line only (Emit.lean `summary` 56-61); the map file is not ported |

## Trust: what the tests check and what stays trusted

- **The object of the theorems is `encB`, and the emitter prints `encB`.** In the `twin-*` modes the exe computes
  `encode m K t`, whose fields are `encB m K t` and `numVars m K t` by definition. It prints the base as
  `header numVars (length) ++ bodyL encB`, and each cube `c` of `cubes64` as
  `header numVars (length (cubeCnf encB c)) ++ bodyL (cubeCnf encB c)` (`cubeBody_eq`). Since the package has
  none of the escapes listed above, the compiled program is the definition the kernel reduces. That holds up to the
  Lean compiler and core's runtime code for `Array`, `List`, `String` and `IO.FS` (trust item E4 of `DESIGN.md`
  §1.4). The kernel and Python agree on (3,4,1), (3,4,2), (6,4,1) and (4,5,1) for `encB`; for `gen` on the M1
  instances (3,4,1), (3,4,2) and (4,4,2), and on (4,5,1).
- **The text rendering is unverified and trusted** (named under E3/E4 in `DESIGN.md` §1.4):
  - `pushClause` (Emit.lean:43-47), `bodyL` (:73), `header` (:52);
  - the file assembly in `twinMain` (Emit.lean:138-243);
  - core's `toString` on `Int` and `Nat`.

  `twin-check` (b, f above) now compares `encB` with `gen` as values, so a renderer bug would have to produce the
  right bytes from the right list. That is still not excluded for the trust path (E1), since only the renderer
  turns `encB 6 8 11` into the hashed bytes. It would be closed by a proved round trip
  `parseDimacs (render F) = F` (not done; optional in M9).
- **`allCodes` order = Python's `new()` order is tested, not proved.** Soundness does not need it (D4):
  `dimacsSat_of_holds` holds for any duplicate-free or duplicate-containing code list, and the numbering only has
  to make the hashes match.
- **The cube variables.** The cover theorem holds for any six nonzero variables. That `cubeVars64` are Y12 Y13 Y14
  Y23 Y24 Y34 in `encB 6 8 11` matters only for the reading of the cubes. It is checked by compiled code in the
  emission run and by the hashes of the c- and n-cube files against the records.

## What is NOT yet proved

- **The meaning of the clauses.** No theorem relates the clauses of `genCoded` to orientations, ψ-orders or chains.
  The missing pieces are:
  - `encB_satisfiable : Model m K t → DimacsSatisfiable (encB m K t)` (M3, Std-only, can start now). It is to be
    proved through `dimacsSatisfiable_of_holds` with `τ := M.τ` (`DESIGN.md` §2.3; `.other _ ↦ False`);
  - the geometric side, labelling and `modelOfLabelling` (M4–M6, Mathlib, after the campaign cutoff 2026-11-16
    17:00);
  - the assembly `sixfold_es8` (M8);
  - the hash binding of all 64 cubes (M9; 8 of 65 files are bound so far: base and 7 cubes, in (e)).
- **No equality between `encB`, `gen` and gen_b2.py is proved.** It is tested:
  - by bytes on 225 + 4 instances and 7 cubes (the M2 review checked 7 more cubes in its own emission);
  - as Lean values on 229 instances;
  - by kernel evaluation on 4 tiny instances.
- **Three lemmas that M3 needs first** (found by the M2 review; not M2 defects, nothing in M2 depends on them):
  - `dedupBy` keeps only input elements: `x ∈ dedupBy key S l → x ∈ l`. M2 proved only that nothing is lost
    (`mem_dedup_foldl`). M3 needs it so that each `c ∈ orbList` is `canon` of a triple of three distinct valid
    labels.
  - `canon` keeps triples valid: `canon` of three distinct valid labels gives three distinct valid labels, so that
    `orbCode m t c` decodes to `.orb c` (via `decodeCode_code`).
  - Every literal of `genCoded` is `±(v.code m K t)` for a `v` with `v.Valid m K t`. Today this is checked only by
    compiled code (`codesDecode`, true at (6,8,9), (7,8,9), (7,8,10) and (6,8,11)) and by the kernel at (3,4,2)
    (`codesDecode_3_4_2`).
- **The DIMACS round trip** (see Trust above) is not proved.
- **n-cube verdicts.** The c6upper-noty12 run's `run.log` says at 15:40:35: "32 of 32 NOT-Y(1,2) cube proofs
  accepted by cake_lpr, hash-bound (results.tsv)". This was only read. Its post-run gate `verify_final64.py` has
  no log yet, and this step did not run it. Variant A of `DESIGN.md` needs that gate.
- **m = 7** (sevenfold) is ported for byte identity only. Its soundness is out of scope (`DESIGN.md` §1.3).

## M1 review fixes applied (2026-11-06, about 15:00 KST)

All four issues of the review were checked against the files, found real, and fixed:

1. **Stale Gen line numbers in `DESIGN.md`.** All 21 `Gen:` citations had drifted. 19 were two lines low and two
   (Gen:33-34 and Gen:25-28) had shifted less. Each was re-read against the current Gen.lean and corrected
   individually: `gen` 240-380, `patternLit` 142-181, `canon` 103-109, `unitOf` 210-213, key test 155, `Pt` 42,
   and so on. The PPP-failure branch is now cited at Gen:170. A revision note at the top of `DESIGN.md` names the
   Gen.lean hash the citations refer to.
2. **The trust list now names the emitter's text rendering.** `DESIGN.md` E3 and E4 list Emit.lean:26-40, `main`
   (:82-131) and core's `toString`, with the round trip as the optional way to remove them. This README says the
   same. Appendix A item 8 wrongly called `pushClause` Gen's; it now cites Emit.lean.
3. **Chain-variable code collision for tiny K.** In `DESIGN.md` §3.1 the code is now
   `fBase + ((piv·FL + l)·N + ptCode a)·N + ptCode b` with `FL = max (K−1) 3`, matching Gen's `FL` (Gen:325).
   The levels that occur satisfy l < FL for every K, including K ≤ 2, where F₂ exists. The `decodeCode` row now
   states the level bound and needs no hypothesis on K. (Gen itself was already safe: its `F` table is per pivot
   and sized `FL·N²`.)
4. **Minor points.**
   - The `sixfold66_of_unsat` sketch now passes both side conditions, `(by decide) (by decide)` for `heven` and
     `hm`. It also uses the name `modelOfLabelling` of §2.4 consistently, in D5 and the §2.4 heading too.
   - M9 now says to emit from the Lean list `cubes64`, not from `cubeUnits`, and to read recorded hashes from
     files.
   - `check_recorded.sh` no longer hard-codes any hash. It reads each one from its record file and requires it to
     equal a second record, otherwise it reports RECORD-ERROR. A negative test with missing records exits 1. The
     (7,8,9) record is labelled as not independent.

No Lean source changed in this step: Gen.lean `ec97b335…`, Emit.lean `7cdd3f1c…` and KernelCheck.lean `6a141b39…`
are the same as in M1, and the exe hash is unchanged. `scripts/audit.sh` and the logs `build.log`, `ref_regen.log`
and `audit.log` are new.
