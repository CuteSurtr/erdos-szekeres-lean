# Resource accounting and retained incidents

The owner caps all research at 16 CPU threads and 24 GB combined research
memory. The verifier track is limited to 6000 MiB of anonymous resident
memory plus swap. Long jobs use `nov13c-vfy-*` user units with CPUQuota,
MemoryMax, MemorySwapMax=0 and finite RuntimeMaxSec. The existing shared
guard is kept active while any research remains.

## Important qualification about earlier file-cache peaks

The 04:55 envelope unit requested MemoryMax1000M, but its completed
systemd journal reports **1000.2M total cgroup memory peak**. Its solver
anonymous memory was small; output file cache accounted for the discrepancy.
The first two terminal sweeps also reached approximately their nominal
1600 MiB watermarks through proof-file cache (journal reports 1.5G peaks).
These were not proof-checker anonymous-memory spikes. This record does
**not** claim that every nominal MemoryMax watermark was respected.

The pre-existing guard lifts kernel `memory.max` to avoid kernel OOM and
retains the requested value in `memory.high`, enforcing anonymous memory
budgets by clean process termination. Thus its protection does not itself
prevent a file-cache watermark crossing. The relevant journal and guard
records report no OOM or guard STOP for these delta6 jobs; no swap was
observed. That limited evidence is distinguished from a universal claim
about all activity on the machine.

The parent added explicit file sync and advisory release of completed
proof prefixes. Every subsequent long solver uses binary LRAT, releases
old proof cache every ten seconds while retaining a 32 MiB writing tail,
and streams hashes with cache release every 64 MiB. Raw and compressed
proofs are both retained and their compression roundtrip is checked.
The independent size-13 replay additionally monitored cgroup memory and
released proof-input cache once per second. Its actual peak was about
709 MiB against MemoryMax1200M, with zero swap.

## Current reservation at 06:28 KST

| Work | CPU ceiling | Process or RSS reservation | Nominal MemoryMax | Runtime |
|---|---:|---:|---:|---:|
| Original terminal n7/m14 | 1 | AS900 MiB | 1200 MiB | 6600 s |
| Cup-support n7/m15 | 1 | AS900 MiB | 1200 MiB | 6600 s |
| Conditional indecomposable terminal n7/m14 | 1 | AS800 MiB | 1100 MiB | 6600 s |
| Endpoint-sign protection n7/m16 | 1 | AS800 MiB | 1100 MiB | 4800 s |
| Lean geometry, sequential probes | 1 | RSS1300 MiB, AS4 GiB | short CLI guard | 27 s/probe |
| Independent audit, sequential probes | 1 | AS300 MiB | short CLI cap | 20 s/probe |
| Written-theory controls | 1 | AS400 MiB | short CLI cap | 20 s/probe |
| Parent short controls | 1 | AS300 MiB | short CLI cap | bounded individually |

The conservative working reservations sum to 5700 MiB, leaving room for
small driver overhead within the 6000 MiB verifier budget. AS is a virtual
address-space ceiling, not a claim of actual resident use. Lean's larger
virtual ceiling accommodates shared read-only library mappings; its
independent RSS and swap guard remains active. CPU ceilings total eight,
usually four live solvers plus fewer short checks. No unrelated research
unit was active at the 06:25 snapshot.

The m16 estimate used 1,368,917 literals at the policy's 150–250 bytes per
literal estimate (roughly 196–327 MiB), plus variable tables and solver
buffers, under AS800 MiB and nominal MemoryMax1100M. This search is a
bounded experiment, with no result claim before certification and audit.

## Other retained development failures

Earlier Lean probes exhausted lower address-space ceilings or were
cleanly stopped by their own 900/950 MiB RSS guards. Their logs remain in
the Lean packet. The later shared 1300 MiB RSS reservation was allocated
only after solver slots became free; it did not raise the owner's caps.
All six finished Lean sources subsequently passed independent parent
replays without a guard stop.

Two short R figure attempts failed under AS300 MiB: OpenBLAS allocation,
then a fontconfig worker-thread allocation. After fixing thread/arena
settings, a bounded unit with AS600 MiB and MemoryMax500M rendered the
figure at 68 MiB peak and zero swap. No proof relied on those attempts.

The isolated wrong determinant expression in a discarded shell probe is
retained in `data/failed_quick_cup_check.json`; the main geometry code and
proof artifacts did not use it. No failed search, timeout, rejected
checker output or heuristic status is promoted to mathematical evidence.

## Monitoring and shutdown

