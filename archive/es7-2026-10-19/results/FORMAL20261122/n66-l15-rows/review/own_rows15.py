#!/usr/bin/env python3
"""Reviewer's own static check of the level-15 row data (n66-l15-rows). Reads only; writes review/own_rows15.json.

* parses the Std-only chunk constants rows<k> (N66R15Enc/RowsD*.lean), rowsAll (RowList.lean), rowChunks
  (N66R15Chk/RowsAll.lean) and the certificates just<k> (N66R15Chk/Rows*.lean) with its own bracket parser;
* compares the concatenation (rowsAll order) with n66-level15's rows_used15.txt (byte level, after the same
  "a b c" formatting) and with n66enc's level-14 rows_used.txt (shared / new);
* checks the pairing rows<k>/just<k> (same length), the template/core index ranges, and the docstring ids of the
  templates/cores against n66-rowsvalid's certs_manifest.tsv;
* lists the certificates the new rows use (template / core ids).
"""
import hashlib, json, re, sys
from pathlib import Path

D = Path('/home/jay/research/data/formalize-20261122/n66-l15-rows')
L = D / 'lean'
ROWS15 = Path('/home/jay/research/data/formalize-20261122/n66-level15/lean/N66E15/data/rows_used15.txt')
ROWS14 = Path('/home/jay/research/data/formalize-20261122/n66enc/lean/N66Enc/data/rows_used.txt')
MAN = Path('/home/jay/research/data/formalize-20261122/n66-rowsvalid/data/certs_manifest.tsv')


def bracket(s, i):
    """s[i] == '['; return the index just after the matching ']'."""
    assert s[i] == '['
    d = 0
    for j in range(i, len(s)):
        if s[j] == '[':
            d += 1
        elif s[j] == ']':
            d -= 1
            if d == 0:
                return j + 1
    raise ValueError('unbalanced')


def defs(path, pat):
    s = path.read_text()
    out = {}
    for m in re.finditer(pat, s):
        i = m.end()
        while s[i] == ' ':
            i += 1
        j = bracket(s, i)
        k = int(m.group(1))
        assert k not in out, (path, k)
        out[k] = s[i:j]
    return out


def nat_lists(txt):
    v = json.loads(txt)
    assert isinstance(v, list) and all(isinstance(r, list) and all(isinstance(x, int) for x in r) for r in v)
    return v


def parse_rc(txt):
    """Parse a `List RC` literal: .tr t [..] | .mt t [..] | .co c | .mc c | .cy [..]."""
    assert txt[0] == '[' and txt[-1] == ']'
    s = txt[1:-1]
    i, out = 0, []
    while i < len(s):
        while i < len(s) and s[i] in ' ,\n':
            i += 1
        if i >= len(s):
            break
        m = re.compile(r'\.(tr|mt|co|mc|cy)\b').match(s, i)
        assert m, s[i:i + 40]
        kind = m.group(1)
        i = m.end()
        while s[i] == ' ':
            i += 1
        if kind in ('tr', 'mt'):
            m2 = re.compile(r'(\d+) ').match(s, i)
            t = int(m2.group(1))
            i = m2.end()
            j = bracket(s, i)
            out.append((kind, t, json.loads(s[i:j])))
            i = j
        elif kind in ('co', 'mc'):
            m2 = re.compile(r'(\d+)').match(s, i)
            out.append((kind, int(m2.group(1)), None))
            i = m2.end()
        else:
            j = bracket(s, i)
            out.append((kind, None, json.loads(s[i:j])))
            i = j
    return out


