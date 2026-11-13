# Streaming fingerprint of a textual LRAT proof (A6-3 verification).
# addition line: "id lit... 0 hint... 0"; deletion line: "id d id... 0".
{
  if ($2 == "d") { dl++; did += NF - 3; if ($NF != "0") bad++ }
  else { add++; if ($2 == "0") { emp++; if (!fe) fe = $1 } if ($NF != "0") bad++ }
  if ($1 + 0 > mx) mx = $1 + 0
  last = ($2 == "0") ? "empty" : (($2 == "d") ? "deletion" : "clause")
}
END { printf "lines=%d additions=%d empty_additions=%d first_empty_id=%d deletion_lines=%d deleted_ids=%d max_id=%d last_line=%s malformed=%d\n", NR, add, emp, fe, dl, did, mx, last, bad+0 }
