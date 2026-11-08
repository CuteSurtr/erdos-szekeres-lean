#!/usr/bin/env python3
"""Completeness check of the written proofs (Stage 1): is every Lean declaration of the Stage 1 units either
restated (a \\leanref head or a statement-map row) or named in a Coverage paragraph, or inside a range that a
Coverage paragraph declares a verbatim copy / an excluded file?  Also re-checks the verbatim-copy claims.

Usage (from anywhere):  python3 completeness_check.py
Paths are derived from the location of this file: STAGE = parent of build/, REPO = STAGE/../es7.
Read-only: it reads REPO and STAGE/sections and prints a report; it writes nothing.
"""
import collections
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
STAGE = os.path.dirname(HERE)
REPO = os.path.join(os.path.dirname(STAGE), 'es7')
RES = os.path.join(REPO, 'cloud', 'es7-2026-10-19', 'results')
KEYS = ['fd', 'll', 'lg', 'oc', 'pc', 'ec', 'sr', 'ar', 'mm', 'mb', 'cb', 'sa']
UNIT_DIRS = ['LAYERLEAN', 'LEANEXT', 'SYMLEAN', 'MIRRORETV', 'C3LEAN', 'C2FINAL', 'C3L', 'AUDIT2',
             'AUDIT3/A1_reduction', 'ES7SPLIT', 'ES8SYM', 'PRIMEFOLD', 'ES8SLACK']

# ---------------------------------------------------------------- Lean declaration extractor
KW = r'(theorem|lemma|def|abbrev|structure|instance|inductive|class|opaque|axiom|example)'
MOD = r'(?:(?:private|protected|noncomputable|partial|unsafe|nonrec|scoped|local)\s+)*'
ATTR = r'(?:@\[[^\]]*\]\s*)*'
DECL = re.compile(r'^' + ATTR + MOD + KW + r'\b\s*(.*)$')


def strip_comments(lines):
    out, depth = [], 0
    for ln in lines:
        res, i = '', 0
        while i < len(ln):
            if depth > 0:
                if ln.startswith('/-', i):
                    depth += 1; i += 2; continue
                if ln.startswith('-/', i):
                    depth -= 1; i += 2; continue
                i += 1; continue
            if ln.startswith('/-', i):
                depth += 1; i += 2; continue
            if ln.startswith('--', i):
                break
            if ln[i] == '"':
                j = i + 1
                while j < len(ln) and ln[j] != '"':
                    if ln[j] == '\\':
                        j += 1
                    j += 1
                res += ln[i:j + 1]; i = j + 1; continue
            res += ln[i]; i += 1
        out.append(res)
    return out


def extract(path):
    lines = strip_comments(open(path, encoding='utf-8').read().split('\n'))
    stack, res = [], []
    for idx, ln in enumerate(lines, 1):
        s = ln.strip()
        m = re.match(r'^(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$', s)
        if m:
            stack.append(('sec', m.group(1) or '')); continue
        m = re.match(r'^namespace\s+(\S+)\s*$', s)
        if m:
            stack.append(('ns', m.group(1))); continue
        if re.match(r'^mutual\s*$', s):
            stack.append(('mutual', '')); continue
        if re.match(r'^end(?:\s+(\S+))?\s*$', s):
            if stack:
                stack.pop()
            continue
        m = DECL.match(ln)
        if m:
            kind, rest = m.group(1), m.group(2)
            if kind == 'example':
                name = '(example)'
            else:
                if kind == 'instance':
                    rest = re.sub(r'^\(priority\s*:=\s*[^)]*\)\s*', '', rest)
                nm = re.match(r"^([^\s:({\[⦃]+)", rest)
                name = nm.group(1) if nm and not rest.startswith(':') else '(anonymous)'
            ns = '.'.join(x[1] for x in stack if x[0] == 'ns' and x[1])
            full = (ns + '.' + name) if ns and not name.startswith('(') else name
            res.append((idx, kind, name, full))
    return res


