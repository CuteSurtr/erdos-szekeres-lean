"""Generator of lean/RowChk/Tab{Ps,Can}.lean, TabTt{0..13}.lean + TabTt.lean, TabDr{0,1}.lean + TabDr.lean, saved
after the fact (run as heredocs on 22 Nov 2026 ~18:50-18:55 KST). Kernel memory accumulates over the declarations of
one file, so: ttChk one row per theorem, 5 theorems per file; drChkN 5 rows per theorem, 7 per file; psChkN and
canChkN 10 rows per theorem in one file. Do not re-run without recompiling downstream (DESIGN.md §7)."""
import sys
D = '/home/jay/research/data/formalize-20261122/n66-rowsvalid/lean/RowChk/'
if '--write' not in sys.argv:
    raise SystemExit('refusing to overwrite without --write')
def single(name, fn, step):  # TabPs / TabCan: one file
    L = ['import RowChk.Look', '', f'/-! Kernel checks of the table `{fn}` (generated). -/', '', 'namespace RowChk', '']
    chunks = []
    for s in range(0, 70, step):
        k = min(step, 70 - s)
        L.append(f'theorem {name}_{s} : (List.range\' {s} {k}).all {fn} = true := by decide +kernel')
        chunks.append(f"List.range' {s} {k}")
    L.append('')
    L.append(f'theorem {name}_all : (List.range 70).all {fn} = true := by')
    L.append(f'  have e : List.range 70 = ' + ' ++ '.join(chunks) + ' := by decide')
    L.append(f'  rw [e]; simp only [List.all_append, ' + ', '.join(f'{name}_{s}' for s in range(0, 70, step)) + ', Bool.and_self]')
    L += ['', 'end RowChk', '']
    open(D + f'Tab{name.capitalize()}.lean', 'w').write('\n'.join(L))
def files(name, fn, step, per_file):  # TabTt*/TabDr*: several files + aggregator
    starts = list(range(0, 70, step))
    groups = [starts[i:i + per_file] for i in range(0, len(starts), per_file)]
    mods = []
    for fi, ss in enumerate(groups):
        mod = f'Tab{name.capitalize()}{fi}'
        L = ['import RowChk.Look', '', f'/-! Kernel checks of the table `{fn}`, part {fi} (generated). -/', '', 'namespace RowChk', '']
        for s in ss:
            L.append(f'theorem {name}_{s} : (List.range\' {s} {min(step, 70 - s)}).all {fn} = true := by decide +kernel')
        L += ['', 'end RowChk', '']
        open(D + mod + '.lean', 'w').write('\n'.join(L)); mods.append(mod)
    chunks = [f"List.range' {s} {min(step, 70 - s)}" for s in starts]
    L = [f'import RowChk.{m}' for m in mods] + ['', f'/-! The table `{fn}` agrees on all 70 rows (generated). -/', '', 'namespace RowChk', '',
         f'theorem {name}_all : (List.range 70).all {fn} = true := by',
         f'  have e : List.range 70 = ' + ' ++ '.join(chunks) + ' := by decide',
         f'  rw [e]; simp only [List.all_append, ' + ', '.join(f'{name}_{s}' for s in starts) + ', Bool.and_self]', '', 'end RowChk', '']
    open(D + f'Tab{name.capitalize()}.lean', 'w').write('\n'.join(L))
single('ps', 'psChkN', 10); single('can', 'canChkN', 10)
files('tt', 'ttChk', 1, 5); files('dr', 'drChkN', 5, 7)
