# Additional certified cubes for 36 points

The 21 November evening run closed **4** of the 46 open cubes in case A of the 36-point $M(5;7)$ owner model. Its certified coverage rose from $37/64$ to **41/64** of the occupancy assignments. There are 42 open cubes. Case B has a separate complete certificate. The current upper bound for $M(5;7)$ is 36. [Previous mathematical statement and certificates](../M57R36N20261121/README.md) · [New leaves and proof hashes](leaves.tsv)

For each leaf, the solver used the previous case-A CNF and appended the listed occupancy units. The base SHA-256 is `aba65111d42151131a55e7596043721bd86fe94d05c8fea0b2750212d2808bbe`. CaDiCaL wrote an LRAT proof and cake_lpr returned `s VERIFIED UNSAT`. Each zstd-compressed proof was decompressed and matched to its raw hash. The raw files are in the Mac proof archive `es7-r36-20261121-evening`. [Checker outputs](cake) · [CNF and coverage checker](check.py)

Run `python3 check.py` in this directory to replay coverage of the earlier and new leaves. Pass `--base /path/to/c36_rle13.cnf --proofs /path/to/es7-r36-20261121-evening` to check all reconstructed CNF hashes and archived compressed proofs. The checker verifies that the previous verified and open leaves partition all 256 assignments to the split variables, and that the added leaves were on the previous open list.
