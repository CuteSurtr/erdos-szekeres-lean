# Ready for parent scheduling: compact weak m=16

Source and exact controls are ready. **No m=16 solver run or outcome here.**
Source argument: [SOUNDNESS.md](SOUNDNESS.md). This track's separate
integer-hull checker imports neither encoder nor existing audit code.
The parent reports reviewing the convexity recurrence, containment cover,
and reduced Delta interval and finding those arguments sound. This is
distinct from a second replay of either tiny certificate.

| n | variables | clauses | literals | DIMACS bytes |
|---|---:|---:|---:|---:|
| 7 | 127,584 | 296,714 | 1,250,856 | 8,204,520 |
| 8 | 123,216 | 346,608 | 1,350,008 | 8,984,902 |

The former no-n-gon family shrinks from 183,040 / 283,140 clauses to
11,440 / 12,870 five-literal clauses. Convex flags are full equivalences
using a five-child recurrence; the target flags reuse them. Full-formula
clause reductions are 42.1% / 60.7%; literal reductions are 42.2% / 60.8%.
No solver-speed advantage is claimed. All-side containment equivalences
were tested but cost 954,586 / 941,626 clauses; default containment uses
one-way witnesses with the exact projection argument in SOUNDNESS.md.

The files ready for the parent's 900-second reservation are:

```
/home/jay/research/data/delta3-codex-20261113/resume/compact/n7m16-final.cnf
/home/jay/research/data/delta3-codex-20261113/resume/compact/n8m16-final.cnf
```

They are byte-identical to the earlier n7m16.cnf / n8m16.cnf files audited
by the coordinate checker. Corresponding `.map` and `.stats.json` files
are present. Default generation uses no symmetry, cube, or fixed signs.
MANIFEST.json binds source, binary, CNFs, maps, and controls by SHA-256.

From the repository root, a bounded rebuild and generation command is:

```bash
R=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/compact
W=/home/jay/research/data/delta3-codex-20261113/resume/compact
(ulimit -v 491520; ulimit -t 20; timeout 25s g++ -std=c++17 -O2 -Wall -Wextra -pedantic "$R/compact_cnf.cpp" -o "$W/compact_cnf-rebuilt")
(ulimit -v 389120; ulimit -t 20; timeout 25s "$W/compact_cnf-rebuilt" --m 16 --n 7 --out "$W/n7m16-rebuilt.cnf" --map "$W/n7m16-rebuilt.map")
```

Replace `--n 7` and the output basename for n=8. The parent can run its
normal CaDiCaL/cake pipeline directly on the final CNFs. This encoder does
not start units, schedule queues, or impose a long-job memory reservation.
At 250 bytes/input literal the initial planning allowance is about
313/338 MB, before learned clauses and proof buffers. The parent's updated
proposal is one CPU per case, AS900 MiB, MemoryMax1200M, no swap, 900 seconds
for the solver, cake heap750, and a 1350-second unit deadline. Those are
parent scheduling parameters, not measured solver bounds. No such unit
was launched by this track.

For an abstract SAT candidate, orientation IDs are compatible with the
existing separately authored checker:

```bash
python3 -B cloud/es7-2026-10-19/results/DELTA3N20261113/encoder/check_model.py --model SOLVER_LOG --m 16 --n 7 --mode weak
```

For independent real-coordinate replay, with no SAT library:

```bash
(ulimit -v 389120; ulimit -t 20; timeout 25s python3 -B "$R/check_coordinates.py" --points "$R/real_n7m16.json" --n 7 --cnf "$W/n7m16-final.cnf" --map "$W/n7m16-final.map" --out "$W/n7-real-recheck.json")
(ulimit -v 389120; ulimit -t 20; timeout 25s python3 -B "$R/check_coordinates.py" --points "$R/real_n8m16_targeted.json" --n 8 --cnf "$W/n8m16-final.cnf" --map "$W/n8m16-final.map" --out "$W/n8-real-recheck.json")
```

Controls: n7 real m16 has 71 four-caps, 279 hexagons, 7,835 working weak
Deltas; n8 real m16 has 280 four-caps, 168 heptagons, 8,439 working weak
Deltas. Both have no five-cap and no forbidden n-gon. The checker evaluates
every emitted clause using integer hulls and a separate full zeta transform;
only the expected pool clauses are false. This is a positive check that
the actual ambient geometry and all definitions survive the new encoding.

Exhaustive tiny controls have zero discrepancies against the existing
encoder and direct signs. Retained `tiny_examples/` has SAT models for an
empty Delta missing a pentagon and a Delta containing a four-cap; the
working singleton Delta gives UNSAT for its individual failure query in
both encoders. Both tiny negative proofs now have exact cake success lines
in `cert-{new,old}/*.stack16.cake.out`. The initial default-stack allocation
failures remain beside them. These are tiny control certificates only.
