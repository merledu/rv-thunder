module dff_mux_2x1(
    input wire clk,
    input x1, x2, s,
    output f
    );

    and A1(g1, x2, s);
    and A0(g0, x1, ~s);
    or O0(f, g0, g1);
endmodule
