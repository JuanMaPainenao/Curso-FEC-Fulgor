module golay_mult_b (
    input  wire [11:0] i_vec,
    output wire [11:0] o_vec
);
    // o_vec = i_vec * B  en GF(2)
    assign o_vec[11] = i_vec[11] ^ i_vec[8]  ^ i_vec[7]  ^ i_vec[3] ^ i_vec[2] ^ i_vec[1] ^ i_vec[0];
    assign o_vec[10] = i_vec[10] ^ i_vec[7]  ^ i_vec[6]  ^ i_vec[5] ^ i_vec[2] ^ i_vec[1] ^ i_vec[0];
    assign o_vec[ 9] = i_vec[9]  ^ i_vec[8]  ^ i_vec[6]  ^ i_vec[4] ^ i_vec[2] ^ i_vec[1] ^ i_vec[0];
    assign o_vec[ 8] = i_vec[11] ^ i_vec[9]  ^ i_vec[8]  ^ i_vec[7] ^ i_vec[6] ^ i_vec[5] ^ i_vec[1];
    assign o_vec[ 7] = i_vec[11] ^ i_vec[10] ^ i_vec[8]  ^ i_vec[7] ^ i_vec[6] ^ i_vec[4] ^ i_vec[0];
    assign o_vec[ 6] = i_vec[10] ^ i_vec[9]  ^ i_vec[8]  ^ i_vec[7] ^ i_vec[6] ^ i_vec[3] ^ i_vec[2];
    assign o_vec[ 5] = i_vec[10] ^ i_vec[8]  ^ i_vec[5]  ^ i_vec[4] ^ i_vec[3] ^ i_vec[2] ^ i_vec[0];
    assign o_vec[ 4] = i_vec[9]  ^ i_vec[7]  ^ i_vec[5]  ^ i_vec[4] ^ i_vec[3] ^ i_vec[2] ^ i_vec[1];
    assign o_vec[ 3] = i_vec[11] ^ i_vec[6]  ^ i_vec[5]  ^ i_vec[4] ^ i_vec[3] ^ i_vec[1] ^ i_vec[0];
    assign o_vec[ 2] = i_vec[11] ^ i_vec[10] ^ i_vec[9]  ^ i_vec[6] ^ i_vec[5] ^ i_vec[4] ^ i_vec[2];
    assign o_vec[ 1] = i_vec[11] ^ i_vec[10] ^ i_vec[9]  ^ i_vec[8] ^ i_vec[4] ^ i_vec[3] ^ i_vec[1];
    assign o_vec[ 0] = i_vec[11] ^ i_vec[10] ^ i_vec[9]  ^ i_vec[7] ^ i_vec[5] ^ i_vec[3] ^ i_vec[0];

endmodule