
# def bench():
#         yield dut.we.eq(1)
#         yield dut.rd.eq(0)
#         yield dut.wr_reg.eq(0x0)
#         yield
        
#         yield dut.we.eq(1)
#         yield dut.rd.eq(1)
#         yield dut.wr_reg.eq(0x12345678)
#         yield

#         yield dut.we.eq(1)
#         yield dut.rd.eq(2)
#         yield dut.wr_reg.eq(0x11112222)
#         yield

#         yield dut.we.eq(1)
#         yield dut.rd.eq(3)
#         yield dut.wr_reg.eq(0xfff11100)
#         yield

#         #yield dut.we.eq(0)
#         yield dut.rd.eq(0)
#         yield dut.rs1.eq(1)
#         yield dut.rs2.eq(2)
#         yield
#         yield

#         yield dut.rs2.eq(3)
#         yield
#         yield
        
#         # for _ in range(10):
#         #     yield dut.we.eq(1)
#         #     yield dut.rs1.eq(1)
#         #     yield dut.rs2.eq(2)
#         #     yield dut.rd.eq(1)
#         #     yield dut.wr_reg.eq(0x12345678)
#         #     yield

#         # for _ in range(10):
#         #   yield dut.rs1.eq(1)
#         #   yield dut.rs2.eq(2)
#         #   yield

# sim = Simulator(dut)
# sim.add_clock(1e-6) # 1 MHz
# sim.add_sync_process(bench)
# with sim.write_vcd("regfile.vcd"):
#     sim.run()
    

# from amaranth.back import verilog

# top = regfile()
# with open("regfile.v", "w") as f:
#     f.write(verilog.convert(top, ports=[top.rs1, top.rs2, top.rd, top.out1, top.out2, top.wr_reg, top.we]))