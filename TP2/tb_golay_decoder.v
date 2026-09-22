`timescale 1ns/1ps
module tb_golay_decoder;

    reg         i_clk, i_rst;
    reg  [23:0] i_rx;
    wire [11:0] o_msg;
    wire [23:0] o_err;
    wire        o_corrected, o_uncorrectable;

    parameter LAT = 3;           // latencia del pipeline del decoder

    reg [23:0] rx_mem  [0:20000];
    reg [11:0] msg_mem [0:20000];
    reg [23:0] err_mem [0:20000];
    reg        cor_mem [0:20000];
    reg        unc_mem [0:20000];

    integer fd, r, N, i, j, casos, fallas;
    reg [23:0] t_rx, t_err;
    reg [11:0] t_msg;
    reg        t_cor, t_unc;

    golay_decoder dut (
        .i_clk (i_clk), .i_rst (i_rst), .i_rx (i_rx),
        .o_msg (o_msg), .o_err (o_err),
        .o_corrected (o_corrected), .o_uncorrectable (o_uncorrectable)
    );

    initial i_clk = 0;
    always #5 i_clk = ~i_clk;

    initial begin
        $dumpfile("decoder.vcd");
        $dumpvars(0, tb_golay_decoder);   // 0 = toda la jerarquia
    end

    initial begin
        casos = 0; fallas = 0;

        N = 0;
        fd = $fopen("vec_decoder.txt", "r");
        if (fd == 0) begin $display("No pude abrir el archivo"); $finish; end
        r = $fscanf(fd, "%h %h %h %h %h\n", t_rx, t_msg, t_err, t_cor, t_unc);
        while (r == 5) begin
            rx_mem[N]=t_rx; msg_mem[N]=t_msg; err_mem[N]=t_err;
            cor_mem[N]=t_cor; unc_mem[N]=t_unc;
            N = N + 1;
            r = $fscanf(fd, "%h %h %h %h %h\n", t_rx, t_msg, t_err, t_cor, t_unc);
        end
        $fclose(fd);

        i_rst = 1; i_rx = 0;
        @(negedge i_clk); @(posedge i_clk); @(negedge i_clk); i_rst = 0;

        for (i = 0; i < 20 + LAT; i = i + 1) begin
            @(posedge i_clk); #1;
            if (i >= LAT) begin
                j = i - LAT;
                casos = casos + 1;
                if (o_uncorrectable !== unc_mem[j] || o_corrected !== cor_mem[j]) begin
                    fallas = fallas + 1;
                    $display("FALLA rx=%06h (flags): rtl(cor=%b unc=%b) esp(cor=%b unc=%b)",
                             rx_mem[j], o_corrected, o_uncorrectable, cor_mem[j], unc_mem[j]);
                end
                else if (unc_mem[j] == 1'b0) begin
                    if (o_msg !== msg_mem[j] || o_err !== err_mem[j]) begin
                        fallas = fallas + 1;
                        $display("FALLA rx=%06h: rtl(msg=%03h err=%06h) esp(msg=%03h err=%06h)",
                                 rx_mem[j], o_msg, o_err, msg_mem[j], err_mem[j]);
                    end
                end
            end
            @(negedge i_clk);
            if (i < N) i_rx = rx_mem[i];
            else       i_rx = 24'd0;
        end
        $display("golay_decoder: %0d casos, %0d fallas", casos, fallas);
        $finish;
    end
endmodule