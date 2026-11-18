# VERIFY_P307V_L10: claim `p307v-l10-pycheck` (verifier VB, 18 Nov 2026, 02:51-03:10 KST)

**Verdict: CONFIRMED.**
- An own fourth implementation of the leaf rule replays both budget-35 packets completely; every check passes:
  - (18,17): `runs/b35s18/bb`, 3,672 rows, 4,838 contexts;
  - (19,16): `runs/b35s19/bb`, 3,707 rows, 7,170 contexts.
- Per context it agrees with tcheck_b35 (the VERIFY308 per-context TSVs) on all eight compared columns: nodes, leaves,
  weighted, over_budget, minimum margin, number of leaves at the minimum, maximum positive-weight row, errors. It also
  agrees with the claim's pycheck_b35 TSVs: nodes, leaves, minimum margin, maximum row, errors, and the master line.
- **0 differences** in either packet.
- Totals equal the claim's:

| packet | contexts | master nodes / leaves | total nodes | total leaves | min margin (leaves at it) | errors |
|---|---|---|---|---|---|---|
| (18,17) | 4,838 | 11,519 / 922 | 416,935 | 206,049 | 1 (9,317) | 0 |
| (19,16) | 7,170 | 15,147 / 404 | 15,533,581 | 7,763,206 | 1 (614,548) | 0 |

