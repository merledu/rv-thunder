from amaranth import *

class regfile(Elaboratable):
     def __init__(self):
          self.rs1 = Signal(5)
          self.rs2 = Signal(5)
          self.rd = Signal(5)
          self.rf_out1 = Signal(32)
          self.rf_out2 = Signal(32)
          self.wb_data = Signal(32)
          self.regfile = Memory(width = 32, depth = 32)
          self.we = Signal()
          
     def elaborate(self, platform):
        
        m = Module()
        m.d.comb +=self.rf_out1.eq(self.regfile[self.rs1]),
        m.d.comb +=self.rf_out2.eq(self.regfile[self.rs2])
        with m.If(self.we == 1):
            m.d.sync += self.regfile[self.rd].eq(self.wb_data)

        return m

