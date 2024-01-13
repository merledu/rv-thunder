
#include <systemc.h>

SC_MODULE(CSR) {
	sc_in <bool> csr_sig,interrupt,ti_intr,ex_intr;
	sc_in <sc_uint<3>> func3;
	sc_in <sc_uint<5>>  rd_in,rs1_in;
	sc_in<sc_int<32>> rs1_data,pc;
	sc_in <sc_uint<12>> csr_val;
	sc_out<sc_int<32>> csr_out,pc_out,trap_add;
	
	sc_int<12> prevcsr;
	sc_int<12> csr_value;
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
				csr_value=rs1_data.read();	
				
			}
			//======================CSRRS================================================
			else if (func3.read() == 0b010) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(csr_value);
					
				}
				if (rs1_in.read() != 0b00000) {
					csr_value = (csr_val.read() | rs1_data.read());
					
				}

			}
			//======================CSRRC==============================================
			else if (func3.read() == 0b011) {
				if (rd_in.read() != 0b00000) {

					csr_out.write(csr_value);

				}
				if (rs1_in.read() != 0b00000) {
					csr_value= (csr_val.read() & rs1_data.read());
					
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
			
		}	
		if (csr_val.read() ==0x304) {
			mie_reg = csr_value;
		}
		else if (csr_val.read() == 0x344) {
			mip_reg = csr_value;
		}
		else if (csr_val.read() == 0x300) {
			mstatus_reg = csr_value;
		}
		else if (csr_val.read() == 0x342) {
			mcause_reg = csr_value;
		}
		else if (csr_val.read() == 0x305) {
			mtvec_rec = csr_value;
		}
		else if (csr_val.read() == 0x341) {
			mepc_reg = csr_value;
		}

		//interrupt code in mcause
		if (interrupt.read() == true) {
			mstatus_reg.range(3, 3) = 0b1;  //mie bit
			mstatus_reg.range(7, 7) = 0b1;  //mpie bit
			mcause_reg.range(31, 31) = 0b1; // setting msb for interrupt
			mepc_reg = pc.read();
			if (mcause_reg.range(31, 31) == 0b1) {
				if (mcause_reg.range(7, 7) == true) { // checking timer interrupt
					mip_reg.range(7, 7) = 0b1; //machine  timer interrupt pending bit
					mie_reg.range(7, 7) = 0b1; //machine timer interrupt enable bit
				}
				else if (mcause_reg.range(11, 11) == true) { // checking external  interrupt
					mip_reg.range(11, 11) = 0b1; //machine  external interrupt pending bit
					mie_reg.range(11, 11) = 0b1; //machine external interrupt enable bit
				}
			}
			if (mtvec_rec.range(1, 0) == 0b00) {  //direct mode
				trap_add.write(mtvec_rec.range(31, 2).to_int());
			}
			else if (mtvec_rec.range(1, 0) == 0b01) {
				trap_add.write(mtvec_rec.range(31, 2) + (mcause_reg.range(30, 0) << 2)); //vectored mode
			}

			//trap_add.write(csr_value);
			if (csr_val.read() == 0b001100000010) { //mret value
				pc_out.write(mepc_reg.to_int());
				mstatus_reg = 0;
				mcause_reg = 0;
				mtvec_rec = 0;
				mip_reg = 0;
				mie_reg = 0;

			}
		}
			
		
		
	}

};