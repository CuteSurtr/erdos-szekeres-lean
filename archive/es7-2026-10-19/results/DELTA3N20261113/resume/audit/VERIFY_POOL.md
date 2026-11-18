# Independent audit of the lazy subset pool

**COMPUTED independent checks passed for the intended m16 searches, with two
reproduced input/progress bugs.** No soundness defect was found in the clause
selection, Boolean geometry, or tiny export. This does not certify either
m16 search or establish an all-size Delta statement. The compact encoder is
outside this audit. The subsequent maximal-set family has a separate report.

Scope: `../pool/batch_pool.py`, its README, the previous encoder's `DESIGN.md`,
and its clause-order contract. The audited driver SHA-256 is
`0e1700be00d4fbf93f2965f3ff3caf1a5ccbd9b4c966f3ff04ec5322b1995c30`.
Only the assigned `audit/` directories were written. No git action, long job,
systemd unit, proof checker, or third-party installation was performed.

## Findings requiring attention

1. **Valid small instances crash.** At driver lines 40, 45, 59 and 61, empty
   combination lists become one-dimensional NumPy arrays. Consequently
   `analyze` raises `AxisError` for valid inputs with m=4 or m<n. Exact
   parabola fixtures reproduced this at (m,n)=(4,5),(4,8),(5,6),(5,8),(6,7),
   (7,8). The reference finds respectively 15,16,31,32,63,127 working masks.
   Shape empty arrays with their intended second dimensions, or explicitly
   restrict the driver's input domain. The active m16 inputs are unaffected.
2. **`--batch 0` prevents progress.** Lines 139–148 sample no masks, despite
   a valid model having working Delta. A one-second control revisited one
   identical sign model 14,306 times, added zero clauses and returned UNKNOWN.
   Require a strictly positive batch; a negative batch is also invalid.
3. **The internal deadline is cooperative.** Lines 122–124 check the clock
   only between solver calls. A 5,000-conflict budget is not a wall-time
   bound, and SIGTERM only sets a Python flag. Loading, analysis and final
   export also have no internal wall-time interrupt. Continue to use the
   parent's finite external unit deadline; `--seconds` alone is insufficient.
   No long-run deadline experiment was performed here.
4. **Execution provenance is recorded late.** Line 161 hashes the script
   at exit, not when Python loaded it. Editing this shared script while a
   run is active can misidentify the executed revision. Preserve a startup
   hash/source snapshot when revising the driver. The hash remained unchanged
   throughout these short controls.

Details and exception messages: [edges.json](results/edges.json) and
[exports.json](results/exports.json). No parent source was edited.

## Formula contract and written justification

Write the original unconditioned formula as
`F = B AND (AND_{0 <= d < 2^m} C_d)`. The encoder calls `pool()` after all
base, witness and lattice clauses, emits one clause per ascending integer
mask, then calls `restrictions()`. The driver requires weak mode, no symmetry,
no cube and no fixed signs, so those later restrictions emit no clauses.
The original encoder source hash is
`b953e14fc7d0840712bbf63f502e00c7342cbd1cdb9ef3ed548759e8ae8aa12c`.

Every stage is exactly `B AND (AND_{d in P} C_d)` for a growing set P. Entire
original clauses are retained, including empty ones; no literal is deleted
from within a clause. Thus F implies every stage, and certified UNSAT of a
stage implies UNSAT of F. The canonical-assignment argument for the original
encoder in DESIGN applies unchanged. This is a fixed-m implication; it
does not establish the conjecture for all m. Even adding an arbitrary mask's
original clause is safe. Working-mask discovery matters for progress and
candidate interpretation, not for that weakening implication.

The independent checker reconstructs the old weak/lattice variable allocation
and checks the complete suffix clause for each mask, rather than merely
trusting its length. It also compares the running base file byte-for-byte
with the original prefix. Both actual m16 inputs passed:

| n | Base clauses | Suffix clauses checked | Distinct masks in captured pool |
|---|---:|---:|---:|
| 7 | 446,670 | 65,536 | 511 |
| 8 | 815,610 | 65,536 | 511 |

