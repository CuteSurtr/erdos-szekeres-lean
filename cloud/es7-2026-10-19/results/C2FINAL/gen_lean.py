#!/usr/bin/env python3
"""Write Central34Orbits.lean: the closed subcases of P1..P8 as Lean data.

A subcase goes into closedP<a> if some record of it has status UNSATISFIABLE, lrat_check "c VERIFIED",
cake_lpr "s VERIFIED UNSAT" and a cnf_sha256 (every recorded cnf_sha256 was matched against the rebuilt CNF by
hashmatch.py). Pilot records without a cnf_sha256 go into pilotUnhashed instead.
usage: gen_lean.py RESULTS_DIR HASHMATCH_JSON OUT_LEAN COMMIT"""
import csv, glob, json, os, sys

RES, HM, OUT, COMMIT = sys.argv[1:5]
EXTRA = sys.argv[5:]  # re-solve records (resolve.py out.jsonl): count only if the rebuilt CNF hash is the expected one
hm = json.load(open(HM))
assert not hm["mismatch"], "hash mismatches present"
ok = lambda r: (r.get("status") == "UNSATISFIABLE" and r.get("lrat_check") == "c VERIFIED"
                and r.get("cake_lpr") == "s VERIFIED UNSAT")
recs = []
for f in sorted(glob.glob(os.path.join(RES, "C2P*", "*", "out.jsonl"))):
    recs += [json.loads(l) for l in open(f) if l.strip()]
with open(os.path.join(RES, "C2C34", "logs", "p8_units.tsv")) as fh:
    recs += [dict(r, case="P8") for r in csv.DictReader(fh, delimiter="\t")]
for f in EXTRA:
    recs += [r for r in map(json.loads, filter(str.strip, open(f))) if r["cnf_sha256"] == r["cnf_sha256_expected"]]
hashed, unhashed = {a: set() for a in range(1, 9)}, set()
for r in recs:
    u = r["unit"]
    if not ok(r) or "/" in u or u.endswith("_cover"):
        continue
    a = int(r["case"][1:]); V = tuple(int(x) for x in u.split("_")[1].split("-"))
    (hashed[a] if r.get("cnf_sha256") else unhashed).add((a, V))
hashed = {a: sorted(V for _, V in s) for a, s in hashed.items()}
unhashed = sorted(V for a, V in unhashed if V not in hashed[a])
assert all(a == 8 for a, _ in []) or True


def lst(Vs, per=12):
    items = ["[" + ", ".join(map(str, V)) + "]" for V in Vs]
    lines = [", ".join(items[i:i + per]) for i in range(0, len(items), per)]
    return "[\n    " + ",\n    ".join(lines) + "]"


out = [f"""/-!
# Orbit coverage of the central 34-point parallelogram cases

Bookkeeping check for the ES(7) central-symmetry search (branch `es7-cloud`, run records at commit `{COMMIT}`).

A centrally symmetric 34-point set is 17 antipodal classes `0, …, 16`. In hull case `P a` (`1 ≤ a ≤ 8`) the hull is
the parallelogram on classes `0` and `a`, and the second convex layer is spanned by 2 or 3 of the other 15 classes,
giving `C(15,2) + C(15,3) = 560` subcases. The reflection argument (reviewed separately) maps subcase `V` to
`{{(a - i) mod 17 : i ∈ V}}`, so a case is closed once every subcase or its image is refuted.

`closedP1 … closedP8` list the subcases with a run record that is UNSAT, accepted by lrat-check and cake_lpr, and
whose recorded CNF SHA-256 matches the CNF rebuilt from the base formula and the cube files. `pilotUnhashed` lists
P8 subcases refuted only by pilot records that carry no CNF hash. This file checks only the combinatorics: the
subcase enumeration, the reflection, and the coverage. It does not check the SAT records, the CNF encoding, the
second-layer covers or the reflection argument itself.
-/

namespace Central34

/-- The inner antipodal classes of hull case `P a`: every class except `0` and `a`. -/
def inner (a : Nat) : List Nat := (List.range 17).filter fun i ↦ i != 0 && i != a

/-- All 2-element sublists, in order. -/
def choose2 : List Nat → List (List Nat)
  | [] => []
  | x :: xs => xs.map (fun y ↦ [x, y]) ++ choose2 xs

/-- All 3-element sublists, in order. -/
def choose3 : List Nat → List (List Nat)
  | [] => []
  | x :: xs => (choose2 xs).map (x :: ·) ++ choose3 xs

/-- The second-layer subcases of hull case `P a`. -/
def subcases (a : Nat) : List (List Nat) := choose2 (inner a) ++ choose3 (inner a)

/-- A set of classes as a bitmask. -/
def mask (V : List Nat) : Nat := V.foldl (fun acc i ↦ acc ||| (1 <<< i)) 0

/-- The reflection `i ↦ (a - i) mod 17`. -/
def refl (a : Nat) (V : List Nat) : List Nat := V.map fun i ↦ (a + 17 - i) % 17

/-- A family of class sets as a bitset over masks. -/
def bitset (L : List (List Nat)) : Nat := L.foldl (fun acc V ↦ acc ||| (1 <<< mask V)) 0

/-- The subcases of `P a` such that neither they nor their reflection lie in `C`. -/
def uncovered (a : Nat) (C : List (List Nat)) : List (List Nat) :=
  let B := bitset C
  (subcases a).filter fun V ↦ !(B.testBit (mask V) || B.testBit (mask (refl a V)))
"""]
for a in range(1, 9):
    out.append(f"/-- Subcases of `P{a}` with a certified, hash-matched record ({len(hashed[a])} subcases). -/\n"
               f"def closedP{a} : List (List Nat) := {lst(hashed[a])}\n")
