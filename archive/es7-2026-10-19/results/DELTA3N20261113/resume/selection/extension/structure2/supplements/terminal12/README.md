# Structural diagnostic of the parent's n6 terminal12 example

**COMPUTED exact diagnostic, complete and frozen.** The parent reports
an accepted fixed-membership certificate and a pending independent audit
for the twelve-point terminal-safe obstruction at n=6. This supplement
checks its relation to the written split/rank candidates. It does not
repeat the membership/certificate audit or infer global minimality.

Source: `extension/terminal12/data/3/points.txt`. Check every x cut against
the high-split, low-split and all-mixed-cup hypotheses, retaining a failing
triple at each rejected cut. Recompute cap/cup/gon bounds and inspect only
the prescribed cup-rank levels and their top unions. No whole-set uniform
selection search or new SAT encoder is involved.

All eleven cuts fail each of the high-split, low-split and all-mixed-cup
conditions. `data/profile.json` retains an actual failing triple, its
integer determinant and required sign for each rejection. Thus this
example is outside all three proved split subclasses.

The separate coordinate check reproduces maxima (cap,cup,gon)=(4,5,5),
14 four-caps, 44 terminal-unprotected cap triples and 134 pentagons. Its
cup-ending ranks are

    (1,2,2,3,4,3,3,4,4,5,4,5).

The fixed rank candidates behave as follows:

| Selected ranks | Size | Missed pentagons | Selected four-caps | Unprotected selected triples |
|---|---:|---:|---:|---:|
| 3 | 3 | 27 | 0 | 0 |
| 4 | 4 | 4 | 0 | 0 |
| 5 | 2 | 61 | 0 | 0 |
| 4,5 | 6 | 2 | 0 | 0 |
| 3,4,5 | 9 | 0 | 8 | 16 |

For example {0,1,2,5,6} is a pentagon missed by both rank-four and
rank-five selections. The input has maximum cup n-1=5, so the earlier
no-(n-1)-cup selection statement does not apply. These are diagnostics
of specified candidates, not a new universal theorem or a uniform-
envelope counterexample.

The parent's 4096-model terminal/weak counts, accepted certificate,
pending global-minimality audits, and all-size n5 conclusion are outside
this supplement's verification scope. Weak D(5,6) is unaffected.

The earlier 65-file structure2 packet and its high-split subpacket remain
unchanged. This new supplement has its own manifest. All work uses one
CPU, AS400 MiB and an external 20-second deadline.

The completed probe took 0.0062 seconds and 18,216 KiB peak RSS. One
initial output-directory error is preserved in `data/development_notes.json`;
the corrected full replay passed. No timeout, OOM, solver call or long
job occurred. `SHA256SUMS` covers this supplement only; the earlier
structure2 manifest remains unchanged and still verifies.
