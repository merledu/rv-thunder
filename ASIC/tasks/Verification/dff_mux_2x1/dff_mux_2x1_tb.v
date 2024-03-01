`timescale 1ns/1ns

module dff_mux_2x1_tb;

    reg clk;
    reg x1, x2, s;
    wire f;

    dff_mux_2x1 dut (
        .clk(clk),
        .x1(x1),
        .x2(x2),
        .s(s),
        .f(f)
    );

    // Clock generation
    always begin
        #5 clk = ~clk;
    end
    initial begin
        clk = 0;
        x1 = 0;
        x2 = 0;
        s = 0;
//=================s0======================
        #10;
        x1 = 0;
        #10 ;
        x2 = 0;
        #10;
        s = 0;
        
        #10 ;
        x1 = 0;
        #10 ;
        x2 = 1;
        #10;
        s = 0;
        
        #10;
        x1 = 1;
        #10 ;
        x2 = 0;
        #10;
        s = 0;
        
        #10 ;
        x1 = 1;
        #10 ;
        x2 = 1;
        #10;
        s = 0;
        
        //=================s1======================
        #10;
        x1 = 0;
        #10 ;
        x2 = 0;
        #10;
        s = 1;
        
        #10 ;
        x1 = 0;
        #10 ;
        x2 = 1;
        #10;
        s = 1;
        
        #10;
        x1 = 1;
        #10 ;
        x2 = 0;
        #10;
        s = 1;
        
        #10 ;
        x1 = 1;
        #10 ;
        x2 = 1;
        #10;
        s = 1;

        // Stop the simulation
        #20 $stop;
    end
    initial begin
       $dumpfile("dff_mux_2x1.vcd");
       $dumpvars(0,dff_mux_2x1_tb);
    end

endmodule
