"""Diff audit (section mb, polish round 1): statement environments vs. map rows.

Checks, for sections/mb.tex and sections/mb.map.tsv:
- the map has one row per statement environment, in order, with the same label and kind;
- the Lean-name and file:line columns equal the \\leanref pairs of the head, in order,
  once with a tolerant split (';' with optional spaces) and once with the split regex of
  tools/make_appendix.py ('[;,]\\s+'), which is what the appendix generator uses;
- every cited file:line declares the named identifier (last name component) in the checkout.
"""
import csv
import os
import re
import sys

STAGE = sys.argv[1]
REPO = sys.argv[2]
RES = os.path.join(REPO, 'cloud/es7-2026-10-19/results')

tex = open(os.path.join(STAGE, 'sections/mb.tex'), encoding='utf-8').read()
rows = list(csv.reader(open(os.path.join(STAGE, 'sections/mb.map.tsv'), newline='', encoding='utf-8'),
                       delimiter='\t'))
header, rows = rows[0], rows[1:]
print('header', header, 'rows', len(rows))

envs = 'theorem|lemma|proposition|corollary|fact|definition|remark'
pat = re.compile(r'\\begin\{(' + envs + r')\}(\[(?:[^\[\]]|\[[^\]]*\])*\])?\s*\\label\{([^}]*)\}', re.S)
stmts = []
for m in pat.finditer(tex):
    kind, opt, label = m.group(1), m.group(2) or '', m.group(3)
    pairs = re.findall(r'\\leanref\{([^}]*)\}\{([^}]*)\}', opt)
    stmts.append((label, kind, pairs))
print('statement environments with labels:', len(stmts))
nolabel = re.findall(r'\\begin\{(' + envs + r')\}(?!(?:\[(?:[^\[\]]|\[[^\]]*\])*\])?\s*\\label)', tex)
print('environments without an immediate label:', len(nolabel))

def tolerant(s):
    return [x.strip() for x in re.split(r';\s*', s) if x.strip()]

def appendix(s):
    return [x.strip() for x in re.split(r'[;,]\s+', s) if x.strip()]

bad = 0
for i, ((label, kind, pairs), r) in enumerate(zip(stmts, rows)):
    rl, rk, rn, rf, note = r
    if rl != label or rk != kind:
        print('ORDER/KIND MISMATCH', i, label, kind, '|', rl, rk); bad += 1
    names = [p[0] for p in pairs] or ['-']
    files = [p[1] for p in pairs] or ['-']
    if tolerant(rn) != names or tolerant(rf) != files:
        print('PAIR MISMATCH (tolerant)', label); bad += 1
    if pairs and (appendix(rn) != names or appendix(rf) != files):
        print('PAIR MISMATCH (make_appendix split)', label)
        print('   names :', appendix(rn))
        print('   files :', appendix(rf))
        bad += 1
if len(stmts) != len(rows):
    print('COUNT MISMATCH', len(stmts), len(rows)); bad += 1

# every cited line declares the identifier
for label, kind, pairs in stmts:
    for name, fl in pairs:
        path, line = fl.rsplit(':', 1)
        base = REPO if path.startswith('ErdosSzekeres/') else RES
        lines = open(os.path.join(base, path), encoding='utf-8').read().split('\n')
        text = lines[int(line) - 1]
        short = name.split('.')[-1]
        if not re.search(r'(theorem|lemma|def|structure|abbrev|instance)\s+(\S+\.)?' + re.escape(short) + r'(\s|$|\{|\()', text):
            # allow the declaration keyword to be preceded by attributes / noncomputable / protected
            print('DECL NOT ON LINE', label, name, fl, '::', text.strip()[:80]); bad += 1
print('problems:', bad)
