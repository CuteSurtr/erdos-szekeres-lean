# STATUS20261121_1930: Linux session of 21 November 2026 from 19:15 KST (handoff, updated as it goes)

**Status: RESUMED 22 Nov 03:48 (owner: "start to research ES and #810 by utilizing all of these"); RUNNING.** Stopped 03:00–03:48 (§6). New caps (owner, about 03:55): memory at most 80 % in use, CPU at most 90 % (§6, "Resumed"). ES(8) ≤ 304 ([ES304N20261119](../ES304N20261119/README.md)) is unchanged. Nothing has been committed, pushed or e-mailed in this session.
03:00:00 and 03:00:05; there was no kernel OOM kill. State at the stop and the resume commands are in §6. ES(8) ≤ 304 ([ES304N20261119](../ES304N20261119/README.md)) is unchanged: the budget-68 checks for 303 were stopped
unfinished. Nothing has been committed, pushed or e-mailed in this session.
- The Mac pushed its own handoff, `STATUS20261121`, on the unmerged branch `origin/es-mac-2026-11-21`. That name and the
  Mac's record names (ES8CHECK20261121, M57R36N20261121, M57R36E20261121, PREFIX20261121) are taken. This Linux page uses a
  time suffix.
- Previous Linux handoff: [STATUS20261120](../STATUS20261120/README.md) (stop of 20 Nov 23:52 and resume commands, §6).

## 1. Owner request (21 Nov ~19:15)

Check GitHub, push further on the ES lower and upper bounds and on Erdős problem #810, use agents freely, "fully utilize
this pc and keep researching until you find something useful". Caps unchanged: 28 of 32 threads, 24 GB for research
jobs (SKILL.md §1).

## 2. GitHub state (fetched 19:10, read-only)

- ES repository: new branch `origin/es-mac-2026-11-21`, 4 Mac commits on top of main 2d1cb6baa (1f084cc62, a4405765c,
  dedc94e62, ee7994318). Merging into main is an open owner decision; main is unchanged.
- #810 repository (`~/research/sat/erdos-810-research`): new remote branches `research/810-overnight-20261121` (last
  commit 7bbe261, 19:00 KST), `research/810-evening-20261120`, `main`, `lean-formalization`. The local working tree is
  on the two-week-old `research-2026-11-07` and is not used.

## 3. What runs (resumed 19:23–19:25 in the layout of STATUS20261120 §6)

| unit | job | note |
|---|---|---|
| `esr-memguard-1121b` + `esv-memguard-1121` | memory guards, 21,000 MB (bal 9500, dlt 7000, n66 17000, r36 8500, ag 3000; log `memguard-20261119.log`) + 3,000 MB (fv 3000) | started before every other unit; `-1121b` replaced `-1121` at about 20:10 to add the r36 and ag tracks |
| `esr-bal-zbs68` | budget-68 tree with the Z*-row → ES(8) ≤ 303 ([ES303N20261120](../ES303N20261120/README.md)) | CPUQuota 1600 %, `taskset -c 5-15,21-31`; resumed with todo 7,817 of 32,755 contexts |
| `esr-n66-drv15` + 4 `esr-n66-c15-*` | N66 level-15 cube campaign → N66 ≤ 54 | driver deadline moved from 23 Nov 12:00 to **24 Nov 08:00** (the stop lasted 19.5 h); the n66 memory track allows 4 cubes |
| `esr-vfy-drv15` | independent check of the level-15 leaves | |
| `esv-fv-drv` + 2 `esv-fv-c-*` | FV304, the Lean check of the 304 tree | resumes after the 379 finished modules |

At 19:27 the anonymous memory was 11.8 GB under the research guard and 1.1 GB under the FV guard, and the CPUs were
69 % busy at nice, with Tctl at 78.5 °C.

No finish time is quoted for b68. The remaining contexts are the tail of the context order, where the cost per context
rises. The block before the stop averaged about 2,800 s of wall time per 1,000 contexts, and its last partial block cost
91 CPU-s per context against about 60 before that (HEURISTIC). After the search come the assembly with `check_tree` and
`balcheck2`; at budget 67 these took 4 and 3.5 minutes.

## 4. Results of this session

