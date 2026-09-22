`timescale 1ns/1ps
module tb_golay_err_gen;

    reg [11:0] i_syn, i_q, i_res_syn, i_res_q;
    reg [3:0]  i_w_syn, i_w_q, i_idx_syn, i_idx_q;
    reg        i_found_syn, i_found_q;
    wire [23:0] o_err;
    wire        o_uncorrectable;

    integer fd, r, casos, fallas;
    reg [23:0] exp_err;
    reg        exp_unc;

    golay_err_gen dut (
        .i_syn      (i_syn),      .i_q        (i_q),
        .i_res_syn  (i_res_syn),  .i_res_q    (i_res_q),
        .i_w_syn    (i_w_syn),    .i_w_q      (i_w_q),
        .i_idx_syn  (i_idx_syn),  .i_idx_q    (i_idx_q),
        .i_found_syn(i_found_syn),.i_found_q  (i_found_q),
        .o_err          (o_err),
        .o_uncorrectable(o_uncorrectable)
    );

    initial begin
        casos  = 0;
        fallas = 0;
        fd = $fopen("vec_err_gen.txt", "r");
        if (fd == 0) begin
            $display("No pude abrir el archivo");
            $finish;
        end
        while (!$feof(fd)) begin
            r = $fscanf(fd, "%h %h %h %h %h %h %h %h %h %h %h %h\n",
                        i_syn, i_q, i_res_syn, i_res_q,
                        i_w_syn, i_w_q, i_idx_syn, i_idx_q,
                        i_found_syn, i_found_q,
                        exp_err, exp_unc);
            if (r == 12) begin
                #1;
                casos = casos + 1;
                if (o_err !== exp_err || o_uncorrectable !== exp_unc) begin
                    fallas = fallas + 1;
                    $display("FALLA: s=%03h q=%03h -> rtl(err=%06h unc=%b) esp(err=%06h unc=%b)",
                             i_syn, i_q, o_err, o_uncorrectable, exp_err, exp_unc);
                end
            end
        end
        $fclose(fd);
        $display("golay_err_gen: %0d casos, %0d fallas", casos, fallas);
        $finish;
    end
endmodule