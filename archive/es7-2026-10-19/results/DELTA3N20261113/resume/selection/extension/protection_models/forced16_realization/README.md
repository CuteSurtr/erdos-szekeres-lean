# Fixed forced16 model is nonrealizable — PROVED

**PROVED by an explicit algebraic product contradiction, with independent
exact integer replay PASS.** Completed 14 November 2026, 07:30 KST;
started 07:06 KST. The 560 signs of this fixed forced16 model have no real
planar realization. The proof uses 387 strict determinant-product
inequalities with positive integer weights whose exponents cancel exactly.
It is a written algebraic proof with checked finite data, not a Lean proof
or an LRAT/cake certificate. No LP or nonlinear-solver verdict is evidence
for this conclusion.

## Target and scope

The fixed sixteen-point n=7 model has 136,711 variables and 338,704 clauses.
Parent's semantic report gives no five-cap, no seven-gon, 6,439 ordinary
weak Deltas and zero terminal/cup/forced selections. The parent already
tried 100,000 random fixed-x LP proposals without an exact witness.
This sidecar will not repeat that unchanged search.

## Method and soundness

The coordinate searches remained unsuccessful. The successful fallback
uses the exact identity

`[a b c][a d e] - [a b d][a c e] + [a b e][a c d] = 0`.

For each selected five-label identity, the prescribed signs force one
product magnitude to equal the sum of the other two positive magnitudes.
It is strictly larger than either summand. Raising selected inequalities
to the checked positive integer powers and multiplying gives `X > X`:
every bracket has exactly the same exponent on both sides. See
[VERIFY_FORCED16.md](VERIFY_FORCED16.md) for the proof and scope, and
[METHODS.md](METHODS.md) for finder and acceptance details.

The LP proposed only a support. Sparse integer elimination on its
560-by-387 exponent matrix had rank 386 and nullity one; exact back
substitution, denominator clearing, and integer checks produced the
certificate. `verify_product.py` imports no finder and reconstructs every
inequality from the target signs, ignoring the certificate's claimed
coefficient arrays.

## Result and controls

- 387 positive integer weights, gcd 1, ranging from 1,433,869,918,829 to
  228,087,592,790,168; sum 19,282,471,848,322,771.
- All 560 bracket exponents cancel exactly. All 16 labels occur; no
  minimality claim is made.
- Reconstruction: 0.250 seconds, 56,556 KiB peak RSS. Independent replay:
  PASS. No further coordinate search is needed for this fixed model.
- Independent real-coordinate controls: two sixteen-point sets, 43,680
  exact identities and 87,360 strict product inequalities, all PASS.
- Negative controls: one altered weight and one reversed inequality were
  both rejected. Failed-control inputs and logs are retained in scratch.

## Evidence files and hashes

The complete small certificate and receipts are archived in `data/`.
`data/manifest.json` gives SHA-256 and byte sizes for the archived evidence.

| Artifact | SHA-256 |
|---|---|
| `data/orientation.signs` | `b21664b06887c4019d75023025b1cd80582064a0b06f53698d2a70bc8fc49067` |
| `data/certificate.json` | `cfe42cec6041709b2ed7ac18ee16b13e57f091239ac19b8e5257aac46d2a326d` |
| `data/independent-replay.json` | `8ae4462877b5b0d0113de8e3f234f51b8a0f87038319fdb5757d900fe490849c` |
| `verify_product.py` | `3ae6b1b1d7bf1ae4b3714853788822630b6fed2bd7b2c54141fe284905d040ba` |

## Scope and remaining work

This resolves realizability of this fixed sign model negatively. It does
not exclude other real sixteen-point counterexamples or settle the
general forced/cup/terminal selector statements. Parent integration and
any later Lean formalization are outside this bounded sidecar. The
earlier heuristic failures remain failures, independently of this proof.

## Reproduce the exact replay

From this directory, write a fresh receipt under the owned scratch path:

```bash
timeout 20s /usr/bin/prlimit --as=629145600 --cpu=18 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  verify_product.py --signs data/orientation.signs \
  --certificate data/certificate.json \
  --out /home/jay/research/data/delta3-codex-20261113/extension/forced16-realization-independent/replay-fresh.json
```

The expected response is `status: PASS`, 387 rows, and exact cancellation.
No numerical package or solver is used by this replay.

## Milestones

- `probe-a`: 12 trials, 2.886 seconds, best 18 wrong signs; no witness.
- `run-a`: 1,159 trials, 167.106 seconds, best 13 wrong signs; no witness.
  **The SIGTERM was an intentional agent-issued `systemctl --user stop`
  for a controlled method restart, not a guard stop or resource failure.**
  Peak process RSS 79,408 KiB; no OOM. The source and negative outcome remain
  in `run-a/source.py` and `run-a/DONE.json`.
- `probe-b`: projective recentering, 52 trials, 12.001 seconds; still 13
  wrong signs. Better spacing alone did not resolve the model.
- Algebraic-search method: direct QF_NRA coordinate constraints with installed Z3.
  Only integer determinant replay accepts a model. Timeouts, solver
  failure, or an unsupported numerical/solver verdict cannot establish
  nonrealizability here. This is separate from the parent's fixed-x search.
- `algebraic-probe`: 3.268 seconds, `unknown`, no witness.
- `algebraic-run`: 152.596 seconds, `unknown`, no witness. This stage was
  deliberately shortened by sending SIGINT to its Z3 child to prioritize
  the product-identity method. It was not a guard/resource stop. Peak
  child RSS was 225,536 KiB; the retained log and DONE describe the result.
- `product-probe`: 3.340 seconds, 219,816 KiB peak RSS, no verified
  obstruction. The LP supplied a 387-entry numerical hint, but the initial
  rational reconstruction did not cancel the exponents exactly. Thus
  there is **no nonrealizability conclusion** from this probe. The hint,
  sources, and unsuccessful outcome are retained for exact reconstruction.

## Resource hold and restoration history

The parent requested a compute hold after the above completed probes to
borrow the 600 MiB allocation for the real12 Lean adapter checks. **This
sidecar releases that allocation until explicit restoration.** No further
LP, nonlinear, algebraic-solver, or native compute runs during the hold;
only editing/planning may continue. The parent expects to return the
allocation by 07:35 KST or when its checks finish. No automatic restart is
authorized merely by reaching that time. Earlier records remain intact.

During the hold, `recover_product.py` was written but not executed.
The parent explicitly restored the allocation before 07:26:26 KST.
Only then did the exact reconstruction, independent replay, and controls
run. The hold itself ran no new research computation. The restored
allocation is released on completion; no further probes are required.

The parent reports all 16 size-15 and all 120 size-14 restrictions have
positive terminal/cup/forced selections. That does not resolve realization
of the fixed sixteen-point orientation model.

## Original inputs and retained search artifacts

Input: `/home/jay/research/data/delta3-codex-20261113/extension/forced16-model/orientation.signs`.
Semantic context: sibling `forced16-semantics/report.json` in scratch.
All outputs and logs stay under this record or
`/home/jay/research/data/delta3-codex-20261113/extension/forced16-realization-independent/`.
Other packets and shared manifests are outside scope.

## Resource envelope and schedule

Owner reserves one CPU and AS600 MiB. Long work must use
`nov13c-vfy-delta6-realize16-independent`, CPUQuota100%, MemoryMax800M,
MemorySwapMax=0, RuntimeMaxSec<=2400 and driver wall<=2200 seconds.
Short probes have external 20-second deadlines. Review target 07:45 KST;
finish no later than 08:00. The shared memory guard is checked before launch.
No installation, deletion, git, external action or shared-scope edit.
