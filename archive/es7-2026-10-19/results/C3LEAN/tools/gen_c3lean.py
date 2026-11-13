#!/usr/bin/env python3
"""Write C3Cover.lean: a kernel-checked bookkeeping proof for the threefold 33-point class (m = 11, k = 7).

usage: gen_c3lean.py RESULTS_DIR OUT_DIR COMMIT [--cap=B] [--roots=N]

Inputs (read-only): RESULTS_DIR/C3FINAL/compose_files.txt and the 280 record files it lists,
RESULTS_DIR/C3FINAL/C3FINAL_mirrorh6_roots.tsv.  Output: OUT_DIR/C3Cover.lean, OUT_DIR/c3cover_keys.tsv (one row per
certified node used: root index, key, name, records), OUT_DIR/c3cover_summary.json, and two negative-control files.

A record counts only if compose.py (C3U2, cad4e050) counts it as certified: "certified" true, lrat_check "c VERIFIED",
cake_lpr "s VERIFIED UNSAT".  compose.py re-derives the CNF sha256 of every such record from the base CNF and the
node name and exits 1 on any mismatch; the C3FINAL run did so for all 116,883 of them (run_final.log, sha_checked).
The cover tree of each root is the one compose.py --mirror-h6 finds (cover.tree mirrors covered2); the Lean file
re-checks it from scratch, with its own children functions."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c3tree as T  # noqa: E402
import cover  # noqa: E402

args = [a for a in sys.argv[1:] if not a.startswith("--")]
opts = dict(a[2:].split("=") for a in sys.argv[1:] if a.startswith("--"))
R, OUT, COMMIT = args[:3]
CAP = int(opts.get("cap", 800))
NROOTS = int(opts.get("roots", 910))
os.makedirs(OUT, exist_ok=True)

D = cover.load(R)
roots = T.roots()
names = [T.node_name(r, []) for r in roots]
tsv = [l.split("\t")[0] for l in open(os.path.join(R, "C3FINAL", "C3FINAL_mirrorh6_roots.tsv")).read().splitlines()[1:]]
assert len(roots) == 910 and set(names) == set(tsv) and len(set(tsv)) == 910
assert all(T.decode_layer(T.layer_code(L)) == L for r in roots for L in r)

# hash consistency: all certified records of one node carry the same cnf_sha256
multi = {n: {h for _, _, h in v} for n, v in D["cert"].items()}
inconsistent = [n for n, h in multi.items() if len(h) != 1]
assert not inconsistent, inconsistent[:5]


def cert_of(r):
    t = cover.tree(r, [], D)
    assert t is not None, T.node_name(r, [])
    digits, ks, leaves = [], [], []
    for (lay, C), d in cover.walk(t, r, []):
        digits.append(0 if d[0] == "C" else 1 if d[0] == "L" else 1 + d[1])
        if d[0] == "C":
            nm = T.node_name(lay, C)
            assert nm in D["cert"]
            k = T.node_key(lay, C)
            assert T.decode_key(k) == (lay, C)
            ks.append(k)
            leaves.append(nm)
    assert all(0 <= x < 16 for x in digits)
    return digits, ks, leaves, t


def ds_of(digits):
    return sum(x << (4 * i) for i, x in enumerate(digits))


def hexnat(x):
    return "0x" + format(x, "X") if x else "0"


def root_code_of(layers):
    assert len(layers) == 2
    return T.layer_code(layers[0]) * 1123 + T.layer_code(layers[1])


def cert_lit(rc, digits, ks):
    assert all(0 < k < 2 ** 64 for k in ks)
    return f"⟨{rc}, {hexnat(ds_of(digits))}, {hexnat(sum(k << (64 * i) for i, k in enumerate(ks)))}⟩"


certs = [cert_of(r) for r in roots[:NROOTS]]
nleaves = sum(len(c[1]) for c in certs)
nnodes = sum(len(c[0]) for c in certs)
nsig = sum(sum(1 for x in c[0] if x >= 2) for c in certs)
nlay = sum(sum(1 for x in c[0] if x == 1) for c in certs)
# batches: consecutive roots, at most CAP cover nodes per batch (a larger root gets a batch of its own)
bounds = []
cur = curn = 0
for c in certs:
    if cur and curn + len(c[0]) > CAP:
        bounds.append(cur)
        cur = curn = 0
    cur += 1
    curn += len(c[0])
if cur:
    bounds.append(cur)
nb = len(bounds)
starts = [sum(bounds[:i]) for i in range(nb)]

# ------------------------------------------------------------------ sidecar files
with open(os.path.join(OUT, "c3cover_keys.tsv"), "w") as fh:
    fh.write("root_index\troot\tkey\tnode\tcnf_sha256\trecords\n")
    for i, c in enumerate(certs):
        for k, nm in zip(c[1], c[2]):
            recs = D["cert"][nm]
            fh.write(f"{i}\t{names[i]}\t{k}\t{nm}\t{recs[0][2]}\t{';'.join(f'{f}:{ln}' for f, ln, _ in recs)}\n")

# ------------------------------------------------------------------ controls (data)
# (a) a root whose cover starts with a sigma split: drop one certified record (key) of it
ia = next(i for i, c in enumerate(certs) if c[0] and c[0][0] >= 2 and len(c[1]) >= 8)
da, ka, _, _ = certs[ia]
ctl_missing_record = (ia, da, ka[:3] + ka[4:])
# (b) the same root: drop the subtree of the last child of its first sigma split (decisions and keys)
t = certs[ia][3]
K = t[1]
def count(sub):
    if sub[0] == "C":
        return 1, 1
    n, l = 1, 0
    for s in sub[-1]:
        a, b = count(s)
        n, l = n + a, l + b
    return n, l


tot_n = 1 + sum(count(s)[0] for s in t[2])
last_n, last_l = count(t[2][-1])
# the root's own subtree is the whole stream; the last child's subtree is the last last_n digits / last_l keys
db = da[:len(da) - last_n] if last_n else da
kb = ka[:len(ka) - last_l]
assert tot_n == len(da)
ctl_missing_sibling = (ia, db, kb, last_n, last_l)
# (c) swap two adjacent keys
kc = list(ka)
kc[1], kc[2] = kc[2], kc[1]
ctl_swapped = (ia, da, kc)
# (d) a root covered by a plain layer split whose children are all certified: drop one child (one key)
idd = next(i for i, c in enumerate(certs) if c[0][:1] == [1] and all(x == 0 for x in c[0][1:]) and len(c[1]) >= 3)
dd, kd, _, _ = certs[idd]
ctl_layer_short = (idd, dd, kd[:-1])
# (e) the certificate of root i used for root i + 1
ie = next(i for i in range(len(certs) - 1) if certs[i][1] != certs[i + 1][1])

# ------------------------------------------------------------------ Lean text
prelude = open(os.path.join(HERE, "prelude.lean")).read()
L = []
L.append(f'''/-!
# Coverage of the threefold 33-point case split (bookkeeping only)

Generated by `gen_c3lean.py` from the run records on branch `es7-cloud` (record files of `results/C3FINAL/
compose_files.txt`, unchanged between the C3FINAL snapshot f788780c and {COMMIT}).

A 3-fold symmetric set of 33 points (11 orbits of a rotation by 120°) is split by its convex layers
(`results/C3-S/soundness.md`, `results/C3H6M/soundness_h6m.md`): 11 top cases, then second layers reduced by the
mirror lemmas (Lemma 5 below `H3`, Lemma H6M below `H6(a, s)`), giving the 910 depth-2 roots; below them every next
layer (layer split) or every assignment of the σ bits of the `K` smallest free residues (σ-split, `results/C3U2/
sigma_split.md`).

This file proves, by kernel evaluation (`decide +kernel`, no `native_decide`):
1. `roots` (the depth-2 nodes of the reduced split, computed here from the definitions) has 910 elements, they are
   distinct, they are exactly the 910 roots of `C3FINAL_mirrorh6_roots.tsv`, and the reflections behave as the
   lemmas' corollaries need (involutions on the options; the kept options are one per pair plus the fixed ones).
2. `all_roots_covered`: every root is `Covered` — certified, or split with all children covered — using only the
   nodes in `certifiedKeys`. Those are the {nleaves} certified nodes of the compose.py cover tree; each is the name of
   a record that compose.py counts as certified (`certified`, lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`)
   and whose CNF SHA-256 compose.py re-derived from the base CNF and matched (all 116,883 such records matched in the
   C3FINAL run). The record behind each key is listed in `c3cover_keys.tsv`.

It checks only the combinatorics: the split's children, the reduction's bookkeeping and the coverage. It does not
check the SAT records, the CNF encoding, the hash matching itself, Lemmas 1–5 or Lemma H6M.
-/
''')
L.append("set_option Elab.async false\n")
L.append(prelude)
L.append('''
/-! ## Part 1: the 910 roots -/

/-- Boolean equality of layers. -/
def beqLayer (a b : Layer) : Bool := beqList beqTok a b


/-- A valid second-layer option on the residues not in `used`: one orbit `r` without σ, or two orbits `b < c`
with σ values in `{0, 1}`. -/
def isOption (used : List Nat) : Layer → Bool
  | [(r, s)] => Nat.blt r m && !used.contains r && Nat.beq s 2
  | [(b, sb), (c, sc)] => Nat.blt b c && Nat.blt c m && !used.contains b && !used.contains c && Nat.blt sb 2 && Nat.blt sc 2
  | _ => false

/-- The codes are pairwise distinct (checked with a bitset). -/
def distinctCodes : List Nat → Nat → Bool
  | [], _ => true
  | c :: cs, acc => !acc.testBit c && distinctCodes cs (acc ||| (1 <<< c))

/-- The set of codes as a bitset. -/
def codeSet (l : List Nat) : Nat := l.foldl (fun acc c => acc ||| (1 <<< c)) 0

/-- For each top case with `f` free residues: the options are `f + 4 C(f, 2)` distinct valid options; `refl` maps
options to valid options and is an involution; the number of options fixed by `refl`; the number of kept options;
and every pair `{O, refl O}` has a kept member, both being kept only if `O = refl O`. -/
def reflectionFacts (t : Layer) : Nat × Bool × Bool × Nat × Nat × Bool :=
  let used := t.map Prod.fst
  let O := layerOptions used
  let kept := fun o => lexLe (okey o) (okey (refl t o))
  (O.length,
   O.all (isOption used) && distinctCodes (O.map layerCode) 0,
   O.all (fun o => isOption used (refl t o) && beqLayer (refl t (refl t o)) o),
   (O.filter fun o => beqLayer (refl t o) o).length,
   (keptOptions t).length,
   O.all fun o => (kept o || kept (refl t o)) && (beqLayer (refl t o) o || !(kept o && kept (refl t o))))

theorem reflection_facts_H3 : reflectionFacts [(0, 0)] = (190, true, true, 10, 100, true) := by decide +kernel

''')
for a in range(1, 6):
    for s_ in (0, 1):
        L.append(f"theorem reflection_facts_H6_{a}_{s_} : reflectionFacts [(0, 0), ({a}, {s_})] = (153, true, true, 9, 81, true) := by\n  decide +kernel\n")
L.append(r'''
theorem topCases_eq : topCases = [[(0, 0)], [(0, 0), (1, 0)], [(0, 0), (1, 1)], [(0, 0), (2, 0)], [(0, 0), (2, 1)],
    [(0, 0), (3, 0)], [(0, 0), (3, 1)], [(0, 0), (4, 0)], [(0, 0), (4, 1)], [(0, 0), (5, 0)], [(0, 0), (5, 1)]] := by
  decide +kernel

/-- One-orbit and two-orbit kept second layers per top case (strata of `results/C3U2/open_roots.tsv`). -/
theorem strata :
    topCases.map (fun t => ((keptOptions t).filter (·.length == 1)).length) = List.replicate 11 5 ∧
    topCases.map (fun t => ((keptOptions t).filter (·.length == 2)).length) = 95 :: List.replicate 10 76 := by
  decide +kernel

''')


def root_code(name):
    lay, C = T.parse_node(name)
    assert len(lay) == 2 and not C
    return T.layer_code(lay[0]) * 1123 + T.layer_code(lay[1])


L.append(f'''/-- The `root` column of `results/C3FINAL/C3FINAL_mirrorh6_roots.tsv` (file order), as root codes. -/
def tsvRootCodes : List Nat := [{', '.join(str(root_code(n)) for n in tsv)}]

/-! ## Part 2: coverage

`certs` holds one cover certificate per root, in `roots` order (written by `gen_c3lean.py` from the compose.py cover
tree). `checkRoot` re-derives every child itself, so a certificate only says which split to use where and names the
certified nodes; a wrong or missing piece makes the check fail.
''')
L[-1] += "-/\n"
for b in range(nb):
    lo, hi = starts[b], starts[b] + bounds[b]
    body = ",\n  ".join(cert_lit(root_code_of(roots[i]), certs[i][0], certs[i][1]) for i in range(lo, hi))
    L.append(f"/-- Certificates of roots {lo} … {hi - 1}. -/\ndef certs{b} : List Cert := [\n  {body}]\n")
L.append("/-- The cover certificates, one per root (appends nested to the right). -/\ndef certs : List Cert := " +
         " ++ (".join(f"certs{b}" for b in range(nb)) + ")" * (nb - 1) + "\n")
L.append(f"/-- Batch sizes (number of roots per batch theorem; at most {CAP} cover nodes per batch). -/\n"
         f"def bounds : List Nat := [{', '.join(map(str, bounds))}]\n")
L.append(f'''/-- The derived roots are 910 depth-2 nodes, each recovered from its root code. -/
theorem roots_match :
    roots.length = 910 ∧ roots.all (fun ρ => beqNode (decodeRoot (rootCode ρ)) ρ) = true := by
  decide +kernel

/-- The root codes of the derived roots are the root codes of the certificates, in order. -/
theorem roots_codes_match : beqList Nat.beq (roots.map rootCode) (certs.map Cert.root) = true := by
  decide +kernel

/-- The certificates' root codes are 910 distinct codes, exactly the 910 distinct codes of the TSV roots. Together
with `roots_match`: the derived roots are distinct and are exactly the roots of `C3FINAL_mirrorh6_roots.tsv`. -/
theorem roots_eq_tsv :
    tsvRootCodes.length = 910 ∧ distinctCodes tsvRootCodes 0 = true ∧
    distinctCodes (certs.map Cert.root) 0 = true ∧ codeSet (certs.map Cert.root) = codeSet tsvRootCodes := by
  decide +kernel

/-- The keys of the certified nodes used by the certificates ({nleaves} keys, all distinct; counted by
`audit_keys.py`). -/
def certifiedKeys : List Nat := certs.flatMap Cert.keys
''')
for b in range(nb):
    L.append(f"/-- Roots {starts[b]} … {starts[b] + bounds[b] - 1}. -/\n"
             f"theorem batch{b} : certs{b}.all (fun c => checkRoot (decodeRoot c.root) c) = true := by\n  decide +kernel\n")
chain = f"batch{nb - 1}"
for b in range(nb - 2, -1, -1):
    chain = f"all_append_of batch{b} ({chain})"
L.append(f'''theorem all_checked : certs.all (fun c => checkRoot (decodeRoot c.root) c) = true :=
  {chain}

/-- **Every depth-2 root of the reduced split is covered**, using only certified nodes named in `certifiedKeys`. -/
theorem all_roots_covered : ∀ ρ ∈ roots, Covered (fun n => ∃ k ∈ certifiedKeys, decodeKey k = n) ρ := by
  intro ρ hρ
  obtain ⟨_, hrt⟩ := roots_match
  have hmap : roots.map rootCode = certs.map Cert.root :=
    beqList_eq (fun a b h => Nat.eq_of_beq_eq_true h) _ _ roots_codes_match
  have hcode : rootCode ρ ∈ certs.map Cert.root := by rw [← hmap]; exact List.mem_map.mpr ⟨ρ, hρ, rfl⟩
  obtain ⟨c, hc, hcr⟩ := List.mem_map.mp hcode
  have hdec : decodeRoot c.root = ρ := by rw [hcr]; exact beqNode_eq (List.all_eq_true.mp hrt ρ hρ)
  have hchk : checkRoot (decodeRoot c.root) c = true := List.all_eq_true.mp all_checked c hc
  rw [hdec] at hchk
  exact (checkRoot_sound hchk).mono fun n ⟨k, hk, he⟩ => ⟨k, List.mem_flatMap.mpr ⟨c, hc, hk⟩, he⟩
''')
# controls
ia_, da_, ka_ = ctl_missing_record
ib_, db_, kb_, ln_, ll_ = ctl_missing_sibling
ic_, dc_, kc_ = ctl_swapped
id_, dd_, kd_ = ctl_layer_short
L.append(f'''/-! ## Negative controls -/

/-- Root {ia_} (`{names[ia_]}`) with one certified record (the fourth key) removed: the check fails. -/
theorem control_missing_record : checkRoot (decodeRoot {root_code_of(roots[ia_])}) {cert_lit(root_code_of(roots[ia_]), da_, ka_)} = false := by
  decide +kernel

/-- Root {ib_} with the subtree of the last child of its first σ-split removed ({ln_} decisions, {ll_} keys): fails. -/
theorem control_missing_sigma_child : checkRoot (decodeRoot {root_code_of(roots[ib_])}) {cert_lit(root_code_of(roots[ib_]), db_, kb_)} = false := by
  decide +kernel

/-- Root {ic_} with two certified nodes swapped: fails. -/
theorem control_swapped_keys : checkRoot (decodeRoot {root_code_of(roots[ic_])}) {cert_lit(root_code_of(roots[ic_]), dc_, kc_)} = false := by
  decide +kernel

/-- Root {id_} (`{names[id_]}`, a layer split into certified children) with its last child dropped: fails. -/
theorem control_missing_layer_child : checkRoot (decodeRoot {root_code_of(roots[id_])}) {cert_lit(root_code_of(roots[id_]), dd_, kd_)} = false := by
  decide +kernel

/-- The certificate of root {ie} does not cover root {ie + 1}. -/
theorem control_wrong_root : checkRoot (decodeRoot {root_code_of(roots[ie + 1])}) (certs.getD {ie} ⟨0, 0, 0⟩) = false := by
  decide +kernel

/-- Dropping the fixed points (strict `<` in the reduction) would leave 810 roots, not 910. -/
theorem control_strict_reduction :
    (topCases.flatMap fun t => (layerOptions (t.map Prod.fst)).filter fun o =>
      lexLe (okey o) (okey (refl t o)) && !beqLayer o (refl t o)).length = 810 := by
  decide +kernel

/-- φ without the `[s = 0]` term: the kept options below `H6(1, 0)` would not all be TSV roots. -/
theorem control_phi_mutant :
    ((layerOptions [0, 1]).filter fun o =>
      lexLe (okey o) (okey (sortTok (o.map fun t => ((1 + m - t.1) % m,
        if t.2 = 2 then 2 else t.2 ^^^ (if t.1 < 1 then 1 else 0)))))).all
      (fun o => (codeSet tsvRootCodes).testBit (rootCode ⟨[[(0, 0), (1, 0)], o], []⟩)) = false := by
  decide +kernel

end C3Cover
''')
for th in ["reflection_facts_H3"] + [f"reflection_facts_H6_{a}_{s}" for a in range(1, 6) for s in (0, 1)] + ["topCases_eq", "strata", "roots_match", "roots_codes_match", "roots_eq_tsv", "all_checked",
           "all_roots_covered", "control_missing_record", "control_missing_sigma_child", "control_swapped_keys",
           "control_missing_layer_child", "control_wrong_root", "control_strict_reduction", "control_phi_mutant",
           "run_sound", "checkRoot_sound"]:
    L.append(f"#print axioms C3Cover.{th}")
text = "\n".join(L) + "\n"
open(os.path.join(OUT, "C3Cover.lean"), "w").write(text)

# ------------------------------------------------------------------ compile-failure controls (separate files)
for tag, (i, dg, ks) in {"record": (ia_, da_, ka_), "sibling": (ib_, db_, kb_)}.items():
    ctext = (prelude + f"\nset_option maxRecDepth 100000 in\n/-- Control ({tag}): must FAIL to compile. -/\n"
             f"theorem control_{tag}_must_fail : checkRoot (decodeRoot {root_code_of(roots[i])}) {cert_lit(root_code_of(roots[i]), dg, ks)} = true := by\n"
             f"  decide +kernel\n\nend C3Cover\n")
    open(os.path.join(OUT, f"Control_{tag}.lean"), "w").write(ctext)

summary = dict(commit=COMMIT, records=D["nrec"], certified_records=D["ncert_rec"], certified_nodes=len(D["cert"]),
               roots=NROOTS, cap=CAP, batches=nb, cover_nodes=nnodes, certified_leaves=nleaves,
               sigma_splits=nsig, layer_splits=nlay,
               lean_sha256=hashlib.sha256(text.encode()).hexdigest(),
               controls=dict(missing_record=ia_, missing_sigma_child=[ib_, ln_, ll_], swapped=ic_,
                             missing_layer_child=id_, wrong_root=ie))
json.dump(summary, open(os.path.join(OUT, "c3cover_summary.json"), "w"), indent=1)
print(json.dumps(summary))
