"""Draft PROGRESS.md of the N66 level-14 cube campaign at the 09:40 KST stop (15 Nov 2026) from the final campaign_status.json,
chk.py's re-check (CHK.json), the user journal (systemd CPU accounting per unit) and the memguard log.  Glue only.
usage: prog.py CHK.json OUT.md RESUME.md   (RESUME.md: hand-written section 10, appended verbatim)"""
import json, os, re, subprocess, sys, glob, time, itertools

W = '/home/jay/research/data/n66-20261113'
STATUS = os.environ.get('N66_STATUS', W + '/p2/c14/campaign_status.json')   # the same file chk.py read
MGLOG = '/home/jay/research/data/es308-20261114/memguard-s18.log'
chkf, outf, resumef = sys.argv[1:4]
st = json.load(open(STATUS)); ck = json.load(open(chkf))
C = st['cubes']; R = ck['cubes']; cov = ck['cover']
assert ck['status_updated'] == st['updated'], (ck['status_updated'], st['updated'])   # re-check ran on this exact status file

def prio(c): return (0 if c['id'] == 'hhhhhh' else 1 if c['up_refuted'] else 2, -c['holes'], c['depth'], c['seq'])
def dur(s):
    return sum(float(v) * {'d': 86400, 'h': 3600, 'min': 60, 's': 1, 'ms': 1e-3, 'us': 1e-6}[u] for v, u in re.findall(r'(\d+(?:\.\d+)?)(d|h|min|ms|us|s)\b', s))
def fmt(n): return f'{n:,}'
def gb(b): return f'{b / 1e9:.2f} GB'

# systemd accounting: "<unit>.service: Consumed X CPU time over Y wall clock time, Z memory peak."
jr = subprocess.run(['journalctl', '--user', '--since', '2026-11-15 05:45', '--no-pager', '-o', 'cat'], capture_output=True, text=True).stdout
acct = {}
for m in re.finditer(r'^(esr-[\w-]+)\.service: Consumed (.+?) CPU time(?: over (.+?) wall clock time)?, (\S+) memory peak', jr, re.M):
    acct.setdefault(m.group(1), []).append({'cpu_s': dur(m.group(2)), 'wall_s': dur(m.group(3) or ''), 'peak': m.group(4)})
mg = [l.strip() for l in open(MGLOG) if l.startswith('2026-11-15') and ' STOP ' in l]
mg_n66 = [l for l in mg if 'esr-n66-' in l]
stopped_files = sorted(os.path.basename(p) for p in glob.glob(W + '/MEMGUARD_STOPPED_esr-n66-*'))
du = int(subprocess.run(['du', '-sb', W + '/p2/c14'], capture_output=True, text=True).stdout.split()[0])

