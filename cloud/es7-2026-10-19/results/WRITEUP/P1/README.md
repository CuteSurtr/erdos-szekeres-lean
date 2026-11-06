# P1: sixfold and sevenfold rotationally symmetric point sets without a convex octagon

First full draft of preprint P1, written 6 November 2026 (KST) and revised the same day after an internal review (see
"Revision after review") and again after an audit of its bibliography, numbers and claims (see "Revision after the
audit") and a checker's fix round (see "Fix round after the checker"), and once more after encoder B's sixfold base
formula was certified unsatisfiable on its own (see "Revision for the encoder-B base formula" and the checker's round
after it). Not refereed, not circulated.

**Theorem of the paper.** For k = 8, the largest m-fold rotationally symmetric set in general position with no 8
points in convex position has exactly 60 points for m = 6 and exactly 64 for m = 7. Since 6-fold sets in general
position have 6t points and 7-fold ones 7t or 7t + 1, this is the 6- and 7-fold case of ES(8) = 65 together with
attainment of the largest sizes it permits (the paper says so explicitly, following `NOVELTY20261106` "Do not claim").

**Rigor, as stated in the paper.** Upper bounds: certificates (cake_lpr `s VERIFIED UNSAT` only), two separately
implemented encoders, on top of a Lean-checked reduction (`LAYERLEAN`) and a written soundness proof (not refereed) with
gaps (G1)–(G4). Sixfold: in the hash-bound cake_lpr replay (6 Nov 2026) all 64 cube formulas, regenerated with
hashes matching the record, were solved again, and cake_lpr accepted every fresh proof (64 of 64,
`C6UPPER/replay-2026-11-06`). Before it, the 64 verdicts of 3 November were on record by cube label only, and 6 of the
64 were hash-bound (4 November). Encoder B's sixfold base formula `B_m6K8t11.cnf` (`479e31a9…`) is certified
unsatisfiable on its own by 64 hash-bound cake_lpr verdicts on the 2^6 sign patterns of Y(1,2), …, Y(3,4): the 32
encoder-B cubes of that replay and 32 cubes with ¬Y(1,2), 32 of 32 accepted on 6 Nov 2026
(`C6UPPER/noty12-2026-11-06`). So the sixfold bound via encoder B no longer uses the reflection lemma
(k8s:lem:refl) or the τ case of k8s:lem:affine; encoder A, the cross-check, still does. The layer lemma is Lean-checked in its core; the assembly
of the layers is a written proof (G4). Lower bounds: exact computation. No priority claim; "we did not find prior
work" only.

## Files

| file | content |
|---|---|
| `p1.tex` | the paper (33 pages since the revision for the encoder-B base formula; 31 before). Inline bibliography, no BibTeX. |
| `p1.pdf` | compiled with pdflatex (TeX Live 2025), three passes, each exit 0: **0 errors, 0 undefined references or citations, no LaTeX warnings**; 1 overfull box (13.3 pt, the head of Lemma 5.2, from the reviewed source) and 2 underfull boxes (badness 1270 and 1953). Rebuilt on 6 November 2026 after the replay status was filled in, with the same result (30 pages). Rebuilt again on 6 November 2026 (about 10:30 KST) after the one-clause 311 update in §1 (open item 14), with the same result. Rebuilt again on 6 November 2026 (about 13:30 KST) after the proof of Corollary k8s:cor:geom was corrected (it had cited Lemma k8s:lem:affine for the translation of the centre to O, although that lemma's admissibility clause assumes g(O) = O; the translation step is now argued directly, and part (b) no longer says "the same" for a step that has no cube split): 31 pages, 0 errors, 0 undefined references, 1 overfull box. **Build after the audit: 6 November 2026, about 13:40 KST, after the audit edits ("Revision after the audit"): three passes, each exit 0; 31 pages; 0 errors, 0 undefined references or citations, 0 LaTeX warnings; the same single overfull box (13.3 pt, head of Lemma 5.2); 5 underfull boxes (the 2 earlier ones, plus 3 in the bibliography: ETV96 badness 2418, Sche20 1281, the `Supp` entry 5260).** Rebuilt once more on 6 November 2026 (about 13:55 KST) after the checker's fix round (§1.1 citation placement, §9 C7UPPER paragraph), under `systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0 nice -n 5`: the same result (three passes, each exit 0; 31 pages; 0 errors, 0 undefined references or citations, 0 LaTeX warnings; 1 overfull, 5 underfull boxes). **Build after the revision for the encoder-B base formula: 6 November 2026, about 16:35 KST, under the same `systemd-run` caps: three passes, each exit 0; 33 pages; 0 errors, 0 undefined references or citations, 0 LaTeX warnings; the same overfull box (13.3 pt, head of Lemma 5.2) and 5 underfull boxes (the `Supp` entry now has badness 1158 instead of 5260).** **Build after the checker's round on that revision: 6 November 2026, about 16:47 KST, under the same caps: three passes, each exit 0; 33 pages; 0 errors, 0 undefined references or citations, 0 LaTeX warnings; the same overfull box and the same 5 underfull boxes (badness 1270, 1953, 2418, 1281, 1158).** |
| `p1.log` | the log of the third pass, kept for reviewers. |
| `k8_soundness_p1.tex` | Section 5 of the paper: an adapted copy of `WRITEUP/note/k8_soundness.tex` (see below). |
| `tables/*.tex` | data fragments \input by `p1.tex` (sixfold cube table, hash appendix, seeds of the point sets). Generated; do not edit. |
| `tools/make_tables.py` | generates `tables/` from the repository records and checks them (standard library only; calls `git show` once, read-only). |
| `rerun-20261106/` | the re-run of the lower-bound checkers of 6 November 2026 (§7 "Re-run for this draft"): scripts, copies of the inputs, logs, timings; see its `README.txt`. |
| `reviews/corollary-geom-review-20261106.md` | the in-session check of a draft of the corrected proof of Corollary k8s:cor:geom (open item 5). |

Build: `pdflatex p1 && pdflatex p1 && pdflatex p1` in this directory (run under the session's caps with
`systemd-run --user --scope -p MemoryMax=12G nice -n 5`; the rebuild after the replay used `-p MemoryMax=4G -p
MemorySwapMax=0` and `nice -n 10`, and the rebuild after the audit used `systemd-run --user --scope -q -p MemoryMax=4G
-p MemorySwapMax=0 nice -n 5 pdflatex -interaction=nonstopmode -halt-on-error p1`); then delete `p1.aux`, `p1.toc`,
`p1.out` and keep `p1.log`.
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
   credit (Erdős–Szekeres, Szekeres–Peters, Marić, Scheucher, Heule–Scheucher, Subercaseaux et al. ITP 2024, SMQH CICM 2025 which
   stops at k = 7, Mackey, Baek, Baek–Balko, Dumitru with priority for fivefold k = 7, Georgiev et al.), "what we did
   not find".
2. Definitions, Lean conventions, rigor labels.
3. The layer reduction (Lean-checked core): layer lemma (core Lean-checked, assembly written), encoding facts (a)–(e),
   `Sixfold66`/`Sevenfold70` verbatim,
   Proposition 3.3 (`sixfold_octagon`, `sevenfold_octagon`), build/axioms, what is not in Lean.
4. The encodings: variables, four clause families, encoders A and B, symmetry breaking (only encoder A uses a unit),
   instance sizes, validation (including the 32 cube files with ¬Y(1,2)).
5. Soundness (the adapted reviewed section; rigor tags of the statements and gaps G1–G3 unchanged; since the revision
   for the encoder-B base formula: Theorem 5.24(a′) "F_B is satisfiable" without Lemma refl, Corollary 5.28(a) from
   "F_B(6,8,11) unsatisfiable", the 64-cube split in §5.9, and the trust table and G4 marking Lemma refl and the τ case
   of Lemma affine as used only by encoder A).
6. The certificates: checkers and the lrat-check defect; sevenfold table; sixfold split (and encoder B's 64-cube split),
   12-cube table (both encoders, times, sizes, proof-hash prefixes of the 3 November proofs, the 4 November replays
   marked), runs, what has been replayed (including the hash-bound cake_lpr replay of 6 November, 64 of 64), the cubes
   with ¬Y(1,2) (32 of 32, 6 November); Theorem 6.1 (sixfold via F_B unsatisfiable, encoder A as cross-check).
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
- `WRITEUP/note/k8_soundness.tex` (SHA-256 `50bcd17a2614c3ba…`, the revision of 6 November 2026 for
  `C6UPPER/noty12-2026-11-06` with the checker's round on it, not committed; `0fe99cfe46b99406…` before that round;
  before the revision `248bf0375e6acab1…` at commit b583d89ab, which changed the proof of Corollary k8s:cor:geom in
  both files; the copy was first made from `197bc214…` at 597961bbd): Section 5.
- `WRITEUP/note/symmetric_extremal.tex`: context, Table 1, literature and bibliography entries.
- `C6UPPER/README.md`, `C6UPPER/SHA256SUMS.txt`, `C6UPPER/logs/{cadical_summary,encb_cadical_summary,cake,encb_cake,regen,replay_2026-11-04}.txt|log`.
- `C7UPPER/README.md`, `C7UPPER/SHA256SUMS.txt`, `C7UPPER/logs/cake_{A,B}.out`, `C7UPPER/repro.sh`,
  `C7UPPER/logs/repro_validation{,_20261106,_20261106b}.log`.
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
- `C6UPPER/noty12-2026-11-06/` (`README.md`, `results.tsv`, `run.log`, `SUMMARY.txt`, `cubes.sha256`,
  `TOOLS_AND_PROOFS.sha256`, `verify_cover64.log`, `verify_final64.log` = PASS): encoder B's 32 cubes with ¬Y(1,2),
  32 of 32 accepted (finished 15:40:35 KST), which with the replay's 32 encoder-B cubes certify `B_m6K8t11.cnf` alone.
- `LRATCHECK20261105/README.md`, `LRATCHECK20261105/recheck/README.md` (lrat-check defect; calibration re-certified).
- `ROT45CHORD20261105/README.md`, `ROT456` §3–4, `ROTREFINE20261104/README.md` and `m5_REPORT.md`, `THREEFOLDRELAX/README.md`
  (open cases, evidence only); `SYMLEAN/README.md` and `SymmetricReduction.lean` (`Threefold33`), `C3FINAL/README.md`, `C3SPOT/README.md`.
- `SYMLEAN/README.md` §4 and `SYMLEAN/AffineReduction.lean` (statement of `hasConvexNGon_of_affine_symmetry`, for
  Remark 1.3).
- `NOVELTY20261106/README.md` (safe wording, credit, what not to claim), `LIT/references.bib`, `LIT/RELATED.md`.

### Changes made to the soundness section

`k8_soundness_p1.tex` is the source plus a 28-line header comment (21 lines before the revision for the encoder-B
base formula), four cross-reference edits, two footnotes, one
deleted clause and two provenance edits (`diff WRITEUP/note/k8_soundness.tex WRITEUP/P1/k8_soundness_p1.tex` shows
them):
1. "described in the section on rotational upper bounds for k = 8 (draft STATUS20261104/k8_section.tex)" →
   "described in Section~\ref{sec:cert}";
2. "As in the rest of the note," → "As in Section~\ref{sec:defs},";
3. "is stated in the companion section" → "is stated in Section~\ref{sec:cert}";
4. trust-table row "certificate (companion section)" → "certificate (Section~\ref{sec:cert})";
5. a footnote after "Lean was not rerun for this section": "Note added in this paper: for this paper the file was
   checked again with `lake env lean` on 6 November 2026; see Section~\ref{sec:layer}, ``Build and axioms''.";
6. a footnote after "fresh runs reproduce the formula files byte for byte": "Note added in this paper: for the 64
   sixfold cube files of the hash-bound replay of 6 November 2026 this is on record by hash for all of them, and
   structurally for all; the 32 cube files of encoder~B with $\neg Y(1,2)$, written on 6 November, are the regenerated
   base formula plus six units, checked byte for byte; see Section~\ref{sec:enc}, ``Validation''." (Until the replay it
   read "by hash for the 6 sampled ones and structurally for all"; from the replay until the revision for the
   encoder-B base formula it read "for the 64 sixfold cube files this is on record by hash for all of them since the
   hash-bound replay of 6 November 2026, and structurally for all; see …". The header comment records both changes.)
7. after the replay of 6 November had finished: "and is not repeated here, since it changes as the replay proceeds."
   → "and is not repeated here." (the status no longer changes; Section 6.2 gives the finished replay);
8. (audit of 6 November, numbers F11) the first citation of the checks script in the text, `\dirn{k8_soundness_checks.py}`
   in the paragraph on triple sizes, → `\dirn{WRITEUP/note/k8_soundness_checks.py}`, and in the source's own header
   comment "in this directory." → "in WRITEUP/note/." (the script and its log exist only there); the later citations
   stay short;
9. (audit of 6 November, numbers F9 / claims 5) in the rigor-label paragraph, "for every cited theorem of that file)" →
   "for every cited theorem of that file except the one-line \lean{hullVerts_subset}, which is used in
   \lean{layers_are_orbits} and \lean{exists_layer} and so is covered by their checks)".
The rigor tags of the statements and gaps (G1)–(G3) are unchanged; (G4) gained two sentences in the revision for the
encoder-B base formula (in source and copy alike). The source hashes to
`50bcd17a2614c3ba28530d2ce9ae7b35eb5149e651b2641cc4020be85897093d` (since the checker's round on the revision of
6 November 2026; from that revision until the round `0fe99cfe…`; before: `248bf037…` since b583d89ab, which changed
the proof of Corollary k8s:cor:geom in both files, and `197bc214…` before that); apart from the header comment and edits 1–9 the copy equals it (checked with `diff`). If the source changes,
re-create the copy and re-apply these nine edits.

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
  the cyclic shifts of the printed seeds (layer blocks in ten files; p7_compound_64, p7_two_orbit_64 and m7_x2_G9s_centre list
  rows cluster by cluster; rule_p7_64pts is built from clusters but stored by orbits); the sevenfold files have exactly one zero row (the centre); the replayed cube CNF and proof hashes in
  `C6C7REVIEW/replay.json` equal the recorded ones; the computed cube orders equal those of `C6UPPER/README.md`. The
  cube table and hash appendix it now writes are byte-identical to the earlier ones; the seed lists gained those three
  files and the coefficient sizes.
- Outputs: `LAYERLEAN/logs/axioms_recheck_20261106/` and `WRITEUP/P1/rerun-20261106/` (copied from the session
  scratch directory on 6 November 2026; each has a `README.txt` saying where and when it ran and how to rerun it).

For the revision: `make_tables.py` re-run (PASS), and three pdflatex passes under the caps (each exit 0; 30 pages; no
warnings; 1 overfull, 2 underfull boxes). No SAT solver or proof checker was run for that revision, and no file outside
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

## Revision after the audit (6 November 2026, about 13:30–13:45 KST)

Three audits of the draft (bibliography, numbers, claims) were each re-checked by a skeptic, who confirmed, refuted or
narrowed every finding against the records and the web. Every confirmed finding was acted on as listed below; refuted
findings were not (bibliography 3 and 8, claims 7 for the cake_lpr build, claims 10a). Paths are under
`cloud/es7-2026-10-19/results`.

| finding | change |
|---|---|
| bib F1 | KKS70 title "A combinatorial problem on convex n-gons" (zbMATH 0223.52009), also in `WRITEUP/note/symmetric_extremal.tex` |
| bib F2, numbers F2, claims 2 | `Supp`: "the records cited are those at commit b583d89ab or later; the commit to cite is to be fixed before circulation" (open item 3) |
| bib F4 | §1.1: Lemma 14 of BB25 has its proof omitted in the conference version (journal version not read); the note also has a construction without Lemma 14, checked by exact computation |
| bib F5, F6, F7 | SMQH25: LNCS 16136 (LNAI), published October 2025; HS24: pages 61–80; KPH26: "to appear in CICM 2026" (arXiv comment; no proceedings record on 6 November 2026) |
| bib M1–M6 | new entries ETV96 (cited for the Erdős–Tuza–Valtr refinement, "not read"), Sche20, Sche23, SMHM24; §1: ES(6) credits (Marić, Scheucher, faster SAT proofs, SNGCCH24 §7 corollary), ES(5) credit (Makai per ES35 p. 464, Makai–Turán per ES61); §1.1: earlier symmetric constructions (MS00, Sche20, SMHM24, as credited in SMQH §1); §10: SMQH §6.2 orbit count for k = 7 |
| extra | GGTW25 cited as arXiv:2511.02864v3; v3 (22 Dec 2025) is current and its §38 is still the Erdős–Szekeres Happy Ending section (2^{k−2} points for k ≤ 8, no symmetry stated), checked on 6 November 2026 |
| numbers F1, F14, claims 2 | `k8_soundness_p1.tex` header: source hash `248bf037…` (b583d89ab); this README's source line and edit list updated |
| numbers F3 | §8 and `Supp`: `es8-c6c7-review-2026-11-04` described as the review archive (regenerated formulas, models, witnesses), not a proof archive; open item 8 likewise |
| numbers F4 | §7: "the scale of each sixfold file and the number of digits … of each sevenfold file" |
| numbers F5, F6, claims 1 | logs kept: `LAYERLEAN/logs/axioms_recheck_20261106/` and `WRITEUP/P1/rerun-20261106/` (each with a `README.txt`), cited in §3 and §7 |
| numbers F7 | §9: "32 hardware threads and about 64 GB of memory (59.5 GiB visible to Linux)"; host also recorded in the two archive READMEs |
| numbers F8 | §1.1: searches of 21 October and 1–2, 3, 4, 6 November with their records (LIT, PRIMEFOLD §8, C6UPPER/README.md, C6C7REVIEW/LITERATURE.md, NOVELTY20261106) |
| numbers F9, claims 5 | §3 and the soundness copy (edit 9): `hullVerts_subset` is not in the axiom log but covered through `layers_are_orbits` and `exists_layer` |
| numbers F10 | §7: `rule_p7_64pts` is built from clusters but stored by orbits |
| numbers F11 | soundness copy (edit 8): `WRITEUP/note/k8_soundness_checks.py` at its first citation; header comment "in WRITEUP/note/" |
| numbers F12, F13 | `C6UPPER/README.md`: 1.3–2.0 GB peak RSS per phase-order cube (2,046 MB for c10000); encoder B: 12 phase-order proofs 45.7 GB, all 32 proofs 46.5 GB |
| claims 3 | `C7UPPER/repro.sh` paths adjusted for a checkout (tools `$S/resolve/bin`, `tests/` prefix with `C7UPPER` on `PYTHONPATH`, ES8SYM/PRIMEFOLD set paths, outputs to `$S/repro`, quoted `S` check, `cd` exits on failure). The first validation run (no `solve`, 2-minute limit, `nice -n 19`, 4 GB cap, fully loaded machine) did **not** pass cleanly: it stopped at the limit during the A/B comparison, and it ran before the quoting fix (`C7UPPER/logs/repro_validation_20261106.log`). So §9 and `C7UPPER/README.md` first carried the caveat: complete run of the adjusted script not on record. A second run of the adjusted script by the independent checker (no `solve`) completed with exit 0, output equal to the original log apart from point-set paths (`C7UPPER/logs/repro_validation_20261106b.log`); §9 and `C7UPPER/README.md` now say so (fix round below) |
| claims 4 | §10: C3FINAL verdicts recorded at solve time on hash-matched formulas, proofs not kept, 2,120 of 116,883 re-solved and accepted again (C3SPOT, added to `Supp`) |
| claims 6 | §1 and `Supp`: `experiments/omission-final311-2026-10-14` and `experiments/omission-compact-checker-2026-11-05` cited for the 311 remark; §2 says such paths are relative to the repository root |
| claims 7 (cover checkers) | §8 "What is trusted": the programs named for each exact computation (cube cover: `verify_cover.py`, `strict_cover.py`; lower bounds: at least two per set) |
| claims 8 | §7: set D is `cand1r_s19.pts`; its pipeline run is in `SIX60/construction/REALIZE_README.md`, "cand1r" |
| claims 9 | §3: the mutant thresholds are "reported in LAYERLEAN/README.md; no log of these runs was kept" |
| claims 10b | §4: "the sixfold 54-point set ES8SYM/sets/c6_54pts_9layers.pts" instead of "the certified …" |
| claims 11 | Table 1 caption: `RefuteC6.part_a` is a version over ℂ with centre 0; its link to §2's conventions is not formalized |
| claims 12 | the in-session check of a draft of the corrected corollary is kept as `reviews/corollary-geom-review-20261106.md`; the paper keeps "no internal review" (open item 5) |
| bib, typed from memory | open item 4 closed (Crossref check of the six entries) |

Builds after the audit: `p1.pdf` as in the file table (31 pages, 0 errors, 0 undefined references or citations, 1
overfull box as before). `WRITEUP/note/k8_soundness_wrapper.tex` and `WRITEUP/note/symmetric_extremal.tex` were
compiled into a scratch directory (three passes each, exit 0; 12 pages each; 0 errors and 0 undefined references; the
one overfull box of `symmetric_extremal`, 36.3 pt at lines 539–561, was there before). The committed
`WRITEUP/note/symmetric_extremal.pdf` was not rebuilt, so it still shows the old KKS70 title. `make_tables.py` was not
re-run, since no table input changed. No proof was produced or checked for this revision; the only solver call was
the 9-layer CaDiCaL satisfiability check (s SATISFIABLE) in the checker's complete `repro.sh` run.

## Fix round after the checker (6 November 2026, about 13:50–14:00 KST)

An independent checker re-examined the audit edits. It passed all of them and raised four further points, each acted
on as listed. No mathematics changed, and nothing new is claimed beyond what the cited records show.

| point | change |
|---|---|
| 1 (C7UPPER caveat out of date) | The checker ran the adjusted `C7UPPER/repro.sh` once to completion (no `solve`, absolute `S`, CaDiCaL 2.1.3, `nice -n 19`, 4 GB cap, 15-minute limit; exit 0, 2:34.64 wall clock, peak RSS 0.63 GB). Its output from "== generate" to "s SATISFIABLE" equals `logs/repro_validation.log` apart from the point-set path prefixes (re-checked here with diff). The run is archived with a header as `C7UPPER/logs/repro_validation_20261106b.log`. The raw part after the 13 header lines has the SHA-256 of the checker's file, `856cee3d…`. §9 of `p1.tex`, `C7UPPER/README.md`, the `repro.sh` header comment and the claims 3 row above now describe both runs. §9 says "with an absolute S", since the script was changed after the run (point 2). The `solve` branch was not re-run |
| 2 (`repro.sh` relative `S`) | `B=$S/resolve/bin` was set before `cd "$S"`, so a relative `S` other than `.` broke the CaDiCaL step and the solve branch. Now `B=$PWD/resolve/bin` is set right after `cd "$S" \|\| exit 1`. Checked with a copy of the script's head: with `S` relative and with `S` absolute, `$B/cadical --version` prints 2.1.3. For an absolute `S` the behaviour is unchanged, as the log header, the script header and `C7UPPER/README.md` say. The full script was not re-run after this change |
| 3 (§1.1 citation placement) | "Balko and Valtr~\cite{BV17} ran a SAT attack on the Erdős–Tuza–Valtr refinement~\cite{ETV96} of the conjecture"; Sche20 and Sche23 added to "the works cited above" |
| 4 (review provenance) | Open item 5, the file table, the claims 12 row and the header of `reviews/corollary-geom-review-20261106.md` now say that the review checked a draft written with τ and A, shortly before b583d89ab. The committed wording took up its remarks afterwards and was not re-checked. The paper is unchanged here: it still says "no internal review" |

Build after the fix round: three passes, each exit 0; 31 pages; 0 errors, 0 undefined references or citations, 0 LaTeX
warnings; 1 overfull box (13.3 pt, head of Lemma 5.2) and 5 underfull boxes, as after the audit. `p1.aux`, `p1.out`
and `p1.toc` were deleted. No proof was produced or checked in this round.

## Revision for the encoder-B base formula (6 November 2026, about 16:20–16:40 KST)

**New certified fact.** `C6UPPER/noty12-2026-11-06` (finished 15:40:35 KST; `verify_final64.log`: PASS): cake_lpr
accepted the proofs of encoder B's 32 cubes "base + ¬Y(1,2) + pattern" (32 of 32, `s VERIFIED UNSAT`, each bound to
the CNF and proof hashes). With the 32 encoder-B cubes "base + Y(1,2) + pattern" of the replay of 6 November, the 64
cubes carry all 2^6 sign patterns of Y(1,2), Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4) (variables 1, 2, 3, 10, 11, 18), so
`B_m6K8t11.cnf` (`479e31a9…`) is unsatisfiable on its own. Numbers used, from `results.tsv` there: 35,411 s of CaDiCaL
time (sum 35,410.6 s; 0.8–3,921.3 s per cube; 2,319.7–3,921.3 s for the 12 phase-order cubes, at most 1.0 s for the
others), 2,471 s of cake_lpr time (sum 2,471.4 s), 56.3 GB of raw proofs (sum of `proof_bytes`), 14.9 GB of
`.lrat.zst` (sum of the 32 file sizes, 14,929,339,154 bytes; the record README's "16 GB as `.lrat.zst`" is the size of
the whole data directory `c6upper-noty12-20261106`, 16,805,199,344 bytes, which also holds the 32 cube CNFs and the
logs, so the paper gives both figures). The record README's "the 12 phase-order cubes take 2,600–3,900 s" does not
match `results.tsv` (2,319.7–3,921.3 s); the paper uses the `results.tsv` values. That record was not changed here.

