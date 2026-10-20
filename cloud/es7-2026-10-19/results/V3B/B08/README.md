# V3B B08: shard 8 of 16

Tools (see tools.txt):
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`)
- verify/v3 at commit bdf319c; input commit Z = 066eaa9

F.cnf sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).

Manifest (see inputs.txt):
- v3_jsonl_leaves: WAVE1 119 dirs / 30151 leaf lines / 71 skipped; WAVE2 86 / 5156 / 0; WAVE3 5 / 232 / 0
- v3_manifest: 35153 leaves, 253 cases with leaves, 0 problems
- M.jsonl sha256 22b6f6a782cd2b2e6319c61c7bc7029032d10aa5fd583dcfbba47ec627e1c549
- C.jsonl sha256 cd03dd0a81aec5d738a2ef5e6f817a1c151f4b9141b0ca5a3f0546978a7e1fbe
- Step 3: 21 JSONL files, 11308 VERIFIED leaf records, 10121 distinct VERIFIED keys; n = 25032
- Mt.jsonl sha256 605e39d27b8a11c8b8de36b167d1760f91dc3e6c4e49a2e570bf607689e7cfe7
- shard 8 of 16: 1564 leaves

Command: `v3_check.py --root $ROOT --base /opt/work/F.cnf --manifest /opt/work/Mt.jsonl --shard 8 --nshards 16 --skip-covers --out /opt/work/out/out.jsonl --work /opt/work/v3w --jobs 4 --cap 1800` (12:39 to 14:53 UTC, finished).

Results (out.jsonl, sha256 3ae1b6c66e5933342591d58803316a8ba9ba59d660b8eb453a911113a88d3e70):
- VERIFIED 1564, REJECTED 0, SAT 0, TIMEOUT 0; unchecked 0.
- Every record has rc 20 and cake_lpr `s VERIFIED UNSAT`; the 1564 (case, lits) keys are exactly the shard's 1564 manifest keys.
- solve time: sum 26297.4 s, median 9.62 s, max 273.3 s
- check time: sum 5767.2 s, median 2.80 s, max 22.0 s
- No REJECTED leaves with an empty cake_lpr field, so no rechecks were needed.
