from Top import *
from data_mem import *
from mmio import *
from amaranth import *
from amaranth.sim import *
import time

class rv_thunder(Elaboratable):
    def __init__(self):
        self.address = Signal(32)
        self.readsig = Signal ()
        self.d_wem = Signal(1)
        self.dec_addout = Signal(32)
        self.d_memmask = Signal(2)
        self.wrt_sel = Signal(1)
        self.dmem_en = Signal(1)
        self.time_en = Signal(1)
        self.timecmp_en = Signal(1)
        self.data_time = Signal(32)
        self.dout = Signal(32)
        self.data = Signal(32)
        self.dataout = Signal(32)
        self.mtime = Signal(64)
        self.mtimecmp = Signal(64)
        self.clkcount = Signal(64)

    def elaborate(self, platform):
        m = Module()
        data_memory_unit = data_mem()
        top_unit = TopModule()
        mmio_unit = mmio()
        m.submodules.data_memory_unit = data_memory_unit
        m.submodules.top_unit = top_unit
        m.submodules.mmio_unit = mmio_unit

        m.d.comb += [
            self.d_memmask.eq(top_unit.data_mem_mask),
            self.address.eq(top_unit.data_mem_adr),
            self.d_wem.eq(top_unit.data_mem_we),
            self.data.eq(top_unit.data_mem_in),
            self.dataout.eq(data_memory_unit.dmem_dout),
            self.dec_addout.eq(mmio_unit.add_out),
            self.time_en.eq(mmio_unit.time_en),
            self.timecmp_en.eq(mmio_unit.timecmp_en),
            self.dmem_en.eq(mmio_unit.dmem_en),
            self.dout.eq(top_unit.writedata),
            self.readsig.eq(top_unit.readsig),
            top_unit.data_mem_out.eq(data_memory_unit.dmem_dout),
            data_memory_unit.adr.eq(self.dec_addout),
            data_memory_unit.dmem_din.eq(top_unit.data_mem_in),
            data_memory_unit.dmem_we.eq(top_unit.data_mem_we),
            top_unit.data_mem_invadd.eq(data_memory_unit.inv_add),
            mmio_unit.address.eq(top_unit.data_mem_adr),
            mmio_unit.wrt.eq(top_unit.data_mem_we),
            mmio_unit.rd.eq(top_unit.readsig),

        ]
        m.d.sync += [
            self.clkcount.eq(self.clkcount + 1)]
#================ mtime ================================
        with m.If(self.time_en == 0b1):
            m.d.sync += self.mtime.eq((self.clkcount // 10)+((self.clkcount % 10)>=5))
            
        with m.If(self.d_wem == 0b1):
            with m.If(self.timecmp_en ==0b1):
                m.d.sync += self.mtimecmp.eq(self.data)  #########

        with m.If(self.time_en == 0b1): 
            m.d.sync += self.wrt_sel.eq(0b0)
            m.d.comb += self.data_time.eq(self.mtime)

        with m.Elif(self.timecmp_en == 0b1):
            m.d.sync += self.wrt_sel.eq(0b0)
            m.d.comb += self.data_time.eq(self.mtimecmp)
        
        with m.Elif(self.dmem_en == 0b1): 
            m.d.sync += self.wrt_sel.eq(0b1)
        
        with m.If(self.wrt_sel == 0b0):
            m.d.comb += self.dataout.eq(self.data_time)
        
        with m.Elif(self.wrt_sel == 0b1):
            m.d.comb += self.dataout.eq(self.dout)
		
        return m
    
dut = rv_thunder()
def bench():
    yield
    yield
    yield
    yield
    yield

    yield
    yield
 
    

    

sim = Simulator(dut)
sim.add_clock(1)  #Add clock
sim.add_sync_process(bench)
with sim.write_vcd("simm.vcd"): # Generate Vcd, which is useful to see a result in GTKwave
    sim.run()