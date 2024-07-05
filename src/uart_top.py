from amaranth import *
from uart_tx import *
from uart_rx import *

class uart_top(Elaboratable):
    def __init__(self):
        self.tx_ack = Signal()
        self.rx_ack = Signal()
        self.tx_stb = Signal()
        self.rx_stb = Signal()
        self.tx_data_in = Signal(8)
        self.rx_data_out =Signal(8)
        self.uart_tx = Signal()
        self.uart_rx = Signal()

    def elaborate(self, platform):
        m = Module()
        uart_tx_unit = UARTTransmitter()
        uart_rx_unit = UARTReceiver()
        m.submodules.uart_rx_unit = uart_rx_unit
        m.submodules.uart_tx_unit = uart_tx_unit

        m.d.comb += [
            self.tx_ack.eq(uart_tx_unit.tx_ack),
            self.rx_ack.eq(uart_rx_unit.rx_ack),
            #self.tx_data_in.eq(uart_tx_unit.tx_data_in),
            uart_tx_unit.tx_data_in.eq(self.tx_data_in),
            self.rx_data_out.eq(uart_rx_unit.rx_data_out),
            uart_rx_unit.rx_stb.eq(self.rx_stb),
            uart_tx_unit.tx_stb.eq(self.tx_stb),
            
        ]
        m.d.comb += [
            uart_rx_unit.uart_rx.eq(self.uart_rx),
            self.uart_tx.eq(uart_tx_unit.uart_tx),
        ]
        return m 