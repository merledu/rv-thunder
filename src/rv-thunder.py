from amaranth import *
from amaranth.sim import *
from Top import *
from data_mem import *
from mmio import *
from inst_mem import *
from wishbone_top import *
from uart_top import *
#from fetch import *

class rv_thunder(Elaboratable):
    def __init__(self):
        self.address = Signal(32)
        self.d_wem = Signal(1)
        self.sel_o = Signal(3)
        self.dout = Signal(32)
        self.data = Signal(32)
        self.stb_r = Signal(1)
        self.ack_i = Signal(1) #acknowledge of slave
        self.mtime = Signal(64)
        self.mtimecmp = Signal(64)
        self.clk = ClockSignal()
        self.m_dat_i = Signal(32) # data of master
        self.rd = Signal()
        self.uart_tx = Signal()
        self.uart_rx = Signal()

    
    def elaborate(self, platform):
        m = Module()
        uart_top_unit = uart_top()
        top_unit = TopModule()
        data_memory_unit = data_mem()    
        mmio_unit = mmio()
        inst_memory_unit = instr_mem()
        #fetch_unit = FetchUnit()
        wishbone_top_unit = wishbone_connection()
        m.submodules.top_unit = top_unit
        m.submodules.data_memory_unit = data_memory_unit
        m.submodules.mmio_unit = mmio_unit
        m.submodules.inst_memory_unit = inst_memory_unit
        #m.submodules.fetch_unit = fetch_unit
        m.submodules.wishbone_top_unit = wishbone_top_unit
        m.submodules.uart_top_unit = uart_top_unit

        m.d.comb += [
            uart_top_unit.uart_rx.eq(self.uart_rx),
            self.uart_tx.eq(uart_top_unit.uart_tx),
        ]
        
#=================================mtime write ================================================
        m.d.sync += self.mtime.eq(self.clk + self.mtime)
        m.d.comb += wishbone_top_unit.ack_o.eq(data_memory_unit.dm_ack),
#=================================For mtimecmp write ==============================================
        with m.If((wishbone_top_unit.stb_i == 0b1)&(wishbone_top_unit.we_i == 0b1)&(wishbone_top_unit.sel_i == 0b001)):
            m.d.sync += self.mtimecmp.eq(self.data),
            m.d.comb += [
                # self.mtimecmp.eq(self.data),
                wishbone_top_unit.ack_o.eq(0b1),
            ]
  
#=================================for Data Memory write ===========================================
        with m.Elif((wishbone_top_unit.stb_i == 0b1)&(wishbone_top_unit.we_i == 0b1)&(wishbone_top_unit.sel_i == 0b010)):
            m.d.comb += [
            #      data_memory_unit.dmem_din.eq(wishbone_top_unit.dat_i),
            #      data_memory_unit.adr.eq(wishbone_top_unit.adr_i),
            #      data_memory_unit.dmem_we.eq(wishbone_top_unit.we_i),
            #      wishbone_top_unit.rd_o.eq(self.rd),
            #      wishbone_top_unit.ack_o.eq(0b1),
            ]
            m.d.comb += [
                data_memory_unit.dmem_din.eq(wishbone_top_unit.dat_i),
                data_memory_unit.adr.eq(wishbone_top_unit.adr_i),
                data_memory_unit.dmem_we.eq(wishbone_top_unit.we_i),
                #wishbone_top_unit.rd_o.eq(self.rd),
            ]
#=================================for UART Tx writee ================================================
        with m.Elif((wishbone_top_unit.stb_i == 0b1)&(wishbone_top_unit.we_i == 0b1)&(wishbone_top_unit.sel_i == 0b011)):
            m.d.comb += [
                #uart_top_unit.tx_stb.eq(wishbone_top_unit.stb_i),
                uart_top_unit.tx_data_in.eq(wishbone_top_unit.dat_i),
                wishbone_top_unit.ack_o.eq(uart_top_unit.tx_ack),
            ]
            m.d.comb += uart_top_unit.tx_stb.eq(wishbone_top_unit.stb_i),
#=============================== For mtime read ==================================================
        with m.If((wishbone_top_unit.sel_i == 0b000) & (self.rd == 0b1)):
            m.d.comb += [
                wishbone_top_unit.slave_dat_o.eq(self.mtime),
                wishbone_top_unit.ack_o.eq(0b1),
                wishbone_top_unit.rd_o.eq(self.rd),
            ]
