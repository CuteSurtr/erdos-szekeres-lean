Level-15 pilot (N66 <= 54 would follow from UNSAT at L=15; HEURISTIC/COMPUTED only until certified).
Started 20 Nov 2026 by the main session: p2_batch.py (unchanged), warm = p2/s14/h2.json (660,810 quadruples, the base of
the CERTIFIED level-14 cube campaign), --tauclose --sb, default CaDiCaL options (expect SAT iterations), 0.6 thread.
Question: does the L=15 CEGAR keep finding models with violated quadruples (normal progress), or a model with none
(then the relaxation is SAT at 15 and N66 <= 54 needs new clause families)?
05:56 stopped by memguard (track n66 default 3000 MB; my oversight). 05:59 restarted as esr-n66-p15b from p.json (665,176 quads), track n66=6000 (total 24000 unchanged).
10:28 esr-n66-p15b reached its 4.5 h RuntimeMax during iteration 3 (COMPUTED so far: it1 SAT 2,406 s / 4,563 violated,
it2 SAT 7,216 s / 2,928 violated; it3 > 6,500 s unfinished). No SAT_MODEL. State: q.json (676,907 quads).
Leftover of the killed solve: p2/b15q/it3/cert.lrat (13.7 GB partial, certifies nothing) + cert.cnf (0.68 GB); kept
until the owner decides. Next: cube calibration cal15.sh (unit esr-n66-cal15, p2/cal15/), 10:33-18:10.
2026-11-20 12:35:54 deleted p2/b15q/it3/cert.lrat (13,713,108,992 bytes; partial LRAT of the solve killed at 10:28 by RuntimeMax, no verdict; owner OK ~12:25). cert.cnf (0.68 GB, regenerable from q.json) kept.