**Soundness section** (`WRITEUP/note/k8_soundness.tex` and `k8_soundness_p1.tex`, identical text; source hash
`0fe99cfe…` after this revision, `50bcd17a…` after the checker's round below; the bullets give the text after that
round):
- header comment of the note: a 5-line revision note;
- after the proof of Lemma k8s:lem:affine: the case gρg⁻¹ = ρ⁻¹ is needed only for τ (Lemma k8s:lem:refl), i.e. only
  for parts (a) and (b) of Theorem k8s:thm:sound (formulas with the reflection unit); the bounds via encoder B use
  part (a′) and do not need it; elsewhere g is a rotation about O or, in Corollary k8s:cor:geom, a translation (first
  part only);
- end of §k8s:sec:reflection: the reflection unit is used only by encoder A; encoder B's formulas are certified on
  their own, at (7,8,10) directly and at (6,8,11) through 64 cubes;
- Theorem k8s:thm:sound: new part (a′) "F_B is satisfiable, by an argument that does not use Lemma k8s:lem:refl";
  the paragraph after the theorem says that (a′) also follows from (a), that its own proof omits the reflection step,
  and that it was added on 6 November after the certificate; "the one for B is for F_B alone, which the theorem covers
  a fortiori" now reads "…, the case of part (a′)", plus the sixfold certificate shapes (B: F_B alone, 64 cubes; A:
  F_A + Y(1,2), 32 cubes);
