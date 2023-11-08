#include<systemc.h>

SC_MODULE(mux2bit){
	sc_in<sc_int<32>> in1, in2, in3, in4;
	sc_out <sc_int<32>> out;
	sc_in<sc_uint<2>> insel;

	SC_CTOR(mux2bit) {
		SC_METHOD(operations);
		sensitive << insel<<in1<<in2<<in3<<in4;

	}
	void operations() {
		if (insel.read() == 0b00) {
			out.write(in1);
		}
		else if (insel.read() == 0b01) {
			out.write(in2);
		}
		else if (insel.read() == 0b10) {
			out.write(in3);
		}
		else if (insel.read() == 0b11) {
			out.write(in4);
		}
	}

};