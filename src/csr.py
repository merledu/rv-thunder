from amaranth import *

# Define constants
MIP    = 0x344
MIE    = 0x304
MSTATUS = 0x300
MCAUSE  = 0x342
MTVEC  = 0x305
MEPC   = 0x341

class csr(Elaboratable):
    def __init__(self):
        self.csr_sig = Signal(1)
        self.func3 = Signal(3)
        self.rd_in = Signal(5)
        self.rs1_data = Signal(32)
        self.csr_val = Signal(12)
        self.csr_reg = Signal(32)
        self.rs1_in = Signal(5)
        self.pc = Signal(32)
        self.pc_out = Signal(32)
        self.trap_add = Signal(32)
        self.interrupt = Signal()
        self.ti_intr = Signal()
        self.ex_intr = Signal()
        self.mip_reg = Signal(32)
        self.mie_reg = Signal(32)
        self.mstatus_reg = Signal(32)
        self.mcause_reg = Signal(32)
        self.mepc_reg = Signal(32)
        self.mtvec_reg = Signal(32)

    
    def elaborate(self, platform):
        m = Module() 
        rs1_data12 = self.rs1_data[0:12]

#====================       csr       ============================
        with m.If(self.csr_sig == 1):
#====================CSRRW========================================
            with m.If(self.func3 == 0b001):
                csr_value = rs1_data12
                with m.If (self.rd_in != 0b00000): 
                    self.csr_reg = prevcsr
                    prevcsr = self.csr_val
                    
#====================CSRRS========================================
            with m.Elif(self.func3 == 0b010):
                with m.If(self.rd_in != 0b00000):
                    self.csr_reg = csr_value
					
                with m.If(self.rs1_in != 0b00000):
                    csr_value = self.csr_val | rs1_data12

#====================CSRRC========================================					
            with m.Elif(self.func3 == 0b011):
                with m.If(self.rd_in != 0b00000):
                    self.csr_reg = csr_value

                with m.If (self.rs1_in != 0b00000):
                    csr_value = self.csr_val & rs1_data12
			
#====================CSRRWI=======================================
            with m.Elif (self.func3 == 0b101):
                csr_value = self.csr_val
                csr_value = self.rs1_in
				
                with m.If (self.rd_in != 0b00000):
                        self.csr_reg = prevcsr
                        prevcsr = csr_value
                        
#====================CSRRSI=======================================
            with m.Elif (self.func3 == 0b110):
                with m.If (self.rd_in != 0b00000):

                    self.csr_reg = csr_value

                with m.If (self.rs1_in != 0b00000):
                    csr_value = self.csr_val | self.rs1_in   # contains the immediate

#=====================CSRRCI======================================					
            with m.Elif (self.func3 == 0b111):
                with m.If (self.rd_in != 0b00000):
                    self.csr_reg = csr_value

                with m.If (self.rs1_in != 0b00000):
                    csr_value = self.csr_val & self.rs1_in # contains the immediate

#======================interrupt code(mcause)=====================
        with m.If(self.interrupt == 0b1):
            m.d.comb += self.mstatus_reg[3].eq(1) #mie bit
            m.d.comb += self.mstatus_reg[7].eq(1) #mpie bit
            m.d.comb += self.mcause_reg[31].eq(1) #setting MSB for interrupt
            m.d.comb += self.mepc_reg.eq(self.pc)

            with m.If(self.mcause_reg[31] == 0b1):
                with m.If(self.mcause_reg[7] == 1): #checking timer interrupt
                    m.d.comb += self.mip_reg[7].eq(1) #machine timer interrupt pending bit
                    m.d.comb += self.mie_reg[7].eq(1) #machine timer interrupt enable bit
        
                with m.Elif(self.mcause_reg[11] == 0b1): #checking external interrupt
                    m.d.comb += self.mip_reg[11].eq(1) #external interrupt pending bit
                    m.d.comb += self.mie_reg[11].eq(1) #external interrupt enable bit
            
            with m.If(self.mtvec_reg[0:1]== 0b00): #direct mode
                m.d.comb += self.trap_add.eq(self.mtvec_reg[2:31])
            
            with m.Elif(self.mtvec_reg[0:1] == 0b01): #vectored mode
                 m.d.comb += self.trap_add.eq((self.mtvec_reg[2:31])+(self.mcause_reg[0:30]<<2)) 
            
#==================================================================================================
            with m.If(self.csr_val == 0b001100000010): #mret value
                m.d.comb += self.pc_out.eq(self.mepc_reg)
                self.mstatus_reg = 0
                self.mcause_reg = 0
                self.mtvec_reg = 0
                self.mip_reg = 0
                self.mie_reg = 0

            return m


