`timescale 1ns/1ps
module tb_golay_encoder;

    reg         i_clk, i_rst;
    reg  [11:0] i_msg;
    wire [23:0] o_cw;

    integer fd, r, casos, fallas;
    reg [11:0] in_msg;
    reg [23:0] exp_cw;

    golay_encoder dut (
        .i_clk (i_clk),
        .i_rst (i_rst),
        .i_msg (i_msg),
        .o_cw  (o_cw)
    );

    // reloj: arranca en 0 y da vuelta cada 5 -> periodo 10
    initial i_clk = 0;
    always #5 i_clk = ~i_clk;

    initial begin
        casos  = 0;
        fallas = 0;
        i_rst  = 1;
        i_msg  = 12'd0;

        @(negedge i_clk);
        @(posedge i_clk); #1;
        if (o_cw !== 24'd0) begin
            fallas = fallas + 1;
            $display("FALLA en reset: o_cw=%06h (esperado 000000)", o_cw);
        end
        @(negedge i_clk);
        i_rst = 0;

        fd = $fopen("vec_encoder.txt", "r");
        if (fd == 0) begin $display("No pude abrir el archivo"); $finish; end

        while (!$feof(fd)) begin
            r = $fscanf(fd, "%h %h\n", in_msg, exp_cw);
            if (r == 2) begin
                @(negedge i_clk);
                i_msg = in_msg;
                @(posedge i_clk);
                #1;
                casos = casos + 1;
                if (o_cw !== exp_cw) begin
                    fallas = fallas + 1;
                    $display("FALLA msg=%03h: rtl=%06h esperado=%06h", in_msg, o_cw, exp_cw);
                end
            end
        end
        $fclose(fd);
        $display("golay_encoder: %0d casos, %0d fallas", casos, fallas);
        $finish;
    end
endmodule