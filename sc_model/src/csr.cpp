
#include <systemc.h>

SC_MODULE(CSR) {
	sc_in <bool> csr_sig;
	sc_in <sc_uint<3>> func3;
	sc_in <sc_uint<5>>  rd_in,rs1_in;
	sc_in<sc_int<32>> rs1_data,pc,instr;
	sc_in <sc_uint<12>> csr_val;
	sc_out<sc_int<32>> csr_out,pc_out,trap_add;
	sc_in <sc_uint<1>> ill_instr;
	
	
	
	sc_uint<32> mip_reg, mie_reg, mstatus_reg, mcause_reg, mepc_reg,mtvec_rec,mtval_reg;
	sc_int<32> csr_reg;
	
	
	SC_CTOR(CSR) {
		SC_METHOD(operations);
		sensitive << csr_sig << rd_in << rs1_data;

	}
	void operations(){
		if (csr_sig.read() == true) {
			//===================CSRRW===================================================
			
			if (func3.read() == 0b001) {
				if (csr_val.read() == 0x342) {


					if (rd_in.read() != 0b00000) {

						csr_out.write(csr_reg);


					}
				}
				csr_reg=rs1_data.read();	
				
			}
			//======================CSRRS================================================
			else if (func3.read() == 0b010) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(csr_reg);
					
				}
				if (rs1_in.read() != 0b00000) {
					csr_reg = (csr_val.read() | rs1_data.read());
					
				}

			}
			//======================CSRRC==============================================
			else if (func3.read() == 0b011) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(csr_reg);

				}
				if (rs1_in.read() != 0b00000) {
					csr_reg= (csr_val.read() & rs1_data.read());
					
				}

			}
			//=====================CSRRWI===============================================
			else if (func3.read() == 0b101) {
				

				
					if (rd_in.read() != 0b00000) {

						csr_out.write(csr_reg);
						
					}

					csr_reg= rs1_in.read().to_int();  // contains the immediate

			}
			//======================CSRRSI==============================
			else if (func3.read() == 0b110) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(csr_reg);

				}
				if (rs1_in.read() != 0b00000) {
					csr_reg = (csr_val.read() | rs1_in.read());  // contains the immediate
					
				}

			}
			//=================CSRRCI=================================
			else if (func3.read() == 0b111) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(csr_reg);

				}
				if (rs1_in.read() != 0b00000) {
					csr_reg= (csr_val.read() & rs1_in.read()); // contains the immediate
				
				}

			}
			
		}	
		if (csr_val.read() ==0x304) {
			mie_reg = csr_reg;
		}
		else if (csr_val.read() == 0x344) {
			mip_reg = csr_reg;
		}
		else if (csr_val.read() == 0x300) {
			mstatus_reg = csr_reg;
		}
		else if (csr_val.read() == 0x342) {
			mcause_reg = csr_reg;
		}
		else if (csr_val.read() == 0x305) {
			mtvec_rec = csr_reg.range(31,2);
		}
		else if (csr_val.read() == 0x341) {
			mepc_reg = csr_reg;
		}
		if (ill_instr.read() == 0b1) {
			mepc_reg = pc.read();
			mtval_reg = instr.read();
			mcause_reg.range(31, 31) = 0b0;
			mcause_reg.range(2, 2) = 0b1;
			mtvec_rec.range(1, 0) = 0b00;
			mtvec_rec.range(31, 2) = 0xbc; //exception handler address
		 }
		
			

			
			if (csr_val.read() == 0b001100000010) { //mret value
				pc_out.write(mepc_reg.to_int()+4);
				mstatus_reg = 0;
				mcause_reg = 0;
				mtvec_rec = 0;
				mip_reg = 0;
				mie_reg = 0;

			}
		
			
		
		
	}

};