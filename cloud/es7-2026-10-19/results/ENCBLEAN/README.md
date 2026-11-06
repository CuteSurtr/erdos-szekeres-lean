# ENCBLEAN: encoder B in Lean (M0 design and M1 byte-identical port)

`EncB.gen m K t` is a Lean definition of the CNF that `C6UPPER/encb/gen_b2.py m K t` writes (gen_b2.py SHA-256
`3d47459a9723b5f7344205f3f2d7463e0be00b41c5070155e5da8dbf78fd40ba`). It has the same variable numbering, clause
order and literal order as Python, for both even and odd m. `lake exe encb_dimacs` prints it in gen_b2.py's DIMACS
layout, and prints cubes in the layout of `C6UPPER/tools/mkcubes.py`.

**Status (2026-11-06, 15:00 KST).**
- **M0 and M1 are done:** the design is in `DESIGN.md`, and the byte-identical port is built and tested.
- **Nothing about what the clauses mean is proved yet.** That is M2 to M9 of `DESIGN.md`; see "What is NOT yet
  proved" below.
- The package is Std-only: it has no `[[require]]` and no Mathlib, and it uses `leanprover/lean4:v4.24.0` (Lean
  4.24.0, commit `797c613e`), the repository's toolchain.
- It contains no `sorry`, `admit`, `native_decide`, `implemented_by`, `extern`, `unsafe`, `partial`, `axiom` or
  `opaque` (`scripts/audit.sh`).
- No git commit was made.

## What exists

| file | content |
|---|---|
| `DESIGN.md` | M0: target theorem (variant A: 64 cubes on Y12 Y13 Y14 Y23 Y24 Y34, no Y(1,2) assumption), trust list E1–E6, interfaces (`Model`, `PolarLabelling`), lemma map with file:line sources, milestones M0–M9 (M7 dropped), risks |
| `EncB/Gen.lean` | the port: helpers (`canon`, `olit`, `permSign`, itertools orders), `patternLit`, `angOuts`, `gen` (Gen.lean SHA-256 `ec97b335…`) |
| `EncB/Emit.lean` | DIMACS and cube text rendering, plus `main` for `encb_dimacs` |
| `EncB/KernelCheck.lean` | `decide +kernel`: the **kernel** evaluates `gen` on (3,4,1), (3,4,2) (odd m) and (4,4,2) (even m) to the clause lists gen_b2.py writes. Axiom audit by `#guard_msgs`: `gen` and `gen_4_4_2` use only `propext` |
| `ref/make_ref.py` | checks gen_b2.py's hash, runs it on the 225-instance grid and writes `ref/hashes.tsv` |
| `ref/hashes.tsv` | the reference corpus: m K t, status (OK or FAIL:exception), SHA-256, bytes, nv, ncl, the counts, seconds |
| `scripts/compare_b.sh` | emits every corpus instance with the exe and compares SHA-256 values. A row where Python raised must make the exe refuse (exit 1, no output) |
| `scripts/check_recorded.sh` | the recorded instances. `small`: (6,8,9), (7,8,9) and (7,8,10), streamed into sha256sum. `big`: one generation of (6,8,11), written as base + 7 cubes to a scratch directory, hashed, deleted. The recorded hashes are read from the record files and cross-checked against a second record (see below) |
| `scripts/audit.sh` | static check: forbidden tokens (comments stripped), no Mathlib, toolchain |
| `logs/` | `build.log`, `compare_tiny.log`, `ref_regen.log`, `check_recorded_small.log`, `check_recorded_big.log`, `audit.log`, `env.txt` (exe and source hashes) |

Sizes in lines: Gen.lean 382, Emit.lean 132, KernelCheck.lean 35, make_ref.py 80, compare_b.sh 26,
check_recorded.sh 79, audit.sh 25, DESIGN.md 611.

## How to build and run

Every compile and Python run goes at nice 10, one at a time, inside an 8 GB scope. `lake build` is run only in this
directory.

