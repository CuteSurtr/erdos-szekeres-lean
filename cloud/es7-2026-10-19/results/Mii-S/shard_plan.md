# Shard plan: closing sub-case (ii)

**Recommended route (H): C2's tree with the hull split at its open leaves.** Each of C2's
1,340 open cubes `o` becomes one CNF, `G_o`. In it, fresh selector variables pick a hull case,
and the hull-case cubes do the work. Measured here on open cubes 1–31: 26 are UNSAT and
cake_lpr-verified (max 883 s CaDiCaL; at most 53 s cake_lpr), and 5 hit the 900 s limit
(`open_ext_lrat.jsonl`). That puts the total at roughly **120–160 core-hours** at this VM's
speed: about 84% direct, and the rest through per-case products.

The pure hull-split route (S) is kept below as the alternative. It is sound and partly done
(172/450 cases closed, cover certified). Its remaining cost is dominated by a few hard 4-gon
cases and is estimated at 135–300+ core-hours.

## 0. Inputs (pin these)

- Branch `es7-cloud`. Generator scripts are in `results/Mii-S/scripts/` at commit
  `6a44b5fac3e8e7e6ea490637f4cc66dbcf1aa7c8`.
- `F` = `m33k7int.sub.cnf` from `results/C/scripts/make_cnfs.sh OUT`. It must have sha256
  `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`, and it is byte-identical to H3's
  `lake exe mir_dimacs interior 33 7`.
- Tools: CaDiCaL 3.0.1 (c6073042), march_cu (CnC 705b60c6, built with `-fcommon`), cake_lpr
  (a36874a8; `cake_lpr.S` sha256 `2f3af32d…72b7d4a`).
- The hull cases are `scripts/hullsplit.py cubes cases.icnf cases.json`. That gives 450 cubes;
  `cases.icnf` has sha256 `6b6f0946245da5cb33f287a0484c5ce7ef022bc26452a949848704018e6db742`
  and is committed. Case `n` (0-based line) is `hullsplit.cases()[n]`.
- C2's leaves: the closed ones are `results/C2/logs/cnc_ii_interior/closed.txt` (749, all
  cake_lpr-verified by H3: `results/H3/logs/cube_lrat_ii_interior.jsonl`). The open ones are
  `results/H3/logs/open_cubes_ii_interior.txt` (1,340). H3's `cover_check` accepts the union
  (`results/H3/logs/cover_check_C2_final.log`).

## 1. Hull cover certificates (done: 122/122 cake_lpr VERIFIED)

`scripts/cover.py list` lists `root` and `up:U` (121 upper chains U). For each obligation:
`python3 scripts/cover.py cnf F OB X.cnf; cadical --lrat --binary=false X.cnf X.lrat;
cake_lpr X.cnf X.lrat`. Results are in `cover_lrat.jsonl`: 503 s CaDiCaL and 222 s cake_lpr in total.

## 2. Route H: one job per C2 open cube (1,340 jobs)

For open cube number `i`, the 1-based line of `open_cubes_ii_interior.txt`:

```
scripts/run_open_ext.sh F i 900 WORKDIR     # -> one JSON line
#   = python3 scripts/open_ext.py F "<o, comma separated>" G.cnf
#     cadical --lrat --binary=false -t 900 G.cnf G.lrat ; cake_lpr G.cnf G.lrat
```

`G_o = F + units(o) + {¬e_c ∨ l : l ∈ cube(c)} for the 450 cases c + (e_1 ∨ … ∨ e_450)`,
where `e_c = 47003 + index(c)` are fresh variables.

- Shards: machine `m` of `N` takes the indices `i ≡ m (mod N)`, with one job per core.
  Order inside a shard does not matter.
- Determinism: replace `-t 900` with a conflict budget `-c 5000000` if needed. Nothing tried
  here came close to that budget.
- A job that does not finish: split it with `march_cu G.cnf -d 4`, using the cube literals over
  the original variables only, i.e. drop the `e_c`. Alternatively, solve
  `F + o + cube(c)` per case c (`hybrid_grid.py` shows that only about 1–37 of the 278 open
  cases survive 2,000 conflicts per open cube). Both are covered by section 4.
- Expected cost, from the 31 jobs run here: a censored mean of 301 s of CaDiCaL + 12 s of
  cake_lpr per cube under contention, so at least 117 core-h for all 1,340, plus the splits of
  the roughly 16% that time out. Proofs are up to 463 MB; delete them after checking. On
  N = 8 machines × 4 cores this is about 4–5 h wall.
- For a G_o that times out, use per-case products. Write `F + units(o) + units(cube(c))` for each
  of the 278 cases not already closed (the 172 closed cases are covered by monotonicity), and
  check each with cake_lpr. Most die in under 1 s; the survivors took 5–36 s. Compose with
  `hcov` (section 4) and the 450 product refutations, the closed cases' ones included by
  monotonicity.
- Optional speed-ups:
  - drop the open cubes that are fully inside the union of Mii's closed cubes (each also needs its
    Mii proof checked by cake_lpr, since most Mii leaves used lrat-check);
  - keep one solver per shard and pass cubes as assumptions. This was measured at 21 s for one
    cube in PySAT, but it needs an incremental proof format that cake_lpr does not check.

