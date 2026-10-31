# ES8SAT E02

TASK.md at commit b4c150e1, V = E02, H = 1.2. Build: `cc -O2 -o /opt/work/sat sat.c`; sat.c and witness8.txt match MANIFEST.sha256.

**Control** `/opt/work/sat sat witness8.txt 8`: `bad_candidates` 0, `faces_euler` = `faces_hit_by_valid_candidates` = 1,909,613 (48.0 s CPU). Full JSON in env.txt.

**Walkers** (seeds 201–204, deadline 1793436966 = start + 1.2 h − 12 min; commands in run.sh):

| seed | saturation tests (walk.log lines) | accepted moves | tries | min faces | max faces |
|---|---|---|---|---|---|
| 201 | 73 | 730 | 1104 | 1,910,504 | 1,911,642 |
| 202 | 73 | 730 | 1045 | 1,910,098 | 1,911,772 |
| 203 | 73 | 730 | 1100 | 1,910,123 | 1,911,669 |
| 204 | 74 | 740 | 1124 | 1,910,163 | 1,911,688 |

Total 293 exact saturation tests. Smallest face count seen: 1,910,098 (w202); largest: 1,911,772 (w202).

Lines with `bad` > 0 or `hit` ≠ `faces`: **none**. No ALARM, no ERROR lines. Every tested 64-point octagon-free set
was saturated: no point can be added without creating a convex octagon.
