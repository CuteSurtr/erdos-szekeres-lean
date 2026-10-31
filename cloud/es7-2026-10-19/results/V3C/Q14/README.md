# V3C Q14 (shard 14 of 16)

Tools and inputs:
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (its bundled example prints `s VERIFIED UNSAT`).
- F regenerated from source: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit 71bcca7; verify/v3 from commit bdf319c.
- Work list results/V3C/worklist.jsonl: sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines (matches).
- Cross-check at fdd0393: v3_manifest gives 47533 leaves, sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb (matches), problems 0. All 12380 work-list (case, lits) pairs occur in it. Details are in inputs.txt.

Run: v3_check.py --shard 14 --nshards 16 --skip-covers --jobs 4 --cap 1800, with OUT=/opt/work/out/out.jsonl (outside the checkout). It ran from 14:22 to 16:03 UTC, then I stopped it at the end of the time budget.

Operational note: by mistake two v3_check.py instances with identical arguments and the same OUT ran together from 14:22 to 15:44 UTC. Each solve/check uses its own mkdtemp directory, so the instances could not overwrite each other's CNF or proof files. They did duplicate the work, so 392 leaves have two records each. In every duplicated pair both records are VERIFIED, with the same cnf_sha256. I stopped the second instance at 15:44, and from then on only one ran.

Results (shard has 773 leaves):
- out.jsonl: 1029 records covering 637 distinct leaves (392 of them duplicated, as noted above).
- Verdicts per distinct leaf: VERIFIED 637, REJECTED 0, SAT 0, TIMEOUT 0.
- Still unchecked: 136 leaves. The run is resumable with the same arguments.
- No REJECTED leaf with an empty cake_lpr field, so no step-4 rechecks were needed.
- Solve time, first record per leaf (637): sum 20523.7 s, median 15.12 s, max 729.96 s. Over all 1029 records: sum 37202.7 s, median 18.54 s, max 744.22 s.
- Check time (cake_lpr), first record per leaf: sum 3145.4 s, median 4.24 s, max 44.4 s. Over all records: sum 5603.9 s, median 4.9 s, max 53.11 s.
- No SAT, REJECTED or TIMEOUT leaves.
