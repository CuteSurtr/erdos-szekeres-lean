# VERIFY v182-lean (statement-fidelity lens): all five theorems and the hash binding confirmed

**Reviewer.** I am an independent statement-fidelity reviewer in slot lrv3. I wrote this on 22 Nov 2026 at about
19:10 KST. I re-proved nothing; recompiling the worker's sources does re-check its proofs in the kernel. My own code is:
- `Audit.lean`: the elaborated statements, the unfolded definitions and `#print axioms`;
- `Sanity.lean`: the non-vacuity theorems;
- `tools/compile_review.sh`: the rebuild from source and the exe reproduction;
- `tools/hashcheck.py`: the hash binding.

I ran none of the worker's scripts and imported none of its code. I compiled its Lean sources only as copies, after
checking each copy against its manifest.

| key | worker's claim | verdict | why the claim holds |
|---|---|---|---|
| `V182Geo.rainbowColorable_six` | Lean-checked, no hypothesis | **confirmed** | The type is `RainbowColorable 6`, exactly "G has a rainbow edge colouring with at most 6 colours". Axioms: [propext, Classical.choice, Quot.sound], from my own rebuild. |
| `V182Geo.not_rainbowColorable_five` | Lean-checked modulo PieceVerdicts and E1-E6 | **confirmed** | The type is `PieceVerdicts → ¬RainbowColorable 5`. The hypothesis says exactly that the 4,404 listed CNFs are unsatisfiable (`sanity_pv_iff`). Those CNFs are byte for byte the certified files (§2). Axioms: the same three. |
| `V182Geo.chiRainbow_eq_six` | the same | **confirmed** | The type is `PieceVerdicts → chiRainbow = 6`, with `chiRainbow = sInf {k \| RainbowColorable k}`. Axioms: the same three. |
| `V182Geo.chiRainbow_eq_six'` | the same, with the hypothesis unfolded | **confirmed** | The hypothesis is `PieceVerdicts` verbatim (`sanity_pv_unfold`, by `rfl`). Axioms: the same three. |
| `V182Geo.pieces_shape` | kernel check, no axioms | **confirmed** | The type says 4,404 pieces, 84 of them direct, and `splitSet` has 36 distinct entries, all below 120. It depends on no axioms. |
| M9 hash binding (E1) | COMPUTED, 4,404/4,404 | **confirmed** | My own code also gets 4,404/4,404, and my hashes equal the worker's. The exe that printed the bytes is reproduced from source byte for byte. |

**Label.** The labels stay as the worker gave them; nothing is rounded up.
- `rainbowColorable_six` is **Lean-checked**.
- `not_rainbowColorable_five`, `chiRainbow_eq_six` and `chiRainbow_eq_six'` are **Lean-checked modulo PieceVerdicts**
  (the 4,404 cake_lpr verdicts) **and trust items E1-E6**.
  - E1 rests on COMPUTED hash comparisons: the worker's M9 and this review.
  - E2-E6 are trusted.

## 1. Check 1: the Lean statement says the intended statement

The intended statement (task text; wave-1 README §2, A2) is about the graph G. Its vertices are the 3-, 4- and 5-subsets
of {0..7}, and its edges are the inclusions between consecutive sizes. G has no edge colouring with at most 5 colours in
which every 4-cycle subgraph is rainbow (colourings need not be proper), and chi_rainbow(G) = 6.

I unfolded each definition as it was elaborated, from the `Audit.lean` output in `logs/compile_review.log`:
- `V = {s : Finset (Fin 8) // 3 ≤ s.card ∧ s.card ≤ 5}`. These are the 3-, 4- and 5-subsets of {0..7}.
- `Adj u v = (u ⊆ v ∧ |v| = |u| + 1) ∨ (v ⊆ u ∧ |u| = |v| + 1)`, and `G = {Adj := Adj, …}`. These are exactly the
  inclusions between consecutive sizes, not the comparability graph.
- `IsFourCycle a b c d` has six distinctness fields and `a~b`, `b~c`, `c~d`, `d~a`. This is a 4-cycle subgraph, and the
  definition allows chords.
- `IsRainbow col` holds for `col : G.edgeSet → α` when, for every `IsFourCycle a b c d`, the list
  `[col s(a,b), col s(b,c), col s(c,d), col s(d,a)]` is `Nodup`. The colours are on unordered edges, and properness is
  not required.