Input CNF hashes are `6bc7690369f19b2a908f6adbc0b4b9a23f67de8e8c4cf41482670a835e6df425`
and `56b09f02c0c3c116ebee2b3778372d5b9d2a7d9312ff2f53eaa1cca287c55eca`.
The results and separately hashed interim status/pool snapshots are retained
in [input7.json](results/input7.json), [input8.json](results/input8.json), and
`results/interim/`. There was no final m16 CNF at those reads; neither final
formula is checked here. Status and pool files are written separately and
must not be assumed to be an atomic snapshot.

## Exact geometry, complement and reversal

[`audit_pool.py`](audit_pool.py) is new independent code. Its reference uses
Python integer determinants, monotone convex hulls of each relevant subset,
and a direct scan of every Delta against cap and polygon families. It imports
neither the previous checker nor its lattice/zeta logic. Importing Geometry
serves only to exercise the implementation under test.

The driver's NumPy arithmetic uses Boolean signs, Boolean convexity tests,
uint8 OR transforms and int32 mask/index arrays. For the inherited m<=20
domain, masks fit in int32; no coordinate or floating arithmetic occurs.
The zeta step computes exact containment. Reversing the length-2^m array
maps d to `2^m-1-d = full XOR d`, exactly the complement, not a spatial
reflection. In contrast, reversal of an m-bit mask at line 145 is the vertex
order reversal. It only chooses another original clause; it imposes no sign
symmetry and need not be a working Delta in that same model.

Controls passed all **101,184** individual Delta-mask comparisons (15 cases)
and **131,056** bit-reversal comparisons (all masks, m=4 through 16). Each
cap/target containment array and every complement lookup was also compared
directly. The real fixture's 455 signs were recomputed from its integer
coordinates and matched the saved signs exactly.

| Actual real15 fixture | Four-caps | Target polygons | Working weak Delta |
|---|---:|---:|---:|
| n=6 | 80 | 216 | 353 |
| n=7 | 80 | 0 | 9,182 |
| n=8 | 80 | 0 | 9,182 |

All three have no five-cap and no prohibited n-gon. The other twelve controls
use small integer coordinates, three for each n=5,6,7,8; they were selected
only for general position and the geometric premises, never for their Delta
outcome. Coordinates, signs, complete families and every working mask are
retained in [geometry.json](results/geometry.json).

## Progress and candidate criteria

For a positive batch, every successful model with a working Delta contributes
at least one previously unused mask: the assertion at line 135 checks that
none already belongs to P. Its genuine working status makes its failure
clause impossible under any valid auxiliary assignment for those signs.
Consequently that orientation model is eliminated and the finite pool grows.
At most 2^m such successful additions can occur. Random selection does not
need a probabilistic fairness assumption for this argument. This is not a
guarantee that budgeted solver calls terminate promptly or that a finite
runtime finds a decisive result.

`ABSTRACT_CANDIDATE` requires a model of the stage plus valid signotope
packets, no five-cap, no convex n-gon, and zero working masks across the full
2^m scan. It is evidence of an abstract counterexample only. Independently
check its signs before accepting it; exact coordinates are additionally
needed for a real-point claim. UNKNOWN and SAT with working Delta provide no
counterexample. Finder UNSAT remains UNSAT_UNCERTIFIED until fresh CaDiCaL
2.1.3 LRAT and the exact cake acceptance line for the exported CNF.

## Tiny export and both parent checker outcomes

An independent driver invocation reproduced the parent's n6/m8 run: one
model, 195 working masks, 31 selected clauses, then finder UNSAT. Both final
CNFs have 382 variables and 1,785 clauses: exactly the 1,754-clause original
prefix plus the 31 recorded original subset clauses in their insertion order.
All 256 original suffix clauses were checked too. The files are byte-identical:
`1dda6ceb4fe33203428f317e8dd9aad1dddc598a8a0f8a442a1ce43f0def67c0`.
The independent invocation remains labelled COMPUTED / UNSAT_UNCERTIFIED.

The parent's separate certificate evidence is retained with both outcomes:

- [Initial helper log](results/parent-tiny/cert/certify.jsonl) records
  `REJECTED or incomplete`, with [initial checker output](results/parent-tiny/cert/final.cake.out)
  `CakeML: cannot allocate the heap and stack: Cannot allocate memory.`
  This was a safe allocation failure under the reported 400 MiB address-space
  cap, not an OOM kill or mathematical rejection of the proof.