| time | result | label | record |
|---|---|---|---|
| 19:55 | Rung N = 36 of the M(5;7) owner model, **case B** (`c36_tle22`): cake_lpr accepted the 13 Nov CaDiCaL 2.1.3 proof (heap 6,000 MB, 176 s; CNF `08b8ea9c…`, LRAT `a0d2cb92…` re-hashed) | **CERTIFIED** (modulo the written arguments of ETV7SAT §2) | [ETV7SAT20261113](../ETV7SAT20261113/README.md) §6.2 update |
| 22 Nov 01:08 | **Budget-68 finder complete**: all 32,755 contexts closed (rc 0). The assembly + check_tree step was stopped cleanly by the memory guard twice (01:09:41 and 01:12:07; one context alone needs > 8 GB in v4). It was re-run from 01:26 with the memory-lean `balz_assemble_v5.py` (controls 27/27 equal, 7/7 negative caught); balcheck2 follows via `chain303.sh` | – (no claim yet) | [ES303N20261120](../ES303N20261120/README.md) §5 |
| 22 Nov 00:40 | **sat_g(6) ≤ 11, sat_g(8) ≤ 26, sat_g(9) ≤ 39** (were 12, 27, 40): explicit saturated sets, five exact implementations agree, including the verifier's own code; cell counts equal the Euler count | **EXACT** (stated coordinates) | [SATG20261118](../SATG20261118/README.md) SAT4 addendum |
| 22 Nov 00:45 | Radius 1 around AE33 is empty at the order-type level: all 203 two-point CNFs UNSAT, a fresh cake_lpr gives one verdict line each, all 223,165,944 clauses checked by own code | **CERTIFIED + PROVED soundness** (unrefereed; support evidence for ES(7) = 33 only) | [LOWERBOUND_RUN_1118](../ROADMAP20261115/LOWERBOUND_RUN_1118.md), claim `lb-l18-e72-ae33` |

#810 results of wave 1 (kept in the work folders under `~/research/data/e810-linux-20261121/`, since #810 has its own
repository; nothing was written there):

- **M(16) ≤ 73, extension step** (B2): all 210 extensions with 74 edges and all 6,435 with 73 edges are UNSAT under
  an own encoder. This is CERTIFIED (CaDiCaL 2.1.3 plus cake_lpr; the verifier stored cake stdout for 6,645/6,645).
  6,615 of them also have a 17-edge conflict clique, which is EXACT. M(16) ≤ 73 itself stays **conditional** on the
  notes' two one-run censuses, F(14,16) ≤ 57 and the uniqueness of the 65-edge optimum.
- **Ten-point and Hamming CNFs** (B1): 125 + 1 CNFs CERTIFIED, at the CNF level only. The encodings and the
  ten-point reduction were not checked independently.
- **t = 34 copies** (A1): for all 7 open shapes, χ_f(C_B) = 901/3 exactly. Hence the price method cannot exclude
  t = 34, and the single-star test passes (EXACT). χ(C_B) = 301 for six shapes; for {0,2,8} it is between 301 and
  306. Whether t_max is 33 or 34 stays open.
- **182-vertex graph** (A2):
  - the proper version with 7 colours is CERTIFIED UNSAT;
  - the fractional value is χ_f = 5 (EXACT);
  - rainbow with 5 colours is **undecided**: 78 of 120 Y1-cubes are CERTIFIED, 1,624 proofs, re-run by the verifier;
  - the reduction to cubes is PROVED.
- **Proof attempts** (F: 1/4 − δ, G: 1/18 − δ): no δ > 0 was found. The lemmas are in the work folders.
  - Several lemmas are conditional on Lean theorems that were not rebuilt here (F Thm 3; G L2, Cor 7, L3(ii), L3(iv)).
  - G L3(iii) carries the graph-limit transfer GAP-S.
  - F Prop. 5 is true only with "at least one edge": the edgeless graph refutes the literal statement.

Case A of rung 36 is still open: 34 cubes, 65/256 of the case-A cube space, according to the Mac's records as of
18:59 (`es_mac_digest.md` §1). M(5;7) ≤ 35 is not established.

## 5. Agents (read-only digests, 19:30)

Outputs in `~/research/data/agents-20261121/`: `es_mac_digest.md` (Mac ES branch: rung-36 open set, ES8CHECK findings),
`e810_digest.md` (#810 overnight branch: frontier and next steps), `lower_digest.md` (what "lower bound" covers here and
what can improve). Agent summaries are not evidence.

### Wave 1 (workflow `research-wave1-1121`, launched about 20:15)

