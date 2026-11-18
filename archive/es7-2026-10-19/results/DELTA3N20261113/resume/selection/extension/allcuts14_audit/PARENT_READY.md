# All37 cut rows and projection pass

Independent reconstruction matches CNF
`01de4ba0c9831690f5e64a3592fd335ef701c100224060733e9734d55ac65554`:
32,086vars,231,650rows,631,274lits; old231,613rows unchanged;37 addedrows,
8,034addedlits. All39 cut references and the two endpoint duplicates match.

[VERIFY_ALLCUTS14.md](VERIFY_ALLCUTS14.md) independently supplies complete
14-point low coverage and the terminal all-mixed-cup proof. High/exactbase
reuse their frozen audit. Separate through11,size12,exact13 and fresh
low11/12/13 proofs are explicit; no ambient-size monotonicity is used.
Fresh low14 also passes, yielding T7(left<=14) with the stated lower chain.

12 real controls /1,158 selectors /92,592 mixed-subset checks pass.
The combined search remains conditional on an accepted matching proof;
no finite14 UNSAT theorem, left15/16 theorem or unrestricted low theorem
is claimed. No extra cake allocation remains.
