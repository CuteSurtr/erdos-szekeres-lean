# PROOF NOT ACCEPTED 0s0-1s0_5_6 (07:44 UTC, --jobs 4): memory, not a real rejection
Driver record: lrat_check "c VERIFIED", cake_lpr "none" (no output). dmesg: memory cgroup OOM killed cake_lpr
(anon-rss 4 GB) while 4 workers were running cadical/checkers at once (15 GB VM, no swap).
Re-run alone (same CNF construction as close_tree.solve, cap 300, --sat):
sha 196b59d31e4b5987fd215efd7e489f3b529416c55de292d3243e32e99acb610a
['s UNSATISFIABLE'] 75.8 211243512
('c VERIFIED', 's VERIFIED UNSAT', True) 27.2
-> both checkers accept. Driver resumed with --jobs 3 (node re-solved by the driver, its record is in out.jsonl).
Note: after printing PROOF NOT ACCEPTED, close_tree.py returns inside the ProcessPoolExecutor block, whose exit
waits for every queued node of the batch and discards their results; I killed it at 07:55.
