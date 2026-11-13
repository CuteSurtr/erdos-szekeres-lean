#!/bin/bash
# markdown table of a cube directory: cube_table.sh CUBEDIR NV0 ZOFF NZ
C=$1; NV0=$2; ZOFF=$3; NZ=$4
echo "| cube | Z cube | CaDiCaL s | conflicts | LRAT GB | cake_lpr | cube CNF SHA-256 | LRAT SHA-256 |"
echo "|---|---|---:|---:|---:|---|---|---|"
r=0; while [ $r -le $NZ ]; do
  d=$C/c_$r; f=$d/result.txt
  s=$(grep -oE "seconds [0-9]+" $d/solved | head -1 | cut -d' ' -f2); c=$(grep "conflicts:" $f | awk '{print $3}')
  b=$(grep "proof bytes" $f | awk '{printf "%.2f", $3/1e9}'); k=$(grep -oE "cake_lpr seconds [0-9]+" $f | cut -d' ' -f3)
  h=$(sed -n 2p $f | cut -c1-8); p=$(sed -n 3p $f | cut -c1-8); v=$(grep -c "VERIFIED_LINES 1" $f)
  a=$((ZOFF + 1)); if [ $r -eq 0 ]; then z="not Z_$a"; elif [ $r -eq $NZ ]; then z="Z_$a..Z_$((ZOFF + NZ))"; elif [ $r -eq 1 ]; then z="Z_$a, not Z_$((ZOFF + 2))"; else z="Z_$a..Z_$((ZOFF + r)), not Z_$((ZOFF + r + 1))"; fi
  [ $v = 1 ] && vv="verified, ${k} s" || vv="NOT VERIFIED"
  echo "| c_$r | $z | $s | $(printf "%'d" $c) | $b | $vv | \`$h…\` | \`$p…\` |"
  r=$((r + 1))
done