- [Explicit replay output](results/parent-tiny/cert/cake-stack32.out) contains
  the exact line `s VERIFIED UNSAT`. The parent reports 128 MiB heap and
  32 MiB stack for that replay. The successful output does not overwrite the
  failed initial attempt.

The retained 3,075-byte LRAT hashes to
`bf843d82fc0ee09e2232c8494413d69c0ae2a04a2d257c74200a124093e73ee1`.
The CNF/proof hashes match the original helper record; decompressing the
retained zstd proof reproduces those exact proof bytes. This audit checked
the logs and hashes and did **not** independently rerun cake. The parent's
tiny fixed-size certificate is separate from either m16 search and from any
all-size claim. See [certificate.json](results/certificate.json).

## Resources, files and reproduction

Each control used a 400 MiB RLIMIT_AS, one CPU affinity, one numerical-library
thread, an 18-second CPU limit and an external 20-second SIGKILL deadline.
Observed controls took 0.04–1.16 seconds; checker peak RSS was at most
49,324 KiB. The numerical runs verified one live thread. The initial capacity
check included both `esr` and `nov13c` prefixes and showed four spare cores
at the start of controls. No user unit was started or altered.

Run `audit_pool.py` with each mode separately under `timeout -s KILL 20s`,
using `/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B`:
`geometry`, `edges`, `exports`, `input7`, `input8`. The exports control uses
fresh scratch subdirectories and deliberately refuses to overwrite a run;
preserve earlier runs when choosing new names. [`collect_results.py`](collect_results.py)
copies the small evidence, checks its hashes and preserves both checker
outcomes. [MANIFEST.json](results/MANIFEST.json) lists every copied source,
size and SHA-256. Scratch remains
`/home/jay/research/data/delta3-codex-20261113/resume/audit`.

Initial outstanding items were fixes/provenance, completed m16 exports,
and fresh proof/checker evidence for any UNSAT. The two follow-ups below
resolve the first two items; both completed finder results are UNKNOWN.

## Follow-up: v2 fix review

The original source was kept frozen for its running jobs. The separately
named `../pool/batch_pool_v2.py` was reviewed by a direct source diff, with
SHA-256 `d1a7f65a991426407774152cbca231114d739d09d0f675d568cd3bda2fc8d4f7`.
The fixes address the reported issues without changing clause selection:

- The five-cap index array explicitly has width ten; polygon index arrays
  explicitly have shape `(number_of_sets, C(k,4))`, including zero rows.
  All supported k are at least four, so these dimensions are well-defined.
  Vacuous reductions on zero rows produce no forbidden five-cap or n-gon.
- Argument validation rejects batch<=0 before creating the output directory;
  it also rejects nonpositive seconds and AS below 200 MiB.
- The source is captured once at startup, written to `script_snapshot.py`,
  and its startup hash is included in status from the beginning. The exit
  code no longer re-hashes the potentially modified source path.

The parent reports all six edge fixtures now pass with counts
15,16,31,32,63,127. Per the requested limited fix review, those controls and
the full suite were not rerun against v2 here. The diff supports the fixes;
the runtime deadline remains cooperative and still needs the external cap.
The original two bug reproductions remain valid evidence about v1.

## Follow-up: completed m16 exports

Both original pool runs completed with **COMPUTED / UNKNOWN**, after about
901 seconds. [`audit_pool_final.py`](audit_pool_final.py) independently
stream-compared each final prefix with its original source and saved base,
then compared every selected clause with its exact original suffix clause
in pool order. The original input hashes still match the previously
audited complete suffixes, and the frozen driver hashes match too.

| n | Selected masks | Final clauses | Result |
|---|---:|---:|---|
| 7 | 767 | 447,437 | Exact prefix plus selected original clauses |
| 8 | 511 | 816,121 | Exact prefix plus selected original clauses |

Final hashes are
`98d69a5edd96d51fbda084028c63d218510e9ff6a458a81fcb30ca1ced76ec03`
and `8d026714b22e7ac2d04792e19b5217d9665cfd2f5d74e52d7812bc87eca2db9c`.
[pool_final_audit.json](results/pool_final_audit.json) retains the final
status records, mask lists and hashes. This 0.424-second streaming check
used the same AS400/one-CPU/20-second caps. Neither UNKNOWN result supports
an exclusion or counterexample claim.
