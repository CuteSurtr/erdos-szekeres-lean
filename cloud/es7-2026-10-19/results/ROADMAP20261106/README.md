# ROADMAP20261106: where the project should go next (6 November 2026)

Produced by a read-only planning workflow: four readers mapped the open fronts (ES(8) bound, symmetric k = 8,
rigor and publication, k = 7 and the rest), three planners wrote roadmaps from different angles (impact,
publication and rigor, feasibility at about 20% CPU), and a judge scored them and spot-checked the repo. This is a
plan, not a result; nothing below is claimed as proved. The judge's verdict follows verbatim.

*Note added 6 November 2026, after 07:41 KST.* The `c6upper-replay` job mentioned below has finished. In the hash-bound
cake_lpr replay (6 Nov 2026), cake_lpr accepted the fresh proofs of all 64 cube formulas, 64 of 64, each verdict bound
to the CNF and proof hashes. The job continued as unit `c6upper-replay-par` from 04:52. The record is in
`C6UPPER/replay-2026-11-06/README.md` and `C6UPPER` §6. Step 3D was then carried out as follows:
- the per-cube hash and verdict table is in `C6UPPER/replay-2026-11-06/README.md`, not in `C6UPPER/README.md`;
- `C6UPPER/README.md` has a summary in §6;
- `symmetric_extremal.tex` (abstract and the sixfold trust row) and `k8_section.tex` were updated.
The text below is unchanged.

---

## Judge's verdict (6 Nov 2026, read-only)

**What I checked in the repo:**
- `ES8SLACK/review/C1_certificates/replay63.out` gives 782,437 of 782,437 leaves, "ALL LEAVES EXCLUDED", SHA-256 `d51f0dc2…`. The arithmetic of 311 has already been replayed exactly by a separately written checker, so the Rust checker that roadmap D3 proposes is redundant.
- The Catalan identity is already recorded in `PRIMEFOLD/README.md:147` (A000245). The even-m half of the guess is weak: `PROOFS.md:284` shows the m = 10 relaxation satisfiable at 46, which is more than Cat(5) = 42.
- `c6upper-replay` is active and working on encoder-A cube `c00001`. Its memory is at 14.8 of 16 GB MemoryMax, which is worth watching through journalctl only.
- `es8-b64-campaign` is active and has used 23.8 CPU-h so far.

## 1. Where we should get to (2–4 weeks)

1. **Preprint P1, a draft ready for the author by about 12 Nov.** Theorem: ES(8) = 65 holds for 6-fold and 7-fold symmetric sets, and the maxima 60 and 64 are attained.
   - Upper bounds rest on cake_lpr certificates, 64 of 64 plus 2 of 2 hash-bound.
   - The reduction is Lean-checked.
   - The encoding Soundness Theorem goes in the paper as a written proof (not refereed), with encoder B as the primary encoder.
   - Lower bounds are exact computations from printed generators.
   - This is CICM/EuroCG-level work and the strongest result the project has.
