# V1R / R3: second from-scratch check of the sub-case (i) leaves, shard j = 3

Task: `results/V1R/TASK.md` at 640a56c2, with V = R3, j = 3, H = 1.5.

**Result: all 299 leaves of my share (0-based line index i ≡ 3 mod 4 of `verify/hull_leaves.icnf`)
are verified: CaDiCaL exit 20 and cake_lpr printed the line `s VERIFIED UNSAT` for every one,
on the first run. No leaf was SAT or unverified, so nothing was re-run.**

## Tools (`tools.txt`)
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source (`./configure && make`).
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`; its example prints `s VERIFIED UNSAT`.
- Driver and comparison are my own (`driver.py`, `compare.py`); no scripts of V1-0..V1-3, V1-L or verify/v3 were used.
- Machine: 4 cores, 15 GB (`env.txt`).

## Inputs
- `hm33k7.sub.cnf`: `tools/etv/gen_etv.py 33 7 7 7 --mirror --hull` then `results/C/scripts/mirgen.py hm33k7.cnf 33 --hull`
  (as in `results/C/scripts/make_cnfs.sh`; results/H3 states the Lean `mir_dimacs hull 33 7` output is identical).
  sha256 `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d` (matches), header `p cnf 47002 535454`.
- `verify/hull_leaves.icnf`: sha256 `cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6` (matches), 1,198 lines.

## Method
Per leaf c: CNF = `p cnf 47002 535454+|c|`, the body of `hm33k7.sub.cnf` unchanged, then one unit clause per literal
of c in file order (= `cubeCnf (hullCnf 33 7) c`); sha256 recorded. `cadical --lrat=true --no-binary`, then
`cake_lpr cnf proof`; proof sha256 recorded before deletion. 3 leaves in parallel.
One JSON line per leaf in `out.jsonl` (i, cube, cnf_sha256, solver_exit, solve_s, proof_bytes, proof_sha256, cake_lpr, check_s, ok).

## Numbers
- Verified: **299 / 299**.
- Total solve time 6,802.9 s, total cake_lpr time 1,484.3 s (sum over leaves; wall time about 46 min, 04:40 to 05:26 UTC).
- Largest leaf by solve time: i = 879 (19 literals), 278.6 s solve, 20.6 s check, proof 196,032,147 bytes.
  Largest proof: i = 755 (19 literals), 237,327,313 bytes, 277.8 s solve, 22.8 s check.

## Differences from the earlier records (`results/V1-3/leaves_cake.jsonl`, key `line`)
- Every one of my 299 leaves has an earlier record with the same index and the same cube.
- Same solver exit (20) and same cake_lpr verdict (VERIFIED UNSAT) for all 299. No verdict differences.
- Informational only: proof sizes differ for 150 of the 299 leaves (list in `compare.txt`); the other 149 have
  byte-identical sizes. The earlier records have no CNF or proof hashes, so those cannot be compared.
