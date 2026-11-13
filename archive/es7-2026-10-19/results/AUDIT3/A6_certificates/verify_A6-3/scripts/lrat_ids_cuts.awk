# Pass 2 (A6-3): addition-ID contiguity from M+1 and hint references to the cut clause IDs LO..HI (base M0+1..M0+6).
# usage: awk -v M=5272500 -v LO=5272495 -v HI=5272500 -f lrat_ids_cuts.awk
$2 == "d" { for (i = 3; i < NF; i++) if ($i + 0 >= LO && $i + 0 <= HI) delcut[$i]++; next }
{
  id = $1 + 0
  if (!seen) { first = id; prev = id - 1; seen = 1 }
  if (id != prev + 1) gaps++
  prev = id
  z = 0
  for (i = 2; i <= NF; i++) {
    if ($i == "0") { z++; continue }
    if (z == 1) { h = $i + 0; if (h < 0) h = -h; if (h >= LO && h <= HI) { use[h]++; lines_using[id] = 1 } }
  }
}
END {
  printf "first_addition_id=%d last_addition_id=%d noncontiguous_steps=%d (expect first=M+1=%d)\n", first, prev, gaps+0, M+1
  for (c = LO; c <= HI; c++) printf "cut clause id %d: hint references=%d deletions=%d\n", c, use[c]+0, delcut[c]+0
  n = 0; for (k in lines_using) n++; printf "addition lines citing a cut clause as a hint: %d\n", n
}