Seven workers. Each positive claim is checked by an independent rebuild (own code) and a soundness review.

| worker | slot (1 thread each) | task | work dir |
|---|---|---|---|
| A | `esr-ag-a810-*`, 700 MB | #810: t = 34 copy count (local colouring of at most 304 classes, or integer prices); 5 colours on the 182-vertex graph | `~/research/data/e810-linux-20261121/a-t34-sat182` |
| B | `esr-ag-b810-*`, 700 MB | #810: re-certify the ten-point and Hamming CNFs with cake_lpr; own-encoder recheck of the 210 + 6,435 extensions behind M(16) ≤ 73 | `…/b-recert-ext16` |
| C | `esr-ag-ae33-*`, 1,000 MB | ES lower side: AE33 radius 1 (203 pairs): hashes, cake_lpr re-run, own clause check, draft record text | `~/research/data/lower-20261121/ae33` |
| D | `esr-ag-satg-*`, 600 MB | sat_g descents (K = 8 below 27, K = 6 below 12, K = 9 below 40) | `…/satg` |
| E | none | prepare rung-36 case A on Linux: all 84 leaves with 2.1.3, no solving | `~/research/data/r36-linux-20261121/caseA` |
| F, G | none | proof attempts: M(n) ≤ (1/4 − δ)n², g(n;7,4) ≤ (1/18 − δ)n² | `…/f-quarter`, `…/g-eighteenth` |

- The agent pool has 4 threads and 3,000 MB (memguard track `ag`, inside the research total of 21,000 MB).
- `agents-20261121/yield_guard.sh` creates `agents-20261121/YIELD` at a Tctl 5-minute average of 87 °C or above, or
  at a research memory total above 19,000 MB. Agents then stop their units.
- Agents write only under `~/research/data/`. The main session applies record edits after it has checked the verdict
  lines and hashes itself.

**Wave 1 finished at 00:32 (22 Nov).** 19 agents ran with no errors. Every claim was confirmed by both verifiers,
except F's Prop. 5, which holds only in the amended form above.
- The memory guard stopped one agent unit cleanly (`esr-ag-a810-combo1`, 703 MB of 700 MB); there was no kernel OOM
  kill.
- E (rung-36 case A preparation) had no verifier stage. Its ported driver (`drive2.py`, which includes a race fix)
  must be reviewed before case A starts.
- Proofs kept: about 12 GB of zstd LRATs under `a-t34-sat182/a2/` and about 330 MB under `b-recert-ext16/`.

### Wave 2 (workflow `research-wave2-1122`, 00:48 to 02:57; stopped by the main session before the 03:00 stop)

Four workers, each meant to be followed by an independent rebuild and a soundness review. Only the driver review
finished. None of the workers' claims below reached the verifier stage: they are agent outputs, not evidence.

- **Rung-36 case-A driver review** (two independent reviewers, both finished; `~/research/data/r36-linux-20261121/caseA/review/REVIEW_drive2_lens1.md`, `…_lens2.md`).
  - Neither found an unsound path for a single driver instance.
  - Lens 2's verdict: **not ready to launch as is**. Before launch: RF1 (a lock against a second driver on the same
    directory), RF2 (atomic cube write), RF3a (record the solver identity), RF4 (an esr-total check). Before the
    CERTIFIED label: RF3b, a solver check in `cover.py --final`. RF3b can be added after the run because the per-cube
    logs are kept.
  - Lens 1: `cover.py --final` never checks "CaDiCaL 2.1.3, exit 20", and the README §8.4 recovery edits statuses by hand.
- **182-vertex graph, rainbow with 5 colours** (A2). The agent's `a2/campaign_status.py` (run by the main session at
  03:05) prints:
  - 118 of 120 Y1-cubes refuted: 84 directly, 34 via 120 sub-cubes each;
  - cube 118 is partly done (115 of 120 sub-cubes); cube 119 is open.
  - Undecided. Wave 1's verifier re-ran the proofs of the first 78 cubes only, so cubes 78–117 still need an
    independent re-check.
- **M(16) ≥ 72 and factor checks** (`~/research/data/e810-linux-20261121/m16-72/README.md`; the agent marked it "DONE" at 02:45).
  - The agent reports exact factor-level checks of the notes' 32,768-vertex and 226,981-vertex constructions.
  - No 16-vertex 72-edge witness among 1,816,353 candidates (HEURISTIC negative).
  - "Every 72-edge example has minimum degree ≥ 8": COMPUTED, conditional on the notes' two one-run censuses.
  - Not verified independently.
