# V3C Q09: shard 9 of 16, third acceptance pass of mirror sub-case (ii)

- Tools, built from source: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04, cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa. The bundled cake_lpr example prints `s VERIFIED UNSAT`. See tools.txt.
- F.cnf was regenerated with gen_etv.py and mirgen.py. Its sha256 is 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, which matches.
- Input commit: 71bcca7456f44fb27385fa0e0f8b2ac1c4c2a42c. verify/v3 commit: bdf319c.
- Work list: sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc, 12380 lines. Both match.
- Cross-check at fdd0393: the manifest is 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb with 47533 lines, which matches. All 12380 work-list (case, lits) records occur in it. Details are in inputs.txt.
- Run: `v3_check.py --shard 9 --nshards 16 --skip-covers --jobs 4 --cap 1800`, from 14:02 to about 15:20 UTC.
- Leaf verdicts for 774 of 774 shard leaves: VERIFIED 774, REJECTED 0, SAT 0, TIMEOUT 0. No leaves are unchecked.
  Every record has rc 20 and cake_lpr `s VERIFIED UNSAT`.
- Solve time: sum 15659.7 s, median 10.46 s, max 322.21 s.
- Check time: sum 2895.6 s, median 2.71 s, max 26.77 s.
- There were no SAT, REJECTED or TIMEOUT leaves. No leaf had an empty cake_lpr field, so step 4 had nothing to recheck.
