# Independent review of the sixfold product-cycle witness

4 November 2026.

**Written proof (reviewed, not refereed) + exact computation.** The three-comparison witness is valid. It excludes the archived 60-point model from realization by a point configuration invariant under the specified Euclidean sixfold rotation. It does **not** establish that the abstract order type has no arbitrary nonsymmetric realization, and it does not settle the exact sixfold maximum.

No blocking sign, canonicalization, or reflection error was found. The scope restriction above is essential: equal absolute brackets within a rotation orbit follows from the prescribed rotation, not merely from an automorphism of the sign pattern.

## Algebra and contradiction

Write `[abc] = det(b-a,c-a)`. Translation of `a` to the origin and expansion of the four two-dimensional vectors gives

```
[abc][ade] - [abd][ace] + [abe][acd] = 0.
```

**Written proof.** When the three displayed signed terms are nonzero and one has the opposite sign from the other two, the magnitude of that unique term equals the sum of the other two magnitudes. It is therefore strictly larger than either one. General position supplies nonzero brackets. A Euclidean rotation preserves the signed determinant; reordering a triple changes only its sign. Thus the absolute bracket is constant on each canonical triple orbit.

Let `A_v > 0` denote that absolute bracket for encoder A triple variable `v`. The independently reconstructed signs and orbit maps give:

| Anchor quintuple | Signs of the three signed GP terms | Strict consequence |
|---|---|---|
| `(0,2,4,22,23)` | `(+,+,-)` | `A_71 A_76 > A_72 A_75` |
| `(0,2,4,19,20)` | `(-,+,-)` | `A_72 A_75 > A_73 A_74` |
| `(0,2,4,18,21)` | `(+,+,-)` | `A_73 A_74 > A_71 A_76` |

**Written proof.** These three strict inequalities form a contradiction. Equivalently, multiplying them gives the same positive product strictly greater than itself. Each orbit exponent cancels exactly.

**Exact computation.** The independent script expands the GP identity as a formal integer polynomial, checks all coefficient cancellation, recomputes the sign of every witness bracket, and verifies all listed products. In particular, the canonical signs of the potentially troublesome brackets are negative:

```
[0,4,23] -> -72     [0,4,22] -> -71
[0,4,20] -> -75     [0,4,19] -> -74
[0,4,21] -> -76     [0,4,18] -> -73
```

The script reconstructs the full orbit numbering independently and cross-checks all 5,710 triple IDs against the actual encoder A. It imports no code from `m6_product_cycles.py`.

## Clause and model binding

**Written proof + exact computation.** All ten involved model signs, expressed as true literals, are

```
58 71 72 73 74 75 76 712 -751 868
```

Their conjunction implies the impossible cycle. Consequently this clause is sound for the specified rotation:

```
-58 -71 -72 -73 -74 -75 -76 -712 751 -868 0
```

It is false in the archived model. The clause does not depend on the nesting order of the two involved orbits; an injective replacement by any two rotation orbits preserves the proof. Common rotation of all indices preserves the proof, and all six relative phase-index shifts of one orbit also give sound instances. The relevant index orbits are layers 0 and 3.

**Exact computation.** The scratch model was compared byte for byte with a fresh in-memory decompression of the archived model. Its compressed SHA-256 agrees with the archive manifest. This review checks the witness's model signs; it does not replay every GP relation or every clause of the historical model's full CNF.

## Exact certified-set test

**Exact computation.** The cut was tested on the certified 54-point set with the rational/integer `Q(sqrt(3))` normalization described in `TESTS.md`. Every ordered pair of its nine orbits, every relative shift of the second orbit, and both the original and mirror were tested: `9 * 8 * 6 * 2 = 864` embeddings.

All embeddings satisfy the cut. The number of true cut literals was distributed as follows:

| True literals | Embeddings |
|---:|---:|
| 1 | 48 |
| 2 | 192 |
| 3 | 198 |
| 4 | 240 |
| 5 | 186 |

No floating-point computation or tolerance is used in this test. This finite test supports the implementation of the universally justified cut; the universal justification is the written determinant argument above.

## Reproduction and hashes

From the results directory, with `MODEL` and `ARCHIVE` pointing to the retained model and its archive:

