#include <systemc.h>
#include <iostream>
SC_MODULE(MMIO) {
	sc_in<sc_int<32>> address;
	sc_in<sc_uint<1>>wrt, rd;
	sc_out<sc_uint<1>> time_en, timecmp_en, dmem_en;
	sc_out<sc_int<32>> add_out;

	SC_CTOR(MMIO) {
		SC_METHOD(decoder);
		sensitive << address;

	}
	void decoder() {
		if (address.read().range(31, 30) == 0b01) {
			if (address.read() == 0x4000b000 && wrt.read() == 0b1 || rd.read() == 0b1) { //mtime
				dmem_en.write(0b0);
				timecmp_en.write(0b0);
				time_en.write(0b1);
				add_out.write(address.read());

			}
			else if (address.read() == 0x4000b004 && wrt.read() == 0b1 || rd.read() == 0b1) { //mtimecmp
				dmem_en.write(0b0);
				time_en.write(0b0);
				timecmp_en.write(0b1);
				add_out.write(address.read());

			}
		}
		else if (address.read().range(31, 30) == 0b00) {
			 if ((address.read().range(15, 2) >= 0x0000 && address.read().range(15, 2) <= 0x1fff) && wrt.read() == 0b1 || rd.read() == 0b1) {
				time_en.write(0b0);
				timecmp_en.write(0b0);
				dmem_en.write(0b1);
				add_out.write(address.read());
			 }
		}

	}
};