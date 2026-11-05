# STATUS20261105: where the project stands (5 November 2026, early morning KST)

This is the page to read first. It supersedes `STATUS20261104`, which remains the record of the previous evening.
Rigor labels: Lean-checked / certificate (an LRAT proof accepted by cake_lpr, i.e. its line `s VERIFIED UNSAT`;
lrat-check alone is not one) / exact computation / written proof (not refereed) / evidence only.

## Added 6 November 2026

- **Novelty check.** A literature novelty check of the main results, with adversarial reviews, is summarised in
  `NOVELTY20261106/README.md`. It found that the lrat-check defect of item 5 was already public upstream.
- **C6UPPER hash binding.** cake_lpr accepted all 64 sixfold cube proofs (32 per encoder) at solve time on
  3 November, but those logs record cube labels, not CNF or proof hashes. A hash-bound cake_lpr replay exists for only
  6 of the 64 (4 November review); the 4 November replay of all 64 used lrat-check only. A full hash-bound cake_lpr
  replay is planned.
  - *Update, 6 November 2026 (07:41 KST):* the hash-bound cake_lpr replay (6 Nov 2026) has finished. All 64 cube
    formulas were regenerated with their recorded hashes and solved again, and cake_lpr accepted every fresh proof: 64
    of 64 (`C6UPPER` §6, `C6UPPER/replay-2026-11-06/README.md`).
- **Budget-64 search.** It runs at about 20% of the machine (6 workers, since about 22:35 KST on 5 November) while
  the machine is needed for other work. At this rate the 9 November cutoff will stop it partway unless it is extended
  (`ES8UPPER20261105/README.md`).

## New since STATUS20261104

1. **The sixfold maximum is exactly 60** (`SIX60`).
   - Five exact 60-point 6-fold sets in general position (ten nested hexagons; A, B, C, C' and D, five pairwise
     different order types) have no 8 points in convex position. Each is checked by three independent
     implementations (exact computation).
   - With `C6UPPER` (61 or more points excluded; certificate), the 6-fold value is 60. A 6-fold set in general
     position cannot contain the centre, so its size is a multiple of 6: ES(8) = 65 holds for 6-fold symmetric sets,
     and the largest size it allows, 60, is attained.
   - Two independent methods found them: alternating projections between real configurations and phase-guided SAT
     models, and a phase-fixed SAT plus LP search (orientations are linear in the inverse radii once the phases are
     fixed).
2. **The chord lemma** (`CHORD20261105`; written proof; for m = 6 a degree-2 certificate per clause, checked by
   exact computation; independent review).
   - It fixes, from phases alone, the orientation of any triple with two points on one layer. The encoder had no
     clause for antipodal triples and missed outer points beyond an inner chord.
   - For m = 6 it adds 524 clauses, and it is all the local degree-2 information that prunes models.
   - It explains why the `SIX10CEGAR` "hard cores" looked hard: their SDP never received phase rows.
   - The generator covers any m.
3. **The known record sets do not extend** (certificate: 94 LRAT proofs, first checked by lrat-check only, regenerated and accepted by cake_lpr after item 5). Neither 54-point 6-fold order type extends to
   60 points, and the 4-fold 52-point set does not extend to 56. The 5-fold 56-point set extends only abstractly
   (innermost layer), and that extension was not realized (`SIX10LINUX20261105` §5).
4. **The 101 hard models of SIX10CEGAR are all non-realizable** (`SIX10LINUX20261105`; exact, re-checked).
   - They are excluded by facial-reduction degree-2 certificates, by biquadratic final polynomials on 3–4 layers, and
     by GP violations.
   - Each GP family comes down to a single orbit sign.

5. **The lrat-check on this Linux machine is the unpatched, unsound build** (`LRATCHECK20261105`).
   - The defect was already public upstream (drat-trim issue #31, 2022; regression reported in issue #42 and PR #43,
     29 September 2026). `E2` (20 Oct) found it independently and patched it. The headline certificates are anchored
     on cake_lpr.
   - It was rediscovered here because the Linux setup built drat-trim without the E2 patch.
   - A project-wide audit (`LRATCHECK20261105/AUDIT.md`) found every headline result unaffected except PRIMEFOLD
     Theorem E (lrat-check only). That theorem is **now certified**: 7/7 regenerated CNFs with matching hashes were
     accepted by cake_lpr (`LRATCHECK20261105/recheck/`).
   - The 5 November items that had used lrat-check were all re-checked with cake_lpr.

## Updated table (k = 8, largest m-fold symmetric set without a convex octagon)

