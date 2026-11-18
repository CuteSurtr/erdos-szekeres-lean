# CONFIRMED: a second, independent cake_lpr run accepts the LRR(7) m = 15 LRAT (verifier VL, 15 Nov 2026, 21:19 KST)

**Verdict: CONFIRMED.** cake.out contains exactly one line, `s VERIFIED UNSAT`, and nothing else. The CNF SHA-256
and the SHA-256 and byte count of the streamed LRAT equal the claim (`claims/lrr7-m15-certified`). The certificate of
claim lrr7-m15-certified (label CERTIFIED) now rests on two cake_lpr acceptances: the main session's (heap 4500,
18:52-19:04) and this one (heap 4500, 21:05-21:19). Both used the same cake_lpr binary, but this run used VL's own
streaming and hashing script.

Scope: this run shows only that cake_lpr accepts this LRAT for the CNF with SHA-256 `651241db…`. It does not
re-check that the CNF encodes LRR(7) at |S| = 15. VB did that in VERIFY_LRR7_M15.md: byte-identical regeneration from
`lr_cnf.py 7 15`, the encoder read line by line, and semantic controls on 544 real sets.

## Command

Work dir V = `/home/jay/research/data/roadmap-20261115/pm1115/vl/` (VL's own).

```bash
systemd-run --user --unit=esr-mainv-vl-lrr7m15 -p CPUQuota=100% -p MemoryMax=5800M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=5078 --nice=10 -E OPENBLAS_NUM_THREADS=1 --working-directory=$V \
  /bin/bash $V/cake_stream.sh /home/jay/research/data/roadmap-20261115/pm1115/t1/lrr7/lrr7_m15.cnf \
  /home/jay/research/data/roadmap-20261115/pm1115/t1/lrr7/cert15/lrr7_m15.lrat.zst 4500 $V
```

- RuntimeMaxSec=5078 ends the unit at 22:30:00 at the latest; it was launched at 21:05:22.
- **Unit name deviation.** The task asked for `esr-agv-vl-<job>`. The memory guard `esr-memguard-ev15` caps the
  track `agv` at 3000 MB, but cake_lpr with a 4500 MB heap holds about 4.5 GB. The guard would have stopped this unit,
  or a VB unit in the same track. VL reported this before launching anything. At 21:03 the main session directed
  the track `mainv` (budget 6500 MB, no other mainv unit running, none to be started until VL finished). All other
  limits are as in the task.
- **Script:** `V/cake_stream.sh`, SHA-256 `cbf2abf47b99089279188d05542258c09442cbc2c33a8f5960e4515bfe5541bf`, written by
  VL. It is not certify_cnf.sh, nor the main session's or VB's scripts. Its core:
  ```bash
  sha256sum "$cnf" > cnf.sha256
  mkfifo lrat.fifo hash.fifo
  sha256sum < hash.fifo > lrat.sha256 &
  ( zstd -dc "$zst" | tee -p lrat.fifo hash.fifo | wc -c > lrat.bytes ) &
  /usr/bin/time -v -o cake.time /home/jay/.local/bin/cake_lpr --CML_HEAP_SIZE="$heap" "$cnf" lrat.fifo > cake.out 2> cake.err
  wait; rm -f lrat.fifo hash.fifo
  ```
  - The decompressed LRAT never touched disk. The hash and the byte count are of the exact stream cake_lpr read.
  - `tee -p` keeps feeding the hash if cake_lpr stops reading early. That did not happen here.
  - Both FIFOs are VL's own and were removed by the script.
- **cake_lpr binary:** `~/.local/bin/cake_lpr` → `/home/jay/research/sat/tools/cake_lpr/cake_lpr`, SHA-256
  `c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54`. The main session's cake.err names the same path
  `/home/jay/.local/bin/cake_lpr`.

## Results

| item | expected (claim) | this run |
|---|---|---|
| cake.out | exactly one line `s VERIFIED UNSAT` | `s VERIFIED UNSAT` (1 line, 17 bytes; exact-line count 1) |
| cake.err | — | empty (0 bytes) |
| CNF SHA-256 (computed at run time) | `651241dbc65d664730eb4f33e4d6f2c08a9e7c0c9c4918d2e076839749cda7f4` | `651241dbc65d664730eb4f33e4d6f2c08a9e7c0c9c4918d2e076839749cda7f4` |
| streamed LRAT SHA-256 | `99c38ea8e322246b3af60e2a8f04161f6fff5b5c7674462a1fe4a1896679d32c` | `99c38ea8e322246b3af60e2a8f04161f6fff5b5c7674462a1fe4a1896679d32c` |
| streamed LRAT bytes | 23,709,710,423 | 23,709,710,423 |
| exit codes | (cake_lpr exits 0 even on rejection) | cake_lpr 0; zstd, tee, wc 0 0 0 |
| wall time, cake_lpr (GNU time) | main session: 11:43.28 | 13:55.15 (user 729.67 s, sys 11.92 s, 88 % CPU) |
| peak RSS, cake_lpr (GNU time) | main session: 4,618,288 KB | 4,616,964 KB (about 4,509 MiB) |
| unit result | — | `Result=success`, `ExecMainStatus=0`; 21:05:22-21:19:17 |

- **Unit journal:** "Consumed 13min 55.027s CPU time over 13min 55.213s wall clock time, 5.6G memory peak".
  - The unit used its whole 100 % CPU quota, shared by cake_lpr and the zstd/tee/sha256sum/wc pipeline. That is why
    the run took longer than the main session's.
  - systemd's 5.6G peak includes page cache from streaming the 4.9 GiB `.zst`.
  - The anon peak, which is what the memory guard counts, was 4,517 MiB (sampled every 10 s). The guard's stop line
    for this unit is 95 % of 5800 MiB = 5,510 MiB. The guard logged only its LIFT line for this unit, no STOP. Swap: 0.

## Controls run before the job

1. **uutils `tee -p` (this machine's tee is uutils coreutils 0.10.0).** A FIFO reader closed after 1,000 bytes. The
   other outputs still received the whole stream: 50,000,000 bytes, and the SHA-256 equals a direct
   `sha256sum` (`ab46920a…`).
2. **Smoke test of the script** on root6_m10 (heap 2000, output in `V/smoke/`). It reproduced VB's recorded values
   (`vb/rerun/rerun.jsonl`): CNF `fc89445d…`, stream `011009062d1587ed…`, 134,186 bytes, `s VERIFIED UNSAT`.

## Files (V = `/home/jay/research/data/roadmap-20261115/pm1115/vl/`)

- `cake_stream.sh` (the script, hash above).
- `run.txt` (start/end, arguments, binary hash, exit codes, exact-line count).
- `cnf.sha256`, `lrat.sha256`, `lrat.bytes`, `cake.out`, `cake.err`, `cake.time`.
- `smoke/` (control 2).

The proof `t1/lrr7/cert15/lrr7_m15.lrat.zst` was only read. VL deleted and modified nothing outside V.
