`timescale 1ns/1ns

module dff_mux_4x1_tb;

    reg clk;
    reg x0, x1, x2, x3;
    reg s0, s1;
    wire f;

    dff_mux_4x1 dut (
        .clk(clk),
        .x1(x1),
        .x2(x2),
        .x3(x3),
        .x0(x0),
        .s0(s0),
        .s1(s1),
        .f(f)
    );

    // Clock generation
    always begin
        #5 clk = ~clk;
    end
    initial begin
        clk = 0;
        x0 = 0;
        x1 = 0;
        x2 = 0;
        x3 = 0;
        s0 = 0;
        s1 = 0;
//=================s0======================
        #10;
        x0 = 0;
        x1 = 0;
        x2 = 0;
        x3 = 0;
        #10;
        s0 = 0;
        s1 = 0;
        
        #10 ;
        x0 = 1;
        x1 = 0;
        x2 = 0;
        x3 = 1;
        #10;
        s0 = 0;
        s1 = 1;

        // Stop the simulation
        #20 $stop;
    end
    initial begin
       $dumpfile("dff_mux_4x1.vcd");
       $dumpvars(0,dff_mux_4x1_tb);
    end

endmodule
