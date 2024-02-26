`timescale 1ns/1ps

module dff_ram_4x72_tb;

    reg clk;
    reg [1:0] address;
    reg en;
    reg wr;
    reg [71:0] wdata;
    wire [71:0] rdata;

    // Instantiate the DFF_RAM_4x72 module
    dff_ram_4x72 dut (
        .clk(clk),
        .address(address),
        .en(en),
        .wr(wr),
        .wdata(wdata),
        .rdata(rdata)
    );

    // Clock generation
    always begin
        #5 clk = ~clk;
    end

    // Initial block for stimulus generation
    initial begin
        clk = 0;
        address = 2'b00; // Initial address
        en = 0;        // Enable (active low)
        wr = 0;          // Write enable
        wdata = 72'b1100110000000000000000000000000000000000000000000000000000000000; // Initial data

        // Apply stimulus and observe results
        // Write operation
        #10 en = 0; // Assert enable
        #10 wr = 0;   // Write operation
        #10 wdata = 72'b1010101010101010101010101010101010101010101010101010101010101010; // New data
        #10 wr = 1;   // Deassert write enable
        #10 en = 1; // Deassert enable

        // Read operation
        #10 en = 0; // Assert enable
        #10 wr = 1;   // Read operation
        #10 en = 1; // Deassert enable

        // Additional test cases can be added as needed

        // Stop the simulation
        #10 $stop;
    end
    initial begin
       $dumpfile("dff_ram_4x72.vcd");
       $dumpvars(0,dff_ram_4x72_tb);
    end

endmodule
