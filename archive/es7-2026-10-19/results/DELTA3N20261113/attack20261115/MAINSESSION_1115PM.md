# Main-session checks, 15 November 2026 afternoon (13:05-19:00 KST)

Each item is the main session's own exact check, using only the coordinates or sign strings named. Agents' records and
verifier files are linked; the team workflow and claims protocol are in `/home/jay/research/data/roadmap-20261115/pm1115/`.
Code: `/home/jay/research/data/roadmap-20261115/round6/mainsession/root15/`.

## ROOT(7) is false for a REAL 17-point set (EXACT; checked 14:13)

- Set: `/home/jay/research/data/roadmap-20261115/pm1115/r7/root7_real17.json` (SHA-256
  `d9b5e6c453fb6f75ab0bbdab77fe0545682caafd059c5d36ddfda35dd7ab7d6e`). Agent R7 found it with the CEGAR/BFP loop on
  `root7_m17.cnf`: iteration 4 gave a model, and `realize_sig.py` (seed 1) realized it. Record:
  [ROOT7_M17_REALIZE.md](ROOT7_M17_REALIZE.md). Claim: `root7-real-17`.
- The set (x strictly increasing; r = the last point):
  `[[-2384,413],[-1837,269],[-751,1129],[-719,-13],[-717,-145],[210,539],[211,-184],[383,-293],[418,-334],[424,4678],
  [1067,2579],[1072,-383],[2049,-519],[2054,-589],[2073,7779],[2357,8412],[2384,-1781]]`
- Check: `root_real_check_n.py <file> 7` (`cff5fb0a5dfaec55…`; output `root7_real17_check.out.json`). It uses integer
  orientations only:
  - no collinear triple; convexity by exact point-in-triangle tests on 4-subsets; caps by the all-triples definition;
  - an exhaustive search over the 2^16 subsets of U.
- The same script on the real 15-point ROOT(6) set reproduces the earlier counts (86 / 37 / 0 / 0 / 254 / 992 / 0).
- Results:
  - The sign string in the file matches the coordinates.
  - **0 five-caps and 0 convex 7-gons**, so the set is (5,7)-valid.
  - 170 four-caps, **117 of them contain r**.
  - U has 290 convex hexagons and 9,808 weak Δs, and **0 rooted weak Δs**.
- Context:
  - ROOT(7) at 17 points was first found false for an abstract signotope by agent T3: claim `root7-m17-abstract`,
    CONFIRMED by V1 ([VERIFY_ROOT7_M17.md](VERIFY_ROOT7_M17.md)).
  - That first model is not realizable: claims `root7-m17-nonreal-1` (R7) and `root7-m17-t3-nonrealizable` (T1), both
    CONFIRMED.
  - The least size at which ROOT(7) fails is not determined here; see PROBES_1115PM.md for m = 15 and 16.
- **Second party: V1 CONFIRMED it at 14:13** ([VERIFY_ROOT7_REAL17.md](VERIFY_ROOT7_REAL17.md)). T1 found a second,
  independent real 17-point example (claim `root7-real-17-t1`).
- No ES bound changes.

## ROOT(6) is false for a REAL 15-point set (EXACT; checked 13:39)

See [ROOT6_MAIN.md](ROOT6_MAIN.md) (update sections) and [VERIFY_ROOT6_REAL15.md](VERIFY_ROOT6_REAL15.md) (V3,
CONFIRMED).

## LRR(6) at m = 15: fresh cake_lpr re-run of T1's proof (14:19-14:21)

- Proof `pm1115/t1/lrrcert/cert/lrr6_m15.lrat.zst` for `pm1115/t3/cnf/lrr6_m15.cnf`. It was streamed through a FIFO
  (`zstd -dc | tee fifo | sha256sum`), so no decompressed copy was written. Unit `esr-vfy-main-lrr6`, heap 1400 MB.
  Script and outputs: `round6/mainsession/lrr6recake/`.
- Result: **`s VERIFIED UNSAT`** (exactly 1 line).
  - LRAT SHA-256 recomputed while streaming: `625dffe51617b889…`. CNF SHA-256: `0555d770b08e2e0d…`. Both equal T1's
    `certify.jsonl`.
  - Wall time 2 min 18 s; peak RSS 1.44 GB.
- With V1's confirmation of the encoder, the CNF regeneration and the semantic tests ([VERIFY_LRR6.md](VERIFY_LRR6.md)),
  the m = 15 certificate now has an independent cake_lpr re-run. **LRR(6) holds for every (5,6)-valid signotope and every
  point set** (CERTIFIED at m = 15; ROOT(6) CERTIFIED at m ≤ 14; m ≥ 16 vacuous).

## TS±(6) at m = 14: fresh cake_lpr re-run of T3's proof (14:45-14:46), requested by V2

