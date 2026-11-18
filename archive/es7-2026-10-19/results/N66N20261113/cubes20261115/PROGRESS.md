# N66 level-14 cube campaign: progress at the stop (15 November 2026, driver ended 09:29:33 KST)

**Status: N66 ≤ 55 is NOT decided. N66 ≤ 56 (level 13, CERTIFIED, parent README §9) remains the bound.** At the stop, **33 of the 70 leaf cubes are CERTIFIED**, each with its full certification path (§1) re-checked here (§2); 37 leaves are open. By measure the certified cubes make up 32 of the 64 base cubes (50.0 %). 6 cubes reached their CaDiCaL time limit and were re-split. No cube was SAT. Nothing is committed.

The campaign ended before its 09:40 deadline. The driver starts no cube after 09:24 (the deadline minus 960 s), and the cubes started last got CaDiCaL limits shortened to fit the deadline: ohhooh at 09:10:08 with 1132 s (certified), ohhoho at 09:21:30 with 449 s (split), ohohho_23h at 09:23:07 with 352 s (split), ohhhoo at 09:23:52 with 307 s (split). When the last of them ended, the driver wrote its final status at 09:29:33 and exited. No esr-n66-* unit has been running since then.

Written 09:31 KST, 15 November 2026, by the monitoring step, after every esr-n66-* unit had ended; the driver's final status was written at 09:29:33 KST (final = True). W = `/home/jay/research/data/n66-20261113`. Sources: `W/p2/c14/campaign_status.json`, the certificate directories `W/p2/c14/<id>/it<k>/`, `journalctl --user` (systemd CPU accounting) and the memguard log `/home/jay/research/data/es308-20261114/memguard-s18.log`. The per-cube status table is `STATUS_campaign.md` in this folder; the model, the cover argument and the acceptance rules are `README.md` §2 and §6 (written 05:44, before the campaign; its note that cube B is not yet a certified cube is superseded: cube B = hhhhhh is certified below).

Labels: **CERTIFIED** = CaDiCaL 2.1.3 LRAT proof accepted by cake_lpr (`s VERIFIED UNSAT`, grepped) for the stated CNF, hashes recorded; **COMPUTED** = solver verdict only; **HEURISTIC** = timings and estimates.

Corrections to `README.md`, which stays unedited under the new-files-only rule:

- Cube B (hhhhhh) is now a certified cube (§3).
- The pilot's row count is 392, not "392 or 393". The critic counted the pilot's used_ids.txt directly. This run's own core of cube B also has 392 rows, but it comes from a different CNF and proof, so it does not settle the pilot count by itself.
- The folder no longer holds only the README. It also has STATUS_campaign.md (the driver's status), tools/ and this file.

## 1. What counts as a certified cube

A cube fixes the signs of the split states 25 12 16 29 17 37 (o = occupied = +sel_s, h = hole = −sel_s, sel_s = DIMACS variable 988541 + s), followed by `_<s><o|h>` for each re-split state. A cube counts only with its full certification path, run in its own unit esr-n66-cube-<id> and certificate directory:

1. CaDiCaL 2.1.3 (`--unsat -t T --lrat=true`) exits 20 on cert.cnf, which is the level-14 CNF with the cube's units (p2_write.py; the layout's `cube` field is the cube);
2. p2_lrat_trim keeps the cone of the empty clause: trim.cnf (the used original clauses) and trim.lrat;
3. `/home/jay/.local/bin/cake_lpr` on trim.cnf and trim.lrat prints the exact line `s VERIFIED UNSAT` (cake.out);
4. every used row is justified: p2_template_cert66 (0 unjustified), final_verify66 (bad 0, rows_match), link re-check ALL_OK;
5. p2_verify ALL_OK: every distinct clause of trim.cnf is a mono66 clause, a fixed or cube unit, a justified row, a counter clause or an SB clause (0 unclassified);
6. cert.json ALL_OK, and the driver's accept() (README §6: L = 14, W = range(70), the 27 SB pairs of b14h2, the cube in layout, verify and cert equal to the planned cube, trim.cnf hash recomputed).

By README §2, certificates for every leaf of a cover would make the level-14 relaxation UNSAT and give N66 ≤ 55, after an independent check.

## 2. Re-check of the certified cubes (this step)

`tools/progress_chk.py` (new; glue around sha256sum and zstd, run as units esr-vfy-n66prog*, CPUQuota 200 %, MemoryMax 1G, MemorySwapMax 0, nice 10) re-read the files of every cube with status certified. It required all of the following:

