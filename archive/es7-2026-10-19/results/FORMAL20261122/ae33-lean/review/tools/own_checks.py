#!/usr/bin/env python3
"""Reviewer's own checks for ae33-lean (statement fidelity, binding evidence). Read-only on every input.

1. Data: the `ae33` array of lean/AE33Enc/Data.lean = ae33.txt (L18 and ref copy); 33 distinct points; general
   position (exact integers); H = REC's heptagon, its 35 increasing triples in ccw order positive.
2. Pairs: `pairs203` of Data.lean = (u, v) columns of hashes_203.tsv in order; as a set = all u < v < 33 meeting H.
3. Binding chain per pair (all 203): hashes_203 cnf_sha256 = L18 certify.jsonl = L18 summary.jsonl = fresh-run
   results.jsonl cnf_sha256_regen (the hash of the file the fresh cake_lpr read) = M9 exe hash; clause counts;
   exact verdict line counts in L18 cert/<name>.cake.out and fresh cake/<name>.cake.out; LRAT hash chain
   (.lrat.zst on disk = table; certify lrat = table = results.jsonl decompressed).
Writes review/logs/own_checks.json; exit 0 iff every check passes.
"""
import hashlib, itertools, json, re, sys

W = '/home/jay/research/data/formalize-20261122/ae33-lean'
L18 = '/home/jay/research/data/roadmap-20261115/pm1115/l1118/e72'
AE = '/home/jay/research/data/lower-20261121/ae33'
V = 's VERIFIED UNSAT'
H = [14, 15, 17, 20, 23, 32, 25]  # REC §1, ccw order


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def lean_array(src, name):
    m = re.search(r'def ' + name + r' : Array \([^)]*\) := #\[(.*?)\]', src, re.S) or \
        re.search(r'def ' + name + r' : Array \w+ := #\[(.*?)\]', src, re.S)
    return [(int(x), int(y)) for x, y in re.findall(r'\((-?\d+),\s*(-?\d+)\)', m.group(1))]


