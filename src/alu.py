from amaranth import *

class ALU(Elaboratable):

    def __init__(self):

        self.aluop = Signal(4)
        self.inp1 = Signal(32)
        self.inp2 = Signal(32)
        self.alu_out = Signal(32)
        self.mtype = Signal()
        self.m_alu_out = Signal (64)

       
    def elaborate(self, platform):
        m = Module() 

        with m.If(self.mtype == 1): # Checking that M-type Extension is high
            with m.If(self.aluop == 0b0000): #Mul
                m.d.comb += [
                self.m_alu_out.eq(self.inp1 * self.inp2), #Transfer 64-bit after Multiple 
                self.alu_out.eq(self.m_alu_out[0:32]) #Taking only first 32 bit from 64bit
                ]
            with m.Elif(self.aluop == 0b0001): #Mulh
                m.d.comb += [
                self.m_alu_out.eq(self.inp1.as_signed() * self.inp2.as_signed()),
                self.alu_out.eq(self.m_alu_out[32:]) # Taking most significant 32 bit from 64bit
                ]
            with m.Elif(self.aluop == 0b0010): #Mulh(S)(U)
                m.d.comb += [
                self.m_alu_out.eq(self.inp1.as_signed() * self.inp2.as_unsigned()),
                self.alu_out.eq(self.m_alu_out[32:])
                ]
            with m.Elif(self.aluop == 0b0011): #Mulh(U)
                m.d.comb += [
                self.m_alu_out.eq(self.inp1.as_unsigned() * self.inp2.as_unsigned()),
                self.alu_out.eq(self.m_alu_out[32:])
                ]
            with m.Elif(self.aluop == 0b0100): #Div
                with m.If(self.inp2 == 0): #IF Divided By Zero
                    m.d.comb += self.alu_out.eq(-1)
                with m.Elif((self.inp1 == 0x80000000) & (self.inp2 == 0xffffffff)): #Signed overflow
                    m.d.comb += self.alu_out.eq(self.inp1)
                with m.Else():
                    m.d.comb += self.alu_out.eq(self.inp1 // self.inp2)

            with m.Elif(self.aluop == 0b0101): #Div(U)
                with m.If(self.inp2 == 0): #IF Divided By Zero
                    m.d.comb += self.alu_out.eq(4294967295)
                with m.Else():
                    m.d.comb += self.alu_out.eq(self.inp1.as_unsigned() // self.inp2.as_unsigned())
            
            with m.Elif(self.aluop == 0b0110): #Rem
                with m.If(self.inp2 == 0): #IF Division By Zero
                    m.d.comb += self.alu_out.eq(self.inp1)
                with m.Elif((self.inp1 == 0x80000000) & (self.inp2 == 0xffffffff)): #Signed overflow
                    m.d.comb += self.alu_out.eq(0)
                with m.Else():
                    m.d.comb += self.alu_out.eq(self.inp1 % self.inp2)

            with m.Elif(self.aluop == 0b0111): #Rem(U)
                with m.If(self.inp2 == 0): #IF Division By Zero
                    m.d.comb += self.alu_out.eq(self.inp1)
                with m.Else():
                    m.d.comb += self.alu_out.eq(self.inp1.as_unsigned() % self.inp2.as_unsigned())
            
                
        with m.Else():
            forshft = self.inp2 & 0x1F
            forshft1 = forshft[0:5]
        
            with m.If(self.aluop == 0b0000): #Add,ADDI
                m.d.comb += self.alu_out.eq(self.inp1 + self.inp2)

            with m.Elif(self.aluop == 0b0001): #SLL,SLLI
                m.d.comb += self.alu_out.eq(self.inp1 << (forshft1))

            with m.Elif(self.aluop == 0b0010): #SLT,SLTI
                m.d.comb += self.alu_out.eq(self.inp1 <= self.inp2)

            with m.Elif(self.aluop == 0b0011): #SLTU,SLTIU 
                m.d.comb += self.alu_out.eq(self.inp1.as_unsigned() <= self.inp2.as_unsigned())

            with m.Elif(self.aluop == 0b0100): #XOR,XORI
                m.d.comb += self.alu_out.eq(self.inp1 ^ self.inp2)

            with m.Elif(self.aluop == 0b0101): #SRL,SRLI
                m.d.comb += self.alu_out.eq(self.inp1 >> (forshft1))
        
            with m.Elif(self.aluop == 0b0110): #OR,ORI
                m.d.comb += self.alu_out.eq(self.inp1 | self.inp2)

            with m.Elif(self.aluop == 0b0111): #AND,ANDI
                m.d.comb += self.alu_out.eq(self.inp1 & self.inp2)  

            with m.Elif(self.aluop == 0b1000): #SUB
                m.d.comb += self.alu_out.eq(self.inp1 - self.inp2)

            with m.Elif(self.aluop == 0b1101): #SRA,SRAI
                m.d.comb += self.alu_out.eq(Cat(self.inp1[-1], self.inp1[:-1]) >> self.inp2)
        



        return m