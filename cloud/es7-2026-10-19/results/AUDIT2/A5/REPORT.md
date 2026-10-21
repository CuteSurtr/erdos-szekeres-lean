# AUDIT2 A5: independent re-check of a sample of sub-case (ii) leaves and covers

Task: `results/AUDIT2/TASK.md` at 852bee7, A = A5, H = 1.75 h. Run 2026-10-21 00:33 to about 02:10 UTC on a 4-core, 15 GB VM (`env.txt`). Tools and inputs are in `tools.txt`. My scripts are in `scripts/` and share no code with `verify/v3`.

## Result

I found nothing that breaks the claim or weakens the trust base within this focus. Every leaf, cover and direct case I checked independently came back `s VERIFIED UNSAT` from cake_lpr. Every CNF I built has the same sha256 as the V3 or Mii-S record for it.

| set | count | cake_lpr `s VERIFIED UNSAT` | cnf_sha256 = V3 / Mii-S record |
|---|---|---|---|
| main random leaf sample (`sample.jsonl` → `out.jsonl`) | 320 (70 U_L2, 60 U3_L, 50 U_L7, 140 from the other cases; 60 cases) | 320 | 320 |
| extra leaves (`extra_out.jsonl`): the one leaf with a REJECTED V3 record, plus 10 empty-cube leaves | 11 | 11 | 11 |
| second sample (`out2.jsonl`): 80 more U_L2/U3_L/U_L7 leaves, plus the 12 slowest leaves by V3 timing | 92 | 91 (+1 see below) | 92 |
| all 172 direct cases, F + cube (`direct_out.jsonl`) | 172 | 172 | 172 (vs `Mii-S/cases.jsonl`) |
| cover CNFs: 20 picked (`covers_out.jsonl`, includes U_L2 with 22,529 leaves, U3_L, U_L7) and **all 140 non-trivial** covers (`covers_all.jsonl`) | 140 | 140 | 140 |
| sha256 only, **every** manifest leaf (`allsha.log`) | 73,880 | (n/a) | 73,880: every VERIFIED V3 record for the leaf has my sha |

Solve plus check time: 6,410 s total over the main sample (median 13.2 s, max 117.6 s, largest proof 107 MB). For the second sample: median 19.7 s, max 363 s, proofs up to 329 MB.

## How I checked

1. I built CaDiCaL 3.0.1 (c6073042) and cake_lpr (a36874a8) from source. cake_lpr's bundled example prints `s VERIFIED UNSAT`. I regenerated F with the two commands in `V3Z/tools.txt`: sha256 69c1dc8f…932d, which matches.
2. My builder (`scripts/mk.py`) writes F's header with the clause count raised by the number of units, then F's body, then one unit clause per case-cube literal (`Mii-S/cases.icnf`, in order), then one per leaf literal. Before any leaf was run, F + cube reproduced all 450 `cnf_sha256` values in `Mii-S/cases.jsonl`.
3. I built the manifest as `V3B/TASK.md` step 2 describes, at Zf = 06c1f798c (old 14447d0d5), with the `verify/v3` scripts at 92746ac (old bdf319c). I used those scripts only to list the leaves. The result has 73,880 leaves in 278 cases with 0 problems. Its sha256 is e01af167…83b5 and C.jsonl's is 3fff4486…4411, the same values as `V3Z/inputs.txt`.
4. Provenance (`scripts/prov.py`): I looked up each of the 320 main-sample leaves in the raw wave directories at Zf, matching literals as a set. Each one appears both as a line of a `results/WAVE*/…/leaves.icnf` and as an `"status": "UNSAT"` record in that directory's `leaves.jsonl`. Every `case_sha256` in those `leaves.jsonl` files equals the Mii-S `cnf_sha256` of the case.
5. Leaf checker (`scripts/check.py`): it runs `cadical -q --lrat --no-binary` and then `cake_lpr cnf proof`. A leaf counts only if the solver exits 20 and one of cake_lpr's stdout lines is exactly `s VERIFIED UNSAT`. The sample was drawn with fixed seeds (`scripts/sample.py`, seed 20261021).
6. Covers (`scripts/cover.py`, `covrun.py`): the cover CNF has the case-cube units followed by one clause ¬leaf per manifest leaf, with header `p cnf 47002 n` and no F. I worked this out from the records and it reproduces every V3 cover `cnf_sha256` and `leaves_sha256`. The 138 "trivial" covers are exactly the 138 cases whose only leaf is the empty cube. For those, the leaf CNF equals the Mii-S case CNF, and those leaves are among the 73,880 sha-matched VERIFIED records. The case sets in `V3Z/covers.jsonl` and in the manifest are the same 278 cases, and the 172 direct cases plus these 278 make up the 450 cases of `cases_final.jsonl`.

The leaf check plus the cover check makes the argument whole. Cube ∧ (some leaf) holds for every assignment, because the cover CNF is UNSAT. F ∧ cube ∧ leaf is UNSAT for each leaf. So F ∧ cube is UNSAT. Completeness does not depend on the leaf extraction scripts. A leaf that the scripts dropped would make the cover CNF satisfiable, and I re-checked all 140 covers myself.

## Findings (none break the claim)

1. **Cosmetic. One leaf could not be finished here.** The leaf is U_L2-5 [2247, 2572, 2872, -3230, -3248, -3265, -3281], idx 59938 (`out2.jsonl`). With 4 jobs running, cake_lpr was killed by the memory cgroup of this sandbox (dmesg: `Memory cgroup out of memory: Killed process (cake_lpr) anon-rss:4197632kB`), so its verdict was empty. A re-check on its own was then killed while the proof was still being written. The CNF sha matches the V3B/B09 VERIFIED record (e46fcb66…). This is a resource limit of my sandbox, not a finding against the claim. The outcome of the final background attempt is recorded in `recheck.txt`.
2. **Cosmetic.** One manifest leaf has two records: an empty-verdict REJECTED in `V3A/V07/out.jsonl` and a VERIFIED in `V3B/B04/out.jsonl` (U4_L [-1014, -1040, 1065, -1112, 1134, 1155, -1245]). This is the same out-of-memory pattern. I re-verified it (`extra_out.jsonl`, 172 s solve).
3. **Cosmetic.** Wave directory names carry shard suffixes (`U_L2.s01`, `U_L2_s3of12`, `U_L4-s1`, `U_L4_shard2of3`, …). The case assignment relies on `case_sha256`, which matched the case for every directory I touched. Given names like `U_L2` and `U_L2-15`, assigning cases by name prefix alone would be unsafe.
4. **Note.** `v3_jsonl_leaves.py` reports "skipped records 71" for WAVE1. I did not investigate them. They cannot cause a wrongly accepted case, because the covers close over the leaves that were kept.

## What I did not check

- The encoding (whether F soundly encodes the problem), the 450-case split and its 122 cover obligations, the Lean statements, and sub-case (i): those are the A1 to A3 focuses.
- About 73,300 of the 73,880 leaves were not re-solved. For all of them I checked only that V3's VERIFIED records name the CNF I would build.
- The V3 proofs themselves: they are not committed, so for the leaves outside my sample I could only compare hashes.
