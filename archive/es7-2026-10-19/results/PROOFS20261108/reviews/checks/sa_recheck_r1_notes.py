"""Dry run of the appendix note conversion for the sa map rows (prints only; writes nothing)."""
import csv
import importlib.util
import sys

spec = importlib.util.spec_from_file_location('mkapp', 'tools/make_appendix.py')
mk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mk)
mk.collect_labels()
with open('sections/sa.map.tsv', newline='') as fh:
    rows = list(csv.reader(fh, delimiter='\t', quoting=csv.QUOTE_NONE))
assert rows[0] == ['label', 'kind', 'lean_name', 'file_line', 'note'], rows[0]
for r in rows[1:]:
    assert len(r) == 5, r
    for fld in r:
        mk.check_ascii(fld, r[0])
    if r[0] in sys.argv[1:] or not sys.argv[1:]:
        print(r[0])
        print('  ', mk.note_tex(r[4].strip()))
print('rows', len(rows) - 1)