- `RainbowColorable k = ∃ col : G.edgeSet → Fin k, IsRainbow col` means "at most k colours".
  `chiRainbow = sInf {k | RainbowColorable k}`. That set is nonempty, because `rainbowColorable_six` proves 6 is in it.

The theorem types (`#check`) carry no other hypothesis:
- `rainbowColorable_six : RainbowColorable 6`
- `not_rainbowColorable_five : PieceVerdicts → ¬RainbowColorable 5`
- `chiRainbow_eq_six : PieceVerdicts → chiRainbow = 6`

There is no weakening, and no hidden assumption. My own grep, which is wider than the worker's `audit.sh`, covered the
15 sources and the five ENCBLEAN modules in the closure. It found no command `variable`, `set_option`, `macro`,
`elab`, `syntax`, `notation`, `run_cmd`, `initialize`, `axiom`, `opaque`, `unsafe` or `partial`. It also found no
`sorry`, `admit`, `native_decide`, `implemented_by`, `@[extern]`, `import Lean` or `skipKernelTC`. The only matches
are three mentions inside ENCBLEAN doc comments (`Render.lean:15`, `:118`, `Gen.lean:35`).

The counts 182, 560 and 560 are not theorems. The statement does not need them.

## 2. Check 2: the verdict hypothesis names Lean CNFs bound by hash to the certified files

The hypothesis is defined as:

`PieceVerdicts = ∀ q ∈ pieces, ∀ nv F, EncB.parseDimacs (pieceText q) = some (nv, F) → ¬EncB.DimacsSatisfiable F`

Its parts:
- `pieceText q = EncB.renderCube nVars baseCnf (EncB.bodyR baseCnf) (pieceCube q)`. This is a Lean definition in
  `V182Enc/Gen.lean`, Std-only.
- `pieces`, `pieceCube`, `starUnits`, `perms5`, `y1Star`, `y2Star`, `splitSet`, `baseCnf`, `nVars` and `lit` are as
  printed in the audit.
- `DimacsSat` is the usual clause semantics over `ν : ℕ → Bool`, and a 0 literal is never true.

**Which exe produced the bytes, and is it frozen?**
- `v182print all DIR` writes `pieceText q` for each `q in pieces` to `DIR/i.cnf`, and `piece I` writes
  `pieceText pieces[I]` (`Main.lean:47-55`, `36-40`).
- The M9 run used `build/bin/v182print`, sha256 b0b270cb5840bb92151900b77eb76ff8be1b71efd3dee93dbfe198ed6a531c5d, as
  `exe_sha256` in `logs/m9_hash_binding.summary.json` records.
- That exe is frozen:
  - `Gen.lean` (6d03f39a…) and `Main.lean` (e418a316…) are unchanged since the M9 freeze file
    (`logs/m9_freeze.sha256`, 18:05);
  - all 46 entries of `logs/final_manifest.sha256` still match;
  - the exe has the same sha256 at the start and at the end of my run.
- The exe is reproduced from source. My unit did three things:
  1. compiled ENCBLEAN's `Gen`, `Dimacs`, `Coded`, `Cover` and `Render` from copies whose sha256 equals the git HEAD
     blobs;
  2. compiled all 15 v182 modules from copies equal to the manifest;
  3. relinked the printer from **my own** IR C only.

  The result is **byte-identical to b0b270cb…** (`EXE_REPRODUCES_FROZEN`). In addition:
  - my `Gen.c` and `Main.c` equal the M9 build's;
  - my five ENCBLEAN oleans and IR C equal the record's `.lake` files;
  - my 15 v182 oleans equal the worker's `build_clean/` (15 of 15 `OLEAN_SAME_AS_WORKER`).

  So the exe that printed the bytes, and the oleans the theorems live in, both come from the same `Gen.lean`.

**My own hash binding** (`tools/hashcheck.py`, run in the unit; `logs/hashcheck.summary.json`, per-piece
`logs/hashcheck.tsv`; ALL_OK true):
- `v182print list` gives 4,404 pieces. That list equals my own reading of the `pieces` definition (for `n < 120`: all
  120 `(n, some m)` if `n ∈ splitSet`, else `(n, none)`).