```sh
python3 -I C6C7REVIEW/tests/review_m6_witness.py \
  --witness C6C7REVIEW/m6_cycle_witness.json \
  --model "$MODEL" --archive "$ARCHIVE" \
  > C6C7REVIEW/logs/witness_review.jsonl
```

**Exact computation.** Retained-run SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| Witness JSON | `e25599d3816e4d5ea94484633dde910afaa5f2a8404ec2c5ac164c0882689973` |
| Decompressed model | `b0cde9d9e0ce5652211136d6443b91cbb7d261b601b5ff887a4273e834d14472` |
| Archived model `.zst` | `9365fc6c39e5b534c0712a1b9604b1c9b063121b2319ae3acc21c81c8309eb4c` |
| `tests/review_m6_witness.py` | `dd79bfdacf0ade6d32bd13404ef387398ddfc349513c6d5fabcb204a7c77d9d5` |
| `logs/witness_review.jsonl` | `f33e6bd1e9906bc0334032b02eabcc609c53b1c1730e91a27783d306f20d4e04` |

**Evidence only (run observation).** The independent check exited successfully, with no SAT solver or proof checker started and no remaining process.

## Second witness and its complete three-orbit family

**Written proof (reviewed, not refereed) + exact computation.** The witness found in `m6/family_run0/search/m6_cycle_witness.json` also passes independent review. It concerns source orbits 0, 1, and 3 and the model with SHA-256 `7fa3fe304361b20940b30e5a3fb3443b87c1bb6931acc50152e07421526e94f7`. It yields

```
A_61 A_74 > A_59 A_76 > A_63 A_72 > A_61 A_74.
```

All three GP identities have signed-term pattern `(+,+,-)`:

| Anchor quintuple | Canonical orientation-literal pairs for its three terms |
|---|---|
| `(0,2,4,6,21)` | `(58,154)`, `(59,-76)`, `(74,-61)` |
| `(0,2,4,10,23)` | `(58,358)`, `(63,-72)`, `(76,-59)` |
| `(0,2,4,8,19)` | `(58,255)`, `(61,-74)`, `(72,-63)` |

The middle term has coefficient `-1`, as in the displayed GP identity. All ten underlying model variables are true, so the sound exclusion clause is exactly

```
-58 -59 -61 -63 -72 -74 -76 -154 -255 -358 0
```

**Exact computation.** `tests/review_m6_second.py` independently binds the decompressed model to its compressed archive and manifest, reconstructs and cross-checks all 5,710 triple IDs, verifies the formal GP identity and each witness sign, and confirms exponent cancellation. It imports no candidate search, verifier, or family-generator implementation.

### Why the complete embedding rule is sound

**Written proof.** For an injective map `f` of the source orbit labels, independent offsets `s_i`, and a single common direction `epsilon` equal to `+1` or `-1`, map

```
(i,k) -> (f(i), epsilon*k + s_i mod 6).
```

This map intertwines a source rotation by `r` steps with a target rotation by `epsilon*r` steps. Both directions are determinant-preserving Euclidean rotations. Therefore every equality of absolute brackets used in the source cycle remains an equality in the embedded cycle. Injectivity keeps distinct points distinct. The proof does not require the target orbits to preserve any nesting order.

A simultaneous reversal of every required bracket sign is also sound: each GP term is a product of two brackets, so its sign is unchanged. The same strict inequalities and exponent cancellation follow. This is a global reversal; the argument does not authorize unrelated sign reversals or separate direction choices on individual orbits. A common shift of all target indices is a rotation, so fixing the first offset to zero loses no distinct condition.

**Exact computation.** The independent check enumerated all `10*9*8 * 6^2 * 2 * 2 = 103,680` embeddings, covering every injection, relative offset pair, common direction, and global sign reversal. It reconstructed each required canonical sign assignment and rechecked the three GP term signs and exponent cancellation. There were no inconsistent premises. The resulting 17,280 distinct clauses match `m6/embedding_family1/family.clauses` **byte for byte**.

This review does not repeat the primary verifier's 217,728 exact certified-set embeddings. Those are separately retained in its verification output; the present check independently verifies the entire formal clause family. As with the first witness, the exclusion concerns realization with the prescribed rotational action, not arbitrary realization of the abstract order type.

Reproduce with the relevant retained archive subdirectories:

