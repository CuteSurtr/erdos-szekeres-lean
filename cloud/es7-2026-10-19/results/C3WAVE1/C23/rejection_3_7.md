# PROOF NOT ACCEPTED on 0s0-1s1_2s0-8s0_3_7 (07:50 UTC): memory, not a real rejection

Driver record: lrat_check "c VERIFIED", cake_lpr "none" (empty stdout), --jobs 4.
Re-run alone (same CNF sha256 9eea20aa…f85, fresh CaDiCaL proof of 1,737,879 bytes, identical size):
- cadical: s UNSATISFIABLE (3.7 s)
- lrat-check (E2): c VERIFIED
- cake_lpr (CML_HEAP_SIZE=12000, CML_STACK_SIZE=2000): s VERIFIED UNSAT, rc 0, peak RSS 4.2 GB
Four cake_lpr at ~4.2 GB each exceed the 15 GB, no-swap VM, so the cause is memory.
The driver was stopped and resumed with --jobs 3 (as instructed). The node is re-solved and
re-checked by the driver on resume; only the driver's record counts.
dmesg confirms: cake_lpr invoked oom-killer at ~913 s uptime (07:50 UTC).
