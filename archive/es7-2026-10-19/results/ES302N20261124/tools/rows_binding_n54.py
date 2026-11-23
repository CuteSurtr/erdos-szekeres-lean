#!/usr/bin/env python3
"""rows_binding_n54.py (b69-prep, 22 Nov 2026). Own code, written for this item; it does not call the record's
rows_match.py. It asserts that the rows of the budget-69 finder are the rows of the Lean statement
OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69 (ES303N20261120/BalancedBudgetsZZsN.lean):
 A. zrow/balzs_n54.rows (sha256 pinned): rows 0..3130 = the catalog constraints in order, compared as ordered lists
    (support list, rhs); row 3131 = (zrow.json support, 16); row 3132 = (zstar.json support, 16); 3,133 rows in all.
 B. Z and Z* recomputed from the catalog states (f0 <= 4 and f4 = 0; f0 = 5 and f4 >= 1) equal those supports, and
    zrow/zzs_rows_n54.json (balcheck2's extra rows) is the same two rows at rhs 16.
 C. Lean source text: zIndices (LemmaZ.lean) and zsIndices (LemmaZStar.lean) are the JSON supports (Z_eq and Zs_eq
    pin Lean's Z and Zs to them by decide +kernel); ExcludesHoleBudgetZZsN is the expected definition (both extra rows
    at demand r, total <= budget, holes 0 = holes 1 = 0, 0/1 holes, the OmissionBalanced and BalancedCoverCutsV2 rows);
    composition_302_n54 takes ExcludesHoleBudgetZZsN 16 69, so r = 16 for both extra rows and the budget is 69.
 D. Lean rows = catalog rows: OmissionBalanced.row r = rowChunks[r/128]![r%128]!, rowChunks = #[rows0 .. rows2560] in
    order, chunks of exactly 128 entries (the last 125: a short chunk would silently yield a default row), support and
    demand = components 1 and 2 (2,685 rows); BalancedCoverCutsV2.support = ![support0 .. support445] in order and
    demand = 446 literals. Compared with catalog constraints 0..2684 and 2685..3130 (support as a set, demand = rhs).
Inherited assumption, not checked here: the chain311 oleans of the Lean build were compiled from the chain311/src
files parsed in D (the comp-audit pinned the oleans, not their sources).
Self-test (run first): zrow/balzs.rows (rhs 15) must fail exactly at rows 3131 and 3132, and a copy of the n54 rows
with one catalog row changed must fail. Exit 0 iff the self-test behaves and every assertion holds.
usage: python3 -I -B rows_binding_n54.py
"""
import hashlib, json, re, sys

ZR = '/home/jay/research/data/bal186-20261119/zrow/'
REC = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/'
SRC = '/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05/build/chain311/src/'
CAT = '/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'
PINS = {  # from ES303N20261120 sections 6/7, ES305N20261119 section 7 and STATUS20261121_1930 section 6
    ZR + 'balzs_n54.rows': '9e2dc29a81b54cdc0b4977d433f31d2c1fbcb64a0c4a11d8c18fdda517b66ebb',
    CAT: 'acaf6323a2539be869304f42263f80a87db95be1b998e41638dba9bca4d63d72',
    ZR + 'zrow.json': 'b43ba5f80582f7754fe6acf04cbbf81fc7822a5f784fb8c5ddedf643cce51258',
    ZR + 'zstar.json': '26d8886058cc53972dfe274e04150c4aee0ff4fffafb974a8c7c89cd57cef328',
    ZR + 'zzs_rows_n54.json': '8419984cc6477d76a32b383dd1f0b05f94aac53efdfd3047085be97e83480a6a',
    REC + 'ES303N20261120/BalancedBudgetsZZsN.lean': '4cfface86e87798e34e60c98228a757505f13ea491c763a2caa67b73b41203f7',
    REC + 'ES303N20261120/LemmaZStar.lean': '47bd1f5618ee515b4f9f5c398bd6239b1c650a16dc6aa1ae687b7dafd49fd61c',
    REC + 'ES305N20261119/LemmaZ.lean': 'e6b28efaa80cb2158180daf12dd4ce76cf2b86cc833ae9d79b1c08ffca005d65',
}
EXPECTED_DEF = """def ExcludesHoleBudgetZZsN (r budget : ℕ) : Prop :=
  ¬ ∃ holes : Fin 252 → ℕ, holes 0 = 0 ∧ holes 1 = 0 ∧ (∀ i, holes i ≤ 1) ∧
    (∀ q, OmissionBalanced.demand q ≤ ∑ i ∈ OmissionBalanced.support q, holes i) ∧
    (∀ q, BalancedCoverCutsV2.demand q ≤ ∑ i ∈ BalancedCoverCutsV2.support q, holes i) ∧
    r ≤ ∑ i ∈ OmissionZRow.Z, holes i ∧ r ≤ ∑ i ∈ OmissionZStarRow.Zs, holes i ∧
    (∑ i, holes i) ≤ budget"""
