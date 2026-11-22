#!/usr/bin/env python3
"""lrev row binding check (own code; reads only).

Parses the ROW/CUT/ZIDX/ZSIDX/ZSET/ZSSET/CAT lines that Review.lean's #eval printed from the LOADED oleans
(OmissionBalanced.demand/support over Fin 2685, BalancedCoverCutsV2.demand/support over Fin 446, the Z and Z* supports,
the 252-state catalog) and compares them, exactly and in order, with the inputs of the trusted checkers:
  balanced-v2-source.json (check_tree via balz_assemble*.py, balcheck/balcheck2), the extra-row files of balcheck
  (zrow.json, zzs_rows.json, zzs_rows_n54.json), zstar.json, and the finder row files (balz*.rows).
Also: sha256 of every file against the record values, and two non-vacuity witnesses on the Lean rows.
usage: rows_compare.py  (writes rows_compare.json here)
"""
import hashlib, json, re, sys

R = '/home/jay/research/data/formalize-20261122/comp-audit/review'
REPO = '/home/jay/research/lean/erdos-szekeres-lean'
ZR = '/home/jay/research/data/bal186-20261119/zrow'
REC303 = REPO + '/archive/es7-2026-10-19/results/ES303N20261120/data'
FILES = {  # path: record sha256 (full, or a recorded prefix)
    REPO + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json':
        'acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72',
    ZR + '/balz.rows': '7076dd8212c382caf19b7fe39fca9b81de9ae8fba9150727efa1997d54f6288f',
    ZR + '/balz_m0.rows': '6fb2337976f23ffd328f3704d6905af57441009ff5d469316e264b816250f055',
    ZR + '/zrow.json': 'b43ba5f80582f7754fe6acf04cbbf81fc7822a5f784fb8c5ddedf643cce51258',
    ZR + '/balzs.rows': '9135465aac32b575d3f859192891b5088b6a23c6d521687aef1b032e64e2f2b8',
    ZR + '/zstar.json': '26d8886058cc53972dfe274e04150c4aee0ff4fffafb974a8c7c89cd57cef328',
    REC303 + '/zstar.json': '26d8886058cc53972dfe274e04150c4aee0ff4fffafb974a8c7c89cd57cef328',
    ZR + '/zzs_rows.json': 'dc6a410f9fa164ee5565fd9827f4697af052b311afda6d806a136c0cd3d896d3',
    REC303 + '/zzs_rows.json': 'dc6a410f9fa164ee5565fd9827f4697af052b311afda6d806a136c0cd3d896d3',
    ZR + '/balzs_n54.rows': '9e2dc29a',
    ZR + '/zzs_rows_n54.json': '8419984c',
    REC303 + '/zzs_rows_n54.json': '8419984c',
}


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def ints(s):
    return [int(x) for x in re.findall(r'\d+', s)]


CH = REPO + '/experiments/omission-compact-checker-2026-11-05/build/chain311'
SRC = {'catalog': CH + '/src/BalancedProof/Catalog.lean', 'cuts': CH + '/src/BalancedCoverCutsV2.lean',
       'lemmaz': '/home/jay/research/data/formalize-20261122/comp-audit/src/LemmaZ.lean',
       'lemmazs': '/home/jay/research/data/formalize-20261122/comp-audit/src/LemmaZStar.lean',
       'catdata': REPO + '/ErdosSzekeres/Omission/BalancedCatalogData.lean'}
SRC_SHA = {  # chain311 build.tsv src_sha256 of the last ok row (olean built from it); worker/record hashes
    'catalog': '17080b3c93264fcf', 'cuts': 'a79cf10030df67ae',
    'lemmaz': 'e6b28efaa80cb2158180daf12dd4ce76cf2b86cc833ae9d79b1c08ffca005d65',
    'lemmazs': '47bd1f5618ee515b4f9f5c398bd6239b1c650a16dc6aa1ae687b7dafd49fd61c'}


