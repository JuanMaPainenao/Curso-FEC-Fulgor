module golay_syndrome (
input wire [23:0] i_rx,
output wire [11:0] o_syn
);


always @(*) begin
    
    o_syn = i_rx[23:12]

end


endmodule