EXPECTED_302 = """theorem composition_302_n54 (trees : ExcludesHoleBudgetZZsN 16 69) (n66 : OmissionZRow.N66Bound 54)
    (hR : Partition.ResidualBound 118) : ForcesConvexNGon 302 8 :="""


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def norm(s):
    return ' '.join(s.split())


def parse_rows(path):
    """FASTBB-ROWS: header 'key value' lines, then one row per line: rhs size i_1 .. i_size"""
    hdr, rows = {}, []
    for line in open(path):
        t = line.split()
        if not t:
            continue
        if t[0].isdigit():
            v = [int(x) for x in t]
            assert len(v) == 2 + v[1], ('row length', len(rows))
            rows.append((v[2:], v[0]))
        else:
            assert not rows, 'header line after the rows'
            hdr[t[0]] = ' '.join(t[1:])
    return hdr, rows


def check_rows(hdr, rows, cons, Z, Zs, rhs):
    bad = []
    if hdr.get('states') != '252' or hdr.get('rows') != str(len(rows)) or len(rows) != 3133:
        bad.append(f"header/count: states {hdr.get('states')} rows {hdr.get('rows')} parsed {len(rows)}")
    for k, (sup, d) in enumerate(rows):
        if len(set(sup)) != len(sup) or not all(0 <= i < 252 for i in sup) or not 0 <= d <= len(sup):
            bad.append(f'row {k}: invalid support or rhs')
    want = [(c['support'], c['rhs']) for c in cons] + [(Z, rhs), (Zs, rhs)]
    bad += [f'row {k} differs from the expected (support list, rhs)' for k in range(min(len(rows), 3133))
            if rows[k] != want[k]]
    return bad


def lean_list(text, name):
    m = re.search(r'def ' + name + r' : List ℕ := \[([0-9,\s]*)\]', text)
    return [int(x) for x in m.group(1).replace('\n', ' ').split(',')]


