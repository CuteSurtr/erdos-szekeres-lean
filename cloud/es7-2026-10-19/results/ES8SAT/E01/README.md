# ES8SAT E01 (H = 1.2, task commit b4c150e1)

Control `sat sat witness8.txt 8`: bad_candidates = 0, faces_euler = 1909613, faces_hit_by_valid_candidates = 1909613, cpu 46.2 s. PASS.

Machine: 4 cores, 15 GB; build `cc -O2 -o /opt/work/sat sat.c` (gcc 13.3.0); sha256 of sat.c and witness8.txt match MANIFEST.sha256.

| walker | saturation tests (walk.log lines) | accepted moves | min faces | max faces | bad>0 | hit≠faces | other lines |
|---|---|---|---|---|---|---|---|
| w101 | 74 | 740 | 1909948 | 1911593 | 0 | 0 | 0 |
| w102 | 74 | 740 | 1910423 | 1911704 | 0 | 0 | 0 |
| w103 | 73 | 730 | 1910305 | 1911806 | 0 | 0 | 0 |
| w104 | 74 | 740 | 1910222 | 1911502 | 0 | 0 | 0 |

Total 295 exact saturation tests; face counts ranged from 1909948 to 1911806.

Lines with bad > 0 or hit ≠ faces (or ALARM/ERROR): none.

Every tested 64-point octagon-free set admitted no one-point extension without a convex octagon.
