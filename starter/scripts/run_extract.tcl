# Gate 6 — Extraction (Magic, batch)
# Run:  magic -dnull -noconsole scripts/run_extract.tcl
#
# Produces $RUN_DIR/$PROJECT_NAME.spice — the LAYOUT netlist for Gate 7B-1R2.
# Exit status is written to $RUN_DIR/extract.status  (PASS | FAIL)
#
# NOTE ON PARASITICS: this extraction deliberately excludes parasitics, because
# v1.0 has no PEX/RCX step. The netlist is therefore connectivity-accurate and
# NOT timing-accurate. Saying so is part of the honest-boundaries contract; do
# not describe the output of this gate as post-layout.

set project $env(PROJECT_NAME)
set rundir  $env(RUN_DIR)
set pdkroot $env(PDK_ROOT)
set pdk     $env(PDK)

puts "=== Gate 6 — Extraction ==="
puts "design : $project"

gds readonly true
gds rescale false
gds read $rundir/$project.gds
load $project
select top cell
expand

# --- extraction settings ------------------------------------------------
# LVS-grade extraction: topology only. Turning capacitance/coupling/resistance
# on here WITHOUT a PEX deck produces numbers that look like parasitics and are
# not. Leave them off until v1.1 ships RCX.
extract do local
extract no capacitance
extract no coupling
extract no resistance
extract no adjust
extract unique

extract all

# --- netlist out --------------------------------------------------------
ext2spice lvs
ext2spice ngspice
ext2spice -o $rundir/$project.spice

set spice $rundir/$project.spice

if { [file exists $spice] && [file size $spice] > 0 } {
    puts ""
    puts "wrote: $spice  ([file size $spice] bytes)"
    puts "GATE 6: PASS"
    set f [open $rundir/extract.status w]; puts $f "PASS"; close $f
} else {
    puts ""
    puts "ERROR: $spice missing or empty"
    puts "GATE 6: FAIL"
    set f [open $rundir/extract.status w]; puts $f "FAIL"; close $f
}

exit 0
