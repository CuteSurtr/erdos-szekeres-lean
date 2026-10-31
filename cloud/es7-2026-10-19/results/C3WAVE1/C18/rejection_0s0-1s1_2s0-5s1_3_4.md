# PROOF NOT ACCEPTED 0s0-1s1_2s0-5s1_3_4 (07:48 UTC): memory, not a real rejection

In the driver run (--jobs 4) the record had lrat_check "c VERIFIED" and cake_lpr "none".
dmesg: `Memory cgroup out of memory: Killed process 2892 (cake_lpr) total-vm:8391796kB,
anon-rss:4194304kB` (cgroup limit 14,343,688,192 bytes; four cake_lpr ran at once, ~4 GB each).
Re-run alone (same CNF sha256 275c682c..., same proof size 430,040 bytes): lrat-check
"c VERIFIED", cake_lpr "s VERIFIED UNSAT" (`recheck_0s0-1s1_2s0-5s1_3_4.json`).
Per the task, the driver was resumed with --jobs 3; the node is re-solved and re-checked by
the driver itself, so the closure record comes from the driver.