cubes = sorted(C.values(), key=prio)
cert = [c for c in cubes if c['status'] == 'certified']
counted = [c for c in cert if R.get(c['id'], {}).get('ok')]
notcounted = [c for c in cert if not R.get(c['id'], {}).get('ok')]
leaves = [c for c in cubes if c['status'] != 'split']
openl = [c for c in leaves if not (c['status'] == 'certified' and R.get(c['id'], {}).get('ok'))]
splits = [c for c in cubes if c['status'] == 'split']
ran = [c for c in cubes if c.get('started')]
counts = {}
for c in cubes: counts[c['status']] = counts.get(c['status'], 0) + 1
assert cov['certified_counted'] == len(counted) and cov['leaves'] == len(leaves)
k = len(cov['states']); A = cov['assignments']
meas = cov['certified_measure_of_64']
def lits(c): return ' '.join(f'{s}{"o" if b else "h"}' for s, b in c['lits'])
def cpu(c): return sum(a['cpu_s'] for a in acct.get(c['unit'], []))
cpu_cert = sum(cpu(c) for c in counted); cpu_split = sum(cpu(c) for c in splits); cpu_all = sum(cpu(c) for c in ran)
drv = acct.get('esr-n66-driver', [])
vfy = {u: a for u, a in acct.items() if u.startswith('esr-vfy-n66prog')}
anon_max = max((c.get('peak_anon_mb', 0) for c in ran), default=0)
cad_max = max((c.get('cadical_rss_mb') or 0 for c in ran), default=0)
cake = [(int(R[c['id']]['info']['cake_rss_kb']) // 1024, R[c['id']]['info']['cake_heap_mb'], c['id']) for c in counted if R[c['id']]['info'].get('cake_rss_kb')]
over80 = [(c['id'], c['peak_anon_mb']) for c in ran if c.get('peak_anon_mb', 0) > 0.8 * 3.6 * 1024]
trim_lrat = sum(R[c['id']]['info']['trim_lrat_bytes'] for c in counted); zst = sum(R[c['id']]['info']['trim_lrat_zst_bytes'] for c in counted)
cnf_kept = [p for p in glob.glob(W + '/p2/c14/*/it*/cert.cnf')]
deleted = sum(c.get('deleted_partial_bytes', 0) for c in splits)
open_by = {}
for c in openl: open_by.setdefault(c['status'], []).append(c)

L = []
P = L.append
P(f'# N66 level-14 cube campaign: progress at the stop (15 November 2026, driver ended {st["updated"]} KST)')
P('')
P(f'**Status: N66 ≤ 55 is NOT decided. N66 ≤ 56 (level 13, CERTIFIED, parent README §9) remains the bound.** At the stop, '
  f'**{len(counted)} of the {len(leaves)} leaf cubes are CERTIFIED**, each with its full certification path (§1) re-checked here (§2); '
  f'{len(openl)} leaves are open. By measure the certified cubes make up {meas:g} of the 64 base cubes ({100 * meas / 64:.1f} %). '
  f'{len(splits)} cubes reached their CaDiCaL time limit and were re-split. '
  + ('No cube was SAT. ' if not counts.get('SAT') else f'**{counts["SAT"]} cube(s) SAT: the campaign stopped; see §4.** ')
  + 'Nothing is committed.')
P('')
last = sorted((c for c in ran if c.get('limit_s', 1200) < 1200), key=lambda c: c['t0'])
P(f'The campaign ended before its 09:40 deadline. The driver starts no cube after 09:24 (the deadline minus 960 s), and the cubes started '
  f'last got CaDiCaL limits shortened to fit the deadline: ' + ', '.join(f'{c["id"]} at {c["started"]} with {c["limit_s"]} s ({c["status"]})' for c in last)
  + f'. When the last of them ended, the driver wrote its final status at {st["updated"]} and exited. No esr-n66-* unit has been running since then.')
P('')
P(f'Written {time.strftime("%H:%M")} KST, 15 November 2026, by the monitoring step, after every esr-n66-* unit had ended; the driver\'s '
  f'final status was written at {st["updated"]} KST (final = {st.get("final")}). W = `{W}`. Sources: `W/p2/c14/campaign_status.json`, '
  'the certificate directories `W/p2/c14/<id>/it<k>/`, `journalctl --user` (systemd CPU accounting) and the memguard log '
  f'`{MGLOG}`. The per-cube status table is `STATUS_campaign.md` in this folder; the model, the cover argument and the acceptance '
  'rules are `README.md` §2 and §6 (written 05:44, before the campaign; its note that cube B is not yet a certified cube is superseded: '
  'cube B = hhhhhh is certified below).')
P('')
P('Labels: **CERTIFIED** = CaDiCaL 2.1.3 LRAT proof accepted by cake_lpr (`s VERIFIED UNSAT`, grepped) for the stated CNF, hashes '
  'recorded; **COMPUTED** = solver verdict only; **HEURISTIC** = timings and estimates.')
P('')
P('Corrections to `README.md`, which stays unedited under the new-files-only rule:')
P('')
P('- Cube B (hhhhhh) is now a certified cube (§3).')
P('- The pilot\'s row count is 392, not "392 or 393". The critic counted the pilot\'s used_ids.txt directly. This run\'s own core of '
  'cube B also has 392 rows, but it comes from a different CNF and proof, so it does not settle the pilot count by itself.')
P('- The folder no longer holds only the README. It also has STATUS_campaign.md (the driver\'s status), tools/ and this file.')
P('')
P('## 1. What counts as a certified cube')
P('')
P('A cube fixes the signs of the split states 25 12 16 29 17 37 (o = occupied = +sel_s, h = hole = −sel_s, sel_s = DIMACS variable '
  '988541 + s), followed by `_<s><o|h>` for each re-split state. A cube counts only with its full certification path, run in its own '
  'unit esr-n66-cube-<id> and certificate directory:')
P('')
P('1. CaDiCaL 2.1.3 (`--unsat -t T --lrat=true`) exits 20 on cert.cnf, which is the level-14 CNF with the cube\'s units (p2_write.py; '
  'the layout\'s `cube` field is the cube);')
P('2. p2_lrat_trim keeps the cone of the empty clause: trim.cnf (the used original clauses) and trim.lrat;')
P('3. `/home/jay/.local/bin/cake_lpr` on trim.cnf and trim.lrat prints the exact line `s VERIFIED UNSAT` (cake.out);')
P('4. every used row is justified: p2_template_cert66 (0 unjustified), final_verify66 (bad 0, rows_match), link re-check ALL_OK;')
P('5. p2_verify ALL_OK: every distinct clause of trim.cnf is a mono66 clause, a fixed or cube unit, a justified row, a counter clause '
  'or an SB clause (0 unclassified);')
P('6. cert.json ALL_OK, and the driver\'s accept() (README §6: L = 14, W = range(70), the 27 SB pairs of b14h2, the cube in layout, '
  'verify and cert equal to the planned cube, trim.cnf hash recomputed).')
P('')
P('By README §2, certificates for every leaf of a cover would make the level-14 relaxation UNSAT and give N66 ≤ 55, after an '
  'independent check.')
P('')
P('## 2. Re-check of the certified cubes (this step)')
P('')
P('`tools/progress_chk.py` (new; glue around sha256sum and zstd, run as units esr-vfy-n66prog*, CPUQuota 200 %, MemoryMax 1G, '
  'MemorySwapMax 0, nice 10) re-read the files of every cube with status certified. It required all of the following:')
P('')
P('- cake.out contains the exact line `s VERIFIED UNSAT` exactly once;')
P('- the timed command in cake.err is `/home/jay/.local/bin/cake_lpr` on that directory\'s trim.cnf and trim.lrat;')
P('- sha256sum of trim.cnf and of trim.lrat, recomputed, equal cert.json, verify.json and the driver status;')
P('- `zstd -dc trim.lrat.zst | sha256sum` equals the trim.lrat hash;')
P('- cert.json and verify.json are ALL_OK, with 0 unclassified clauses;')
P('- the kinds add up to the distinct clauses, and the clause count equals the trim.cnf header and cert.json;')
P('- L = 14, W = 70 states, the sel range, bound 55, the cube equals the plan and the SB pairs equal b14h2\'s;')
P('- rows: used = justified = final_verify66 rows, bad 0 and rows_match, every template and core verified, link re-check ALL_OK;')
P('- cadical.log has `Version 2.1.3`, `exit 20` and `s UNSATISFIABLE`;')
P('- pipeline.log has every step and ends with P2_CERT_DONE.')
P('')
P(f'**Result: {len(counted)} of {len(cert)} certified cubes pass every check**' +
  (f'; not counted: {", ".join(c["id"] + " (" + ", ".join(R.get(c["id"], {}).get("bad", ["no re-check"])) + ")" for c in notcounted)}.' if notcounted else '.'))
P('This is not the independent VERIFY that the house rules require. That VERIFY still has to re-run cake_lpr, check that trim.cnf is a '
  'subset of cert.cnf, and check rows and geometric clauses with its own encoder (§8).')
P('')
P(f'## 3. Certified cubes ({len(counted)})')
P('')
P('Hashes are SHA-256. The cake_lpr column is the line in `<certdir>/cake.out`, matched exactly. trim.lrat is kept, and so is '
  'trim.lrat.zst (round trip checked). p2_cert.sh deleted the untrimmed LRAT after cake_lpr accepted the trimmed one; its hash is in '
  'cert.lrat.sha256. The full cube CNF cert.cnf is kept. The certificate directory is `W/p2/c14/<id>/it1/` for every cube below. The 8 '
  'cubes that unit propagation refutes have identical trimmed files: their core uses only the units 25h, 29o and 37h, which they share, '
  'plus SB clauses.')
P('')
P('| # | cube | holes | rows | trim clauses | trim.cnf SHA-256 | trim.lrat SHA-256 | cake_lpr | heap MB / s |')
P('|---|---|---|---|---|---|---|---|---|')
for n, c in enumerate(counted, 1):
    i = R[c['id']]['info']
    assert i['certdir'].endswith(c['certdir']) and c['certdir'] == f'p2/c14/{c["id"]}/it1', c['certdir']
    P(f'| {n} | {c["id"]}{" (UP)" if c["up_refuted"] else ""} | {c["holes"]} | {i["rows"]} | {fmt(i["trim_cnf_clauses"])} | '
      f'`{i["trim_cnf_sha256"]}` | `{i["trim_lrat_sha256"]}` | `{i["cake_line"]}` | {i["cake_heap_mb"]} / {i["cake_s"]} |')
P('')
P(f'## 4. Open cubes ({len(openl)})')
P('')
for s, cs in sorted(open_by.items()):
    if s == 'queued':
        by = {}
        for c in cs: by.setdefault(c['holes'], []).append(c['id'])
        P(f'- **queued, never started ({len(cs)}):** ' + '; '.join(f'{h} hole{"" if h == 1 else "s"} ({len(v)}): {", ".join(v)}' for h, v in sorted(by.items(), reverse=True)) + '.')
    else:
        P(f'- **{s} ({len(cs)}):** ' + '; '.join(c['id'] + ' (' + ', '.join(x for x in [c.get('why') or c.get('accept') or '',
            f'started {c.get("started")}', f'limit {c.get("limit_s")} s', f'conflicts {fmt(c["conflicts"])}' if c.get('conflicts') else '',
            f'certdir {c["certdir"]}' if c.get('certdir') else ''] if x) + ')' for c in cs) + '.')
P('')
P(f'## 5. Re-splits ({len(splits)})')
P('')
P('When a cube\'s CaDiCaL run reaches its time limit without a verdict, the driver replaces the cube by its two children: c with s '
  'occupied and c with s hole, where s is the first state of 23 49 44 40 20 32 46 45 52 35 30 39 not already in c. The two children '
  'cover the parent.')
P('')
P('| cube | started | limit s | CaDiCaL conflicts | CaDiCaL process s | split on | children (status) | partial files deleted |')
P('|---|---|---|---|---|---|---|---|')
for c in splits:
    P(f'| {c["id"]} | {c["started"]} | {c["limit_s"]} | {fmt(c.get("conflicts") or 0)} | {c.get("process_s")} | {c["split_on"]} | '
      + ', '.join(f'{x} ({C[x]["status"]})' for x in c['children']) + f' | {gb(c.get("deleted_partial_bytes", 0))} |')
P('')
short = [c for c in splits if c.get('limit_s', 1200) < 1200]
P(f'- Every split above hit the full 1,200 s limit.' if not short else
  f'- Splits after a shortened limit (deadline): {", ".join(c["id"] + " (" + str(c["limit_s"]) + " s)" for c in short)}; such a cube was split, not retried at 1,200 s.')
P(f'- The driver\'s finalize() deleted the partial cert.lrat and cert.cnf of each timed-out run, {gb(deleted)} in total. These files were '
  'written by this campaign and are not part of any certificate. The critic flagged the deletion as an owner question (issue 1, 06:46), '
  'because AGENTS.md makes deleting large proof material ask-first. The running driver was not changed.')
P('')
P('## 6. Cover')
P('')
P(f'- **Leaves: {len(leaves)}**, which is the 64 base cubes, minus {len(splits)} split parents, plus {2 * len(splits)} children. Own '
  f'brute-force check (progress_chk.py) over all 2^{k} = {A} assignments of the {k} states that occur ({" ".join(map(str, cov["states"]))}): '
  f'**{cov["leaf_uncovered"]} uncovered**. The roots are exactly the 64 sign patterns of 25 12 16 29 17 37 '
  f'({"yes" if cov["roots_are_64_patterns"] else "NO"}). Each split parent\'s two children are the parent with s occupied and with s '
  f'hole ({"yes" if cov["split_children_ok"] else "NO"}). The driver\'s own check agrees: '
  f'{"COVER_OK" if st["cover"]["leaf_cover_ok"] else "NOT COVERED"}.')
P(f'- **Certified: {len(counted)} leaves. Certified cover NOT complete.** {cov["certified_uncovered"]} of the {A} assignments satisfy no '
  f'certified cube, with each cube\'s literals read from its verify.json. By measure the certified cubes make up {meas:g} of the 64 base '
  f'cubes. Open: {len(openl)} leaves, measure {64 - meas:g}.')
P('')
P('## 7. Resource use')
P('')
P(f'- **Units.** {len(ran)} cube units ran (esr-n66-cube-<id>), plus esr-n66-driver. Each cube unit had 1 thread (CPUQuota 98 %), '
  'MemoryMax 3.6G, MemorySwapMax 0, nice 10 and a RuntimeMaxSec ending by 09:39. The memguard lifts the kernel limit, keeps '
  'memory.high = 3.6G as a brake, and stops a unit at 95 % of 3,686 MiB counted as anon plus swap. The driver unit had 6 % and 300M. '
  'At most 3 cubes ran at once: 3 × 98 % + 6 % = 3.0 threads of the 16-thread cap.')
P(f'- **CPU** (systemd accounting from the journal): {cpu_all / 3600:.2f} CPU-h in cube units. Of that, {cpu_cert / 3600:.2f} CPU-h '
  f'went to the certified cubes and {cpu_split / 3600:.2f} CPU-h to the {len(splits)} runs without a verdict. Driver: '
  + (', '.join(f'{a["cpu_s"]:.0f} s CPU over {a["wall_s"] / 3600:.2f} h' for a in drv) or 'no accounting line') + '.')
P(f'- **Memory.** Highest anon of a cube unit (driver samples every 15 s): {anon_max} MB. Highest CaDiCaL maximum resident '
  f'(cadical.log): {cad_max:.0f} MB. Highest cake_lpr maximum RSS: ' +
  (f'{max(cake)[0]} MB (heap {max(cake)[1]} MB, {max(cake)[2]}); every accepted run used the 2000 MB heap tier' if cake and all(h == 2000 for _, h, _ in cake)
   else f'{max(cake)[0]} MB (heap {max(cake)[1]} MB, {max(cake)[2]})' if cake else 'none') +
  f'. **Above 80 % of MemoryMax (2,949 MiB) in the anon samples: {", ".join(f"{i} {m:,} MiB ({100 * m / 3686.4:.0f} %)" for i, m in over80) or "none"}**'
  + (' (a breach of the 80 % sizing rule; no guard stop, no OOM kill). ' if over80 else '. ') +
  f'{"No unit reached" if not mg_n66 else "Units stopped at"} the guard\'s 95 % stop (3,502 MiB, checked every 0.25 s): the memguard log has {len(mg_n66)} STOP lines for esr-n66 units today{" (" + "; ".join(mg_n66) + ")" if mg_n66 else ""}, and '
  f'{"there are no" if not stopped_files else "there are"} `W/MEMGUARD_STOPPED_esr-n66-*` files{": " + ", ".join(stopped_files) if stopped_files else ""}. '
  'systemd\'s "memory peak 3.6G" figures count page cache held under the memory.high brake, so they are not anon. The 15 s samples can miss '
  'short peaks (critic issue 3).')
P(f'- **Disk.** `W/p2/c14` holds {gb(du)}. That includes {gb(trim_lrat)} of trimmed LRATs, {gb(zst)} of zstd copies and '
  f'{len(cnf_kept)} full cube CNFs (cert.cnf, about 664 MB each). Partial files deleted at re-splits: {gb(deleted)}.')
started = sorted(set(re.findall(r'^Started (esr-vfy-n66prog\d+)\.service', jr, re.M)))
P(f'- **This step:** {len(started)} re-check units (' + ', '.join(f'{u} {sum(a["cpu_s"] for a in vfy[u]):.0f} s CPU' if u in vfy else f'{u} no accounting line (under 1 s)' for u in started)
  + '); 1-2 threads each, at most 1G.')
P('')
P('Per cube: the unit CPU comes from systemd. wall s is the driver\'s, from the start of p2_batch_cube.py to the end of p2_cert.sh. '
  'Anon is the driver\'s 15 s samples. CaDiCaL RSS is the maximum resident in cadical.log. cake is the maximum RSS from /usr/bin/time.')
P('')
P('| cube | status | started | wall s | unit CPU s | CaDiCaL conflicts | CaDiCaL RSS MB | anon peak MB | cake RSS MB |')
P('|---|---|---|---|---|---|---|---|---|')
for c in sorted(ran, key=lambda c: c.get('t0', 0)):
    i = R.get(c['id'], {}).get('info', {})
    P(f'| {c["id"]} | {c["status"]} | {c.get("started")} | {c.get("wall_s", "")} | {cpu(c):.0f} | {fmt(c["conflicts"]) if c.get("conflicts") else ""} | '
      f'{c.get("cadical_rss_mb") or ""} | {c.get("peak_anon_mb", "")} | {int(i["cake_rss_kb"]) // 1024 if i.get("cake_rss_kb") else ""} |')
P('')
P('## 8. What remains')
P('')
P(f'- **{len(openl)} open leaves (measure {64 - meas:g} of 64).** Observed so far (HEURISTIC): certified real cubes took '
  + ', '.join(f'{h} holes {min(v):.0f}' + (f'–{max(v):.0f}' if max(v) > min(v) else '') + f' s wall ({len(v)} cube{"" if len(v) == 1 else "s"})' for h, v in sorted(
      {h: [c['wall_s'] for c in counted if not c['up_refuted'] and c['holes'] == h] for h in {c['holes'] for c in counted if not c['up_refuted']}}.items(), reverse=True))
  + f'. {len(splits)} cubes reached their CaDiCaL limit without a verdict: ' + '; '.join(f'{c["id"]} ({c["holes"]} holes, {c["limit_s"]} s{" = full limit" if c["limit_s"] == 1200 else ", shortened by the deadline"})' for c in splits) + '. '
  + f'{sum(1 for c in openl if c["holes"] <= 3)} of the {len(openl)} open leaves have 3 or fewer holes; cubes with 3 holes were the slowest so far. '
  'At 3 slots the open part needs many more slot-hours; no completion time is claimed.')
P('- **Independent VERIFY** of the accepted certificates, with own code, is still owed. It should re-run cake_lpr on every '
  'trim.cnf/trim.lrat, check that every trim.cnf clause is in that cube\'s cert.cnf, check that cert.cnf is F_c plus the cube units, and '
  'check rows and geometric clauses with its own encoder. The critic\'s unit esr-vfy-n66chk (06:13) did this for 4 cubes (hhhhhh, '
  'hohhhh, ohhhhh, hhhohh): cake_lpr re-run, zstd, subset and units. Their rows and geometric clauses were not checked with own code.')
P('- **Driver issues** still in the code (critic, 06:46), for a new copy before a long resume:')
P('  1. A split deletes the partial LRAT and CNF; this has happened now (§5).')
P('  2. Memory for the cake_lpr heap tiers above 2000 MB is not budgeted inside the 3.6G unit.')
P('  3. The 80 % check uses 15 s samples.')
P('  4. The split test also fires on ends that are not time limits.')
P('  5. cad_stats() parsing is not guarded.')
P(f'  Also: near the deadline the CaDiCaL limit is shortened, and a cube that hits a shortened limit is split rather than retried. This happened {len(short)} times (§5).')
P('- **Owner decisions:** whether partial proofs of timed-out runs may be deleted (§5), and the allocation for a resume.')
P('')
P('## 9. Files and hashes')
P('')
P('- `W/p2/c14/campaign_status.json`: machine status (final). `W/p2/c14/<id>.out`: event stream of each cube. `W/p2/c14/<id>/it<k>/`: '
  'certificate directory (cadical.log, cert.cnf, trim.cnf, trim.lrat, trim.lrat.zst, cake.out, cake.err, cake_attempts.json, '
  'used_rows.json, tcert/, fv66.out, verify.json, cert.json, pipeline.log).')
REC = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/N66N20261113/cubes20261115'
sc = subprocess.run(['sha256sum', '-c', REC + '/tools/sha256.txt'], cwd=W, capture_output=True, text=True)
sc_ok = [l for l in sc.stdout.splitlines() if l.endswith(': OK')]; sc_bad = [l for l in sc.stdout.splitlines() if not l.endswith(': OK')]
hd = subprocess.run(['sha256sum', W + '/p2c14_driver.py', REC + '/tools/p2c14_driver.py', W + '/p2_batch_cube.py', REC + '/tools/p2_batch_cube.py'],
                    capture_output=True, text=True).stdout.split()[0::2]
P(f'- Driver `W/p2c14_driver.py`, SHA-256 `{hd[0]}`, {"equal to" if hd[0] == hd[1] else "DIFFERENT FROM"} tools/p2c14_driver.py. '
  f'Cube runner `W/p2_batch_cube.py`, SHA-256 `{hd[2]}`, {"equal to" if hd[2] == hd[3] else "DIFFERENT FROM"} tools/p2_batch_cube.py. '
  f'`sha256sum -c tools/sha256.txt` in W at writing time: {len(sc_ok)} OK' + (f', mismatches: {"; ".join(sc_bad)}' if sc_bad or sc.returncode else '') + '.')
import hashlib
h = lambda f: hashlib.sha256(open(f, 'rb').read()).hexdigest()
here = os.path.dirname(os.path.abspath(__file__))
hf = lambda *ns: next((h(os.path.join(here, n)) for n in ns if os.path.exists(os.path.join(here, n))), 'not found')   # scratch or tools/ name
P(f'- New in this step: `tools/progress_chk.py` (the re-check of §2 and §6; SHA-256 `{hf("chk.py", "progress_chk.py")}`) and '
  f'`tools/progress_write.py` (writes this file from the status, the re-check output, the journal and the memguard log; SHA-256 '
  f'`{hf("prog.py", "progress_write.py")}`). The re-check output stayed in the session scratchpad, which is not durable. Re-running '
  '`progress_chk.py OUT.json` recomputes it from the files in W.')
P('')
L.append(open(resumef).read().rstrip('\n'))
L.append('')
open(outf, 'w').write('\n'.join(L))
print('PROG_OK', outf, len(counted), 'certified;', len(openl), 'open;', len(splits), 'splits')
