#!/usr/bin/env bash
# run_all.sh — the whole chain, one command.
#
#   ./scripts/run_all.sh                 # reads ./config.env
#   RUN_DIR=... ./scripts/run_all.sh     # override the run directory
#
# EXIT CODES — the contract from review 03 (G3). VOID has its own code so it
# can never be mistaken for success by a script or by a reviewer skimming.
#   0  all gates PASS
#   1  a gate FAILED
#   2  a gate returned VOID (circular input, or an input that cannot be verified)
#   3  environment error (bad config, missing tool, reused RUN_DIR)
#
set -u
set -o pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"

# ---------------------------------------------------------------- config
CONF="${CONF:-$ROOT/config.env}"
[ -f "$CONF" ] || { echo "FATAL: $CONF not found (copy config.env.example)"; exit 3; }
# shellcheck disable=SC1090
source "$CONF"

: "${RUN_DIR:?RUN_DIR not set in config.env}"
: "${PROJECT_NAME:?PROJECT_NAME not set in config.env}"

# ------------------------------------------------- never reuse a RUN_DIR
# Two runs sharing a path makes the recorded SHA meaningless.
if [ -e "$RUN_DIR" ]; then
    echo "FATAL: RUN_DIR already exists: $RUN_DIR"
    echo "       Point RUN_DIR at a fresh directory. Never overwrite (rule G4)."
    exit 3
fi
mkdir -p "$RUN_DIR"

export RUN_DIR PROJECT_NAME PDK_ROOT PDK STDCELL_LIB
export PYTHONHASHSEED="${PYTHONHASHSEED:-0}"
export MSYS2_ARG_CONV_EXCL='*'

log()  { echo "[run_all] $*"; }
die()  { echo "[run_all] $*"; echo "$2" > "$RUN_DIR/FAILED"; exit "$1"; }

# --------------------------------------------------- isolated launcher ---
# On Windows/Cygwin a bare shell rewrites Windows-style paths and the tools
# silently receive garbage. Always go through `env -i` (rule G5).
if [ -n "${CYGWIN_ROOT:-}" ] && [ -d "$CYGWIN_ROOT" ]; then
    ENVEXE="$CYGWIN_ROOT/bin/env.exe"
    [ -x "$ENVEXE" ] || { echo "FATAL: $ENVEXE not found"; exit 3; }
    run_tool() { "$ENVEXE" -i \
        PDK_ROOT="$PDK_ROOT" PDK="$PDK" \
        RUN_DIR="$RUN_DIR" PROJECT_NAME="$PROJECT_NAME" \
        PYTHONHASHSEED="$PYTHONHASHSEED" \
        MSYS2_ARG_CONV_EXCL='*' \
        PATH="$CYGWIN_ROOT/bin:/usr/bin:/bin" \
        HOME="$RUN_DIR" \
        "$@"; }
else
    run_tool() { "$@"; }
fi

log "RUN_DIR      = $RUN_DIR"
log "PROJECT_NAME = $PROJECT_NAME"
log "PYTHONHASHSEED = $PYTHONHASHSEED"

# ---------------------------------------------------------- 0. tool check
for t in magic netgen python3; do
    command -v "$t" >/dev/null 2>&1 || die 3 "required tool not found: $t"
done
log "tools present: magic, netgen, python3"

# ------------------------------------------------------- 1. place & route
# Adapt this block to your P&R flow (Microlane in the reference run).
# It must produce $RUN_DIR/$PROJECT_NAME.gds
if [ -d "${MICROLANE_SRC:-}" ]; then
    log "P&R: Microlane at $MICROLANE_SRC"
    # ---- PRE-STREAMOUT HOOK -------------------------------------------
    # The reference netlist is exported from the LIVE P&R DATABASE, before the
    # GDS exists. This is the single most important line in this tutorial:
    # export after stream-out and the LVS is circular (review 03, B4).
    # --------------------------------------------------------------------
    ( cd "$MICROLANE_SRC" && run_tool python3 "$HERE/db_export.py" \
        --db-in  "$MICROLANE_SRC/layout.db.json" \
        --out    "$RUN_DIR/reference_from_db.v" \
        --marker "$RUN_DIR/.db_export_marker" ) \
        || die 2 "db_export hook failed — Gate 7B-1R2 would be circular (VOID)"
