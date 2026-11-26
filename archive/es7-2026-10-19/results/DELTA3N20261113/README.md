# Delta conjecture: third research pass, 13 November 2026

> **Retention update (23 Nov 2026, owner OK):** the 39 no-verdict proof traces of this record were deleted: 34 UNKNOWN
> traces (cleanup set C29), 4 traces of SAT runs (C30: cup15-a and forced16-a proof.blrat.zst, scheduled-cup-n6-m15
> and terminal7-a/m15 case/proof.lrat.zst) and 1 UNKNOWN probe trace (NO-B9). None was a certificate; their hashes stay
> pinned in coordinator/data/archives.json and the archive manifests, and the SAT models stay in each run's kept
> cadical.log. Every certified proof, extension/low16-n7-a included, is kept. This supersedes the "retained" statements
> at README l.343-349, resume/selection/README.md l.116, ROOTED.md l.90, VERIFY_ROOTED.md l.212 and
> longcup16/README.md l.53-54. Exact paths: ~/research/data/cleanup-20261123/manifest.txt.
>
> **Retention update (24 Nov 2026, owner: "delete redundant or useless files", after "verify ..., git push and commit,
> then delete"):** 52 proofs of the 15-16 Nov tracks in `~/research/data/roadmap-20261115` (DELTA3N `attack20261115/`)
> were re-checked by a fresh cake_lpr run each on 24 Nov (`receipts/recheck_set.py`; the CNF required to have its
> recorded SHA-256, the proof decompressed and required to have its recorded LRAT SHA-256): **52/52 `s VERIFIED UNSAT`,
> 0 alerts**.
> - 49 (`receipts/roadmap_proofs_A_20261124.tsv`, sha256 `56f282941a0f7329…`, 21.07 GB of .zst): accepted in their
>   campaign (`certify.jsonl` and the `.cake.out` beside the proof), so each has now been accepted at least twice.
> - 3 (`receipts/roadmap_proofs_H_20261124.tsv`, `fdfae6461c358994…`, 8.90 GB): their own campaign's cake_lpr ran out
>   of heap. `lrr7_m15` (LRR(7) at 15) was accepted before by the main session (MAINSESSION_1115EV.md, heap 4,500 MB)
>   and `v1_base_m16` by VERIFY_RERUNS_1115EV.md; today's run is their second acceptance. The untrimmed `d48_m16` had no
>   earlier verdict; today's run (heap 11,000 MB) is its first. The **trimmed** `d48_m16.trim.lrat.zst`, accepted twice
>   (ROUND6.md), certifies the same CNF and is kept. No label changes.
> These 52 `.lrat.zst` files are deleted after this note and the tables are pushed (guarded `receipts/delete_proofs.py`:
> every file re-hashed against the pushed table first). Their CNFs, cake outputs, logs and `certify.jsonl` stay, so a new
> check needs a re-solve. This supersedes "every certified proof ... is kept" above for these 52 files only. The track
> map of the folder is `ROADMAP20261115/CLEANUP_MAP_20261124.md`.
> **Done 24 Nov 2026:** 51 of the 52 deleted at 19:18 (26.65 GB), after an AI model review (not a person), with every file re-hashed
> against the pushed tables (commit 6e39be770). Before the untrimmed `d48_m16` went, its kept trimmed proof was checked
> again (a condition of the AI model review, not a person): decompressed SHA-256 `1abf185657fb6509…` = ROUND6.md, CNF `fcc31f0428a5ffce…`, cake_lpr
> heap 4,000 MB: `s VERIFIED UNSAT` (`receipts/trim_d48_m16_check_20261124.jsonl`); the untrimmed `d48_m16` (3.32 GB)
> was then deleted at 19:25. Manifest: `~/research/data/verify-20261124/manifest_deletions.txt`. Total 29.97 GB.


**New result: the cup-side strengthening of D(5,6) is false for real point
sets.** A 15-point integer counterexample is exhibited and certified below.
**CERTIFIED:** cup-side D(5,8) holds for all 14-point signotopes, extending its
previous 13-point frontier. Independent review is in `VERIFY_DELTA3.md`.
Weak D(5,7), weak D(5,8), and their respective cup-side statements remain open.
No ES(8) bound changes. The continuation requested at 23:57 KST is complete;
[its record](resume/README.md) adds written weak-extension lemmas, sharp
repair obstructions, a real maximality counterexample, and a certified
one-point cup-side lift exclusion for the fixed old15 order type. The new
m16 universal searches ended UNKNOWN. The separate ES(8)
≤ 309 verification remains in
`../VERIFY309N20261113/` and `../ES309N20261113/`.

**14 November boundary follow-up:** [boundary/README](resume/selection/boundary/README.md)
certifies terminal-safe selection through 9/11/13 old points at n=6/7/8,
with independent encoder checks and proof replays. A written construction
refutes the proposed cup/complement shortcut for every n>=6, while exact
uniform-envelope lemmas preserve a weaker selection route. General Delta
remains open; no ES bound changes.

**14 November selection follow-up:** [selection/README](resume/selection/README.md)
adds a written rooted-Delta theorem through 2n−3 points without a no-n-gon
premise, independently replayed rooted certificates through 13 points for
n7 and 14 for n8, and certified real failures of terminal-rank selection
and one-old-blue repair. Weak D(5,7) and D(5,8) still remain open; all those
strategy counterexamples have ordinary weak Deltas.

Definitions: a valid S has distinct x-coordinates, is in general position, has no
5-cap and no convex n-gon. A cup-side Delta is a 4-cap-free subset meeting the
lower chain, including endpoints, of every convex (n−1)-gon in S. This implies
weak D(5,n). It is different from the old strong Delta statement, which also
forbids an (n−1)-gon inside Delta and is false in general.

Labels retain the previous records' meanings: **PROVED** means a written
mathematical argument; **CERTIFIED** means an explicit CNF/LRAT pair accepted by
cake_lpr with the exact line `s VERIFIED UNSAT`, together with the stated
encoding argument; **COMPUTED** means a finite exact calculation without that
certificate; **HEURISTIC** describes extrapolation from sampled configurations.
None of this record is Lean-checked or refereed.

## A real 15-point counterexample to cup-side D(5,6)

**CERTIFIED fixed-instance coloring obstruction; independently COMPUTED exact
integer geometry.** The points in `coordinator/data/cup15/realized.json` have
distinct x-coordinates, no collinear triples, no 5-cap, and no convex hexagon.
Nevertheless, every 4-cap-free subset misses the lower chain (including both
endpoints) of at least one convex pentagon. Thus the general cup-side claim of
DELTA2 §4.2b is false already at (a,n)=(5,6).

| Exact quantity | Value |
|---|---:|
| Points / nonzero triple orientations checked | 15 / 455 |
| Minimum absolute integer determinant | 70,172,849,827,134 |
| 5-caps / convex hexagons | 0 / 0 |
| 4-caps / convex pentagons | 80 / 216 |
| Distinct pentagon lower chains / upper chains | 103 / 77 |
| Cup-side Delta subsets | **0** |
| Weak Delta subsets | **353** |
| Cap-side Delta subsets | 87 |

This is not a counterexample to weak D(5,6), which was previously certified.
For example `{0,1,2,5,6,7,8}` is a weak Delta, with zero-based increasing-x
indices. Nor does the example by itself settle either n=7 or n=8. The
15-point example is deletion-minimal: every one-point deletion has an explicit
cup-side Delta, listed in `coordinator/data/cup15/deletions.json`. Global
minimality is not claimed; both universal 14-point trials timed out UNKNOWN.

The coordinates, in increasing x order, are:

```text
0                   0
652453143971       -142909694036
652470609053       -141841384900
653245553008        -69221165330
653647088977       -142390403699
653647089243        -69225072949
653647090137       -143171209446
653647090208        -69873998489
653647306973       -142430303811
688840524694       -127083550974
689437064328       -128062760103
801581924232       -310388045351
814839552245       -217612785369
836518575673        -67160176345
1000000000000       0
```

### Discovery and independent fixed-instance proof

The new streaming encoder found an abstract model of the 15-point cup-side
counterexample CNF after 668.641 seconds. A separate sign-based checker counted
all 32,768 possible subsets and obtained zero cup-side Delta choices. This SAT
discovery trace is **not** an UNSAT certificate.

`coordinator/realize_cup15.py` then found integer coordinates after 12 heuristic
SLSQP starts. The numerical optimizer's status is not evidence: acceptance
required that **all 455 integer determinants** have exactly the prescribed
nonzero signs and that the x-coordinates increase strictly. The realized
coordinates above are the evidence; the numerical search only found them.

`coordinator/audit_cup15.py` independently enumerates subsets using a monotone
hull and arbitrary-precision integer determinants. It imports neither the
discovery encoder nor its sign-based model checker. It checks the premises,
all target polygons and their lower chains, and every possible Delta. It
emits a simple **15-variable, 183-clause** coloring CNF: 80 negative four-cap
clauses and 103 positive lower-chain clauses. Every positive clause comes with
an explicit pentagon witness in `independent_geometry.json`.

Fresh CaDiCaL 2.1.3 and cake_lpr runs on that small coloring CNF produced the
exact line **`s VERIFIED UNSAT`**. This certificate, together with the direct
coordinate checks, establishes the counterexample independently of the large
universal discovery encoding. The small proof, CNF, coordinates, witnesses,
logs, and hashes are all kept in `coordinator/data/cup15/`.

| Artifact | SHA-256 |
|---|---|
| `realized.json` | `1e8b43136d096abb2deaea14743ed62a52ff622a991dd2fbbcb7140a15593b04` |
| `independent_geometry.json` | `38ba8dfbed5dd4a011670a3394f57468560db8baf7e3ea518469324e0d47320d` |
| `cup15_coloring.cnf` | `739c18a2261ba90acabd74c88f7b461485d4f1153f960d776995aef901760c71` |
| `cup15_coloring.lrat` | `f44d9ca8f512b4ee51df1d17991f67403e29e742b6f50d1246abd3baca1d889d` |

The commands are recorded in `coordinator/certify_cup15.sh`. The checker used
heap128/stack32, AS512MiB, MemoryMax700M, CPUQuota100%, no swap, and a 120-second
unit limit. No Lean check or literature-priority claim is made. A second,
separately written coordinate audit agrees on every target family and all
Delta counts: `encoder_audit/candidate_geometry.json` and `AUDIT.md`.

## A false optimization strengthening

**CERTIFIED exclusion; independently COMPUTED by complete enumeration.** A
minimum-cardinality hitting set of the lower chains need not have a 4-cap-free
minimizer. The 16-point example in
`coordinator/data/minimum16/witness.json` is valid for n=7 and has:

| Quantity | Exact value |
|---|---:|
| 5-caps / convex heptagons | 0 / 0 |
| 4-caps | 71 |
| Convex hexagons | 279 |
| Distinct lower chains of those hexagons | 176 |
| Minimum unrestricted transversal size | 4 |
| Minimum 4-cap-free transversal size | 5 |

Indices are zero-based in increasing x order. The **unique** four-point
transversal is `{1,5,6,7}`, which is itself a 4-cap. A working five-point
cup-side Delta is `{0,1,2,5,6}`. There are 17 working five-point choices.
Thus this example satisfies the cup-side conjecture and refutes only the
minimum-size strengthening.

The example was found among the old real fixtures (`pool_hept.jsonl`, index 33,
23 points, unrestricted optimum 8) and reduced by point deletion. The final
16-point example is deletion-minimal for failure of this auxiliary statement;
this does not assert it is globally smallest. Initial success on 40 cases was
only sampling evidence and did not establish the stronger lemma.

### Independent checks and certificates

`coordinator/minimum_transversal.py` implements integer orientation and
endpoint-chain dynamic programming from scratch. A lazy SAT procedure adds an
actual lower-chain constraint whenever a proposed hitting set misses it. A
forward unary counter expresses the cardinality bound: actual prefix counts
always give a satisfying extension, and the forward implications force a
threshold variable whenever that many selected points occur. Negating the
(k+1)-threshold therefore expresses size at most k.

`coordinator/audit_minimum.py` imports neither that search code nor the previous
geometry/SAT libraries. It enumerates convex subsets with a monotone hull,
checks cap inequalities using arbitrary-precision integer determinants, and
enumerates all 65,536 possible Delta subsets. It also checks that every dynamic
cup constraint saved by the search is the actual lower chain of a hexagon.
The counts, all optimum transversals, and a valid five-point Delta are in
`coordinator/data/minimum16/independent_audit.json`.

The two saved CNFs prove respectively that no unrestricted transversal has size
at most three and no 4-cap-free transversal has size at most four. Each contains
only necessary lower-chain clauses, the cardinality counter, and (for the
second) the complete list of four-cap prohibitions. Omitting other lower chains
can only weaken these CNFs, so their UNSAT verdicts suffice. Both were freshly
solved by `/usr/bin/cadical --lrat=true --binary=false` and checked with
`cake_lpr --CML_HEAP_SIZE=256 --CML_STACK_SIZE=32`; both logs contain exactly
`s VERIFIED UNSAT`. Complete files, logs, and SHA-256 values are retained in
`coordinator/data/minimum16/`.

| File | SHA-256 |
|---|---|
| `unconstrained_lower.cnf` | `5f18461168a9fcd552ed4b2498cb42f5cd00301aa3a554f2d10d681c87b5ee36` |
| `unconstrained_lower.lrat` | `130a2fd4032274864dfc9c1e21eb03fbb4f907c7463720aac032e90471bd91ae` |
| `cap_free_same_size.cnf` | `e826e80b0e8b3f667551a80b253f1ad0139e264ee1af741f374d27d5ccaa7c74` |
| `cap_free_same_size.lrat` | `68f89595c6ccbd11e66a0eefdcac147a865dd04ca0ae85f9337a8cb5234161cf` |

Reproduction scripts are in `coordinator/`. The search, deletion minimization,
and certification ran in `nov13c-vfy-delta3-minimum*` / `nov13c-vfy-delta3-minimize`
user units. Search address space was bounded at 350 MiB with MemoryMax 500 MiB;
the certificate runner used address space 512 MiB and MemoryMax 700 MiB. Each
unit had CPUQuota 100%, MemorySwapMax 0, and a finite runtime limit.

## A partial human theorem for a=4

**PROVED (written argument; independently reviewed).** Let k≥3 and let
S have no 4-cap. If deleting its rightmost point r leaves no k-cup, let E be the
right endpoints of convex k-gons in S minus {r}. Then E union {r} is a cup of
at most k−1 points and meets the lower chain of every convex k-gon of S.
Taking k=n−1 gives the strong cup-side form of D(4,n) under this extra
hypothesis, for every n≥4. The leftmost-point version follows by reflection.
The theorem does not need S to be n-gon-free.

The key step is that when k-cups are absent, every k-gon has upper chain of
length three and lower chain of length k−1. Its right endpoint therefore ends
both chains. The standard no-4-cap extension argument makes E a cup and bounds
its size by k−2; adding r preserves the cup condition. The full proof and the
precise place where the extra hypothesis is essential are in `a4/theory.md`.
This does not prove D(4,n) unconditionally or any D(5,n) case.
The independent review is `encoder/A4_REVIEW.md`; 456 bounded exact theorem
instances and the seven-point trimming obstruction passed in `a4/controls.json`.

## New compiled tools and scheduled frontier tests

`encoder/delta_cnf.cpp` is a streaming C++17 implementation of the universal
counterexample CNF. It shares containment witnesses on a subset lattice
instead of repeating every possible witness in every Delta clause. At n=6,
m=14 this yields 35,647 variables and 102,025 clauses; at m=15, 69,770 variables
and 181,556 clauses. Generation used under 6 MiB RSS. This is a memory
improvement; no solver speedup is inferred from it.

`encoder/DESIGN.md` gives the one-way witness argument, the bounded-deletion
pigeonhole identity, treatment of aliases/absent witnesses, and a written
general signotope proof connecting cap/cup unions to four-subset convexity.
The independent adversarial audit found no soundness gap, including the flat
pool and the all-size convexity argument (`encoder_audit/AUDIT.md`). The control program checked
501,024 individual Delta-failure queries against direct sign semantics and
the old encoders with zero discrepancies. Six small CNFs have accepted LRAT
proofs; cap-side negative fixtures produce checked SAT models. These controls
do not extend the universal frontier. See `encoder/CONTROLS.md`.

Three frontier pipelines were launched at about 22:57 KST:

| Unit suffix after `nov13c-vfy-delta3-` | Statement tested | State |
|---|---|---|
| `n6m14` | cup-side (5,6), 14 points | UNKNOWN at 900s |
| `n6m15` | cup-side (5,6), 15 points | SAT after 668.641s; real counterexample certified above |
| `n7m14` | cup-side (5,7), 14 points | UNKNOWN at 900s |

Each uses CPUQuota100%, MemoryMax1800M, MemorySwapMax0, RuntimeMaxSec1250,
AS1300MiB, solver limit900s, and checker heap1100/stack32 with limit300s.
All have `--sym none`, with no orientation assumptions or cubes. Distinct
CPU affinities 29,30,31 were set on their process groups after launch. Source
and binary snapshots match the recorded hashes. Their outputs remain under
`/home/jay/research/data/delta3-codex-20261113/encoder/scheduled-*`.

`search/delta_search.cpp` is an exact integer C++ engine for real configurations,
with an independent geometry recurrence, complete bounded DPLL, lazy witnessed
clauses, and strict separation of UNKNOWN from an exhaustive failure. Its
60 control invocations include known failures of the strong/cap-side/end-only
variants and 36 small hull/subset oracle comparisons. The new 16-point
minimum-size example also gives the independently confirmed optimum five.

One 600-second n=7 adversarial run, seeded with 14 diverse real sets including
that example, started at about 23:04 KST in `nov13c-vfy-delta3-search-n7`.
It uses one CPU, MemoryMax700M, no swap, AS512MiB, and a 630-second unit limit.
Minimum-Delta and private-cup calculations guide the search. Sampling evidence
is HEURISTIC even though individual successful Delta witnesses are exact.
Outputs are in the search scratch directory's `scheduled-n7-701/`.
The run finished with 521,758 mutation proposals, 188,477 newly tested order
types (including invalid configurations), 14,127 accepted moves, and no
counterexample. One final candidate reached the global time limit; a separate
recheck returned a valid Delta in 0.196ms and passed the independent packet
audit (`search/pending-n7-audit/` in scratch). Thus that pending case is resolved.
Statistics are correlated
sampling evidence, not a universal theorem.

After the lattice timeouts, three 300-second trials using the flat containment
pool were scheduled for n=6,7,8 at m=14. The exact initial literal counts are
3,934,603 / 4,160,567 / 3,752,111 respectively. A conservative 200-byte-per-literal
planning estimate remains under the AS1300MiB cap. Each uses the same 1800M
memory reservation and a 750-second outer unit limit; all first-trial results
are preserved. The n=6 and n=7 cases remain UNKNOWN at 300 seconds. The n=8
case was **CERTIFIED**, using 53.564 seconds for CaDiCaL and 8.429 seconds for
cake_lpr. It is an unconditioned theorem for every 14-point signotope, hence
for every real point set at that size. CNF and LRAT hashes are respectively
`a0e37105f825fc655ea76faef691c92b3748d99e654fb86cd101545afc1a1dbc` and
`03e6d69917731b55a4fd2d70255668c4caf8a5c52b9343cf99662ac9c2d8344c`.
The 315,253,167-byte proof remains in scratch. Small records are in
`coordinator/data/frontier/fallback-flat-n8-m14/`.

A further flat n=8,m=15 trial remained UNKNOWN at 300 seconds. Its 11,070,642
literals were planned at up to 250 bytes/literal; AS2800MiB under a fresh
MemoryMax3800M reservation kept the process below 80% of its unit limit. The
sum of all concurrent verifier address-space limits stayed under the shared
6-GB track budget. That reservation was released when the pipeline finished.

Direct **weak** n=7,m=16 and n=8,m=16 lattice trials both remained **UNKNOWN**
at 600 seconds. Each ran with
a 600-second solver limit, 300-second checker limit, AS1300MiB, MemoryMax1800M,
and a 1050-second unit deadline. They test the original conjecture, without
requiring a hit on the cup part. No theorem or counterexample follows from
either timeout. `coordinator/data/frontier_summary.json` records all nine
frontier trials and has an empty pending list.

## Other mathematical findings and the remaining gap

`descent/theory.md` proves that a doubly extendible type-four lower chain forces
one of its two entire helper sets into any transversal of the longest cups.
It also gives a cap-safe exchange under an explicit endpoint hypothesis.
That exchange need not preserve prior coverage: independently checked real
examples on ten points (n=7) and eleven points (n=8) show it can lose an already
hit longest cup. The more flexible one-point exchange E1 remains open and,
even if true, would not by itself handle all missed chains.

`hypergraph/theory.md` proves a satisfiability-preserving clause elimination
rule and a necessary coherent cap-star condition for a counterexample. It
also gives an exact 13-point obstruction to arbitrarily long one-hole repair:
four proper partial colorings form a closed component, despite another valid
full coloring. This refutes that repair strategy, not Delta. Its coordinate
predicates and transition obstruction have an independent exact checker.

`hypergraph/LIFT.md` investigates transferring the new 15-point example to
n=7 or n=8. A written eight-chain contradiction excludes constant-weight
duplication. Two small cake_lpr certificates exclude the specified generic
binary and thin ternary cup-cluster models, with a geometric argument bounding
every convex subset of the clusters. These exclusions concern only those
models; arbitrary lifts remain open, and no n=7 or n=8 counterexample follows.

The point-deletion and one-hole arguments distinguish a fixed lower-chain
hypergraph from the geometric instance after deleting a point: a lower chain
can lose its upper-chain carrier without losing one of its own vertices.
That distinction is retained in all stated lemmas.

The original weak D(5,7) and D(5,8), and their general cup-side forms, remain
open. The n=6 cup-side counterexample invalidates an induction that assumes
that sharpening in every smaller parameter. It does not invalidate the
previous ES(8) ≤ 309 chain or supply a smaller numerical ES bound.

## Files, resources, and continuation

`README.md` gives the statements and outcomes; `VERIFY_DELTA3.md` gives the
independent verification scope. `coordinator/` contains discovery, realization,
direct geometry, deletion, certification, and archival scripts, with small
evidence under `coordinator/data/`. `encoder/` and `search/` contain the C++
engines and their bounded Python drivers. `encoder_audit/`, `a4/`, `descent/`,
and `hypergraph/` contain separately authored arguments and checks. The final
root `SHA256SUMS` covers the retained files. Large CNFs and traces remain under
`/home/jay/research/data/delta3-codex-20261113/` and are identified by the
per-case result JSON and `coordinator/data/archives.json`.

Compressed copies of completed proofs and traces are checked by decompressing
and comparing SHA-256; uncompressed originals are also retained. A SAT or
UNKNOWN trace is explicitly not an UNSAT certificate. No proof directory was
deleted. The repository's research skill, discovered when AGENTS.md appeared
at 23:16 KST, was read; its budgets and evidence rules agree with the owner's
existing instructions. No new permission request was needed.

All long computations are centrally launched as `nov13c-vfy-*` user units.
Existing n66 and fastbb jobs count toward the 16-thread / 24-GB global ceilings;
the verifier track has a shared 6-GB budget under memguard5. No new unit was
stopped for memory during the runs reported above. No cap was increased, no
commit/push/branch change was made, and the root README and math.md were untouched.

Separately, pre-existing background checks finished during this work:
`verify-E2-20261113` accepted its fresh proof at 22:45:28 KST, and
`verify-D1b-20261113` at 22:53:34 KST. Their exact status logs and flag files remain
under `/home/jay/research/data/`. The latter completes the previously pending
independent check for the strong (a,n)=(4,7) case at m=16. Neither completion
proves weak D(5,7) or D(5,8).

To inspect a future continuation without launching work:

```bash
systemctl --user list-units 'nov13c-*' 'memguard*' --state=running --no-pager
/home/jay/research/data/phase2-20261113/cpu_free.sh -v
cat /home/jay/research/data/delta3-codex-20261113/encoder/direct-weak-n7-m16/result.json
cat /home/jay/research/data/delta3-codex-20261113/encoder/direct-weak-n8-m16/result.json
```

Reproduction commands are in `encoder/COMMANDS.md`, `search/README.md`, the
coordinator certification scripts, and the per-case JSON command arrays.
Research units must retain the resource limits and shared-budget accounting.
The guard must remain active while the unrelated n66/fastbb jobs continue.
