# Shard plan: closing sub-case (ii) through the hull-pair split

Everything is deterministic except where a wall-clock timeout is named. For a reproducible
tree, replace `-t <sec>` with CaDiCaL's conflict limit `-c <n>`. On this VM, 1M conflicts was
roughly 300–700 s.

## 0. Inputs and generator

- Branch `es7-cloud`, generator scripts in `results/Mii-S/scripts/` (commit: see
  `README.md`, "Generator commit").
- Base CNF: `results/C/scripts/make_cnfs.sh OUT` → `OUT/m33k7int.sub.cnf`, which must have
  sha256 `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`. This is the same file
  that H3's `lake exe mir_dimacs interior 33 7` writes.
- Tools: CaDiCaL 3.0.1 (c6073042), march_cu (CnC 705b60c6, `-fcommon`), cake_lpr (a36874a8,
  `cake_lpr.S` sha256 `2f3af32d…72b7d4a`). The patched lrat-check is only an optional second checker.
- Case cubes: `python3 scripts/hullsplit.py cubes cases.icnf cases.json` gives 450 lines, sha256
  `6b6f0946245da5cb33f287a0484c5ce7ef022bc26452a949848704018e6db742` (committed as
  `cases.icnf`). Each case CNF is `python3 scripts/hullsplit.py case F U L OUT`, i.e. `F` plus
  the cube's units appended in the order of the cube line. Its sha256 is in `cases.jsonl`.
  The Lean-side meaning is H3's `cubeCnf F cube`.

## 1. Cover certificates (done here, 122 obligations)

`scripts/cover.py list` lists `root` and `up:U` for 121 upper chains U. Each obligation is
`python3 scripts/cover.py cnf F OB OUT.cnf`, solved by `cadical --lrat --binary=false`
and checked with `cake_lpr OUT.cnf proof`. All 122 are **UNSAT, cake_lpr VERIFIED**
(`cover_lrat.jsonl`: 503 s CaDiCaL and 222 s cake_lpr in total, 1.0 GB of proofs, largest
obligation `up:` at 206 s). Re-running them is optional: about 0.2 core-hours.

If a case is later split by layers (section 3b), each expanded node P also needs its
`cover2.py list P` obligations, about 107 per node. For P = `8/` and `/7` (214 obligations)
this took about 10–60 s per obligation.

## 2. The 450 case CNFs: status after this run

See `cases.jsonl`, one line per case: sha256, status, times, estimate.

| group | cases | status |
|---|---|---|
| closed by plain CaDiCaL (≤ 10 s each) | 172 | UNSAT, cake_lpr VERIFIED |
| further closed here | see README | UNSAT, cake_lpr VERIFIED |
| open, hull a 6-gon (two extra pairs) | 248 → see README | estimated below |
| open, hull a 4-gon (one extra pair) | 28 → see README | estimated below |

## 3. Per-case procedure (what each machine runs)

For a case CNF `C` (from `hullsplit.py case`):

a. **Cube-and-conquer, the default** (the Mi recipe that closed sub-case (i)):
   ```
   march_cu C -d 7 -o top.icnf          # 128 cubes; refuted leaves are written too
   for each cube c:  C+c  ->  cadical --lrat --binary=false -t 300  ->  cake_lpr
   on timeout:       march_cu C+c -d 6  -> 64 children c+s, recurse
   ```
   `scripts/close_march.py C OUT --depth 7 --timeout 300 --split-depth 6 --jobs <cores>`
   does exactly this. It writes `OUT/leaves.jsonl` and `OUT/leaves.icnf` (the closed
   leaves). Completion is checked with H3's `lake exe cover_check OUT/leaves.icnf`, which must
   print `s COVERED`. `scripts/covercheck.py` is an unverified Python port for quick checks.
   The 6-gon cases are smaller, so `-d 5` is enough to start.
b. **Layer split, optional.** `scripts/layers.py next SPEC` gives the next convex layer, and
   `cover2.py` gives the certified cover of that step. It pays off only when the next layer is
   a 6-gon. The children whose next layer is again a 4-gon (one pair, no axis vertex) timed out
   at 60 s in 10/10 tries under `/7`, so the 4-gon chains recur. Use it only for cases whose
   probes favour it.

## 4. Expected cost (core-hours, this VM's speed)

See the estimate table in `README.md`, which draws on `est_one.jsonl`, `est_two.jsonl`,
`probes.jsonl` and `cases.jsonl`. Assign cases to N machines by longest-processing-time on the
estimate. The 4-gon cases go first and get the most cores, because their spread is largest.

## 5. Composing the certificate

The goal is `¬DimacsSatisfiable (Mir.interiorCnf 33 7)`, the `h2` of
`Mir.mirrorExclusionLine_of_unsat`.

1. Lean extension, small and not yet written. It needs a clause-cover lemma next to
   `not_dimacsSatisfiable_of_cover` in `results/H3/MirrorEncoding/Cover.lean`:
   ```lean
   /-- Blocking-clause cover: if F ∧ P ∧ (no cube of `cubes` holds) is UNSAT and every
   F ∧ c (c ∈ cubes) is UNSAT, then F ∧ P is UNSAT. -/
   theorem not_dimacsSatisfiable_of_blocked {F : List (List ℤ)} {P : List ℤ} {cubes : List (List ℤ)}
       (h0 : ∀ c ∈ cubes, ∀ z ∈ c, z ≠ 0)
       (hb : ¬DimacsSatisfiable (cubeCnf F P ++ cubes.map (List.map (fun z => -z))))
       (hc : ∀ c ∈ cubes, ¬DimacsSatisfiable (cubeCnf F c)) :
       ¬DimacsSatisfiable (cubeCnf F P)
   ```
   Proof: let ν satisfy `cubeCnf F P`. If some c ∈ cubes holds under ν, then ν satisfies
   `cubeCnf F c`, contradicting hc. Otherwise every c has a false literal z, so `-z` holds
   (`litSat_neg`, using h0), and ν satisfies every blocking clause, contradicting hb. With
   `P = []`, `cubeCnf F [] = F` up to `++ []`.
2. Data:
   - `root` (P = [], cubes = UP(U) for 121 U);
   - `up:U` (P = UP(U), cubes = cube(U,L));
   - per case either a direct cake_lpr refutation of `cubeCnf F cube(U,L)`, or a march leaf list
     for which `coverCheck` holds, with one cake_lpr refutation of
     `cubeCnf (cubeCnf F cube) leaf` per leaf (`not_dimacsSatisfiable_of_coverCheck` with F
     replaced by `cubeCnf F cube`).
3. Chain: per case gives `¬Sat (cubeCnf F cube(U,L))`. `up:U` with
   `not_dimacsSatisfiable_of_blocked` gives `¬Sat (cubeCnf F UP(U))`, and `root` gives
   `¬Sat F`.
4. Trust base: the same as H3's (cake_lpr, the unit/clause appending in the scripts, Lean's
   `coverCheck` binary). The Python generators (`hullsplit.py`, `cover.py`, `layers.py`) are
   **not trusted**. A wrong cube only makes some obligation SAT, or leaves it unprovable. The
   geometric argument (`soundness.md`) explains why the obligations are UNSAT. It is not
   needed for soundness.
5. File order. `check_cubes.sh` appends cube units after F. The blocking CNFs are F, then P's
   units, then the blocking clauses (`cover.py cnf`). That is `cubeCnf F P ++ blocks`, the
   order in `hb`.