- proof of the theorem: (a′) is the old argument of (a) without the reflection step ("Neither Lemma refl nor τ is
  used"); (a) applies Lemma refl and then (a′); (b) takes S as in (a);
- §k8s:sec:cube: the cube-cover paragraph now describes two splits: F_B(6,8,11) with x₁…x₆ = Y(1,2)…Y(3,4)
  (variables 1, 2, 3, 10, 11, 18; 40 of 64 patterns contradict transitivity; checks `verify_cover64.py`,
  `verify_final64.py`; by Lemma k8s:lem:cube this gives "F_B(6,8,11) unsatisfiable"; no variable needs a geometric
  meaning), and the earlier split of base + Y(1,2) for both encoders (text kept, with an italic heading, the added count "20 of the 32 patterns contradict transitivity", and a closing sentence "This is the route of encoder A, the cross-check; for encoder B these 32 cubes are one half of the split above");
- Corollary k8s:cor:geom(a): hypothesis "F_B(6,8,11) is unsatisfiable" (proof: Theorem (a′), no Lemma refl); the
  32-cube hypothesis with Y(1,2) for one encoder kept as the second route, marked "this route uses Lemma refl, through
  Theorem (a), resp. (b); it is the route of encoder A, the cross-check"; (b): "unsatisfiability of F_B
  contradicts Theorem (a′)" instead of "(a), since a model of F_B plus H(1) is a model of F_B", so the sevenfold
  encoder-B route does not use Lemma refl either, and the redundant "and Y(1,2) … H(1)" was dropped from the
  replacement list;
- trust table: "Reflection unit; cube cover" → "Cube cover (64 cubes for F_B(6,8,11), 32 for F_A(6,8,11) plus
  Y(1,2))"; the affine row points to the last row for the τ case; new last row "Used only by encoder A (cross-check),
  not for the bounds via encoder B: the reflection unit (Lemma refl) and the case gρg⁻¹ = ρ⁻¹ of Lemma affine";
  caption says the last two rows are not used for the bounds via encoder B;
