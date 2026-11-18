# Delta boundary audit — COMPLETE

**PROVED:** the prior written cup-rank, `2n-3` extreme-root and `2n-2`
localization arguments are sound, with initial ranks made explicit for
leftmost reflection. **CERTIFIED:** three terminal-boundary CNFs pass
independent cake_lpr replay. **COMPUTED:** independent exact geometry,
canonical assignments and literal-family reconstruction pass.
The conclusions, assumptions and distinction between these evidence types
are in [VERIFY_BOUNDARY.md](VERIFY_BOUNDARY.md). Formal Lean is excluded.

For n=6,7,8, the written localization plus the three checked certificates
establish terminal-safe weak Delta selection on old five-cap-free,
n-gon-free sets through 9,11,13 points. A rightmost extension preserving
no five-cap is safe even if a new n-gon appears. General-size Delta remains
open. Raw and refined cup/complement obstructions are real but still admit
terminal-safe selections.

The audit reconstructed all new families in `complement.cpp`, `refine.py`
and `terminal_boundary.py`, regenerated all six original CNFs/maps, and
checked six frozen coordinate fixtures using its own code. It also checked
272 general-position grid permutations, both proof branches, horizontal
reflection, exact projective signs, and deliberate bad-clause assignments.
One source-hash path lookup failed and was corrected; details and the
benign legacy-main compile warning are retained in `data/failures.json`.

Files: `check.py`, `replay.py`, frozen fixtures and receipts in `data/`,
`data/inputs.json` for external source/proof hashes, and scoped `SHA256SUMS`.
No parent checker is imported. No prior record or shared manifest changed.
Nothing remains running or queued in this track.

## Reproduce from the repository root

Compile the reviewed source into this track's scratch directory:

```sh
audit=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/boundary/audit
scratch=/home/jay/research/data/delta3-codex-20261113/boundary/audit
py=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
mkdir -p "$scratch"
timeout 20s prlimit --as=524288000 --cpu=18 g++ -std=c++17 -O1 \
  "$audit/../complement.cpp" -o "$scratch/complement"
for mode in fixtures small; do
  timeout 20s env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    prlimit --as=419430400 --cpu=18 "$py" -B "$audit/check.py" "$mode" || break
done
for n in 6 7 8; do
  for mode in old root refined terminal; do
    timeout 20s env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      prlimit --as=419430400 --cpu=18 "$py" -B "$audit/check.py" "$mode" --n "$n" || break
  done
done
```

Formula controls read the retained parent `boundary/{sweep,refined,terminal}`
scratch inputs; original formula generation writes only audit scratch.
Frozen-fixture and small-grid controls need no external data. Each script
rewrites its own receipt, so timing/RSS and receipt hashes can change.

The parent explicitly allocated one CPU, AS800 MiB, heap600/stack32 for
these three short replays within its existing 6000 MiB track reservation:

```sh
for n in 6 7 8; do
  "$py" -B "$audit/replay.py" "$n" || break
done
```

`replay.py` enforces each cake invocation's external 20-second timeout,
AS800 MiB and 18 CPU seconds, checks the exact acceptance line, and records
before/after CNF, proof and checker hashes. For a later replay, coordinate
the same allocation with the parent and check live resources first.
No solver search, long unit, proof deletion, git or external action ran here.
