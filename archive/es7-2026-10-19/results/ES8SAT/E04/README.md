# ES8SAT E04 (H = 1.2 h, task commit b4c150e1)

Control `sat sat witness8.txt 8`: bad_candidates = 0, faces_euler = 1909613, faces_hit_by_valid_candidates = 1909613, cpu 53.4 s (PASS). sha256 of sat.c and witness8.txt match MANIFEST.sha256.

Walkers: seeds 401-404, deadline epoch 1793436971 (08:56:11Z), 4 cores.

| seed | saturation tests (walk.log lines) | accepted moves | min faces | max faces | bad>0 | hit!=faces | ERROR lines |
|---|---|---|---|---|---|---|---|
| 401 | 64 | 640 | 1910186 | 1911527 | 0 | 0 | 0 |
| 402 | 64 | 640 | 1910128 | 1911745 | 0 | 0 | 0 |
| 403 | 64 | 640 | 1910156 | 1911699 | 0 | 0 | 0 |
| 404 | 64 | 640 | 1910248 | 1911717 | 0 | 0 | 0 |

Overall face counts: smallest 1910128, largest 1911745 over 256 exact saturation tests.

Lines with bad > 0 or hit != faces: none.

Result: no one-point extension without a convex octagon was found for any of the 256 tested 64-point octagon-free sets (no ALARM).
