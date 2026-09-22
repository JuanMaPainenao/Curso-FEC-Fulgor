`timescale 1ns/1ps
module tb_manual;
    reg  i_clk, i_rst;
    reg  [23:0] i_rx;
    wire [11:0] o_msg;
    wire [23:0] o_err;
    wire        o_corrected, o_uncorrectable;

    integer fd, r, casos, fallas;
    reg [23:0] rx, exp_err;
    reg [11:0] exp_msg;
    reg        exp_cor, exp_unc;

    golay_decoder dut (
        .i_clk(i_clk), .i_rst(i_rst), .i_rx(i_rx),
        .o_msg(o_msg), .o_err(o_err),
        .o_corrected(o_corrected), .o_uncorrectable(o_uncorrectable));

    initial i_clk = 0;
    always #5 i_clk = ~i_clk;

    initial begin
        casos = 0; fallas = 0;
        i_rst = 1; i_rx = 0;
        @(negedge i_clk); @(posedge i_clk); @(negedge i_clk); i_rst = 0;

        fd = $fopen("vec_manual.txt", "r");
        if (fd == 0) begin $display("No pude abrir vec_manual.txt"); $finish; end

        $display("");
        $display("   RX     | RTL: msg  err     c u | GOLD: msg  err     c u | ?");
        $display("----------+------------------------+------------------------+----");

        r = $fscanf(fd, "%h %h %h %h %h\n", rx, exp_msg, exp_err, exp_cor, exp_unc);
        while (r == 5) begin
            @(negedge i_clk); i_rx = rx;      // presento la palabra
            repeat (3) @(posedge i_clk);      // espero la latencia (3 ciclos)
            #1;
            casos = casos + 1;
            if (o_uncorrectable !== exp_unc || o_corrected !== exp_cor)
                fallas = fallas + 1;
            else if (exp_unc == 1'b0 && (o_msg !== exp_msg || o_err !== exp_err))
                fallas = fallas + 1;

            $display(" %06h  |     %03h  %06h  %b %b |     %03h  %06h  %b %b | %s",
                rx, o_msg, o_err, o_corrected, o_uncorrectable,
                exp_msg, exp_err, exp_cor, exp_unc,
                ((o_uncorrectable===exp_unc && o_corrected===exp_cor &&
                  (exp_unc==1'b1 || (o_msg===exp_msg && o_err===exp_err))) ? "OK" : "DIFF"));

            r = $fscanf(fd, "%h %h %h %h %h\n", rx, exp_msg, exp_err, exp_cor, exp_unc);
        end
        $fclose(fd);
        $display("----------+------------------------+------------------------+----");
        $display("total: %0d casos, %0d DIFF", casos, fallas);
        $finish;
    end
endmodule