# PROOF NOT ACCEPTED at 07:5x UTC: node 0s0-1s1_3s1-4s0_2_5 (re-checked alone)

Driver record: lrat_check "c VERIFIED", cake_lpr "none" (no output), while 4 jobs ran on 15 GB RAM
(each cake_lpr is started with CML_HEAP_SIZE=12000).

Re-run alone (same commands, same tools), with the driver stopped:
- node CNF from `gen_case.py 11 7 0s0-1s1_3s1-4s0_2_5`: sha256 5669c6e40563aace5318118b44d19cca8a386bb3677bcdba45dff419a1b454e4 (same as the driver record)
- cadical -q --sat --lrat --binary=false: s UNSATISFIABLE (5.7 s)
- lrat-check (E2 patch): c VERIFIED (2.2 s)
- cake_lpr (CML_HEAP_SIZE=12000 CML_STACK_SIZE=2000): s VERIFIED UNSAT (17.7 s), rc 0

Cause: memory (concurrent cake_lpr heaps), not a real rejection. Resumed with --jobs 3; the
driver re-solves and re-checks the node itself on resume (it is not in the certified set).
