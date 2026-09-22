`timescale 1ns/1ps
module tb_golay_row_search;

    reg  [11:0] i_vec;
    wire        o_found;
    wire [3:0]  o_idx;
    wire [11:0] o_res;

    integer fd, r, casos, fallas;
    reg [11:0] in_vec;
    reg        exp_found;
    reg [3:0]  exp_idx;
    reg [11:0] exp_res;

    golay_row_search dut (
        .i_vec  (i_vec),
        .o_found(o_found),
        .o_idx  (o_idx),
        .o_res  (o_res)
    );

    initial begin
        casos  = 0;
        fallas = 0;
        fd = $fopen("vec_row_search.txt", "r");
        if (fd == 0) begin
            $display("No pude abrir el archivo");
            $finish;
        end
        while (!$feof(fd)) begin
            r = $fscanf(fd, "%h %h %h %h\n", in_vec, exp_found, exp_idx, exp_res);
            if (r == 4) begin
                i_vec = in_vec;
                #1;
                casos = casos + 1;
                if (o_found !== exp_found ||
                    o_idx   !== exp_idx   ||
                    o_res   !== exp_res) begin
                    fallas = fallas + 1;
                    $display("FALLA en %03h: rtl(f=%b i=%0d r=%03h) esp(f=%b i=%0d r=%03h)",
                             in_vec, o_found, o_idx, o_res, exp_found, exp_idx, exp_res);
                end
            end
        end
        $fclose(fd);
        $display("golay_row_search: %0d casos, %0d fallas", casos, fallas);
        $finish;
    end
endmodule