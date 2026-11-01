# V1R, machine R1, shard j = 1 (i ≡ 1 mod 4)

**Result: 300 of 300 leaves verified** (CaDiCaL exit 20 and a cake_lpr output line exactly
`s VERIFIED UNSAT` for every leaf). No leaf was SAT or failed; no re-runs were needed.

## Tools (`tools.txt`)
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source here.
  Call: `cadical --lrat=true --no-binary -q leaf.cnf leaf.lrat` (text LRAT).
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr` (gcc 13 -O2);
  `cake_lpr.S` sha256 2f3af32d…72b7d4a; bundled example prints `s VERIFIED UNSAT`.
- Own driver `driver_v1r.py` (3 leaves in parallel) and comparison script `compare_v1r.py`.

## Inputs
- `hm33k7.sub.cnf` generated with `tools/etv/gen_etv.py 33 7 7 7 --mirror --hull` then
  `results/C/scripts/mirgen.py hm33k7.cnf 33 --hull` (the `make_cnfs.sh` route; H3 shows it is
  byte-identical to the Lean `mir_dimacs hull 33 7` output): sha256
  `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d` (matches), `p cnf 47002 535454`.
- `verify/hull_leaves.icnf`: sha256 `cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6` (matches).

## Leaf CNFs
For leaf i with cube c: header `p cnf 47002 (535454+|c|)`, the body of `hm33k7.sub.cnf`
unchanged, then one unit clause per literal of c in file order — the clause list of
`cubeCnf (hullCnf 33 7) c`. Each CNF's sha256 and each proof's sha256 are in `out.jsonl`
(300 distinct CNF hashes). CNFs and proofs were deleted after hashing.

## Numbers
- Leaves: i = 1, 5, …, 1197 (300); cube lengths 7: 30, 13: 158, 18: 1, 19: 79, 25: 32.
- Total solve time 6,206.7 s, total cake_lpr time 1,368.8 s (wall per leaf, 3 in parallel on
  4 vCPUs; run wall time about 43 min, 04:41–05:24 UTC 2026-10-21).
- Largest leaf: i = 13, cube [-1015, -525, -2045, 1979, 1960, 1940, 1919], proof 185,762,009
  bytes (sha256 1a5b61d2…cb8ee), solve 262.5 s (also the slowest), check 27.4 s.

## Comparison with results/V1-0 to V1-3 (`compare.txt`)
The earlier records for this shard are all in `V1-1/leaves_cake.jsonl` (300 records, index key
`line`). Same i, same cube, same solver exit 20 and a cake_lpr verdict for all 300.
**Differences: none** in substance. Only a format difference: V1-1 records the verdict as
`VERIFIED UNSAT` while this run records the exact line `s VERIFIED UNSAT`. The earlier records
carry no CNF or proof hash, so those columns have nothing to compare against.

Files: `env.txt`, `tools.txt`, `out.jsonl`, `driver_v1r.py`, `compare_v1r.py`, `compare.txt`, `run.log`.
