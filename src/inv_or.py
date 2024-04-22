from amaranth import *

class inv_or(Elaboratable):
    def __init__(self):
        self.in1 = Signal()
        self.in2 = Signal()
        self.or_out = Signal()
    
    def elaborate(self, platform):
        m = Module()
    
        m.d.comb += self.or_out.eq(self.in1 | self.in2)

        return m