from amaranth import *

class instr_mem(Elaboratable):
    def __init__(self):
        # Define the inputs and outputs of the instruction memory module
        self.adr = Signal(13)  # 10-bit address for 8192 (2^13) instructions
        self.dat_r = Signal(32)  # 32-bit RISC-V instruction output
        # Make a .txt file and put Hexa decimal values in it 
        with open('src/memory.txt', 'r') as file: # this is the format for open file  
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
            self.dat_r.eq(rdport.data)
        ]

        return m

class data_mem(Elaboratable):
    def __init__(self):
        self.adr = Signal(13)
        self.dmem_din = Signal(32)
        self.dmem_dout = Signal(32)
        self.dmem_we = Signal()
        # Create a memory with the specified depth (replace this with your actual data)
        self.memory = Memory(width=32, depth=8192)

    def elaborate(self, platform):
        m = Module()
        # Create a read and write port for the data memory
        m.submodules.rdport = rdport = self.memory.read_port(domain="comb")
        m.submodules.wrport = wrport = self.memory.write_port()
        # Connect the address and data signals
        m.d.comb += [
            rdport.addr.eq(self.adr),
            self.dmem_dout.eq(rdport.data),
            wrport.addr.eq(self.adr),
            wrport.data.eq(self.dmem_din),
            wrport.en.eq(self.dmem_we)  # Enable write operation
        ]

        return m