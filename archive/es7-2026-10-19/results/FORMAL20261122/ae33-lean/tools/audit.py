#!/usr/bin/env python3
"""Static audit of the Lean sources (comments stripped): forbidden tokens anywhere in code; `--selftest` plants
violations in a temporary string and checks that each is reported."""
import re, sys
from pathlib import Path

D = Path('/home/jay/research/data/formalize-20261122/ae33-lean/lean')
FORBID = ['sorry', 'admit', 'native_decide', 'implemented_by', 'extern', 'unsafe', 'axiom', 'opaque', 'partial',
          'set_option', 'ofReduceBool', 'Lean.Elab', 'macro', 'elab', '#exit', 'debug.skipKernelTC', 'csimp']


def strip(src):
    out, i, depth, n = [], 0, 0, len(src)
    while i < n:
        if src.startswith('/-', i):
            depth += 1; i += 2; continue
        if depth and src.startswith('-/', i):
            depth -= 1; i += 2; continue
        if depth:
            i += 1; continue
        if src.startswith('--', i):
            j = src.find('\n', i); i = n if j < 0 else j; continue
        if src[i] == '"':  # string literal
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == '\\' else 1
            out.append('""'); i = j + 1; continue
        out.append(src[i]); i += 1
    return ''.join(out)


def scan(name, src):
    code = strip(src)
    hits = []
    for t in FORBID:
        for m in re.finditer(r'(?<![A-Za-z0-9_.])' + re.escape(t) + r'(?![A-Za-z0-9_])', code):
            hits.append((name, t, code[:m.start()].count('\n') + 1))
    return hits


def main():
    if '--selftest' in sys.argv:
        planted = 'theorem x : True := by\n  sorry\n-- sorry in comment\n/- axiom in block -/\naxiom foo : False\n'
        h = scan('planted', planted)
        ok = sorted(t for _, t, _ in h) == ['axiom', 'sorry']
        print('selftest', 'PASS' if ok else 'FAIL', h)
        return 0 if ok else 1
    files = sorted(D.glob('AE33Enc/*.lean')) + sorted(D.glob('AE33Geo/*.lean'))
    hits = [h for f in files for h in scan(str(f.relative_to(D)), f.read_text())]
    for h in hits:
        print('FORBIDDEN', *h)
    print(f'audited {len(files)} files: {"PASS" if not hits else "FAIL"} ({len(hits)} hits)')
    return 0 if not hits else 1


if __name__ == '__main__':
    sys.exit(main())