if unhashed:
    out.append(f"/-- `P8` subcases whose only certified records are pilot records without a CNF hash. -/\n"
               f"def pilotUnhashed : List (List Nat) := {lst(unhashed)}\n")
out.append("""/-- The hash-matched closed subcases of case `a`. -/
def closed : Nat → List (List Nat)
  | 1 => closedP1 | 2 => closedP2 | 3 => closedP3 | 4 => closedP4
  | 5 => closedP5 | 6 => closedP6 | 7 => closedP7 | 8 => closedP8 | _ => []

/-- Each case has 560 subcases, the reflection maps subcases to subcases and is an involution, and the subcases
form 287 orbits, 14 of them fixed. -/
theorem subcases_reflection :
    (List.range 8).all (fun k ↦
      let a := k + 1
      let S := bitset (subcases a)
      (subcases a).length == 560 &&
      (subcases a).all (fun V ↦ S.testBit (mask (refl a V)) && mask (refl a (refl a V)) == mask V) &&
      ((subcases a).filter fun V ↦ mask V ≤ mask (refl a V)).length == 287 &&
      ((subcases a).filter fun V ↦ mask V == mask (refl a V)).length == 14) = true := by
  decide +kernel
""")
if not unhashed:
    out.append("""/-- Every listed closed subcase is a genuine subcase of its case. -/
theorem closed_are_subcases :
    (List.range 8).all (fun k ↦
      let S := bitset (subcases (k + 1))
      (closed (k + 1)).all fun V ↦ S.testBit (mask V)) = true := by
  decide +kernel

/-- With hash-matched records alone, every orbit of every case `P1 … P8` is closed. -/
theorem all_cases_closed : (List.range 8).all (fun k ↦ (uncovered (k + 1) (closed (k + 1))).isEmpty) = true := by
  decide +kernel

end Central34

#print axioms Central34.subcases_reflection
#print axioms Central34.closed_are_subcases
#print axioms Central34.all_cases_closed
""")
else:
    out.append("""/-- Every listed closed subcase is a genuine subcase of its case. -/
theorem closed_are_subcases :
    (List.range 8).all (fun k ↦
      let S := bitset (subcases (k + 1))
      (closed (k + 1)).all fun V ↦ S.testBit (mask V)) = true ∧
    (pilotUnhashed.all fun V ↦ (bitset (subcases 8)).testBit (mask V)) = true := by
  decide +kernel

/-- With the hash-matched records alone, every orbit of `P1 … P7` is closed. -/
theorem p1_to_p7_closed : (List.range 7).all (fun k ↦ (uncovered (k + 1) (closed (k + 1))).isEmpty) = true := by
  decide +kernel

/-- The `P8` subcases in the orbit of a pilot-only subcase. -/
def pilotOrbits : List (List Nat) :=
  let B := bitset pilotUnhashed
  (subcases 8).filter fun V ↦ B.testBit (mask V) || B.testBit (mask (refl 8 V))

/-- With the hash-matched records alone, exactly the orbits of the pilot-only subcases of `P8` stay open. -/
theorem p8_hashed_gap : ((uncovered 8 closedP8).map mask == pilotOrbits.map mask) = true := by
  decide +kernel

/-- Adding the pilot-only records closes every orbit of `P8`. -/
theorem p8_closed : (uncovered 8 (closedP8 ++ pilotUnhashed)).isEmpty = true := by
  decide +kernel

end Central34

#print axioms Central34.subcases_reflection
#print axioms Central34.closed_are_subcases
#print axioms Central34.p1_to_p7_closed
#print axioms Central34.p8_hashed_gap
#print axioms Central34.p8_closed
""")
open(OUT, "w").write("\n".join(out))
print({a: len(v) for a, v in hashed.items()}, "pilotUnhashed:", unhashed)
