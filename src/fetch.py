from amaranth import *

class FetchUnit(Elaboratable):
    def __init__(self):
        self.branch = Signal()
        self.branch_tar = Signal(32)
        self.pc = Signal(32)
        self.csr_pcsel = Signal()
        self.csr_in = Signal(32)
        self.stb_f = Signal()
    def elaborate(self, platform):
        m = Module()

        with m.If (self.branch):
            m.d.sync += self.pc.eq(self.branch_tar)
        with m.Elif(self.csr_pcsel == 0b1):
            m.d.sync += self.pc.eq(self.csr_in)
            # Increment the program counter.
        with m.Elif(self.stb_f == 0b1):
            m.d.sync += self.pc.eq(self.pc)
        with m.Else():    
            m.d.sync += self.pc.eq(self.pc + 4)  
        return m

