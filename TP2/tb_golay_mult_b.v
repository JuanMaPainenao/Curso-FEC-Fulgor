`timescale 1ns/1ps
module tb_golay_mult_b;

    reg  [11:0] x;        // entrada que barro
    wire [11:0] bx;       // x * B
    wire [11:0] bbx;      // (x * B) * B  =  x * B^2

    integer i, casos, fallas;

    // aplico B dos veces en cascada
    golay_mult_b m1 (.i_vec (x),  .o_vec (bx));
    golay_mult_b m2 (.i_vec (bx), .o_vec (bbx));

    initial begin
        casos  = 0;
        fallas = 0;
        for (i = 0; i < 4096; i = i + 1) begin
            x = i[11:0];
            #1;
            casos = casos + 1;
            if (bbx !== x) begin
                fallas = fallas + 1;
                $display("FALLA en %03h: B*B da %03h", x, bbx);
            end
        end
        $display("golay_mult_b (B^2=I): %0d casos, %0d fallas", casos, fallas);
        $finish;
    end
endmodule