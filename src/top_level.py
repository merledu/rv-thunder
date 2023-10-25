from amaranth import *
from amaranth.sim import Simulator
# Import the modules you've defined
from fetch import *
from control import *
from regfile import *
from alu import *
from mem import *

# Create a top-level module that connects the modules
class TopModule(Elaboratable):
    def elaborate(self, platform):
        m = Module()

        # Instantiate each module
        fetch_unit = FetchUnit()
        control_unit = control()
        reg_file = regfile()
        alu = ALU()
        inst_memory_unit = instr_mem()
        data_memory_unit = data_mem()
        # Connect modules together
        m.submodules.fetch_unit = fetch_unit
        m.submodules.control_unit = control_unit
        m.submodules.reg_file = reg_file
        m.submodules.alu = alu
        m.submodules.inst_memory_unit = inst_memory_unit
        m.submodules.data_memory_unit = data_memory_unit

        # Connect signals between modules
        m.d.comb += [
            inst_memory_unit.adr.eq(fetch_unit.pc[2:15]),
            control_unit.instr.eq(inst_memory_unit.dat_r),
            alu.aluop.eq(control_unit.aluop),
            reg_file.rs1.eq(control_unit.rs1),
            reg_file.rs2.eq(control_unit.rs2),
            reg_file.rd.eq(control_unit.rd),
            reg_file.we.eq(control_unit.we),
            alu.inp1.eq(reg_file.out1),
            data_memory_unit.adr.eq(alu.out[2:15]),
            data_memory_unit.we.eq(control_unit.sw),
            # Add more signal connections as needed
        ]
        with m.If (control_unit.ld_wd == 1):
            m.d.comb += reg_file.wr_reg.eq(data_memory_unit.dat_w)
        with m.Else ():
            m.d.comb += reg_file.wr_reg.eq(alu.out)

        with m.If(control_unit.sw == 1):
            m.d.comb += data_memory_unit.dat_in.eq(reg_file.out2)

        with m.If (control_unit.op_b_sel == 1):
            m.d.comb += alu.inp2.eq(control_unit.imm)
        with m.Else ():
            m.d.comb += alu.inp2.eq(reg_file.out2)
        # Return the top module
        return m

# Simulate the top module
dut = TopModule()
def bench():
    yield
    yield
    yield
    yield
    yield
    yield
# We can provide initial values for signals above

sim = Simulator(dut)
sim.add_clock(1e-6)  #Add clock
sim.add_sync_process(bench)
with sim.write_vcd("sim.vcd"): # Generate Vcd, which is useful to see a result in GTKwave
    sim.run()
