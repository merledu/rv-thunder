from amaranth import *
from amaranth.sim import Simulator

class UARTTransmitter(Elaboratable):
    def __init__(self, delay_frames= 10):
        self.uart_tx = Signal()
        self.tx_data_in = Signal(8)
        self.tx_stb = Signal()
        self.tx_ack = Signal()
        self.tx_ready = Signal()
        self.tx_bit_number = Signal(3)
        self.txPinRegister = Signal()
        self.tx_data_out = Signal(8)
        self.tx_counter = Signal(25)
        self.testmemory = Signal(8)
        self.delay_frames = delay_frames
        #self.half_delay_wait = delay_frames // 2

    def elaborate(self, platform):
        m = Module()
        
        m.d.comb += self.uart_tx.eq(self.txPinRegister)
        with m.FSM() as fsm :
            with m.State(0):
                m.next = "TX_STATE_IDLE"
                m.d.sync += [
                    self.txPinRegister.eq(1),
                    self.tx_counter.eq(0),
                ]
                #m.d.comb += self.tx_ready.eq(1)
                #m.d.sync += self.tx_data_out.eq(0)
                #m.d.sync += self.testmemory.eq(0)
            with m.State("TX_STATE_IDLE"):
                m.d.comb += self.tx_ready.eq(1)
                with m.If((self.tx_ready == 1) & (self.tx_stb == 1)): 
                    m.d.sync += self.testmemory.eq(self.tx_data_in)
                    m.next = "TX_STATE_START_BIT"
                    m.d.sync += [
                        self.tx_counter.eq(0),
                        self.tx_ack.eq(0)
                    ]
                with m.Else():
                    m.d.sync += self.txPinRegister.eq(0b1)
            with m.State("TX_STATE_START_BIT"):
                m.d.sync += self.txPinRegister.eq(0)
                m.d.comb += self.tx_ready.eq(0)
                with m.If(self.tx_counter + 1 == self.delay_frames):
                    m.next = "TX_STATE_Write"
                    m.d.sync +=[
                        self.tx_data_out.eq(self.testmemory),
                        self.tx_bit_number.eq(0),
                        self.tx_counter.eq(0)
                    ]
                with m.Else():
                    m.d.sync += self.tx_counter.eq(self.tx_counter + 1)
            with m.State("TX_STATE_Write"):
                #m.d.comb += self.uart_tx.eq(self.txPinRegister)
                with m.Switch(self.tx_bit_number):
                    for i in range(8):
                        with m.Case(i):
                            m.d.sync += self.txPinRegister.eq(self.tx_data_out[i])
                with m.If(self.tx_counter + 1 == self.delay_frames):
                    with m.If(self.tx_bit_number == 7):
                        m.next = "TX_STATE_Stop_Bit"
                    with m.Else():
                        m.next = "TX_STATE_Write"
                        m.d.sync += self.tx_bit_number.eq(self.tx_bit_number + 1)
                    m.d.sync += self.tx_counter.eq(0)
                with m.Else():
                    m.d.sync += self.tx_counter.eq(self.tx_counter + 1)
            with m.State("TX_STATE_Stop_Bit"):
                m.d.sync += self.txPinRegister.eq(1)
                with m.If(self.tx_counter + 1 == self.delay_frames):
                    m.next = 0
                    m.d.sync += self.tx_counter.eq(0)
                    m.d.sync += self.tx_ack.eq(1)
                with m.Else():
                    m.d.sync += self.tx_counter.eq(self.tx_counter + 1)         
        return m

'''dut=UARTTransmitter()
def bench():
    yield dut.btn1.eq(0)
    yield dut.tx_data_in.eq(55)
    yield dut.valid.eq(1)
    yield
    yield dut.valid.eq(0)
    for i in range(110):
        yield
    yield dut.btn1.eq(1)
    for i in range(14):
        yield
    yield
    yield dut.btn1.eq(0)
    yield dut.tx_data_in.eq(75)
    yield dut.valid.eq(1)
    yield
    yield dut.valid.eq(0)
    for i in range(350):
        yield
  
sim = Simulator(dut)
sim.add_clock(1e-6) # 1 MHz
sim.add_sync_process(bench)
with sim.write_vcd("fsm_tx.vcd"):
    sim.run()


from amaranth.back import verilog
top = UARTTransmitter()
with open("uart_tx.v", "w") as f:
    f.write(verilog.convert(top, ports=[top.uart_tx, top.btn1]))'''