- gap (G4): two sentences (part (a′) and the 64-cube split were added after the review; Lemma refl and the τ case of
  Lemma affine are used only by encoder A, and the bounds via encoder B do not depend on them).

**P1-only parts of the copy:** the header comment (new source hash, the revision, 28 lines) and footnote 6 (edit 6
above: it now also covers the 32 cube files with ¬Y(1,2)).

**`p1.tex`:**
- header comment: one more revision line;
- abstract: after the replay sentence, a new sentence: for one of the encoders, its 32 replayed cube formulas and 32
  further ones, certified the same day, cover all 2^6 sign patterns of six phase-order variables, so that encoder's
  sixfold base formula is certified unsatisfiable on its own and its route to the sixfold bound does not use the
  reflection symmetry breaking;
- Theorem 1.1, rigor note: "all 64 cube formulas of the original split (32 per encoder)" were regenerated and
  replayed; F_B(6,8,11) certified by 64 hash-bound verdicts, one for each sign pattern of "the six phase-order
  variables Y(1,2), …, Y(3,4) (Section 4)" (32 from the replay, 32 for ¬Y(1,2), 32 of 32 accepted); the bound via
  encoder B does not use "the reflection lemma (Lemma k8s:lem:refl)";
- §3 "What is not in Lean": "the reflection unit (used only by encoder A, the cross-check)";
- §4 "Symmetry breaking": only encoder A's certificates use a unit (H(1), Y(1,2)); encoder B's formula is certified on
  its own at both instances (64-cube split at (6,8,11)), so the bounds via encoder B do not use Lemma refl;