# ---------------------------------------------------------------- the document
def norm(s):
    return (s.replace('\\_', '_').replace('\\textquotesingle', "'").replace('{}', '')
            .replace('\\allowbreak', ''))


TOK = re.compile(r'\\(?:lean|texttt|dirn)\{((?:[^{}]|\{[^{}]*\})*)\}')
LREF = re.compile(r'\\leanref\{([^{}]*)\}\{([^{}]*)\}')


def tokens(text):
    toks = set()
    for m in TOK.finditer(text):
        t = norm(m.group(1))
        toks.add(t)
        for part in re.split(r'[\s,;()]+', t):
            if part:
                toks.add(part.strip('.').rstrip(':'))
    return toks


heads, cov_toks = set(), {}
for k in KEYS:
    src = open(os.path.join(STAGE, 'sections', k + '.tex')).read()
    lines = src.split('\n')
    start = max(i for i, l in enumerate(lines) if re.search(r'(paragraph|subsection\*?)\{(\\textbf\{)?Coverage', l))
    cov_toks[k] = tokens('\n'.join(lines[start:]))
    for m in LREF.finditer(src):
        heads.add(norm(m.group(1)))
    with open(os.path.join(STAGE, 'sections', k + '.map.tsv')) as fh:
        rd = csv.reader(fh, delimiter='\t')
        next(rd)
        for row in rd:
            if len(row) >= 3:
                for n in re.split(r'[;,]', row[2]):
                    n = n.strip()
                    if n and n != '-':
                        heads.add(n)


def named(name, full, toks):
    if full in toks or name in toks:
        return True
    parts = full.split('.')
    return any('.'.join(parts[i:]) in toks for i in range(1, len(parts)))


# ranges that a Coverage paragraph declares verbatim copies or excluded files (file -> [(lo, hi, who)])
COPY = {
    'LAYERLEAN/logs/axioms_recheck_20261106/LayerLemmaAxioms.lean': [(1, 1148, 'lg/ll: copy of LayerLemma.lean')],
    'LEANEXT/merged/Merged.lean': [(1, 1147, 'oc (ii): copy of LayerLemma.lean 1-1147')],
    'LEANEXT/linked/Linked.lean': [(1, 1384, 'pc: copy of Merged.lean 1-1384')],
    'LEANEXT/capstone/Capstone.lean': [(19, 1424, 'pc: copy of Linked 11-1416'),
                                       (1426, 1965, 'pc: copy of PhaseClassification 6-545')],
    'LEANEXT/capstone/Capstone2.lean': [(1, 2003, 'pc: copy of Capstone 1-2003')],
    'LEANEXT/es7corr/ES7Corollaries.lean': [(1, 1147, 'ec: copy of LayerLemma 1-1147')],
    'LEANEXT/review/VacuityTest.lean': [(1, 1148, 'lg: copy of LayerLemma (lines 11-1147 claimed)')],
    'SYMLEAN/AffineReduction.lean': [(1, 1058, 'sr/ar: copy of SymmetricReduction 1-1058')],
    'SYMLEAN/SymmetricReductionAxioms.lean': [(1, 1059, 'sr: copy')],
    'SYMLEAN/AffineReductionAxioms.lean': [(1, 1533, 'ar: copy')],
    'SYMLEAN/mirror/ReductionThreeClasses.lean': [(38, 1559, 'ar: copy of AffineReduction 12-1533'),
                                                  (1562, 4236, 'mm: copy of MirrorMain 3-2677')],
    'SYMLEAN/review/ReviewSanity.lean': [(1, 10 ** 9, 'sr: audit file')],
    'SYMLEAN/review/VariantChecks.lean': [(1, 10 ** 9, 'sr: audit file')],
    'SYMLEAN/review/SupMetric.lean': [(1, 10 ** 9, 'sr: audit file')],
    'C3LEAN/tools/prelude.lean': [(1, 301, 'cb: source of C3Cover 29-329')],
    'C3LEAN/Control_record.lean': [(1, 10 ** 9, 'cb: must-fail file')],
    'C3LEAN/Control_sibling.lean': [(1, 10 ** 9, 'cb: must-fail file')],
    'C3LEAN/review/RevCtrl_mut.lean': [(1, 10 ** 9, 'cb: review controls')],
    'C3LEAN/review/RevCtrl_pass.lean': [(1, 10 ** 9, 'cb: review controls')],
    'C3LEAN/review/RevDiff.lean': [(1, 10 ** 9, 'cb: eval harness')],
}
FAMILY = ('certs', 'batch', 'reflection_facts_H6_', 'closedP')

