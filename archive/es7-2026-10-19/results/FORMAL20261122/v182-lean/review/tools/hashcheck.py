"""R3 (reviewer's own code, run in one unit): does each Lean-printed piece text equal a certified CNF?

The frozen printer (sha256 FROZEN, checked before and after) prints the piece list (`list`), B (`base`) and every piece
(`all DIR`). For piece i = (n, m) the printed SHA-256 must equal: the one campaign certify.jsonl row of that cube
(verdict exactly 's VERIFIED UNSAT', its 'cnf' path the cube's file), the SHA-256 of that CNF file on disk; the
campaign cake output must contain the exact line; at least one independent cake_lpr re-run row (wave-1 verifier,
recheck, rebuild lens) must carry the same CNF sha, the campaign LRAT sha, the exact verdict and the exact line in its
stored output. Also: the exe's list equals my own reading of V182Enc.pieces; my hashes equal the worker's M9 TSV.
Controls (each must fail): a one-hex-digit change of a printed hash; piece i against piece i+1's record; the unlisted
cube (36, -). usage: python3 -I hashcheck.py OUTDIR TMPDIR"""
import hashlib, json, os, subprocess, sys

D = '/home/jay/research/data/formalize-20261122/v182-lean'
EXE = f'{D}/build/bin/v182print'
FROZEN = 'b0b270cb5840bb92151900b77eb76ff8be1b71efd3dee93dbfe198ed6a531c5d'
A2 = '/home/jay/research/data/e810-linux-20261121/a-t34-sat182/a2'
W1 = '/home/jay/research/data/e810-linux-20261121/a-t34-sat182/verify/cake'
RC = '/home/jay/research/data/e810-linux-20261121/v182-recheck'
B_SHA = 'c3ae52244554013383f1447b981a3a8f10132a50ec45b0a4f74f3e7248807074'
LINE = b's VERIFIED UNSAT'
SPLIT = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 78, 79, 80, 81, 82, 83, 90, 91, 92, 93, 94, 95,
         102, 103, 104, 105, 106, 107, 114, 115, 116, 117, 118, 119]  # V182Enc.splitSet as I read Gen.lean:130-132
outdir, tmp = sys.argv[1], sys.argv[2]


def h_file(p):
    s = hashlib.sha256()
    with open(p, 'rb') as f:
        while True:
            b = f.read(1 << 22)
            if not b:
                return s.hexdigest()
            s.update(b)


def has_line(p):
    if not os.path.isfile(p):
        return False
    with open(p, 'rb') as f:
        return any(l.rstrip(b'\n') == LINE for l in f)


def certdir(n, m):
    return 'certY1' if m is None else f'cert{n:03d}Y2'


def cubefile(n, m):
    return f'cubesY1/cube{n:03d}.cnf' if m is None else f'cubes{n:03d}Y2/cube{m:03d}.cnf'


def tag(n, m):
    return certdir(n, m) + '/' + os.path.basename(cubefile(n, m))[:-4]


res = {'exe_sha_start': h_file(EXE)}
assert res['exe_sha_start'] == FROZEN, 'exe is not the frozen M9 exe'

# my reading of V182Enc.pieces (Gen.lean:135-137)
expect = [(n, m) for n in range(120) for m in (range(120) if n in SPLIT else [None])]
lst = []
for k, line in enumerate(subprocess.run([EXE, 'list'], capture_output=True, text=True, check=True).stdout.splitlines()):
    i, n, m = line.split(' ')
    assert int(i) == k
    lst.append((int(n), None if m == '-' else int(m)))
res['list_len'] = len(lst)
res['list_eq_my_reading'] = lst == expect

b = subprocess.run([EXE, 'base'], capture_output=True, check=True).stdout
res['base_sha'] = hashlib.sha256(b).hexdigest()
res['base_ok'] = res['base_sha'] == B_SHA == h_file(f'{A2}/g182_k5_st_sb2.cnf')

# records
camp = {}
for d in sorted(os.listdir(A2)):
    p = f'{A2}/{d}/certify.jsonl'
    if os.path.isfile(p):
        for line in open(p):
            r = json.loads(line)
            camp.setdefault(d + '/' + os.path.basename(r['cnf'])[:-4], []).append(r)
indep = {}
for line in open(f'{W1}/results.jsonl'):
    r = json.loads(line)
    indep.setdefault(r['tag'], []).append(('wave1', r, f"{W1}/out/{r['tag'].replace('/', '_')}.cake.out"))
