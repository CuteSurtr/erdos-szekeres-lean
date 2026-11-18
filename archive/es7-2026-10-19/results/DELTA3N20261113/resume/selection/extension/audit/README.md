# General terminal-safe encoder audit — COMPLETE

**CERTIFIED:** independent cake_lpr replays accept n7/m11, **n7/m12**, and
n8/m13. **PROVED:** the general projection argument.
**COMPUTED:** all independent clause, map, real-coordinate and subset
controls pass. The complete scope is in [VERIFY_EXTENSION.md](VERIFY_EXTENSION.md).
Started 14 November 2026, 04:48 KST; bounded audit completed about 05:03 KST.

## Statement

Every real five-cap-free, seven-gon-free old set through **12 points** has
a terminal-safe weak Delta, using the prior result through 11 and the new
m12 certificate. The n8/m13 certificate reconfirms the existing bound.
The same selection works after any rightmost insertion preserving no
five-cap, with the inserted point added to the selection. No new ES bound
or general-size selection result is claimed.

## Model and soundness

The source supports 5<=n<=8 and n-1<=m<=20. It retains compact geometry
and removes boundary cup/complement assumptions. Exact bad-triple flags,
four-child bad containment, n-child target containment and failure rows
for every size **0 through m-n+2** have the stated existential projection.
Under no-five-cap, avoiding bad triples also excludes four-caps. Smaller
universes outside the source domain are explicitly rejected.

## Method and results

The audit's own standard-library code reconstructs all rows/maps, checks
exact integer geometry and all subsets, and regenerates the three accepted
CNFs byte-for-byte. `replay.py` independently checks the retained LRATs;
all three logs have exactly `s VERIFIED UNSAT`.

The 18-point real counterexample supplies a canonical satisfying assignment
for all **1,047,884 fixed-sign clauses**, using only 29,092 KiB peak RSS.
It has no six-cup either, so that restriction does not rescue terminal
selection for all sizes. No large SAT solve was run.

## Controls

Six smaller real fixtures, 272 general-position grid permutations, twelve
domain-edge formulas, 462 deliberately flipped exact flags, 1,024
containment projection cases, and missing-premise/wrong-cover controls pass.
No parent or previous checker is imported.

All six small-cardinality filters match their stated masks and preserve
every other clause. The n7/m11/k2 abstract SAT model is independently
checked and has minimum terminal-safe Delta size three; real realizability
is unconfirmed. The other five short runs remain **UNKNOWN**.

## Files and hashes

Only this `audit/` directory is owned by this subtrack. Scratch is
`/home/jay/research/data/delta3-codex-20261113/extension/audit/`.
Source snapshots, frozen fixtures, full receipts, `data/inputs.json` and
scoped `SHA256SUMS` pin the evidence. No shared manifest is edited.

## What remains

The bounded audit is complete and no audit job remains running or queued.
Further parent results require separate review. General terminal-safe
existence is false at the known 18-point example; intermediate sizes and
uniform-envelope selection remain outside this conclusion. No Lean or
literature-priority review is included.

## Resource envelope and resume

Short invocations used one CPU, AS400 MiB (compile AS500 MiB), external
20 seconds. The parent separately authorized replay at AS1100 MiB with
heap800/stack32; maximum cake RSS was 825,464 KiB. Global caps remain
16 CPUs/24 GB, verifier track 6000 MiB. No long unit was needed.

From the repository root, after checking available resources:

```sh
audit=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/audit
scratch=/home/jay/research/data/delta3-codex-20261113/extension/audit
py=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
timeout 20s prlimit --as=524288000 --cpu=18 g++ -std=c++17 -O1 \
  "$audit/source/selection/extension/terminal_general.cpp" -o "$scratch/terminal_general"
timeout 20s env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  prlimit --as=419430400 --cpu=18 "$py" -B "$audit/check.py" real \
  --fixture terminal18 --fixed --path "$scratch/m18n7-terminal18/input.cnf" \
  --receipt real-terminal18-recheck.json
timeout 20s env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  prlimit --as=419430400 --cpu=18 "$py" -B "$audit/extra_controls.py" filters \
  --receipt filters-recheck.json
```

Receipt names and generated case directories must be fresh; scripts refuse
overwriting them. `check.py` also has `algebra`, `small`, `formula` and
`generate` modes. `extra_controls.py` contains domain, mutation, fixture-
fact and small-SAT checks. A future replay must coordinate the same memory
allocation first; its command is recorded in each replay receipt and
`replay.py` enforces the 20-second external limit. Preserve failed replays
and UNKNOWN outcomes. No new proof deletion, git mutation, installation,
external action or old-record edit is authorized by these commands.
