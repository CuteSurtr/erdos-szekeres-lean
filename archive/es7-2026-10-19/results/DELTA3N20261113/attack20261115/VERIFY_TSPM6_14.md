**Verdict: CONFIRMED** (claim `tspm6-14`, verifier V2; updated 15 November 2026, 16:55 KST). Label CERTIFIED is
correct. The 14:46 verdict below was NOT CONFIRMED only because no cake_lpr re-run with enough heap existed, and that
gap is now closed.

**Update 16:55: an independent cake_lpr re-run by the main session, checked by V2.** V3's note
(`pm1115/claims/tspm6-14.note-from-V3.txt`) pointed to `round6/mainsession/tspm6recake/`, and I read its script and
outputs.
- **Script** (`recake.sh`): `zstd -dc <kept .zst> | tee FIFO | sha256sum`, then
  `cake_lpr --CML_HEAP_SIZE=1500 <CNF> FIFO`, then `grep -c '^s VERIFIED UNSAT$'`.
- **Inputs:**
  - CNF SHA-256 `921018d6…c9ac`, equal to the claim and to V2's regeneration;
  - archive SHA-256 `cdd5adea30f0b54e…3c1c`, which I recomputed on the kept file (equal);
  - streamed LRAT SHA-256 `aa802dae…e104`, equal to the claim and to V2's own stream hash.
- **Output:** `cake.out` is exactly `s VERIFIED UNSAT` (17 bytes, `grep -x` count 1). cake_lpr exited with status 0
  after 77 CPU s, with a peak RSS of 1.54 GB. It finished at 14:46:19.

The re-run was made by the main session, not by the claim's author (T3) and not by V2. Together with V2's encoder
review, CNF regeneration, stream hash and 18/18 semantic controls below, every check the house standard asks for is
now done.

---

*Original verdict, 14:46:* NOT CONFIRMED (incomplete, not refuted), from 14:34-14:45 KST. Every part of the check that
fits V2's budget passed. The decisive step, an independent cake_lpr
re-run of the 2.35 GB proof, could not be completed: **"CakeML heap space exhausted" at heap 300 MB**, the most V2's
0.4 GB budget allows under the 80 % rule. T3 used 1,500 MB. Until a verifier with a larger memory budget re-runs it
(command below), the CERTIFIED label for |S| = 14 rests only on T3's own cake_lpr run.

# Independent check: TS±(6) for every signotope with 14 points

**Claim (filed by T3).**
- Statement: if S is (5,6)-valid with |S| = 14, r ends a 4-cap and l starts a 4-cap, then U = S − r has a terminal-safe
  weak Δ or V = S − l has an initial-safe weak Δ.
- CNF: `tspm6_m14.cnf`, built by T4's `ts_cnf.py 6 14` plus `lr_cnf.py`, SHA-256 `921018d6…`.
- T3's run: UNSAT, with an LRAT of 2,348,480,245 bytes (`aa802dae…`) and T3's cake_lpr `s VERIFIED UNSAT` at heap 1500.

**Definitions.**
- candidates.md K2 and §0;
- terminal-safe as in CONJTS_TEST.md §2: every 3-cap (a,b,c) of A has (b,c) ending a 4-cap of U;
- initial-safe: the mirror notion, where (a,b) starts a 4-cap of V.

## What passed

1. **Encoder soundness**, read line by line: `t4/ts_cnf.py` (`caef7805…`) and `t4/lr_cnf.py` (`3e24db5b…`).
   - ts_cnf.py, which builds F_TS. Its base clauses are the same as those reviewed in [VERIFY_CB6.md](VERIFY_CB6.md),
     and its auxiliaries are one-way witnesses:
     - R_abc → (a,b,c) and (b,c,r) are caps, i.e. (a,b,c,r) is a 4-cap by the consecutive-caps fact, plus the clause
       OR R ("r ends a 4-cap");
     - F_K → K is a 4-cap of U;
     - NB(b,c) → for all u<v<b, (u,v,b) or (v,b,c) is a cup. That says "(b,c) ends no 4-cap of U", and every u,v < b
       is in U;
     - BAD(a,b,c) → (a,b,c) is a cap and NB(b,c);
     - Z_T → T is a gon of U;
     - rows for A ⊆ U with |A| ≤ 9.
     - A CONJ-TS′ counterexample with canonical auxiliaries satisfies every clause.
   - lr_cnf.py. Copy 2 renames triple t to μ(t) = (13−k, 13−j, 13−i) and shifts the auxiliaries by 4,017. On S's
     assignment, copy 2 is F_TS evaluated at the signs of the mirror image S′.
     - S′ is valid, since μ reverses each 4-tuple sequence and keeps the 4-point convexity rule.
     - r′ = μ(l) ends a 4-cap.
     - U′ = μ(V), and the terminal-safe weak Δs of U′ are the images of the initial-safe weak Δs of V.
     - So S′ is a CONJ-TS′ counterexample whenever S is a TS± counterexample. **Sound.**