- **sat_g descents** (`~/research/data/lower-20261121/satg2/README.md`): no new bound (HEURISTIC finder runs only).
  - K = 8: stuck at 2 failing cells at 25 points.
  - K = 10: 51 points with 2 failing cells (`seeds/k10u_best_n51.txt`).
  - Exhaustive one-point relocation repairs neither (COMPUTED by the finder).

## 6. Resume

### Resumed 22 Nov 03:48 (owner: research ES and #810 with the new tools; fully use the PC)

- **Caps (owner, about 03:55):** memory at most 80 % in use (48.7 GB of 60.9 GB), CPU at most 90 % (28 threads). With
  about 8–10 GB used by the desktop, the guards are `esr-memguard-1122` (`esr 34000 bal=9500 dlt=7000 n66=23500 r36=8500
  ag=5000`) and `esv-memguard-1122` (`esv 6000 fv=6000`). They were started before the old 21,000 / 3,000 MB guards were
  stopped. SKILL.md §1, AGENTS.md and memory `caps-80-90-20261122` record the new caps.
- **Restarted:**
  - b68 v5 assembly with a fresh marker (03:48:48), then `chain303.sh` (balcheck2). Same SHA and parameters as in §6.
  - The L15 driver: 7 slots, `C15_RES_MB=3300` (observed cube peaks ≤ 2.7 GB), `C15_CPU_CAP_MILLI=24500`.
  - vfy15.
  - FV304: `FV_JOBS=6`, `FV_MEM=5500`. FV_MEM is the total over all FV jobs, not a per-job limit.
- **Restart race (fixed at 03:56).** The old L15 driver launched `ohooho_40o` seconds before its restart. The new
  instance then marked that cube `failed` while its unit ran. Fix: driver stopped, unit stopped, cube set back to
  `queued` with a note, partials renamed `.stopped-20261122b`, driver restarted.
  - Lesson: stop the drivers BEFORE changing the guards.
  - The FV driver had the same clash. It was harmless: the old units finished with rc 0 and their oleans exist.
- **182-vertex graph, 5 colours: the campaign finished at 03:57.** Its own `campaign_status.py` reports 120 of 120
  Y1-cubes refuted (84 directly, 36 through 120 sub-cubes each). **Not a claim yet**: about 2,900 pieces (cubes 78–119)
  have no independent re-check. Wave 3's `v182-recheck` does that re-check.
- **Wave 3** (workflow `research-wave3-1122`, launched about 04:00; 5 workers, each followed by verifiers):
  - `v182-recheck`: independent re-check of the 182-vertex campaign;
  - `m16-premises`: SMS and nauty second routes for P1 = F(14,16) ≤ 57 and P2 = the unique 65-edge support, with census
    controls;
  - `m16-le72-encoder`: forced-structure encoder for M(16) ≤ 72, with 4 positive controls; no run longer than 60 min;
  - `r36-fixes`: RF1–RF4 and RF3b, then an adversarial re-review;
  - `bal2-assure`: sanitizers, clang-tidy and bounded model checking of balcheck2; production binary untouched.
