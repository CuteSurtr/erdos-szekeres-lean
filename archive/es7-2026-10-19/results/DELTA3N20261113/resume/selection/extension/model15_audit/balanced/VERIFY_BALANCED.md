# Balanced fifteen-point coordinate equivalence — confirmed

**COMPUTED exact independent geometry and equivalence check.** The existing
**CERTIFIED fixed-membership result** applies without changing its CNF or
proof. The discovery coordinates, original audit and all its receipts remain
unchanged. This follow-up writes only the `balanced/` subdirectory.

The independently checked points, in increasing x order, are:

```
(0,0), (37,-35), (38,-248), (84,-270), (202,-640),
(472,-427), (653,-757), (665,-793), (666,-717), (683,-718),
(736,-567), (737,-827), (926,-895), (999,-926), (1000,0).
```

`verify.py` imports only the previous audit's own independent geometry
helper, whose hash is pinned in the receipt. It does not import the parent
coordinate finder or encoder. It repeats exact integer determinant, hull,
cap and all-subset calculations on both the balanced and original inputs.

All 455 orientations agree and are nonzero; the minimum absolute determinant
for the balanced set is **45**. The entire four-cap, bad-triple and six-target
families agree, as do their complete containment tables and every nonconvex
four-subset containment value. Direct results are unchanged:

- 48 four-caps, no five-cap; 78 bad triples.
- 187 convex six-subsets, no seven-gon; maximum cap/cup/convex sizes (4,6,6).
- No terminal-safe weak Delta among **32,768** selections.
- **4,805 ordinary weak Deltas**, with the same size counts and root-specific
  minimum sizes/witnesses as the original audit.

The checker reconstructs all 48+78+187 membership clauses from its own
balanced-coordinate geometry. They match the full emitted clause multiset.
The parent's `balanced.terminal.cnf` is also **byte-for-byte identical** to
the archived independently certified original CNF, with SHA-256

`7d18c713d190d893a4d3d7873e8caa7d45061326c403ee8133888382040cc22a`.

The retained proof still hashes to
`1f25c0cbe8988577fecbfaf9379ffde400bca45d047cee6ce15bf3391bf94cef`,
and the previously checked receipt and exact `s VERIFIED UNSAT` log are
intact. Therefore the same certificate applies to the balanced realization;
this follow-up does not claim a new solver run or fresh cake replay.

The JSON and point-file coordinates were compared with the requested point
list and with each other. All input hashes were stable before/after the
check. The historical audit manifest verifies all 28 original files.
Frozen balanced coordinates, CNF and the full receipt are in `data/`, with
a separate scoped manifest here. No original discovery file or shared
manifest was overwritten.

The check took 0.255 seconds, peaked at 16,704 KiB RSS, and used one CPU,
AS400 MiB, an 18-CPU-second cap and an external 20-second deadline. There
was no failed check, timeout, memory failure or long job. No global
minimality or coordinate-optimality claim is made. Uniform-envelope
behavior is not asserted by this orientation-equivalence audit.
