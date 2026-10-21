# AUDIT2 A6: tree certificates and data

Audit A6 of `AUDIT2/TASK.md` (852bee7). Budget 1.75 h, from 00:33 UTC on 21 Oct 2026. One cloud VM (`env.txt`).
Zf = `06c1f798c` (old `14447d0d5`, `FINAL/COMMIT_MAP.tsv`). `git diff 06c1f798c HEAD` is empty for WAVE1–4 and
Mii-S. All inputs were read from a `git archive` of Zf. V2-L's Lean data and scripts were read at the branch head.
My scripts are in `scripts/` and my running log is in `NOTES.md`.

## Verdict

**I found nothing that breaks the claim.** For sub-case (ii), every tree leaf behind `hleaves` of
`V2L.mirrorExclusionLine_final` has a recorded cake_lpr `s VERIFIED UNSAT` on the right CNF. I checked this in three
ways:

- my own tree builder (different dir-to-case rule, own cover check) gives the same trees;
- every leaf has a wave record with that verdict;
- every leaf has a V3 re-check record with that verdict, and its `cnf_sha256` matches a leaf CNF I rebuilt myself
  from F.

The findings below are about how the evidence is documented or labelled. None of them is a gap in the claim.

## Findings, most serious first

1. **No per-leaf CNF hash in the wave records** (weakens the trust base, mildly; fully covered by V3).
   - `V2-L/scripts/gen_trees.py:101-113` accepts a closure from any wave record with `status` UNSAT and `cake_lpr`
     `s VERIFIED UNSAT`, keyed by the cube's literal sequence. The wave leaf records carry no `cnf_sha256`
     (record key survey in `NOTES.md`).
   - So, on the wave side, "the file solved was case file + leaf units" rests on reading the driver code.
     `V2-L/README.md` §3 (lines 161-170) reviewed the 56 WAVE1 drivers only.
   - I checked the WAVE2–4 drivers myself:
     - 113 `close_march.py` files: 109 identical copies and 4 variants (F4, F5, F6, S5);
     - all 113 have the same leaf-file write line, `p cnf nv nc+|cube|`, the case body, then the cube units;
     - `SKIP` ("closed elsewhere") records are never counted as closed, by `gen_trees.py` or by my builder.
   - The V3 re-check makes this point moot (item S5 below): every tree leaf has a V3 VERIFIED record, and its hash
     equals my own rebuild of the leaf file.
2. **61 of the 138 empty-cube closures carry no hash, and 44 are `cube: []` records without a `whole`/`direct`
   flag** (cosmetic).
   - `gen_trees.py:104-113` accepts both kinds through the directory's case assignment.
   - The breakdown: 45 whole+hash, 28 direct+hash, 4 cube[]+hash, 21 whole without hash, 40 cube[] without hash.
   - No such record names another case.
   - Mitigation: all 142 V3 records for an empty leaf carry exactly the Mii-S `cnf_sha256` of their case.
3. **The V3 file is not byte-identical to Lean's per-leaf CNF** (cosmetic).
   - Lean's hypothesis is about `cubeCnf (cubeCnf F c) l`, with the leaf units in tree order.
   - `verify/v3/v3_check.py:133-135` (at 92746ac) writes the case units, then the leaf literals that are not in the
     case cube, sorted by |x|.
   - No tree leaf shares a literal with its case cube (0 of 73,690). So the two files differ only by a permutation
     of the leaf unit clauses, and they are equisatisfiable.
   - The wave runs wrote the leaves in recorded order, the same as Lean.
   - `V2-L/README.md` §9.6 is accurate as written, because it cites the wave records. "Re-checked from scratch"
     means this permuted file.
