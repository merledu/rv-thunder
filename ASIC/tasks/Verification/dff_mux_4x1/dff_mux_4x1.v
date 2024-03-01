module dff_mux_4x1(
    input wire clk,
    input x0, x1, x2, x3,
    input s0, s1,
    output f
    );

    wire g0, g1;
    dff_mux_2x1 m0 (
        .clk(clk),
        .x1(x0),
        .x2(x1),
        .s(s0),
        .f(g0)
        );

    dff_mux_2x1 m1 (
        .clk(clk),
        .x1(x2),
        .x2(x3),
        .s(s0),
        .f(g1)
        );
    dff_mux_2x1 m2 (
        .clk(clk),
        .x1(g0),
        .x2(g1),
        .s(s0),
        .f(f)
        );
endmodule