# dut=FetchUnit()
# def bench():
#     yield dut.pc.eq(0x0000)  # Set the initial PC value
#     yield  # In a real CPU, you would decode and execute the instruction here.
    
#     for _ in range(10):
#         yield 
#         yield
#         yield 
#         yield
    
# sim = Simulator(dut)
# sim.add_clock(1e-6) # 1 MHz
# sim.add_sync_process(bench)
# with sim.write_vcd("Fetch.vcd"):
#     sim.run()
    

# from amaranth.back import verilog

# top = FetchUnit()
# with open("Fetch.v", "w") as f:
#     f.write(verilog.convert(top, ports=[top.pc]))