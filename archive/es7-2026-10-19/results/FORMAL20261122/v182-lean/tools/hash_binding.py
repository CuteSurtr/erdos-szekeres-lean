"""M9 (trust item E1): bind the text the Lean exe prints for each of its 4,404 pieces to a certified CNF and verdict.

The piece list comes from the exe itself (`v182print list`: index, n, m), never from the campaign directories.
`v182print all DIR` writes `pieceText pieces[I]` (V182Enc.Gen) to DIR/I.cnf; this script hashes each file, deletes it,
and for piece (n, m) with tag certY1/cubeNNN (m = -) or certNNNY2/cubeMMM requires:
  (a) campaign row (a2/<dir>/certify.jsonl): exactly one row for the tag, verdict 's VERIFIED UNSAT',
      cnf_sha256 == printed;
  (b) the campaign CNF file on disk (a2/cubesY1/cubeNNN.cnf or a2/cubesNNNY2/cubeMMM.cnf) has SHA-256 == printed;
  (c) the campaign cake output (a2/<dir>/cubeXXX.cake.out) has the exact line 's VERIFIED UNSAT';
  (d) at least one independent cake_lpr re-run (wave-1 verifier verify/cake/results.jsonl + out/, the recheck
      v182-recheck/status.jsonl + out/, or the rebuild lens v182-recheck/verify/vcake_status.jsonl + out/) with
      verdict 's VERIFIED UNSAT', cnf_sha256 == printed, lrat_sha256 == the campaign row's lrat_sha256, and the exact
      line in its stored output.
Also: the B text printed by `v182print base` equals a2/g182_k5_st_sb2.cnf (sha256), and the piece list is
84 direct + 36 x 120 with distinct tags.
Negative controls (each must FAIL / differ): the unlisted cube (36, -) printed by `v182print cube 36 -` is not
certified (its campaign row is the abandoned timeout); piece I's hash against piece I+1's record; an out file with a
trailing space or a 'c ' prefix fails the exact-line test.
Exit 0 iff 4,404/4,404 MATCH and every control behaves.  usage: python3 -I hash_binding.py OUT.tsv WORKDIR"""
import hashlib, json, os, subprocess, sys

D = '/home/jay/research/data/formalize-20261122/v182-lean'
A2 = '/home/jay/research/data/e810-linux-20261121/a-t34-sat182/a2'
W1 = '/home/jay/research/data/e810-linux-20261121/a-t34-sat182/verify/cake'
RC = '/home/jay/research/data/e810-linux-20261121/v182-recheck'
EXE = f'{D}/build/bin/v182print'
B_SHA = 'c3ae52244554013383f1447b981a3a8f10132a50ec45b0a4f74f3e7248807074'
VL = 's VERIFIED UNSAT'
out_tsv, work = sys.argv[1], sys.argv[2]


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as g:
        for chunk in iter(lambda: g.read(1 << 24), b''):
            h.update(chunk)
    return h.hexdigest()


def exact_line(p):
    try:
        with open(p, 'rb') as g:
            return VL.encode() in g.read().split(b'\n')
    except OSError:
        return False


def tag_of(n, m):
    return f'certY1/cube{n:03d}' if m is None else f'cert{n:03d}Y2/cube{m:03d}'


def cnf_path(n, m):
    return f'{A2}/cubesY1/cube{n:03d}.cnf' if m is None else f'{A2}/cubes{n:03d}Y2/cube{m:03d}.cnf'


# campaign rows by tag
camp = {}
for d in sorted(os.listdir(A2)):
    if d.startswith('cert') and os.path.isfile(f'{A2}/{d}/certify.jsonl'):
        for line in open(f'{A2}/{d}/certify.jsonl'):
            r = json.loads(line)
            t = d + '/' + os.path.basename(r['cnf'])[:-4]
            camp.setdefault(t, []).append(r)
# independent re-runs by tag: list of (source, row, out path)
ind = {}
for line in open(f'{W1}/results.jsonl'):
    r = json.loads(line)
    ind.setdefault(r['tag'], []).append(('wave1', r, f"{W1}/out/{r['tag'].replace('/', '_')}.cake.out"))
for line in open(f'{RC}/status.jsonl'):
    r = json.loads(line)
    ind.setdefault(r['tag'], []).append(('recheck', r, f"{RC}/{r['out']}"))
for line in open(f'{RC}/verify/vcake_status.jsonl'):
    r = json.loads(line)
    ind.setdefault(r['tag'], []).append(('rebuild', r, f"{RC}/verify/{r['out']}"))


def check(tag, n, m, printed):
    """Return (verdict, details)."""
    rows = camp.get(tag, [])
    det = {'campaign_rows': len(rows)}
    if len(rows) != 1:
        return 'FAIL', det
    r = rows[0]
    det['campaign_verdict'] = r['verdict'] == VL
    det['campaign_sha'] = r['cnf_sha256'] == printed
    cp = cnf_path(n, m)
    det['file_sha'] = os.path.isfile(cp) and sha_file(cp) == printed
    d, base = tag.split('/')
    det['campaign_out'] = exact_line(f'{A2}/{d}/{base}.cake.out')
    srcs = [s for s, x, op in ind.get(tag, []) if x.get('verdict') == VL and x.get('cnf_sha256') == printed
            and x.get('lrat_sha256') == r.get('lrat_sha256') and exact_line(op)]
    det['independent'] = ','.join(srcs)
    ok = det['campaign_verdict'] and det['campaign_sha'] and det['file_sha'] and det['campaign_out'] and srcs
    return ('MATCH' if ok else 'FAIL'), det