def olean_dump():
    """ROW lines printed by Review.lean section F from the loaded oleans (strict format; the dump was cut off)"""
    rows = {}
    pat = re.compile(r'^ROW (\d+) (\d+) \[([\d, ]*)\]$')
    for line in open(R + '/review.log', errors='replace'):
        m = pat.match(line.rstrip('\n'))
        if m:
            rows[int(m.group(1))] = (int(m.group(2)), ints(m.group(3)))
    n = len(rows)
    assert sorted(rows) == list(range(n)), 'ROW lines not contiguous'
    return [rows[i] for i in range(n)]


def source_rows():
    """2,685 rows from chain311/src/BalancedProof/Catalog.lean in rowChunks order"""
    text = open(SRC['catalog']).read()
    chunks = re.findall(r'^def (rows\d+) : Array \(Finset \(Fin 252\) × ℕ × ℕ\) := #\[\n(.*?)^\]', text, re.M | re.S)
    order = re.search(r'^def rowChunks := #\[(.*?)\]$', text, re.M).group(1).replace(' ', '').split(',')
    assert order == [c for c, _ in chunks] == [f'rows{128 * k}' for k in range(21)], 'rowChunks order'
    tup = re.compile(r'^\s*\(\{([\d, ]*)\}, (\d+), (\d+)\),?$')
    out = []
    for name, body in chunks:
        lines = [l for l in body.split('\n') if l.strip()]
        assert len(lines) == (128 if name != 'rows2560' else 2685 - 2560), (name, len(lines))
        for l in lines:
            m = tup.match(l)
            assert m, l[:80]
            out.append((int(m.group(2)), ints(m.group(1))))
    return out


def source_cuts():
    text = open(SRC['cuts']).read()
    sup = {int(k): ints(v) for k, v in re.findall(r'^def support(\d+) : Finset \(Fin 252\) := \{([\d, ]*)\}$', text, re.M)}
    order = re.search(r'^def support : Fin 446 → Finset \(Fin 252\) := !\[(.*?)\]$', text, re.M).group(1).replace(' ', '').split(',')
    assert order == [f'support{k}' for k in range(446)] and sorted(sup) == list(range(446)), 'cut support order'
    dem = ints(re.search(r'^def demand : Fin 446 → ℕ := !\[(.*?)\]$', text, re.M).group(1))
    assert len(dem) == 446
    return [(dem[k], sup[k]) for k in range(446)]


def source_lists():
    z = ints(re.search(r'def zIndices : List ℕ := \[(.*?)\]', open(SRC['lemmaz']).read(), re.S).group(1))
    zs = ints(re.search(r'def zsIndices : List ℕ := \[(.*?)\]', open(SRC['lemmazs']).read(), re.S).group(1))
    cat = re.search(r'def catalog : List \(List Nat\) := \[(.*)\]', open(SRC['catdata']).read()).group(1)
    profs = [ints(x) for x in re.findall(r'\[([\d,]*)\]', cat)]
    assert len(profs) == 252 and all(len(p) == 5 for p in profs)
    return z, zs, profs


def read_rowfile(p):
    lines = open(p).read().split('\n')
    hdr = {}
    j = 0
    while not lines[j][:1].isdigit():
        k, _, v = lines[j].partition(' ')
        hdr[k] = v
        j += 1
    out = []
    for line in lines[j:]:
        if not line.strip():
            continue
        rhs, size, *sup = map(int, line.split())
        assert size == len(sup), (p, line[:60])
        out.append((rhs, sorted(sup)))
    assert len(out) == int(hdr['rows']), (p, len(out), hdr.get('rows'))
    return hdr, out


def sat(rowlist, h):
    """every row (demand, support) satisfied by the 0/1 hole vector h"""
    return all(d <= sum(h[i] for i in s) for d, s in rowlist)