- **Tools:** the owner's installs are checked (`~/research/data/agents-20261121/tools-20261122.md`).
- **Cleanup** (owner-approved, each item checked first; manifest `~/research/data/cleanup-20261122/manifest.txt`):
  - Deleted:
    - the stopped L15 partials `p2/c15/*.stopped-2026112*` (60.1 GB by per-entry du; no certified cube's
      certdir is among them);
    - the two Delta partials (28.6 GB; "not a proof");
    - Lean toolchains 4.35.0 and 4.36.0 (elan's default is now 4.24.0; nothing pins 4.35 or 4.36);
    - `esbmc-v8.7.zip`.
  - `df`: 962 GB → 897 GB used.
  - Not deleted: `~/.cache/uv`. The running uvx MCP servers use it. A `uv cache clean` was started by mistake; it
    blocked on their lock and was stopped before it removed anything.
  - **Not deleted, and must be kept: `~/research/data/es308-20261114/runs`.** The owner approved it as superseded
    307/308 evidence, but the check found that ES(8) ≤ 304, and the pending 303 and 302, use **ResidualBound 118**
    from ES307N20261118. Its slice trees (L10/L11: `runs/b35s18`–`b35s20`) live there.

### Formalization decisions (owner, 22 Nov 04:45-06:00)

- **Goal: full Lean formalization of every result that is worth it**, before any cleanup of the machine.
  - The keep-set stays on this disk; the running jobs finish; the cleanup scope is not decided yet.
  - SAT-certificate parts aim at **Lean + cake_lpr**: each encoding is formalized in Lean (the ENCBLEAN pattern), and
    cake_lpr's verdicts are the one trusted step. Lean uses the standard axioms only.
  - The owner approved a commit and push of these records.
- **Inventory:** `LEAN_STATUS_20261122.md` (this folder) is the Lean-status agent's map of the 30x chains, with a
  correction of its 303/302 cost figures. The ledger workflow `ledger-1122` is still mapping every record and data
  folder.
- **Formalization wave 1** (`formalize-wave1-1122`, about 05:50):
  - an audited rebuild of the nine 30x composition files into one olean directory, with an import-closure check and
    `#print axioms` (including `composition_303_zzsf` on Linux);
  - `ResidualBound 118` as a Lean theorem modulo explicit slice and row hypotheses (Lemma A, h(F) ≥ 18, gluing).
  - Each item has a statement-fidelity reviewer. No Lake build runs in the repo, because FV304 depends on hash-pinned
    oleans.
- **Preserved in git:** the 14 hash-pinned inputs of the 304/303 tree checks that existed only on disk (LEAN_STATUS
  finding 10). They are rows, zrow.json, assemblers, run scripts, and the balcheck/balcheck2 sources and binaries.
  They were copied into `ES305N20261119/{tools,data}` and `ES303N20261120/data`; every copy matches its record pin
  (`data/PRESERVED_20261122.tsv`).
- **182-vertex graph:** wave 3's `v182-recheck` reports every one of the 4,404 pieces independently accepted (04:35).
  Its rebuild and soundness verifiers are still running, so this is not filed as a result yet.

### Stopped 22 Nov 03:00 (owner: "stop at 3 o clock")

At 02:57 the main session stopped the wave-2 workflow. At 03:00:00 the timer unit `stop0300-research` ran
`~/research/data/agents-20261121/stop0300.sh`. It stopped the drivers, then the job units, then the two guards; by
03:00:05 no `esr-*` or `esv-*` unit was left, and there was no kernel OOM line (log `agents-20261121/stop0300.log`).

- **b68 (ES(8) ≤ 303).**
  - The finder is complete (01:08, rc 0).
  - The v5 assembly + check_tree was stopped after it had written 12,168 of the 32,765 files: all 2,007 big
    contexts, which run first, and part of the small ones. It had run 93.5 minutes. It writes no summary until the
    end, so **no check result exists**.
  - v5 has no resume. Re-run it from the start with a fresh marker, then chain303 (commands below). balcheck2 never
    started. The acceptance values pre-registered in ES303N20261120 §5 stay as they are.
- **L15 campaign (N66 ≤ 54).**
  - 63 certified (51 at the 20 Nov stop; the last one, `ohoooo_40h`, at 02:43), 34 split, 35 queued. The leaf
    cover holds over 98 leaves; the certified cover is not complete.
  - The 4 cubes running at the stop (`ooohho_40o`, `oohoho_40o`, `oohhoo_40o`, `ooohoo_40h_52h`) were set back to
    `queued` with a `requeued` note. Their partial files were renamed `p2/c15/<id>*.stopped-20261122`; nothing was
    certified there.
  - Copy of the status before the stop: `campaign_status.before-stop-20261122.json`.
  - The driver deadline is 24 Nov 08:00; move it if the stop lasts long.
- **Verifier (`vfy15`):** up to date at the stop. The last certified leaf (`ohoooo_40h`) passed cake and sub at 02:48,
  both rc 0.
- **FV304:** 1,280 of 8,192 modules done, none failed (status 02:59:56). The two compiles running at the stop left no
  olean. The driver skips finished modules.
- **Agents:**
  - Wave 2 is stopped (§5).
  - The stop script created `agents-20261121/YIELD`. Delete it before agent units run again.
  - Rung-36 case A has not started; RF1–RF4 of the driver review (§5) come first.

Restart order: the guards first, then the b68 checks, the campaign driver, the verifier, FV.

```bash
# memory guards (start before any unit of their prefix)
systemd-run --user --unit=esr-memguard-1121b -p CPUQuota=30% -p MemoryMax=200M -p MemorySwapMax=0 --nice=5 \
  -E LOG=/home/jay/research/data/memguard-20261119.log \
  /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/memguard.sh esr 21000 bal=9500 dlt=7000 n66=17000 r36=8500 ag=3000
systemd-run --user --unit=esv-memguard-1121 -p CPUQuota=20% -p MemoryMax=200M -p MemorySwapMax=0 --nice=5 \
  -E LOG=/home/jay/research/data/memguard-20261119.log \
  /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/memguard.sh esv 3000 fv=3000
# b68 checks: v5 assembly + check_tree from the start, then chain303 (waits for the assembly unit, then starts balcheck2)
cd /home/jay/research/data/bal186-20261119/zrow
date '+%F %T' > b68zs/asm_v5_start.txt     # fresh marker: chain303 rejects any file older than it
echo "$(date '+%F %T') start assemble (v5 sha 964b00007e5b..., re-run after the 22 Nov 03:00 stop)" >> b68zs/steps.log
systemd-run --user --unit=esr-bal-zbs68asm -p CPUQuota=1000% -p MemoryMax=8G -p MemorySwapMax=0 -p RuntimeMaxSec=21600 \
  --nice=10 --working-directory=$PWD -E NW_BIG=3 -E BIG_BYTES=10000000 -E SUB_NODES=30000 /usr/bin/taskset -c 5-14 \
  bash -c 'O=/home/jay/research/data/bal186-20261119/zrow/b68zs; python3 -I balz_assemble_v5.py 68 $O/occ - $O/files 10 > $O/assemble.out 2>&1; rc=$?; echo "$(date "+%F %T") assemble+check_tree (v5) rc=$rc $(tail -c 700 $O/assemble.out)" >> $O/steps.log; exit $rc'
systemctl --user is-active -q esr-bal-zbs68asm && systemd-run --user --unit=esr-bal-chain303 -p CPUQuota=10% \
  -p MemoryMax=200M -p MemorySwapMax=0 -p RuntimeMaxSec=28800 --nice=10 --working-directory=$PWD ./chain303.sh
# L15 campaign driver (state in p2/c15/campaign_status.json; move the deadline if needed)
cd /home/jay/research/data/n66-20261113
systemd-run --user --unit=esr-n66-drv15 -p CPUQuota=6% -p MemoryMax=300M -p MemorySwapMax=0 --nice=10 \
  --working-directory=$PWD -E C15_DEADLINE_DAY=24 -E C15_DEADLINE_HM=08:00 -E C15_SLOTS=5 -E C15_RES_MB=3800 \
  -E C15_CPU_CAP_MILLI=27500 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u p2c15_driver.py
# verifier
systemd-run --user --unit=esr-vfy-drv15 -p CPUQuota=5% -p MemoryMax=200M -p MemorySwapMax=0 --nice=10 \
  --working-directory=/home/jay/research/data/n66-20261113/vfy15 /bin/bash /home/jay/research/data/n66-20261113/vfy15/bin/driver15.sh
# FV304 driver (resumable)
systemd-run --user --unit=esv-fv-drv -p CPUQuota=20% -p MemoryMax=300M -p MemorySwapMax=0 -p RuntimeMaxSec=432000 \
  --nice=10 --working-directory=/home/jay/research/data/fv304-20261120 -E FV_JOBS=2 -E FV_MEM=2800 -E FV_TMAX=90 \
  taskset -c 5-15,21-31 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u \
  /home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05/drive_es304z.py
```

Tools: the owner finished the installs at about 03:10 (kissat, drat-trim, SMS, march_cu, z3, cvc5, cbmc, esbmc, ethos,
cryptominisat, nauty 2.8.9 from source, and the Mathlib cache of the #810 Lean project). Versions, hashes and three passing smoke tests are in
`~/research/data/agents-20261121/tools-20261122.md`; es-research SKILL.md §5 lists them.

Open owner questions (unchanged): may main be fast-forwarded to `es-mac-2026-11-21`; deletion of the kept wave-1
proofs (about 12 GB under `a-t34-sat182/a2/`, about 330 MB under `b-recert-ext16/`) once they are re-checked;
whether the Mac session still runs.