## 3. Route S (fallback): finish the 278 open hull cases directly

`cases.jsonl` has every case's CNF sha256 and status. 172 cases are UNSAT with cake_lpr
VERIFIED. U8_L is nearly done by cube-and-conquer: 433 leaves verified and about 70 left
(see README).

Per case: `scripts/close_march.py CASE.cnf OUT --depth 7 --timeout 300 --split-depth 6 --jobs
<cores>`, with `--depth 6` for the 6-gon cases. The leaves are checked by cake_lpr, and
`lake exe cover_check OUT/leaves.icnf` must print `s COVERED`.

Measured march estimates (`probes.jsonl`, 6 sampled cubes per case at 300 s, censored at 300):

- 4-gon cases: 0.84 h (11/), 0.93 (/11), 1.13 (/8), 1.52 (8/; the real partial run already
  used about 4.9 h because of re-splits), 1.64 (/4), 3.44 (6/),
  ≥ 8.3 (3/, 3/6 cubes timed out), ≥ 10.7 (/2, 6/6 timed out).
  - 28 cases × mean ≥ 3.6 h → ≥ 100 core-h, dominated by /2 and 3/.
- 6-gon cases: 0.06 h (5/10), 0.62 (3,5/), 0.75 (6/2), 1.79 (/2,3).
  - 250 cases × 0.15–0.8 h → 35–200 core-h. The layer-probe mean was 0.14 h, and it is biased low.

The layer split (`layers.py`, `cover2.py`) was tested and does not help in general. Under /7,
the layer-2 children whose layer is again a 4-gon timed out at 60 s in 11 of 12 cases.

## 4. Composing the certificate (Lean)

The target is `¬DimacsSatisfiable (Mir.interiorCnf 33 7)`, the `h2` of
`Mir.mirrorExclusionLine_of_unsat`. Two small lemmas are needed next to H3's `Cover.lean`.
They are **not written or compiled here**.

```lean
/-- Blocking-clause cover. -/
theorem covers_of_blocked {F : List (List ℤ)} {P : List ℤ} {cubes : List (List ℤ)}
    (h0 : ∀ c ∈ cubes, ∀ z ∈ c, z ≠ 0)
    (hb : ¬DimacsSatisfiable (cubeCnf F P ++ cubes.map (List.map (fun z => -z)))) :
    ∀ ν, DimacsSat (cubeCnf F P) ν → ∃ c ∈ cubes, CubeSat ν c
-- proof: otherwise every cube has a false literal z, so -z holds (litSat_neg), so ν
-- satisfies every blocking clause, contradicting hb.

/-- Selector extension. -/
theorem not_sat_of_selector {F : List (List ℤ)} {o : List ℤ} {cubes : List (List ℤ)} (nv : ℕ)
    (hvars : ∀ cl ∈ cubeCnf F o, ∀ z ∈ cl, z.natAbs ≤ nv) (hcv : ∀ c ∈ cubes, ∀ z ∈ c, z.natAbs ≤ nv)
    (hcov : ∀ ν, DimacsSat F ν → ∃ c ∈ cubes, CubeSat ν c)
    (hG : ¬DimacsSatisfiable (cubeCnf F o ++ selectorClauses nv cubes)) :
    ¬DimacsSatisfiable (cubeCnf F o)
-- selectorClauses nv cubes = [[-(e n), z] | n, z ∈ cubes[n]] ++ [[e 0, …, e (k-1)]],
-- e n = nv + 1 + n.  Proof: extend ν by ν (e n) := decide (CubeSat ν cubes[n]).
```

Chain:
1. `root` and `covers_of_blocked` (with P = []): every model of F satisfies some UP(U).
   Then `up:U` and `covers_of_blocked` (with P = UP(U)): it satisfies some cube(U,L). That gives
   `hcov` for the 450 case cubes.
2. Each open o: `hG` comes from cake_lpr on `G_o` (`open_ext.py` writes F, then o's units, then
   the selector clauses in that order: `cubeCnf F o ++ selectorClauses`).
   `not_sat_of_selector` then gives `¬Sat (cubeCnf F o)`.
3. Each closed C2 cube k: `¬Sat (cubeCnf F k)` (H3, cake_lpr).
4. `not_dimacsSatisfiable_of_coverCheck` on closed ∪ open, which H3's `cover_check` accepts,
   gives `¬Sat F`.

Route S composes in the same way: per case, `¬Sat (cubeCnf F cube)`, directly or through
`coverCheck` on march leaves of `cubeCnf F cube`. With `hcov`, a variant of
`not_dimacsSatisfiable_of_cover` that takes a covering hypothesis relative to F, then gives `¬Sat F`.

Trust base: as in H3 (cake_lpr, the scripts' clause appending, the compiled `cover_check`).
`hullsplit.py`, `cover.py` and `open_ext.py` are **not trusted**: a wrong cube can only make
some certificate fail. `soundness.md` gives the geometric reason the obligations are UNSAT.
