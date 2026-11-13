# C2P2 M23

Task `results/C2P2/TASK.md` at commit d266d2c3, with V = M23, LIST = C2P2.tsv, j = 23, N = 42 and H = 2.5. Machine (`env.txt`): 4 cores, 15 GB RAM. Started 06:47 UTC; lane END 09:02:06 UTC (epoch 1793437326).

## Tools and checks (`tools.txt`)
- Built with `C2P/vendor/build_tools.sh` from the vendored sources only (all 196 manifest hashes match): CaDiCaL c6073042 (3.0.1), cake_lpr a36874a8, and lrat-check 2e3b2dc with the E2 patch. Nothing was cloned or downloaded.
- Sanity checks: lrat-check and cake_lpr both reject the bad LRAT and both accept the good one. The cake_lpr example prints `s VERIFIED UNSAT`.
- Base CNF: header `p cnf 838032 16653336`, and the sha256 of base.cnf (b0061e90…) and base.json (2476faff…) are the expected values.
- Cubes P1..P8 are byte-identical to `C2P/cubes/P{a}_cubes.txt`.

## Units (`units.tsv`, rows with idx ≡ 23 mod 42)
| unit | case | kind | cap | result | solve s | lrat-check s | cake_lpr s | proof |
|---|---|---|---|---|---|---|---|---|
| P7_1-9 | P7 | Q | 6000 | **certified** UNSAT | 5577.2 | 155.6 | 784.4 (heap 8000) | 9.83 GB |
| P6_1-3-15 | P6 | H | 739 (shortened by END) | **certified** UNSAT | 219.0 | 51.0 | 301.3 (heap 8000) | 3.19 GB |
| P6_1-9-15 | P6 | H | 1800 | not reached | | | | |
| P6_2-4 | P6 | Q | 2400 | not reached | | | | |
| P6_2-11-15 | P6 | H | 1800 | not reached | | | | |
| P6_3-10-13 | P6 | H | 1800 | not reached | | | | |
| P6_8-9 | P6 | Q | 2400 | not reached | | | | |
| P6_11-12 | P6 | Q | 2400 | not reached | | | | |

Counts by case and kind:
- Certified 2: P7 Q 1 and P6 H 1.
- Timed out (UNKNOWN) 0.
- Errors 0.
- Not reached 6: P6 H 3 and P6 Q 3. At 08:49:28 the lane stopped with 757 s left, under the 900 s it needs to start a unit.

Over the 2 certified units (minimum / maximum; with two values there is no separate median):
- solve: 219.0 / 5577.2 s
- lrat-check: 51.0 / 155.6 s
- cake_lpr: 301.3 / 784.4 s
- proof size: 3.19 / 9.83 GB

P7_1-9 (the P7 subcase that hit its cap in the first wave) closed at 5577 s, under the 6000 s cap. Both proofs were deleted after checking; their sha256 values are in `out.jsonl`.

The largest solver RSS was 4424 MB (P6_1-3-15). There were no memory problems: free disk never went below about 18 GB.

No SAT, no proof rejection, no ERROR record.