#===============================For mtimecmp read =================================================
        with m.Elif((wishbone_top_unit.sel_i == 0b001) & (self.rd == 0b1)):
            m.d.comb += [
                wishbone_top_unit.slave_dat_o.eq(self.mtimecmp),
                wishbone_top_unit.ack_o.eq(0b1),
                wishbone_top_unit.rd_o.eq(self.rd),
            ]
#========================================== For data memory read===================================
        with m.Elif((wishbone_top_unit.sel_i == 0b010) & (self.rd== 0b1)):
            m.d.comb += [
                wishbone_top_unit.slave_dat_o.eq(data_memory_unit.dmem_dout),
                wishbone_top_unit.rd_o.eq(self.rd),
                data_memory_unit.adr.eq(wishbone_top_unit.adr_i),
                #wishbone_top_unit.ack_o.eq(0b1),
            ]
#================================= for UART Rx Read================================================
        with m.Elif((wishbone_top_unit.stb_i == 0b1)&(self.rd == 0b1)&(wishbone_top_unit.sel_i == 0b100)):
            m.d.comb += [
                uart_top_unit.rx_stb.eq(wishbone_top_unit.stb_i),
                wishbone_top_unit.slave_dat_o.eq(uart_top_unit.rx_data_out),
                wishbone_top_unit.ack_o.eq(uart_top_unit.rx_ack),
                wishbone_top_unit.rd_o.eq(self.rd),
            ]
            #m.d.comb += uart_top_unit.rx_stb.eq(self.stb_r),
#===================================For write================================================
        with m.If((self.sel_o == 0b000) & (self.d_wem == 0b1)):
            m.d.comb += self.stb_r.eq(0b1)
        
        with m.Elif((self.sel_o == 0b001) & (self.d_wem == 0b1)):
            m.d.comb += self.stb_r.eq(0b1)

        with m.Elif((self.sel_o == 0b010) & (self.d_wem == 0b1)):
             m.d.comb += self.stb_r.eq(0b1)

        with m.Elif((self.sel_o == 0b011) & (self.d_wem == 0b1)):
            m.d.comb += self.stb_r.eq(0b1)

        with m.Elif((self.sel_o == 0b100) & (self.d_wem == 0b1)):
            m.d.comb += self.stb_r.eq(0b1)
        
        with m.If(self.ack_i == 0b1):
            m.d.comb += self.stb_r.eq(0b0)

        # with m.Else():
        #     m.d.comb += self.stb_r.eq(0b0)

#==================================For Read ================================================
        with m.If((self.sel_o == 0b000) & (self.rd == 0b1)):
            m.d.comb += self.stb_r.eq(0b1)
        
        with m.Elif((self.sel_o == 0b001) & (self.rd == 0b1)):
            m.d.comb += self.stb_r.eq(0b1)

        with m.Elif((self.sel_o == 0b010) & (self.rd == 0b1)):
            m.d.comb += self.stb_r.eq(0b1)

        with m.Elif((self.sel_o == 0b011) & (self.rd == 0b1)):
            m.d.comb += self.stb_r.eq(0b1)
        
        with m.Elif((self.sel_o == 0b100) & (self.rd == 0b1)):
            m.d.comb += self.stb_r.eq(0b1)
        
        with m.If(self.ack_i == 0b1):
            m.d.comb += self.stb_r.eq(0b0)

        # with m.Else():
        #     m.d.comb += self.stb_r.eq(0b0)

#============================= Top and MMIO unit connection===============================  
        m.d.comb += [      
            mmio_unit.address.eq(top_unit.data_mem_adr),
            self.d_wem.eq(top_unit.data_mem_we),
            self.sel_o.eq(mmio_unit.sel_o),
            self.address.eq(top_unit.data_mem_adr),
            self.data.eq(top_unit.dmem_data),
            top_unit.data_mem_out.eq(self.m_dat_i),
#=============================== Instr Memory connection====================================
            # inst_memory_unit.adr.eq(fetch_unit.pc[2:15]),
            inst_memory_unit.adr.eq(top_unit.f_pc[2:15]), ###
            top_unit.inst_inval_add.eq(inst_memory_unit.inval_add),
            top_unit.inst_dat_r.eq(inst_memory_unit.dat_r),
        ]
