from amaranth import *
from amaranth.sim import Simulator

# Import the defined modules
from fetch import *
from control import *
from regfile import *
from alu import *
#from inst_mem import *
#from data_mem import *
from branch import *
from csr import *
from inv_or import *

# Create a top-level module that connects the modules
class TopModule(Elaboratable):
    def __init__(self):
        self.data_mem_adr = Signal(32)
        self.data_mem_we = Signal()
        self.data_mem_out = Signal(32)
        self.data_mem_in = Signal(32)
        self.data_mem_invadd = Signal()
        self.data_mem_mask = Signal(2)
        self.readsig = Signal()
        self.writedata = Signal(32)
        self.inst_mem_adr = Signal(13)
        self.inst_dat_r = Signal(32)
        self.inst_inval_add = Signal()
        
    
    def elaborate(self, platform):
        m = Module()

        # Instantiate each module
        csr_unit = csr()
        inv_or_unit = inv_or()
        fetch_unit = FetchUnit()
        control_unit = control()
        reg_file = regfile()
        branch_unit = branch()
        alu = ALU()
        #inst_memory_unit = instr_mem()
        #data_memory_unit = data_mem()

        # Connect modules together
        m.submodules.fetch_unit = fetch_unit
        m.submodules.control_unit = control_unit
        m.submodules.reg_file = reg_file
        m.submodules.alu = alu
        m.submodules.branch_unit = branch_unit
        #m.submodules.inst_memory_unit = inst_memory_unit
        #m.submodules.data_memory_unit = data_memory_unit
        m.submodules.csr_unit = csr_unit
        m.submodules.inv_or_unit = inv_or_unit
#===========================< Instruction memory connection >===========================
        m.d.comb += [
            self.inst_mem_adr.eq(fetch_unit.pc[2:15]),
            #inst_memory_unit.adr.eq(fetch_unit.pc[2:15]),
            control_unit.instr_dat.eq(self.inst_dat_r),  
            alu.aluop.eq(control_unit.aluop),
#===========================< Registers Connections >===========================
            reg_file.rs1.eq(control_unit.rs1),
            reg_file.rs2.eq(control_unit.rs2),
            reg_file.rd.eq(control_unit.rd),
            reg_file.we.eq(control_unit.we),

            branch_unit.op1.eq(reg_file.rf_out1), #####
            branch_unit.op2.eq(reg_file.rf_out2), #####
            branch_unit.func3.eq(control_unit.funct3),
            
            #self.data_mem_adr.eq(alu.alu_out[2:15]),
            self.data_mem_we.eq(control_unit.dmem_we),
            self.data_mem_mask.eq(control_unit.mem_mask),
            self.data_mem_adr.eq(alu.alu_out),
            self.writedata.eq(reg_file.wb_data),
            self.readsig.eq(control_unit.readsig),
            #data_memory_unit.adr.eq(alu.alu_out[2:15]),
            #data_memory_unit.dmem_we.eq(control_unit.dmem_we),

#====================== csr connections ===================================            
            
            #control_unit.i1.eq(self.data_mem_out),
            control_unit.i1.eq(reg_file.wb_data),
            csr_unit.csr_sig.eq(control_unit.csr_sig),
            csr_unit.func3.eq(control_unit.funct3),
            csr_unit.rd_in.eq(control_unit.rd),
            csr_unit.rs1_data.eq(reg_file.rf_out1),
            csr_unit.rs1_in.eq(control_unit.rs1),
            control_unit.i2.eq(csr_unit.csr_out),
            control_unit.muxout.eq(reg_file.wb_data),
            #reg_file.wb_data.eq(control_unit.muxout),
            csr_unit.ill_instr.eq(control_unit.ill_instr),
            csr_unit.pc.eq(fetch_unit.pc),
            fetch_unit.csr_pcsel.eq(csr_unit.pc_sel),
            fetch_unit.csr_in.eq(csr_unit.pc_out)
         ]
        
#=========================Invalid Or connection ==============================
        m.d.comb += [
            inv_or_unit.in1.eq(self.inst_inval_add),
            #inv_or_unit.in2.eq(data_memory_unit.inv_add),
            inv_or_unit.in2.eq(self.data_mem_invadd), 
        ]
#==========================< Operand b select >========================
        with m.If (control_unit.op_b_sel == 1):
            m.d.comb += alu.inp2.eq(control_unit.imm) 
        with m.Else ():
            m.d.comb += alu.inp2.eq(reg_file.rf_out2) 

#==========================< Operand a select >========================
        with m.If (control_unit.op_a_sel == 0):
            m.d.comb += alu.inp1.eq(reg_file.rf_out1) 
        with m.Elif (control_unit.op_a_sel == 1):
            m.d.comb += alu.inp1.eq(fetch_unit.pc[0:12]) 
        with m.Elif (control_unit.op_a_sel == 2):
            m.d.comb += alu.inp1.eq(fetch_unit.pc) 
        with m.Else ():
            m.d.comb += alu.inp1.eq(0x00000000) 

