module golay_err_gen (
    input wire [11:0] i_syn, i_q,
    i_res_syn, i_res_q,
    input wire [3:0] i_w_syn, i_w_q,
    i_idx_syn, i_idx_q,
    input wire i_found_syn, i_found_q,
    output wire [23:0] o_err,
    output wire o_uncorrectable
);

reg [23:0] err_reg;
wire [11:0] u_syn = 12'b1 << i_idx_syn;
wire [11:0] u_q = 12'b1 << i_idx_q;
reg uncorrectable_reg;


always @(*) begin
     if (i_w_syn <= 3) begin
        err_reg = {12'b000000000000, i_syn};
        uncorrectable_reg = 0;
     end
     else if (i_found_syn) begin
        err_reg = {u_syn, i_res_syn};
        uncorrectable_reg = 0;
     end
     else if (i_w_q <= 3) begin
        err_reg = {i_q, 12'b000000000000};
        uncorrectable_reg = 0;
     end
     else if (i_found_q) begin
        err_reg = {i_res_q, u_q};
        uncorrectable_reg = 0;
     end
     else begin
        err_reg = 24'd0;
        uncorrectable_reg = 1;
     end
end

assign o_err = err_reg;
assign o_uncorrectable = uncorrectable_reg;

endmodule