from amaranth import *

class branch(Elaboratable):        

    def __init__(self):
        self.op1 = Signal(32) # connect with reg file out1
        self.op2 = Signal(32) # connect with reg file out2
        self.func3 = Signal(3) # connect with control unit func3
        self.br_out = Signal()

    def elaborate(self, platform):
        m = Module()

        with m.If(self.func3 == 0b000): #beq
            m.d.comb += self.br_out.eq(self.op1 == self.op2)

        with m.Elif(self.func3 == 0b001): #bne
            m.d.comb += self.br_out.eq(self.op1 != self.op2)

        with m.Elif(self.func3 == 0b100): #blt
            m.d.comb += self.br_out.eq(self.op1 < self.op2)

        with m.Elif(self.func3 == 0b101): #bge 
            m.d.comb += self.br_out.eq(self.op1 >= self.op2)

        with m.Elif(self.func3 == 0b110): #bltu
            m.d.comb += self.br_out.eq(self.op1.as_unsigned() < self.op2.as_unsigned())

        with m.Elif(self.func3 == 0b111): #bgeu
            m.d.comb += self.br_out.eq(self.op1.as_unsigned() >= self.op2.as_unsigned())
    
        return m