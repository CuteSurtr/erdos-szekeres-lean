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
