#include<systemc.h>

SC_MODULE(alu) {
	sc_in<sc_uint<4>> aluop;
	sc_in<sc_int<32>> aluop1, aluop2;
	sc_out<sc_int<32>> alu_out;


	sc_uint<5> rs1_uint, rs2_uint;
	sc_int<32> rd;
	bool sign = 0;


	SC_CTOR(alu) {
		SC_METHOD(rtype);
		sensitive << aluop1<<aluop2;

	}
	void rtype() {

		if (aluop.read() == 0b0000) {
			rd = aluop1.read() + aluop2.read();
		
		}

		else if (aluop.read() == 0b1000) {
			rd = aluop1.read() - aluop2.read();
		}
		else if (aluop.read() == 0b0001) {
			rs2_uint = aluop2.read().range(4, 0).to_uint();

			rd = aluop1.read() << rs2_uint;
		}
		else if (aluop.read() == 0b0010) {
			if (aluop1.read() < aluop2.read())
			{
				rd = 1;
			}
			else {
				rd = 0;
			}
		}
		else if (aluop.read() == 0b0011) {

			rs1_uint = aluop1.read().to_uint();
			rs2_uint = aluop2.read().to_uint();
			if (rs1_uint < rs2_uint)
			{
				rd = 1;
			}
			else {
				rd = 0;
			}

		}
		else if (aluop.read() == 0b0100) {
			
			rd = aluop1.read() ^ aluop2.read();
		}
		else if (aluop.read() == 0b0101) {
			rs2_uint = aluop2.read().range(4, 0).to_uint();

			rd = aluop1.read() >> rs2_uint;
		}
		else if (aluop.read() == 0b1101) {
			rs2_uint = aluop2.read().range(4, 0).to_uint();
			sc_int<32> rs1_int = aluop1.read();
			for (int i = 0; i < rs2_uint; i++) {

				rs1_int = rs1_int >> 1;

				// Shift sign bit into vacant MSB position  
				rs1_int = rs1_int | (rs1_int << 31);

			}

			rd = rs1_int;

		}
		else if (aluop.read() == 0b0110) {

			rd = aluop1.read() | aluop2.read();
		}
		else if (aluop.read() == 0b0111) {

			rd = aluop1.read() & aluop2.read();
		}
		else if (aluop.read() == 0b1111) { // lui
			rd = aluop2.read();
		}
		else if (aluop.read() == 0b1110) {
			rd = aluop1.read();
		}
		
		
		alu_out.write(rd);


	}
};
	