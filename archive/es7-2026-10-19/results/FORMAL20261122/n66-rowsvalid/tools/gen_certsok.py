"""Generator of lean/RowChk/certsOk{T,C}F{0..3}.lean and CertsOk.lean, saved after the fact (run as a heredoc on 22 Nov
2026 ~19:02 KST): 8 chunks of templates (`certOk`) and of cores (`coreOk`), two chunk theorems per file; CertsOk
reassembles `templates.all certOk` / `cores.all coreOk` with `rfl` on the list split (maxRecDepth 100000).
Do not re-run without recompiling downstream (DESIGN.md §7)."""
import sys
D = '/home/jay/research/data/formalize-20261122/n66-rowsvalid/lean/RowChk/'
if '--write' not in sys.argv:
    raise SystemExit('refusing to overwrite without --write')
mods = []
def part(name, pre, count, nch, fn, per_file):
    per = (count + nch - 1) // nch
    lists = ['[' + ', '.join(f'{pre}{k}' for k in range(per * c, min(per * (c + 1), count))) + ']' for c in range(nch)]
    for f in range(0, nch, per_file):
        mod = f'{name}F{f // per_file}'
        L = ['import RowChk.Check', '', '/-! Kernel checks of certificate data validity (generated). -/', '', 'namespace RowChk', 'open RowEnc', '']
        for c in range(f, min(f + per_file, nch)):
            L.append(f'theorem {name}{c} : ({lists[c]} : List Cert).all {fn} = true := by decide +kernel')
        L += ['', 'end RowChk', '']
        open(D + mod + '.lean', 'w').write('\n'.join(L)); mods.append(mod)
    return lists
lt = part('certsOkT', 'tmpl', 421, 8, 'certOk', 2)
lc = part('certsOkC', 'core', 208, 8, 'coreOk', 2)
L = [f'import RowChk.{m}' for m in mods] + ['', '/-! Data validity of all 629 certificates (generated). -/', '', 'namespace RowChk', 'open RowEnc', '']
for name, which, lists, fn in [('certsOkT', 'templates', lt, 'certOk'), ('certsOkC', 'cores', lc, 'coreOk')]:
    L += ['set_option maxRecDepth 100000 in', f'theorem {name} : {which}.all {fn} = true := by',
          f'  have e : {which} = ' + ' ++ '.join(lists) + ' := rfl',
          f'  rw [e]; simp only [List.all_append, ' + ', '.join(f'{name}{c}' for c in range(8)) + ', Bool.and_self]', '']
L += ['end RowChk', '']
open(D + 'CertsOk.lean', 'w').write('\n'.join(L))