- `v182print base` gives sha c3ae5224…7074. That equals B, and equals `a2/g182_k5_st_sb2.cnf` on disk.
- `v182print all` wrote exactly the 4,404 files `0.cnf` to `4403.cnf`. For **every** piece the printed SHA-256 equals:
  - the one campaign `certify.jsonl` row of that cube, which has the verdict `s VERIFIED UNSAT` exactly and `cnf`
    equal to the cube's path;
  - the SHA-256 of that CNF file on disk.

  In addition, for every piece:
  - the campaign cake output has the exact line;
  - at least one independent cake_lpr re-run carries the same CNF sha, the campaign's LRAT sha, the exact verdict, and
    the exact line in its stored output. That is the wave-1 verifier for 1,623 pieces, and both the recheck and the
    rebuild lens for 2,781 pieces.
- Result: 4,404/4,404. All 4,404 printed hashes are distinct and equal to the worker's M9 TSV.
- Controls, each of which failed as intended:
  - a printed hash with one hex digit changed;
  - piece 0's hash checked against piece 1's record;
  - the unlisted cube (36, -): its row is the CaDiCaL timeout, with no verdict line and no re-run.
- At reading level, the last lines of `cubesY1/cube000.cnf` (26 217 253 289 325), of `cubes036Y2/cube000.cnf`
  (27 219 251 288 325 66 222 373 409 445) and of B (16 62 228 634 1440 161 127 95 58 24) equal my hand evaluation of
  `pieceCube` and `unitPairs`. The header counts are 23,535, 23,540 and 23,530.
- cake_lpr on this machine has sha256 c14ff498…8a54, as DESIGN §4 and the recheck record name it.

## 3. Check 3: the hypotheses are not vacuous

- `sanity_pv_iff` (Lean, in `Sanity.lean`):
  `PieceVerdicts ↔ ∀ q ∈ pieces, ¬DimacsSatisfiable (cubeCnf baseCnf (pieceCube q))`.
  - The parse antecedent holds for every piece (`EncB.parseDimacs_renderCube` with the literal bounds), so a parse
    failure cannot discharge the hypothesis.
  - It asserts exactly that the 4,404 listed CNFs are unsatisfiable. By §2 these are the certified files, so the
    hypothesis is precisely the certified facts (E1-E3), and nothing beyond them. No evidence says it is false.
- `sanity_not_three : ¬RainbowColorable 3` uses the kernel-checked 4-cycle `cycXY`. So rainbowness is a real
  constraint: G has 4-cycle subgraphs, and the condition is not satisfied trivially.
- `rainbowColorable_six` shows the condition can be met, so the conclusion is not degenerate either.
- The six-colour half has no hypothesis at all.

## 4. Check 4: axioms (one compile unit, slot lrv3)

The compile ran as unit `esr-ag-lrv3-v182a`, 19:00:44 to 19:02:39 KST (1 min 54 s; CPU 1 min 51 s).
- Peak memory: systemd reports 1.4G for the unit, with no swap. The largest maximum RSS was 2.12 GB, for `Norm`, which
  is 61 % of the 3500M MemoryMax.
- Gate: no YIELD, Tctl 79 C, agent-pool anon 391 MB, no active lrv3 unit, and `cpu_free.sh` showed 1 free thread.

These axiom lists come from `#print axioms` on the oleans I rebuilt from source:
- `chiRainbow_eq_six`, `chiRainbow_eq_six'`, `not_rainbowColorable_five` and `rainbowColorable_six`:
  **[propext, Classical.choice, Quot.sound]**.
- `pieces_shape`: **no axioms**.
- The path lemmas (`normalize`, `norm_finite`, `exists_piece`, `no_normal_colouring`, `baseCnf_sat`, `baseCnf_wf`,
  `piece_unsat`, `cyc_bridge`, `conflict_ne`, `col6_rainbow`, `chiRainbow_eq_six_of`) use subsets of the same three.
  - `walk_all`, `walk_spec` and `EncB.parseDimacs_renderCube`: [propext, Quot.sound].
  - The controls `ctl_orig` and `ctl_mut`: [propext].
- The sanity theorems: the same three or fewer.

No `sorryAx`, `Lean.ofReduceBool` or `Lean.trustCompiler` appears anywhere.

## 5. Not covered here (trust items, unchanged)

- **E2:** I re-ran no cake_lpr verdict. The verdicts rest on the records: the campaign run plus one independent re-run
  for 1,623 pieces, and two for 2,781.
