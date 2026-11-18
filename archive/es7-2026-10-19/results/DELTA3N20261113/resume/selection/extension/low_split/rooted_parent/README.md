# Independent parent controls for the rooted lemma — PASS

**COMPUTED exact controls.** The universal result is the separate
[written rooted lemma](../consequences/ROOTED_LEMMA.md); this packet is
not an order-type enumeration or a replacement proof.

The parent wrote a new checker importing no worker code or result. It
uses integer determinants, an independent monotone-hull convexity test,
complete cup enumeration for ending ranks, and direct tests of every
target and selected endpoint. It implements both constructions in the
written proof and tests their conclusions independently.

From 10006 generated/named coordinate sets, 1425 have no four-cap.
Across parameters n=5 through8, **3360 eligible configuration/parameter
pairs pass**. This includes1607 nonvacuous target families and400 cases
having a convex n-gon; the latter exercise the theorem's absence of a
no-n-gon premise. All1607 deliberately empty selections fail coverage.
Fifty successful selections have a first vertex with no cap-end witness,
testing the required first-point exception. Pure cups supply explicit
examples of that exception. Representative exact coordinates and targets
for each branch/parameter/polygon status are retained in `result.json`.

The final bounded run took0.268s, peak RSS16228KiB, one CPU affinity,
AS150MiB, CPU18/19s and wall20s. Reproduction from the repository root:

```bash
/usr/bin/timeout 20 /usr/bin/taskset -c 4 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split/rooted_parent/check.py
```

The deterministic seed is202611140831. The initial successful run tested
only n<=m and therefore missed the intended pure(n-1)-cup boundary
controls. Its source and result are retained as `initial-smaller-range.*`.
The final range includes n=m+1 when n<=8 and explicitly requires a
successful unprotected-first-point example. The mathematical proof was
unchanged. No result here settles the unrestricted geometric T_n case.
