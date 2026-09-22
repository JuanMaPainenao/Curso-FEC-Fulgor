module golay_row_search #(
    parameter b0 = 12'b100110001111,
    parameter b1 = 12'b010011100111,
    parameter b2 = 12'b001101010111,
    parameter b3 = 12'b101111100010,
    parameter b4 = 12'b110111010001,
    parameter b5 = 12'b011111001100,
    parameter b6 = 12'b010100111101,
    parameter b7 = 12'b001010111110,
    parameter b8 = 12'b100001111011,
    parameter b9 = 12'b111001110100,
    parameter b10 = 12'b111100011010,
    parameter b11 = 12'b111010101001 
)
(
    input wire [11:0] i_vec,
    output wire o_found,
    output wire [3:0] o_idx,
    output wire [11:0] o_res
);

    wire [11:0] cand0, cand1, cand2, cand3, cand4, cand5, cand6, cand7, cand8, cand9, cand10, cand11;
    wire [3:0] weight0, weight1, weight2, weight3, weight4, weight5, weight6, weight7, weight8, weight9, weight10, weight11;

    assign cand0 = i_vec ^ b0;
    assign cand1 = i_vec ^ b1;
    assign cand2 = i_vec ^ b2;
    assign cand3 = i_vec ^ b3;
    assign cand4 = i_vec ^ b4;
    assign cand5 = i_vec ^ b5;
    assign cand6 = i_vec ^ b6;
    assign cand7 = i_vec ^ b7;
    assign cand8 = i_vec ^ b8;
    assign cand9 = i_vec ^ b9;
    assign cand10 = i_vec ^ b10;
    assign cand11 = i_vec ^ b11;

    reg found_r;
    reg [3:0] idx_r;
    reg [11:0] res_r;

popcount12 u_popcount0 (
    .i_vec (cand0),
    .o_weight (weight0)
);

popcount12 u_popcount1 (
    .i_vec (cand1),
    .o_weight (weight1)
);

popcount12 u_popcount2 (
    .i_vec (cand2),
    .o_weight (weight2)
);

popcount12 u_popcount3 (
    .i_vec (cand3),
    .o_weight (weight3)
);
popcount12 u_popcount4 (
    .i_vec (cand4),
    .o_weight (weight4)
);

popcount12 u_popcount5 (
    .i_vec (cand5),
    .o_weight (weight5)
);
popcount12 u_popcount6 (
    .i_vec (cand6),
    .o_weight (weight6)
);

popcount12 u_popcount7 (
    .i_vec (cand7),
    .o_weight (weight7)
);
popcount12 u_popcount8 (
    .i_vec (cand8),
    .o_weight (weight8)
);

popcount12 u_popcount9 (
    .i_vec (cand9),
    .o_weight (weight9)
);
popcount12 u_popcount10 (
    .i_vec (cand10),
    .o_weight (weight10)
);

popcount12 u_popcount11 (
    .i_vec (cand11),
    .o_weight (weight11)
);

always @(*) begin
    found_r = 1'b0;
    idx_r = 4'd0;
    res_r = 12'd0;

    if (weight0 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd0;
        res_r = cand0;
    end
    else if (weight1 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd1;
        res_r = cand1;
    end
    else if (weight2 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd2;
        res_r = cand2;
    end
    else if (weight3 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd3;
        res_r = cand3;
    end
    else if (weight4 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd4;
        res_r = cand4;
    end
    else if (weight5 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd5;
        res_r = cand5;
    end
    else if (weight6 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd6;
        res_r = cand6;
    end
    else if (weight7 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd7;
        res_r = cand7;
    end
    else if (weight8 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd8;
        res_r = cand8;
    end
    else if (weight9 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd9;
        res_r = cand9;
    end
    else if (weight10 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd10;
        res_r = cand10;
    end
    else if (weight11 <= 2) begin
        found_r = 1'b1;
        idx_r = 4'd11;
        res_r = cand11;
    end
end

assign o_found = found_r;   // puente reg -> wire
assign o_idx   = idx_r;
assign o_res   = res_r;


endmodule