for line in open(f'{RC}/status.jsonl'):
    r = json.loads(line)
    indep.setdefault(r['tag'], []).append(('recheck', r, f"{RC}/{r['out']}"))
for line in open(f'{RC}/verify/vcake_status.jsonl'):
    r = json.loads(line)
    indep.setdefault(r['tag'], []).append(('rebuild', r, f"{RC}/verify/{r['out']}"))


def judge(n, m, hx):
    t = tag(n, m)
    rows = camp.get(t, [])
    if len(rows) != 1:
        return False, f'rows={len(rows)}', ''
    r = rows[0]
    bad = []
    if r.get('verdict') != LINE.decode():
        bad.append('verdict')
    if r.get('cnf') != cubefile(n, m):
        bad.append('cnfpath')
    if r.get('cnf_sha256') != hx:
        bad.append('rowsha')
    if not os.path.isfile(f'{A2}/{cubefile(n, m)}') or h_file(f'{A2}/{cubefile(n, m)}') != hx:
        bad.append('filesha')
    if not has_line(f'{A2}/{t}.cake.out'):
        bad.append('cakeline')
    src = [s for s, x, op in indep.get(t, []) if x.get('verdict') == LINE.decode() and x.get('cnf_sha256') == hx
           and x.get('lrat_sha256') == r.get('lrat_sha256') and has_line(op)]
    if not src:
        bad.append('noindep')
    return not bad, ','.join(bad), '+'.join(src)


os.makedirs(tmp)
subprocess.run([EXE, 'all', tmp], check=True, capture_output=True)
files = os.listdir(tmp)
res['files_written'] = len(files)
res['file_names_ok'] = sorted(files) == sorted(f'{i}.cnf' for i in range(len(lst)))
worker = {}
for line in open(f'{D}/logs/m9_hash_binding.tsv').read().splitlines()[1:]:
    c = line.split('\t')
    worker[int(c[0])] = c[4]
mine, ok, srcs, fails = {}, 0, {}, []
with open(f'{outdir}/hashcheck.tsv', 'w') as out:
    out.write('i\tn\tm\ttag\tprinted_sha256\tok\tproblems\tindependent\n')
    for i, (n, m) in enumerate(lst):
        p = f'{tmp}/{i}.cnf'
        hx = h_file(p)
        os.remove(p)
        mine[i] = hx
        good, why, src = judge(n, m, hx)
        ok += good
        if not good:
            fails.append((i, why))
        srcs[src] = srcs.get(src, 0) + 1
        out.write(f"{i}\t{n}\t{'-' if m is None else m}\t{tag(n, m)}\t{hx}\t{good}\t{why}\t{src}\n")
os.rmdir(tmp)
res['pieces_ok'] = ok
res['fails'] = fails[:20]
res['independent_combos'] = srcs
res['equal_to_worker_tsv'] = len(worker) == len(mine) and all(worker[i] == mine[i] for i in mine)
res['distinct_printed_hashes'] = len(set(mine.values()))

# controls
flip = mine[0][:-1] + ('0' if mine[0][-1] != '0' else '1')
res['ctl_flipped_hash_fails'] = not judge(*lst[0], flip)[0]
res['ctl_neighbour_record_fails'] = not judge(*lst[1], mine[0])[0]
c36 = hashlib.sha256(subprocess.run([EXE, 'cube', '36', '-'], capture_output=True, check=True).stdout).hexdigest()
res['ctl_unlisted_cube036'] = judge(36, None, c36)
res['ctl_unlisted_cube036_fails'] = not res['ctl_unlisted_cube036'][0]
res['exe_sha_end'] = h_file(EXE)
res['ALL_OK'] = (res['exe_sha_start'] == res['exe_sha_end'] == FROZEN and res['list_len'] == 4404
                 and res['list_eq_my_reading'] and res['base_ok'] and res['files_written'] == 4404
                 and res['file_names_ok'] and ok == 4404 and res['equal_to_worker_tsv']
                 and res['ctl_flipped_hash_fails'] and res['ctl_neighbour_record_fails']
                 and res['ctl_unlisted_cube036_fails'])
json.dump(res, open(f'{outdir}/hashcheck.summary.json', 'w'), indent=1)
print(json.dumps(res))
sys.exit(0 if res['ALL_OK'] else 1)
