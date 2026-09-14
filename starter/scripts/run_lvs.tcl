# Gate 7B-1R2 — Hierarchical LVS (Netgen)
# Run:  netgen -batch source scripts/run_lvs.tcl
#
# Netgen's LVS takes the FOUR-argument Tcl form. The two-argument form is a
# different command and will silently do the wrong thing.
#
#     lvs [list <file> <cell>] [list <file> <cell>] <setup> <log>
#
# The two inputs must be INDEPENDENT derivations from the same live P&R database:
#   left  — layout netlist, from Magic extraction of the GDS   (gate 6)
#   right — reference netlist, exported PRE-streamout from the DB (gate 7B hook)
# If both come from the GDS the comparison is CIRCULAR and the result is VOID,
# not PASS. run_all.sh checks this mechanically before invoking this script.

set project $env(PROJECT_NAME)
set rundir  $env(RUN_DIR)
set pdkroot $env(PDK_ROOT)
set pdk     $env(PDK)

set layout   $rundir/$project.spice
set source   $rundir/reference_from_db.v
set setup    $rundir/netgen_setup.tcl
set log      $rundir/lvs_netgen.log

foreach f [list $layout $source] {
    if { ! [file exists $f] } {
        puts "GATE 7B-1R2: VOID — missing input $f"
        set o [open $rundir/lvs_netgen.status w]; puts $o "VOID"; close $o
        exit 2
    }
}

# --- setup file ---------------------------------------------------------
# The PDK ships a setup file that knows how to read this process's CDL/SPICE.
# We source it, then add our own readnet directive for the Verilog reference.
# Taking decap/filler power-ground connectivity from the PDK's authoritative
# CDL/SPICE — not inferring it from layout — is rule G2 from review 03.
set pdk_setup $pdkroot/$pdk/libs.tech/netgen/${pdk}_setup.tcl
if { [file exists $pdk_setup] } {
    set s [open $setup w]
    puts $s "source $pdk_setup"
    puts $s "readnet verilog $source $project"
    puts $s "readnet spice   $layout $project"
    close $s
} else {
    puts "WARNING: PDK netgen setup not found at $pdk_setup"
    set s [open $setup w]
    puts $s "readnet verilog $source $project"
    puts $s "readnet spice   $layout $project"
    close $s
}

puts "=== Gate 7B-1R2 — hierarchical LVS ==="
puts "layout  : $layout"
puts "source  : $source"

lvs [list $layout $project] [list $source $project] $setup $log -json

# --- verdict ------------------------------------------------------------
# Netgen writes "Circuits match uniquely." on success. We parse the LOG, not a
# tool's exit code: a gate status is a claim about a log (rule from review 03).
set ok 0
if { [file exists $log] } {
    set fh [open $log r]
    set body [read $fh]
    close $fh
    if { [regexp {Circuits match uniquely} $body] } { set ok 1 }
}

if { $ok } {
    puts "GATE 7B-1R2: PASS"
    set o [open $rundir/lvs_netgen.status w]; puts $o "PASS"; close $o
    exit 0
} else {
    puts "GATE 7B-1R2: FAIL — see $log"
    set o [open $rundir/lvs_netgen.status w]; puts $o "FAIL"; close $o
    exit 1
}