# names that a Coverage paragraph lists only through a generic short name of ANOTHER namespace (false positives
# of the name test): they are counted as missing.
GENERIC = {'orient', 'refl', 'transport', 'V', 'main', 'Layer', 'orient_sum', 'orient_affine'}

files = []
for d in UNIT_DIRS:
    for root, _, fs in os.walk(os.path.join(RES, d)):
        for f in fs:
            if f.endswith('.lean'):
                files.append(os.path.relpath(os.path.join(root, f), RES))
files.sort()

stat = collections.Counter()
missing = collections.defaultdict(list)
for f in files:
    decls = extract(os.path.join(RES, f))
    for ln, kind, name, full in decls:
        if f.startswith('ES8SLACK/'):
            stat['excluded by the task (ES8SLACK)'] += 1
            continue
        if any(lo <= ln <= hi for lo, hi, _ in COPY.get(f, [])):
            stat['verbatim copy / excluded file (declared)'] += 1
            continue
        generic_ns = f.startswith(('MIRRORETV/review/', 'C3L/', 'AUDIT2/'))
        if full in heads and not (generic_ns and '.' not in full):
            stat['restated (head or map row)'] += 1
            continue
        if any(name.startswith(p) and name[len(p):].replace('_', '').isdigit() for p in FAMILY):
            stat['member of a generated family (head cites first member)'] += 1
            continue
        if not (generic_ns and name in GENERIC) and any(named(name, full, cov_toks[k]) for k in KEYS):
            stat['named in a Coverage paragraph'] += 1
            continue
        if kind == 'example' and f.endswith('AssembledSizes.lean'):
            stat['named in a Coverage paragraph'] += 1
            continue
        stat['NEITHER'] += 1
        missing[f].append('%d:%s:%s' % (ln, kind, name))

print('Stage 1 Lean files scanned:', len(files))
for k, v in sorted(stat.items()):
    print('  %-58s %5d' % (k, v))
print()
for f in sorted(missing):
    print('NEITHER covered nor listed: %s (%d)' % (f, len(missing[f])))
    print('   ' + ' '.join(missing[f]))

# ---------------------------------------------------------------- verbatim-copy claims
print()


def rng(path, a, b):
    with open(os.path.join(RES, path), encoding='utf-8') as fh:
        return fh.read().split('\n')[a - 1:b]


