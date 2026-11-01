# ES8SAT E03 results

Task: `TASK.md` at commit b4c150e1, V = E03, H = 1.2. Built with `cc -O2 -o /opt/work/sat sat.c`. The sha256 of sat.c and witness8.txt matches MANIFEST.sha256.
Machine: 4 vCPU, 15 GB RAM (see env.txt). Walkers ran from 07:57 to about 08:58 UTC (deadline epoch 1793437020).

**Control** (`sat sat witness8.txt 8`): bad_candidates = 0, faces_euler = 1909613, faces_hit_by_valid_candidates = 1909613, cpu 52.9 s. PASS.

| walker | saturation tests (walk.log lines) | accepted moves | tries | min faces | max faces | lines with bad>0 | lines with hit≠faces | ERROR/ALARM lines |
|---|---|---|---|---|---|---|---|---|
| w301 | 64 | 640 | 958 | 1910185 | 1911622 | 0 | 0 | 0 |
| w302 | 64 | 640 | 1008 | 1910440 | 1911390 | 0 | 0 | 0 |
| w303 | 64 | 640 | 936 | 1910012 | 1911651 | 0 | 0 | 0 |
| w304 | 64 | 640 | 920 | 1909971 | 1911578 | 0 | 0 | 0 |

Total: 256 exact saturation tests. Across all walkers the face counts range from 1909971 to 1911651.

Lines with `bad` > 0 or `hit` ≠ `faces`: none.

Result: none of the 256 octagon-free 64-point sets visited admits a one-point extension without a convex octagon. Each walker finished normally (`done` line in its stdout).