- cake.out contains the exact line `s VERIFIED UNSAT` exactly once;
- the timed command in cake.err is `/home/jay/.local/bin/cake_lpr` on that directory's trim.cnf and trim.lrat;
- sha256sum of trim.cnf and of trim.lrat, recomputed, equal cert.json, verify.json and the driver status;
- `zstd -dc trim.lrat.zst | sha256sum` equals the trim.lrat hash;
- cert.json and verify.json are ALL_OK, with 0 unclassified clauses;
- the kinds add up to the distinct clauses, and the clause count equals the trim.cnf header and cert.json;
- L = 14, W = 70 states, the sel range, bound 55, the cube equals the plan and the SB pairs equal b14h2's;
- rows: used = justified = final_verify66 rows, bad 0 and rows_match, every template and core verified, link re-check ALL_OK;
- cadical.log has `Version 2.1.3`, `exit 20` and `s UNSATISFIABLE`;
- pipeline.log has every step and ends with P2_CERT_DONE.

**Result: 33 of 33 certified cubes pass every check**.
This is not the independent VERIFY that the house rules require. That VERIFY still has to re-run cake_lpr, check that trim.cnf is a subset of cert.cnf, and check rows and geometric clauses with its own encoder (§8).

## 3. Certified cubes (33)

Hashes are SHA-256. The cake_lpr column is the line in `<certdir>/cake.out`, matched exactly. trim.lrat is kept, and so is trim.lrat.zst (round trip checked). p2_cert.sh deleted the untrimmed LRAT after cake_lpr accepted the trimmed one; its hash is in cert.lrat.sha256. The full cube CNF cert.cnf is kept. The certificate directory is `W/p2/c14/<id>/it1/` for every cube below. The 8 cubes that unit propagation refutes have identical trimmed files: their core uses only the units 25h, 29o and 37h, which they share, plus SB clauses.

