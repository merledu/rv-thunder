from amaranth import *

class control(Elaboratable):

    def __init__(self):

        self.instr_dat = Signal(32)  # Input Instruction
        self.funct3 = Signal(3)  # Function 3
        self.funct7 = Signal()  # Function 7 funct7
        self.rs1 = Signal(5)  # Source Register 1
        self.rs2 = Signal(5)  # Source Register 2
        self.rd = Signal(5)  # Destination Register
        self.op = Signal(7)
        self.mtype = Signal()  # Opcode

        self.we = Signal()  # Register write enable (It will be 1 for R and I type and it is 0 for S type)
        self.mem_mask = Signal(2)  # for memory masking (used in both load and store)
        self.ld_wd = Signal()
        self.aluop = Signal(4)  # ALU Operation
        self.dmem_we = Signal()
        self.ld_adr = Signal()
        self.br = Signal()

        self.imm = Signal(32)  # Immediate

        self.iimm = Signal(12)  # I type immediate

        self.simm = Signal(12)  # S-type full immediate
        self.simm1 = Signal(5)  # Sub1 immediate of S type
        self.simm2 = Signal(7)  # Sub2 immediate of S type

        self.uimm = Signal(20)  # U type immediate

        self.sbimm0 = Signal()
        self.sbimm1 = Signal(4)
        self.sbimm2 = Signal(6)
        self.sbimm3 = Signal()
        self.sbimm4 = Signal()
        self.sbimm = Signal(13)  # SB type immediate

        self.ujimm0 = Signal()
        self.ujimm1 = Signal(10)
        self.ujimm2 = Signal()
        self.ujimm3 = Signal(8)
        self.ujimm4 = Signal()
        self.ujimm = Signal(21)  # UJ type immediate

        self.op_b_sel = Signal()  # Operand B select bit for mux (Useful when there is an immediate)
        self.op_a_sel = Signal(2)
        self.csr_sig = Signal()
        #self.csr_offset = Signal(12)

        self.i1 = Signal(32)
        self.i2 = Signal(32)
        self.muxout = Signal(32)
        self.mux3sel = Signal()
        self.ill_instr = Signal()
        self.readsig = Signal()

    # ==========================< Instr Decode >===========================
    def elaborate(self, platform):
        m = Module()
        m.d.comb += [
            self.op.eq(self.instr_dat[0:]),  # op is of 7 bits so (0 to 6)
            self.rd.eq(self.instr_dat[7:]),  # rd is of 5 bits so (7 to 11)
            self.funct3.eq(self.instr_dat[12:]),  # funct3 is of 3 bits so (12 to 14)
            self.rs1.eq(self.instr_dat[15:]),  # rs1 is of 5 bits so (15 to 19)
            self.rs2.eq(self.instr_dat[20:]),  # rs2 is of 5 bits so (20 to 24)
            

            # ====================================Immediate for I type Instruction===========================
            self.iimm.eq(self.instr_dat[20:]),  # iimm is of 12 bits so (20 to 31)

            # ====================================Immediate for S type Instruction===========================
            self.simm1.eq(self.instr_dat[7:]),  # simm1 is of 5 bits so (7 to 11)
            self.simm2.eq(self.instr_dat[25:]),  # simm2 is of 7 bits so (25 to 31)
            self.simm.eq(Cat(self.simm1, self.simm2)),  # simm is of 12 bits, make simm by concatenating both simm1 and simm2

            # ====================================Immediate for SB type Instruction===========================
            self.sbimm0.eq(0),
            self.sbimm1.eq(self.instr_dat[8:]),
            self.sbimm2.eq(self.instr_dat[25:]),
            self.sbimm3.eq(self.instr_dat[7]),
            self.sbimm4.eq(self.instr_dat[31]),
            self.sbimm.eq(Cat(self.sbimm0, self.sbimm1, self.sbimm2, self.sbimm3, self.sbimm4)),

            # ====================================Immediate for UJ type Instruction===========================
            self.ujimm0.eq(0),
            self.ujimm1.eq(self.instr_dat[21:]),
            self.ujimm2.eq(self.instr_dat[20]),
            self.ujimm3.eq(self.instr_dat[12:]),
            self.ujimm4.eq(self.instr_dat[31]),
            self.ujimm.eq(Cat(self.ujimm0, self.ujimm1, self.ujimm2, self.ujimm3, self.ujimm4)),

            self.uimm.eq(self.instr_dat[12:]),

            self.aluop.eq(Cat(self.funct3, self.funct7)), # aluop is of 4 bits, make aluop by concatenating both funct3 and funct7
        ]  
        m.d.comb += [
            self.we.eq(0),
            self.ld_wd.eq(0),
            self.dmem_we.eq(0),
            self.ld_adr.eq(0),
            self.op_a_sel.eq(0),
            self.op_b_sel.eq(0),
            self.br.eq(0),
            
        ]

        # ====================================< R-Type 33 >=====================================
        with m.If(self.op == 0b0110011):  # opcode of R-Type

            m.d.comb += [
                self.we.eq(1),
                self.op_a_sel.eq(0),
                self.dmem_we.eq(0),
                self.ld_adr.eq(0), 
                self.ld_wd.eq(1), 
                self.readsig.eq(0),
            ]
            with m.If(self.instr_dat[30]==1):# funct7 is of 1 bit (30th bit)
                m.d.comb += self.funct7.eq(self.instr_dat[30])
            with m.Elif(self.instr_dat[25] == 1): #checking 25-bit of Funct7 if M-extension is enabled
                m.d.comb += self.mtype.eq(1)
        with m.Else():
            m.d.comb += self.funct7.eq(0)


        # ====================================< I-Type 13 >=====================================
        with m.If(self.op == 0b0010011):  # opcode of I-Type
            m.d.comb += self.imm[0:12].eq(self.iimm)
            m.d.comb += self.aluop[0:3].eq(self.funct3)
            m.d.comb += self.aluop[3].eq(0)

              # put 12 bit iimm in the first 12 bits of imm
            with m.If(self.imm[11] == 1):  # check for sign extension, if it's 1 then convert (13 to 32) bits of imm to 1 otherwise 0
                m.d.comb += self.imm[12:32].eq(0b11111111111111111111)
            with m.Else():
                m.d.comb += self.imm[12:32].eq(0b00000000000000000000)
            m.d.comb += [
                self.we.eq(1),
                self.op_b_sel.eq(1),
                self.dmem_we.eq(0),
                self.ld_adr.eq(0), 
                self.ld_wd.eq(1), 
                self.readsig.eq(0),
            ]

        # ====================================< S-Type 23 >=====================================
        with m.If(self.op == 0b0100011):  # opcode of S-Type
            m.d.comb += self.imm[0:12].eq(self.simm)  # put 12 bit simm in the first 12 bits of imm
            with m.If(self.imm[11] == 1):
                m.d.comb += self.imm[12:32].eq(0b11111111111111111111)
            with m.Else():
                m.d.comb += self.imm[12:32].eq(0b00000000000000000000)
            with m.If(self.funct3 == 0b000):
                m.d.comb += [
                    self.we.eq(0),
                    self.dmem_we.eq(1),
                    self.aluop.eq(0b0000),
                    self.op_b_sel.eq(1),
                    self.mem_mask.eq(0b01),  # sb
                    self.readsig.eq(0),
                ]
            with m.Elif(self.funct3 == 0b001):
                m.d.comb += [
                    self.we.eq(0),
                    self.dmem_we.eq(1),
                    self.aluop.eq(0b0000),
                    self.op_b_sel.eq(1),
                    self.mem_mask.eq(0b10),  # sh
                    self.readsig.eq(0),
                ]
            with m.Elif(self.funct3 == 0b010):
                m.d.comb += [
                    self.we.eq(0),
                    self.dmem_we.eq(1),
                    self.aluop.eq(0b0000),
                    self.op_b_sel.eq(1),
                    self.mem_mask.eq(0b11), # sw
                    self.readsig.eq(0),
                ]

        # ====================================< ld_wd 3 >========================================
        with m.If(self.op == 0b0000011):  # opcode of Load Instruction
            m.d.comb += self.imm[0:12].eq(self.iimm)
            with m.If(self.imm[11] == 1):
                m.d.comb += self.imm[12:32].eq(0b11111111111111111111)
            with m.Else():
                m.d.comb += self.imm[12:32].eq(0b00000000000000000000)
            with m.If(self.funct3 == 0b000):
                m.d.comb += [
                    self.mem_mask.eq(0b01),  # lb
                    self.aluop.eq(0b0000),
                    self.op_b_sel.eq(1),
                    self.ld_wd.eq(0), 
                    self.ld_adr.eq(0), 
                    self.we.eq(1),
                    self.readsig.eq(1),
                ]
            with m.Elif(self.funct3 == 0b001):
                m.d.comb += [
                    self.mem_mask.eq(0b10),  # lh
                    self.aluop.eq(0b0000),
                    self.op_b_sel.eq(1),
                    self.ld_wd.eq(0), 
                    self.ld_adr.eq(0), 
                    self.we.eq(1),
                    self.readsig.eq(1),
                ]
            with m.Elif(self.funct3 == 0b010):
                m.d.comb += [
                    self.mem_mask.eq(0b11),  # lw
                    self.aluop.eq(0b0000),
                    self.op_b_sel.eq(1),
                    self.ld_wd.eq(0), 
                    self.ld_adr.eq(0), 
                    self.we.eq(1),
                    self.readsig.eq(1),
                ]
            with m.Elif(self.funct3 == 0b100):
                m.d.comb += [
                    self.mem_mask.eq(0b01),  # lbu
                    self.aluop.eq(0b0000),
                    self.op_b_sel.eq(1),
                    self.ld_wd.eq(0), 
                    self.ld_adr.eq(0), 
                    self.we.eq(1),
                    self.readsig.eq(1),
                ]
            with m.Elif(self.funct3 == 0b101):
                m.d.comb += [
                    self.mem_mask.eq(0b10),  # lhu
                    self.aluop.eq(0b0000),
                    self.op_b_sel.eq(1),
                    self.ld_wd.eq(0),  
                    self.ld_adr.eq(0), 
                    self.we.eq(1),
                    self.readsig.eq(1),
                ]
            with m.Elif(self.funct3 == 0b110):
                m.d.comb += [
                    self.mem_mask.eq(0b11),  # lwu
                    self.aluop.eq(0b0000),
                    self.op_b_sel.eq(1),
                    self.ld_wd.eq(0), 
                    self.ld_adr.eq(0), 
                    self.we.eq(1),
                    self.readsig.eq(1),
                ]

        # ====================================< U-Type 17 & 27 >=====================================
        with m.If(self.op == 0b0010111):  # AUIPC
            m.d.comb += self.imm[12:32].eq(self.uimm)
            m.d.comb += self.imm[0:12].eq(0b000000000000)
            m.d.comb += [
                self.ld_adr.eq(0),  # TOP Level not Add pc
                self.ld_wd.eq(1), 
                self.aluop.eq(0b0000),
                self.op_b_sel.eq(1),
                self.op_a_sel.eq(1),
                self.we.eq(1),
                self.readsig.eq(0),
            ]

        with m.If(self.op == 0b0110111):  # LUI
            m.d.comb += self.imm[12:32].eq(self.uimm)
            m.d.comb += self.imm[0:12].eq(0b000000000000)
            m.d.comb += [
                self.ld_adr.eq(0),  # TOP Level Add pc
                self.ld_wd.eq(1), 
                self.aluop.eq(0b0000),
                self.op_b_sel.eq(1),
                self.we.eq(1),
                self.readsig.eq(0),
            ]

        # ====================================< SB-Type 63 >=====================================
        with m.If(self.op == 0b1100011):
            m.d.comb += self.imm[0:13].eq(self.sbimm)
            with m.If(self.imm[12] == 1):
                m.d.comb += self.imm[13:32].eq(0b1111111111111111111)
            with m.Else():
                m.d.comb += self.imm[13:32].eq(0b0000000000000000000)
            m.d.comb += [
                self.br.eq(1),
                self.aluop.eq(0b0000),
                self.op_a_sel.eq(2),
                self.op_b_sel.eq(1),
                self.readsig.eq(0),
            ]

        # ====================================< jalr & jal >=====================================
        with m.If(self.op == 0b1100111):  # jalr
            m.d.comb += self.imm[0:12].eq(self.iimm)  # put 12 bit iimm in the first 12 bits
            with m.If (self.imm[11] == 1):#check for sign extension, if it's 1 then convert (13 to 32) bits of imm to 1 otherwise 0
                    m.d.comb += self.imm[12:32].eq(0b11111111111111111111)

            with m.Else ():
                    m.d.comb += self.imm[12:32].eq(0b00000000000000000000)

            m.d.comb += [
                    self.ld_adr.eq(1),
                    self.ld_wd.eq(1), 
                    self.op_a_sel.eq(0),
                    self.op_b_sel.eq(1),
                    self.aluop.eq(0b0000),
                    self.we.eq(1),
                    self.readsig.eq(0),
                ]

        with m.If(self.op == 0b1101111): # jal
                m.d.comb += self.imm[0:21].eq(self.ujimm)
                with m.If (self.imm[20] == 1):
                    m.d.comb += self.imm[21:32].eq(0b11111111111)

                with m.Else ():
                    m.d.comb += self.imm[21:32].eq(0b00000000000)

                m.d.comb += [
                    self.ld_adr.eq(1),
                    self.ld_wd.eq(1), 
                    self.op_a_sel.eq(2),
                    self.op_b_sel.eq(1),
                    self.aluop.eq(0b0000),
                    self.we.eq(1),
                    self.readsig.eq(0),
                ]
#====================csr 73===========================================
        with m.If(self.op == 0b1110011):
            m.d.comb += [
                self.csr_sig.eq(1),
                self.mux3sel.eq(1)
            ]
            with m.If(self.rd != 0):
                m.d.comb += self.we.eq(1)
            with m.Else():
                m.d.comb += self.we.eq(0)

        with m.Else():
            m.d.comb += self.mux3sel.eq(0)
            m.d.comb += self.csr_sig.eq(0)

        
        with m.If((self.op != 0b0110011) & (self.op !=0b0010011) & (self.op != 0b0100011) & (self.op != 0b0000011) & (self.op != 0b0010111) & (self.op != 0b0110111) & (self.op != 0b1100011) & (self.op != 0b1100111) & (self.op != 0b1101111) & (self.op != 0b1110011)):
            m.d.comb +=[
                self.ill_instr.eq(0b1),
                self.funct3.eq(0) 
            ]
        with m.Else():
            m.d.comb += self.ill_instr.eq(0b0)
        
        with m.If(self.op == 0b0000000):
            m.d.comb += self.ill_instr.eq(0b0)
            
        return m
