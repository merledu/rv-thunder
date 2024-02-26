module dff_full_adder(a, b, c, d, e, cin, cout, sum);

    input a, b, cin;
    output c, d, e, sum, cout;

    assign c = a ^ b;         //C = A xor B
    assign sum = c ^ cin;     //Sum = Cin xor C
    assign d = a & b;         //D = A and B
    assign e = cin & c;       //E = (A xor B) and Cin
    assign cout = d | e;       //Cout = ((A and B) or ((A xor B) and Cin))
endmodule
// module dff_full_adder(
//     input wire clk,
//     input wire a,
//     input wire b,
//     input wire cin,
//     output reg sum,
//     output reg cout
// );

//     always @(posedge clk) begin
//         {cout, sum} <= a + b + cin;
//     end

// endmodule

// module top_module;
//     reg clk;
//     reg a, b, cin;
//     wire sum, cout;

//     // Instantiate the full adder module
//     full_adder uut (
//         .clk(clk),
//         .a(a),
//         .b(b),
//         .cin(cin),
//         .sum(sum),
//         .cout(cout)
//     );

//     // Clock generation
//     always begin
//         #5 clk = ~clk; // Toggle every 5 time units
//     end

//     // Testbench stimulus
//     initial begin
//         clk = 0;
//         a = 1;
//         b = 1;
//         cin = 0;

//         // Monitor outputs
//         $monitor("Time=%0t a=%b b=%b cin=%b sum=%b cout=%b", $time, a, b, cin, sum, cout);

//         // Apply stimulus
//         #10 a = 0;
//         #10 b = 0;
//         #10 cin = 1;
//         //#10 $finish;
//     end

//endmodule
