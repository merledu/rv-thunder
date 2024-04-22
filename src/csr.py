from amaranth import *

class csr(Elaboratable):
    def __init__(self):
        self.csr_sig = Signal()
        self.func3 = Signal(3)
        self.rd_in = Signal(5)
        self.rs1_in = Signal(5)
        self.pc = Signal(32)
        self.rs1_data = Signal(32)
        self.csr_val = Signal(12)
        self.csr_out = Signal(32)
        self.pc_out = Signal(32)
        self.trap_add = Signal(32)
        self.ill_instr = Signal()
        self.mis_all_ins = Signal()
        self.mret = Signal()
        self.res_add = Signal()
        self.pc_sel = Signal()
        self.mip_reg = Signal(32)
        self.mie_reg = Signal(32)
        self.mstatus_reg = Signal(32)
        self.mcause_reg = Signal(32)
        self.mepc_reg = Signal(32)
        self.mtvec_reg = Signal(32)
        self.csr_value = Signal(12)
        self.mcycle_reg = Signal(32)
        self.mcycleh_reg = Signal(32)
        self.counter = Signal(64)

    def elaborate(self, platform):
        m = Module() 
        m.d.sync += [
            self.counter.eq(self.counter + 1)]
        m.d.sync += [ 
            self.mcycle_reg.eq(self.counter[0:31]),
            self.mcycleh_reg.eq(self.counter[32:63]),
            ]
#========================== csr ==================================
        with m.If(self.csr_sig == 0b1):
            
