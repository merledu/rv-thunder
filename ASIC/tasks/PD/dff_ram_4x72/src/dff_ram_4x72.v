module dff_ram_4x72 (
    input wire clk,
    input wire [1:0] address,
    input wire en_n,
    input wire wr,
    // Write: 0
    // Read:  1
    input wire [71:0] wdata,
    output reg [71:0] rdata
);
    
    reg [71:0] data [3:0];

    always @(posedge clk) begin
        if (!en_n) begin
            // Write
            if (!wr) begin
                data[address] <= wdata;
            end
            // Read
            else begin
                rdata <= data[address];
            end
        end
        else begin
            data[address] <= data[address];
            rdata <= rdata;
        end
    end
endmodule
