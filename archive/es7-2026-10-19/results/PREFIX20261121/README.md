# A sharp four-state condition for balanced configurations

Let the points be in general position with distinct x-coordinates, ordered by x. Assume there is no 7-cup or 7-cap. Reflect in a horizontal line if necessary so that the first three points form a cup. Their owner states in the balanced catalog are 0, 1 and 3. **The fourth point must occupy one of states 2, 5, 6 and 9.** Consequently a geometric branch of the octagon search with all four states missing can be discarded after this normalization. The earlier budget-68 study already considered fixing state 3 by reflection. [Owner definitions and catalog order](../../../../experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json) · [Earlier fixed-state experiment](../ES305N20261119/README.md#5b-fixed-states-and-zero-side-only-trees-1945-for-budget-68)

For every size from **4 through 20**, this quartet is the unique set of at most four additional states that is guaranteed to meet the occupied states of every such configuration, even when a convex octagon is forbidden. Here “additional” excludes 0, 1 and 3. This is a geometric condition for reflected configurations. Applying it to an abstract omission tree requires a geometric branch justification.

## Why the fourth point gives this quartet

Write the three consecutive edge slopes as $a,b,c$, and the positive horizontal gaps as $u,v,w$. Normalization gives $a<b$. The signs of triples 013, 023 and 123 become positive respectively as $c$ crosses the thresholds $a-u_0$, $(ua+vb)/(u+v)$ and $b$, where $u_0=v(b-a)/w>0$. These thresholds are strictly increasing. Using the project's cap and cup edge labels gives the following exhaustive table. A bare edge has both labels 1. Extending a cap or cup increases its corresponding label by one. Column $j$ of the new owner's state is the greatest cup label among incoming edges whose cap label is at least $j+1$.

| Signs of 012, 013, 023, 123 | New state | Nonzero column heights |
| --- | ---: | --- |
| + − − − | 2 | 1, 1 |
| + + − − | 5 | 2, 1 |
| + + + − | 9 | 2, 2 |
| + + + + | 6 | 3 |

## Why the quartet is sharp

Seventeen explicit configurations have 20 points each. In each line of the data the heights are the y-coordinates, and the x-coordinates are 0 through 19. The checker uses integer determinants for general position, computes every owner state, tests both rank limits, and checks the hull of every eight-point subset. Among sets of at most four additional state IDs, only the indicated quartet meets the occupied states of all 17 examples. To enumerate the possibilities, choose any example a partial choice misses. Every extension to a hitting set must select a state from that example. This enumerates every minimal hitting set of size at most four. Deleting the rightmost points preserves the earlier owners, which proves sharpness at each smaller size down to four. [Coordinates](twenty-point-witnesses.txt) · [Exact checker](check_witnesses.py)

## Longer prefixes

The C++ enumeration below uses the necessary orientation condition that the four signs of each four-point set in lexicographic triple order change at most once. Upon adding point $k$, the old sign of $ijh$ orders the three new signs $ijk,ihk,jhk$ for every $i<j<h<k$. The program enumerates their consistent binary assignments and removes prefixes with a 7-cap or 7-cup. It makes no realizability assumption when counting abstract sign assignments. The second count groups assignments by their unordered set of occupied catalog states.

| Prefix length | Normalized sign assignments after the two rank filters | Distinct occupied-state sets |
| ---: | ---: | ---: |
| 3 | 1 | 1 |
| 4 | 4 | 4 |
| 5 | 31 | 22 |
| 6 | 454 | 180 |
| 7 | 12,348 | 2,124 |
| 8 | 616,081 | 34,744 |

Run the two checks from this directory. The enumerator writes the length, multiplicity and sorted state IDs of each pattern to standard output, and the table totals to standard error. [C++ enumeration](prefix_states.cpp)

```sh
python3 check_witnesses.py
c++ -std=c++17 -O3 prefix_states.cpp -o /tmp/es-prefix-states
/tmp/es-prefix-states > /tmp/es-prefix-patterns.txt
```

## Effect on the budget-68 search

At the top of the Mac budget-68 search, this prefix test eliminated **0 of 16,384 contexts**, even when all eight initial points were used. The missing-state lists across those contexts contain 99 distinct states. The first eight points of examples 11 and 14 occupy respectively $\{0,1,2,3,4,7,21,29\}$ and $\{0,1,3,6,10,17,23,26\}$. Both avoid all 99 states. Their intersection is exactly the three fixed states, so compatibility with missing-state lists alone forces no additional individual state at this depth. This calculation concerns the initial prefixes. Extending them to a complete solution must still satisfy the other conditions. [Coordinate witnesses](twenty-point-witnesses.txt)

The Mac tree used 3,133 rows and budget 68 with `fastbb256`, 16,384 target contexts and options `--ktop=16 --klow=4 --dtop=0 --dmid=0`. Run `python3 check_witnesses.py --contexts /path/to/contexts.json` to verify the two prefixes against that tree. The Linux checkpoint uses a separate 32,755-context partition. Its 7,817 open contexts still require certificates. [Linux checkpoint and row hashes](../ES303N20261120/README.md)
