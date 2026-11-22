# n66-level15 DESIGN (M0): the N66 relaxation encoder at level 15 (N66 ≤ 54)

Written 22 Nov 2026, 17:40-18:00 KST, by the `n66-level15` agent (slot l15). This is a **delta document** on top of
the level-14 design `formalize-20261122/n66enc/DESIGN.md`, copied here as `ref/DESIGN_level14.md`
(SHA-256 `e720a94708e3a44e39198e8a97d64551f6f6fd0d92c66b66f25c1756fd1431cd`, `ref/SHA256SUMS.level14`). Everything
not restated below is inherited unchanged; section numbers "L14 §x" refer to that file. Labels as in es-research §2.
[D] = checked on disk in this session; [R] = read from a record.

## 0. Target, label, method

```lean
-- N66E15 (Std-only), N66G15 (Mathlib side); all compiled in this directory
theorem N66G15.n66_bound_54_of_cubes (h : N66E15.CubesUnsat105) (hR : N66G15.RowsValid N66E15.R0_15) :
    OmissionZRow.N66Bound 54
-- axiom guard (End.lean, #guard_msgs): [propext, Classical.choice, Quot.sound]
```

- `CubesUnsat105 := ∀ c ∈ leaves105, ¬ EncB.DimacsSatisfiable (fullCnf R0_15 c)`, `leaves105 := tree15.leaves`.
- `RowsValid R0_15`: every one of the 10,859 row supports used by the 105 certified trims is left partly unoccupied by
  every configuration of the class (no 6-cap, no 6-cup, no convex octagon). `RowsValid` is a renamed copy of the
  level-14 definition (`N66G15.RowsValid`, not the constant `N66Geo.RowsValid`), and `R0_15` is a different row list
  from the level-14 `R0` (11,884 rows); neither implies the other.
- **Label (when M1 and M9 pass):** Lean-checked modulo `CubesUnsat105` (the 105 cake_lpr verdicts, carried in by
  `fullUnsat_of_text` and the M9 hash binding under trust items E1-E6) and the hypothesis `RowsValid R0_15`. Not
  "modulo the verdicts" alone (L14 D4, D5). Unrefereed; no label of the N66 record changes.
- **Method.** The level-14 sources (all 54 manifest entries verified unchanged before copying,
  `logs/n66enc_manifest_check.log`) were copied, the packages renamed (`N66Enc` → `N66E15`, `N66Geo` → `N66G15`,
  `CubesUnsat132` → `CubesUnsat105`, `leaves132` → `leaves105`, `tree14` → `tree15`, `R0` → `R0_15`,
  `n66_bound_55_*` → `n66_bound_54_*`, `N66Bound 55` → `N66Bound 54`), and only the level-dependent items of §2 were
  edited by hand. A `diff` against n66enc after the same renames shows exactly those edits (§7). Distinct package and
  namespace names let a later composition import level 14 and level 15 together.

## 1. Decisions (in addition to L14 D1-D10, which all carry over)

| # | decision | why |
|---|---|---|
| E15-1 | **Bind to `trim.cnf`** (L14 D1). At level 15 `cert.cnf` and `trim.lrat` are kept only zstd-packed (`c15_post.sh`, owner OK); `trim.cnf` is kept plain [D]. | The verdict hash is `trim_cnf_sha256` (campaign_status, cert.json, verify.json, vfy15 `trim_cnf_sha`). |
| E15-2 | **The activated quadruples are runtime data, not part of the Lean CNF.** `fullCnf` contains mono66's complete F6 + F8 (`quadStream` over every `okQuad` ordered quadruple, L14 D2/D3), so the level-15 warm set `p2/s15/q.json` enters only as the input of control M1(b). | Soundness never depends on which quadruples were activated; every activated set is a sub-list. The task text names the warm state; it is used where it matters (the byte-identity control). [D]: every leaf's `_L15.json` state has exactly 683,670 activated quadruples = the τ-closure of `q.json` (676,907). |
| E15-3 | **Same generator, same command line except `--L 15 --warm p2/s15/q.json`.** | [D] `p2c15_driver.py` launches `p2_batch_cube.py --L 15 --rows mono/rows_1832.json --warm p2/s15/q.json --seed 11 --tauclose --sb --cube …`; `cal15.sh` the same. Generator files hash-equal to the level-14 pins (§3). |
| E15-4 | **Fresh names, separate oleans.** The LEAN_PATH of this directory does not contain the n66enc olean store. | A stale import of a level-14 module fails loudly instead of resolving. |
| E15-5 | **Atom `cnt` widened to `Fin 16`** (s(a, j) for j = 1..15). | The level-14 `Fin 15` cannot hold j = 15. All atoms downstream of `Atom` are recompiled (hence the full copy instead of importing level-14 oleans). |

