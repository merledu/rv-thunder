# dut = ALU()
# def bench():

#     yield dut.aluop.eq(0b1101) 
#     yield dut.inp1.eq(3)
#     yield dut.inp2.eq(8)

#    # Simulate some clock cycles
#     for _ in range(10):
#         yield
#         (yield dut.out)

#     yield 
# # Run the test bench

# sim = Simulator(dut)
# sim.add_clock(1e-6)
# sim.add_sync_process(bench)
# with sim.write_vcd("ALU.vcd"):
#     sim.run()

# from amaranth.back import verilog

# top = ALU()
# with open("ALU.v", "w") as f:
#     f.write(verilog.convert(top, ports=[top.aluop, top.inp1, top.inp2, top.out]))