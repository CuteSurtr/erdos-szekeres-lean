# Task Mii-S: a cheaper sound way to close mirror sub-case (ii)

Sub-case (ii): 33 points in general position, symmetric in a line, with the axis point
strictly inside the hull and no convex 7-gon. CNF `F = m33k7int.sub.cnf`, sha256
`69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d` (regenerated here and matched).

**Nothing here is a claim that sub-case (ii) is closed.** Every UNSAT below is a claim about
one explicit CNF, checked with cake_lpr. All of them are listed in the `*.jsonl` files.

## Summary

1. **Hull-pair split, proved sound two ways.** It has 450 cases. The hull of a sub-case (ii) set is a
   4-gon or a 6-gon made of mirror pairs, and each case fixes the hull with orientation units.
   - Geometric proof: `soundness.md`.
   - Random tests: 2,000 + 1,000 sets, 0 failures. A 2-layer version: 2,000 sets, 0 failures.
   - **SAT-certified cover:** a root lemma plus 121 per-upper-chain lemmas, all 122 UNSAT and
     cake_lpr VERIFIED (`cover_lrat.jsonl`). The cover therefore needs no geometric trust.
2. **Per-case measurements.**
   - 172/450 cases are UNSAT within 10 s, all cake_lpr VERIFIED (`pass2_lrat.jsonl`).
   - Case U8_L (a 4-gon hull) was closed by cube-and-conquer, every leaf cake_lpr VERIFIED (see
     below).
   - The rest are not cheap. The 6-gon cases cost 0.06–1.8 core-h each under march. The 4-gon
     cases cost 0.8 to ≥ 10.7 core-h each, and /2 and 3/ are the hard core.
   - Finishing by the split alone: about 135–300+ core-h.
3. **The cheapest sound route found is a hybrid:** C2's tree, with the hull split at its 1,340 open leaves.
   - For an open cube o, one CNF `G_o` adds fresh selector variables `e_c → cube(c)` and the
     clause `∨ e_c`. That clause holds by the certified cover.
   - C2 had left all of these cubes open. **Every one tried so far is UNSAT, and cake_lpr
     VERIFIED it** (`open_ext_lrat.jsonl`): RESULT_OPEN_EXT.
   - Projected total: about 50–70 core-h at this VM's speed, in 1,340 small jobs of similar size.
     That is cheaper and far more predictable than the baselines (below).
4. `shard_plan.md` gives a deterministic N-machine plan and the Lean composition. The composition
   needs two small lemmas next to H3's `Cover.lean` (stated there, not written or compiled here).

## What ran where

- One cloud VM: Linux 6.18 x86_64, 4 cores, 15 GB RAM (`env.txt`). Run from 04:49 to about
  08:45 UTC on 20 Oct 2026.
- Tools, built here:
  - CaDiCaL 3.0.1 at c6073042;
  - march_cu from CnC 705b60c6, built with `-fcommon`;
  - cake_lpr at a36874a8 (`cake_lpr.S` sha256 `2f3af32d…72b7d4a`, matching the repository; its
    `example.cnf` prints `s VERIFIED UNSAT`);
  - drat-trim 2e3b2dc0 `lrat-check` with `results/E2/tools/lrat-check-E2.patch` applied. It was
    built but not needed: every check below is cake_lpr.
  - PySAT (CaDiCaL 1.9.5) and numpy, from pip. They were used only for measurements
    (`hybrid_grid.py`, `open_cube_full.py`, `baseline.py`), never for a claim.
- `results/C/scripts/make_cnfs.sh` regenerated the CNFs. `m33k7int.sub.cnf` has the sha256 above,
  and `hm33k7.sub.cnf` has `bfbc2d60…`. Both match H3.
- No CNF or proof file is committed. Proofs were deleted right after each cake_lpr check.

## 1. The split and its soundness

A case is (U, L): U and L are disjoint sets of pair labels a ∈ 2..16 (pair a ↔ 34−a) with
1 ≤ |U|+|L| ≤ 2. U holds the pairs on the upper hull, above the horizontal chord 1–33, and L the
pairs on the lower hull. That gives 30 cases with a 4-gon hull and 420 with a 6-gon hull.

The cube of a case has three parts:
- (a) every other point is strictly left of each ccw hull edge;
- (b) hull triples are ccw;
- (c) each upper (lower) vertex is above (below) every chord that spans it.

Cubes have 61–535 orbit literals (`scripts/hullsplit.py`, `cases.icnf`). The unit X(1,2,3) of
F is kept, and both placements (above/below) are enumerated, so the y-flip is used once.

