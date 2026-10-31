# ES8SAT E06 (H = 1.2, Z = b4c150e1)

Control `/opt/work/sat sat witness8.txt 8`: bad_candidates 0, faces_euler = faces_hit_by_valid_candidates = 1,909,613 (cpu 48.0 s). Build: `cc -O2 -o /opt/work/sat sat.c`; sha256 of sat.c and witness8.txt match MANIFEST.sha256. Machine: 4 cores, 15 GB.

Walkers: seeds 601–604, 07:56:41 to 08:56:41 UTC (deadline 1793437001); each finished with 660 accepted moves.

| seed | saturation tests (lines) | tries | min faces | max faces | bad > 0 or hit ≠ faces | ERROR/ALARM lines |
|---|---|---|---|---|---|---|
| 601 | 66 | 959 | 1,910,062 | 1,911,795 | 0 | 0 |
| 602 | 66 | 991 | 1,910,011 | 1,911,622 | 0 | 0 |
| 603 | 66 | 955 | 1,910,131 | 1,911,760 | 0 | 0 |
| 604 | 66 | 980 | 1,910,251 | 1,911,608 | 0 | 0 |

Overall: 264 saturation tests, face counts from 1,910,011 to 1,911,795.

Lines with bad > 0 or hit ≠ faces: none.

No 64-point set along these walks admits a one-point extension without a convex octagon.
