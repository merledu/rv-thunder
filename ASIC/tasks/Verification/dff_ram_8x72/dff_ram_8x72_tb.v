`timescale 1ns/1ns
module dff_ram_8x72_tb;

    reg clk;
    reg wr;
    reg [2:0] address;
    reg [71:0] wdata;
    wire [71:0] rdata;

    // Instantiate the design under test
    dff_ram_8x72 dut (
        .clk(clk),
        .wr(wr),
        .address(address),
        .wdata(wdata),
        .rdata(rdata)
    );

    // Test stimuli
    initial begin
        clk = 0;
        wr = 0;
        
        // Write data to specific addresses
        #10;
        address = 0;
        wr = 0;
        wdata = 72'd19;

        #10;
        address = 1;
        wr = 0;
        wdata = 72'd27;

        #10;
        address = 2;
        wr = 0;
        wdata = 72'd13;

        #10;
        address = 3;
        wr = 0;
        wdata = 72'd40;

        #10;
        address = 4;
        wr = 0;
        wdata = 72'd25;

        #10;
        address = 5;
        wr = 0;
        wdata = 72'd22;

        #10;
        address = 6;
        wr = 0;
        wdata = 72'd17;

        #10;
        address = 7;
        wr = 0;
        wdata = 72'd20;

        // Read data from written addresses
        #10;
        address = 0;
        wr = 1;

        #10; 
        address = 1;
        wr = 1;

        #10;
        address = 2;
        wr = 1;

        #10; 
        address = 3;
        wr = 1;

        #10;
        address = 4;
        wr = 1;

        #10; 
        address = 5;
        wr = 1;

        #10;
        address = 6;
        wr = 1;

        #10; 
        address = 7;
        wr = 1;
        #20;

        $finish;
    end

    initial begin
       $dumpfile("dff_ram_8x72.vcd");
       $dumpvars(0,dff_ram_8x72_tb);
    end

    always #5 clk = ~clk;

endmodule