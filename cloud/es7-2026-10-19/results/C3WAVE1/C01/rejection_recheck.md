# Proof rejection 0s0-1s0_2_3s0-8s1 (08:28 UTC): memory, not a real rejection

Record: status UNSATISFIABLE, lrat_check "c VERIFIED", cake_lpr "none" (no output), proof 49,488,887 bytes.
Cause: cake_lpr was OOM-killed (dmesg, uptime 2559-2617 s = 08:18-08:19 UTC, oom_dmesg.txt). At that time
my own heap test of cake_lpr ran beside the driver's 12 GB checks.
Re-run alone at 08:30 UTC: gen_case.py 11 7 0s0-1s0_2_3s0-8s1 -> sha256 8700009d...43e25 (same as the
record); cadical -q -t 300 --sat --lrat --binary=false -> s UNSATISFIABLE, proof 49,488,887 bytes;
controls.dual -> ('c VERIFIED', 's VERIFIED UNSAT', True), 18.9 s.
The driver re-solves and re-checks the node on resume (it counts only via that new record).