- V2 returned NOT CONFIRMED (incomplete, not refuted) on claim `tspm6-14` ([VERIFY_TSPM6_14.md](VERIFY_TSPM6_14.md)).
  Every other part passed: encoder soundness, byte-identical CNF regeneration, proof-archive integrity and an 18/18
  semantic control. Only the cake_lpr re-run failed, with "heap exhausted" at the 300 MB that V2's budget allowed.
- Main-session re-run: `pm1115/t3/cert/tspm6/tspm6_m14.lrat.zst` was streamed through a FIFO into cake_lpr (heap
  1500 MB) against `pm1115/t3/cnf/tspm6_m14.cnf`. Unit `esr-vfy-main-tspm6`; files in
  `round6/mainsession/tspm6recake/`.
- Result: **`s VERIFIED UNSAT`** (1 line).
  - LRAT SHA-256 recomputed while streaming: `aa802daed66b518f…`, equal to the record. CNF SHA-256: `921018d64fece811…`,
    equal to V2's regeneration.
  - Wall time 1 min 28 s; peak RSS 1.54 GB.
- With V2's passed checks, **TS±(6) holds for every signotope, hence every point set, with 14 points** (CERTIFIED;
  independent re-run done). The claim's verdict file still says NOT CONFIRMED, because the re-run was done by the main
  session, not by a verifier agent.

## LR(6) at m = 15, second certificate: fresh cake_lpr re-run (15:06-15:08), requested by V2

- Claim `lr6-m15-second` is T4's CNF `lr6_m15.cnf` (round 6's `root_cnf.py 6 15` plus the mirrored copy from
  `lr_cnf.py`), with T3's proof. V2 returned NOT CONFIRMED (incomplete, not refuted) only because its cake_lpr run hit
  the heap limit at 300 MB ([VERIFY_LR6_M15_SECOND.md](VERIFY_LR6_M15_SECOND.md)).
- Main-session re-run: `pm1115/t3/cert/t4lr6/t4_lr6_m15.lrat.zst` was streamed through a FIFO into cake_lpr (heap
  1500 MB) against V2's regenerated `pm1115/v2/lr6-m15-second/lr6_m15.cnf`. Unit `esr-vfy-main-lr6b`; script
  `round6/mainsession/recake_generic.sh`; outputs in `round6/mainsession/lr6secondrecake/`.
- Result: **`s VERIFIED UNSAT`** (1 line).
  - LRAT SHA-256 recomputed while streaming: `fc824a77e126c92a…`, equal to the record. CNF SHA-256:
    `cae7193d2722f37b…`, equal to V2's regeneration.
  - Wall time 2 min 26 s; peak RSS 1.54 GB.
- So both LR(6) m = 15 certificates, from two encoders, now have a fresh cake_lpr re-run.

## TWO-ENV#(6) (hypothesised form) at m = 13, 14, 15: fresh cake_lpr re-runs (16:06-16:16)

- V1 CONFIRMED claim `twoenv6-m15`: encoder soundness read, CNF regenerated, semantic tests on 6 sets, other sizes by
  the cited claims. V1 did not re-run cake_lpr (heap 1300 MB, over its budget).
- Main-session re-runs of T3's proofs `pm1115/t3/cert/te6/te6_m{13,14,15}.lrat.zst` against `pm1115/t3/cnf/te6_m*.cnf`,
  streamed through a FIFO, heap 1500. Unit `esr-mainv-te6`, 50 % and later 25 % CPU; outputs in
  `round6/mainsession/te6recake/m13|m14|m15/`.
- Each gave **`s VERIFIED UNSAT`** (1 line), with LRAT and CNF SHA-256 equal to T3's `certify.jsonl`:

  | m | CNF | LRAT |
  |---|---|---|
  | 13 | `1fe964af…` | `f988e0df…` |
  | 14 | `66da85a3…` | `663d3e5f…` |
  | 15 | `fde81f37…` | `87f7f7de…` |

- A first attempt as unit `esr-vfy-main-te6` (16:05) was stopped and moved. Its "vfy" track name shared U1's memory
  budget, and the memory guard cleanly stopped U1's cake unit for cube ohhhoo_23o_49o_44o (track 3,511 > 3,500 MB).
  U1 re-ran its check. That partial attempt is in `te6recake.partial-1606/`.

## Weak D(5,8) at m = 16: fresh cake_lpr re-run (16:19-16:23)

- Claim `wd58-m16` (T3). CNF `pm1115/t3/cnf/wd58_m16.cnf` comes from DELTA2N's reviewed eager encoder
  Enc(5,8,16,weak), through T3's `gen_weakD.py`, which imports `eager_cert.py` unchanged. SHA-256 `d6d34086…`; 15,640
  variables and 778,924 clauses. T3: UNSAT after 4,973 s; LRAT 5,572,040,812 bytes.
