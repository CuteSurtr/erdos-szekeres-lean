#!/bin/sh
# one solve lane over the windows V1 (layers 1..12, cubes on Z_1..Z_12) and V4 (layers 4..15, cubes on Z_4..Z_15)
W=${W:-<lb-k9oct-work-dir>}   # set W to the work directory
BASE=$W/sat/V1/V1.cnf CDIR=$W/sat/cubesV1 NZ=12 ZOFF=0 $W/tools/cubes_g4.sh solve $1
BASE=$W/sat/V4/V4.cnf CDIR=$W/sat/cubesV4 NZ=12 ZOFF=3 $W/tools/cubes_g4.sh solve $2