```
cd cloud/es7-2026-10-19/results/ENCBLEAN
export PATH=$HOME/.elan/bin:$PATH
CAP="systemd-run --user --scope -q -p MemoryMax=8G -p MemorySwapMax=0 nice -n 10"
$CAP lake build                                  # clean: 14 s wall, 2.1 GB peak (KernelCheck 12 s)
$CAP scripts/audit.sh
$CAP python3 ref/make_ref.py OUT.tsv             # 59 s; regenerates the corpus from gen_b2.py
$CAP scripts/compare_b.sh                        # 29 s; the 225 grid instances
$CAP scripts/check_recorded.sh SCRATCH small     # 15 s; (6,8,9), (7,8,9), (7,8,10)
$CAP scripts/check_recorded.sh SCRATCH big       # 7 s; (6,8,11) once, ~470 MB transient in SCRATCH, deleted
```

How to call the exe:

```
.lake/build/bin/encb_dimacs base 6 8 11 > B.cnf                       # base CNF
.lake/build/bin/encb_dimacs cube 6 8 11 1 2 3 -10 11 18 > c.cnf       # base + unit clauses (mkcubes layout)
.lake/build/bin/encb_dimacs files 6 8 11 DIR base full_Y12 c11011 n00000   # one generation, several files
.lake/build/bin/encb_dimacs stats 6 8 11                              # summary line only (stderr)
```

- **Cube names.** `cBBBBB` is the cube with units Y12 followed by the pattern on Y13 Y14 Y23 Y24 Y34, where bit 1
  means a positive literal; these are mkcubes' 32 cubes. `nBBBBB` is the same pattern with −Y12 first; these are
  the not-Y(1,2) cubes of the c6upper-noty12 run.
- **Variable numbers.** At t = 11 these are variables 1, 2, 3, 10, 11 and 18.
- **Refusal.** On an instance where gen_b2.py raises, the exe writes nothing and exits with 1.

## Comparison results (rerun 2026-11-06, 14:57–14:59 KST)

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

## How the port mirrors gen_b2.py

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

- **The compiled code.** The exe runs `EncB.gen` compiled. Since the package has none of the escapes listed
  above, the compiled program is the definition the kernel reduces, up to the Lean compiler and core's runtime
  code for `Array`, `List`, `String` and `IO.FS` (trust item E4 of `DESIGN.md` §1.4). `KernelCheck.lean` shows that
  the kernel and gen_b2.py agree on three tiny instances. The interpreter check of the review shows the same for
  (6,8,5), (7,8,4) and (4,4,2).
- **The text rendering is unverified and trusted** (named under E3/E4 in `DESIGN.md` §1.4):
  - `pushClause` (Emit.lean:26-30), `body` (:32-33), `header` (:35-36) and `cubeTail` (:38-40);
  - the header counts and file assembly in `main` (:82-131);
  - core's `toString` on `Int` and `Nat`.

  Byte equality with gen_b2.py checks this code against Python, but it cannot exclude a printing bug that cancels a
  matching bug in `gen`. That would only be closed by a proved round trip `parseDimacs (render F) = F` (not done;
  optional in M2/M9).
- **Cubes.** `cubeUnits` (Emit.lean:42-55) builds the units from names. In M9 the cubes are to be emitted from the
  Lean list `cubes64` of the theorem instead (`DESIGN.md` M9).

## What is NOT yet proved

- **The meaning of the clauses.** No theorem relates the clauses of `gen` (or the planned functional twin `encB`)
  to orientations, ψ-orders or chains. The missing pieces are:
  - the functional twin with closed-form variable codes and the numbering bridge (M2);
  - `encB_satisfiable : Model m K t → DimacsSatisfiable (encB m K t)` (M3);
  - the geometric side, labelling and `modelOfLabelling` (M4–M6, Mathlib, after the campaign cutoff 2026-11-16 17:00);
  - the assembly `sixfold_es8` (M8);
  - the hash binding of all 64 cubes (M9).
- **No equality between `gen` and gen_b2.py is proved.** It is tested: by bytes on 225 + 4 instances and 7
  cubes, and by kernel evaluation on 3 tiny instances.
- **The DIMACS round trip** (see Trust above) is not proved.
- **The cover of the 64 sign patterns** (`covers_signPatterns`) is not proved yet (M2).
- **Verdicts on the 32 n-cubes** are not available yet. The c6upper-noty12 run is in progress (8 of 32 ACCEPTED at
  14:43). Variant A of `DESIGN.md` needs all 32; otherwise it falls back to variant B, which needs reflection (M7′).
- **m = 7** (sevenfold) is ported only for byte identity. Its soundness is out of scope (`DESIGN.md` §1.3).

## Review fixes applied (2026-11-06, about 15:00 KST)

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
