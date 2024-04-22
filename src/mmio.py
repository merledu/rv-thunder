from amaranth import *

class mmio(Elaboratable):

    def __init__(self):
        self.address = Signal(32)
        self.wrt = Signal(1)
        self.rd = Signal(1)
        self.time_en = Signal(1)
        self.timecmp_en = Signal(1)
        self.dmem_en = Signal(1)
        self.add_out = Signal(32)

    def elaborate(self, platform):
        m = Module()
        with m.If(self.address[30:31] == 0b01):
            with m.If((self.address == 0x4000b000) & (self.wrt == 0b1) | (self.rd == 0b1)):#  mtime
                m.d.comb += [
                    self.dmem_en.eq(0b0),
                    self.timecmp_en.eq(0b0),
                    self.time_en.eq(0b1),
                    self.add_out.eq(self.address),
                ]
            with m.Elif((self.address == 0x4000b004) & (self.wrt == 0b1) | (self.rd == 0b1)):# mtimecmp
                m.d.comb += [
                    self.dmem_en.eq(0b0),
                    self.time_en.eq(0b0),
                    self.timecmp_en.eq(0b1),
                    self.add_out.eq(self.address),
                ]
        with m.Elif(self.address[30:31] == 0b00):
            with m.If((self.address[2:15] >= 0x0000) & (self.address[2:15] <= 0x1fff) & (self.wrt == 0b1) | (self.rd == 0b1)):
                m.d.comb += [
                    self.dmem_en.eq(0b1),
                    self.time_en.eq(0b0),
                    self.timecmp_en.eq(0b0),
                    self.add_out.eq(self.address),
                ]
        return m 