- Main-session re-run: `pm1115/t3/cert/wd58/wd58_m16.lrat.zst` was streamed through a FIFO into cake_lpr (heap
  2000 MB) in unit `esr-mainv-wd58`. Outputs in `round6/mainsession/wd58recake/`.
- Result: **`s VERIFIED UNSAT`** (1 line).
  - LRAT SHA-256 recomputed while streaming: `68c70856c1618ec85ab2151b484ba77ddc3b69462e52ddbaa51c65d5e11f8168`, equal
    to the claim. CNF SHA-256 `d6d340863685d92e…`, equal to the claim.
  - Wall time 4 min 1 s; peak RSS 2.06 GB.
- With DELTA2N's certificates for m ≤ 15: **weak D(5,8) holds for every signotope, hence every point set, with at most
  16 points** (CERTIFIED). It is open from 17 points. No ES(8) bound changes.
- V2 returned NOT CONFIRMED (incomplete, not refuted) at 16:23 ([VERIFY_WD58_M16.md](VERIFY_WD58_M16.md)). Every part
  passed except a cake_lpr run, which V2's 0.4 GB budget does not allow:
  - the encoder's soundness, read against Lemma S;
  - `gen_weakD.py 5 8 15` regenerates DELTA2N's certified m = 15 CNF byte for byte, and `gen_weakD.py 5 8 16` gives
    `d6d34086…`;
  - the proof archive and stream hashes equal the claim;
  - the m ≤ 15 range is complete per DELTA2N.
  The main-session re-run above supplies the missing cake_lpr step.

## TWO-ENV#(6) at m = 15, second certificate (T4's encoder): fresh cake_lpr re-run (18:02-18:11)

- Claim `twoenv6-m15-second`. The CNF `pm1115/t3/cnf/twoenv6_m15.cnf` comes from T4's `twoenv_cnf.py` built on round 6's
  `env_cnf.py`. It shares no code with T3's `tenv_compact.py`. SHA-256 `b48d3fac…`.
- Main-session re-run: `pm1115/t3/cert/t4te6/twoenv6_m15.lrat.zst` was streamed through a FIFO into cake_lpr (heap
  1500 MB) in unit `esr-mainv-te6b`. It ran at 100 % and then at 25 % CPU, after the summed quota briefly reached 16.41.
  Outputs in `round6/mainsession/te6secondrecake/`.
- Result: **`s VERIFIED UNSAT`** (1 line).
  - LRAT SHA-256 recomputed while streaming: `2f07f3c931c1b2af7406974f71fcc61efc104fb243ad782d3ce22fb12040d341`, equal
    to the claim. CNF SHA-256: `b48d3fac3b4fa7d7…`.
  - Wall time 8 min 44 s; peak RSS 1.54 GB.
- So TWO-ENV#(6) at 15 points has two certificates, from encoders that share no code, and each has an independent
  cake_lpr re-run.

## C2(6) at m = 15 (P1): fresh cake_lpr run (18:20)

- Claim `p1-c2six`. C2(6) says: in every (5,6)-valid signotope whose rightmost point r ends a 4-cap and lies in no weak
  Δ, the leftmost point starts a 5-cup. At ≤ 14 points it is vacuous by ROOT(6), and ≥ 16 points is vacuous.
  CNF `pm1115/p1/c2_nolcup6_m15.cnf` (SHA-256 `1d703c4c…`); proof `pm1115/p1/c2_nolcup6_m15.lrat.zst`.
- V1 CONFIRMED the claim at the label COMPUTED (hypotheses, CNF regeneration, controls). Its budget did not allow a
  cake_lpr run, and P1's own run at a 480 MB heap and 15 % CPU had not finished.
- Main-session run: the proof was streamed through a FIFO into cake_lpr (heap 1500 MB) in unit `esr-mainv-c2six`.
  Outputs in `round6/mainsession/c2sixrecake/`.
- Result: **`s VERIFIED UNSAT`** (1 line).
  - LRAT SHA-256 recomputed while streaming: `0b5745db5b3d62a913edc0aa9d747a923875735f789072a2c6ba6ceee45ffd35`, equal
    to the claim. CNF SHA-256 equal to the claim.
  - Wall time 27 s; peak RSS 1.54 GB.
- **So C2(6) is CERTIFIED for every signotope, hence every point set.** It is one of the two conjectures in P1's
  reduction C1(n) ∧ C2(n) ⟹ LR(n) ([PROOF_LR_ATTEMPT_P1.md](PROOF_LR_ATTEMPT_P1.md)), now settled at n = 6. C1(6), C2(7)
  and C1(7) are not settled here.
