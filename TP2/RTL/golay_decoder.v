module golay_decoder (
input wire i_clk, i_rst,
input wire [23:0] i_rx,
output reg [11:0] o_msg,
output reg [23:0] o_err,
output reg o_corrected,
output reg o_uncorrectable
);

wire [11:0] s_comb; 

golay_syndrome u_sindrome (
    .i_rx (i_rx),
    .o_syn (s_comb)
);

reg [11:0] s_e1;
reg [23:0] r_e1;

always @(posedge i_clk) begin
    if (i_rst) begin
        s_e1 <= 12'b000000000000;
        r_e1 <= 24'b000000000000000000000000;
    end
    else begin
        s_e1 <= s_comb;
        r_e1 <= i_rx;
    end
end

wire [3:0] w_s_comb;

popcount12 u_golay_popcount12_s (
    .i_vec (s_e1),
    .o_weight (w_s_comb)
);

wire found_syn;
wire [3:0] idx_syn;
wire [11:0] res_syn;

golay_row_search u_syn_golay_row_search_s(
    .i_vec (s_e1),
    .o_found (found_syn),
    .o_idx (idx_syn),
    .o_res (res_syn)
);

wire [11:0] q_comb;

golay_mult_b u_golay_mult_b(
    .i_vec (s_e1),
    .o_vec (q_comb)
);

wire [3:0] w_q_comb;

popcount12 u_golay_popcount12_q (
    .i_vec (q_comb),
    .o_weight (w_q_comb)
);

wire found_q;
wire [3:0] idx_q;
wire [11:0] res_q;

golay_row_search u_syn_golay_row_search_q(
    .i_vec (q_comb),
    .o_found (found_q),
    .o_idx (idx_q),
    .o_res (res_q)
);

reg [3:0] w_s_reg;
reg [3:0] w_q_reg;
reg [11:0]q_reg;
reg [23:0]r_reg;
reg found_q_reg;
reg [3:0] idx_q_reg;
reg [11:0] res_q_reg;
reg found_s_reg;
reg [3:0] idx_s_reg;
reg [11:0]res_s_reg;
reg [11:0] s_e2;

always @(posedge i_clk) begin
    if (i_rst) begin
        w_s_reg <= 4'd0;
        w_q_reg <= 4'd0;
        q_reg <= 12'd0;
        r_reg <= 23'd0;
        found_q_reg <= 0;
        idx_q_reg <= 4'd0;
        res_q_reg <= 12'd0;
        found_s_reg <= 0;
        idx_s_reg <= 4'd0;
        res_s_reg <= 12'd0;
        s_e2 <= 12'd0;
    end
    else begin
        w_s_reg <= w_s_comb;
        w_q_reg <= w_q_comb;
        q_reg <= q_comb;
        r_reg <= r_e1;
        found_q_reg <= found_q;
        idx_q_reg <= idx_q;
        res_q_reg <= res_q;
        found_s_reg <= found_syn;
        idx_s_reg <= idx_syn;
        res_s_reg <= res_syn;
        s_e2 <= s_e1;
    end

end

wire [23:0] err_comb;
wire uncorrectable_comb;

golay_err_gen u_golay_err_gen(
    .i_syn (s_e2),
    .i_q (q_reg),
    .i_res_syn (res_s_reg),
    .i_res_q (res_q_reg),
    .i_w_syn (w_s_reg),
    .i_w_q (w_q_reg),
    .i_idx_syn (idx_s_reg),
    .i_idx_q (idx_q_reg),
    .i_found_syn (found_s_reg),
    .i_found_q (found_q_reg),
    .o_err (err_comb),
    .o_uncorrectable (uncorrectable_comb)
 );

wire [23:0] cw_comb;
wire [11:0] msg_comb;
wire corrected_comb;

golay_correct u_golay_correct (
    .i_rx (r_reg),
    .i_err (err_comb),
    .o_cw (cw_comb),
    .o_msg (msg_comb),
    .o_corrected (corrected_comb)
);


always @(posedge i_clk) begin
    if (i_rst) begin
        o_msg <= 12'd0;
        o_err <= 24'd0;
        o_corrected <= 1'b0;
        o_uncorrectable <= 1'b0;
    end else begin
        o_msg <= msg_comb;
        o_err <= err_comb;
        o_corrected <= ~uncorrectable_comb;
        o_uncorrectable <= uncorrectable_comb;
    end
end

endmodule