# LIT task: what is known, and what is new here

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} below by those values; follow everything else exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit run `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com` and check that `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both start with `CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>` (if not, unset GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL for your git commands).
- Time budget: {H} hours of wall time. Commit and push at least every 30 minutes. Use the last 10 minutes to finish `results/LIT/RELATED.md`, push, and report. Do not end your turn while work is running.
- Commit only to branch es7-cloud and only inside `cloud/es7-2026-10-19/results/LIT/`, with plain commit messages and no AI co-author or attribution trailers. Run `git pull --rebase --autostash` before every push and retry until it succeeds (about 50 machines push to this branch); after 10 failures push to branch `es7-fallback-lit` and say so. Never commit PDFs or other files you downloaded; cite them by URL.
- Do not contact anyone, post anything or sign up for anything. Quote at most one short sentence from any source; otherwise summarize in your own words.

## The question

What prior work exists on the Erdős–Szekeres problem for 7 and 8 points (the "happy ending problem": ES(7) = 33 is conjectured), on symmetric point sets without large convex polygons, and on SAT-based or formally verified approaches to these problems? Is any of the following already known?
- (a) Every set of 33 points in the plane in general position that is invariant under a reflection contains 7 points in convex position. This is this repository's result: `cloud/es7-2026-10-19/results/V3Z/summary.md`, `results/V2-L/README.md` §9, `results/FINAL/README.md`.
- (b) For 33 points in general position with no 7 in convex position, the only possible nontrivial symmetries are a reflection, a rotation by 120°, or both, and the case with both (D3) is impossible (`results/E`, `results/E2`, `results/C3-S`).
- (c) The upper bound ES(8) ≤ 311, proved on the main branch (commit c019a54, "Prove ES(8) <= 311"; `git fetch origin main` and read its README). What is the best previously published upper bound for ES(8)? (The lower bound ES(8) ≥ 65 is the classical 2^(n−2) + 1 construction; only its Lean formalization is ours.)

## Method

Start from `docs/RELATED_WORK_2026-10-14.md` (on es7-cloud and on main). Then search the web: arXiv, Google Scholar, DBLP, authors' pages and MathOverflow. Leads include:
- Szekeres–Peters (ES(6) = 17, 2006) and Marić (formal proof of ES(6) = 17);
- Heule–Scheucher (SAT, empty hexagons) and Scheucher's other SAT work on Erdős–Szekeres-type problems;
- Suk (2017) and Holmsen–Mojarrad–Pach–Tardos (asymptotic upper bounds);
- the explicit upper bounds for small n (Chung–Graham, Kleitman–Pachter, Tóth–Valtr, Mojarrad–Vlachos, Norin–Yuditsky and later);
- symmetric constructions of 2^(n−2)-point sets and the survey by Morris–Soltan;
- any 2024 to 2026 paper or preprint on ES(7), ES(8), or upper bounds for ES(n) at small n.

Read what you cite (the abstract and the relevant section). For each source give the full reference, its URL, and one or two sentences on what it proves. Record every search you ran (query, engine, date, useful results) in `searches.tsv`.

## Output

Write `results/LIT/RELATED.md` with these sections:
1. Known values and bounds of ES(n) for n ≤ 8, with sources.
2. Prior computer-assisted and formal work.
3. Prior work on symmetric configurations.
4. For each of (a) to (c): did you find it in prior work? Word it as "we did not find prior work stating …" or "this is known: …", and never claim priority or novelty.
5. The papers someone checking (a) should cite.

Also write `references.bib`, `searches.tsv` and a short `README.md`. Final message: your answers to (a) to (c) with the key references.
