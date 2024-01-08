from amaranth import *

class csr(Elaboratable):
    def __init__(self):
        self.csr_sig = Signal(1)
        self.func3 = Signal(3)
        self.rd_in = Signal(5)
        self.rs1_data = Signal(32)
        self.csr_val = Signal(12)
        self.csr_out = Signal(32)
        self.rs1_in = Signal(5)
        
    
    def elaborate(self, platform):
        m = Module() 
        rs1_data12 = self.rs1_data[0:12]
        
        with m.If(self.csr_sig == 1):
            with m.If(self.func3 == 0b001):
                csr_value = rs1_data12
                with m.If (self.rd_in != 0b00000): 
                    m.d.comb += self.csr_out.eq(self.csr_val),
                    prevcsr = self.csr_val
                    


            with m.Elif(self.func3 == 0b010):
                with m.If(self.rd_in != 0b00000):
                    self.csr_out = csr_value
					
                with m.If(self.rs1_in != 0b00000):
                    csr_value = self.csr_val | rs1_data12
					
            with m.Elif(self.func3 == 0b011):
                with m.If(self.rd_in != 0b00000):
                    self.csr_out = csr_value

                with m.If (self.rs1_in != 0b00000):
                    csr_value = self.csr_val & rs1_data12
					


            with m.Elif (self.func3 == 0b101):
                csr_value = self.csr_val
                csr_value = self.rs1_in
				
                with m.If (self.rd_in != 0b00000):
                        self.csr_out = prevcsr,
                        prevcsr = csr_value
                        

            with m.Elif (self.func3 == 0b110):
                with m.If (self.rd_in != 0b00000):

                    self.csr_out = csr_value

                with m.If (self.rs1_in != 0b00000):
                    csr_value = self.csr_val | self.rs1_in   # contains the immediate
					
            with m.Elif (self.func3 == 0b111):
                with m.If (self.rd_in != 0b00000):
                    self.csr_out = csr_value

                with m.If (self.rs1_in != 0b00000):
                    csr_value = self.csr_val & self.rs1_in # contains the immediate
				    
            return m