So route L10 of ROUTE307_1116 has a Python cross-check (the claim's), and now also an independent fourth replay.
- The label is **EXACT TREE**, relative to the rows of each packet as in VERIFY308 §2.
- The rhs-1 rows' LRAT checks are a separate item: VERIFY308 §5 and the audits; they were not re-run here.

## 1. What was checked

The statement is that the two packets pass the leaf rule with B = 35, and that pycheck_b35 agrees per context with
tcheck_b35 (0 differences, the totals above).

Definitions are those of VERIFY308 §2-3:
- states 0..153; rows = the 2,650 catalogue constraints followed by `extra.json`;
- a weighted leaf at missing set M and occupied set O is valid iff
  margin = Σ w_r·max(0, d_r − |S_r ∩ M|) − c·(35 − |M|) − Σ_{i ∈ U} max(0, load_i − c) ≥ 1, with U = states \ (M ∪ O);
- an over_budget leaf is valid iff |M| > 35;
- the master is walked from M = ∅, O = {0}.

## 2. Method: own code, `W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/p307v-l10-pycheck/`

`vb_tree.py` was written from the definitions above. VERIFY308's `tcheck*.cpp` and `pycheck*.py` and the claim's
`pycheck_b35.py` were **not read**. The node format was taken from the data: branch `{type, vertex, zero, one}`,
weighted `{type, capacity, weights: [[row, w], …]}`, context `{type, context}`. Child `zero` adds the vertex to O and
child `one` adds it to M; every context file's missing/occupied sets equal its placeholder's, which confirms this
reading.

**Inputs.**
- Strict JSON: duplicate keys, floats and NaN/Infinity are rejected; integers must be of Python type int.
- Rows: supports are distinct integers in 0..153, with 0 ≤ d ≤ |S|.
- extra[0] = (F, T) and extra[1] = (Lo, 35 − T), with F = {i : states[i][0] ≥ 5} (84 states) and
  Lo = {i : states[i][0] ≤ 4} (70 states).
- The master's `budget` = 35, its `source`/`extra` are the files used, and `contexts` = the number of placeholders.
- Placeholder ids are distinct, and the set of `ctx-*.json.gz` files equals the set of placeholder ids.

**Walk.**
- Iterative DFS, with M and O kept as 0/1 vectors and undone on the way back.
- Every node is reached exactly once (reached twice → error; unreached → error).
- A branch vertex lies in 0..153 and not in M ∪ O; children are in range.
- Context nodes are allowed only in the master; any other node type, e.g. `pending`, is an error.
- Each context file:
  - has keys exactly {context, missing, occupied, root, nodes};
  - has `context` = its id;
  - has missing/occupied equal to the placeholder's M/O as sets, with no duplicates;
  - is walked with the same rules.

**Arithmetic.**
- The leaf margin is computed in numpy int64 only when every weight and the capacity are below 2^40. Then every
  intermediate is below 2^62: w·deficit < 2^48, the sum over ≤ 3,707 rows < 2^60, the load < 2^52, and the excess over
  154 states < 2^60. Otherwise the margin is computed in Python integers.
- c·(35 − |M|) is always computed in Python integers.
- One weighted leaf in 97 is recomputed in pure Python integers and must agree: 1,046 samples in (18,17) and 77,066
  in (19,16), with **0 disagreements**.

**Comparison and runs.**
- `vb_compare.py` compares per context with `/home/jay/research/data/verify308-20261114/b35/out-b35s1{8,9}.contexts.tsv`
  (tcheck_b35, 15 Nov) and with the claim's `VERIFY307/data/py-b35s1{8,9}.tsv`.
- Unit `esr-agv-vb-l10tree` (95 %, MemoryMax 1500M, under `vb1118/unit.lock`):
  - (18,17): 15.3 s, max RSS 83 MB;
  - (19,16): 11 min 37 s, max RSS 387 MB.
- The packets are unchanged since 14 Nov (master files 14 Nov 22:57 and 23:22; no file newer than the 15 Nov tcheck
  summaries). Inputs: source SHA-256 `8c7fe9ef5264182524095d46ef50ed6bc691cab425efa965756d1870112241aa`;
  `b35s18-v13/extra.json` `c9c922c0a113c78effbbbef330c000af90b528152c9c511592f6210c1040caa7` (1,022 rows: capacity rows
  (F, 18) and (Lo, 17), then 1,020 rows of rhs 1); `b35s19-v16/extra.json`
  `1257c4a15a52d89451b7c73736d6182fd859892febdea421e7e4a72b74f5f25c` (1,057 rows: (F, 19) and (Lo, 16), then 1,055 rows
  of rhs 1).

## 3. Results (`W/vb18.tsv.summary.json`, `W/vb19.tsv.summary.json`, `W/cmp18.json`, `W/cmp19.json`)

| check | (18,17) | (19,16) |
|---|---|---|
| row errors; capacity rows exact | none; yes | none; yes |
| master: budget 35, source, extra, `contexts` = placeholders, `master_leaves` = counted | yes (4,838; 922) | yes (7,170; 404) |
| placeholder ids distinct; ctx files = placeholders | yes; yes (4,838) | yes; yes (7,170) |
| master nodes / leaves / min margin (count) / max row / errors / unreached | 11,519 / 922 / 1 (38) / 3,664 / 0 / 0 | 15,147 / 404 / 1 (44) / 3,670 / 0 / 0 |
| total nodes / leaves (all weighted; no over_budget) | 416,935 / 206,049 | 15,533,581 / 7,763,206 |
| minimum margin / leaves at the minimum | 1 / 9,317 | 1 / 614,548 |
| maximum positive-weight row / rows used with positive weight | 3,670 / 2,634 | 3,706 / 3,392 |
| errors / contexts with errors | 0 / 0 | 0 / 0 |
| per-context differences vs tcheck_b35 (8 columns) / vs pycheck_b35 (5 columns + master) | **0 / 0** | **0 / 0** |
| verdict of the own replay | EXACT TREE | EXACT TREE |

The minimum-margin counts, the maximum rows and the numbers of rows used also equal tcheck_b35's
`out-b35s1{8,9}.summary.json` (9,317 / 3,670 / 2,634 and 614,548 / 3,706 / 3,392).

## 4. Controls (negative, on a copy: `W/mut18/bb` = `runs/b35s18/bb` with 9 mutations; `W/mutate18.py`, `W/mut18.tsv`)

| mutation | own replay |
|---|---|
| ctx 0: one leaf's capacity set to 10^12 (also tests the Python-integer path) | margin −26,999,729,980,858 < 1, error |
| ctx 1: a branch vertex set to an occupied state | error "branch vertex" |
| ctx 2: one extra state in `missing` | error "missing differs from placeholder" |
| ctx 3: duplicate key in the JSON | error "duplicate key" |
| ctx 4: file removed | error (file); ctx files ≠ placeholders |
| ctx 10: a leaf replaced by `pending` | error "node type 'pending'" |
| ctx 11: one weight written as a float | error "non-integer number" |
| ctx 12: one negative weight | error "weight entry" |
| ctx 13: branch with both children equal | error "node reached twice" |

Exactly these 9 contexts have errors, and the verdict is NOT CONFIRMED. The positive control is the unmutated
packets above.

## 5. What this does not show

- The soundness of the leaf rule is VERIFY308 §3's derivation. It was read and agreed with, not re-derived
  differently.
- That the rhs-1 extra rows are valid (each a certified coupled row) is VERIFY308 §5 and the cuts audits; not re-run
  here.
- The ES(8) ≤ 307 chain needs other inputs: (20,15) and N66 ≤ 55 (VERIFY307 README §1). This verification covers
  item L10/C2 only.

## 6. Files (`W` as above)

| file | SHA-256 |
|---|---|
| `vb_tree.py` | see `W/SHA256SUMS` (`39f17294…`) |
| `vb_compare.py`, `mutate18.py`, `run.sh` | `W/SHA256SUMS` (`4a70efe5…`, `dcfc808c…`, `2b41f474…`) |
| `vb18.tsv`, `vb19.tsv`, `mut18.tsv`, `cmp18.json`, `cmp19.json` | `W/SHA256SUMS` (`ccd30ddd…`, `8dbc2825…`, `8ceb462e…`, `56368e49…`, `dbc6a1f3…`) |
| compared: `py-b35s18.tsv`, `py-b35s19.tsv`, `out-b35s18.contexts.tsv`, `out-b35s19.contexts.tsv` | `d7627194…`, `46aa9307…`, `18376038…`, `b353f155…` (`W/SHA256SUMS`) |

Re-run: `bash W/run.sh` (about 12 min on one thread; MemoryMax 1500M is ample).