def main():
    out, bad = [], []
    for p, h in PINS.items():
        got = sha(p)
        out.append(f'{p} sha256 {got}' + ('' if got == h else f' != PIN {h}'))
        if got != h:
            bad.append(f'pin {p}')
    for f in ('BalancedProof/Catalog.lean', 'BalancedCoverCutsV2.lean'):
        out.append(f'{SRC + f} sha256 {sha(SRC + f)} (chain311 src; recorded, no pin)')
    cat = json.load(open(CAT)); cons = cat['constraints']; st = cat['states']
    assert len(cons) == 3131 and len(st) == 252
    Z = [i for i, f in enumerate(st) if f[0] <= 4 and f[4] == 0]
    Zs = [i for i, f in enumerate(st) if f[0] == 5 and f[4] >= 1]
    # B: JSON supports and balcheck2's extra rows
    zj = json.load(open(ZR + 'zrow.json')); sj = json.load(open(ZR + 'zstar.json'))
    ex = json.load(open(ZR + 'zzs_rows_n54.json'))
    if not (len(Z) == len(Zs) == 70 and zj[0]['support'] == Z and sj['zstar'] == Zs):
        bad.append('B: Z / Z* from the catalog states differ from zrow.json / zstar.json')
    if [(r['support'], r['rhs']) for r in ex] != [(Z, 16), (Zs, 16)]:
        bad.append('B: zzs_rows_n54.json is not [(Z, 16), (Z*, 16)]')
    # self-test: rhs-15 file and a mutated copy must fail
    h15, r15 = parse_rows(ZR + 'balzs.rows')
    st15 = check_rows(h15, r15, cons, Z, Zs, 16)
    hdr, rows = parse_rows(ZR + 'balzs_n54.rows')
    s0 = rows[1234][0]; mut = list(rows); mut[1234] = (s0[:-1] + [min(set(range(252)) - set(s0))], rows[1234][1])
    stm = check_rows(hdr, mut, cons, Z, Zs, 16)
    selftest = st15 == ['row 3131 differs from the expected (support list, rhs)',
                        'row 3132 differs from the expected (support list, rhs)'] and \
        stm == ['row 1234 differs from the expected (support list, rhs)']
    out.append(f'SELFTEST balzs.rows (rhs 15) failures: {st15}; mutated row 1234 failures: {stm}; '
               f"{'behaves' if selftest else 'DOES NOT BEHAVE'}")
    if not selftest:
        bad.append('self-test')
    # A: the n54 rows
    a = check_rows(hdr, rows, cons, Z, Zs, 16)
    bad += ['A: ' + x for x in a]
    out.append(f"A: balzs_n54.rows header states={hdr.get('states')} rows={hdr.get('rows')} "
               f"base_rows={hdr.get('base_rows')} (base_rows is parsed but unused by fastbb256.cpp); "
               f'{len(rows)} rows parsed; failures {len(a)}')
    # C: Lean statement and Z/Z* index lists
    lz = open(REC + 'ES305N20261119/LemmaZ.lean').read()
    lzs = open(REC + 'ES303N20261120/LemmaZStar.lean').read()
    zn = open(REC + 'ES303N20261120/BalancedBudgetsZZsN.lean').read()
    if lean_list(lz, 'zIndices') != Z or 'theorem Z_eq : ∀ i : Fin 252, i ∈ Z ↔ i.val ∈ zIndices := by' not in lz:
        bad.append('C: zIndices / Z_eq')
    if lean_list(lzs, 'zsIndices') != Zs or 'theorem Zs_eq : ∀ i : Fin 252, i ∈ Zs ↔ i.val ∈ zsIndices := by' not in lzs:
        bad.append('C: zsIndices / Zs_eq')
    if 'namespace OmissionZRow' not in lz or 'namespace OmissionZStarRow' not in lzs:
        bad.append('C: Z / Zs namespaces')
    d0 = zn.index('def ExcludesHoleBudgetZZsN'); d1 = zn.index('\n\n', d0)
    if norm(zn[d0:d1]) != norm(EXPECTED_DEF) or zn.count('def ExcludesHoleBudgetZZsN') != 1:
        bad.append('C: definition text of ExcludesHoleBudgetZZsN')
    if norm(EXPECTED_302) not in norm(zn) or zn.count('theorem composition_302_n54') != 1:
        bad.append('C: composition_302_n54 signature')
    ns0 = zn.index('namespace OmissionBalancedZZsN'); ns1 = zn.index('end OmissionBalancedZZsN')
    if not ns0 < d0 < ns1:
        bad.append('C: definition outside namespace OmissionBalancedZZsN')
    # D: Lean rows vs catalog
    c = open(SRC + 'BalancedProof/Catalog.lean').read()
    blocks = re.findall(r'^def rows(\d+) : Array \(Finset \(Fin 252\) × ℕ × ℕ\) := #\[\n(.*?)\n\]', c, re.S | re.M)
    lean = []; chunk_ok = True
    for j, (start, body) in enumerate(blocks):
        ent = re.findall(r'\(\{([0-9, ]+)\}, (\d+), \d+\)', body)
        if int(start) != 128 * j or len(ent) != (128 if j < 20 else 125) or body.count('({') != len(ent):
            chunk_ok = False
        lean += [(sorted(int(x) for x in s.split(',')), int(d)) for s, d in ent]
    chunks = '#[' + ', '.join(f'rows{128 * j}' for j in range(21)) + ']'
    defs = ['def rowChunks := ' + chunks, 'def row (r : Fin 2685) := (rowChunks[r.val / 128]!)[r.val % 128]!',
            'def support (r : Fin 2685) : Finset (Fin 252) := (row r).1', 'def demand (r : Fin 2685) : ℕ := (row r).2.1']
    if len(blocks) != 21 or not chunk_ok or len(lean) != 2685 or not all(('\n' + x + '\n') in c for x in defs) \
            or not c.startswith('import ErdosSzekeres.OmissionPacking') or c.count('\nnamespace OmissionBalanced\n') != 1:
        bad.append(f'D: OmissionBalanced rows structure (blocks {len(blocks)}, chunk sizes ok {chunk_ok}, rows {len(lean)})')
    v = open(SRC + 'BalancedCoverCutsV2.lean').read()
    sup = dict(re.findall(r'^def support(\d+) : Finset \(Fin 252\) := \{([0-9, ]+)\}$', v, re.M))
    dm = re.search(r'^def demand : Fin 446 → ℕ := !\[([0-9, ]+)\]$', v, re.M)
    order = '![' + ', '.join(f'support{k}' for k in range(446)) + ']'
    dem = [int(x) for x in dm.group(1).split(',')] if dm else []
    if len(sup) != 446 or len(dem) != 446 or ('\ndef support : Fin 446 → Finset (Fin 252) := ' + order + '\n') not in v \
            or '\nnamespace BalancedCoverCutsV2\n' not in v:
        bad.append(f'D: BalancedCoverCutsV2 structure (supports {len(sup)}, demands {len(dem)})')
    else:
        lean += [(sorted(int(x) for x in sup[str(k)].split(',')), dem[k]) for k in range(446)]
    mis = [k for k, (cc, (s, d)) in enumerate(zip(cons, lean)) if sorted(cc['support']) != s or cc['rhs'] != d]
    if len(lean) != 3131 or mis:
        bad.append(f'D: Lean rows vs catalog: {len(lean)} rows, {len(mis)} mismatches {mis[:10]}')
    out.append(f'D: Lean rows parsed {len(lean)} (2,685 OmissionBalanced in 21 chunks + 446 cover cuts); '
               f'mismatches vs catalog {len(mis)}')
    if not bad:
        out.append('ASSERTED: balzs_n54.rows rows 0..3130 = catalog constraints in order (ordered support lists, rhs); '
                   'row 3131 = Z-row = zrow.json support (70), rhs 16; row 3132 = Z*-row = zstar.json support (70), '
                   'rhs 16; zzs_rows_n54.json = the same two rows at rhs 16')
        out.append('ASSERTED: Lean zIndices = zrow.json support, zsIndices = zstar.json support (Z_eq, Zs_eq); '
                   'ExcludesHoleBudgetZZsN r budget has both extra rows at demand r and total <= budget; '
                   'composition_302_n54 uses ExcludesHoleBudgetZZsN 16 69 (r = 16, budget 69)')
        out.append('ASSERTED: Lean OmissionBalanced.row r = rowChunks[r/128]![r%128]!, rowChunks = #[rows0, ..., rows2560] '
                   'in order, 20 chunks of 128 and one of 125 (2,685 rows), support/demand = components 1/2; '
                   'BalancedCoverCutsV2.support = ![support0..support445], 446 demands; all 3,131 equal the catalog '
                   'rows in order (support sets, demand = rhs)')
        out.append('So the tree rows (catalog + Z-row + Z*-row at rhs 16, budget 69) are the rows of '
                   'OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69. Inherited assumption: the chain311 oleans '
                   'were compiled from the parsed chain311/src files.')
    out.append('RESULT: ' + ('PASS' if not bad else 'FAIL ' + '; '.join(bad)))
    print('\n'.join(out))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
