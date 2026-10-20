# FINAL: the commit at which every wave case of mirror sub-case (ii) is closed

`READY.json` names Zf = 14447d0d56c891a89a07a8141b50eae0ebfd44a7 (2026-10-20T16:20:17Z). At Zf, `results/WAVE4/scripts/gfrontier3.py` finds no open cube in any of the 278 wave cases: every top cube of every case is closed by a leaf with a cake_lpr `s VERIFIED UNSAT` record, or split (SPLIT record) into cubes that are, recursively. With the 172 cases closed directly by `results/Mii-S`, all 450 hull cases are closed by the solver runs.

The acceptance manifest at Zf, built exactly as `results/V3B/TASK.md` step 2 does it (verify/v3 at bdf319c: v3_jsonl_leaves.py ROOT results/WAVEk jtreek for k = 1..4, then v3_manifest.py ROOT M.jsonl C.jsonl results/WAVE1 jtree1 results/WAVE2 jtree2 results/WAVE3 jtree3 results/WAVE4 jtree4 (as results/V3B/TASK.md step 2)), has 73880 lines (leaves of all 278 wave cases; its case file lists all 450 cases), sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5.

This is what the waves claim; the acceptance passes check it from scratch: every leaf re-solved and proof-checked (`results/V3T`, `results/V3A` to `results/V3E`), every case cover checked and the final table built (`results/V3Z`), and the Lean instantiation (`results/V2-L`, `TREE_TASK.md`).
