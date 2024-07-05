from amaranth import *

class wishbonemaster(Elaboratable):

    def __init__(self):
        self.adr_o = Signal(32)
        self.sel_o = Signal(3)
        self.dat_i = Signal(32)
        self.dat_o = Signal(32)
        self.we_o = Signal()
        self.stb_o = Signal()
        self.ack_i = Signal()
        self.rd_o = Signal()
    
    def elaborate(self,platform):
        m = Module()

        return m


class wishboneslave(Elaboratable):

    def __init__(self):
        self.adr_i = Signal(32)
        self.sel_i = Signal(3)
        self.dat_i = Signal(32)
        self.dat_o = Signal(32)
        self.we_i = Signal()
        self.stb_i = Signal()
        self.ack_o = Signal()
        self.rd_i = Signal()
    
    def elaborate(self,platform):
        m = Module()

        return m

