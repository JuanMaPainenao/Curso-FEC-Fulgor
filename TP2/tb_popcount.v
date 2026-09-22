`timescale 1ns/1ps
module tb_popcount12;

    reg  [11:0] i_vec;
    wire [3:0]  o_weight;

    integer fd, r, casos, fallas;
    reg [11:0] in_vec;
    reg [3:0]  exp_weight;

    popcount12 dut (
        .i_vec    (i_vec),
        .o_weight (o_weight)
    );

    initial begin
        casos  = 0;
        fallas = 0;

        fd = $fopen("vec_popcount.txt", "r");
        if (fd == 0) begin
            $display("No pude abrir el archivo");
            $finish;
        end

        while (!$feof(fd)) begin
            r = $fscanf(fd, "%h %h\n", in_vec, exp_weight);
            if (r == 2) begin
                i_vec = in_vec;
                #1;
                casos = casos + 1;
                if (o_weight !== exp_weight) begin
                    fallas = fallas + 1;
                    $display("FALLA en %03h: rtl=%0d esperado=%0d",
                             in_vec, o_weight, exp_weight);
                end
            end
        end

        $fclose(fd);
        $display("popcount12: %0d casos, %0d fallas", casos, fallas);
        $finish;
    end

endmodule