- **Geometric proof:** `soundness.md`. In short: 1 and 33 are extreme and level with each other.
  The axis point is not a hull vertex, so the hull vertices come in mirror pairs. Each pair is
  strictly above or strictly below the chord. Convex position gives at most 6 vertices.
  (a)–(c) hold for any convex polygon containing the set.
- **Certificate proof** (`scripts/cover.py`, `cover_lrat.jsonl`):
  - `root`: F + {¬UP(U)} for the 121 upper chains is UNSAT;
  - `up:U`: F + UP(U) + {¬cube(U,L)} is UNSAT for each U.
  - All 122 are cake_lpr VERIFIED. That took 503 s of CaDiCaL (largest 206 s) and 222 s of cake_lpr,
    with 1.0 GB of proofs.
  - A flat version (F + all 450 blocking clauses) did not finish in 1,480 s, which is why the
    cover has two levels. The first gift-wrapping step alone was UNSAT in 2.4 s.
- **Random tests:**
  - `test_split_report.json`: 2,000 sets with a random 4-/6-gon mirror hull, plus 1,000 uniform
    interior-axis mirror sets, 148 of which had hulls of at most 6 vertices. Each set's
    orientations (y-flipped where needed) satisfy all 163,443 orientation-only clauses of F, and
    exactly the set's own case cube holds. Uniform sets with larger hulls satisfy no cube. 0
    failures, 279 distinct cases hit.
  - `test_layers_report.json`: the same check for two nested layers (`layers.py`), 2,000 sets.
    0 failures, 1,207 distinct specs.

## 2. Per-case measurements

`cases.jsonl` has one line per case: sha256 of the case CNF, status, times and estimates.

- **10 s sweep** (`sweep10.jsonl`): 172 cases UNSAT, all of them within 10 s.
  - Re-solved with LRAT, all 172 are **cake_lpr VERIFIED** (`pass2_lrat.jsonl`): 443 s of CaDiCaL,
    331 s of cake_lpr, at most 10 s per case.
  - These include every case with pair 2 on the upper hull, every case with pair 3 on the lower
    hull (both are refuted by the X(1,2,3) unit), and most same-side 6-gon cases with the inner pair
    at 6 or more.
- **60 s direct attempts on 6-gon cases:** 11/11 tried were still UNKNOWN
  (`two_direct_partial.jsonl`).
- **march_cu probes** (`probes.jsonl`): `march_cu -d 7` (4-gon cases) or `-d 6` (6-gon cases),
  then 6 random cubes at 300 s. The estimate is ncubes × mean sample time + march time, censored at 300 s.

  | case | hull | est. core-h | sampled cubes closed |
  |---|---|---|---|
  | 11/ | 4-gon | 0.84 | 6/6 |
  | /11 | 4-gon | 0.93 | 6/6 |
  | /8 | 4-gon | 1.13 | 6/6 |
  | 8/ | 4-gon | 1.52 | 6/6 (closed in full, below) |
  | /4 | 4-gon | 1.64 | 6/6 |
  | 6/ | 4-gon | 3.44 | 6/6 |
  | 3/ | 4-gon | ≥ 8.27 | 3/6 |
  | /2 | 4-gon | ≥ 10.72 | 0/6 |
  | 5/10 | 6-gon | 0.06 | 6/6 |
  | 3,5/ | 6-gon | 0.62 | 6/6 |
  | 6/2 | 6-gon | 0.75 | 6/6 |
  | /2,3 | 6-gon | 1.79 | 6/6 |

- **Layer probes** (`est_one.jsonl`, `est_two.jsonl`; `scripts/lnc.py estimate`, Knuth-type,
  sampling 4 children at layer 2 and 2 at layer 3, 20 s attempts):
  - 28 4-gon cases: 0.1 h to 177 h, censored;
  - 40 6-gon cases: median 126 s, mean 495 s.
  - These are **biased low.** The real layer-2 run under /7 (`layer2_attempts_partial.jsonl`) shows
    that children whose next layer is again a 4-gon time out at 60 s: 11 of 12 did. The sample of
    4 missed them. So the layer split moves the difficulty down a layer rather than removing it.
  - Its certified covers do work: for 8/ and /7 all 214 `cover2.py` obligations are cake_lpr
    VERIFIED (`cover2_lrat_8_7.jsonl`, 484 s + 381 s).
- **Case U8_L closed:** RESULT_U8.

## 3. The hybrid: C2's open cubes × hull cases

- On /2, the hardest hull case, 6 random C2 open cubes added to the case were all UNSAT
  (`probe_open_L2.json`): five in 0.2 s and one in 82 s.
