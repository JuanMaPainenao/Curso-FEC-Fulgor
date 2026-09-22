`timescale 1ns/1ps
module tb_golay_syndrome;

    reg  [23:0] i_rx;
    wire [11:0] o_syn;

    integer fd, r, casos, fallas;
    reg [23:0] in_rx;
    reg [11:0] exp_syn;

    golay_syndrome dut (
        .i_rx  (i_rx),
        .o_syn (o_syn)
    );

    initial begin
        casos  = 0;
        fallas = 0;
        fd = $fopen("vec_syndrome.txt", "r");
        if (fd == 0) begin
            $display("No pude abrir el archivo");
            $finish;
        end
        while (!$feof(fd)) begin
            r = $fscanf(fd, "%h %h\n", in_rx, exp_syn);
            if (r == 2) begin
                i_rx = in_rx;
                #1;
                casos = casos + 1;
                if (o_syn !== exp_syn) begin
                    fallas = fallas + 1;
                    $display("FALLA en rx=%06h: rtl=%03h esperado=%03h",
                             in_rx, o_syn, exp_syn);
                end
            end
        end
        $fclose(fd);
        $display("golay_syndrome: %0d casos, %0d fallas", casos, fallas);
        $finish;
    end
endmodule