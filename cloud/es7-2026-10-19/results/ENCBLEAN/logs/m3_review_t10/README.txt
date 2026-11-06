M3 review, 2026-11-06 (evidence only, not part of the library; interpreted by `lean --run`).
EW10.lean.txt is EncB/EarlyWarning.lean (sha 38d3c253...) with its "Runs" section replaced by a single run on the
whole 60-point SIX60-A set at (m,K,t) = (6,8,10), the largest t below the sixfold bound, and the control (6,7,10).
Renamed .lean.txt so that neither lake nor scripts/audit.sh picks it up. Command (from the package root):
  systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0 nice -n 10 lake env lean --run EW10.lean A full 10 8
Results:
  ew10_A_full.log     (6,8,10): all 13 Model laws hold (incl. noChain, psiLt_zero); psi ranks non-monotone
                      [0,2,...,9,1]; 1,609,785 genCoded clauses (trans 168, ang 7,271, nest 270, chain 1,602,076),
                      0 unsatisfied; the four families concatenate to genCoded. 7m41s, 0.9 GB peak, rc 0.
  ew10_A_laws.log     the law check alone at (6,8,10).
  ew10_A_laws_K7.log  control (6,7,10): only noChain fails (203 violations), as it must (a 7-chain exists).
So Model 6 8 10 is inhabited, at the Bool level, by a known extremal configuration: the Model interface is not vacuous
one step below the bound.