## 2. What changes from level 14 (the complete list)

| item | level 14 (n66enc) | level 15 (here) | where |
|---|---|---|---|
| counter bound | `kBound := 14` (≤ 14 of the 68 hole literals) | `kBound := 15` | Clauses.lean |
| counter aux atom | `cnt (a : Fin 68) (j : Fin 15)`, code `28532770 + 15a + j`, `sbe` base 28533790 | `cnt (a : Fin 68) (j : Fin 16)`, code `28532770 + 16a + j`, `sbe` base 28533858 | Atoms.lean, DecodeA.lean (`ofCode_code` cases) |
| `sAux a j` | `cnt ⟨a % 68⟩ ⟨j % 15⟩` | `cnt ⟨a % 68⟩ ⟨j % 16⟩` | Clauses.lean |
| header variables | `nvHeader := 1647808` | `nvHeader := 1647847` (= mono_top 1,647,026 + 795 counter aux + 26 SB aux) [D layout.json, verify.json] | Alloc.lean |
| split tree | `tree14` (200 nodes, 132 leaves) | `tree15`: 146 campaign cubes (64 depth-0, 41 split, 105 certified leaves) + the 63 implicit base nodes; re-split states 40 (13×), 52 (12), 46 (10), 44 (4), 45, 39 [D] | Cover.lean, `data/tree15.txt` (`tools/mk_data15.py`) |
| rows | `R0` = 11,884 used supports | `R0_15` = 10,859 used supports (union of the 105 trims' row clauses = union of their `used_rows.json`), `data/rows_used15.txt` sha256 `f45e25f1…af2f0511` | Rows.lean |
| hole bound | `holes_le : 56 ≤ M.n → M.holes ≤ 14`; `holds_card : M.holes ≤ 14 → …` | `holes_le : 55 ≤ M.n → M.holes ≤ 15`; `holds_card : M.holes ≤ 15 → …` (same proofs, constants changed) | Small.lean, Tail.lean, Assembly.lean (`Gaps.holes`, `55 ≤ n`) |
| leaf count | `leaves132_length = 132` | `leaves105_length = 105` (kernel) | Facts.lean |
| end statement | `N66Bound 55` from `CubesUnsat132`, `RowsValid R0` | `N66Bound 54` from `CubesUnsat105`, `RowsValid R0_15` | Assembly, Final*, End |

Unchanged (by design, checked by M1/M9): the 70 states, domains, TT, τ; the eager stream (1,489,581 clauses); the
12 quad clauses per ordered quadruple; units (sel0, sel1, cube literals in campaign order); row clause form; the 79
lex-leader clauses of the 27 τ-pairs (cert.json/verify.json `sb_pairs` equal `N66E15.sbPairs` for all 105 leaves,
checked in M9); the allocation order (pairs, orientations, convex_four, sel, chains, CE/UE, counter aux in first
reference order, SB aux); the descriptor language of the printer.

## 3. Generator (pinned, unchanged since level 14)

[D] SHA-256 of the files in W = `/home/jay/research/data/n66-20261113` equal the level-14 pins (n66enc
`ref/SHA256SUMS.ref` and L14 §1.2): `etv_common.py 12f00cc6…`, `coupled5.py fbaf431a…`, `lazymono.py 8fd6bd5d…`,
`mono66.py 75dbf96e…`, `p2_sb.py 2c5844a0…`, `p2_write.py 730bad3e…`, `p2_batch_cube.py 999451d9…`,
`p2_lrat_trim 5f1f031e…` (`.cpp 6a1a9aca…`); all mtimes 13-15 Nov, before the c15 start (20 Nov). The level-15
cert.cnf layout of leaf `oooooh` [D]: eager [1, 1,489,581]; quad [1,489,582, 9,693,621] (683,670 × 12); units
[9,693,622, 9,693,629]; rows [9,693,630, 9,709,277] (15,648); card [9,709,278, 9,710,905] (1,628); sb
[9,710,906, 9,710,984] (79); sel_s = 988,541 + s; mono_top 1,647,026; card_top 1,647,821; vars 1,647,847.

The pysat seqcounter port (L14 R1) was grid-fitted at level 14 including the instance (n, k) = (68, 15)
(`ref/seqcounter_fit_level14.py`); at level 15 the complete counter (all 1,628 clauses, numbered from 1,647,027) is
checked by bytes in M1(b).

## 4. Clause families: inventory and soundness sources

The 15 families and their written soundness arguments are those of L14 §4 (table 4.1-4.15, sources: N66 README §2,
§6.3, §6.7, coupled5.py/lazymono.py/p2_write.py/p2_sb.py line numbers). Level 15 changes only:

| # | family | level-15 statement | written soundness | Lean |
|---|---|---|---|---|
| 4.1-4.11, 4.15 | F1-F8, fixed units, SB | unchanged | L14 §4 | unchanged proofs (`holds_pair`, `holds_pos`, `holds_thresh`, `holds_triple`, `holds_ceue`, `holds_quad`, `holds_fixed`, `holds_sb` + `lexChoice` + `mirror_holds`) |
| 4.12 | cube units | `[±sel_s]` for the literals of the 105 leaves of `tree15` | cover of the campaign split (`covered()` in the driver; record §8 exact partition) | `covers_leaves tree15` (structural, any tree) |
| 4.13 | rows | `[−sel_s | s ∈ T]`, T ∈ R0_15 | record: per-leaf `tcert/justification.json`, templates/cores CERTIFIED, `final_verify66` | hypothesis `RowsValid R0_15` |
| 4.14 | counter | pysat seqcounter "at most **15** of the 68 hole literals −sel_s (s = 2..69)" | UNSAT at level L means every set of the class has ≥ L + 1 = 16 holes, so N66 ≤ 69 − 15 = 54 (record §1); a set of n ≥ 55 points occupies n distinct states, so at most 70 − 55 = 15 of the states 2..69 are holes | `holes_le` (55 ≤ n ⇒ ≤ 15 holes), `holds_card` (≤ 15 holes ⇒ every counter clause holds with s(a, j) = "at least j holes among the first a hole literals") |

## 5. Trust items

As L14 §1.3, with the level-15 files:

| # | item | evidence |
|---|---|---|
| E1 | printer output: for each leaf i, the text `n66print15 trim i desc/i.txt` writes has SHA-256 = the recorded `trim_cnf_sha256` | M9 (`tools/hash_binding15.py`, per leaf, never per distinct hash: 8 leaves are UP-refuted) and M1(c) (`tools/trim_check15.sh`, coreutils only) |
| E2 | cake_lpr printed exactly `s VERIFIED UNSAT` on (trim.cnf, trim.lrat) of each leaf | cake.out per leaf; vfy15 fresh re-run 105/105 (`cake_line`), record §8 [R] |
| E3 | cake_lpr's DIMACS reading = `parseDimacs`; `parseDimacs_render` proved (ENCBLEAN) | inherited from ENCBLEAN (same binary) |
| E4 | Lean compiler/runtime of the printer exe | as ENCBLEAN E4; exe hash logged in every check |
| E5 | kernel, Mathlib, library definitions, `OmissionZRow.N66Bound` (LemmaZ.olean) | `n66Bound_unfold` (rfl) |
| E6 | SHA-256 | — |
| H-rows | `RowsValid R0_15` (hypothesis, not trusted silently) | CERTIFIED row by row in the record (per-leaf justification, vfy15 `rows_ok` 105/105) [R]; not formalized |

## 6. Lemma map

Identical to L14 §5 and §8 with the renames of §0; the only statements whose constants changed are `holes_le`,
`holds_card`, `diag_shape`, `meaning_cnt`, `sAux_eq`, `ofCode_code` (cnt/sbe cases), `leaves105_length`, the
`Gaps.holes` field and the `n66_bound_54_*` chain (Assembly → Final → Final3 → Final4 → Final5 → Final6 → End).

## 7. Milestones

| M | content | done when |
|---|---|---|
| M0 | this file | written |
| M1 | Std-only definitions at L = 15, printer exe `n66print15`; byte identity: (b) complete cert.cnf of leaf 0 (12 cube literals) and of leaf 22 (largest trim) vs `full_cnf_sha256` (subsumes the eager stream and the whole counter); (c) the 105 trims vs `trim_cnf_sha256` and the file (coreutils) | 105/105 MATCH (COMPUTED) |
| M2-M3 | soundness of all families for every `Model`; `printClause_mem`; cover; composition | compiles (inherited proofs) |
| M4-M8 | geometry, holes at 15, end theorem with axiom guard | compiles, guard passes |
| M9 | hash binding vs campaign_status.json, cert.json, verify.json, vfy15/summary.json, fresh SHA-256; E2 lines; level fields; negative controls | 105/105 + controls |
| M10+ | rows (`RowsValid R0_15`) in Lean | later stage (as level 14) |

**State (22 Nov 18:10 KST):** M0-M9 done. M1(b) FULL_MATCH for leaves 0 and 22, M1(c) 105/105 MATCH, M9 105/105
MATCH + controls, end theorem compiled with its axiom guard (README status for the logs). The rename-and-edit claim
of §0 is checked by `tools/diff_vs_level14.sh` (`logs/diff_vs_level14.txt`: the hand edits are exactly the rows of
§2 plus docstrings; Facts.lean's `105` comes from the rename rule `132 → 105`).
