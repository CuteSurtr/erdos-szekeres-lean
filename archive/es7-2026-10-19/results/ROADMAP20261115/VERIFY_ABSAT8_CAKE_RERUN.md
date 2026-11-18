**Verdict: CONFIRMED** (claim `absat8-l1-cake-rerun`, filed by L1; verifier V3, 15 November 2026, 13:59-14:02 KST).
cake_lpr accepted all 28 LRAT proofs for their CNFs, and each output holds exactly one `s VERIFIED UNSAT` line. Every
CNF and LRAT hash equals the record. The certificate part of claim `absat8-l1-indep` has now been re-run
independently, so its label CERTIFIED stands.

# Independent cake_lpr re-run for ABSAT8_INDEPENDENT (28 proofs)

**What was requested.** For each name in `$L1/names28.txt`:
1. decompress `cert/<name>.lrat.zst` into my own folder;
2. compare its SHA-256 with the expected value;
3. run `~/.local/bin/cake_lpr --CML_HEAP_SIZE=300 cnf/<name>.cnf <copy>`;
4. require exactly one `^s VERIFIED UNSAT$` line;
5. compare the CNF's SHA-256 with the expected value.

Here `$L1 = /home/jay/research/data/roadmap-20261115/pm1115/l1`.

**How it was run.**
- My own script `rerun.sh` ran in unit `esr-agy-v3-cake` with CPUQuota=15 %, MemoryMax=400M and MemorySwapMax=0,
  from 14:00:27 to 14:01:16 KST. The unit result was `success`.
- Each expected hash was taken from two places: `$L1/summary_l1.tsv` and the table in
  [ABSAT8_INDEPENDENT.md](ABSAT8_INDEPENDENT.md) §5, parsed from the record text. Each computed hash was compared
  with both.
- cake_lpr ran under `/usr/bin/time` to record peak RSS and exit status.
- I deleted my decompressed copies after each check. No other file was touched; the 28 `.zst` proofs are all still in
  place.

**Tools.** cake_lpr SHA-256 `c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54`, the same binary as
in the record (`c14ff498…`).

## Results (`rerun.tsv`)

| check | result |
|---|---|
| CNF SHA-256 = summary_l1.tsv and = record table | 28/28 and 28/28 |
| decompressed LRAT SHA-256 = summary_l1.tsv and = record table | 28/28 and 28/28 |
| exact lines `^s VERIFIED UNSAT$` per proof | exactly 1 in each of the 28 outputs (28 in total) |
| other output | none: each output file consists of that single line |
| cake_lpr exit status | 0 for all 28. The exit status is not evidence; the grep above is. |
| peak RSS | 310,072-310,396 KB, which is 76 % of the 400 MiB limit |

The proofs checked are those of ae_d0, ae_d1, ae_d15, ae_d23, ae_d27, ae_d29, ae_d30, ae_d57, c2_64points_k8,
c2_64points_k8_bb, ot0000, ot0174m, ot0341, ot0550, ot0682, ot0822, ot0977, ot1150, ot1313, ot1451, ot1588,
v2w21_last_set, v2w22_last_set, v3w31_last_set, v3w32_last_set, w1_last_set, w2_last_set and w3_last_set.

**Comparison with the author's second pass** (`$L1/logs/heaptest.log`, read afterwards). Both passes give the same
per-proof verdict, 1 line each, and the same LRAT hash prefixes. The peak RSS values agree to within 0.1 %.

**Scope.**
- This re-run confirms only the certificate step: each CNF is UNSAT, by cake_lpr.
- The encoder's soundness (§3), the 933 controls and the equivalence to absext were checked by V1 in
  VERIFY_ABSAT8_INDEPENDENT.md, not here.
- The geometric reading covers the 28 order types only, as the record states.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/v3/absat8-l1-cake-rerun/`)

| file | SHA-256 |
|---|---|
| `rerun.sh` | `a614539e88d22a6b3b3fa7bfcd96a7a70829fb2ecdf911ff7a6fc779d2cca3c7` |
| `rerun.tsv` (per proof: hash checks, line count, peak RSS, exit status, full LRAT SHA-256) | `0816683ee4e78e89ff3fec269d4f0989cbeef1e26ea6cd4cab529b9b4c99f82f` |
| `out/<name>.cake.out` and `out/<name>.time` | raw outputs |
| `env.txt` | cake_lpr hash and completion time |

Re-run: `systemd-run --user --unit=esr-agy-v3-cake -p CPUQuota=15% -p MemoryMax=400M -p MemorySwapMax=0
-p RuntimeMaxSec=1500 --nice=10 /bin/bash <folder>/rerun.sh`. It takes about 50 s of wall time at 15 % CPU.
