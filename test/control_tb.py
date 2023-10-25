# from amaranth.sim import Simulator

# dut = control()
# def bench():
#     for i in range(0xf1):
#         yield dut.instr.eq(i)
#         yield dut.op
#         #(yield dut.op.eq(dut.instr[0:2]))
#         #(yield dut.op)
#         yield
#         yield
#         yield
#         yield


# sim = Simulator(dut)
# sim.add_clock(1e-6) # 1 MHz
# sim.add_sync_process(bench)
# with sim.write_vcd("control.vcd"):
#     sim.run()

# from amaranth.back import verilog


# top = control()
# with open("control.v", "w") as f:
#     f.write(verilog.convert(top, ports=[top.instr, top.op]))