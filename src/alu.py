from amaranth import *

class ALU(Elaboratable):

    def __init__(self):

        self.aluop = Signal(4)
        self.inp1 = Signal(32)
        self.inp2 = Signal(32)
        self.alu_out = Signal(32)
       
    def elaborate(self, platform):
        m = Module() 

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