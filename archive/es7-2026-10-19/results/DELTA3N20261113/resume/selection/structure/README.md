# PROVED: bounded favorable selection from cup ranks

**PROVED (written):** for n>=6, every five-cap-free S with a prescribed
rightmost point r and |S|<=2n-3 has a rooted weak Delta. The no-n-gon
hypothesis is unnecessary. This gives **11 points for n=7 and 13 for n=8**.
The unrestricted weak conjectures remain open.

These written bounds do not enlarge the parent's separately certified
rooted frontiers through 13/14 points, whose audits belong to that track.
Dropping no-n-gon gives weaker premises and a stronger theorem at the stated
sizes. Nothing here is Lean-checked, SAT-certified, or a new numerical ES
bound. No literature-priority claim is made.

## 1. Statements

Full hypotheses, proofs and attribution are in [theory.md](theory.md).

| Result | Scope |
|---|---|
| A terminal-rank-three cap a<b<c satisfies beta(a)<beta(b), where beta is longest-cup ending rank | Written Lemma 1 |
| Each beta-level is terminal-safe in a five-cap-free set | Level unions are not justified |
| With no (n-2)-cup, right endpoints of (n-1)-gons give a terminal-safe weak Delta | Theorem 2, any size U |
| A prescribed extreme root is supported on at most 2n-3 points | Theorem 4; no no-n-gon premise |
| Any prescribed root is supported on at most 2n-4 points | Cup-complement argument; no no-n-gon premise |
| First possible failure forces maximum cup length n-2 and a convex (n-1)-gon complement to every maximum cup | Corollary 5; contradiction remains open |
| Parent's arbitrary-root n+3 lemma under no-n-gon | Reviewed proof, attributed to parent |
| Seven-point pure-cap cardinality strengthening fails | Illustrative exact real example only |
| Proposed projective slope sign must be reversed | Positive transformed last slope blocks r |

## 2. Model and soundness

Points are real, in general position, with distinct x-coordinates. A weak
Delta is four-cap-free and hits **whole** convex (n-1)-gons. Caps have
negative consecutive turns; cups have positive turns.

If U=S-r has an (n-2)-cup, counting makes that cup a transversal at the
claimed size. Otherwise every target ends on cup-rank level n-3. Each
level is terminal-safe: a cap a,b,c in one level can be preceded by the
penultimate point of a longest cup ending at a, producing an ambient
four-cap ending b,c. Hence a blocking cap a,b,c,r would force a five-cap.
The chosen endpoints hit all old targets and r hits all new targets.

Only the separate |S|<=2n-4 theorem permits an arbitrary root without
no-n-gon. The terminal-rank branch needs an extreme root. The parent's
n+3 lemma uses no-n-gon to keep a nonconvex four-set in the complement.

For T(x,y)=(x/(1-x),y/(1-x)) with r=(1,0), old signs and x-order are
preserved. A cap turn ending at r has **positive** transformed last slope.
Thus old four-caps have negative last slope in a five-cap-free full set.
Section 7 proves the identities; this is not an existence proof.

## 3. Method

Read AGENTS.md, es-research, latest STATUS20261113, resume/README,
weak_theory, descent, a4 and hypergraph. One tiny exploratory probe used
six fixed old fixtures. After the parent's finalization request, only
exact controls and record completion ran. The independent checker imports
no finder or earlier checker. Parent review of the written rank lemma and
bound is recorded, without claiming an independent code replay or formal proof.

## 4. Results and gap

At the first size outside the written extreme-root bound, failure of
terminal-safe selection requires |U|=11 with maximum cup five at n=7,
or |U|=13 with maximum cup six at n=8. **Every** maximum cup must leave
a convex target polygon. No-n-gon additionally prohibits extending any
such polygon by any point of its cup. Turning these simultaneous conditions
into a favorable exchange remains open.

Private-hit stars already coexist with no five-cap and no n-gon in old
fixtures; they do not force a contradiction. The new rank inequality alone
does not resolve their coverage obstruction. Lexicographic failures retained
by the probe concern fixed larger cardinalities, not minimum-size or
minimum-envelope selection; those selected sets already hit all full targets.

The seven-point example has maximum rooted cap-free size four and no
convex six-gon. It refutes only a proposed cardinality tool, not Delta.
All six fixed controls admit a common beta-level transversal; this finite
observation is not a universal level-selection theorem.

## 5. Controls and preserved failure

[Exact controls](exact_controls.json): **COMPUTED PASS**. Convexity is
reconstructed by triangle containment, caps by consecutive turns, and cup
ranks by direct subset enumeration. The probe instead used monotone hulls,
all-triple cap tests, and edge dynamic programming for cup ranks.

| Control | Outcome |
|---|---:|
| Frozen real configurations | 6; sizes 9, 10, 12, 13, 13, 16 |
| Terminal-rank-three triples / cup-rank levels | 275 / 35 |
| 2n-3 constructions | 10: 6 cup-complement, 4 endpoint-level |
| Nonvacuous endpoint-level constructions | 3 |
| Convex controls deliberately containing n-gons | 2, with 330/1,287 n-gons |
| Arbitrary-root cup-complement checks | 22 |
| Parent lemma, all roots at n+2 and n+3 | 40 |
| Projective identity controls | Six frozen fixtures and the seven-point example |
| Rooted five-subset failures in illustrative example | All 15, explicit cap witnesses |

Final checker: about 0.27 seconds, maximum RSS 16,760 KiB. Programs used
one thread, 384 MiB AS, 18 CPU seconds and external 20-second timeouts.
[failure_01.json](failure_01.json) preserves the initial source-path error
before any geometry ran. No conclusion was drawn from it. A later patch
format error is also retained there. No solver or long unit was launched.

## 6. Files and hashes

- [theory.md](theory.md): written arguments and exact gap.
- [probe_selection.py](probe_selection.py), [probe_selection.json](probe_selection.json):
  bounded probe, frozen full coordinates, source hashes and unsuccessful rules.
- [exact_controls.py](exact_controls.py), [exact_controls.json](exact_controls.json):
  independent exact checker and positive/negative controls.
- [failure_01.json](failure_01.json), [RESULT.json](RESULT.json), [SHA256SUMS](SHA256SUMS):
  failure record, handoff and scoped manifest (excluding itself).

Scratch: `/home/jay/research/data/delta3-codex-20261113/selection/structure/`.
Its probe result is frozen here too. Replay needs no mutable external input.
No other track or old manifest changed; no git command, install or external action ran.
No proof or candidate was deleted. No work is queued.

## 7. Resume

From the repository root:

```sh
timeout 20s env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  prlimit --as=402653184 --cpu=18 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/structure/exact_controls.py
```

This writes only this track's `exact_controls.json`; timing/RSS may differ,
so the manifest describes the delivered snapshot until refreshed. New or
larger searches belong to the parent's scheduling and resource decisions.
