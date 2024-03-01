module dff_ram_8x72 (
    input wire clk,
    input wire wr,

    input wire [2:0] address,
    input wire [71:0] wdata,

    output reg [71:0] rdata
);

    wire [71:0] rdata_inst1;
    wire [71:0] rdata_inst2;
    wire en_1 , en_2;

    assign en_1 = address[2];
    assign en_2 = !(address[2]);

    dff_ram_4x72 instance_1 (
        .clk(clk),
        .en(en_1),
        .wr(wr),
        .address({address[1:0]}),
        .wdata(wdata),
        .rdata(rdata_inst1)
    );

    dff_ram_4x72 instance_2 (
        .clk(clk),
        .en(en_2),
        .wr(wr),
        .address({address[2:1]}),
        .wdata(wdata),
        .rdata(rdata_inst2)
    );

    // always @* begin
    //     if (address[2] == 0) begin
    //         rdata = rdata_inst1;
    //     end else begin
    //         rdata = rdata_inst2;
    //     end
    // end

endmodule