# Gate 5 — DRC (Magic, batch)
# Run:  magic -dnull -noconsole scripts/run_drc.tcl
#
# Exit status is written to $RUN_DIR/drc.status  (PASS | FAIL)
# The log is append-only; a re-run gets a new RUN_DIR, it never edits this one.

set project $env(PROJECT_NAME)
set rundir  $env(RUN_DIR)
set pdkroot $env(PDK_ROOT)
set pdk     $env(PDK)

puts "=== Gate 5 — DRC ==="
puts "design : $project"
puts "gds    : $rundir/$project.gds"
puts "pdk    : $pdkroot/$pdk"

# --- load ---------------------------------------------------------------
# Order matters: read the GDS, then load the top cell, then expand.
# Expanding is not optional — without it Magic only checks the top level.
gds readonly true
gds rescale false
gds read $rundir/$project.gds
load $project
select top cell
expand

# --- check --------------------------------------------------------------
drc off
load $project
select top cell
expand
drc on
drc check
drc catchup

set drcresult [drc listall why]
set count     [llength $drcresult]

puts ""
if { $count == 0 } {
    puts "DRC: 0 violations"
    puts "GATE 5: PASS"
    set f [open $rundir/drc.status w]; puts $f "PASS"; close $f
} else {
    puts "DRC: $count violations"
    foreach r $drcresult { puts "  $r" }
    puts "GATE 5: FAIL"
    set f [open $rundir/drc.status w]; puts $f "FAIL"; close $f
}

# Enumerate warnings too. A suppressed warning is a future bug: if something is
# expected (e.g. standard-cell abutment with this library), write it into the
# release notes, do not filter it out of the log.
puts ""
puts "--- warnings (enumerated, not suppressed) ---"
foreach w [drc listall] { puts "  $w" }

exit 0
