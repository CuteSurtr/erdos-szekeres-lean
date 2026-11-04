import sys, subprocess, os
src = open(sys.argv[1]).read()
root = sys.argv[2]
outdir = sys.argv[3]
muts = [
 ("M1 drop rd<=rb from rule-B radius hyp in orient_pos_of_phase",
  "(hB : RunMidB α β δ → ra ≤ rb ∧ rd ≤ rb)", "(hB : RunMidB α β δ → ra ≤ rb)", None, None),
 ("M2 weaken alpha<beta to alpha<=beta in alternating_iff_gaps_lt_pi",
  "theorem alternating_iff_gaps_lt_pi {α β δ : ℝ} (hab : α < β)",
  "theorem alternating_iff_gaps_lt_pi {α β δ : ℝ} (hab : α ≤ β)", None, None),
 ("M3 drop genericity g3 != pi in runMidB_iff",
  "    (hg3 : α + 2 * π - δ ≠ π) : RunMidB α β δ ↔ δ - α < π := by",
  "    (hg3 : True) : RunMidB α β δ ↔ δ - α < π := by", None, None),
 ("M4 flip sign in orient_sign_of_phase second case",
  "      orient (polar c ra α) (polar c rb β) (polar c rd δ) < 0) := by",
  "      0 < orient (polar c ra α) (polar c rb β) (polar c rd δ)) := by", None, None),
 ("M5 strict half-plane replaced by pi+1 bound in orient_polar_halfplane",
  "(hba : ra ≤ rb) (hbd : rd ≤ rb) (h1 : 0 < β - α) (h2 : 0 < δ - β) (h12 : δ - α < Real.pi) :",
  "(hba : ra ≤ rb) (hbd : rd ≤ rb) (h1 : 0 < β - α) (h2 : 0 < δ - β) (h12 : δ - α < Real.pi + 1) :", None, None),
 ("M6 replace alternation hyp by True in orient_pos_of_alternating",
  "    (halt : Alternating α β δ) :\n    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by\n  obtain ⟨g1, g2, g3⟩ := (alternating_iff_gaps_lt_pi hab hbd hda).1 halt",
  "    (halt : True) :\n    0 < orient (polar c ra α) (polar c rb β) (polar c rd δ) := by\n  obtain ⟨g1, g2, g3⟩ := (alternating_iff_gaps_lt_pi hab hbd hda).1 halt", None, None),
 ("M7 drop antipodal premise in word_dichotomy",
  "    ∀ s : Fin 6 → Bool, (∀ i : Fin 6, s (i + 3) = !s i) →\n", "    ∀ s : Fin 6 → Bool, True →\n", None, None),
 ("M8 drop r>0 in exists_polar conclusion replaced by r<0",
  "∃ r θ : ℝ, 0 < r ∧ p = polar c r θ", "∃ r θ : ℝ, r < 0 ∧ p = polar c r θ", None, None),
]
for i,(name,a,b,c,d) in enumerate(muts):
    assert src.count(a)==1, name
    s = src.replace(a,b)
    if c:
        assert s.count(c)==1, name
        s = s.replace(c,d)
    f = os.path.join(outdir, "Mutant%d.lean"%(i+1))
    open(f,'w').write(s)
    r = subprocess.run(["lake","env","lean",f], cwd=root, capture_output=True, text=True)
    out = r.stdout + r.stderr
    errs = [l for l in out.splitlines() if ': error' in l]
    flag = "declaration uses" in out
    print("%s: exit=%d errors=%d first=%s%s" % (name, r.returncode, len(errs), errs[0][len(outdir)+1:][:110] if errs else "-", " (gap warning)" if flag else ""))
