#!/bin/bash
# Copy trimmed logs and sets from the Task C work directory into results/C.
# usage: collect.sh <workdir> <resultsdir>
W="$1"; R="$2"
mkdir -p "$R/logs/cnc_i_hull" "$R/logs/cnc_ii_interior" "$R/logs/anneal" "$R/sets/heptagon_free_mirror32" "$R/sets/anneal33_low_energy"
for r in i_hull ii_interior; do
  for f in cnc.log latest.json state.json closed.txt state_phase1.json; do
    [ -f "$W/runs/$r/$f" ] && cp "$W/runs/$r/$f" "$R/logs/cnc_$r/$f"
  done
done
[ -f "$W/runs/progress_30min.jsonl" ] && cp "$W/runs/progress_30min.jsonl" "$R/logs/cnc_progress_30min.jsonl"
cp "$W/runs/i_probe/probes.jsonl" "$R/logs/knuth_probes_i_hull.jsonl"
cp "$W/runs/ii_probe/probes.jsonl" "$R/logs/knuth_probes_ii_interior.jsonl"
cat "$W"/runs/lrat_i_*.jsonl "$W"/runs/lrat_ii_*.jsonl 2>/dev/null > "$R/logs/lrat_spot_checks.jsonl"
for d in ctl32 m33 m33_phase1 walk; do
  for f in "$W"/ann/$d/*.log "$W"/ann/$d/*.scan; do
    [ -f "$f" ] || continue
    b=$(basename "$f")
    # the phase-1 33-point scan file repeats one line per accepted move; keep its head and tail
    if [ "$(wc -l < "$f")" -gt 200 ]; then { head -50 "$f"; echo "... ($(wc -l < "$f") lines in total; trimmed) ..."; tail -50 "$f"; } > "$R/logs/anneal/${d}_$b"
    else cp "$f" "$R/logs/anneal/${d}_$b"; fi
  done
done
cat "$W"/ann/ctl32/*.zero > "$R/sets/heptagon_free_mirror32/all_found.txt" 2>/dev/null
cat "$W"/ann/m33/*.best "$W"/ann/walk/*.walkbest 2>/dev/null > "$R/sets/anneal33_low_energy/best_states.txt"
du -sh "$R"
