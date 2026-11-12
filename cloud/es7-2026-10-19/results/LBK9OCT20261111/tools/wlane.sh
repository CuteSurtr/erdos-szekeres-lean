#!/bin/sh
# one solve lane over the windows W1 (layers 1..13, cubes on Z_1..Z_13) and W3 (layers 3..15, cubes on Z_3..Z_15)
W=${W:-<lb-k9oct-work-dir>}   # set W to the work directory
BASE=$W/sat/W1/W1.cnf CDIR=$W/sat/cubesW1 NZ=13 ZOFF=0 $W/tools/cubes_g4.sh solve $1
BASE=$W/sat/W3/W3.cnf CDIR=$W/sat/cubesW3 NZ=13 ZOFF=2 $W/tools/cubes_g4.sh solve $2
