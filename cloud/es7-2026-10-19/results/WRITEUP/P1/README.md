# P1: sixfold and sevenfold rotationally symmetric point sets without a convex octagon

First full draft of preprint P1, written 6 November 2026 (KST) and revised the same day after an internal review (see
"Revision after review"). Not refereed, not circulated.

**Theorem of the paper.** For k = 8, the largest m-fold rotationally symmetric set in general position with no 8
points in convex position has exactly 60 points for m = 6 and exactly 64 for m = 7. Since 6-fold sets in general
position have 6t points and 7-fold ones 7t or 7t + 1, this is the 6- and 7-fold case of ES(8) = 65 together with
attainment of the largest sizes it permits (the paper says so explicitly, following `NOVELTY20261106` "Do not claim").

**Rigor, as stated in the paper.** Upper bounds: certificates (cake_lpr `s VERIFIED UNSAT` only), two separately
implemented encoders, on top of a Lean-checked reduction (`LAYERLEAN`) and a written soundness proof (not refereed) with
gaps (G1)–(G4). Sixfold: in the hash-bound cake_lpr replay (6 Nov 2026) all 64 cube formulas, regenerated with
hashes matching the record, were solved again, and cake_lpr accepted every fresh proof (64 of 64,
`C6UPPER/replay-2026-11-06`). Before it, the 64 verdicts of 3 November were on record by cube label only, and 6 of the
64 were hash-bound (4 November). The layer lemma is Lean-checked in its core; the assembly
of the layers is a written proof (G4). Lower bounds: exact computation. No priority claim; "we did not find prior
work" only.

## Files

