#!/bin/bash
# Reviewer's pipeline hash check: rebuild each sampled unit CNF as a byte stream with awk (as hlane.sh / solver.sh do)
# and hash it with shasum. No Python involved in producing the bytes.
# usage: pipehash.sh BASE RESULTS SAMPLE_TSV
BASE=$1; R=$2; S=$3
ok=0; bad=0
while IFS=$'\t' read -r src unit rec; do
  case=${unit%%_*}
  if [[ $unit == *_cover ]]; then
    # hull units, then one clause per subcase line (cube-file order) negating its non-hull literals
    got=$( { hn=$(grep "^$case " $R/C2C34/cubes.txt | wc -w); nsub=$(grep -c . $R/C2P/cubes/${case}_cubes.txt);
             n=$(( hn - 1 + nsub ));
             awk -v n=$n '/^p cnf/ {print $1, $2, $3, $4 + n; next} {print}' $BASE;
             awk -v C=$case 'FNR==NR { if ($1==C) for (i=2;i<=NF;i++) { h[$i]=1; print $i " 0" }; next }
                             NF { s=""; for (i=2;i<=NF;i++) if (!($i in h)) { v=-$i; s = s v " " }; print s "0" }' \
                 $R/C2C34/cubes.txt $R/C2P/cubes/${case}_cubes.txt; } | shasum -a 256 | cut -d' ' -f1)
  else
    if [[ $src == hex ]]; then CF=$R/C2C34/cubes.txt; else CF=$R/C2P/cubes/${case}_cubes.txt; fi
    lits=$(grep "^$unit " $CF | cut -d' ' -f2-); n=$(echo $lits | wc -w | tr -d ' ')
    got=$( { awk -v n=$n '/^p cnf/ {print $1, $2, $3, $4 + n; next} {print}' $BASE; for l in $lits; do echo "$l 0"; done; } | shasum -a 256 | cut -d' ' -f1)
  fi
  if [ "$got" = "$rec" ]; then ok=$((ok+1)); r=MATCH; else bad=$((bad+1)); r=MISMATCH; fi
  echo -e "$r\t$src\t$unit\t${rec:0:16}\t${got:0:16}"
done < $S
echo "match $ok mismatch $bad"