- **E3:** that cake_lpr reads each file as the clause list `EncB.parseDimacs` returns is trusted. This review adds no
  evidence for it. The files use only the plain subset: a header line, then single-space clause lines with no comments.
- **E4:** the Lean compiler and runtime of the printer.
- **E5:** the kernel, Mathlib (f897ebcf) and the definitions; §1 is my reading of the definitions.
- **E6:** SHA-256.
- Only the needed direction of the reduction is formalized. The converse "B SAT iff a colouring exists" is not, and
  the theorem does not need it.
- I did not check the provenance of the six-colour table. That does not matter, because the kernel checks the
  colouring itself.

## 6. Fixes

- **Required:** none.
- **Suggestion (non-blocking):** add `set_option|run_cmd|elab|macro|initialize|import Lean` to the worker's
  `tools/audit.sh` pattern, so that `set_option debug.skipKernelTC` or meta-level code would be caught. None is present
  now (my grep in §1).

## 7. What I ran, and incidents

- **Units:** one unit, `esr-ag-lrv3-v182a`, ran `tools/review_unit.sh`, which is `compile_review.sh` followed by
  `hashcheck.py`. I started it through `tools/launch.sh`, which runs `tools/gate.sh` first.
- **Foreground:** all read-only and short:
  - file reads and greps, and `sha256sum` of a few files (including cake_lpr);
  - read-only `git show HEAD:…` and `git rev-parse` (Mathlib commit);
  - `systemctl --user show`/`list-units`, `sensors`, `df`, `free` and `cpu_free.sh`;
  - small Python one-liners: a `certify.jsonl` row count, a syntax check of `hashcheck.py`, and the edit of this
    directory's README.

  No compile and no exe run happened outside the unit.
- **Disk:** `tmp_hb/` (1.4 GB of printed pieces) was written and deleted inside the unit. `build/` (22 MB), `src/` and
  `encb_src/` are kept.
- **Shared slot:** the slot name lrv3 is also used by the reviewers of n66-level15 (`esr-ag-lrv3-e1`) and
  res118-rowblocks (`esr-ag-lrv3-rbx-bind`). I did not touch those units. To keep "one unit of the slot at a time", my
  gate waited until no `esr-ag-lrv3-*` unit was active, and also for `cpu_free.sh` to show at least 1 (the house cap
  of 28 threads). That took one 60-second poll.
- **Rule deviation, "ONE compile":** the task asked for one compile to re-run `#print axioms`. My single unit did
  more:
  - 22 `lean` invocations: 5 ENCBLEAN modules, 15 v182 modules, `Audit.lean` and `Sanity.lean`;
  - 7 `leanc` compiles and one link;
  - the printer runs `list`, `base`, `all` and `cube 36 -` inside `hashcheck.py`.

  It was still one unit on 1 thread, 1 min 54 s in all, peak RSS 2.12 GB. I did this so that the axiom audit runs on
  oleans built from the reviewed sources, and so that the exe is tied to them. It changes no verdict.

## 8. Files and SHA-256 (in this directory)

- `Audit.lean` e8b22671a2d4a6a4f081d982b7017af0f29502b574b4decad7b1c2fe4e937208
- `Sanity.lean` ddfd276879289601693ef7bd27b810c14fc5d6350ab9db7e2f5c88b2a29f119a
- `tools/compile_review.sh` f297feb869bd9166e36e3e8daa34deb592233ee563f4bb2d530444be102c1ff5
- `tools/hashcheck.py` a54b45c763c9f0e789443fbc710b06461a72a7fc705a8f9aeda1a0de858b12f4
- `tools/gate.sh` 6269929f…7601, `tools/launch.sh` 79d6e806…3799, `tools/review_unit.sh` 823d1030…b0a1
- `logs/compile_review.log` 0af55130…25d1, `logs/hashcheck.log` 10a17909…4aa4
- `logs/hashcheck.summary.json` 6f84f1b8…94ba
- `logs/hashcheck.tsv` c0bd12bd…c52a (4,404 rows, all ok)
- `build/bin/v182print` b0b270cb5840bb92151900b77eb76ff8be1b71efd3dee93dbfe198ed6a531c5d. This is my relink, and it
  equals the frozen exe.

To re-run (from this directory): `tools/launch.sh <job>`. It runs the gate, then one unit of about 2 minutes. The
compile log is `logs/compile_review.log` and the binding log is `logs/hashcheck.*`.
