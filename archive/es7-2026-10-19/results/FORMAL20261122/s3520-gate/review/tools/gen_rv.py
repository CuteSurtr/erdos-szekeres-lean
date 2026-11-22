# Reviewer: write review/lean/RV3520.lean, the ONE review compile.
#  - my own typed statement of RS3520.U2080.root (path from tools/rv_master.py) checked by `example`-style theorems;
#  - the catalog constant tied to Res118 (RS.cat3520_ok) and the Final glue re-typed by me;
#  - #print axioms for U2080.root, RS.cat3520_ok, my theorems and all 75 chunk axiom targets (no profiler);
#  - negative controls proved in the kernel as `checkF2 ... = false`: the worker's corrupted block, and the genuine
#    block at budget 36 (my own perturbation);
#  - the imported module list (#eval) for a one-provider audit.
import json, re, sys
G = '/home/jay/research/data/formalize-20261122/s3520-gate'
R = G + '/review'
path = open(R + '/logs/path4274.txt').read().strip()
targets = json.load(open(R + '/logs/axtargets.json'))
mods = sorted({t[0] for t in targets})
bad_src = open(G + '/controls/neg2080/src/RS3520/C208021.lean').read().split('\n')
orig_src = open(G + '/export/3520/src/RS3520/C208021.lean').read().split('\n')
bad_def = [l for l in bad_src if l.startswith('noncomputable def b231858 : PTree := ')]
assert len(bad_def) == 1
bad_def = bad_def[0].replace('noncomputable def b231858 :', 'noncomputable def rvBad231858 :', 1)
chk = [l for l in orig_src if l.startswith('theorem chk231858 : ')]
assert len(chk) == 1
m = re.match(r'theorem chk231858 : checkF2 fcatS3520 4642 154 35 (\d+) 16777216 137438953472 16 b231858 (\(pmask \(zerosF 154\) \[.*?\]\)) = true := by decide \+kernel$', chk[0])
assert m, 'unexpected chk231858 shape'
base, mask = m.group(1), m.group(2)
L = []
L += ['import RS3520.U2080'] + [f'import {x}' for x in mods if not x.startswith('RS3520.C2080')]
L += ['import RS.Bridge3520', 'import Res118.Final', '']
L += ['set_option maxRecDepth 100000', 'set_option Elab.async false', 'set_option linter.all false', '']
L += ['namespace RV3520', '']
L += ['/-- My own text of the context-level statement for ctx-4274 (path from my master walker). -/',
      f'theorem rv_stmt : ¬ ∃ holes : Fin 154 → ℕ, CompactChecker.FFeas CompactChecker.fcatS3520 4642 154 35 (CompactChecker.pmask (CompactChecker.zerosF 154) {path}) holes := RS3520.U2080.root', '']
L += ['/-- The catalog constant of the gate is the one bridged to Res118 rows P ++ Q ++ A for (B, T) = (35, 20). -/',
      'theorem rv_cat : Res118.SliceCatalog CompactChecker.fcatS3520 (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20 := RS.cat3520_ok', '',
      'theorem rv_rows : 2652 + (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA).length = 4642 := by',
      '  rw [List.length_append, List.length_append, Res118.rows_lengths.1, Res118.rows_lengths.2.1, Res118.rows_lengths.2.2.2]', '',
      '/-- Glue re-typed: a root exclusion at the residual root gives Res118\'s hypothesis s35_20 verbatim. -/',
      'theorem rv_glue (h : ¬ ∃ holes : Fin 154 → ℕ, CompactChecker.FFeas CompactChecker.fcatS3520 4642 154 35 (CompactChecker.pmask (CompactChecker.zerosF 154) [(0, 2)]) holes) :',
      '    Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20 := by',
      '  apply Res118.slice_of_root rv_cat', '  rw [rv_rows]', '  exact h', '']
L += ['open CompactChecker in', bad_def, '']
L += ['open CompactChecker in',
      f'theorem rv_pos : checkF2 fcatS3520 4642 154 35 {base} 16777216 137438953472 16 RS3520.C208021.b231858 {mask} = true := RS3520.C208021.chk231858', '',
      'open CompactChecker in',
      f'theorem rv_neg_worker : checkF2 fcatS3520 4642 154 35 {base} 16777216 137438953472 16 rvBad231858 {mask} = false := by decide +kernel', '',
      'open CompactChecker in',
      f'theorem rv_neg_budget36 : checkF2 fcatS3520 4642 154 36 {base} 16777216 137438953472 16 RS3520.C208021.b231858 {mask} = false := by decide +kernel', '',
      'end RV3520', '']
L += ['#check @RS3520.U2080.root', '#print axioms RS3520.U2080.root', '#print axioms RS.cat3520_ok']
L += [f'#print axioms RV3520.{t}' for t in ('rv_stmt', 'rv_cat', 'rv_rows', 'rv_glue', 'rv_pos', 'rv_neg_worker', 'rv_neg_budget36')]
L += [f'#print axioms {mod}.{t}' for mod, t, _ in targets]
L += ['', 'open Lean in', '#eval show CoreM Unit from do', '  for m in (← getEnv).header.moduleNames do', '    IO.println s!"MODULE {m}"', '']
open(R + '/lean/RV3520.lean', 'w').write('\n'.join(L))
print('wrote', R + '/lean/RV3520.lean', 'imports', 1 + len([x for x in mods if not x.startswith('RS3520.C2080')]) + 2, 'axiom targets', len(targets))
