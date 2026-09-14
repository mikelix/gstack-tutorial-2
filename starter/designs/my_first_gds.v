// my_first_gds.v — the RTL you feed to place-and-route.
//
// Deliberately trivial. The point of this tutorial is the VERIFICATION CHAIN and
// the determinism contract, not the design. Resist the urge to make it bigger
// until the four gates pass on this one.
//
// This file is NOT the LVS reference. The LVS reference is
// $RUN_DIR/reference_from_db.v, which db_export.py generates from the live P&R
// database after synthesis/mapping. RTL and reference are different things:
//   source.v             -> what you asked for
//   reference_from_db.v  -> what the tool actually built
// Comparing layout against THIS file would be wrong (no mapping, no buffers).

module my_first_gds (
    input  wire din,
    output wire dout
);
    wire n1;
    wire n2;

    assign n1  = ~din;
    assign n2  = ~(n1 & n1);
    assign dout = ~n2;
endmodule
