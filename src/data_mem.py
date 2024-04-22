from amaranth import *

class data_mem(Elaboratable):
    def __init__(self):
        self.adr = Signal(32)
        self.dmem_din = Signal(32)
        self.dmem_dout = Signal(32)
        self.dmem_we = Signal()
        self.inv_add = Signal()
        # Create a memory with the specified depth (replace this with your actual data)
        self.memory = Memory(width=32, depth=8192)

    def elaborate(self, platform):
        m = Module()
        # Create a read and write port for the data memory
        m.submodules.rdport = rdport = self.memory.read_port(domain="comb")
        m.submodules.wrport = wrport = self.memory.write_port()
        # Connect the address and data signal  
        m.d.comb += [
            rdport.addr.eq(self.adr),
            self.dmem_dout.eq(rdport.data),
            wrport.addr.eq(self.adr),
            wrport.data.eq(self.dmem_din),
            wrport.en.eq(self.dmem_we)  # Enable write operation
            
        ]
        with m.If((self.adr < 0x0000) & (self.adr > 0x1fff)):
            m.d.comb += self.inv_add.eq(1)
        with m.Else():
            m.d.comb += self.inv_add.eq(0)

        return m