| # | cube | holes | rows | trim clauses | trim.cnf SHA-256 | trim.lrat SHA-256 | cake_lpr | heap MB / s |
|---|---|---|---|---|---|---|---|---|
| 1 | hhhhhh | 6 | 392 | 31,613 | `da037243e51599d602777df0aac2443f25e65248a4adc45246ecf45ab555553d` | `ef428accb834c028530bf8517a19e3e833b862c08e71c85fc9df3592beab24a0` | `s VERIFIED UNSAT` | 2000 / 0.8 |
| 2 | hhhohh (UP) | 5 | 0 | 6 | `06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06` | `e1d1b3fce3125b73cd384e9592263e40df93d76fcb0be96c8ebcb0fe583c5c91` | `s VERIFIED UNSAT` | 2000 / 0.0 |
| 3 | hohohh (UP) | 4 | 0 | 6 | `06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06` | `e1d1b3fce3125b73cd384e9592263e40df93d76fcb0be96c8ebcb0fe583c5c91` | `s VERIFIED UNSAT` | 2000 / 0.0 |
| 4 | hhoohh (UP) | 4 | 0 | 6 | `06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06` | `e1d1b3fce3125b73cd384e9592263e40df93d76fcb0be96c8ebcb0fe583c5c91` | `s VERIFIED UNSAT` | 2000 / 0.0 |
| 5 | hhhooh (UP) | 4 | 0 | 6 | `06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06` | `e1d1b3fce3125b73cd384e9592263e40df93d76fcb0be96c8ebcb0fe583c5c91` | `s VERIFIED UNSAT` | 2000 / 0.0 |
| 6 | hooohh (UP) | 3 | 0 | 6 | `06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06` | `e1d1b3fce3125b73cd384e9592263e40df93d76fcb0be96c8ebcb0fe583c5c91` | `s VERIFIED UNSAT` | 2000 / 0.0 |
| 7 | hohooh (UP) | 3 | 0 | 6 | `06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06` | `e1d1b3fce3125b73cd384e9592263e40df93d76fcb0be96c8ebcb0fe583c5c91` | `s VERIFIED UNSAT` | 2000 / 0.0 |
| 8 | hhoooh (UP) | 3 | 0 | 6 | `06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06` | `e1d1b3fce3125b73cd384e9592263e40df93d76fcb0be96c8ebcb0fe583c5c91` | `s VERIFIED UNSAT` | 2000 / 0.0 |
| 9 | hooooh (UP) | 2 | 0 | 6 | `06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06` | `e1d1b3fce3125b73cd384e9592263e40df93d76fcb0be96c8ebcb0fe583c5c91` | `s VERIFIED UNSAT` | 2000 / 0.0 |
| 10 | ohhhhh | 5 | 537 | 95,017 | `f4ed31b1c2c2b11d353a63cc086d63238c49873c634df0b7e230fa25c96cf427` | `a8ab4c3739f933a42f88a67e1ff03e72983974e962c274901cb9d0a4b68c44ef` | `s VERIFIED UNSAT` | 2000 / 5.0 |
| 11 | hohhhh | 5 | 543 | 57,214 | `a3b1cc463cade60cdccc54a562e273dbe557067e856a01e780d9054fda60f4fc` | `d4cc545fa8363f07cf6afd24e451e3e0fd4ed46ed3ee836f6d4635eea9b2862b` | `s VERIFIED UNSAT` | 2000 / 2.4 |
| 12 | hhohhh | 5 | 557 | 51,048 | `b2df3fab3470e23e5ab2f557e8f52f76b36f0aa9cca646109916fb24148ece01` | `cfb721feaf23645ff62486ee02f4ed571fe7c3fae61576d6a7fae508ab22f49c` | `s VERIFIED UNSAT` | 2000 / 2.4 |
| 13 | hhhhoh | 5 | 605 | 62,638 | `6c2076079b922e06d55ddd3f40cb358528069971b684cc7e822e96670e74d66d` | `8660863ebfad0dab18d9b8e1291f4ea27bc77ffc18ac63787afe15b626445c6b` | `s VERIFIED UNSAT` | 2000 / 2.3 |
| 14 | hhhhho | 5 | 1153 | 100,104 | `2197e250693fb9f289086bce02def5b5fa164ed217bcfbdec57dd32c84fd6270` | `06e51fec5e35f5330dda44336c54e9407f3bc45adecb582a1a529f21a2a936ed` | `s VERIFIED UNSAT` | 2000 / 4.9 |
| 15 | oohhhh | 4 | 646 | 148,676 | `2cfd5245366ff0bb8b548bb95070d4d19df40fe1b1881d9f6aea4b97a7d828e5` | `a295c531aa3f76d87d2902ff41f7c53484dd471d336fb3e638d0de37ec599ce3` | `s VERIFIED UNSAT` | 2000 / 12.7 |
| 16 | ohohhh | 4 | 668 | 134,617 | `ce461d2088b60e3d57aeaebe25d179708ef620ce07c58128b9d2d26cb358d7c5` | `7e76e0715d4df22abf19fa22f11cb9f91c9b344b82cbc7bf21d478bba2e407b8` | `s VERIFIED UNSAT` | 2000 / 12.2 |
| 17 | ohhohh | 4 | 754 | 110,597 | `662816b28ce9b4ff4f573a6e1376d83f0ac9dc84606734b9037151870296ccd0` | `f03dcda35a241ece50592f4f51a7f4d20e8c209ad8e38a90fe5188c268fa3d58` | `s VERIFIED UNSAT` | 2000 / 6.8 |
| 18 | ohhhoh | 4 | 687 | 128,902 | `ade600c5536be38932228cff766f6f938db7d28f1268293d75f835a1e89f4e61` | `1aa46cf8d86c83bb053fa7a65306b7e96802d05b951fff4e7b53d6efe70db286` | `s VERIFIED UNSAT` | 2000 / 11.8 |
| 19 | ohhhho | 4 | 1414 | 174,224 | `6529d3e1e6b2eef5a9769f31cb9e2a64c722a3c058c7b8c5bbbd7b901d41366c` | `59a3889a708fceb2d78d8b946c1a0afca9b6b8bf518f365bfa74e18e22bd013b` | `s VERIFIED UNSAT` | 2000 / 18.6 |
| 20 | hoohhh | 4 | 843 | 69,611 | `6dfc85318407c9aced860d618bd5e0efb8f328dc164f4f367646a018fbe51b31` | `10dae99d3511a2fec58820d20f61fa1d491427a2a37e3a502ec98a1b423b5e2b` | `s VERIFIED UNSAT` | 2000 / 4.5 |
| 21 | hohhoh | 4 | 692 | 111,643 | `acdac32079fab7e6550ea5d60e8d188f0f9299bfd232b35992ea0a868e9dca9b` | `58ce6e44447c09d6ef2492b12f97c6ad4c03776011731dfbb3b80d4d97d65f60` | `s VERIFIED UNSAT` | 2000 / 7.2 |
| 22 | hohhho | 4 | 1286 | 154,473 | `f06d3c60f3289a8fa4f34c6f2a82666f0f7bcf887c0d280b622aa836d4bf2160` | `0aff2e5f7b53e98eb3a38267f87b02e5fd63b231a68e64d5bb67b1920069623d` | `s VERIFIED UNSAT` | 2000 / 11.9 |
| 23 | hhohoh | 4 | 678 | 102,178 | `422a3f17b59b90f414911282d8ab1915f6fb8b10435957de83679e18621baff9` | `792c328abbe18f3e6ab1379e5442bbcbf6b64a194d1e11cf80a264b0a0bb3a82` | `s VERIFIED UNSAT` | 2000 / 8.2 |
| 24 | hhohho | 4 | 1418 | 137,403 | `743c2e2977b8214e8a5e20889c922a1088a905bde8d9d9767af2afbf86d4f62b` | `a5887bdf7fe494419b6fb93afd83afde6612207cd6fd14c914df1db39c45eef9` | `s VERIFIED UNSAT` | 2000 / 12.3 |
| 25 | hhhoho | 4 | 830 | 105,313 | `fbd1ae5cb7aef79e217dcef0e82608d51a1c168fb5f9fd7df82f01f3a4cf45d6` | `2785c26f3b7bc04c5eede664954a8d4246fb635574fd78109dbb8fab7b54835d` | `s VERIFIED UNSAT` | 2000 / 6.1 |
| 26 | hhhhoo | 4 | 1185 | 170,987 | `15aeef7a17efd20897e9c38c763843f9555f1c37b645cd4f494033f63a26008c` | `7f4e43411cc72436ffb0a13323b3a4b3fa121fa18d449f351291a23181f8c668` | `s VERIFIED UNSAT` | 2000 / 16.1 |
| 27 | oohhoh_23h | 4 | 730 | 121,909 | `34c151d02a9a11fbbb325a39b0f0d8076548225a871bda511a1201673694b75b` | `97b6ee7229c5c57de68a07aa21b173337bca82e468284dce06dd14cf80abeb81` | `s VERIFIED UNSAT` | 2000 / 8.8 |
| 28 | oohhho_23h | 4 | 1362 | 154,293 | `70ed97914d325e3cfccc5e6e9a9efcb031292413a5df8f58eb5897db273f9df5` | `9fd9443e11aa37ddd79d03e5c32e7928f5b3f283df8f945881ee6255ea777604` | `s VERIFIED UNSAT` | 2000 / 13.6 |
| 29 | ooohhh | 3 | 1034 | 171,148 | `eaf17517f00d3fc66c3ea542e06850e42c3ec09b31e3f9b45ffa251a0a6efd3d` | `462f6c30e41321fee9acf856bb5542c659c6aacaef87887f6b19ebaafc6ca15b` | `s VERIFIED UNSAT` | 2000 / 22.5 |
| 30 | oohohh | 3 | 858 | 165,315 | `b591c12ca269031435f7b588534b11137004bfd4a36c42d030ea541954bda3e3` | `73a440924195eff80bf7f38695e86b24db3a6638eda7d6442b7ff15114113ecf` | `s VERIFIED UNSAT` | 2000 / 15.9 |
| 31 | ohoohh | 3 | 993 | 159,613 | `1ababa5fcbb22112bbab2c8c1763a72f57143a881294bd8f33772a260751796b` | `b9bff56da10c604713308cce71731e02dd529b0920b3dea648b8c25f128e5ccb` | `s VERIFIED UNSAT` | 2000 / 14.4 |
| 32 | ohohoh | 3 | 1004 | 190,102 | `6ea976558f2382ac54b83160d1f615237f7f22246d6063fe5c9990330d3df7e5` | `de85e8aaebc68aa047e88a27bb10d1e84682d80e93bcbc0b1cd8bf14306c305c` | `s VERIFIED UNSAT` | 2000 / 26.0 |
| 33 | ohhooh | 3 | 1008 | 130,466 | `562aa43412a5b0a2a5c39a382039b613f1b2eb6d9cc102f14a69dfd9292a3083` | `8c54dab7890bf513e43cee89f4c073dc203c46d24a8b4d72e28fb1a1fddf4e88` | `s VERIFIED UNSAT` | 2000 / 9.4 |