| file | content |
|---|---|
| `p1.tex` | the paper (30 pages). Inline bibliography, no BibTeX. |
| `p1.pdf` | compiled with pdflatex (TeX Live 2025), three passes, each exit 0: **0 errors, 0 undefined references or citations, no LaTeX warnings**; 1 overfull box (13.3 pt, the head of Lemma 5.2, from the reviewed source) and 2 underfull boxes (badness 1270 and 1953). Rebuilt on 6 November 2026 after the replay status was filled in, with the same result (30 pages). Rebuilt again on 6 November 2026 (about 10:30 KST) after the one-clause 311 update in §1 (open item 14), with the same result. Rebuilt again on 6 November 2026 (about 13:30 KST) after the proof of Corollary k8s:cor:geom was corrected (it had cited Lemma k8s:lem:affine for the translation of the centre to O, although that lemma's admissibility clause assumes g(O) = O; the translation step is now argued directly, and part (b) no longer says "the same" for a step that has no cube split): 31 pages, 0 errors, 0 undefined references, 1 overfull box. |
| `p1.log` | the log of the third pass, kept for reviewers. |
| `k8_soundness_p1.tex` | Section 5 of the paper: an adapted copy of `WRITEUP/note/k8_soundness.tex` (see below). |
| `tables/*.tex` | data fragments \input by `p1.tex` (sixfold cube table, hash appendix, seeds of the point sets). Generated; do not edit. |
| `tools/make_tables.py` | generates `tables/` from the repository records and checks them (standard library only; calls `git show` once, read-only). |

Build: `pdflatex p1 && pdflatex p1 && pdflatex p1` in this directory (run under the session's caps with
`systemd-run --user --scope -p MemoryMax=12G nice -n 5`; the rebuild after the replay used `-p MemoryMax=4G -p
MemorySwapMax=0` and `nice -n 10`); then delete `p1.aux`, `p1.toc`, `p1.out` and keep `p1.log`.
Regenerate the tables first with `python3 -I WRITEUP/P1/tools/make_tables.py` (prints `PASS`; exits 1 on any hash or
structure mismatch).

**Where the table values come from.** The generated fragments take every number and hash from a record: seeds,
coefficient sizes and scales from the `.pts` files (scale from their header line); point-set hashes from
`SIX60/sets/SHA256SUMS.txt` and `PRIMEFOLD/SHA256SUMS`; cube wall times from `C6UPPER/logs/cubes.txt` and
`encb_cubes.txt`; proof sizes and hashes from `C6UPPER/SHA256SUMS.txt`; the replayed cubes (daggers) from the
`sampling` record of `C6C7REVIEW/replay.json` (whose CNF and proof hashes are checked against `C6UPPER/SHA256SUMS.txt`);
the cube orders computed from the cube labels and compared with `C6UPPER/README.md`; the Lean file hash computed and
compared with the prefix recorded in `WRITEUP/note/k8_soundness.tex` and with the blob of commit 393619a57. The script's
own constants are the file lists, their labels and the record locations. Numbers in the body of `p1.tex` outside
`tables/` (for example Table 3, the sevenfold certificates, and the convex-subset counts of Tables 5 and 6) are typed
from the records named next to them; they were compared with those records by hand and by the re-runs listed below.

## Structure of the paper

1. Introduction: problem, SMQH and their §7 suspicion, Theorem 1.1, Corollary 1.2 (ES(8) = 65 within the two classes),
   Remark 1.3 (affine symmetries), Table 1 (m = 2..7 and m ≥ 8), method, what is and is not claimed, related work and
   credit (Erdős–Szekeres, Szekeres–Peters, Marić, Heule–Scheucher, Subercaseaux et al. ITP 2024, SMQH CICM 2025 which
   stops at k = 7, Mackey, Baek, Baek–Balko, Dumitru with priority for fivefold k = 7, Georgiev et al.), "what we did
   not find".
2. Definitions, Lean conventions, rigor labels.
3. The layer reduction (Lean-checked core): layer lemma (core Lean-checked, assembly written), encoding facts (a)–(e),
   `Sixfold66`/`Sevenfold70` verbatim,
   Proposition 3.3 (`sixfold_octagon`, `sevenfold_octagon`), build/axioms, what is not in Lean.
4. The encodings: variables, four clause families, encoders A and B, symmetry breaking, instance sizes, validation.
5. Soundness (the adapted reviewed section, rigor tags and gaps G1–G4 unchanged).
6. The certificates: checkers and the lrat-check defect; sevenfold table; sixfold split, 12-cube table (both encoders,
   times, sizes, proof-hash prefixes of the 3 November proofs, the 4 November replays marked), runs, what has been
   replayed (including the hash-bound cake_lpr replay of 6 November, 64 of 64); Theorem 6.1.
7. Lower bounds: Theorem 7.1, format and seeds (set D and `c7_64pts_small` in the text), how found, verification by
   separately written programs, re-run of 6 November, convex-subset count tables, order types, consistency with the
   encodings, Remark 7.2 (history of 54 vs 60).
8. Trust and rigor table; what is trusted; further limitations.
9. Reproducibility: commands, run times, machines.
10. Open problems: 3-, 4-, 5-fold (threshold runs closed nothing; evidence only), half-turn, larger k, formalization.
Appendix A hashes (with the first twelve digits of the 24 replay proofs of the phase-order cubes), Appendix B seeds
of all thirteen set files (twelve order types).

## Sources (paths under `cloud/es7-2026-10-19/results`)

- `STATUS20261104/k8_section.tex` (SHA-256 `04af8189…`, before its replay update of 6 November): exposition reused for
  §§1, 3, 4, 6 and the open problems.
- `WRITEUP/note/k8_soundness.tex` (SHA-256 `197bc2149619e052…`, commit 597961bbd): Section 5.
- `WRITEUP/note/symmetric_extremal.tex`: context, Table 1, literature and bibliography entries.
- `C6UPPER/README.md`, `C6UPPER/SHA256SUMS.txt`, `C6UPPER/logs/{cadical_summary,encb_cadical_summary,cake,encb_cake,regen,replay_2026-11-04}.txt|log`.
- `C7UPPER/README.md`, `C7UPPER/SHA256SUMS.txt`, `C7UPPER/logs/cake_{A,B}.out`, `C7UPPER/repro.sh`.
- `LAYERLEAN/README.md`, `LAYERLEAN/LayerLemma.lean` (SHA-256 `afb8542d…`), `LAYERLEAN/logs/`. Lean names were taken
  from the file itself (declaration list checked with grep) and from the axiom log.
- `SIX60/README.md`, `SIX60/sets/` (five 60-point sets, hashes verified), `SIX60/construction/REALIZE_README.md` (set D).
- `PRIMEFOLD/README.md` §3, §9; `PRIMEFOLD/sets/k8/`, `PRIMEFOLD/check64/check64.log`.
- `ES8SYM/README.md` §§2, 3, 6 (verification pipeline, structure of the 7-fold sets, threefold).
- `K8EXACT20261106/README.md` (exact Z[ζ7] clause check, 0 violations, 16 configurations, both encoders).
- `C6C7REVIEW/REPLAY.md` (4 November hash-bound replay: A c11111, c11000, c11110; B c11001, c11000, c11111; both
  sevenfold proofs; binary hashes).
- `C6UPPER/replay-2026-11-06/` (`README.md`, `results.tsv`, `replay.log`, `TOOLS_AND_PROOFS.sha256`): the hash-bound
  cake_lpr replay of 6 November, which fills the former `\replaystatus` placeholder.
- `LRATCHECK20261105/README.md`, `LRATCHECK20261105/recheck/README.md` (lrat-check defect; calibration re-certified).
- `ROT45CHORD20261105/README.md`, `ROT456` §3–4, `ROTREFINE20261104/README.md` and `m5_REPORT.md`, `THREEFOLDRELAX/README.md`
  (open cases, evidence only); `SYMLEAN/README.md` and `SymmetricReduction.lean` (`Threefold33`), `C3FINAL/README.md`.
- `SYMLEAN/README.md` §4 and `SYMLEAN/AffineReduction.lean` (statement of `hasConvexNGon_of_affine_symmetry`, for
  Remark 1.3).
- `NOVELTY20261106/README.md` (safe wording, credit, what not to claim), `LIT/references.bib`, `LIT/RELATED.md`.

### Changes made to the soundness section

`k8_soundness_p1.tex` is the source plus a 14-line header comment, four cross-reference edits, two footnotes and one
deleted clause (`diff WRITEUP/note/k8_soundness.tex WRITEUP/P1/k8_soundness_p1.tex` shows them):
1. "described in the section on rotational upper bounds for k = 8 (draft STATUS20261104/k8_section.tex)" →
   "described in Section~\ref{sec:cert}";
2. "As in the rest of the note," → "As in Section~\ref{sec:defs},";
3. "is stated in the companion section" → "is stated in Section~\ref{sec:cert}";
4. trust-table row "certificate (companion section)" → "certificate (Section~\ref{sec:cert})";
5. a footnote after "Lean was not rerun for this section": "Note added in this paper: for this paper the file was
   checked again with `lake env lean` on 6 November 2026; see Section~\ref{sec:layer}, ``Build and axioms''.";
6. a footnote after "fresh runs reproduce the formula files byte for byte": "Note added in this paper: for the 64
   sixfold cube files this is on record by hash for all of them since the hash-bound replay of 6 November 2026, and
   structurally for all; see Section~\ref{sec:enc}, ``Validation''. (Until the replay it read "by hash for the 6
   sampled ones and structurally for all"; the header comment records the change.)"
7. after the replay of 6 November had finished: "and is not repeated here, since it changes as the replay proceeds."
   → "and is not repeated here." (the status no longer changes; Section 6.2 gives the finished replay).
Mathematical text, rigor tags and gaps (G1)–(G4) are unchanged; the source still hashes to `197bc214…`. If the source
changes, re-create the copy and re-apply these seven edits.

## Checks run for this draft (6 November 2026, KST; all on copies or read-only, under the caps)

- **Lean.** `lake env lean` on a scratch copy of `LAYERLEAN/LayerLemma.lean` with 19 `#print axioms` lines appended,
  from the repository root with the dependencies already built (no rebuild): exit 0, only `propext`,
  `Classical.choice`, `Quot.sound` for all 19 declarations (including `sixfold_octagon`, `sevenfold_octagon`,
  `chain_clauses_sound`, `strict_nesting`, `centre_not_mem_of_even`), 23 s wall clock, 2.6 GB peak.
- **Lower bounds.** `PRIMEFOLD/check64/run_all.sh` on copies of `check64/` and `sets/k8/` (35 s), and
  `SIX60/verify/verify60.py` plus `SIX60/verify/dfs_convex.c` on all five sixfold sets (2.6–3.5 s each for
  `dfs_convex`): every hash, every collinearity count (0) and every convex-subset count in Tables 5 and 6 of the paper
  reproduced; largest convex subset 7 for all thirteen files (twelve order types).
- **Hashes and structure.** `tools/make_tables.py` (revised version): all thirteen point-set files, encoder and tool
  sources and the Lean file hash to the recorded values; in every file the non-centre rows are distinct and are exactly
  the cyclic shifts of the printed seeds (layer blocks in ten files; the three cluster files list rows cluster by
  cluster); the sevenfold files have exactly one zero row (the centre); the replayed cube CNF and proof hashes in
  `C6C7REVIEW/replay.json` equal the recorded ones; the computed cube orders equal those of `C6UPPER/README.md`. The
  cube table and hash appendix it now writes are byte-identical to the earlier ones; the seed lists gained the three
  cluster files and the coefficient sizes.
- Scratch outputs (not kept): `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/rerun/`
  and `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/ed6c9cac-8b42-4af7-a7d1-a8fb17116ce4/scratchpad/leancheck/`.

For the revision: `make_tables.py` re-run (PASS), and three pdflatex passes under the caps (each exit 0; 30 pages; no
warnings; 1 overfull, 2 underfull boxes). No SAT solver or proof checker was run for this draft, and no file outside
`WRITEUP/P1/` was changed.

For the replay update (6 November 2026, after 07:43 KST): the replay figures in `p1.tex` were taken from
`C6UPPER/replay-2026-11-06` (`results.tsv`, `replay.log`, `TOOLS_AND_PROOFS.sha256`). Its CNF and `.zst` hash columns
were compared again with `C6UPPER/SHA256SUMS.txt` and `TOOLS_AND_PROOFS.sha256` (all equal). `make_tables.py` was re-run
(PASS; `tables/` byte-identical). Three pdflatex passes followed (each exit 0; 30 pages; no errors, undefined references
or warnings; the same 1 overfull and 2 underfull boxes). No SAT solver or proof checker was run for this update. The
same step also updated records outside `WRITEUP/P1/`: `C6UPPER`, `SIX60`, `ES8SYM`, the status, roadmap and novelty
pages, `C6C7REVIEW`, `STATUS20261104/k8_section.tex` and `WRITEUP/note/symmetric_extremal.tex`.

After a review of that update (same day):
- Proof size corrected to about 28.4 GB of `.lrat.zst` (sum of the 64 file sizes); the earlier 31 GB was `du -sh` of
  the whole replay directory, which also holds the regenerated CNFs.
- Appendix A now says that the sixfold certificates are the replay proofs and lists the 24 new phase-order proof
  prefixes; a script compared every prefix in the compiled PDF with `results.tsv` (12 cubes x 2 encoders, all equal).
- "so 6 of the 64 ... are bound" now reads "before the replay below, ... were bound"; the §2 bullet names 2.1.3 for
  the re-checks of 5 November too; the abstract says that cake_lpr accepted every fresh proof; §9 notes the two
  meanings of `CAKE` and the `CAMP_CAP` block; edit 7 of the soundness copy.
- The cake_lpr binary of the replay was rebuilt from commit `033aad53` in a scratch directory (`make`, `cc -O2`): same
  SHA-256 `c14ff498…`. cake_lpr was not run.
- `make_tables.py` re-run (PASS; `tables/` byte-identical). Three pdflatex passes (each exit 0; 30 pages; no errors,
  undefined references or warnings; the same 1 overfull and 2 underfull boxes).

For the 311 update (6 November 2026, about 10:30 KST): one clause of §1 changed (open item 14). Three pdflatex passes
followed, under `systemd-run --user --scope -p MemoryMax=4G -p MemorySwapMax=0 nice -n 10`: each exit 0, 30 pages, no
errors, undefined references or warnings, and the same 1 overfull and 2 underfull boxes. `make_tables.py` was not
re-run, since no table input changed.

## Revision after review (6 November 2026)

An internal review listed 20 findings. Each was checked against the records before acting; all 20 were confirmed and
acted on, two of them (public artifact, venue length) only by recording them as open items 12 and 13.

| # | finding | verified against | change |
|---|---|---|---|
| 1 | §10 misquoted ROT456 §3 on the 12-layer fivefold model | ROT456 §3 ("still SAT after 44 rounds"), ROTREFINE20261104/m5_REPORT.md | §10 now: 14-layer fourfold GP-consistent model unrealized (ROT456 §3); 12-layer fivefold GP-consistent model excluded for the prescribed rotation by an exact identity over Q(√5) (written proof, not refereed; ROTREFINE); the 12-layer formula stayed SAT, the refined 13-layer one gave no answer in 600 s |
| 2 | threefold relaxation called "not implemented" | THREEFOLDRELAX/README.md | §10 now reports `gen_relax.py --nonest`, its validation, that it is too weak (SAT at K = 7 for 10–13 orbits; the maximum is 10 orbits by `Threefold33`/C3FINAL), and (3,8,22): 170,270 vars, 7,400,332 clauses, no answer in 800 s |
| 3 | Lemma 3.1 and "Method" overclaimed Lean | k8_soundness Lemma 5.2 and trust table; LayerLemma.lean declaration list | Lemma 3.1 labelled "Lean-checked core (names); assembly a written proof"; §3 title "(Lean-checked core)"; new sentence on the assembly and (G4); "What is not in Lean" lists it; Method and abstract say the Lean reduction is to 66-/70-point centre-free sets (`Sixfold66`, `Sevenfold70`) and that the nested-polygon form is Lemma 5.2; Table 7 split into two rows |
| 4 | "certificate" headings without the m = 6 qualification | C6UPPER/logs/cake.txt, encb_cake.txt (labels only) | qualification now in Theorem 1.1's rigor note, Theorem 6.1's heading and Table 7; §2's certificate bullet says such cases are flagged |
| 5 | "every certified formula byte for byte" | replay.json (6 cube `cnf_sha256`, all matching C6UPPER/SHA256SUMS.txt), regen.log, REPLAY.md, verify_cover logs | §4 "Regeneration" bullet, §6 "Checkers" and Table 7 state exactly what is on record; footnote in the soundness copy (edit 6) |
| 6 | Remark 1.3 overstated the Lean statement | SYMLEAN/AffineReduction.lean l. 1330 (hE over all non-identity isometries) | remark now says the conjugation step is Lean-checked only in that order-forgetting form; no order-preserving version is formalized |
| 7 | Table 1 caption, row ≥ 8, missing m = 2 | LIT/RELATED.md, NOVELTY20261106, symmetric_extremal.tex | m = 2 row added (2t; 64; 33 orbits; layer lemma fails; open); row ≥ 8 sizes "mt, mt+1" (odd m only, in caption); caption says the best *refereed* bound comes from 408; §1 cites Schroeder's 319 and the project's 311 (unrefereed); abstract adds the half-turn |
| 8 | Corollary 1.2 skipped the power step; abstract omitted {O} | — | one-line power argument added; proof labelled "written proof (not refereed; new)"; abstract says "(or consist of the centre alone)" |
| 9 | `c7_64_own_s1000` missing from the line-module paragraph | PRIMEFOLD/check64/check64.log | added (no module of size 2–20; larger not checked); the cluster sets are now said to have line-modules including seven of size 9 |
| 10 | no public artifact; length | — | open items 12 and 13; Supp entry carries a bracketed deposit placeholder; §2 and §8 say no public deposit exists yet |
| 11 | "coordinates up to 10^30" wrong; three files unchecked | file contents (14, 13, 31 digits), PRIMEFOLD/SHA256SUMS | seeds of all 13 files printed with digit counts; `make_tables.py` checks all eight sevenfold hashes and the orbit structure of every file |
| 12 | Baek's N undefined | symmetric_extremal.tex Thm. (Baek) | stated in forcing form with "4-cap" defined |
| 13 | "0.4 s each"; column label | cubes.txt, encb_cubes.txt, cadical summaries | "under 1 s each"; column "wall (s)"; caption says these are lane wall times, 3–10 s above CaDiCaL's process time |
| 14 | "twelve point sets/files" | Theorem 7.1 | "twelve order types in thirteen files" (Table 7, README) |
| 15 | stale "Lean was not rerun" | — | footnote in the soundness copy (edit 5) |
| 16 | credits | LIT/RELATED.md, C6C7REVIEW/LITERATURE.md, LIT/references.bib | Makai–Turán credited for ES(5) = 9; SMQH "§6.1, App. C"; KPH26 venue CICM 2026 (proceedings data unchecked) |
| 17 | addunits command incomplete | C7UPPER/repro.sh l. 13 | full command in §9 |
| 18 | `make_tables.py` hard-coded values | REPLAY.md, replay.json, cubes logs, git blob | daggers from replay.json `sampling`, times from the raw logs, orders computed, scales from file headers, Lean hash checked against the recorded prefix and the commit blob; output for the cube table and hash appendix unchanged byte for byte |
| 19 | "known" wording; "written by an independent check" | — | "known to us", "in our records"; "written for an independent check" |
| 20 | overfull boxes; log removed | p1.log | Theorem 7.1(a) and Table 6 overfulls removed (also a new 7.8 pt one in Table 1 that the m = 2 row caused); `p1.log` kept |

## Open items before circulation

1. **Replay placeholder: done (6 November 2026).** The hash-bound cake_lpr replay (6 Nov 2026) finished at 07:41:26
   KST; cake_lpr accepted the fresh proofs of all 64 cube formulas (`C6UPPER/replay-2026-11-06/README.md`). It also recorded matching hashes
   for all 64 regenerated cube CNFs, so both parts of this item applied:
   - The macro `\replaystatus` was removed. Its five places were rewritten: the abstract, the rigor note of
     Theorem 1.1, the heading of Theorem 6.1 (and its proof, which now cites the replay), §6.2 "What has been
     replayed" (a new paragraph on the replay), and the sixfold row of Table 7.
   - The surrounding qualifications were rewritten too:
     - the abstract sentence;
     - the caption of Table 4: its hashes and times are those of the 3 November proofs, and the 24 fresh phase-order
       proofs differ from them;
     - the certificate bullet of §2: CaDiCaL 2.1.3 for the re-checks of 5 November and the replay of 6 November, and
       the upper bounds no longer depend on label-only verdicts;
     - the "weakest links" sentence of "What is and is not claimed" in §1, which now says that every cake_lpr verdict
       the upper bounds use is bound to formula and proof hashes;
     - the "Regeneration" bullet of §4;
     - the "Checkers" paragraph of §6, which gains the replay's tool hashes `4acf5860…` and `c14ff498…`;
     - the Table 7 row "Certified files are the output of the analysed programs";
     - "Further limitations" (1) in §8;
     - §9: replay commands, and the replay ran on the same workstation;
     - the hash appendix intro;
     - the `Supp` entry, which adds the local proof directory `c6upper-replay-20261106`;
     - footnote 6 of the soundness copy (edit 6 above), with its header comment.
   - New label `sec:c6` on §6.2.
   - The replayed proofs of the 24 phase-order cubes are new files (CaDiCaL 2.1.3); `tables/cubes6.tex` still lists the
     3 November proofs. The first twelve digits of the 24 fresh proof hashes are in Appendix A (typed into `p1.tex`
     from `results.tsv`, not generated by `make_tables.py`); the full hashes are in `results.tsv` and the replay
     README.
   - The replay used a cake_lpr binary (`c14ff498…`) different from that of the 4 November review (`2fee767a…`); the
     "Checkers" paragraph of §6 says so and that a build of commit `033aad53` of the public cake_lpr repository
     reproduces it byte for byte (replay README, "Provenance of the cake_lpr binary").
   - The soundness copy no longer says that the replay status "changes as the replay proceeds" (edit 7 above).
2. **Author and acknowledgements.** `[author]` on the title page; the acknowledgement paragraph is a placeholder that
   also asks for a statement on computational and AI assistance.
3. **Commit to cite.** The `Supp` entry names branch `es7-night-2026-11-01` and says the draft was written at
   597961bbd; fix the commit to cite once P1 is committed.
4. **Bibliographic data from memory.** The entries for CaDiCaL 2.0 (CAV 2024), cake_lpr (Tan–Heule–Myreen, STTT 2023
   and TACAS 2021), LRAT (Cruz-Filipe et al., CADE 2017), Lean 4 (de Moura–Ullrich, CADE 2021) and Mathlib (CPP 2020)
   are not in `LIT/references.bib` and were entered from memory: check volumes and pages. The other entries follow
   `LIT/references.bib` and the notes' bibliographies (Dumitru given as "B. Dumitru", as `NOVELTY20261106` asks).
5. **Unreviewed new text.** Remark 1.3 (affine symmetries) and the proof of Corollary 1.2 (now with the step from a
   rotation of order m to the rotation by 2π/m) are new in this draft and have had no internal review; both are labelled
   so in the paper and in Table 7. The revision text of the review round (below) restates records and has had no
   second review.
6. **Seven-fold verification count.** The paper says every sevenfold convex-subset count rests on at least two
   separately written programs, and on four or more for the five files also in `ES8SYM/sets`. `c7_64_own_s1000` has
   only the two `check64` programs on record (`m7_x2_G9s_centre` has a third DP in
   `PRIMEFOLD/cluster/thmA/cert_m7_x2_G9s_centre.log`). Running the `ES8SYM` pipeline on it would make "three programs"
   uniform for both symmetry types.
7. **Inconsistencies found in the sources** (the paper uses the values computed from the raw records):
   - `C6UPPER/README.md` gives 41.0 GB for encoder A's proofs (all 32 cubes) but 45.7 GB for encoder B's (the 12
     phase-order cubes only). From the byte counts in `C6UPPER/SHA256SUMS.txt`: A 40.8 GB (12) / 41.0 GB (32), B 45.7 GB
     (12) / 46.5 GB (32). The paper gives both.
   - `C6UPPER/README.md` says CaDiCaL peak RSS 1.3–1.7 GB for encoder A; `logs/cadical_summary.txt` has up to 2,046 MB
     (cube c10000). The paper says 1.3–2.0 GB.
   - The hardware of the original solver runs is not uniformly recorded (the sevenfold cake_lpr logs are macOS `time`
     output); §9 says so.
8. **Gaps of the proof itself** (unchanged from the reviewed section): (G1) code-to-clause correspondence by reading
   the source; (G2) no formalized step from DIMACS to `Sixfold66`/`Sevenfold70`; (G3) encoder A's binary64
   classification (covered twice at the certified instances); (G4) parts marked "new here" or "not in the review" are
   unreviewed. The proof archives (`es8-c6-octagon-2026-11-03`, `es8-c7-octagon-2026-11-03`,
   `es8-c6c7-review-2026-11-04`) and the replay proofs of 6 November (`c6upper-replay-20261106`, about 28.4 GB of
   `.lrat.zst`) are not public. The replay of 6 November closes no gap among (G1)–(G4); it closes the separate gap that only 6 of the 64
   sixfold verdicts were hash-bound.
9. **Literature.** The novelty paragraph is evidence only. Not accessed: the SMQH CICM chapter text, Baek–Balko's
   JCTA version, Erdős–Tuza–Valtr 1996, paywalled databases. Repeat the search before submission.
10. **Cosmetic.** One 13.3 pt overfull line in the head of Lemma 5.2 (long Lean names in the reviewed source; left as
    is so that the copy differs from the source only by the documented edits).
11. **Sync.** If `WRITEUP/note/k8_soundness.tex`, `C6UPPER`, `SIX60` or `PRIMEFOLD` change, rerun
    `tools/make_tables.py`, re-create `k8_soundness_p1.tex` and recompile.
12. **Public artifact (gap, not closed).** The supplementary material has no public archived deposit or DOI, and the
    proof archives (about 90 GB, plus about 28.4 GB of replay proofs from 6 November) are private, so a referee cannot inspect the artifacts. Deposit (for example on
    Zenodo) the generators, the cube files or their generator commands, the logs, the proof hashes and replay logs and,
    where size permits, the sevenfold and sixfold LRAT proofs, and cite it by DOI in the `Supp` entry (which now carries
    a bracketed placeholder for this). Publishing is the author's decision.
13. **Length and internal paths (not changed).** At 30 pages, with a 15-page soundness section, the draft far exceeds a
    CICM (LNCS) page limit or a EuroCG abstract. For a venue version, move Section 5 and the internal directory names
    (C6UPPER, K8EXACT20261106, ...) to an appendix or an arXiv long version and cut the body to the limit. No venue was
    fixed for this draft, so the structure requested for P1 was kept.
14. **The ES(8) ≤ 311 mention.** §1 now cites Schroeder's unrefereed 319 and the project's own unrefereed 311 (wording
    from `NOVELTY20261106` "Safe wording"). If the author prefers not to mention 311 before its own write-up, delete that
    clause; Table 1's caption only points to §1.
    *6 November 2026, about 10:30 KST:* "checked by the Lean kernel in a single run" now reads "in two complete runs
    (the second a reproduction with a compact certificate checker)". The reason is the completed compact recheck
    (`experiments/omission-compact-checker-2026-11-05/README.md`, section "6 November 2026: the compact recheck is
    complete"). This is the only change; the paper's scope is unchanged.
15. **Line-modules of `c7_64_own_s1000`.** Only sizes 2–20 were checked (`check64.log`); the paper says so. Running
    `PRIMEFOLD/check64/modules60` on it would bring it in line with the other annealed sets.