2. **ES(8) ≤ 311 made reproducible.** The compact checker runs on the full 782k + 438k leaves on a second platform, with artifacts kept. That is the precondition for the Schroeder email. The math is incremental (89 of 97 points are Schroeder's). The goal here is credibility, not a new bound.

## 2. Ranked plan

| # | Step | Significance / P(success) | Cost | Credibility gain / risk |
|---|---|---|---|---|
| 1 | P1 note: soundness section, exact Z[ζ7] clause check, Zenodo manifest, 64/64 replay recorded | Medium / ~90% | ≤1 core-h plus the running replay | High. Risk: a replay cube fails, which pauses the 6-fold claim only |
| 2 | 311 compact recheck: lookup optimisation, Fcat bridge, residual adapter, full run, then the Schroeder email | Low–medium / ~70% | 100–200 CPU-h, on the campaign's cores after its cutoff or on a cloud VM | High for 311. Risk: never run above 995 leaves, 12 GB per module |
| 3 | 4-fold t = 14 CEGAR (lift-Farkas, GP and final-polynomial cuts), with the realizer as its dual | Medium–high (exact value 52, or a 56-point set) / 20–30% | 20–200 core-h on the freed replay core; go/no-go at 24 core-h | Research bet |
| 4 | Lean encoder B for m = 6 (EmptyHexagonLean standard) | Medium (rigor, CPP/ITP) / ~50% in 4 weeks | About 0 CPU, 2–4k LOC | Moves soundness items (i)–(iv) to Lean-checked. Does not block P1 |
| 5 | Cheap exact side results: SMQH App. B comparison (49 vs 46 classes) and a written all-h proof of the odd-m Catalan lower bound | Low–medium / 50–60% | <10 core-h | No priority claims before every class is closed |
| 6 | Theorem A (k = 7) note cleanup and lane spot checks | Medium / high | About 25 CPU-h, after step 2 | Second paper |

## 3. Start now (next 24 h, fits the 20% cap)

- **A. Soundness section (no CPU).**
  - Write a new standalone file `WRITEUP/note/k8_soundness.tex`, drawing on `C6C7REVIEW/SOUNDNESS.md`, the `C7UPPER/gen.py` docstring and `C6UPPER/encb/gen_b2.py`.
  - Done when: a lemma chain plus a Soundness Theorem is written, each lemma is tagged with its `LAYERLEAN/LayerLemma.lean` name or "written proof", and it covers the omitted antipodal case, even-m genericity, the 3-cycle stabiliser, Y(1,2) and the cube cover.
- **B. Exact Z[ζ7] check (minutes, nice 19).**
  - Check that the 7-fold 63- and 64-point sets satisfy every clause of encoder B's (7,8,9) formula, and that H(1) flips for the mirror image.
  - Done when: 0 violations in exact arithmetic, and the generator output hashes `542c8a3a…`, `479e31a9…` and `b4d29017…` are unchanged.
- **C. Compact-checker optimisation.**
  - In a copy of `experiments/omission-compact-checker-2026-11-05/CompactChecker/Fast.lean`, store row indices as literals and fuse the three passes.
  - Benchmark only the 64-leaf Chunk733 (about 30 s, about 6 GB).
  - Done when: s/leaf, peak RSS and KB/leaf are logged in `logs/`.
- **D. When the replay ends (do not touch the unit):**
  - Add a per-cube hash and verdict table to `C6UPPER/README.md`.
  - Update `symmetric_extremal.tex:674` and `k8_section.tex`.
  - Done when: 64 of 64 show `s VERIFIED UNSAT`. Otherwise drop the 6-fold claim and keep the 7-fold one.

## 4. Stop or deprioritize

- **Budget-64 campaign (route to 310).** Do not extend it; let it stop on 9 Nov at 17:00, at about a third done. That is lossless, since closed contexts remain usable. The remaining cost is about 1,800–2,450 CPU-h for one point that a geometer would not notice. Do not export its tree before step 2 passes.
- **4-fold and 5-fold threshold SAT lanes (m5K8t13, m4K8t15–17).** About 445 core-h closed 0 of 36 cubes. No new lane, and not even the 20–60 core-h pricing run, until the campaign ends and kissat/march_cu are approved.
- **ES(8) rows.** New balanced rows have under 5% chance of reaching 304. Residual capacity 21 gains +1 at best, and 22-owner models already exist.
- **Other dead ends.**
  - Regenerating the Theorem A proofs (about 2,050 CPU-h).
  - Construction searches seeded from C1 or the 52-point set.
  - Growing `symmetric_extremal.tex` as a survey.
  - Claiming the even-m Catalan pattern.

## 5. Decisions only the author can make

1. The campaign cutoff, and whether to reassign its 5 cores to the 311 recheck for 2–3 days. I recommend both.
2. Whether to rent a cloud VM (64 vCPU, 512 GB, about 4–6 h) for the 311 recheck.
3. P1 packaging:
   - focused (recommended) or combined with Theorem A;
   - whether to merge `k8_section.tex`;
   - author and affiliation, arXiv endorsement;
   - whether to post before the Lean encoder is done.
4. When to email Schroeder, and whether to contact the SMQH authors.
5. Whether to copy the CEGAR tools from the work directories into Git, and whether to build kissat and march_cu.
6. The k = 8 email draft on the Mac, which still says "54 or 60".