CLAIMS = [
    ('LAYERLEAN/LayerLemma.lean', 11, 1147, 'LEANEXT/capstone/Capstone.lean', 19),
    ('LAYERLEAN/LayerLemma.lean', 11, 1147, 'LEANEXT/capstone/Capstone2.lean', 19),
    ('LAYERLEAN/LayerLemma.lean', 1, 1147, 'LEANEXT/merged/Merged.lean', 1),
    ('LAYERLEAN/LayerLemma.lean', 1, 1147, 'LEANEXT/linked/Linked.lean', 1),
    ('LAYERLEAN/LayerLemma.lean', 1, 1147, 'LEANEXT/es7corr/ES7Corollaries.lean', 1),
    ('LAYERLEAN/LayerLemma.lean', 1, 1148, 'LEANEXT/review/VacuityTest.lean', 1),
    ('LAYERLEAN/LayerLemma.lean', 11, 1147, 'ENCBLEAN/geo/ES8Geo/Capstone2.lean', 19),
    ('LAYERLEAN/LayerLemma.lean', 1, 1148, 'LAYERLEAN/logs/axioms_recheck_20261106/LayerLemmaAxioms.lean', 1),
    ('LEANEXT/review/tests_tail.lean', 1, 149, 'LEANEXT/review/VacuityTest.lean', 1149),
    ('LEANEXT/merged/Merged.lean', 1, 1384, 'LEANEXT/linked/Linked.lean', 1),
    ('LEANEXT/merged/Merged.lean', 1148, 1383, 'LEANEXT/capstone/Capstone.lean', 1156),
    ('LEANEXT/merged/Merged.lean', 1148, 1383, 'LEANEXT/capstone/Capstone2.lean', 1156),
    ('LEANEXT/linked/Linked.lean', 11, 1416, 'LEANEXT/capstone/Capstone.lean', 19),
    ('LEANEXT/phase/PhaseClassification.lean', 6, 545, 'LEANEXT/capstone/Capstone.lean', 1426),
    ('LEANEXT/capstone/Capstone.lean', 1, 2003, 'LEANEXT/capstone/Capstone2.lean', 1),
    ('LEANEXT/capstone/Capstone2.lean', 1, 2132, 'ENCBLEAN/geo/ES8Geo/Capstone2.lean', 1),
    ('LEANEXT/orbit/OrbitConsistency.lean', 1, 429, 'ENCBLEAN/geo/ES8Geo/OrbitConsistency.lean', 1),
    ('LEANEXT/keys/KeyOrder.lean', 1, 158, 'ENCBLEAN/geo/ES8Geo/KeyOrder.lean', 1),
    ('SYMLEAN/SymmetricReduction.lean', 1, 1059, 'SYMLEAN/SymmetricReductionAxioms.lean', 1),
    ('SYMLEAN/SymmetricReduction.lean', 1, 1058, 'SYMLEAN/AffineReduction.lean', 1),
    ('SYMLEAN/SymmetricReduction.lean', 1, 1059, 'SYMLEAN/review/ReviewSanity.lean', 1),
    ('SYMLEAN/SymmetricReduction.lean', 1, 1059, 'SYMLEAN/review/VariantChecks.lean', 1),
    ('SYMLEAN/AffineReduction.lean', 1, 1533, 'SYMLEAN/AffineReductionAxioms.lean', 1),
    ('SYMLEAN/AffineReduction.lean', 12, 1533, 'SYMLEAN/mirror/ReductionThreeClasses.lean', 38),
    ('MIRRORETV/lean/MirrorMain.lean', 3, 2677, 'SYMLEAN/mirror/ReductionThreeClasses.lean', 1562),
    ('C3LEAN/tools/prelude.lean', 1, 301, 'C3LEAN/C3Cover.lean', 29),
    ('C3LEAN/tools/prelude.lean', 1, 301, 'C3LEAN/Control_record.lean', 1),
    ('C3LEAN/tools/prelude.lean', 1, 301, 'C3LEAN/Control_sibling.lean', 1),
    ('C3LEAN/tools/prelude.lean', 1, 301, 'C3LEAN/review/RevCtrl_mut.lean', 1),
    ('C3LEAN/tools/prelude.lean', 1, 301, 'C3LEAN/review/RevCtrl_pass.lean', 1),
    ('C3LEAN/tools/prelude.lean', 1, 301, 'C3LEAN/review/RevDiff.lean', 1),
]
for a, lo, hi, b, lo2 in CLAIMS:
    same = rng(a, lo, hi) == rng(b, lo2, lo2 + hi - lo)
    print('%s  %s:%d-%d == %s:%d-%d' % ('SAME' if same else 'DIFF', a, lo, hi, b, lo2, lo2 + hi - lo))
