# VERIFY_N66_COVER_FINAL_1118: verdict on claim vb-n66-55-cover-final (verifier VS, 18 November 2026, 04:40-04:44 KST)

**Verdict: CONFIRMED at the claimed labels.** VS reproduced both parts with its own code, read-only:
- **(2), cover from the certified formulas themselves.** The selector unit clauses of the 132 trimmed CNFs that cake_lpr
  accepted cover the whole selector space.
- **(1), four-check coverage.** The four-check records cover exactly the 132 certified leaves, with current hashes.

With the four checks (trim ⊆ cert.cnf = F_c + cube units, fresh cake_lpr per leaf), F_c is UNSAT. So N66 ≤ 55 holds,
CERTIFIED leaf by leaf, modulo the parent record's written soundness of the encoding, as for N66 ≤ 56. This agrees with
VS's verdict on `n66-le55-cubes-1118` (VERIFY_N66LE55_FINAL.md), which reached the same cover from the cube ids.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/n66final/`)

1. **Cover from trim.cnf** (`V/vs_cover_trim.py`; output `V/cover_trim.out`).
   - For each of the 132 leaves with status `certified` in `campaign_status.json`:
     - SHA-256(trim.cnf) = cert.json `trim_cnf_sha256`: **132/132**;
     - all unit clauses on 988541..988610 were collected, with +sel_0 and +sel_1 removed;
     - **every remaining unit is a literal of the leaf's cube id** (0 outside);
     - exactly 8 leaves lack some id literal: hhhohh, hhhooh, hhoohh, hhoooh, hohohh, hohooh, hooohh and hooooh, the
       cubes refuted by unit propagation.
   - The units mention 14 states (12, 16, 17, 23, 25, 29, 37, 39, 40, 44, 45, 46, 49, 52). **Their union covers all
     16,384 assignments of those states: measure exactly 1.**
2. **F_c's units.** `awk` over `p2/b14h2/it1/cert.cnf` (SHA-256 14f43bf4…, recomputed by VS) finds **exactly two unit
   clauses, 988541 and 988542** (+sel_0, +sel_1), and no other unit clause of any kind (`V/fc_units.txt`).
3. **Four-check coverage.** This was done for VERIFY_N66LE55_FINAL.md check 2 (`V/vs_fourcheck_cover.py`).
   - U1 76, VB 23, VB 6 and VB 27 cubes are disjoint, and their union is exactly the 132 certified ids.
   - Every table row has the fresh exact cake line and passes.
   - Hash prefixes are current for VB's rows, and cert.json times predate the check for U1's rows.
   - Today's 27 equal `vb1118/n66/gen/list_last.txt`.

## Not checked by VS

- No cake_lpr re-run (about 2 GB heap per leaf).
- The consolidated re-run VERIFY_N66CUBES_1118_ALL.md mentioned by the claim, which was in progress at filing.
- The written soundness of the encoding (parent record).

Files (SHA-256): vs_cover_trim.py 180d3966f814db06…; cover_trim.out 11a88e144d00ba07…; fc_units.txt fdc92b06e99e07b8…; 