[snapshot_resources.py](snapshot_resources.py) appends read-only live
cgroup evidence to `data/resource-snapshots.jsonl`, including actual
anonymous/cache memory, swap, pressure, CPU quota and OOM counters.
Disappeared historical cgroups are explicitly outside those snapshots.
Long proof files stay in the scratch tree. They will not be deleted
without the owner's agreement.

The parent will stop starting long work by 08:20, finish archiving by
08:35, and report at the requested 08:40 KST deadline. Once **all** research
units, including unrelated ones, have finished, stop `memguard5-20261113`
and `p2-watch-d1b` as instructed. Until then the guard stays active.

## Reallocation at 07:10 KST

The original14 search finished UNKNOWN, cup15 and forced16 finished SAT,
and the low14 formula finished UNSAT with an initial cake128 heap
exhaustion. The unchanged proof subsequently passed cake450 in27.155s
under AS700 and MemoryMax1000M; the failed128 log is retained. The
forced16 first realization batch found no exact witness in100000 trials;
no nonrealizability conclusion follows. Cup15 realization and simplification
finished at about75MiB RSS. An accidentally launched `--help` unit did
no research computation and exited; the correctly bounded simplification
used a separate named unit.

The written-theory worker released its400MiB reservation. The real Lean
bridge received2000MiB RSS only after older solvers completed, within the
same6000MiB owner budget. Its failed1300 import is retained; file-backed
imports caused the excess and the process was stopped cleanly. The
successful minimal import path uses about1.9GiB RSS, AS4GiB, one thread;
no larger owner cap was requested or used.

Active conservative reservations: high-split14 AS800, low-left15 AS800,
all-cuts14 AS700, Lean2000RSS, independent formula auditAS300,
independent metric auditAS400, independent realizationAS600, and parent
short controlsAS150: **5750MiB plus small driver overhead**. Before the
all-cuts unit started, the parent fixed-cup geometry probe used AS300MiB
and its tiny proof run used AS150MiB. Subsequent parent controls stay
within the150MiB reservation. Auditors coordinate brief compilation peaks separately.
CPU ceilings total eight, below16. Actual07:05 research-unit anon memory
was about281MiB, swap0; short CLI work is accounted by reservation and
its per-command resource receipts rather than the unit-only snapshot.

The all-cuts14 unit uses CPU100%, MemoryMax1000M, Swap0, Runtime3900s,
solver2700s and cake360s, with AS700 and heap450. Its roughly600000
literals plus solver buffers fit that reservation by the policy estimate.
It remains conditional on all written and finite dependencies listed in
`allcuts14/README.md`; a running search is not mathematical evidence.

## Reallocation and completed checks at 07:44 KST

The real15 Lean bridge passed a fresh parent replay (six modules,31 axiom
reports; peak1,973,880KiB). The real12 obstruction passed14 finite modules
(32 reports, peak621,268KiB) and5 real modules (27 reports,
peak1,959,500KiB). Their2000MiB RSS reservation is now released.

The left15 proof exhausted checker heaps550 and900 without acceptance.
The unchanged proof passed a separately allocated1400MiB heap under
AS1650, nominal MemoryMax2200M, Swap0. The independent replay then also
passed in73.805s, peak1,436,788KiB, cgroup peak1,531,453,440bytes, swap0.
The temporary replay reservation is released; failed checker logs remain.
The two direct n6 cases and independent cake128 replays were small and
ran sequentially within the existing300MiB audit slot.

The forced16 realization worker released its600MiB allocation after
finding an exact algebraic nonrealizability certificate. Its earlier
nonlinear search was manually stopped, and a Z3 probe returned unknown;
these are not guard stops or proof evidence. Independent exact recovery
and replay were small. The parent's third replay used AS150MiB.

Four solvers currently reserve AS800 (high-cut14), AS700 (all-cuts14),
AS800 (left16), and AS700 (no-six-cup14). Each has one CPU and no swap.
The latter two have2700s/1500s solver deadlines respectively and finite
unit deadlines. The explicit no-six-cup condition is retained in every
claim about that run. Independent formula work reserves300MiB, written
consequences150MiB, and the parent150MiB. A new algebraic Lean sidecar
uses at most500MiB for short probes; it is held to150MiB during the
upcoming larger capacity replay. These are allocations inside the same
6000MiB verifier cap, not increased owner caps.