## 4. Open cubes (37)

- **queued, never started (37):** 5 holes (1): ohohho_23h_49h; 4 holes (3): ohhoho_23h, ohhhoo_23h, ohohho_23h_49o; 3 holes (12): hoohoh, hoohho, hohoho, hohhoo, hhooho, hhohoo, hhhooo, oohhoh_23o, oohhho_23o, ohohho_23o, ohhoho_23o, ohhhoo_23o; 2 holes (14): oooohh, ooohoh, ooohho, oohooh, oohoho, oohhoo, ohoooh, ohooho, ohohoo, ohhooo, hoooho, hoohoo, hohooo, hhoooo; 1 hole (6): oooooh, ooooho, ooohoo, oohooo, ohoooo, hooooo; 0 holes (1): oooooo.

## 5. Re-splits (6)

When a cube's CaDiCaL run reaches its time limit without a verdict, the driver replaces the cube by its two children: c with s occupied and c with s hole, where s is the first state of 23 49 44 40 20 32 46 45 52 35 30 39 not already in c. The two children cover the parent.

| cube | started | limit s | CaDiCaL conflicts | CaDiCaL process s | split on | children (status) | partial files deleted |
|---|---|---|---|---|---|---|---|
| ohohho_23h | 09:23:07 | 352 | 483,833 | 348.3 | 49 | ohohho_23h_49o (queued), ohohho_23h_49h (queued) | 2.31 GB |
| oohhoh | 08:22:01 | 1200 | 3,497,409 | 1174.55 | 23 | oohhoh_23o (queued), oohhoh_23h (certified) | 4.18 GB |
| oohhho | 08:31:34 | 1200 | 3,244,346 | 1171.95 | 23 | oohhho_23o (queued), oohhho_23h (certified) | 4.13 GB |
| ohohho | 09:02:43 | 1200 | 3,804,976 | 1173.94 | 23 | ohohho_23o (queued), ohohho_23h (split) | 4.43 GB |
| ohhoho | 09:21:30 | 449 | 708,164 | 440.19 | 23 | ohhoho_23o (queued), ohhoho_23h (queued) | 2.53 GB |
| ohhhoo | 09:23:52 | 307 | 347,745 | 300.83 | 23 | ohhhoo_23o (queued), ohhhoo_23h (queued) | 2.05 GB |

