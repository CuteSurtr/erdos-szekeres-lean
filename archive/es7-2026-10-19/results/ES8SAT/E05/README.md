# ES8SAT E05 (H = 1.2, task commit b4c150e1)

- Build: `cc -O2 -o /opt/work/sat sat.c` (gcc 13.3.0); `sha256sum sat.c witness8.txt` matches `MANIFEST.sha256`.
- Machine: 4 CPUs, 15 GB RAM (see env.txt).
- Control `sat sat witness8.txt 8`: `bad_candidates` 0, `faces_euler` = `faces_hit_by_valid_candidates` = 1,909,613
  (53.0 s CPU). Pass.
- Walkers: seeds 501–504, start 07:56:50Z (epoch 1793433410), deadline 08:56:50Z (epoch 1793437010); all exited normally.

| seed | saturation tests (walk.log lines) | accepted moves | tries |
|------|-----------------------------------|----------------|-------|
| 501  | 63 | 630 | 918 |
| 502  | 64 | 640 | 913 |
| 503  | 64 | 640 | 953 |
| 504  | 64 | 640 | 969 |
| total | 255 | | |

- Face counts over all 255 tests: smallest 1,910,152, largest 1,911,800.
- Lines with `bad` > 0: none. Lines with `hit` ≠ `faces`: none. No `ALARM`, no `ERROR` lines.

Result: none of the 255 octagon-free 64-point sets tested admits a one-point extension without a convex octagon.