After the high-cut14 unit ends, the parent plans a sequential capacity
Lean check at RSS3000MiB, AS6GiB, CPU100%, nominal MemoryMax4000M, Swap0,
Runtime240s. It replaces the parent's short slot. The other three solver
reservations sum to2200MiB; the300/150/150MiB audit/theory/algebra slots
leave200MiB for drivers within6000. Each Lean child has a27-second
CPU/wall deadline and10ms RSS/swap sampling. This check has not run at
the time of this entry. No overlapping additional solver is authorized.

The07:41 live-unit snapshot records about795MB anonymous research memory,
989MB including file cache, and zero swap. Short CLI checks remain
separately budgeted; these unit-only measurements do not cover historical
jobs or unrelated desktop applications.

### Clean capacity stop and another cache watermark, 07:47

The capacity child stopped itself at its3000MiB RSS guard after2.598s,
with225916KiB anonymous and2853840KiB file-backed RSS at the sampled peak.
There was no swap, kernel OOM, Lean diagnostic or checked theorem. The
3000MiB reservation was released. The original source and failed receipt
are retained in low_split/capacity_checks/attempt-rss3000. A larger
temporary share may be used only after other solver reservations finish;
the shared6000MiB cap remains unchanged.

During high-cut14 proof compression the cgroup cache reached a total peak
of1154158592bytes, slightly above its nominal1100MiB watermark. Anonymous
use remained small; the manual advisory release at07:46:17 dropped current
memory to about109MB, then43MB, with zero swap observed. This is another
nominal file-cache watermark incident, not a successful claim of staying
below every nominal cap. The original driver is preserved unchanged. A
new run_binary_cache.py releases cache every2s during solving and0.25s
during proof checking/compression, instead of every10s. Future runs use
that revised driver. No proof file was deleted or modified by cache release.

### Protection during the final proof-archiving phases

A dedicated bounded cache watcher starts07:49:31. It uses AS40MiB,
CPUQuota5%, nominal MemoryMax80M, Swap0, Runtime2460s, and only watches
the three remaining old solvers and the planned long-cup16 unit. At55%
of each nominal watermark it syncs and releases old proof-file cache,
retaining a32MiB writing tail. It never deletes or truncates files.
Source archive_cache_watch.py and data/cache-watch.jsonl retain its
behavior. Observed initial current memory was about5.7MB. This watcher
will be stopped explicitly during final shutdown.

The revised capacity driver accepts an explicit RSS guard; its previous
3000MiB version is preserved with the failed receipt. A4500MiB retry is
planned after both700MiB14-point searches finish. During that short check
the regular independent audit slot is reduced to150MiB and the algebra
track stays at150MiB. With left16AS800, theory150, cache watcher40 and
small drivers, the reservations remain below6000MiB. Nominal MemoryMax
for the capacity unit is6000M, so its4500MiB RSS limit is75% of that value.
No new search overlaps this larger check.

## Capacity success and final left16 proof check, 08:01

Capacity16 and Capacity11 both passed at07:54:09, all five standard-only
axiom reports. Total2.890s; maximum sampled RSS3,111,920KiB, swap0.
The4500MiB allocation was released. The generic product/GP Lean packet
also passed its fresh five-module/29-report parent replay under the480MiB
RSS guard,1.090s and382808KiB maximum child RSS.

The original left16 solver returned UNSAT at2648.668s, producing a
4,724,116,807-byte binary LRAT. Its550MiB checker exhausted its heap after
29.009s; this is not acceptance. The finished run retained both raw and
compressed proof and verified their compression roundtrip. The independent
new instance audit separately reconstructs all903593 original base rows.

A parent proof replay began08:00:42: heap2800MiB, AS3100MiB, nominal
MemoryMax4000M, CPU100%, Swap0, checker540s and Runtime660s. Its proof
cache is released every0.25s and hashes are checked before and after.
During this check the independent auditor and algebra worker each hold
only150MiB for reading/preparation; the written worker also has150MiB.
The two diversity searches each reserveAS1000, the parent short slot150,
and the watcher40, totaling5740MiB plus small drivers, within6000MiB.
The old800MiB left16 unit ended before the replay began. No owner cap
was raised. If the proof passes, redundant searches will be stopped and
the same checker allocation transferred to independent replay.

The second diversity search uses the identical audited augmented CNF,
CaDiCaL --unsat --seed=713, solver900s, cake180s/heap650, AS1000,
MemoryMax1400M, Swap0, Runtime1800s; it began07:57:43. The default
variant began07:54:55 with1200s solver budget. Both use the new frequent
cache-release drivers. Their outcomes remain separate from the original
left16 proof, and a running/UNKNOWN result supplies no theorem.

