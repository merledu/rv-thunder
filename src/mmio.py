from amaranth import *

class mmio(Elaboratable):

    def __init__(self):
        self.address = Signal(32)
        self.sel_o = Signal(3)

    def elaborate(self, platform):
        m = Module()

        with m.If(self.address == 0xa0000000):#  mtime
            m.d.comb += [ 
                self.sel_o.eq(0b000)
            ]
        with m.Elif(self.address == 0xa0000004):# mtimecmp
            m.d.comb += [ 
                self.sel_o.eq(0b001)
            ]
        with m.Elif(self.address == 0x90000000): # uart_t
            m.d.comb += [
                self.sel_o.eq(0b011)
            ]
        with m.Elif(self.address == 0x90000004): # uart_r
            m.d.comb += [
                self.sel_o.eq(0b100)
            ]
        with m.Elif((self.address[2:15] >= 0x0000) & (self.address[2:15] <= 0x1fff)): # data mem
            m.d.comb += [
                self.sel_o.eq(0b010)
            ]
               
        return m 