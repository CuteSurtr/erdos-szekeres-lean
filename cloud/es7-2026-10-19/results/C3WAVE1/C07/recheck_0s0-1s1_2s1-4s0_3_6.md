# Re-check of 0s0-1s1_2s1-4s0_3_6 (PROOF NOT ACCEPTED at 08:01 UTC)

Driver record: status UNSATISFIABLE, proof 21,101,284 bytes, lrat_check "c VERIFIED", cake_lpr "none" (no output).
Cause: memory. dmesg: "Memory cgroup out of memory: Killed process 3613 (cake_lpr) total-vm:8391796kB, anon-rss:3820672kB"
(4 solver/checker jobs in parallel; cake_lpr at a36874a uses its default 4096 MB heap + 4096 MB stack).

Re-run alone (08:03:00 UTC): gen_case.py 11 7 0s0-1s1_2s1-4s0_3_6 -> sha256 4c409bc0515ab58bc1f45d4252260e001153e5e8f036250ef1cb6c2d07d1ecaa (= record);
cadical -q -t 600 --sat --lrat --binary=false -> s UNSATISFIABLE, proof 21,101,284 bytes (identical size);
lrat-check (E2) -> c VERIFIED; cake_lpr -> s VERIFIED UNSAT.
Not a real rejection. The driver was resumed with --jobs 3 (it re-solves and re-checks this node itself, so the certified record comes from the driver).
