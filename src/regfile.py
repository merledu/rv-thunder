from amaranth import *

class regfile(Elaboratable):
     def __init__(self):
          self.rs1 = Signal(5)
          self.rs2 = Signal(5)
          self.rd = Signal(5)
          self.out1 = Signal(32)
          self.out2 = Signal(32)
          self.wr_reg = Signal(32)
          self.regfile = Memory(width = 32, depth = 32)
          self.we = Signal()
          
     def elaborate(self, platform):
        
        m = Module()
        m.d.comb +=self.out1.eq(self.regfile[self.rs1]),
        m.d.comb +=self.out2.eq(self.regfile[self.rs2])
        with m.If(self.we == 1):
            m.d.sync += self.regfile[self.rd].eq(self.wr_reg)

        return m

