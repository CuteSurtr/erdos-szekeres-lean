# Private-polygon proof candidates

The integer predicates are COMPUTED by two geometry implementations.
The implication from these predicates is PROVED in THEORY.md.
The core CNFs have not been solved or certified by this track.

## rightmost-n7

T=[5, 11, 12, 13] is a four-cap; A=T minus r, r=13.

| Deleted vertex t | Blue supports of private polygons H={t} union Q |
|---|---|
| 5 | [0, 1, 2, 6, 8]; [0, 2, 4, 7, 8]; [1, 3, 4, 6, 7] |
| 11 | [0, 4, 8, 9, 10]; [1, 2, 3, 8, 9]; [1, 3, 4, 6, 10] |
| 12 | [0, 4, 8, 9, 10]; [1, 2, 3, 8, 9]; [1, 3, 4, 6, 10] |
| 13 | [1, 2, 3, 8, 9]; [1, 3, 4, 6, 10]; [2, 4, 8, 9, 10] |

Core: `rightmost-n7-core.cnf`, 14 variables, 58 clauses.
SHA-256: `6937d721c0cb6cfe9439c51ec234158933ff166be792a18712fb31a9ba275d8e`.

## rightmost-n8

T=[7, 13, 14, 15] is a four-cap; A=T minus r, r=15.

| Deleted vertex t | Blue supports of private polygons H={t} union Q |
|---|---|
| 7 | [0, 1, 2, 3, 8, 10]; [0, 1, 2, 3, 9, 10]; [1, 2, 4, 5, 8, 9]; [3, 4, 5, 6, 8, 9] |
| 13 | [0, 2, 3, 10, 11, 12]; [1, 2, 4, 5, 10, 11]; [3, 4, 5, 6, 8, 12] |
| 14 | [0, 2, 3, 10, 11, 12]; [1, 2, 4, 5, 10, 11]; [3, 4, 5, 6, 8, 12] |
| 15 | [1, 2, 3, 10, 11, 12]; [1, 2, 4, 5, 10, 11]; [3, 4, 5, 6, 8, 12] |

Core: `rightmost-n8-core.cnf`, 16 variables, 80 clauses.
SHA-256: `a5b66b4b902c180a8765340ce3d58aec6ddaf33edf9c02531b47691aa1a01481`.

## arbitrary-n7

T=[1, 5, 6, 7] is a four-cap; A=T minus r, r=1.

| Deleted vertex t | Blue supports of private polygons H={t} union Q |
|---|---|
| 1 | [0, 4, 8, 9, 10]; [2, 4, 8, 12, 13]; [2, 9, 10, 12, 13] |
| 5 | [0, 2, 4, 9, 10]; [0, 3, 4, 9, 11]; [2, 3, 8, 10, 11] |
| 6 | [0, 2, 4, 9, 10]; [0, 3, 4, 9, 11]; [2, 3, 8, 10, 11] |
| 7 | [0, 2, 4, 9, 10]; [0, 3, 4, 9, 11]; [2, 3, 8, 10, 11] |

Core: `arbitrary-n7-core.cnf`, 14 variables, 58 clauses.
SHA-256: `fcf1c84a6f867cecab87ea3da74cbd4e2e4d29b59dcd0df16e4be66fe3a96cdb`.

## Direct contradiction

Any four-cap-free B omits some t from T. If at most one old-blue
point q is selected, all private polygons listed for that t would
need to contain q: their only possible selected vertices lie in
their displayed blue supports. But the intersection of those
supports is empty. With no selected blue point they are all missed.
This covers either color of r and every deletion from A.
