# review/: independent review of item s35_20-gate (started 22:50 KST, 22 Nov 2026)

Reviewer's work directory (the only place this review writes). Output: `VERIFY_s35_20-gate.md` here.
Units: `esr-s20-rv5-<job>` (track s20, budget 8,000 MB). No edits to the worker's files, no git, no campaign launch.

## Milestones

| # | check | state |
|---|---|---|
| R0 | this README | done 22:50 |
| R1 | pre-registration: timing, statement, hashes, expected leaves | done 22:53: README at 21:16:56 rebuilt from the worker transcript, sha256 = recorded 1aaae17c…; §3 unchanged since; first 3520 output 21:31:15 |
| R2 | statement of `RS3520.U2080.root` | done 22:54: my walker gives the same path; `rv_stmt` in R5 |
| R3 | pre-pass vs T7 | done 22:59: 0 mismatches (json), 8,080 gz sha256 = T7, 6 streamed counts = T7 (units esr-s20-rv5-gzhash, -gzhash2) |
| R4 | export binding | done 22:56 (`logs/rv_files.out`) |
| R5 | ONE compile (unit `esr-s20-rv5-ax`) | done 23:00: lean_rc 0, 34 s, 277 MB anon; all lines standard (`logs/RV3520.log`); provider audit `logs/rv_providers.out` |
| R6 | measurements | done (`logs/rv_files.out`) |
| R7 | controls | done |
| R8 | tools | done |
| R9 | LAUNCH_PLAN | done (one inconsistency: FVR_JOBS=4) |
| R10 | VERIFY_s35_20-gate.md | done 23:25 (gate confirmed except literal item 3 and the launch command; fixes in VERIFY §4) |