4. **One V3 leaf record is REJECTED** (cosmetic).
   - `V3A/V07/out.jsonl`, case U4_L, key 2119, lits `[-1014, -1040, 1065, -1112, 1134, 1155, -1245]`: rc 20 and
     `cake_lpr` "" (cake_lpr printed no verdict).
   - This cube is a leaf of the U4_L tree. Another V3 record of the same leaf is VERIFIED, with the same
     `cnf_sha256`.
   - Acceptance depends on the aggregator preferring that record (A4's area).
5. **`V3Z/cases_final.jsonl` labels the 278 accepted wave cases `"status": "OPEN"`** (cosmetic).
   - The label is the Mii-S status, carried over. Acceptance is recorded in `accepted_final.tsv` (278 ACCEPTED,
     cover VERIFIED).
   - The file is the manifest's `C.jsonl`. I reproduced its sha256 `3fff4486…f44411`.
6. **Wording: "40 directories with only a `leaves.icnf`"** in `V2-L/README.md` §9.3 (cosmetic).
   - All 40 are W34 cases that were never started, and each has a 0-byte `leaves.icnf`. No data is skipped.
7. **Two silent paths in `gen_trees.py`** (cosmetic; neither occurs in the data).
   - Line 88 ignores hashes that are not a case's `cnf_sha256`. My scan found 0 unknown `case_sha256` or
     `cnf_sha256` values.
   - Line 111 drops an UNSAT record whose cube is not a list.

## What I checked and found sound

- **S1. An independent recomputation of the trees** (`scripts/mytrees.py`).
  - Directories are assigned to cases by their names (my own regex). Every `case_sha256` and `cnf_sha256` in every
    record is then checked against that name: 0 mismatches, 0 unknown hashes. 54 directories carry no hash; they
    are the same 54 as in status.json.
    - W06 and W07 record the U_L2 case hash `1d26b947…` in their READMEs.
    - The other 52 are W35 directories with an empty `leaves.jsonl`.
  - The cover check is semantic (branching on literals), not a transcription of `coverCheck`.
  - Result:
    - cases: 172 direct, 138 empty-cube, 140 trees;
    - 73,690 tree leaves, 910 splits;
    - 0 open nodes, 0 conflicting SPLIT records, every sibling list and root list a cover.
  - The directory list of each tree case equals status.json.
- **S2. The Lean data says the same.**
  - `scripts/lean_leaves.py` is my own decoder of `unpackT`/`decLit`. It reads `V2L/Trees/Table.lean` and
    `T*.lean`, and checks each Table entry's (U, L) against the T file's header and `Mii-S/cases.jsonl`.
  - The leaf lists of all 450 cases equal mine, element by element and in the same order.
  - Lean's `caseCubes` (decoded from `casePacked`) equals `Mii-S/cases.icnf`, case by case: 450/450.
- **S3. Regeneration.** `gen_trees.py` rerun at Zf into a scratch directory reproduces all 503 files of
  `V2L/Trees/` byte for byte. The status.json rows and summary are equal too.
- **S4. Every leaf is closed by a verified record.**
  - Both builders count a cube as closed only on `status` UNSAT with `cake_lpr` exactly `s VERIFIED UNSAT`.
  - No leaf has duplicate or complementary literals, or a literal outside 1..47002.
  - The 172 direct cases:
    - `Mii-S/pass2_lrat.jsonl` has the exact verdict and the case's `cnf_sha256` for all 172;
    - `Haudit/t5_all172.jsonl` confirms all 172;
    - the set equals the UNSAT_VERIFIED cases of `cases.jsonl`.
- **S5. V3 backing with my own hashes** (`scripts/leafsha.py`).
  - F rebuilt as `V3Z/tools.txt` says: sha256 `69c1dc8f…932d`, `p cnf 47002 515121`.
  - All 450 case CNFs (F + cube units) hash to `cases.jsonl`.
  - The 73,828 non-direct leaves are the 73,690 tree leaves plus the 138 empty cubes. For each, I rebuilt the V3
    leaf file and its hash equals the `cnf_sha256` of its V3 records, which are VERIFIED with `cake_lpr` exactly
    `s VERIFIED UNSAT`: 73,828 match, 0 mismatch, 0 missing.
- **S6. Manifest.**
  - Rebuilt at Zf with `verify/v3` at 92746ac, as `V3B/TASK.md` step 2 says. M.jsonl has sha256 `e01af167…3b5`
    and 73,880 lines; C.jsonl has `3fff4486…`. All equal READY.json and V3Z.
  - Tree leaves not in the manifest: 0. Manifest leaves not in a tree: 52, all U_L7, each strictly extending a
    tree leaf.
  - Those 52 lie under one 31-literal cube. It was split in `WAVE4/H69/U_L7` and closed (verified) in `H26` and
    `H59`; the tree stops at the closed node.
- **S7. The W34 `children` key.**
  - `WAVE1/W34/run_w34.py` lines 9, 44, 57, 130 and 135: `children` is the march_cu sub-cube list of a timed-out
    cube, and the driver queues `cube + child`.
  - That is exactly `subs` of close_march.py. Its 10 SPLIT records (U3-5_L, U_L2-4, U_L2-7) are relative, as
    `gen_trees.py` assumes.
- **S8. Structural soundness.** A wrong tree shape cannot break the claim:
  - the kernel checks every sibling list with `coverCheck`;
  - `hleaves` is stated over exactly the leaves of the checked tree.
  
  So what matters is that each leaf's hypothesis is a true verified fact (S4, S5), not that the tree matches the
  runs.

## Lean build

LEAN_BUILD_PLACEHOLDER

## What I could not check

- I did not re-solve any leaf (that is A5). The proofs were deleted after checking, so the verdicts are trusted
  as recorded, in two independent sets: the wave records and V3.
- For the wave leaf records, I could not confirm by hash which CNF each driver solved (finding 1). I rely on the
  driver code and on V3.
- I did not review A1–A5's topics: the encoding, the 450-case split, the Lean statements beyond the tree layer,
  and V3's aggregation logic.
