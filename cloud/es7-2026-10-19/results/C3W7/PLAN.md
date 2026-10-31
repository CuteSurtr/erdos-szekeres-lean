# C3W7: how the unit list was made

`tools/gen_h3one.py` (the H3/one-only variant of `results/C3W6/tools/gen_w6.py`, planning only, no solving) read the
record files in `lists/files.txt` (the C3COMP1 set, the final C3W4/C3W5 files, the C3COMP1 cap experiment and nine-bit
pilot, and the C3H1 pilot records) and listed the open six-bit σ-cubes of the five H3/one roots: 319 cubes in
`lists/H3one.tsv` (0s0_1: 64, 0s0_2: 64, 0s0_3: 64, 0s0_4: 64, 0s0_5: 63; the 64th of 0s0_5 was closed by
`results/C3H1/X1`). Every H3/one root already has its σ-split records down to the six-bit cubes (C3W4), so no root
needed a presplit.

`tools/gen_w7.py lists/H3one.tsv OUTDIR` then took the first 239 of the 319 cubes, wrote their 8 nine-bit cubes each
(the σ children on residues 8, 9, 10, which are the 3 smallest free residues of every one of them) to `lists/W7.tsv`
(1,912 units: 0s0_1 512, 0s0_2 512, 0s0_3 512, 0s0_4 376), and their 239 σ-split records to `presplit.jsonl`. A cube
whose 8 nine-bit cubes are all certified is covered through its σ split, whatever its older layer-split record says.

The last 80 cubes of `lists/H3one.tsv` are done the same way on a local machine (`results/C3H1/LOCAL/`, in reverse
order; that run's list also holds the 40 cubes before them, as an overlap in case this wave falls short). The final
composition must read `presplit.jsonl` together with the C3W7 and C3H1 out files.
