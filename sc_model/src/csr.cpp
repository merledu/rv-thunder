#define mip =0h344;
#define mie =0h304;
#define mstatus =0h300;
#define mcause =0h342;
#define mie =0h304;
#define mtvec =0h305;
#define mepc =0h341;

#include <systemc.h>

SC_MODULE(CSR) {
	sc_in <bool> csr_sig;
	sc_in <sc_uint<3>> func3;
	sc_in <sc_uint<5>>  rd_in,rs1_in;
	sc_in<sc_int<32>> rs1_data;
	sc_in <sc_uint<12>> csr_val;
	sc_out<sc_int<32>> csr_out;
	
	sc_int<12> csr_value,prevcsr;
	sc_uint<32> mip_reg, mie_reg, mstatus_reg, mcause_reg, mepc_reg,mtvec_rec;
	
	SC_CTOR(CSR) {
		SC_METHOD(operations);
		sensitive << csr_sig << rd_in << rs1_data;

	}
	void operations(){
		if (csr_sig.read() == true) {
			//===================CSRRW===================================================
			
			if (func3.read() == 0b001) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(prevcsr.to_int());
					prevcsr = csr_val.read();
					
				}
				csr_value=rs1_data.read().range(11, 0);	
				
			}
			//======================CSRRS================================================
			else if (func3.read() == 0b010) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(csr_value);
					
				}
				if (rs1_in.read() != 0b00000) {
					csr_value = (csr_val.read() | rs1_data.read().range(11, 0));
					
				}

			}
			//======================CSRRC==============================================
			else if (func3.read() == 0b011) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(csr_value);

				}
				if (rs1_in.read() != 0b00000) {
					csr_value= (csr_val.read() & rs1_data.read().range(11, 0));
					
				}

			}
			//=====================CSRRWI===============================================
			else if (func3.read() == 0b101) {
				csr_value = csr_val.read();

				
					if (rd_in.read() != 0b00000) {

						csr_out.write(prevcsr.to_int());
						prevcsr = csr_value;
					}

					csr_value= rs1_in.read().to_int();  // contains the immediate

			}
			//======================CSRRSI==============================
			else if (func3.read() == 0b110) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(csr_value);

				}
				if (rs1_in.read() != 0b00000) {
					csr_value = (csr_val.read() | rs1_in.read());  // contains the immediate
					
				}

			}
			//=================CSRRCI=================================
			else if (func3.read() == 0b111) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(csr_value);

				}
				if (rs1_in.read() != 0b00000) {
					csr_value= (csr_val.read() & rs1_in.read()); // contains the immediate
				
				}

			}
			cout << "csr value :" << csr_value << hex << endl;
		}	
		
	}

};