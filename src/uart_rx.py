from amaranth import *
from amaranth.sim import Simulator

class UARTReceiver(Elaboratable):
    def __init__(self, delay_frames=10):
        self.uart_rx = Signal()
        #self.led = Signal(8)
        self.rx_ack = Signal()
        self.rx_stb = Signal()
        self.rx_ready = Signal()
        self.rx_counter = Signal(13)
        self.rx_data_out =Signal(8)
        self.rx_bit_number = Signal(3)

        self.delay_frames = delay_frames
        self.half_delay_wait = delay_frames // 2
    

    def elaborate(self, platform):
        m = Module()
        with m.FSM() as fsm :
            with m.State(0):
                m.d.sync += self.rx_data_out.eq(0)
                m.next = "RX_STATE_IDLE"
                m.d.sync += self.rx_ack.eq(0)
                
            with m.State("RX_STATE_IDLE"):
                
                m.d.comb += self.rx_ready.eq(1)
                with m.If((self.rx_ready == 1) & (self.rx_stb == 1)):
                    with m.If(self.uart_rx == 0):
                        m.next = "RX_STATE_START_BIT"
                        m.d.sync += [
                            self.rx_counter.eq(1),
                            self.rx_bit_number.eq(0),
                            # self.rx_ack.eq(0)
                            #m.d.sync += self.rx_ack.eq(0)
                    ]
            with m.State("RX_STATE_START_BIT"):
                m.d.comb += self.rx_ready.eq(0)
                with m.If(self.rx_counter == self.half_delay_wait):
                    m.next = "RX_STATE_READ_WAIT"
                    m.d.sync += self.rx_counter.eq(1)
                with m.Else():
                    m.d.sync += self.rx_counter.eq(self.rx_counter + 1)
            with m.State("RX_STATE_READ_WAIT"): 
                m.d.sync += self.rx_counter.eq(self.rx_counter + 1)
                with m.If(self.rx_counter + 1 == self.delay_frames):
                    m.next = "RX_STATE_READ"
            with m.State("RX_STATE_READ"):
                m.d.sync += self.rx_counter.eq(1)
                m.d.sync += self.rx_data_out.eq(Cat(self.uart_rx, self.rx_data_out))
                m.d.sync += self.rx_bit_number.eq(self.rx_bit_number + 1)
                with m.If(self.rx_bit_number == 7 ):
                    m.next = "RX_STATE_STOP_BIT"
                with m.Else():
                    m.next = "RX_STATE_READ_WAIT"
            with m.State("RX_STATE_STOP_BIT"):
                m.d.sync += self.rx_counter.eq(self.rx_counter + 1)
                with m.If(self.rx_counter + 1 == self.delay_frames):
                    m.next = 0
                    m.d.sync += [
                        self.rx_counter.eq(0),
                        self.rx_ack.eq(1),
                        #self.led.eq(self.data_in[0:8])
                    ]
        # with m.If(self.byte_ready==1):
        #     m.d.sync += self.led.eq(self.data_in[0:8]) # Just for debug
        return m
    


'''from amaranth.back import verilog
top = UARTReceiver()
with open("uart_rx1.v", "w") as f:
    f.write(verilog.convert(top, ports=[top.uart_rx]))

dut=UARTReceiver()
def bench():
    yield
    yield
    yield
    yield dut.rx_stb.eq(1)
    yield dut.uart_rx.eq(0)
    yield
    yield dut.uart_rx.eq(1)  # Shows the 1 start bit is detected correctly
    for i in range(434):
        yield
    yield dut.uart_rx.eq(0)  # Go first data bit uart_rx in lsb (0) postion of data_in
    for j in range(868):
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in              
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 1 postion
        yield
    yield dut.uart_rx.eq(0)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 2 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 3 postion
        yield
    yield dut.uart_rx.eq(0)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 4 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 5 postion
        yield
    yield dut.uart_rx.eq(0)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 6 postion
        yield
    yield dut.uart_rx.eq(1)  # This also go second data bit uart_rx in lsb of data_in  
    for j in range(868):     #but previous data bit value of uart_rx goes into data_in on 7 postion
        yield
    for j in range(867):     # In this bytes_ready value is 1  so it mean one byte has been received
        yield 



        
    #for _ in range(8):
        #yield dut.uart_rx.eq(1)
        #for k in range(868):
            #yield 
    #yield dut.uart_rx.eq(0)
    

    
sim = Simulator(dut)
sim.add_clock(1e-6) # 1 MHz
sim.add_sync_process(bench)
with sim.write_vcd("wb_uart_rx.vcd"):
    sim.run()'''  