# Testben
# dut = mem()
# def bench():
        # yield dut.we.eq(0)
        # yield dut.dat_w
        # yield dut.adr.eq(2)
        # yield
        # yield

        # yield dut.we.eq(1)
        # yield dut.dat_w.eq(0x1111)
        # yield dut.adr
        # yield
        # yield

        # yield dut.we.eq(1)
        # yield dut.dat_w
        # yield dut.adr
        # yield
        # yield

        # yield dut.we.eq(0)
        # yield dut.dat_w
        # yield dut.adr
        # yield
        # yield

        # yield dut.we.eq(0)
        # yield dut.dat_w
        # yield dut.adr
        # yield
        # yield

        # yield dut.we.eq(0)
        # yield dut.dat_w
        # yield dut.adr
        # yield
        # yield

        # yield dut.we.eq(0)
        # yield dut.dat_w
        # yield dut.adr
        # yield
        # yield

        # yield dut.we.eq(0)
        # yield dut.dat_w
        # yield dut.adr
        # yield
        # yield

        # yield dut.we.eq(0)
        # yield dut.dat_w
        # yield dut.adr
        # yield
        # yield

        # yield dut.we.eq(0)
        # yield dut.dat_w
        # yield dut.adr
        # yield
        # yield
        

        # yield dut.we.eq(0)
        # yield dut.dat_w
        # yield dut.adr
        # yield
        # yield

#         yield dut.we.eq(0)
#         for i in range(30):
#             yield dut.we.eq(0)
#             yield dut.adr.eq(i)
#             yield dut.dat_w.eq(i+1)
#             yield

# sim = Simulator(dut)
# sim.add_clock(1e-6) # 1 MHz
# sim.add_sync_process(bench)
# with sim.write_vcd("memory.vcd"):
#     sim.run()
    

# from amaranth.back import verilog

# top = mem()
# with open("Memory.v", "w") as f:
#     f.write(verilog.convert(top, ports=[top.adr, top.dat_r, top.dat_w, top.we]))