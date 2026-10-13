# Shared helpers for the ES(8) <= 313 certificate-check control scripts (sourced, not run).
REPO="$(cd "$(dirname "$0")/.." && pwd)"
RT="$REPO/.cache/runtime"
EXPORT=".cache/es313/lean-export"
CHECKER="scripts/check_omission_lean.py"
export ELAN_HOME="$REPO/.elan"
export PATH="$ELAN_HOME/bin:$PATH"
mkdir -p "$RT"
# PIDs of the coordinator (python running the checker on this export), verified by command line.
coordinator_pids() {
  ps -axo pid=,command= | awk -v pat="$CHECKER $EXPORT" 'index($0, pat) && $0 ~ /[Pp]ython/ && $0 !~ /lake env/ && $0 !~ /awk/ {print $1}'
}
wrapper_pids() {
  ps -axo pid=,command= | awk -v pat="$CHECKER $EXPORT" 'index($0, pat) && $0 ~ /lake env/ && $0 !~ /awk/ {print $1}'
}
# Lean kernel workers checking parts of this export.
worker_pids() {
  ps -axo pid=,command= | awk -v pat="$EXPORT/Residual2650ZeroProof/" 'index($0, pat) && $0 ~ /lean -j 1/ && $0 !~ /awk/ {print $1}'
}
monitor_pids() {
  ps -axo pid=,command= | awk 'index($0, "scripts/research-monitor.sh") && $0 ~ /(ba|z)?sh/ && $0 !~ /awk/ {print $1}'
}
