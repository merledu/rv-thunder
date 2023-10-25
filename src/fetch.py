from amaranth import *
from amaranth.sim import Simulator

class FetchUnit(Elaboratable):
    def __init__(self):
        self.pc = Signal(32) 

    def elaborate(self, platform):
        m = Module()
        # Increment the program counter.
        m.d.sync += self.pc.eq(self.pc + 4)

        return m