- §4 "Validation", Regeneration bullet: the 32 cube files with ¬Y(1,2) have no earlier record; written from the
  regenerated base, hashed before solving (`cubes.sha256`), checked byte for byte by `verify_cover64.py` and
  `verify_final64.py`;
- §6 "Checkers": CaDiCaL 2.1.3 also for the ¬Y(1,2) run; hash check of the cube files split into "64 of the original
  split by hash" and "32 new ones byte for byte"; the same two binaries, checked at the start and end of that run
  (`noty12-2026-11-06/TOOLS_AND_PROOFS.sha256`);
- §6.2 "Split": new paragraph on encoder B's 64-cube split (twenty contradictory and twelve phase orders with
  ψ₂ < ψ₁ among the ¬Y(1,2) cubes);
- §6.2: new paragraph "The cubes with ¬Y(1,2) (encoder B)" with the run's facts (12:47–15:40 KST, CaDiCaL 2.1.3 on four
  lanes, cake_lpr one at a time, 32 of 32 accepted, none rejected, 35,411 s CaDiCaL, 0.8–3,921 s per cube, 2,471 s
  cake_lpr, 56.3 GB raw, 14.9 GB `.lrat.zst`, 16.8 GB data directory, `verify_final64.py` PASS) and the conclusion
  "F_B(6,8,11) is unsatisfiable" by Lemma k8s:lem:cube;