summary = {'exe_sha256': sha_file(EXE),
           'sources': {p: sha_file(f'{D}/lean/V182Enc/{p}') for p in sorted(os.listdir(f'{D}/lean/V182Enc')) if p.endswith('.lean')}}
# B
b = subprocess.run([EXE, 'base'], capture_output=True, check=True).stdout
summary['base_printed_sha256'] = sha_bytes(b)
summary['base_match'] = sha_bytes(b) == B_SHA == sha_file(f'{A2}/g182_k5_st_sb2.cnf')
# piece list from the exe
lst = []
for line in subprocess.run([EXE, 'list'], capture_output=True, text=True, check=True).stdout.splitlines():
    i, n, m = line.split()
    lst.append((int(i), int(n), None if m == '-' else int(m)))
tags = [tag_of(n, m) for _, n, m in lst]
direct = sorted(n for _, n, m in lst if m is None)
split = sorted({n for _, n, m in lst if m is not None})
summary['pieces'] = len(lst)
summary['distinct_tags'] = len(set(tags))
summary['direct'] = len(direct)
summary['split'] = len(split)
summary['split_complete'] = all(sorted(m for _, n2, m in lst if n2 == n) == list(range(120)) for n in split)
summary['cover_shape'] = (len(lst) == 4404 and len(set(tags)) == 4404 and len(direct) == 84 and len(split) == 36
                          and not set(direct) & set(split) and sorted(direct + split) == list(range(120))
                          and summary['split_complete'] and [i for i, _, _ in lst] == list(range(4404)))
# print all pieces, hash, delete
os.makedirs(work, exist_ok=False)
subprocess.run([EXE, 'all', work], check=True)
rows, nmatch, printed_by_i = [], 0, {}
for i, n, m in lst:
    p = f'{work}/{i}.cnf'
    h = sha_file(p)
    os.remove(p)
    printed_by_i[i] = h
    v, det = check(tag_of(n, m), n, m, h)
    nmatch += v == 'MATCH'
    rows.append([i, n, '-' if m is None else m, tag_of(n, m), h, det.get('campaign_rows'), det.get('campaign_verdict'),
                 det.get('campaign_sha'), det.get('file_sha'), det.get('campaign_out'), det.get('independent'), v])
os.rmdir(work)
with open(out_tsv, 'w') as f:
    f.write('index\tn\tm\ttag\tprinted_sha256\tcampaign_rows\tcampaign_verdict\tcampaign_sha_eq\tfile_sha_eq\t'
            'campaign_out_line\tindependent_sources\tverdict\n')
    for r in rows:
        f.write('\t'.join(map(str, r)) + '\n')
summary['match'] = nmatch
src_count = {}
for r in rows:
    for s in (r[10] or '').split(','):
        if s:
            src_count[s] = src_count.get(s, 0) + 1
summary['independent_source_counts'] = src_count
# controls
ctl = {}
c36 = subprocess.run([EXE, 'cube', '36', '-'], capture_output=True, check=True).stdout
v36, d36 = check('certY1/cube036', 36, None, sha_bytes(c36))
ctl['unlisted_cube036_not_certified'] = v36 == 'FAIL'
ctl['cube036_detail'] = d36
p0 = subprocess.run([EXE, 'piece', '0'], capture_output=True, check=True).stdout
ctl['piece_mode_eq_all_mode'] = sha_bytes(p0) == printed_by_i[0]
i0, n0, m0 = lst[0]
i1, n1, m1 = lst[1]
ctl['shifted_record_fails'] = check(tag_of(n1, m1), n1, m1, printed_by_i[0])[0] == 'FAIL'
os.makedirs(f'{D}/logs/ctl', exist_ok=True)
open(f'{D}/logs/ctl/trailing_space.out', 'w').write(VL + ' \n')
open(f'{D}/logs/ctl/c_prefix.out', 'w').write('c ' + VL + '\n')
open(f'{D}/logs/ctl/exact.out', 'w').write(VL + '\n')
ctl['exact_line_rejects_variants'] = (not exact_line(f'{D}/logs/ctl/trailing_space.out')
                                      and not exact_line(f'{D}/logs/ctl/c_prefix.out')
                                      and exact_line(f'{D}/logs/ctl/exact.out'))
summary['controls'] = ctl
ctl_ok = all(v for k, v in ctl.items() if k != 'cube036_detail')
summary['ALL_OK'] = bool(summary['base_match'] and summary['cover_shape'] and nmatch == 4404 and ctl_ok)
json.dump(summary, open(out_tsv[:-4] + '.summary.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != 'sources'}))
sys.exit(0 if summary['ALL_OK'] else 1)