def main():
    res = {}
    rows = {}
    for f in sorted(L.glob('N66R15Enc/RowsD*.lean')):
        for k, v in defs(f, r'def rows(\d+) : List \(List Nat\) :=').items():
            assert k not in rows
            rows[k] = nat_lists(v)
    res['chunks'] = len(rows)
    assert sorted(rows) == list(range(len(rows))), 'chunk numbers not 0..n-1'
    # rowsAll
    s = (L / 'N66R15Enc/RowList.lean').read_text()
    m = re.search(r'def rowsAll : List \(List \(List Nat\)\) := \[([^\]]*)\]', s)
    names = [x.strip() for x in m.group(1).split(',')]
    res['rowsAll_is_rows0_to_rowsN_in_order'] = names == [f'rows{k}' for k in range(len(rows))]
    res['R1nat15_def'] = re.search(r'def R1nat15 : List \(List Nat\) := (.*)', s).group(1).strip()
    res['R1_15_def'] = re.search(r'def R1_15 : List \(List \(Fin 70\)\) := (.*)', s).group(1).strip()
    res['toFin70_def'] = re.search(r'def toFin70 \(x : Nat\) : Fin 70 := (.*)', s).group(1).strip()
    # rowChunks
    s = (L / 'N66R15Chk/RowsAll.lean').read_text()
    m = re.search(r'def rowChunks : List \(List \(List Nat\) × List RC\) := \[(.*?)\]\n', s)
    pairs = re.findall(r'\((rows\d+), (just\d+)\)', m.group(1))
    res['rowChunks_is_pairs_k_k_in_order'] = pairs == [(f'rows{k}', f'just{k}') for k in range(len(rows))]
    # just<k>
    just = {}
    for f in sorted(L.glob('N66R15Chk/Rows[0-9]*.lean')):
        for k, v in defs(f, r'def just(\d+) : List RC :=').items():
            assert k not in just
            just[k] = parse_rc(v)
    res['just_chunks'] = len(just)
    res['pairing_lengths_equal'] = sorted(just) == sorted(rows) and all(len(just[k]) == len(rows[k]) for k in rows)
    allrows = [r for k in range(len(rows)) for r in rows[k]]
    alljust = [j for k in range(len(rows)) for j in just[k]]
    res['rows'] = len(allrows)
    res['all_values_lt_70'] = all(0 <= x < 70 for r in allrows for x in r)
    res['all_sorted_nodup'] = all(all(r[i] < r[i + 1] for i in range(len(r) - 1)) for r in allrows)
    res['distinct_rows'] = len(set(map(tuple, allrows)))
    txt = ''.join(' '.join(map(str, r)) + '\n' for r in allrows).encode()
    ref = ROWS15.read_bytes()
    res['rows_used15_sha256'] = hashlib.sha256(ref).hexdigest()
    res['own_text_sha256'] = hashlib.sha256(txt).hexdigest()
    res['own_text_equals_rows_used15'] = txt == ref
    # level 14
    r14 = [tuple(map(int, l.split())) for l in ROWS14.read_text().splitlines() if l.strip()]
    s14 = set(r14)
    res['level14_rows'] = len(r14)
    new = [i for i, r in enumerate(allrows) if tuple(r) not in s14]
    res['shared_with_level14'] = len(allrows) - len(new)
    res['new_rows'] = len(new)
    # certificates: ids by index (docstrings) and the manifest
    tid = {}
    for f in sorted(L.glob('N66R15Enc/DataT[0-9].lean')):
        for m in re.finditer(r'/-- template ([0-9a-f]{16}) -/\ndef tmpl(\d+) : Cert', f.read_text()):
            tid[int(m.group(2))] = m.group(1)
    cid = {}
    for f in sorted(L.glob('N66R15Enc/DataC[0-9].lean')):
        for m in re.finditer(r'/-- core (C_[0-9a-f]{16}) -/\ndef core(\d+) : Cert', f.read_text()):
            cid[int(m.group(2))] = m.group(1)
    s = (L / 'N66R15Enc/DataT.lean').read_text()
    tl = re.search(r'def templates : List Cert := \[([^\]]*)\]', s).group(1)
    s = (L / 'N66R15Enc/DataC.lean').read_text()
    cl = re.search(r'def cores : List Cert := \[([^\]]*)\]', s).group(1)
    res['templates_list_is_tmpl0_to_N'] = [x.strip() for x in tl.split(',')] == [f'tmpl{k}' for k in range(len(tid))]
    res['cores_list_is_core0_to_N'] = [x.strip() for x in cl.split(',')] == [f'core{k}' for k in range(len(cid))]
    res['templates'] = len(tid)
    res['cores'] = len(cid)
    man = {}
    for line in MAN.read_text().splitlines()[1:]:
        f = line.split('\t')
        man[(f[1], int(f[0]))] = f[2]
    res['docstring_ids_equal_manifest'] = (all(man.get(('T', k)) == v for k, v in tid.items()) and
                                           all(man.get(('C', k)) in (v, v[2:]) for k, v in cid.items()) and
                                           len(man) == len(tid) + len(cid))
    # kinds and certificate use
    kinds = {}
    for j in alljust:
        kinds[j[0]] = kinds.get(j[0], 0) + 1
    res['kinds_all'] = kinds
    res['indices_in_range'] = all((j[0] in ('tr', 'mt') and j[1] < len(tid)) or (j[0] in ('co', 'mc') and j[1] < len(cid))
                                  or j[0] == 'cy' for j in alljust)
    kn = {}
    usedT, usedC = set(), set()
    for i in new:
        j = alljust[i]
        kn[j[0]] = kn.get(j[0], 0) + 1
        if j[0] in ('tr', 'mt'):
            usedT.add(j[1])
        elif j[0] in ('co', 'mc'):
            usedC.add(j[1])
    res['kinds_new'] = kn
    res['new_rows_use_templates'] = len(usedT)
    res['new_rows_use_cores'] = len(usedC)
    res['new_rows_template_ids'] = sorted(tid[t] for t in usedT)
    res['new_rows_core_ids'] = sorted(cid[c] for c in usedC)
    allT = {j[1] for j in alljust if j[0] in ('tr', 'mt')}
    allC = {j[1] for j in alljust if j[0] in ('co', 'mc')}
    res['all_rows_use_templates'] = len(allT)
    res['all_rows_use_cores'] = len(allC)
    res['t208_used_by'] = sum(1 for j in alljust if j[0] in ('tr', 'mt') and j[1] == 208)
    (D / 'review/own_rows15.json').write_text(json.dumps(res, indent=1) + '\n')
    for k, v in res.items():
        if not k.endswith('_ids'):
            print(k, v)


if __name__ == '__main__':
    main()