def main():
    res, bad = {'hashes': {}}, []
    for p, want in FILES.items():
        got = sha(p)
        ok = got.startswith(want)
        res['hashes'][p] = {'sha256': got, 'record': want, 'ok': ok}
        if not ok:
            bad.append(('hash', p))
    res['source_hashes'] = {k: hashlib.sha256(open(p, 'rb').read()).hexdigest() for k, p in SRC.items()}
    for k, want in SRC_SHA.items():
        if not res['source_hashes'][k].startswith(want):
            bad.append(('source hash', k))
    dump = olean_dump()
    srows, scuts = source_rows(), source_cuts()
    zsrc, zssrc, cat = source_lists()
    dm = [r for r in range(len(dump)) if (dump[r][0], sorted(dump[r][1])) != (srows[r][0], sorted(srows[r][1]))]
    res['olean_dump_vs_source_rows'] = {'olean_rows_dumped': len(dump), 'mismatches': dm[:5]}
    if dm:
        bad.append(('olean dump differs from source rows', dm[:5]))
    rows = dump + srows[len(dump):]
    res['row_provenance'] = {'olean_dump': [0, len(dump) - 1], 'source_level': [len(dump), 2684],
                             'cuts': 'source_level (0-445)'}
    cuts = scuts
    oth = {'ZSET': sorted(zsrc), 'ZSSET': sorted(zssrc), 'ZIDX': zsrc, 'ZSIDX': zssrc}
    res['source_support_duplicates'] = sum(len(s) != len(set(s)) for _, s in srows + scuts)
    if res['source_support_duplicates']:
        bad.append(('duplicate entries in a source support', res['source_support_duplicates']))
    lean = [(d, sorted(s)) for d, s in rows] + [(d, sorted(s)) for d, s in cuts]
    src = json.load(open(REPO + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))
    js = [(c['rhs'], sorted(c['support'])) for c in src['constraints']]
    # 1. the 3,131 checker rows = Lean rows, same order
    mism = [k for k in range(max(len(js), len(lean))) if k >= len(js) or k >= len(lean) or js[k] != lean[k]]
    res['rows_vs_json'] = {'lean': len(lean), 'json': len(js), 'mismatches': len(mism), 'first': mism[:5],
                           'json_dup_support_entries': sum(len(c['support']) != len(set(c['support'])) for c in src['constraints'])}
    if mism:
        bad.append(('rows_vs_json', mism[:5]))
    # 2. the catalog = JSON states (state indexing)
    cm = [k for k in range(252) if list(src['states'][k]) != cat[k]]
    res['catalog_vs_json_states'] = {'mismatches': cm[:5], 'state0': cat[0], 'state1': cat[1]}
    if cm or cat[0] != [0, 0, 0, 0, 0] or cat[1] != [1, 0, 0, 0, 0]:
        bad.append(('catalog', cm[:5]))
    # 3./4. Z and Z*
    zj = [i for i, f in enumerate(src['states']) if f[0] <= 4 and f[4] == 0]
    zsj = [i for i, f in enumerate(src['states']) if f[0] == 5 and f[4] >= 1]
    zrow = json.load(open(ZR + '/zrow.json'))
    zst = json.load(open(ZR + '/zstar.json'))
    zst_list = zst['zstar'] if isinstance(zst, dict) else zst
    checks = {
        'zIndices strictly increasing (Z_eq pins Lean Z to it)': oth['ZIDX'] == sorted(set(oth['ZIDX'])),
        'zsIndices strictly increasing (Zs_eq pins Lean Z* to it)': oth['ZSIDX'] == sorted(set(oth['ZSIDX'])),
        'Lean catalog: Z from profiles == zIndices': [i for i, f in enumerate(cat) if f[0] <= 4 and f[4] == 0] == oth['ZSET'],
        'Lean catalog: Z* from profiles == zsIndices': [i for i, f in enumerate(cat) if f[0] == 5 and f[4] >= 1] == oth['ZSSET'],
        'Lean Z == JSON-states Z (check A)': oth['ZSET'] == zj,
        'Lean Z == zrow.json support (check B)': len(zrow) == 1 and sorted(zrow[0]['support']) == oth['ZSET'],
        'zrow.json rhs == 15': len(zrow) == 1 and zrow[0]['rhs'] == 15,
        'Lean Z* == JSON-states Z* (check A)': oth['ZSSET'] == zsj,
        'Lean Z* == zstar.json': sorted(zst_list) == oth['ZSSET'],
        '|Z| == |Z*| == 70, disjoint': len(oth['ZSET']) == 70 == len(oth['ZSSET']) and not set(oth['ZSET']) & set(oth['ZSSET']),
        '0 in Z, 1 in Z, 0,1 not in Z*': 0 in oth['ZSET'] and 1 in oth['ZSET'] and 0 not in oth['ZSSET'] and 1 not in oth['ZSSET'],
    }
    Z, ZS = sorted(oth['ZSET']), sorted(oth['ZSSET'])
    for name, path, want in (('zzs_rows.json', ZR + '/zzs_rows.json', [(15, Z), (15, ZS)]),
                             ('zzs_rows_n54.json', ZR + '/zzs_rows_n54.json', [(16, Z), (16, ZS)])):
        got = [(c['rhs'], sorted(c['support'])) for c in json.load(open(path))]
        checks[f'{name} == [(Z,{want[0][0]}), (Z*,{want[1][0]})]'] = got == want
    for name, path in (('zstar.json', 'zstar.json'), ('zzs_rows.json', 'zzs_rows.json'), ('zzs_rows_n54.json', 'zzs_rows_n54.json')):
        checks[f'{name}: zrow copy == record copy'] = open(ZR + '/' + path, 'rb').read() == open(REC303 + '/' + path, 'rb').read()
    # 5. finder row files
    for name, extra in (('balz.rows', [(15, Z)]), ('balzs.rows', [(15, Z), (15, ZS)]),
                        ('balzs_n54.rows', [(16, Z), (16, ZS)])):
        hdr, fr = read_rowfile(ZR + '/' + name)
        checks[f'{name} == Lean rows + {[r for r, _ in extra]}'] = fr == lean + extra
    hdr, m0 = read_rowfile(ZR + '/balz_m0.rows')
    derived = [(max(0, d - (0 in s)) if 0 in s else d, [i for i in s if i != 0]) for d, s in lean + [(15, Z)]]
    checks['balz_m0.rows == state 0 removed, rhs lowered where 0 in support'] = m0 == derived
    res['checks'] = checks
    bad += [('check', k) for k, v in checks.items() if not v]
    # 6. non-vacuity witnesses on the Lean rows (exact integers)
    ones = [1] * 252
    two = [0, 0] + [1] * 250  # hole vector of a 2-point configuration (states 0 and 1 occupied)
    nv = {
        'all-ones (sum 252) satisfies 3,131 rows + Z@15': sat(lean + [(15, Z)], ones),
        'h0=h1=0, rest 1 (sum 250) satisfies 3,131 rows + Z@15 + Z*@15': sat(lean + [(15, Z), (15, ZS)], two),
        'same vector satisfies Z@17 + Z*@17': sat([(17, Z), (17, ZS)], two),
        'max demand': max(d for d, _ in lean),
        'min (|support| - demand) over Lean rows': min(len(s) - d for d, s in lean),
        'min (|support minus {0,1}| - demand) over Lean rows': min(len([i for i in s if i > 1]) - d for d, s in lean),
        'rows with demand 0': sum(d == 0 for d, _ in lean),
    }
    res['non_vacuity'] = nv
    if not (nv['all-ones (sum 252) satisfies 3,131 rows + Z@15'] and nv['h0=h1=0, rest 1 (sum 250) satisfies 3,131 rows + Z@15 + Z*@15']):
        bad.append(('non_vacuity', None))
    big = [(k, d, len(s)) for k, (d, s) in enumerate(lean) if d >= 8]
    res['rows_with_demand_ge_8'] = big
    res['bad'] = bad
    json.dump(res, open(R + '/rows_compare.json', 'w'), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'hashes'}, indent=1))
    print('hashes ok:', all(v['ok'] for v in res['hashes'].values()))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
