from amaranth import *
from wishbone import *

class wishbone_connection(Elaboratable):
    def __init__(self):
        self.adr_o = Signal(32) # adr of master
        self.master_dat_o = Signal(32)# data of master
        self.slave_dat_o = Signal(32) # data of slave
        self.we_o = Signal(1) # write en of master
        self.sel_o = Signal(3) # sel of master 
        self.stb_o = Signal() # strobe of master
        self.ack_o = Signal() # acknowledge of master
        self.we_i = Signal() # write en of slave
        self.sel_i = Signal(3) #sel  of slave
        self.stb_i = Signal() # strobe of slave
        self.dat_i = Signal(32) #dat_i of slave
        self.adr_i = Signal(32) # adr of slave
        self.rd_o = Signal()
        self.rd_i = Signal()

    def elaborate(self, platform):
        m = Module()
        wishbone_master_unit = wishbonemaster()
        wishbone_slave_unit = wishboneslave()
        m.submodules.wishbone_master_unit = wishbone_master_unit
        m.submodules.wishbone_slave_unit = wishbone_slave_unit

        m.d.comb += [
            wishbone_master_unit.rd_o.eq(self.rd_o),
            self.rd_i.eq(wishbone_master_unit.rd_o),
            # wishbone_slave_unit.rd_i.eq(self.rd_i),
            wishbone_master_unit.adr_o.eq(self.adr_o),
            # wishbone_slave_unit.adr_i.eq(wishbone_master_unit.adr_o),
            # self.adr_i.eq(wishbone_slave_unit.adr_i),

            wishbone_master_unit.dat_o.eq(self.master_dat_o),
            # wishbone_slave_unit.dat_i.eq(wishbone_master_unit.dat_o),
            # self.dat_i.eq(wishbone_slave_unit.dat_i),

            wishbone_master_unit.we_o.eq(self.we_o),
            # wishbone_slave_unit.we_i.eq(wishbone_master_unit.we_o),
            # self.we_i.eq(wishbone_slave_unit.we_i),

            wishbone_master_unit.sel_o.eq(self.sel_o),
            # wishbone_slave_unit.sel_i.eq(wishbone_master_unit.sel_o),
            # self.sel_i.eq(wishbone_slave_unit.sel_i),

            wishbone_master_unit.stb_o.eq(self.stb_o),

            wishbone_slave_unit.stb_i.eq(wishbone_master_unit.stb_o),
            # self.stb_i.eq(wishbone_slave_unit.stb_i),

            wishbone_slave_unit.ack_o.eq(self.ack_o),
            wishbone_master_unit.ack_i.eq(wishbone_slave_unit.ack_o),

            wishbone_slave_unit.dat_o.eq(self.slave_dat_o),
            # wishbone_master_unit.dat_i.eq(wishbone_slave_unit.dat_o),
        ]
        m.d.sync += [
            #wishbone_master_unit.ack_i.eq(wishbone_slave_unit.ack_o),
            #wishbone_slave_unit.stb_i.eq(wishbone_master_unit.stb_o),
            self.stb_i.eq(wishbone_slave_unit.stb_i),
            wishbone_slave_unit.rd_i.eq(self.rd_i),
            wishbone_slave_unit.adr_i.eq(wishbone_master_unit.adr_o),
            self.adr_i.eq(wishbone_slave_unit.adr_i),
            wishbone_slave_unit.dat_i.eq(wishbone_master_unit.dat_o),
            self.dat_i.eq(wishbone_slave_unit.dat_i),
            wishbone_slave_unit.we_i.eq(wishbone_master_unit.we_o),
            self.we_i.eq(wishbone_slave_unit.we_i),
            wishbone_slave_unit.sel_i.eq(wishbone_master_unit.sel_o),
            self.sel_i.eq(wishbone_slave_unit.sel_i),
            wishbone_master_unit.dat_i.eq(wishbone_slave_unit.dat_o),
        ]
        return m