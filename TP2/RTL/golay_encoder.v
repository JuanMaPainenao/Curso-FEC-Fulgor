module golay_encoder (
    input wire i_clk, i_rst,
    input wire [11:0] i_msg,
    output reg [23:0] o_cw
);

    wire [11:0] w_parity;

    golay_mult_b u_mult (
        .i_vec (i_msg),
        .o_vec (parity)
    );

    always @(posedge i_clk) begin
        if (i_rst)
            o_cw <= 24'b0;
        else
            o_cw <= {i_msg, parity};
    end

endmodule