- Theorem 6.1: heading adds the ¬Y(1,2) run (32 of 32); proof: sixfold via the 64 cubes of encoder B, F_B unsat by
  Lemma cube, Corollary (a) without the reflection lemma; encoder A's 32 cubes with Y(1,2) as the cross-check, with
  Lemma refl;
- Table 7: the soundness row says the reflection unit is used only by encoder A; "Certified files…" row adds the 32
  new cube files (byte check); the cover row covers both splits (two checkers each); the sixfold certificate row is
  split into "encoder B: F_B(6,8,11) through 64 cube formulas" and "encoder A (cross-check): 32 cube formulas with
  Y(1,2)";
- §8 "What is trusted": `verify_cover64.py` and `verify_final64.py` for encoder B's 64-cube cover (written for that
  run, so not "separately written" like `strict_cover.py`); "Further limitations" (1): the ¬Y(1,2) proofs (14.9 GB
  compressed, `c6upper-noty12-20261106`) are not public;
- §9: two commands for the ¬Y(1,2) run, a sentence on the paths at the top of `noty12.py` and `verify_final64.py`, and
  "the run for encoder B's cubes with ¬Y(1,2)" ran on the same workstation;
- Appendix A intro: where the hashes of the 32 new formulas, proofs, compressed proofs and tools are;
- `Supp`: "C6UPPER (including C6UPPER/replay-2026-11-06 and C6UPPER/noty12-2026-11-06)" and the proof directory
  `c6upper-noty12-20261106` (not public).

Unchanged: the wording "written proof (not refereed)", gaps (G1)–(G3), the Lean-checked reduction, the sevenfold
certificates, all tables generated by `make_tables.py`. Nothing claims ES(8) ≤ 310.

**Checks.** `make_tables.py` re-run under the caps: PASS, `tables/` byte-identical. `diff` of the note and the copy:
only the header comment and edits 1–9 (the diff outside the header is the same as before the revision apart from line
numbers and the new footnote text). Builds: see the file table (`p1.pdf`: three passes, 33 pages, 0 errors, 0
undefined references, 0 LaTeX warnings); `WRITEUP/note/k8_soundness_wrapper.tex` compiled into a scratch directory
(three passes, each exit 0; 12 pages; 0 errors, 0 undefined references, 0 warnings, no overfull or underfull box); the
committed `WRITEUP/note/k8_soundness_wrapper.pdf` was not rebuilt. No SAT solver or proof checker was run for this
revision; the certificate figures were read from the record.

## Fix round after the checker on the encoder-B revision (6 November 2026, about 16:40–16:50 KST)