- Splits after a shortened limit (deadline): ohohho_23h (352 s), ohhoho (449 s), ohhhoo (307 s); such a cube was split, not retried at 1,200 s.
- The driver's finalize() deleted the partial cert.lrat and cert.cnf of each timed-out run, 19.64 GB in total. These files were written by this campaign and are not part of any certificate. The critic flagged the deletion as an owner question (issue 1, 06:46), because AGENTS.md makes deleting large proof material ask-first. The running driver was not changed.

## 6. Cover

- **Leaves: 70**, which is the 64 base cubes, minus 6 split parents, plus 12 children. Own brute-force check (progress_chk.py) over all 2^8 = 256 assignments of the 8 states that occur (12 16 17 23 25 29 37 49): **0 uncovered**. The roots are exactly the 64 sign patterns of 25 12 16 29 17 37 (yes). Each split parent's two children are the parent with s occupied and with s hole (yes). The driver's own check agrees: COVER_OK.
- **Certified: 33 leaves. Certified cover NOT complete.** 128 of the 256 assignments satisfy no certified cube, with each cube's literals read from its verify.json. By measure the certified cubes make up 32 of the 64 base cubes. Open: 37 leaves, measure 32.

## 7. Resource use

- **Units.** 39 cube units ran (esr-n66-cube-<id>), plus esr-n66-driver. Each cube unit had 1 thread (CPUQuota 98 %), MemoryMax 3.6G, MemorySwapMax 0, nice 10 and a RuntimeMaxSec ending by 09:39. The memguard lifts the kernel limit, keeps memory.high = 3.6G as a brake, and stops a unit at 95 % of 3,686 MiB counted as anon plus swap. The driver unit had 6 % and 300M. At most 3 cubes ran at once: 3 × 98 % + 6 % = 3.0 threads of the 16-thread cap.
- **CPU** (systemd accounting from the journal): 7.04 CPU-h in cube units. Of that, 5.74 CPU-h went to the certified cubes and 1.30 CPU-h to the 6 runs without a verdict. Driver: 65 s CPU over 3.51 h.
- **Memory.** Highest anon of a cube unit (driver samples every 15 s): 3251 MB. Highest CaDiCaL maximum resident (cadical.log): 2622 MB. Highest cake_lpr maximum RSS: 2006 MB (heap 2000 MB, ohhhoh); every accepted run used the 2000 MB heap tier. **Above 80 % of MemoryMax (2,949 MiB) in the anon samples: hohhoh 3,156 MiB (86 %), hhohoh 3,139 MiB (85 %), ohohoh 3,251 MiB (88 %)** (a breach of the 80 % sizing rule; no guard stop, no OOM kill). No unit reached the guard's 95 % stop (3,502 MiB, checked every 0.25 s): the memguard log has 0 STOP lines for esr-n66 units today, and there are no `W/MEMGUARD_STOPPED_esr-n66-*` files. systemd's "memory peak 3.6G" figures count page cache held under the memory.high brake, so they are not anon. The 15 s samples can miss short peaks (critic issue 3).
- **Disk.** `W/p2/c14` holds 37.11 GB. That includes 11.47 GB of trimmed LRATs, 2.62 GB of zstd copies and 33 full cube CNFs (cert.cnf, about 664 MB each). Partial files deleted at re-splits: 19.64 GB.
- **This step:** 4 re-check units (esr-vfy-n66prog1 16 s CPU, esr-vfy-n66prog2 no accounting line (under 1 s), esr-vfy-n66prog3 4 s CPU, esr-vfy-n66prog5 3 s CPU); 1-2 threads each, at most 1G.

