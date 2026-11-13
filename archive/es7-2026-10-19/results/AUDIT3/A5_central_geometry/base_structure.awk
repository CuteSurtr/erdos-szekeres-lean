# Stream the base CNF: clause-length histogram split by whether the clause touches an auxiliary (conv) variable
# (var > XV), list all unit clauses with their line numbers.
BEGIN { XV = 2856 }
/^c/ || /^p/ { next }
{
  n = NF - 1; aux = 0; npos = 0
  for (i = 1; i <= n; i++) { v = $i; if (v < 0) v = -v; else npos++; if (v > XV) aux = 1 }
  key = n "\t" (aux ? "aux" : "X")
  hist[key]++
  if (n == 1) { print "UNIT", NR, $1 > "base_units.txt" }
  total++
}
END { for (k in hist) print k "\t" hist[k] | "sort -n"; print "total\t" total }