An independent checker re-examined the revision for the encoder-B base formula. It found the mathematics, the numbers
(against `C6UPPER/noty12-2026-11-06`), the sync of the two copies and both builds correct, and raised five wording or
precision points, each applied as proposed:

| point | change |
|---|---|
| 1 (remark after Lemma k8s:lem:affine: "only for encoder A" is literally false, since Theorem k8s:thm:sound(a), about F_B plus the unit, uses Lemma refl) | "that is, only for encoder~A, the cross-check." → "that is, only for parts~(a) and~(b) of Theorem~\ref{k8s:thm:sound} (formulas with the reflection unit); the bounds via encoder~B use part~(a$'$) and do not need it." The note's 5-line revision comment in its header, which summarized this remark together with the trust table and (G4), was adjusted to match: it now says that these places state that the bounds via encoder B use neither Lemma refl nor the τ case of Lemma affine (encoder A's route, the cross-check, uses both) |
| 2 (Corollary k8s:cor:geom(a): the second hypothesis is "for one encoder", so it also covers encoder B's 32 Y(1,2) cubes) | "(the route of encoder~A, the cross-check)." → "(this route uses Lemma~\ref{k8s:lem:refl}, through Theorem~\ref{k8s:thm:sound}(a), resp.~(b); it is the route of encoder~A, the cross-check)." |
| 3 (paragraph after Theorem k8s:thm:sound repeated itself) | "; its proof is that of~(a) without the reflection step" deleted; the sentence now ends after "(Section~\ref{k8s:sec:cube})" |
| 4 (abstract read as 96 cubes; sign patterns "certify") | the sentence after "accepted every fresh proof" now reads "For one of the encoders, its $32$ replayed cube formulas and $32$ further ones, certified the same day, cover all $2^6$ sign patterns of six phase-order variables, so that encoder's sixfold base formula is certified unsatisfiable on its own and its route to the sixfold bound does not use the reflection symmetry breaking." |
| 5 (Theorem 1.1 rigor note: notation before its definition, two different 64s) | "all $64$ cube formulas of the original split ($32$ per encoder) were regenerated"; "one for each sign pattern of the six phase-order variables $Y(1,2),\dots,Y(3,4)$ (Section~\ref{sec:enc})"; "does not use the reflection lemma (Lemma~\ref{k8s:lem:refl})" |

Points 1–3 were applied to `WRITEUP/note/k8_soundness.tex` and `k8_soundness_p1.tex` alike. The source now hashes to
`50bcd17a2614c3ba28530d2ce9ae7b35eb5149e651b2641cc4020be85897093d` (before this round `0fe99cfe…`); the copy's header
(line 2, and lines 3–11 reflowed to name this round, still 28 lines) and the two places above carry it. Left as they
were: the end of §k8s:sec:reflection ("The reflection unit is used only by encoder~A, the cross-check"), the last
trust-table row and (G4), which speak of the certificate routes and which the checker passed; §3 and §4 of `p1.tex`
likewise. The "Revision for the encoder-B base formula" bullets above give the text after this round.

**Checks.** `diff WRITEUP/note/k8_soundness.tex WRITEUP/P1/k8_soundness_p1.tex`: the 28-line header and edits 1–9 only;
outside the header the diff is the same as before this round, line numbers aside. `p1.pdf`: three passes under the
caps, each exit 0; 33 pages; 0 errors, 0 undefined references or citations, 0 LaTeX warnings; 1 overfull box (13.3 pt,
head of Lemma 5.2) and 5 underfull boxes, as before; Theorem 5.24, Corollary 5.28 and §5.9 keep their numbers; `p1.aux`,
`p1.out` and `p1.toc` deleted. `WRITEUP/note/k8_soundness_wrapper.tex` compiled into a scratch directory: three passes,
each exit 0; 12 pages; 0 errors, 0 undefined references, 0 warnings, no overfull or underfull box. No SAT solver or
proof checker was run, and nothing new is claimed.

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
3. **Commit to cite.** The `Supp` entry names branch `es7-night-2026-11-01` and says that the records cited are
   those at commit b583d89ab or later; fix the commit to cite once P1 is committed. The record
   `C6UPPER/noty12-2026-11-06/`, which the paper now cites, and the revision for the encoder-B base formula are not
   yet committed (6 November 2026, 16:40 KST).
4. **Bibliographic data from memory: done (6 November 2026).** The entries for CaDiCaL 2.0 (CAV 2024), cake_lpr
   (Tan–Heule–Myreen, STTT 2023 and TACAS 2021), LRAT (Cruz-Filipe et al., CADE 2017), Lean 4 (de Moura–Ullrich,
   CADE 2021) and Mathlib (CPP 2020) were entered from memory. In the bibliography audit of 6 November all six were
   checked against their Crossref records, and volumes and pages match (CaDiCaL 133–152, LRAT 220–236, Lean 4
   625–635, Mathlib 367–381, STTT 25(2) 167–184, TACAS 223–241). The other entries follow `LIT/references.bib` and the
   notes' bibliographies (Dumitru given as "B. Dumitru", as `NOVELTY20261106` asks); the audit corrected or completed
   five of them (KKS70 title, HS24 pages, SMQH25 volume, KPH26 venue, GGTW25 version) and added four (ETV96, Sche20,
   Sche23, SMHM24; see "Revision after the audit").
5. **Unreviewed new text.** Remark 1.3 (affine symmetries) and the proof of Corollary 1.2 (now with the step from a
   rotation of order m to the rotation by 2π/m) are new in this draft and have had no internal review; both are
   labelled so in the paper and in Table 7. The revision text of the review round (below) restates records and has had
   no second review. A draft of the corrected proof of Corollary k8s:cor:geom (written with τ and A, shortly before
   b583d89ab) was checked once by a reviewer within the session (record: `reviews/corollary-geom-review-20261106.md`;
   no defect, three wording remarks). That is not an independent review, so the paper keeps listing the corollary as
   having had no internal review (G4). The committed text (b583d89ab) took up its wording remarks after that check, so
   its final wording was not itself re-checked: the translation is η, not τ; R_c(x) = c + ρ(x − c) replaces the "linear
   part" A; part (b) says that no cube step is needed; and R_c is named as `rotAbout` with centre c. Its optional
   pointer from the sentence "after translating the centre to O" to the corollary was not added, because that would
   change the copy away from `WRITEUP/note/k8_soundness.tex`.
6. **Seven-fold verification count.** The paper says every sevenfold convex-subset count rests on at least two
   separately written programs, and on four or more for the five files also in `ES8SYM/sets`. `c7_64_own_s1000` has
   only the two `check64` programs on record (`m7_x2_G9s_centre` has a third DP in
   `PRIMEFOLD/cluster/thmA/cert_m7_x2_G9s_centre.log`). Running the `ES8SYM` pipeline on it would make "three programs"
   uniform for both symmetry types.
7. **Inconsistencies found in the sources** (the paper uses the values computed from the raw records; the first two
   were corrected in `C6UPPER/README.md` on 6 November 2026, audit findings F12 and F13):
   - `C6UPPER/README.md` gives 41.0 GB for encoder A's proofs (all 32 cubes) but 45.7 GB for encoder B's (the 12
     phase-order cubes only). From the byte counts in `C6UPPER/SHA256SUMS.txt`: A 40.8 GB (12) / 41.0 GB (32), B 45.7 GB
     (12) / 46.5 GB (32). The paper gives both.
   - `C6UPPER/README.md` says CaDiCaL peak RSS 1.3–1.7 GB for encoder A; `logs/cadical_summary.txt` has up to 2,046 MB
     (cube c10000). The paper says 1.3–2.0 GB.
   - The hardware of the original solver runs is not uniformly recorded (the sevenfold cake_lpr logs are macOS `time`
     output); §9 says so.
8. **Gaps of the proof itself** (as in the reviewed section): (G1) code-to-clause correspondence by reading
   the source; (G2) no formalized step from DIMACS to `Sixfold66`/`Sevenfold70`; (G3) encoder A's binary64
   classification (covered twice at the certified instances); (G4) parts marked "new here" or "not in the review" are
   unreviewed; since the revision for the encoder-B base formula (G4) also says that Theorem 5.24(a′) and the 64-cube
   split were added after the review, and that Lemma refl and the τ case of Lemma affine are used only by encoder A.
   The ¬Y(1,2) certificates close none of (G1)–(G4); they remove Lemma refl and the τ case of Lemma affine from the
   encoder-B route. The proof archives (`es8-c6-octagon-2026-11-03`, `es8-c7-octagon-2026-11-03`), the review archive
   `es8-c6c7-review-2026-11-04` (regenerated formulas, models, witnesses) and the replay proofs of 6 November (`c6upper-replay-20261106`, about 28.4 GB of
   `.lrat.zst`) are not public. The replay of 6 November closes no gap among (G1)–(G4); it closes the separate gap that only 6 of the 64
   sixfold verdicts were hash-bound.
9. **Literature.** The novelty paragraph is evidence only. Not accessed: the SMQH CICM chapter text, Baek–Balko's
   JCTA version, Erdős–Tuza–Valtr 1996, Scheucher 2020 and 2023, Subercaseaux–Mackey–Heule–Martins 2024 (cited only as reported in HS24 and SMQH §1), paywalled databases. Repeat the search before submission.
10. **Cosmetic.** One 13.3 pt overfull line in the head of Lemma 5.2 (long Lean names in the reviewed source; left as
    is so that the copy differs from the source only by the documented edits).
11. **Sync.** If `WRITEUP/note/k8_soundness.tex`, `C6UPPER`, `SIX60` or `PRIMEFOLD` change, rerun
    `tools/make_tables.py`, re-create `k8_soundness_p1.tex` and recompile. (`make_tables.py` does not read
    `C6UPPER/noty12-2026-11-06`; the figures of the ¬Y(1,2) run in §6.2 are typed from its `results.tsv`.)
12. **Public artifact (gap, not closed).** The supplementary material has no public archived deposit or DOI, and the
    proof archives (about 90 GB, plus about 28.4 GB of replay proofs and 14.9 GB of ¬Y(1,2) proofs from 6 November) are private, so a referee cannot inspect the artifacts. Deposit (for example on
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
16. **Two figures in `C6UPPER/noty12-2026-11-06/README.md`** (found in the revision for the encoder-B base formula; the
    record was left unchanged): "16 GB as `.lrat.zst`" is the whole data directory (16.8 GB); the 32 `.lrat.zst` files
    take 14.9 GB. "the 12 phase-order cubes take 2,600–3,900 s" should read 2,320–3,921 s (`results.tsv`). The paper
    uses the computed values. Correct the record README when it is committed.


## Second checker round on the encoder-B revision (6 November 2026, about 17:10 KST)

The second independent check found no mathematical problem and four wording points, applied by hand:
- `p1.tex` §6 "Checkers": the 32 cubes with ¬Y(1,2) were solved only once, by CaDiCaL 2.1.3, and lrat-check was not
  used for them (the sentence used to say all formulas were first solved by 3.0.1);
- `p1.tex` §2 "Rigor labels", Certificate bullet: the solver list names the ¬Y(1,2) run;
- this README's §k8s:sec:cube bullet now describes the kept text exactly;
- the copy's header lists the two paragraphs after Theorem k8s:thm:sound's statement and its proof among the changed
  text (comment only; the source hash `50bcd17a…` is unchanged).
Also corrected in the record `C6UPPER/noty12-2026-11-06/README.md`: phase-order cubes 2,320–3,921 s; 14.9 GB of
`.lrat.zst` (16.8 GB for the data directory). The optional rewording of (G4) was not applied. `p1.pdf` rebuilt: three
passes, 33 pages, 0 errors, 0 undefined references.
