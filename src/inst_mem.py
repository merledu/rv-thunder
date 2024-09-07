from amaranth import *

class instr_mem(Elaboratable):
    def __init__(self):
        # Define the inputs and outputs of the instruction memory module
        self.adr = Signal(13)  # 10-bit address for 8192 (2^13) instructions
        self.dat_r = Signal(32)  # 32-bit RISC-V instruction 
        self.inval_add = Signal()
        # Make a .txt file and put Hexa decimal values in it 
        with open('memory.txt', 'r') as file: # this is the format for open file  
            mem_init_file = file.readlines()
            toint = [int(value, 16) for value in mem_init_file] # Add this line to make it int otherwise it shows an error 
        # Define the instruction memory content (replace this with your actual instructions)
        self.mem = Memory(width=32, depth=8192, init= toint)

    def elaborate(self, platform):
        m = Module()
        # Create a read port for the instruction memory
        m.submodules.rdport = rdport = self.mem.read_port(domain="comb")
        m.d.comb += [
            rdport.addr.eq(self.adr),
            self.dat_r.eq(rdport.data),
            #self.dat_r.eq(rdport.memory[rdport.addr])
            ]  
        with m.If((self.adr < 0x0000) & (self.adr > 0x1fff)):
            m.d.comb += self.inval_add.eq(1)

        return m