2. **CNF regeneration.** In V2's folder I ran `python3 ts_cnf.py 6 14 > ts/ts6_m14.cnf`, then
   `python3 lr_cnf.py ts/ts6_m14.cnf 14 tspm6_m14.cnf`. The relative path matters: it is written into the comment line.
   The SHA-256 is `921018d64fece8116c647708f0bf4e7b2955676ac1aa606dc8b22b24acb3c9ac`, equal to the claim and to both
   copies on disk.
3. **Proof archive integrity.** `zstd -dc t3/cert/tspm6/tspm6_m14.lrat.zst` streams exactly 2,348,480,245 bytes with
   SHA-256 `aa802daed66b518f1da4c4ee132dec720931cd748172650ca1f5e2f98c83e104`, equal to T3's certify.jsonl.
4. **Semantic control of the certified CNF** (`control_ts.py`, `8980e4ff…`). For each set, the signs were added as
   units on variables 1..364, and the result was compared with V2's own brute force over all subsets. That brute force
   checks validity and both hypotheses and counts terminal-safe weak Δs of X − r and initial-safe weak Δs of X − l.
   **It agreed in 18 of 18 runs** (copy 1, copy 2 and full CNF each):
   - 10 sets made from the 15-point ROOT(6) failures by dropping an inner point (real m15_it10 drop 1,3,5,7,9,11,13;
     abstract root6_m15 drop 2,6,10). Both sides are nonempty (right 5-24, left 148-389): UNSAT, UNSAT, UNSAT.
   - 4 real 14-point sets with 0 terminal-safe weak Δs (`ts0_14_{0..3}.json`, see the observation below): copy 1 **SAT**,
     copy 2 UNSAT, full UNSAT.
   - Their 4 mirror images (x → −x): copy 2 **SAT**, copy 1 UNSAT, full UNSAT.

## What failed (budget, not mathematics)

The cake_lpr re-run was `replay_ts.sh 300` in unit `esr-agy-v2-tspm14` (CPUQuota 15 %, MemoryMax 400M). It streamed
the proof through a FIFO into `~/.local/bin/cake_lpr --CML_HEAP_SIZE=300` against the regenerated CNF.
- It stopped after 46 s of CPU with `CakeML heap space exhausted.` and exit 1. No verdict line was printed.
- The peak RSS was 313 MB. The output is in `cake_h300.time` (`8baeb4b2…`).
- A heap of 300 MB was enough for proofs up to 846 MB today (VERIFY_CB6.md) but is too small for this one.

**Requested re-run** (any verifier with ≥ 2 GB, e.g. heap 1500 in a 2G unit; about 80 s of CPU):

```bash
W=/home/jay/research/data/roadmap-20261115/pm1115/v2/tspm6-14; mkfifo /path/fifo
zstd -dc /home/jay/research/data/roadmap-20261115/pm1115/t3/cert/tspm6/tspm6_m14.lrat.zst > /path/fifo &
~/.local/bin/cake_lpr --CML_HEAP_SIZE=1500 $W/tspm6_m14.cnf /path/fifo | grep -x 's VERIFIED UNSAT'
```

## Side observation (EXACT, V2's own code; not filed as a claim)

**CONJ-TS′(6) is also false for real 14-point sets.** I inserted one integer point into the real 13-point counterexample
lattice-hyp (VERIFY_ATN_MAIN.md). Each of the four results `ts0_14_k.json` has, by exact checks:
- x strictly increasing and no collinear triple;
- no 5-cap and no convex hexagon;
- r ending a 4-cap;
- **0 terminal-safe weak Δs of U = S − r** (exhaustive over 2^13 subsets).

The left side survives with 287-436 initial-safe weak Δs, so TS±(6) holds on them. The sets are listed below, x-sorted:

- ts0_14_0: `(-800,13) (-484,51) (-303,159) (-285,-529) (-256,-219) (-241,84) (-239,-706) (16,-216) (83,-355) (91,-55) (198,126) (335,348) (516,790) (800,1164)`
- ts0_14_1: the same with (-259,111) in place of (-303,159)
- ts0_14_2: with (-301,185)
- ts0_14_3: with (-275,147)

None of the 286 one-point deletions of the 22 fifteen-point ROOT(6) failures fails CONJ-TS′: each has a nonempty
terminal-safe set (`scan_ts0.py`). That is why the insertion search was used.

## Files

- Folder: `/home/jay/research/data/roadmap-20261115/pm1115/v2/tspm6-14/`.
- Scripts: `replay_ts.sh` (`632717db…`), `control_ts.py` (`8980e4ff…`), `scan_ts0.py` (`153dcc63…`),
  `search_ts0_14.py` (`139a07c1…`), `v2lib.py` (`7c8b1ee0…`).
- `results.jsonl` (`24d9655b…`).
- Sets: `ts0_14_0.json` `7fd6a733…`, `_1` `e563be2d…`, `_2` `5ccaefdf…`, `_3` `141b5c61…`, plus their `_mirror` files.