else
    log "MICROLANE_SRC not set — assuming you placed-and-routed yourself."
    log "You MUST produce BOTH:"
    log "   $RUN_DIR/$PROJECT_NAME.gds"
    log "   $RUN_DIR/reference_from_db.v   (from the live DB, pre-streamout)"
    log "   $RUN_DIR/.db_export_marker     (written by the export hook)"
fi

GDS="$RUN_DIR/$PROJECT_NAME.gds"
[ -f "$GDS" ] || die 3 "no GDS at $GDS"

# freeze the GDS timestamp so the bytes are a function of the design only
if [ "${GDS_TIMESTAMP_FROZEN:-0}" = "1" ]; then
    log "freezing GDS timestamp -> ${GDS_TIMESTAMP:-1700000000}"
    touch -d "@${GDS_TIMESTAMP:-1700000000}" "$GDS"
fi

# --------------------------------------------- 2. CIRCULARITY GUARD ------
# Mechanical check, so VOID cannot be discovered by luck or by a careful human.
REF="$RUN_DIR/reference_from_db.v"
MARK="$RUN_DIR/.db_export_marker"
if [ ! -f "$REF" ] || [ ! -f "$MARK" ]; then
    die 2 "reference netlist or export marker missing -> Gate 7B-1R2 is CIRCULAR (VOID)"
fi
if [ "$REF" -nt "$GDS" ]; then
    die 2 "reference netlist is NEWER than the GDS -> exported post-streamout (VOID)"
fi
log "circularity guard: PASS (reference predates GDS, marker present)"

# --------------------------------------------------------- 3. gate 5 — DRC
log "--- Gate 5  DRC ---"
run_tool magic -dnull -noconsole "$HERE/run_drc.tcl" >"$RUN_DIR/drc.log" 2>&1
[ "$(cat "$RUN_DIR/drc.status" 2>/dev/null)" = "PASS" ] \
    || die 1 "Gate 5 FAILED — see $RUN_DIR/drc.log"
log "Gate 5 PASS"

# -------------------------------------------------- 4. gate 6 — extraction
log "--- Gate 6  extraction ---"
run_tool magic -dnull -noconsole "$HERE/run_extract.tcl" >"$RUN_DIR/extract.log" 2>&1
[ "$(cat "$RUN_DIR/extract.status" 2>/dev/null)" = "PASS" ] \
    || die 1 "Gate 6 FAILED — see $RUN_DIR/extract.log"
log "Gate 6 PASS"

# --------------------------------------------- 5. gate 7A — structural LVS
log "--- Gate 7A structural LVS ---"
if [ -f "${MICROLANE_ORIG:-}/lvs.py" ]; then
    ( cd "$MICROLANE_ORIG" && run_tool python3 lvs.py ) >"$RUN_DIR/lvs_structural.log" 2>&1 \
        || die 1 "Gate 7A FAILED — see $RUN_DIR/lvs_structural.log"
    log "Gate 7A PASS"
else
    log "Gate 7A SKIPPED (Microlane comparator not present) — record this as NOT CHECKED"
    echo "SKIPPED" > "$RUN_DIR/lvs_structural.status"
fi

# ---------------------------------------- 6. gate 7B-1R2 — Netgen LVS
log "--- Gate 7B-1R2 hierarchical LVS ---"
run_tool netgen -batch source "$HERE/run_lvs.tcl" >"$RUN_DIR/lvs_netgen.out" 2>&1
st="$(cat "$RUN_DIR/lvs_netgen.status" 2>/dev/null)"
case "$st" in
    PASS) log "Gate 7B-1R2 PASS" ;;
    VOID) die 2 "Gate 7B-1R2 VOID — see $RUN_DIR/lvs_netgen.log" ;;
    *)    die 1 "Gate 7B-1R2 FAILED — see $RUN_DIR/lvs_netgen.log" ;;
esac

# ------------------------------------------------------- 7. fingerprint
log "--- determinism ---"
( cd "$RUN_DIR" && sha256sum "$PROJECT_NAME.gds" > sha256.txt )
cat "$RUN_DIR/sha256.txt"
log "re-run in a FRESH RUN_DIR and compare: the two SHAs must be identical."

log "ALL GATES PASS"
exit 0
