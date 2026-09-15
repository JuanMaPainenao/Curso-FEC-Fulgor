module golay_decoder (
input wire i_clk, i_rst,
input wire [23:0] i_rx,
output reg [11:0] o_msg,
output reg [23:0] o_err,
output reg o_corrected,
output reg o_uncorrectable
);


endmodule