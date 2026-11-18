# Frozen high-split proof and control packet

**PROVED written reduction; parent proof review passed. COMPUTED exact
controls passed.** Frozen on 14 November 2026 under `HIGHSPLIT_SHA256SUMS`.
This packet does not certify or independently audit a parent SAT run.
Optional further structure work must use separate files.

`highsplit_reduction.md` gives the complete statement and proof for every
n>=5 with no five-cap, no n-gon and both split blocks nonempty. There is
no global cup bound. It separates unconditional cuts with at least two
right points from the conditional last cut, which needs the same
protection property at size m-1. It also gives the recursive corollary,
the exact negated-cut clause and the encoder's thinning argument.

`tools/highsplit_controls.py` checks all cross signs, general position,
cup/cap maxima, absence of five-caps, full/complement polygon maxima,
selected four-cap avoidance, and actual terminal four-cap certificates.
It uses exact integers throughout. Its polygon routine is the separate
endpoint-chain checker in `verify_structure2.py`, previously compared
with triangle-containment enumeration on 24 small configurations. For
named sets with at most ten points it also directly enumerates target
polygons by triangle containment. The control program imports none of
the old separator generator's geometry code.

The eighteen named controls in `data/highsplit_cases.json` comprise
seventeen prescribed/conditional positive controls and one inherited
negative control. They cover all three cases at n5,6,8 and two 26-point
n7 sets. Both n7 selectors have 46 selected cap triples; case (ii) tests
every possible r in the R block. The three small nonvacuous critical
controls exhaust their left selections and check 12,22,78 successful
terminal-safe lifts respectively. Other critical controls explicitly test
the empty left selection and a nontrivial left selector with cap triples.

`data/highsplit_n5_grid.json` completes the bounded 19,608-configuration
grid with 90 valid splits, distributed 5/60/25 across the three cases.
The 25 critical cases permit four-cups. All 344 eligible terminal-safe
left selections lift successfully. These are exact results for the
stated grid, not coverage of all real configurations.

`tools/check_highsplit_provenance.py` is a separate replay of the critical
extension invariants, without importing the high-split generator. It
checks that every new triple is a cup, no four-cap or terminal pair is
added or removed, the selected cap triples are unchanged, and both old
and lifted complements meet the polygon bound. It checks the old inputs
byte-for-byte at the coordinate level against their source records.
Output: `data/highsplit_critical_replay.json`. This replay shares the
existing determinant/polygon helper; it is not an outside independent
review of all geometry.

The negative control appends r=(758071,206805657) to the original
terminal18 coordinates. It has maxima (4,6,6), retains exactly 115 old
four-caps, and all triples involving r are cups. Terminal nonexistence
therefore follows by restricting a hypothetical selector to the old
eighteen points. The premise is the previously certified and parent-
audited terminal18 obstruction; its certificate is not rerun or relabeled
here. This proves why an unconditional last-cut exclusion would be wrong.

All new checks used one CPU, AS400 MiB and an external 20-second limit;
each completed in less than one second. No long unit, SAT run, install,
git mutation, external action or old-record edit was used.

From this directory, verify the frozen packet with:

```sh
sha256sum -c HIGHSPLIT_SHA256SUMS
```

Replays use the project's specified Python with `-B`, the same short-job
limits, and fresh `--out` paths in the assigned scratch directory. Run
`highsplit_controls.py --mode cases`, `--mode grid`, and
`check_highsplit_provenance.py`. The manifest includes their fixed input
fixtures and shared helper, so later optional work must not alter them.