def main():
    res, ok = {}, True
    src = open(W + '/lean/AE33Enc/Data.lean').read()
    pts = lean_array(src, 'ae33')
    txt = [tuple(map(int, l.split())) for l in open(L18 + '/ae33.txt') if l.strip()]
    res['ae33_len'] = len(pts)
    res['ae33_eq_L18_txt'] = pts == txt
    res['L18_txt_sha'] = sha(L18 + '/ae33.txt')
    res['ref_txt_same'] = open(W + '/ref/ae33.txt', 'rb').read() == open(L18 + '/ae33.txt', 'rb').read()
    res['distinct'] = len(set(pts)) == 33
    res['general_position'] = all(orient(pts[a], pts[b], pts[c]) != 0
                                  for a, b, c in itertools.combinations(range(33), 3))
    hm = re.search(r'def hept : List Nat := \[([^\]]*)\]', src)
    res['hept_eq_REC'] = [int(x) for x in hm.group(1).split(',')] == H
    res['H_ccw_35_positive'] = all(orient(pts[H[a]], pts[H[b]], pts[H[c]]) > 0
                                   for a, b, c in itertools.combinations(range(7), 3))
    ok &= res['ae33_len'] == 33 and res['ae33_eq_L18_txt'] and res['ref_txt_same'] and res['distinct'] \
        and res['general_position'] and res['hept_eq_REC'] and res['H_ccw_35_positive'] \
        and res['L18_txt_sha'] == 'cb6a5327b26b869ab39baadf0ade737882f8473dc1ccfbd377d06405a59eb54d'

    pairs = lean_array(src, 'pairs203')
    ht = [l.rstrip('\n').split('\t') for l in open(AE + '/hashes_203.tsv') if not l.startswith('#')]
    res['ht_sha'] = sha(AE + '/hashes_203.tsv')
    res['ht_ref_copy_same'] = open(W + '/ref/hashes_203.tsv', 'rb').read() == open(AE + '/hashes_203.tsv', 'rb').read()
    res['pairs_len'] = len(pairs)
    res['pairs_eq_table_order'] = pairs == [(int(r[1]), int(r[2])) for r in ht]
    res['names_match_pairs'] = all(r[0] == f'ae_d{int(r[1])}_{int(r[2])}' for r in ht)
    meet = {(u, v) for u in range(33) for v in range(u + 1, 33) if u in H or v in H}
    res['pairs_set_eq_meeting_H'] = set(pairs) == meet and len(meet) == 203 and len(set(pairs)) == 203
    ok &= res['pairs_len'] == 203 and res['pairs_eq_table_order'] and res['names_match_pairs'] \
        and res['pairs_set_eq_meeting_H'] and res['ht_ref_copy_same'] \
        and res['ht_sha'] == '90cbb85d506d390e8d6a226296cc7581eeecee10611dce20f2f896031dc2b010'

    cert, summ, fresh = {}, {}, {}
    for l in open(L18 + '/cert/certify.jsonl'):
        j = json.loads(l); cert.setdefault(j['cnf'].split('/')[-1][:-4], []).append(j)
    for l in open(L18 + '/summary.jsonl'):
        j = json.loads(l); summ.setdefault(j['name'], []).append(j)
    for l in open(AE + '/results.jsonl'):
        j = json.loads(l); fresh.setdefault(j['name'], []).append(j)
    m9 = {}
    for l in open(W + '/logs/m9_hash_binding.tsv'):
        if l[:1].isdigit():
            r = l.rstrip('\n').split('\t'); m9[int(r[0])] = r
    bad = []
    for i, r in enumerate(ht):
        nm, cnf_sha, ncl, lrat_sha, lrat_bytes, zst_sha = r[0], r[4], r[5], r[6], r[7], r[8]
        c, s, f = cert.get(nm, []), summ.get(nm, []), fresh.get(nm, [])
        why = []
        if len(c) != 1 or c[0]['cnf_sha256'] != cnf_sha or c[0]['lrat_sha256'] != lrat_sha or c[0]['verdict'] != V:
            why.append('certify')
        if len(s) != 1 or s[0]['cnf_sha256'] != cnf_sha or str(s[0]['stats']['clauses']) != ncl or s[0]['verdict_lines'] != 1:
            why.append('summary')
        if len(f) != 1 or f[0]['cnf_sha256_regen'] != cnf_sha or not f[0]['cnf_all4_equal'] or f[0]['verdict_lines'] != 1 \
                or f[0]['cake_out_lines'] != 1 or not f[0]['lrat_equal'] or f[0]['lrat_sha256'] != lrat_sha \
                or f[0]['lrat_zst_sha256'] != zst_sha:
            why.append('fresh_results')
        l18 = open(f'{L18}/cert/{nm}.cake.out', errors='replace').read().splitlines()
        if sum(x == V for x in l18) != 1:
            why.append('L18_cake_out')
        fo = open(f'{AE}/cake/{nm}.cake.out', errors='replace').read().splitlines()
        if fo != [V]:
            why.append('fresh_cake_out')
        if sha(f'{L18}/cert/{nm}.lrat.zst') != zst_sha:
            why.append('lrat_zst')
        mr = m9.get(i)
        if not mr or mr[1] != nm or mr[2] != cnf_sha or mr[4] != f'p cnf 961 {ncl}' or mr[-1] != 'MATCH':
            why.append('m9_row')
        if why:
            bad.append((i, nm, why))
    res['chain_rows'] = len(ht)
    res['chain_bad'] = bad
    res['distinct_cnf_hashes'] = len({r[4] for r in ht})
    ok &= len(ht) == 203 and not bad
    res['PASS'] = bool(ok)
    json.dump(res, open(W + '/review/logs/own_checks.json', 'w'), indent=1)
    print(json.dumps(res, indent=1))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
