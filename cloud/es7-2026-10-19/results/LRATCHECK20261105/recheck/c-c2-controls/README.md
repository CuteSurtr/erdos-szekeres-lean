# c-c2-controls: cake_lpr re-check of the C/C2 mirror-encoding controls (5 Nov 2026)

**Result: all 7 controls are UNSAT, and cake_lpr printed `s VERIFIED UNSAT` for all 7.** The controls are m9k5,
hm9k5, m9k5.sub, m17k6, hm17k6, m17k6.sub and hm17k6.sub.

Claim checked: `C/logs/part1_controls.log` and `C2/logs/part1_controls.log`. Those 7 CNFs are UNSAT, and before this
re-check the claim rested on lrat-check only, with pre-E2 builds.

## Hash binding (caveat)

**Neither `results/C` nor `results/C2` records a SHA-256 for any CNF.** Mi-0/README.md and Mii-3/README.md say the
same.
- I regenerated all 22 CNFs with the record's own generator: `bash results/C/scripts/make_cnfs.sh gen`, which runs
  `tools/etv/gen_etv.py` and `C/scripts/mirgen.py` (`make_cnfs.log`).
- All 22 hashes are identical to `results/Mi-0/logs/cnf_sha256.txt` and `results/Mii-3/logs/cnf_sha256.txt`
  (`gen_cnf_sha256.txt`). Those were also produced by `C/scripts/make_cnfs.sh`.
- For the 7 controls, `cnf_hash_match` therefore means a full-hash match to those sibling records, not to C/C2
  themselves.
- The variable and clause counts that C and C2 do record match (hm33k7 47,002 / 684,494; m33k7 47,002 / 684,478;
  hm33k7.sub 535,454; m33k7int.sub 515,121).

## Check

- `run_one.sh` copies each CNF into `runs/` and runs `cadical --lrat --binary=false -q X.cnf X.lrat`.
- It then runs `cake_lpr --CML_HEAP_SIZE=12000 X.cnf X.lrat > X.cake.log`.
- The verdict is `grep -qx 's VERIFIED UNSAT'`. lrat-check was not used.
- Proofs were 3–64 KB, and all 7 runs took about 1 s in total (13:23 KST).

## Files

- `results.tsv`.
- `runs/X.*`: the artifacts, with `X.hashes.txt`.
- `gen/`: all 22 generated CNFs and their JSON, with `gen/hashes.txt`.
- `aux_hashes.txt`: the scripts and logs.
