#include<systemc.h>
SC_MODULE(branch) {
	
	sc_in<sc_int<32>> OPA;
	sc_in<sc_int<32>> OPB;
	sc_in <sc_uint<3>> func3;
	sc_out<sc_uint<1>> branch_out;
	sc_uint<32 > unsopa, unsopb;
	sc_uint<1> Branch;

	SC_CTOR(branch) {
		Branch = 0;
		SC_METHOD(operations);
		sensitive <<OPA<<OPB<<func3;


	}
	void operations() {
		
			if (func3.read() == 0b000) {
				if (OPA.read() == OPB.read()) {
					Branch = 0b1;
				}
				else {
					Branch = 0b0;
				}
				
				
			}
			else if (func3.read() == 0b001) {
				if (OPA.read() != OPB.read()) {
					Branch = 0b1;
				}
				else {
					Branch = 0b0;
				}
				
			}
			else if (func3.read() == 0b100) {
				if (OPA.read() < OPB.read()) {
					Branch = 0b1;
				}
				else {
					Branch = 0b0;
				}
				
			}
			else if (func3.read() == 0b101) {
				if (OPA.read() >= OPB.read()) {
					Branch = 0b1;
				}
				else {
					Branch = 0b0;
				}
				
			}
			else if (func3.read() == 0b110) {
				unsopa = OPA.read().to_uint();
				unsopb = OPB.read().to_uint();
				if (unsopa < unsopb) {
					Branch = 0b1;
				}
				else {
					Branch = 0b0;
				}
			
			}
			else if (func3.read() == 0b111) {
				unsopa = OPA.read().to_uint();
				unsopb = OPB.read().to_uint();
				if (unsopa >= unsopb) {
					Branch = 0b1;
				}
				else {
					Branch = 0b0;
				}
				
			}
			branch_out.write(Branch);
		
		
	}
};