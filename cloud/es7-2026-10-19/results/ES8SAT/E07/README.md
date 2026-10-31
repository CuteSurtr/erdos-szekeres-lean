# ES8SAT E07

Machine E07, 4 vCPU, budget H = 1.2 h, task commit b4c150e1. sat.c and witness8.txt matched MANIFEST.sha256.
Build: `cc -O2 -o /opt/work/sat sat.c`.

## Control
`/opt/work/sat sat witness8.txt 8`: bad_candidates = 0, faces_euler = faces_hit_by_valid_candidates = 1,909,613 (PASS).

```
{"N": 64, "K": 8, "lines": 2016, "parallel_pairs": 2098, "nonS_vertex_pairs": 1904030, "nonS_distinct_vertices": 1903444, "max_lines_through_nonS_vertex": 15, "faces_euler": 1909613, "faces_hit_by_valid_candidates": 1909613, "candidates": 7624184, "invalid_candidates": 4, "valid_candidates": 7624180, "cache_hits": 7610095, "dp_found": 14085, "dp_none": 0, "bad_candidates": 0, "cpu_seconds": 52.8}
```

## Walks
Seeds 701-704 ran from 07:57Z to deadline 1793437034 (08:57:14Z). See run.sh.

| walker | lines of walk.log | saturation tests | accepted moves | tries | min faces | max faces | non-JSON lines |
|---|---|---|---|---|---|---|---|
| w701 | 69 | 69 | 690 | 979 | 1,910,256 | 1,911,552 | 0 |
| w702 | 68 | 68 | 680 | 1017 | 1,910,196 | 1,911,620 | 0 |
| w703 | 68 | 68 | 680 | 1005 | 1,909,959 | 1,911,699 | 0 |
| w704 | 69 | 69 | 690 | 1005 | 1,910,115 | 1,911,736 | 0 |

Total saturation tests: 274. Face counts across all tests: smallest 1,909,959, largest 1,911,736.

## Lines with bad > 0 or hit != faces
None.

No ALARM and no ERROR lines. Every 64-point octagon-free set tested along these walks admits no one-point extension
without a convex octagon.