Per cube: the unit CPU comes from systemd. wall s is the driver's, from the start of p2_batch_cube.py to the end of p2_cert.sh. Anon is the driver's 15 s samples. CaDiCaL RSS is the maximum resident in cadical.log. cake is the maximum RSS from /usr/bin/time.

| cube | status | started | wall s | unit CPU s | CaDiCaL conflicts | CaDiCaL RSS MB | anon peak MB | cake RSS MB |
|---|---|---|---|---|---|---|---|---|
| hhhhhh | certified | 05:50:37 | 234.2 | 234 | 109,509 | 2419.2 |  | 1325 |
| hhhohh | certified | 05:59:17 | 45.1 | 45 |  | 1328.39 | 499 | 37 |
| hohohh | certified | 05:59:20 | 45.4 | 45 |  | 1329.29 | 497 | 37 |
| hhoohh | certified | 06:00:09 | 46.9 | 46 |  | 1329.8 | 497 | 37 |
| hhhooh | certified | 06:00:13 | 46.9 | 46 |  | 1329.18 | 497 | 37 |
| hooohh | certified | 06:01:02 | 50.3 | 50 |  | 1329.92 | 498 | 37 |
| hohooh | certified | 06:01:05 | 51.1 | 50 |  | 1330.41 | 498 | 37 |
| hhoooh | certified | 06:01:54 | 47.4 | 47 |  | 1329.93 | 496 | 36 |
| hooooh | certified | 06:02:13 | 45.0 | 44 |  | 1331.08 | 496 | 37 |
| ohhhhh | certified | 06:02:47 | 529.8 | 519 | 601,323 | 2441.84 | 2474 | 2003 |
| hohhhh | certified | 06:03:06 | 405.9 | 398 | 307,741 | 2430.66 | 2182 | 2003 |
| hhohhh | certified | 06:10:02 | 404.5 | 396 | 304,216 | 2411.26 | 2357 | 2003 |
| hhhhoh | certified | 06:12:02 | 370.1 | 363 | 335,006 | 2416.76 | 2316 | 2003 |
| hhhhho | certified | 06:16:58 | 573.2 | 561 | 632,967 | 2500.5 | 2309 | 2003 |
| oohhhh | certified | 06:18:23 | 896.4 | 878 | 1,659,315 | 2478.31 | 2479 | 2005 |
| ohohhh | certified | 06:26:57 | 846.4 | 829 | 1,554,898 | 2452.69 | 2206 | 2005 |
| ohhohh | certified | 06:34:06 | 614.8 | 602 | 745,994 | 2491.49 | 2236 | 2003 |
| ohhhoh | certified | 06:41:47 | 842.2 | 824 | 1,369,240 | 2449.32 | 2495 | 2006 |
| ohhhho | certified | 06:44:56 | 1221.2 | 1195 | 2,145,649 | 2551.16 | 2259 | 2005 |
| hoohhh | certified | 06:45:15 | 570.7 | 559 | 469,287 | 2478.88 | 2392 | 2003 |
| hohhoh | certified | 06:57:17 | 812.2 | 795 | 1,049,444 | 2473.6 | 3156 | 2005 |
| hohhho | certified | 07:11:21 | 997.6 | 977 | 1,613,478 | 2553.27 | 2582 | 2005 |
| hhohoh | certified | 07:28:56 | 754.5 | 738 | 931,398 | 2469.7 | 3139 | 2003 |
| hhohho | certified | 07:36:20 | 1029.1 | 1006 | 1,516,821 | 2537.47 | 2571 | 2005 |
| hhhoho | certified | 07:49:05 | 672.6 | 656 | 886,021 | 2510.05 | 2319 | 2003 |
| hhhhoo | certified | 08:00:46 | 1072.9 | 1048 | 1,850,877 | 2563.5 | 2497 | 2006 |
| ooohhh | certified | 08:05:49 | 1485.4 | 1450 | 2,711,143 | 2553.1 | 2328 | 2005 |
| oohohh | certified | 08:21:58 | 1264.2 | 1235 | 2,014,146 | 2509.32 | 2569 | 2005 |
| oohhoh | split | 08:22:01 | 1213.1 | 1188 | 3,497,409 | 2487.91 | 2548 |  |
| oohhho | split | 08:31:34 | 1216.8 | 1186 | 3,244,346 | 2609.32 | 2453 |  |
| oohhoh_23h | certified | 08:42:31 | 798.3 | 778 | 1,258,411 | 2473.71 | 2399 | 2005 |
| ohoohh | certified | 08:43:43 | 1096.2 | 1067 | 1,849,598 | 2536.13 | 2208 | 2005 |
| oohhho_23h | certified | 08:52:08 | 1034.7 | 1012 | 1,972,451 | 2543.05 | 2629 | 2005 |
| ohohoh | certified | 08:56:25 | 1422.2 | 1388 | 3,604,561 | 2537.53 | 3251 | 2005 |
| ohohho | split | 09:02:43 | 1213.0 | 1187 | 3,804,976 | 2605.1 | 2528 |  |
| ohhooh | certified | 09:10:08 | 787.5 | 770 | 1,196,101 | 2545.68 | 2249 | 2005 |
| ohhoho | split | 09:21:30 | 462.4 | 453 | 708,164 | 2616.21 | 2647 |  |
| ohohho_23h | split | 09:23:07 | 368.7 | 362 | 483,833 | 2558.6 | 2594 |  |
| ohhhoo | split | 09:23:52 | 321.5 | 315 | 347,745 | 2621.64 | 2478 |  |

