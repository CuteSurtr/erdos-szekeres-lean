#!/bin/bash
# Auditor A5: mutation tests of the syntactic reduction check (each must report missing images).
cd "$(dirname "$0")" || exit 1
B=${BASE_CNF:?set BASE_CNF to the central base CNF written by SYMZ/zcnf.py rot 17 7 --m 2 --hull}
for m in mutB8_noneg mutB8_noflip mutB8_swap12; do echo "== $m (extra H_8)"; ./symcheck $B symmaps/sigma_$m.bin symmaps/hull_a8.cnf | tail -4; echo "exit $?"; done
echo "== mutA8_flipall (extra H_9)"; ./symcheck $B symmaps/sigma_mutA8_flipall.bin symmaps/hull_a9.cnf | tail -4
echo "== correct sigma_B8 but extra = H_0 instead of H_8"; ./symcheck $B symmaps/sigma_B8.bin symmaps/hull_a0.cnf | tail -4
