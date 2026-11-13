#!/bin/sh
# Resource snapshot for the research jobs (read-only): per-process CPU and memory, memory
# pressure, swap usage and swap activity over a 10-second window, load average.
. "$(dirname "$0")/research-common.sh"
echo "Relevant processes (pid nice %cpu rssMB elapsed)"
for p in $(coordinator_pids) $(worker_pids) $(monitor_pids) $(ps -axo pid=,command= | awk '/^ *[0-9]+ \.\.\/\.\.\/cadical\/build\/cadical/ {print $1}'); do
  ps -o pid=,nice=,%cpu=,rss=,etime=,command= -p $p | awk '{printf "%6s %3s %6s %7.0f %10s %s\n",$1,$2,$3,$4/1024,$5,substr($6" "$7" "$8,1,60)}'
done
memory_pressure | tail -1
sysctl -n vm.swapusage
a=$(vm_stat | awk '/Swapouts/ {gsub(/\./,"",$2); print $2}'); sleep 10; b=$(vm_stat | awk '/Swapouts/ {gsub(/\./,"",$2); print $2}')
echo "Swapouts in last 10 s: $((b - a)) pages"
printf "Load average: "; sysctl -n vm.loadavg
