module popcount12 (
input wire [11:0] i_vec,
output reg [3:0] o_weight
);


integer k;
reg [3:0] suma;

always @(*) begin
    
    suma = 0;
    for(k = 0; k<12; k = k +1)
        suma = suma + i_vec[k];
    o_weight = suma; 
end

endmodule