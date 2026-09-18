/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */


`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);
    // input and output enables via ui_in 0,1
    wire       load = ui_in[0];
    wire       oe   = ui_in[1];
    wire [7:0] count;

    counter counter_inst (
        .load    (load),
        .rst     (~rst_n),
        .data_in (uio_in),
        .clk     (clk),
        .count   (count)
    );

    assign uo_out = count; // visibility for testing, even when uio_oe is not set 

    // implement tri-state by toggling uio output enable, rather than using hi Z
    assign uio_out = count;
    assign uio_oe  = {8{oe}};

    wire _unused = &{ena, ui_in[7:2], 1'b0};

endmodule

module counter (
    input  wire       load,
    input  wire       rst,
    input  wire [7:0] data_in,
    input  wire       clk,
    output wire [7:0] count
);

    logic [7:0] count_r;

    always_ff @(posedge clk or posedge rst) begin // update ff on rising clock edge or reset detected
        if (rst) begin
            count_r <= 8'd0; // set to zero
        end else begin
            if (load) begin
                count_r <= data_in; // sync data load
            end else begin
                count_r <= count_r + 8'd1; // otherwise continue to count up
            end
        end
    end

    assign count = count_r;

endmodule
