# VERIFY_LP0_7_REAL_2EXT_VB: verdict on claim lp0-7-real-2ext-onn (verifier VB, 15 November 2026, 20:46-20:48 KST)

(The claim names VERIFY_LP0_7_REAL_2EXT.md, which already holds VB's verdict on the parent claim lp0-7-real-2ext; hence
the suffix _VB. Same methods and code as there.)

**Verdict: CONFIRMED.** The pattern `onnoooooooooooooooo` is closed for r7real and r7it3: D2's two final CNFs are UNSAT
by fresh cake_lpr runs (CERTIFIED), every cut clause in them is re-derived by VB from a valid BFP certificate, and VB's
**own** base encoding plus those cuts is UNSAT, **CERTIFIED** for both. With the parent claim, all 765 position patterns
(5 blocks × 153) are closed: 713 base-UNSAT, 52 closed by BFP cuts (final states of `run_k2b/jobs.jsonl`). Labels of the
combined statement at 20:47 (D2's `cert_k2b/certify.jsonl`, all lines exactly `s VERIFIED UNSAT`): **500 of the 765 final
CNFs CERTIFIED** (r7real, r7it3, t1it4 all 153 each; t1it5 31 of 153; t1it6 the 10 cut-closed), the other 265 (t1it5 122
and t1it6 143 base-UNSAT patterns) COMPUTED on D2's side, certification running. Nothing about LP0(7) for point sets
beyond 2-point extensions of these five blocks follows.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vb/claims/lp0-7-real-2ext/`; D2 = `pm1115/d2/`)

1. **Certificates.** VB's exact BFP checker (VERIFY_LP0_7_REAL_2EXT.md, check 2) accepts every entry of
   `cert_k2b/library_snapshot_203949.jsonl` (38/38, used for r7real onn), `library_snapshot_204434.jsonl` (41/41, used for
   r7it3 onn) and `claims/library_k2_final_2044.jsonl` (41/41, SHA-256 `93682c97…` = claim), and of all earlier snapshots.
2. **Cut clauses** (`V/vb_lp0_all3.py`): r7real onn 387 of 387 and r7it3 onn 440 of 440 cuts re-derived from (entry, rev,
   flip, Q) — the block's own brackets agree with B, and D2's clause contains VB's justified clause; each `.cnf`'s cut part
   equals its `.cuts.jsonl`. Over all 52 cut-closed patterns now dumped: 7,141 of 7,141 cuts re-derived.
3. **Own base encoding** (`V/vb_base.py`, VERIFY_LP0_7_REAL_2EXT.md check 4): for both onn patterns own base alone is SAT
   and own base + D2's cuts is UNSAT (pysat, `V/onn_pysat.jsonl`); **VB's own CNFs are CERTIFIED** (house certifier,
   unit `esr-agv-vb-lp0certG`, `s VERIFIED UNSAT`, LRAT kept in `V/owncert/`), together with the other 13 cut-closed
   patterns not certified by VB before: VB's own encoding is now CERTIFIED on **all 52 cut-closed patterns** (with
   re-derived cuts) and on 51 sampled base-UNSAT patterns (103 of 103 own CNFs).
4. **D2's proofs, fresh cake_lpr** (unit `esr-agv-vb-lp0recakeH`, own FIFO wrapper): `r7real_onnoooooooooooooooo` and
   `r7it3_onnoooooooooooooooo`: exactly one line `s VERIFIED UNSAT` each; CNF SHA-256 `17c6a7b7…` / `e337a0ad…` and LRAT
   stream SHA-256 `9256513d…` / `a628bc56…` (and byte counts) equal the claim and `certify.jsonl`.
5. **Counts.** Last state per (block, pattern) in `run_k2b/jobs.jsonl`: 765 patterns, 713 UNSAT, 52 UNSAT_CEGAR, 0 open.

## Files (V as above)

| file | SHA-256 |
|---|---|
| `V/vb_lp0_all3.py` / `V/vb_lp0_ABC_all3.out` | `65ebc79aee300c2f99fa15966f1e4a592719a2e634ac79951974e2ce1e53a0db` / `e417a05c599e297845754a3f6633db4cd4e1a6dc158ff107f70e8c98457a48ab` |
| `V/onn_pysat.jsonl` | `60b02fed4de35e5fce3c4f54d0c30913d7e30e6cf653351c480e103afe4eb52c` |
| `V/owncert/certify.jsonl` (103 lines, all `s VERIFIED UNSAT`) | `9b67aebf1e30b5a16f7792327bcd8cb6c479ab9fa1a5141e895e33a7ebf77a29` |
| `V/d2recake/rerun.jsonl` (8 re-runs) | `814fc0c74b8d5f196da58bf56be9515f66ad7159d66f556770ca744f4615a3f8` |

D2's files were only read.