```sh
python3 -I C6C7REVIEW/tests/review_m6_second.py \
  --run "$RUN" --family "$FAMILY" \
  > C6C7REVIEW/logs/witness_second_review.jsonl
```

**Exact computation.** Hashes:

| Artifact | SHA-256 |
|---|---|
| Second witness JSON | `dc0ee57705319f792d5005ea20266a7fe529d045f7b74b58b9f1a43714bb9e9c` |
| Second model `.zst` | `0b7c77bc6a9b03287cfe14cdb6106bf02a12503d3862bcfca80d1950aaef5867` |
| Three-orbit clause family | `d772a179248c3e1fd93c775f7d69d43ee07dce0b23cb4cde89fb6dd3d34fb9f5` |
| `tests/review_m6_second.py` | `5aeb32929c3aef275f19aa7c30cc26bc8a1bf727ee0c8c378274870f65ca9c00` |
| `logs/witness_second_review.jsonl` | `22aaea1ba23dd0221cdb25063ee4fe094be43d44424b07342c153dec5e8f1572` |

**Evidence only (run observation).** The independent check took 1.849 seconds, reported 70,483,968 bytes peak RSS, and exited successfully. It started no solver and left no process running.

## Third witness: five-comparison cycle in the final successor

**Written proof (reviewed, not refereed) + exact computation.** The witness retained in `m6/final_cycle_search/m6_cycle_witness.json` excludes the successor model `m6/gp_run08/model.json` from realization with the prescribed Euclidean sixfold rotation. It uses layers 1, 8, and 9. The independent check binds the raw model to its compressed archive and manifest, verifies all 5,710 triple IDs, expands the GP identity formally, and checks every witness sign and canonical rotation parity.

The same positive-bracket notation gives the exact strict cycle

```
A_1691 A_2762 > A_1689 A_2802 > A_1664 A_2763
             > A_1666 A_2761 > A_1661 A_2807
             > A_1691 A_2762.
```

The signed GP-term patterns for the five anchor quintuples, in witness order, are:

| Anchor quintuple | Signed-term pattern |
|---|---|
| `(6,9,48,53,54)` | `(+,-,+)` |
| `(48,6,7,9,55)` | `(-,+,-)` |
| `(6,8,48,53,55)` | `(+,-,+)` |
| `(6,10,48,53,59)` | `(+,+,-)` |
| `(48,6,7,10,54)` | `(-,+,-)` |

**Exact computation.** All ten absolute-bracket exponents cancel, the five comparisons form a closed strict cycle, and the associated sound clause is false in the bound model:

```
-1610 1659 -1660 -1661 -1664 -1666 1689 1691 -1692
-2761 -2762 -2763 -2767 -2783 -2793 2802 2803 2807 0
```

This is one clause, displayed across two lines for readability. This review does not rerun the full GP-consistency scan or the primary verifier's large exact certified-set test. It independently checks the algebraic witness and binds it to the same successor model. In particular, GP sign consistency alone does not invalidate this additional obstruction, which uses equal determinant magnitudes imposed by the rotation. No conclusion about an arbitrary nonsymmetric realization or the overall sixfold maximum follows.

Reproduction:

```sh
python3 -I C6C7REVIEW/tests/review_m6_final.py \
  --run "$RUN" --witness "$WITNESS" \
  > C6C7REVIEW/logs/witness_final_review.jsonl
```

**Exact computation.** Retained hashes:

| Artifact | SHA-256 |
|---|---|
| Third witness JSON | `7a72eaf9220fae89b4a98f460d1c09b4dab550897573fc884fc4a698db7f32c7` |
| `gp_run08/model.json` | `7d52dd0f74bbeb1f1ccf11a0777f8c02dcd8be8dda50f8540d9465e75b6c4e76` |
| `gp_run08/model.json.zst` | `74855db1abaa61968488057f0225329329f917f06bc40ada1ab13cda4df328bd` |
| `tests/review_m6_final.py` | `3eed9ee751e20865b2f83631a8664207163a16ff2cbafaee6068af8ee7bde1f2` |
| `logs/witness_final_review.jsonl` | `c091d7ea0ad41b007980ae070c43c2b19e8dbfcdaf871b724e4265d8708ae9f8` |

**Evidence only (run observation).** The check passed in 0.187 seconds, reported 59,473,920 bytes peak RSS, and exited successfully. No solver was started and no process remains.