## 8. What remains

- **37 open leaves (measure 32 of 64).** Observed so far (HEURISTIC): certified real cubes took 6 holes 234 s wall (1 cube), 5 holes 370–573 s wall (5 cubes), 4 holes 571–1221 s wall (14 cubes), 3 holes 788–1485 s wall (5 cubes). 6 cubes reached their CaDiCaL limit without a verdict: ohohho_23h (4 holes, 352 s, shortened by the deadline); oohhoh (3 holes, 1200 s = full limit); oohhho (3 holes, 1200 s = full limit); ohohho (3 holes, 1200 s = full limit); ohhoho (3 holes, 449 s, shortened by the deadline); ohhhoo (3 holes, 307 s, shortened by the deadline). 33 of the 37 open leaves have 3 or fewer holes; cubes with 3 holes were the slowest so far. At 3 slots the open part needs many more slot-hours; no completion time is claimed.
- **Independent VERIFY** of the accepted certificates, with own code, is still owed. It should re-run cake_lpr on every trim.cnf/trim.lrat, check that every trim.cnf clause is in that cube's cert.cnf, check that cert.cnf is F_c plus the cube units, and check rows and geometric clauses with its own encoder. The critic's unit esr-vfy-n66chk (06:13) did this for 4 cubes (hhhhhh, hohhhh, ohhhhh, hhhohh): cake_lpr re-run, zstd, subset and units. Their rows and geometric clauses were not checked with own code.
- **Driver issues** still in the code (critic, 06:46), for a new copy before a long resume:
  1. A split deletes the partial LRAT and CNF; this has happened now (§5).
  2. Memory for the cake_lpr heap tiers above 2000 MB is not budgeted inside the 3.6G unit.
  3. The 80 % check uses 15 s samples.
  4. The split test also fires on ends that are not time limits.
  5. cad_stats() parsing is not guarded.
  Also: near the deadline the CaDiCaL limit is shortened, and a cube that hits a shortened limit is split rather than retried. This happened 3 times (§5).
- **Owner decisions:** whether partial proofs of timed-out runs may be deleted (§5), and the allocation for a resume.

## 9. Files and hashes