The earlier152.596-second Z3 stage was confirmed in the user journal as
nov13c-vfy-delta6-realize16-independent, started07:17:15. It was a bounded
unit, not an untracked long shell job. Its unknown response is not proof
evidence. This resolves the resource-accounting uncertainty about that
retained exploratory stage.

## Accepted left16 proof and retained monitor failure, 08:15

The parent2800MiB proof check accepted with unchanged hashes in205.490s.
The redundant long-cup solvers received SIGINT in their own cgroups at
08:05:34; their wrappers completed UNKNOWN receipts and compression
roundtrips. CONTROLLED_STOP.json explicitly records the reason. This was
a deliberate stop after certification of the original formula, not a
resource failure or proof rejection. Their reservations are released.

The first independent left16 checker also printed exactly s VERIFIED UNSAT,
but optional /proc child-IO sampling raised PermissionError during process
exit before the final receipt/posthash stage. The parent detected the
missing receipt, and the independent worker retained the complete attempt
and started a clean retry in a fresh directory. The optional telemetry
handler now tolerates an exiting inaccessible process; proof-file access,
all hashes, the memory guard and checker arguments are unchanged. The
independent completion claim remains pending until that clean receipt.

The finite Lean instance worker received the coordinated1000MiB slot
(RSS950, AS3GiB, heap500, unitMM1300, CPU100%, Swap0). Rows were split
from16 to4 and then2 per kernel decision block after clean local RSS
stops. All failed logs are retained. Two short probes briefly overlapped
for less than a second before the worker corrected its sequential waiting;
their combined measured peaks remained inside the shared verifier budget.
No broader claim of zero probe overlap is made. The final sequential
run reports338 modules passed; fresh parent replay remains separate.

The four-family14 search began08:07:32, AS700/MM1000, one CPU, Swap0,
solver720s/cake360s, Runtime1560s. Its added all-cap lemma has now passed
written review and68 exact selector controls, independently replayed by
the parent. Formula/proof audits remain separate. With the3100MiB
independent checker,1000MiB Lean slot,150MiB theory/parent slots and40MiB
watcher, conservative reservations are about5140MiB plus small drivers.

## Final verification and shutdown, 08:28

The clean independent left16 retry completed08:17:29 with exact cake
acceptance and all before/after hashes stable. Its checker took134.537s,
peak process RSS2870348KiB, cgroup peak3010473984bytes and swap0.
The failed optional-telemetry attempt remains separate; the clean retry
supplies the completed independent proof receipt. Its3100MiB reservation
was released before final packaging.

The fresh parent fixed-certificate Lean replay ran in
nov13c-vfy-delta6-f16-instance-parent from08:17:08, under the released
worker's1000MiB slot, RSS950, AS3GiB, heap500, MM1300, one CPU and Swap0.
All338 modules passed; successful child times sum169.426s, maximum
process RSS763884KiB. Parent collection independently matches all354
exact axiom lists and every literal certificate/sign-table entry. Its
initial manifest-schema assertion was corrected in the collector only;
the fresh Lean sources, checks and receipts did not change.

The final four-cut14 solver reached UNKNOWN at720.110s; total including
archiving729.813s. Its raw1490790481-byte partial trace and914343064-byte
compressed file are both retained, with roundtrip verified. No proof
acceptance is claimed. The independent48-clause audit passed and froze;
its earlier short control CPU-limit stop is retained in that packet.

At08:28 all solver/checker jobs and worker allocations were complete.
The last auditor confirmed no owned units active and was closed. The
parent stopped the cache watcher, verified zero running nov13c-/p2-
units, then stopped memguard5-20261113 and requested the instructed stop
of p2-watch-d1b, which was already unloaded/inactive. All three monitors
report inactive/dead. The system-wide swap counter was630784bytes; this
is distinct from the zero process/cgroup swap recorded by the checks.
[data/final-shutdown.json](data/final-shutdown.json) records exact time,
monitor states, free memory and branch. No further long computation is
scheduled in this pass. Only bounded metadata/integrity checks and written
integration remain before the requested08:40 report. Historical failed
unit records and all proof/development artifacts were left intact.

One final independent rooted-lemma control ran after shutdown as a bounded
short command: AS150MiB, affinity4, CPU18/19 and wall20s. It took0.268s,
peak RSS16228KiB and launched no background work. This checked the new
written lemma rather than repeating completed proof replays. No monitor
restart or long-job allocation was needed.