#================================== wishbone_top_unit connection==============================
        m.d.comb += [
            wishbone_top_unit.adr_o.eq(self.address),
            wishbone_top_unit.master_dat_o.eq(self.data),
            wishbone_top_unit.we_o.eq(self.d_wem),
            wishbone_top_unit.sel_o.eq(self.sel_o),
            #wishbone_top_unit.stb_o.eq(self.stb_r),
            #self.ack_i.eq(wishbone_top_unit.ack_o), # ack_i = ack_i(master)
            self.m_dat_i.eq(wishbone_top_unit.slave_dat_o),
            top_unit.data_mem_out.eq(self.m_dat_i), #data_mem_out == m_dat_i (master)
            ##########wishbone_top_unit.rd_o.eq(top_unit.readsig),
        ]
        m.d.comb += wishbone_top_unit.stb_o.eq(self.stb_r),
        m.d.comb += self.ack_i.eq(wishbone_top_unit.ack_o),
        m.d.comb += [
            self.rd.eq(top_unit.readsig),
            top_unit.inst_inval_add.eq(inst_memory_unit.inval_add),
            top_unit.data_mem_invadd.eq(data_memory_unit.inv_add),
            self.data.eq(top_unit.dmem_data),

        ]

#================================= fetch_unit connection =====================================
        m.d.comb += top_unit.f_stb_f.eq(self.stb_r)
        # m.d.comb += fetch_unit.stb_f.eq(self.stb_r)
        
        return m
    

'''dut = rv_thunder()
def bench():
    yield
    yield
    yield
    yield
    yield
    yield dut.uart_rx.eq(0)
    yield
    yield dut.uart_rx.eq(1)  # Shows the 1 start bit is detected correctly
    for i in range(434):
        yield
    yield dut.uart_rx.eq(0)  # Go first data bit uart_rx in lsb (0) postion of data_in
    for j in range(868):
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in              
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 1 postion
        yield
    yield dut.uart_rx.eq(0)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 2 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 3 postion
        yield
    yield dut.uart_rx.eq(0)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 4 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 5 postion
        yield
    yield dut.uart_rx.eq(0)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 6 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 7 postion
        yield
    for j in range(868):     # In this bytes_ready value is 1  so it mean one byte has been received
        yield


    # yield
    # yield
    # yield
    for i in range(8694):
        yield
    
    yield
    yield
    yield
    yield
    yield
    yield dut.uart_rx.eq(0)
    yield
    yield dut.uart_rx.eq(1)  # Shows the 1 start bit is detected correctly
    for i in range(434):
        yield
    yield dut.uart_rx.eq(1)  # Go first data bit uart_rx in lsb (0) postion of data_in
    for j in range(868):
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in              
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 1 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 2 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 3 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 4 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 5 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 6 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 7 postion
        yield
    for j in range(868):     # In this bytes_ready value is 1  so it mean one byte has been received
        yield

    # yield
    # yield
    # yield
    for i in range(8694):
        yield
    yield
    yield
    yield
    yield
    yield

    yield dut.uart_rx.eq(0)
    yield
    yield dut.uart_rx.eq(1)  # Shows the 1 start bit is detected correctly
    for i in range(434):
        yield
    yield dut.uart_rx.eq(0)  # Go first data bit uart_rx in lsb (0) postion of data_in
    for j in range(868):
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in              
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 1 postion
        yield
    yield dut.uart_rx.eq(0)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 2 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 3 postion
        yield
    yield dut.uart_rx.eq(0)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 4 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 5 postion
        yield
    yield dut.uart_rx.eq(0)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 6 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 7 postion
        yield
    for j in range(868):     # In this bytes_ready value is 1  so it mean one byte has been received
        yield


    # yield
    # yield
    # yield
    for i in range(8694):
        yield
    
    yield
    yield
    yield
    yield
    yield
    
    
    
sim = Simulator(dut)
sim.add_clock(1)  #Add clock
sim.add_sync_process(bench)
with sim.write_vcd("8694.vcd"): # Generate Vcd, which is useful to see a result in GTKwave
    sim.run()'''

from amaranth.back import verilog

top = rv_thunder()
with open("nop.v", "w") as f:
     f.write(verilog.convert(top, ports=[top.uart_tx, top.uart_rx]))
    