- `W/p2/c14/campaign_status.json`: machine status (final). `W/p2/c14/<id>.out`: event stream of each cube. `W/p2/c14/<id>/it<k>/`: certificate directory (cadical.log, cert.cnf, trim.cnf, trim.lrat, trim.lrat.zst, cake.out, cake.err, cake_attempts.json, used_rows.json, tcert/, fv66.out, verify.json, cert.json, pipeline.log).
- Driver `W/p2c14_driver.py`, SHA-256 `1f08d746a0a1ae8507d38437a914865c39063c55686f3d8c9c93181c9a23f495`, equal to tools/p2c14_driver.py. Cube runner `W/p2_batch_cube.py`, SHA-256 `999451d9622a9ef93b359c102f6dd011df1e0f1508dffa7452f2b7bca7463515`, equal to tools/p2_batch_cube.py. `sha256sum -c tools/sha256.txt` in W at writing time: 14 OK.
- New in this step: `tools/progress_chk.py` (the re-check of §2 and §6; SHA-256 `a8c9f624ce692619a90a042db296fb77f45ad56e996b6ea65973459b36b9c7c2`) and `tools/progress_write.py` (writes this file from the status, the re-check output, the journal and the memguard log; SHA-256 `9d687eac6ff20e34bfd35ed61c6bd794a1288927c8c2fcc6bece3954cd0b1d86`). The re-check output stayed in the session scratchpad, which is not durable. Re-running `progress_chk.py OUT.json` recomputes it from the files in W.

## 10. Resume (exact commands)

The driver resumes from `W/p2/c14/campaign_status.json`. Certified and split cubes stay as they are, and queued cubes start in
priority order (most holes first). Its deadline is fixed in the code (line 22: 15 November 2026, 09:40 KST). Restarted unchanged,
it would start nothing: it would load the state and write the final status again. A resume therefore runs a copy with a new deadline.
The copy is a new file and differs from p2c14_driver.py in exactly one line: line 22 becomes
`DEADLINE, SLOT3 = <epoch of END>, 0`. Setting SLOT3 = 0 gives 3 slots from the start. The command was tested on a scratch copy at
08:58 KST: the diff was that one line, and `--selftest` printed SELFTEST_OK.

At the stop no cube is in state unsat_not_accepted or failed, and no esr-n66-cube-* unit is left loaded in a failed state. So no
p2_cert.sh re-run and no `systemctl --user reset-failed` is needed. The 37 open leaves are all queued.

**Precondition: a memory guard.** The driver starts nothing unless a memguard process is running, and it reads the n66 track budget
from that process's command line (`n66=`; the default is 3000, too small for even one cube). Today's guard was esr-memguard6,
`memguard.sh esr 24000 lo=4000 vfy=8000 n66=9500 k9=12000 agx=7500`. This campaign did not start it. Check with
`pgrep -af memguard.sh`. If no guard is running, start one with the same arguments:

```bash
systemd-run --user --unit=esr-memguard-c14 -p CPUQuota=30% -p MemoryMax=200M -p MemorySwapMax=0 --nice=10 \
  /usr/bin/env LOG=/home/jay/research/data/n66-20261113/memguard-c14.log \
  /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/memguard.sh esr 24000 lo=4000 vfy=8000 n66=9500 k9=12000 agx=7500
```

**Resume:**

```bash
cd /home/jay/research/data/n66-20261113
END='2026-11-16 09:40'   # new deadline (KST); cube units end 60 s before it, and no cube starts in its last 960 s
sed "s/^DEADLINE, SLOT3 = at('09:40'), at('06:45')\$/DEADLINE, SLOT3 = $(date -d "$END" +%s), 0/" p2c14_driver.py > p2c14_driver_r1.py
test "$(diff p2c14_driver.py p2c14_driver_r1.py | grep -c '^[<>]')" = 2 && echo DIFF_OK
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python p2c14_driver_r1.py --selftest
systemd-run --user --unit=esr-n66-driver -p CPUQuota=6% -p MemoryMax=300M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=$(( $(date -d "$END" +%s) - $(date +%s) - 10 )) --nice=10 \
  --working-directory=/home/jay/research/data/n66-20261113 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u p2c14_driver_r1.py
```

The copy keeps every other behaviour of the 15 November driver. That includes the 1,200 s CaDiCaL limit, the 3.6G cube units and
the deletion of partial files when a cube is split (§5, an owner question). Apply the critic's fixes (§8) in a further new copy if
they are wanted. On a resume the driver rewrites STATUS_campaign.md. This PROGRESS.md is the frozen record of this stop (driver ended 09:29:33 KST).
