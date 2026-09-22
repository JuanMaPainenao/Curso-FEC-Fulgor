module golay_syndrome (
    input wire [23:0] i_rx,
    output wire [11:0] o_syn
);

    wire [11:0] r_b;

    golay_mult_b u_mult(
        .i_vec (i_rx[23:12]),
        .o_vec (r_b)
    );

    assign o_syn = r_b ^ i_rx[11:0];


endmodule