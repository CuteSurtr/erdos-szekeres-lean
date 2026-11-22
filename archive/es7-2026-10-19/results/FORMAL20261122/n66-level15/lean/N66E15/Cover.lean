import N66E15.Clauses

/-!
# N66E15.Cover: the split tree of the level-15 campaign (Std-only)

`tree15` is the split tree of `p2/c15/campaign_status.json` (146 campaign cubes: 64 depth-0 cubes, 41 split nodes,
105 certified leaves; written by `tools/mk_data15.py` from the `lits`/`split_on`/`children` fields, which it asserts;
DESIGN.md §3): the first six levels split on states 25, 12, 16, 29, 17, 37, then 41 re-splits; children are (state
occupied, state hole) in that order. `leaves tree15` lists the 105 leaf cubes in depth-first order (occupied child
first); each cube lists its literals from the root.
-/

namespace N66E15

inductive SplitTree
  | leaf
  | node (s : Fin 70) (occ hole : SplitTree)

/-- A cube: `(s, true)` = state s occupied (`+sel s`), `(s, false)` = hole (`-sel s`). -/
abbrev Cube := List (Fin 70 × Bool)

/-- The leaf cubes below a node reached by the literals `pre` (in root-to-node order). -/
def SplitTree.leavesFrom : SplitTree → Cube → List Cube
  | .leaf, pre => [pre]
  | .node s occ hole, pre => occ.leavesFrom (pre ++ [(s, true)]) ++ hole.leavesFrom (pre ++ [(s, false)])

def SplitTree.leaves (t : SplitTree) : List Cube := t.leavesFrom []

def tree15 : SplitTree :=
  (.node 25 (.node 12 (.node 16 (.node 29 (.node 17 (.node 37 (.node 40 (.node 52 (.node 46 (.node 44 (.node 45 (.node 39 .leaf .leaf) .leaf) .leaf) (.node 44 .leaf .leaf)) (.node 46 (.node 44 .leaf .leaf) .leaf)) (.node 52 (.node 46 (.node 44 .leaf .leaf) .leaf) .leaf)) .leaf) (.node 37 (.node 40 (.node 52 (.node 46 .leaf .leaf) .leaf) .leaf) .leaf)) (.node 17 (.node 37 (.node 40 (.node 52 (.node 46 .leaf .leaf) .leaf) (.node 52 (.node 46 .leaf .leaf) .leaf)) .leaf) (.node 37 (.node 40 (.node 52 .leaf .leaf) .leaf) .leaf))) (.node 29 (.node 17 (.node 37 (.node 40 (.node 52 (.node 46 .leaf .leaf) .leaf) .leaf) .leaf) (.node 37 (.node 40 .leaf .leaf) .leaf)) (.node 17 (.node 37 (.node 40 (.node 52 (.node 46 .leaf .leaf) .leaf) (.node 52 .leaf .leaf)) (.node 40 .leaf .leaf)) (.node 37 .leaf .leaf)))) (.node 16 (.node 29 (.node 17 (.node 37 (.node 40 (.node 52 (.node 46 .leaf .leaf) .leaf) .leaf) .leaf) (.node 37 (.node 40 .leaf .leaf) .leaf)) (.node 17 (.node 37 (.node 40 (.node 52 (.node 46 .leaf .leaf) .leaf) (.node 52 .leaf .leaf)) .leaf) (.node 37 .leaf .leaf))) (.node 29 (.node 17 (.node 37 .leaf .leaf) (.node 37 .leaf .leaf)) (.node 17 (.node 37 .leaf .leaf) (.node 37 .leaf .leaf))))) (.node 12 (.node 16 (.node 29 (.node 17 (.node 37 (.node 40 .leaf .leaf) .leaf) (.node 37 .leaf .leaf)) (.node 17 (.node 37 (.node 40 .leaf .leaf) .leaf) (.node 37 .leaf .leaf))) (.node 29 (.node 17 (.node 37 .leaf .leaf) (.node 37 .leaf .leaf)) (.node 17 (.node 37 .leaf .leaf) (.node 37 .leaf .leaf)))) (.node 16 (.node 29 (.node 17 (.node 37 .leaf .leaf) (.node 37 .leaf .leaf)) (.node 17 (.node 37 .leaf .leaf) (.node 37 .leaf .leaf))) (.node 29 (.node 17 (.node 37 .leaf .leaf) (.node 37 .leaf .leaf)) (.node 17 (.node 37 .leaf .leaf) (.node 37 .leaf .leaf))))))

/-- The 105 leaves of the campaign (all certified). -/
def leaves105 : List Cube := tree15.leaves

end N66E15
