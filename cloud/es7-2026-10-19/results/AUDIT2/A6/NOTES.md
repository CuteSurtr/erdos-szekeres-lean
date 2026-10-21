# A6 notes (in progress)

Zf = 06c1f798c (old 14447d0d5); WAVE1-4 and Mii-S identical between Zf and the branch head (git diff empty).

00:50 UTC
- `scripts/lean_leaves.py`: decodes the committed Lean data `V2-L/V2L/Trees/{Table,T*}.lean` (own decoder of
  `unpackT`/`decLit`), checks each Table entry's (U, L) against the T-file header and `Mii-S/cases.jsonl`.
  450 cases, 140 trees, 74,000 leaves.
- `scripts/mytrees.py`: own tree builder from WAVE1-4 at Zf. Dir-to-case by directory name (own regex), then
  every case_sha256 / cnf_sha256 in the records is compared with the name: 0 mismatches, 0 unknown hashes,
  54 dirs with no hash (= the 54 of status.json). Own semantic cover check (not a transcription of coverCheck).
  Result: 172 direct, 138 empty-cube, 140 trees, 73,690 tree leaves, 0 open, 0 conflicting SPLITs, every
  sibling list a cover.
- Leaf lists of all 450 cases equal the Lean data, element for element and in order.

00:50 UTC (cont.)
- V3 coverage: every one of the 73,828 non-direct tree leaves (73,690 + 138 empty cubes) has a V3 leaf record
  (inputs of `V3Z/aggregate_inputs.txt`) with verdict VERIFIED and cake_lpr exactly `s VERIFIED UNSAT`.
  The only V3 REJECTED leaf record (V3A/V07, U4_L key 2119, rc 20, cake_lpr "") is a tree leaf of U4_L that
  has another VERIFIED record with the same cnf_sha256.
- V3 leaves not in a tree: 52, all U_L7, all strictly extending a tree leaf. They lie under the 31-literal
  cube split in WAVE4/H69 and closed in WAVE4/H26 and H59 (closed wins).
- The 138 empty-cube cases: closing records are 45 whole+hash, 28 direct+hash, 4 cube[]+hash, 21 whole
  without hash, 40 cube[] without hash; no record names another case. All 142 V3 empty-leaf records carry
  exactly the Mii-S cnf_sha256 of their case.
- `scripts/leafsha.py`: rebuilt F (gen_etv + mirgen as V3Z/tools.txt): sha256 69c1dc8f…932d. All 450 case
  CNFs (F + cases.icnf cube) hash to cases.jsonl. For all 73,828 leaves, my own rebuild of the V3 leaf
  file (F + case cube + leaf literals not in the cube, sorted by |x|) hashes to the cnf_sha256 of its
  V3 records: 73,828 match, 0 mismatch, 0 leaves contradicting their case cube.
- W34 `children`: `run_w34.py` lines 9, 57, 130, 135: `children` is the march_cu sub-cube list of a
  timed-out cube and the children queued are `cube + x`; same meaning as `subs` of close_march.py.

00:50 UTC (cont.)
- 172 direct cases: Mii-S/pass2_lrat.jsonl has cake_lpr exactly `s VERIFIED UNSAT` for all 172 (2 more
  records for non-direct cases have no cake_lpr), cnf_sha256 = cases.jsonl; Haudit/t5_all172.jsonl: 172/172
  verified with matching hash; the set equals the UNSAT_VERIFIED cases.
- Lean caseCubes (decoded from Data.lean casePacked) = Mii-S/cases.icnf, per (U, L), in order: 450/450.
- `gen_trees.py` rerun at Zf into a scratch dir: `V2L/Trees/` (503 files) byte-identical to the committed
  ones, status.json rows and summary equal.
- Dir lists per tree case equal status.json. All 468 leaves.jsonl sit at WAVEx/VM/dir (none deeper).
  The 40 "leaves.icnf only" dirs are all W34 not-started cases with a 0-byte leaves.icnf.
- WAVE2-4 drivers: 109 close_march.py copies identical, 4 variants (F4, F5, F6, S5); all 113 contain the
  same leaf-file write line as WAVE1. SKIP records ("closed elsewhere") are never counted closed.
- Tree leaves sharing a literal with their case cube: 0. So V3's file for a leaf is Lean's
  `cubeCnf (cubeCnf F c) l` with the leaf units permuted (sorted by |x|), nothing else.
- V3Z cases_final.jsonl: 278 accepted wave cases carry status "OPEN" (inherited from Mii-S); acceptance
  is in accepted_final.tsv (278 ACCEPTED, cover VERIFIED).