#====================CSRRW========================================
            m.d.comb += self.csr_value.eq(self.csr_val)
            with m.If(self.csr_val == 0x304):
                with m.If(self.func3 == 0b001):
                    m.d.sync += self.mie_reg.eq(self.rs1_data)
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mie_reg)
                with m.Elif(self.func3 == 0b010):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mie_reg)
                    with m.If(self.rs1_in != 0b00000):
                        m.d.sync += self.mie_reg.eq(self.csr_val | self.rs1_data)
                with m.Elif(self.func3 == 0b011):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mie_reg) 
                    with m.If(self.rs1_in != 0b00000):
                        m.d.sync += self.mie_reg.eq(self.csr_val & self.rs1_data)
                with m.Elif (self.func3 == 0b101):
                    m.d.sync += self.mie_reg.eq(self.rs1_in)	
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mie_reg)
                with m.Elif (self.func3 == 0b110):
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mie_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mie_reg.eq(self.csr_val | self.rs1_in)
                with m.Elif (self.func3 == 0b111):
                    with m.If (self.rd_in != 0b00000):   
                        m.d.comb += self.csr_out.eq(self.mie_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mie_reg.eq(self.csr_val & self.rs1_in) 
                
            with m.Elif(self.csr_val == 0x344):
                with m.If(self.func3 == 0b001):
                    m.d.sync += self.mip_reg.eq(self.rs1_data)
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mip_reg)
                with m.Elif(self.func3 == 0b010):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mip_reg) 
                    with m.If(self.rs1_in != 0b00000):
                        m.d.sync += self.mip_reg.eq(self.csr_val | self.rs1_data)
                with m.Elif(self.func3 == 0b011):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mip_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mip_reg.eq(self.csr_val & self.rs1_data)
                with m.Elif (self.func3 == 0b101):
                    m.d.sync += self.mip_reg.eq(self.rs1_in)	
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mip_reg)
                with m.Elif (self.func3 == 0b110):
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mip_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mip_reg.eq(self.csr_val | self.rs1_in)
                with m.Elif (self.func3 == 0b111):
                    with m.If (self.rd_in != 0b00000):   
                        m.d.comb += self.csr_out.eq(self.mip_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mip_reg.eq(self.csr_val & self.rs1_in)

            with m.Elif(self.csr_val == 0x300):
                with m.If(self.func3 == 0b001):
                    m.d.sync += self.mstatus_reg.eq(self.rs1_data)
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mstatus_reg)
                with m.Elif(self.func3 == 0b010):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mstatus_reg) 
                    with m.If(self.rs1_in != 0b00000):
                        m.d.sync += self.mstatus_reg.eq(self.csr_val | self.rs1_data)
                with m.Elif(self.func3 == 0b011):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mstatus_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mstatus_reg.eq(self.csr_val & self.rs1_data)
                with m.Elif (self.func3 == 0b101):
                    m.d.sync += self.mstatus_reg.eq(self.rs1_in)	
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mstatus_reg)
                with m.Elif (self.func3 == 0b110):
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mstatus_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mstatus_reg.eq(self.csr_val | self.rs1_in)
                with m.Elif (self.func3 == 0b111):
                    with m.If (self.rd_in != 0b00000):   
                        m.d.comb += self.csr_out.eq(self.mstatus_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mstatus_reg.eq(self.csr_val & self.rs1_in)

            with m.Elif(self.csr_val == 0x342):
                with m.If(self.func3 == 0b001):
                    m.d.sync += self.mcause_reg.eq(self.rs1_data)
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mcause_reg)
                with m.Elif(self.func3 == 0b010):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mcause_reg) 
                    with m.If(self.rs1_in != 0b00000):
                        m.d.sync += self.mcause_reg.eq(self.csr_val | self.rs1_data)
                with m.Elif(self.func3 == 0b011):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mcause_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mcause_reg.eq(self.csr_val & self.rs1_data)
                with m.Elif (self.func3 == 0b101):
                    m.d.sync += self.mcause_reg.eq(self.rs1_in)	
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mcause_reg)
                with m.Elif (self.func3 == 0b110):
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mcause_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mcause_reg.eq(self.csr_val | self.rs1_in)
                with m.Elif (self.func3 == 0b111):
                    with m.If (self.rd_in != 0b00000):   
                        m.d.comb += self.csr_out.eq(self.mcause_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mcause_reg.eq(self.csr_val & self.rs1_in)

            with m.Elif(self.csr_val == 0x305):
                with m.If(self.func3 == 0b001):
                    m.d.sync += self.mtvec_reg.eq(self.rs1_data)
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mtvec_reg)
                with m.Elif(self.func3 == 0b010):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mtvec_reg) 
                    with m.If(self.rs1_in != 0b00000):
                        m.d.sync += self.mtvec_reg.eq(self.csr_val | self.rs1_data) 
                with m.Elif(self.func3 == 0b011):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mtvec_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mtvec_reg.eq(self.csr_val & self.rs1_data)
                with m.Elif (self.func3 == 0b101):
                    m.d.sync += self.mtvec_reg.eq(self.rs1_in)	
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mtvec_reg)
                with m.Elif (self.func3 == 0b110):
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mtvec_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mtvec_reg.eq(self.csr_val | self.rs1_in)
                with m.Elif (self.func3 == 0b111):
                    with m.If (self.rd_in != 0b00000):   
                        m.d.comb += self.csr_out.eq(self.mtvec_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mtvec_reg.eq(self.csr_val & self.rs1_in)

            with m.Elif(self.csr_val == 0x341):
                with m.If(self.func3 == 0b001):
                    m.d.sync += self.mepc_reg.eq(self.rs1_data)
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mepc_reg)
                with m.Elif(self.func3 == 0b010):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mepc_reg) 
                    with m.If(self.rs1_in != 0b00000):
                        m.d.sync += self.mepc_reg.eq(self.csr_val | self.rs1_data)
                with m.Elif(self.func3 == 0b011):
                    with m.If(self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mepc_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mepc_reg.eq(self.csr_val & self.rs1_data)
                with m.Elif (self.func3 == 0b101):
                    m.d.sync += self.mepc_reg.eq(self.rs1_in)	
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mepc_reg)
                with m.Elif (self.func3 == 0b110):
                    with m.If (self.rd_in != 0b00000):
                        m.d.comb += self.csr_out.eq(self.mepc_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mepc_reg.eq(self.csr_val | self.rs1_in)
                with m.Elif (self.func3 == 0b111):
                    with m.If (self.rd_in != 0b00000):   
                        m.d.comb += self.csr_out.eq(self.mepc_reg) 
                    with m.If (self.rs1_in != 0b00000):
                        m.d.sync += self.mepc_reg.eq(self.csr_val & self.rs1_in)
            with m.Elif(self.csr_val == 0xb00):
                m.d.sync += self.mcycle_reg.eq(self.mcycle_reg) 

            with m.Elif(self.csr_val == 0xb80):
                m.d.sync += self.mcycleh_reg.eq(self.mcycleh_reg) 

            with m.Else():                
                    m.d.comb += self.csr_value.eq(0)

        with m.If((self.ill_instr == 0b1) & (self.mepc_reg == 0)):
            m.d.comb += self.pc_sel.eq(0b1)
            m.d.comb += self.pc_out.eq(self.mtvec_reg)
            m.d.sync += [
                self.mepc_reg.eq(self.pc),
                self.mcause_reg[31].eq(0),
                self.mcause_reg[2].eq(1),
                ]
            

        with m.Elif((self.mis_all_ins == 0b1) & (self.mepc_reg == 0)):
            m.d.comb += self.pc_sel.eq(0b1)
            m.d.comb += self.pc_out.eq(self.mtvec_reg)
            m.d.sync += [
                self.mepc_reg.eq(self.pc),
                self.mcause_reg[0].eq(1),
                self.mcause_reg[31].eq(0),
            ]
            
        with m.Elif((self.csr_val == 0b001100000010) & (self.func3 == 0b000)): #mret value
            m.d.comb += self.mret.eq(0b1)
            m.d.comb += self.pc_sel.eq(0b1)
            m.d.comb += self.pc_out.eq(self.mepc_reg)
            m.d.sync += [
                self.mstatus_reg.eq(0),
                self.mcause_reg.eq(0),
                self.mtvec_reg.eq(0),
                self.mip_reg.eq(0),
                self.mie_reg.eq(0),
            ]

        with m.Else():
            m.d.comb += self.mret.eq(0b0)
            m.d.comb += self.pc_sel.eq(0b0)
            
        return m

                
                

