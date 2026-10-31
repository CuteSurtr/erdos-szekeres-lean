# C3W6: how the unit list was made

`tools/gen_w6.py` (planning only, no solving) read the 193 record files in `lists/files.txt` at commit e71a4911: the 187 files
that `results/C3COMP1` composed, the final C3W4 and C3W5 out files, the C3COMP1 cap experiment and its nine-bit pilot. It
follows the split records and the `certified` flags the way `close_tree.py` and `compose.py` read them, but it does not
re-derive CNF hashes (the final composition does that), so its counts are a plan, not a claim.

    python3 tools/gen_w6.py RESULTS results/C3COMP1/open_roots.tsv lists/files.txt OUTDIR

For each of the 910 needed roots (`results/C3COMP1/open_roots.tsv`), a root that is not covered contributes its open
σ-cubes, following a root's σ split in preference to an older layer split:

- an uncovered six-bit cube, if it has no layer split or its layer subtree has more than 4 open leaves (the cube is
  re-solved, as `results/C3COMP1/README.md` recommends); otherwise its open layer leaves (1 unit);
- a root or 3-bit cube without any split record is σ-split in `presplit.jsonl` (bits = the 3 smallest free residues, as
  `close_tree.py` would write it, with no solve): H3 and one-orbit roots down to their 64 six-bit cubes (as C3W4's caps
  1,1 did), the one unreached two-orbit root one level only (its 3-bit cubes often close directly, `results/C3W5`).

Result at e71a4911: 88 roots open (5 H3/one, 65 H3/two, 15 one-orbit H6, 3 two-orbit H6). The 5 H3/one roots are left to
`results/C3H1`. The other 83 give 4,109 units in `lists/W6.tsv`, sorted by stratum, root and node:

| stratum | units | of which: earlier timeout at 300 s | never ran | σ-split by presplit.jsonl | layer leaf |
|---|---|---|---|---|---|
| H3/two | 3,342 | 939 | 284 | 2,118 | 1 |
| one-orbit H6 | 677 | 251 | 56 | 370 | 0 |
| two-orbit H6 | 90 | 0 | 82 | 8 (3-bit cubes) | 0 |
| total | 4,109 | 1,190 | 422 | 2,496 | 1 |

`presplit.jsonl` holds 361 σ-split records for the 41 roots that had no split record: 40 H3/two or one-orbit roots
with their 8 three-bit cubes (9 records each), and the unreached two-orbit root (1 record). Every record names a node with 2 layers and the 3 smallest free
residues, which is what `compose.py` requires of a σ split. The final composition must read `presplit.jsonl` together with
the C3W6 out files.
