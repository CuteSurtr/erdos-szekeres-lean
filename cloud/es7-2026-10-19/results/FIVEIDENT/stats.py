#!/usr/bin/env python3
"""stats.py RUN... : print result, conflicts, decisions, propagations, fixed, remaining-at-start, CPU s, max RSS for logs/RUN.log."""
import re, sys
from pathlib import Path
D = Path(__file__).resolve().parent / 'logs'
def num(pat, text):
    m = re.search(pat, text, re.M)
    return m.group(1) if m else '-'
print('run\tresult\tconflicts\tdecisions\tpropagations\tfixed\tremaining_at_start\tcpu_s\twall_s\tmaxrss_GB')
for r in sys.argv[1:]:
    t = (D / f'{r}.log').read_text()
    tm = (D / f'{r}.time').read_text() if (D / f'{r}.time').exists() else ''
    res = num(r'^s (\S+)', t)
    if res == '-' and re.search(r'^c UNKNOWN', t, re.M): res = 'UNKNOWN'
    wall = num(r'([\d.]+) real', tm)
    first = re.search(r'^c \{\s+\S+(?:\s+\S+){14}\s+(\d+)\s+\d+%', t, re.M)
    rss = num(r'(\d+)\s+maximum resident set size', tm)
    print('\t'.join([r, res, num(r'^c conflicts:\s+(\d+)', t), num(r'^c decisions:\s+(\d+)', t),
                     num(r'^c propagations:\s+(\d+)', t), num(r'^c fixed:\s+(\d+)', t),
                     first.group(1) if first else '-', num(r'^c total process time since initialization:\s+([\d.]+)', t), wall,
                     f'{int(rss)/1e9:.3f}' if rss != '-' else '-']))
