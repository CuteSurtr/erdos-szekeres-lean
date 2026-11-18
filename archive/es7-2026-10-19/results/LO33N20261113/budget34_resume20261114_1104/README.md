# Budget34 slice20 refinement — 68 old branches eliminated; partial exact replay

Owner-authorized ten-minute continuation,14 November2026,11:04:21–11:14:21
KST. No improved ES bound is claimed. The earlier budget34 packet is frozen.

Target the remaining F64/Lo56 population case. The exact finite model is
unchanged:154 Boolean holes, state0 occupied, budget34,2,650 base rows,
capacity rows F20/Lo14,971 independently certified coupled rows. Prior
work checked1,222 closed contexts out of4,064 and left2,842 unresolved.

This pass creates a successor packet in
/home/jay/research/data/es308-resume-20261114-1104. Only the three small
master/context definition files are copied; the1,222 immutable completed
context files are hardlinked. The source packet remains unchanged.

The same pinned C++ finder refines each open context by one branching
level (`--split-open=1`) before searching. The per-context cap remains
50,000 nodes. Independent verification must establish the new frontier,
unchanged old paths and row prefixes before transferring previous replay
receipts, and must exactly check all newly closed subtrees.

Resources: no jobs running on entry,16 threads available. Finder12 CPUs,
childAS1400MiB plus supervisor150MiB, RSS stop1200MiB, nominal MemoryMax
2000MiB, swap0,300s native search, absolute stop11:11:20 and finite unit
deadline. Independent auditor1 CPU/aggregateAS1200MiB, nominal MemoryMax
1600MiB, swap0, completion before11:13:50. Combined reservations remain
under the6000MiB verifier budget and16-CPU/24GB global limits. The usual
memguard5 monitor runs throughout and is stopped after all research jobs.

Input/binary/master hashes are in data/preparation.json. The frozen
previous [result](../budget34/README.md) and
[independent audit](../budget34/audit/final-audit.json) supply prior
evidence. No certificate is reclassified from a solver status. No git,
external message, installation, deletion or cap increase is authorized.

## Search outcome

The main finder stopped cleanly at11:11:20 by its absolute deadline
(SIGTERM exit-15, an intentional stop). Its sampled peak RSS was367,752KiB;
observed swap and OOM counters were zero. No witness was reported.

Refinement replaced2,842 open parent contexts by5,635 smaller contexts,
leaving6,857 total frontier contexts including the1,222 previously closed
ones. A separate bounded two-thread probe searched IDs8000..8199 and saved
99 subtrees. These were imported only after identical master and context
definitions were checked, using exclusive hardlinks without overwrites.
The main finder saved287 new subtrees, giving386 new saved subtrees and
1,608 total saved context files.5,249 refined contexts have no saved proof.

These counts describe the finder output. The increase in frontier size is
caused by subdivision; it does not measure additional mathematical cases
or proof effort. Until independent verification finishes, no new exact
exclusion is claimed. ES(8)<=309 remains the established project bound;
ES(8)<=308 remains open. The earlier frozen result and proof packet are
unchanged. Commands, receipts, resource observations and successor hashes
are retained in data/ and the new work directory.

## Final independent check,11:13:27 KST

The auditor verified the refined master, all old paths and row prefixes,
and carried the1,222 prior checked subtrees only after matching their
actual hashes.132 of386 new saved subtrees received fresh exact replay;
254 saved subtrees remain unchecked. All checked margins are at least1.
Of the original2,842 open roots,68 are now completely discharged,
including4 closed in the refined master;2,774 remain unresolved.

The refined frontier has5,503 unchecked/open contexts, comprising5,249
without saved files and254 saved files awaiting replay. The global pending
count5,504 also includes state0missing. This is PARTIAL EXACT REPLAY,
not a full exclusion. See audit/refinement.json, audit/summary.json and
audit/finished.json. The final audited partial tree has12,686,925 nodes
and6,343,463 leaves including pending branches. All inherited input hashes
remained stable. Search, audit and memory-guard units were stopped before
the owner's ten-minute deadline. No commit or branch change was made.