| Symmetry | Value | Status |
|---|---|---|
| reflection | 46 | via Baek, Lean-checked bounds |
| half-turn | >= 64 (= 64 if ES(8) = 65) | exact computation (`ES8SYM`) |
| 3-fold | >= 61 | open |
| 4-fold | >= 52 | open (threshold run below) |
| 5-fold | >= 56 | open (threshold run below) |
| 6-fold | **exactly 60** | lower bound exact computation (`SIX60`); upper bound certificate (`C6UPPER`) |
| 7-fold | exactly 64 | certificate (`C7UPPER`, two encoders) |
| order >= 8 | 1 | Lean-checked |

On 6 November the note (`WRITEUP/note`, table `tab:k8`) and the draft k = 8 section
(`STATUS20261104/k8_section.tex`) were updated from "54 or 60" to 60. Merging the k = 8 section into the note is still
pending; this is left to the author.

## Running at the time of writing: 5-fold and 4-fold thresholds with the chord lemma

These instances are the threshold formulas of `ROT456`:
- `gen.py 5 8 13`, 65 points, SHA-256 `d7bbb743…`;
- `gen.py 4 8 17`, 68 points, SHA-256 `4843a9e9…`.

Both are byte-identical to the recorded CNFs. The chord lemma's new clauses are added (882 and 801), together with
the reflection unit (H(1), resp. Y(1,2)) and one total phase order of layers 1–4 per cube (24, resp. 12 cubes).
CaDiCaL writes text LRAT. Since 13:01 KST each UNSAT proof is checked by cake_lpr (supervisor v2). The work directory is outside git:
`<rot45-work-dir>` (`results.tsv`, `cubes5/`, `cubes4/`).

UNSAT of all cubes of one instance would give the m-fold case of ES(8) = 65. The soundness of the added clauses rests
on the written chord-lemma proof and its exact case analysis. An independent review of the general-m generator
(`CHORD20261105` §6) proved every added clause by its own exact verifier and found no violation.

**Final state (16:00 KST): no phase-order cube closed.** The 5-fold count is 0 of 24 (19 unresolved, 5 never
started) and the 4-fold count is 0 of 12 (11 unresolved, 1 lost). The transitivity patterns, 40 + 20, are all accepted
by cake_lpr. Most lanes ran about 14.9 h. The 5-fold and 4-fold cases stay **open; no bound is claimed.** Details and
what further work would need are in `ROT45CHORD20261105` (Results). The unfinished partial proofs (about 1.3 TB) are
deleted on the author's instruction (manifest in `ROT45CHORD20261105/logs/`).

## ES(8) upper bound (started 5 November, afternoon)

- `ES8UPPER20261105/MEMO.md` is a scoping memo, built from 9 readers and reviewers. The residual side is tight over the
  present rows. The balanced optimum lies in [64, 72], so **balanced budget 64 would give ES(8) <= 310 with no new
  mathematics**, at about 1,100–1,450 CPU-h of search, plus a compact Lean checker.
- **Compact checker prototype** (`experiments/omission-compact-checker-2026-11-05`). It has a soundness theorem (no
  sorry, standard axioms only). It is 2.2x less kernel time and 24–85x less output per leaf than the current
  pipeline. Gate G2 is narrowly missed (0.35 s per leaf against 0.3), and a concrete lookup optimisation is
  identified.
- **Pilot** (from 16:02 KST, `<es8-pilot-dir>`):
  - budget 64 against 63 on 28 stratified contexts plus the 4 lowest-LP contexts;
  - CP-SAT hunts for balanced vectors with at most 64 holes, and with at most 71 holes.
  - **Pilot result:** all 32 budget-64 contexts closed, pooled ratio **9.34**. That passes the gate, and the
    projection is about 1,500 CPU-h.
  - **Exact side result:** a 71-hole balanced vector satisfies all 3,131 constraints (re-checked against the
    catalog source). So h_B^min lies in [64, 71], and the present catalogs cannot prove better than ES(8) <= 304.
- **Full budget-64 search is running** from 17:24 KST on 28 workers: systemd user unit `es8-b64-campaign`, cutoff
  2026-11-09 17:00 KST (`ES8UPPER20261105/README.md`). No bound below 311 is claimed before the Lean check. It was
  throttled later that evening (see "Added 6 November" above).

## Decisions pending (unchanged from STATUS20261104 unless noted)

1. ~~Push the branch~~. Done on 5 November, about 19:30 KST: `es7-night-2026-11-01`, including the merged review branch
   and all 5 November commits, is on `origin`.
2. Update and merge the k = 8 note section (now with 6-fold = 60).
3. Send the k = 8 email (draft on the Mac). It now needs the 6-fold value 60.
4. Optionally fast-forward `es7-cloud`.