- In the other direction (`hybrid_grid.jsonl`), take 12 random open cubes. Load F + o once in
  incremental CaDiCaL 1.9.5 and try each of the 278 open cases as assumptions with 2,000 conflicts.
  On average only 11 cases (range 1–37) survive. The survivors close in 5–36 s from scratch (9/9
  sampled, `product_probe.jsonl`). One open cube, fully solved incrementally over all 278 cases,
  took 21 s in total (`open_cube_full.jsonl`).
- **Certified form** (`scripts/open_ext.py`, `scripts/run_open_ext.sh`):
  `G_o = F + units(o) + {¬e_c ∨ l : l ∈ cube(c)} + (e_1 ∨ … ∨ e_450)`, with fresh `e_c`.
  - A model of F ∧ o extends to G_o by setting `e_c := cube(c) holds`, and the certified cover
    supplies some true `e_c`. So UNSAT of G_o refutes F ∧ o (`shard_plan.md` §4).
  - Results: RESULT_OPEN_EXT_DETAIL

## 4. Cost against the baselines

Data: `baseline.json` (`scripts/baseline.py`), from the Mii-0..7 `leaves.jsonl` at their final
commits, pulled at 06:47 UTC, and from C2's closed list. The measure is the probability that a
uniform assignment satisfies a closed cube (Monte Carlo, 40,000 samples).

| route | done so far | what is left | estimate (core-h, this VM) |
|---|---|---|---|
| (a) Mii: d7 cubes + 300 s + d6 splits | closed measure 0.460 for 88.6 logged core-h | measure 0.54 | ≥ 104 by linear extrapolation. The rest is the hard tail, so likely several times that |
| (b) C2 ∪ Mii closed, open region cubed afresh | closed measure 0.803 | the 1,340 C2 open cubes (minus Mii overlap); C2 could not close them | ≥ 38 linear; no per-cube cost known |
| (S) hull split only | 172/450 cases + U8_L, cover certified | 277 cases | about 100+ (4-gon cases) + 35–200 (6-gon cases) ≈ 135–300+ |
| **(H) C2 tree + hull split at the open leaves** | 749 closed (H3) + RESULT_OPEN_EXT_SHORT | the remaining open cubes | **≈ 50–70** (mean about 3 min per open cube, contended), evenly sized |

Route H is the recommendation. Its cost is a sum of 1,340 small measured pieces, not an
extrapolation over a hard tail.

## 5. SAT results

None. No case, cube, product or `G_o` was SAT, so nothing needed decoding or realization.

## Files

- `scripts/`: `hullsplit.py` (cases and cubes), `cover.py` / `cover2.py` (certified covers),
  `layers.py` (layer split), `test_split.py` / `test_layers.py` (random tests), `run_case.sh` /
  `run_spec.sh` / `run_cover*.sh` / `run_open_ext.sh` (one job each, cake_lpr),
  `close_march.py` (cube-and-conquer per case), `probe_case.py`, `lnc.py`, `hybrid_grid.py`,
  `product_probe.py`, `open_cube_full.py`, `probe_open.py`, `hybrid_case.py` (measurements),
  `open_ext.py` (G_o), `baseline.py`, `case_overlap.py`, `covercheck.py` (an unverified Python port of
  H3's coverCheck), `summarize.py` (builds `cases.jsonl`).
- Data: `cases.icnf`, `cases.jsonl`, `sweep10.jsonl`, `pass2_lrat.jsonl`, `cover_lrat.jsonl`,
  `cover2_lrat_8_7.jsonl`, `probes.jsonl`, `est_*.jsonl`, `layer2_attempts_partial.jsonl`,
  `two_direct_partial.jsonl`, `hybrid_grid.jsonl`, `product_probe.jsonl`, `open_cube_full.jsonl`,
  `probe_open_L2.json`, `open_ext_lrat.jsonl`, `baseline.json`, `cnc_U8_L/`, and the reports.
- Docs: `soundness.md` and `shard_plan.md`.

## Caveats

- The cost estimates come from small samples (6 cubes per probe, 12 open cubes on the grid) on a
  VM where 4–6 processes shared 4 cores. Times are wall-clock per process under that contention.
- "Closed measure" is a uniform-assignment proxy, and it is not proportional to difficulty.
- The Lean lemmas in `shard_plan.md` §4 are stated, not proved or compiled. Until they exist,
  the composition is an argument on paper. Each piece it uses is a cake_lpr-checked UNSAT claim.
- One experiment was stopped before it finished: hybrid case CNFs (F + case + C2's 749
  closed cubes as blocking clauses) for /2, 3/ and 6/ got no answer in about 15 min and were
  killed. The layer-2 closing run of 8/ and /7 was stopped once the 4-gon-chain problem was clear.