#==========================< Update Pc and Branch select >========================

        with m.If (control_unit.op == 0b1100011):
            m.d.comb += [
                fetch_unit.branch.eq(control_unit.br & branch_unit.br_out),     #branch 
                fetch_unit.branch_tar.eq(alu.alu_out),
                ]
        with m.Elif (control_unit.op == 0b1100111):
            m.d.comb += [
                fetch_unit.branch.eq(1),    #jalr signal 
                fetch_unit.branch_tar.eq(alu.alu_out),
            ]

        with m.Elif (control_unit.op == 0b1101111):
            m.d.comb += [
                fetch_unit.branch.eq(1),    #jal signal
                fetch_unit.branch_tar.eq(alu.alu_out),
            ]

#==========================< load data from memory Or store address of next_pc/ jal/ jalr in regfile >========================
        with m.If(control_unit.ld_wd == 0): #######################################
            
            with m.If(self.data_mem_mask == 0b11):  
                with m.If(control_unit.funct3==0b010): #lw
                    #m.d.comb += reg_file.wb_data.eq(data_memory_unit.dmem_dout) 
                    m.d.comb += reg_file.wb_data.eq(self.data_mem_out) 

            with m.If(self.data_mem_mask == 0b11):  
                with m.If(control_unit.funct3==0b110): #lwu
                    #m.d.comb += reg_file.wb_data.eq(data_memory_unit.dmem_dout) 
                    m.d.comb += reg_file.wb_data.eq(self.data_mem_out) 

            with m.If(self.data_mem_mask == 0b10):
                with m.If(control_unit.funct3==0b001): #lh
                    #m.d.comb += reg_file.wb_data.eq(data_memory_unit.dmem_dout[0:16]) 
                    m.d.comb += reg_file.wb_data.eq(self.data_mem_out[0:16]) 

                    #with m.If(data_memory_unit.dmem_dout[16] == 1): 
                    with m.If(self.data_mem_out[16] == 1): 
                    
                        m.d.comb += reg_file.wb_data[16:32].eq(0b1111111111111111)
                    with m.Else():
                        m.d.comb += reg_file.wb_data[16:32].eq(0b0000000000000000)
            with m.If(self.data_mem_mask == 0b10):
                with m.If(control_unit.funct3==0b101): #lhu
                    #m.d.comb += reg_file.wb_data.eq(data_memory_unit.dmem_dout[0:16])
                    m.d.comb += reg_file.wb_data.eq(self.data_mem_out[0:16])
            with m.If(self.data_mem_mask == 0b01):
                with m.If(control_unit.funct3==0b000): #lb
                    #m.d.comb += reg_file.wb_data.eq(data_memory_unit.dmem_dout[0:8]) 
                    m.d.comb += reg_file.wb_data.eq(self.data_mem_out[0:8]) 
                    #with m.If(data_memory_unit.dmem_dout[8] == 1): 
                    with m.If(self.data_mem_out[8] == 1):
                        m.d.comb += reg_file.wb_data[8:32].eq(0b111111111111111111111111)
                    with m.Else():
                        m.d.comb += reg_file.wb_data[8:32].eq(0b000000000000000000000000)
            with m.If(self.data_mem_mask == 0b01):
                with m.If(control_unit.funct3==0b100): #lbu
                    #m.d.comb += reg_file.wb_data.eq(data_memory_unit.dmem_dout[0:8]) 
                    m.d.comb += reg_file.wb_data.eq(self.data_mem_out[0:8])

        with m.Else ():
            with m.If (control_unit.ld_adr == 0b1):
                m.d.comb += reg_file.wb_data.eq(fetch_unit.pc + 4)

            with m.Else ():
                m.d.comb += reg_file.wb_data.eq(alu.alu_out)

#==================store====================================
        with m.If(self.data_mem_we == 1):
            with m.If(self.data_mem_mask == 0b11):
                #m.d.comb += data_memory_unit.dmem_din.eq(reg_file.rf_out2)   #####
                m.d.comb += self.data_mem_in.eq(reg_file.rf_out2)
            with m.Elif(self.data_mem_mask == 0b10):
                #m.d.comb += data_memory_unit.dmem_din.eq(reg_file.rf_out2[0:16]) #####
                m.d.comb += self.data_mem_in.eq(reg_file.rf_out2[0:16])
            with m.Elif(self.data_mem_mask == 0b01):
                #m.d.comb += data_memory_unit.dmem_din.eq(reg_file.rf_out2[0:8]) #####
                m.d.comb += self.data_mem_in.eq(reg_file.rf_out2[0:8])
#==============csr============================
        with m.If(control_unit.op == 0b1110011):
            m.d.comb += csr_unit.csr_val.eq(self.inst_dat_r[20:32])
   
#================ Mux connection ========================
        with m.If(control_unit.mux3sel == 0):
            m.d.comb += control_unit.muxout.eq(control_unit.i1)
                
        with m.Else():
            m.d.comb += control_unit.muxout.eq(control_unit.i2)

#================ mtime ==================================


        return m

# Simulate the top module
'''dut = TopModule()
def bench():
    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield

    yield
    yield
    yield
    yield
    yield
# We can provide initial values for signals above

sim = Simulator(dut)
sim.add_clock(1e-6)  #Add clock
sim.add_sync_process(bench)
with sim.write_vcd("sim.vcd"): # Generate Vcd, which is useful to see a result in GTKwave
    sim.run()'''
