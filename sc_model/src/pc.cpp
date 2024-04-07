#include<systemc.h>

SC_MODULE(pc) {
	
	sc_in < sc_uint<1>> branchsig,csr_pcsel,branchsel, jump;
	sc_in_clk clk;
	sc_in<sc_int<32>> pc_branch,csr_in;
	sc_out <sc_int<32>> address,pcjal;

	sc_uint<1> AND;
	sc_uint<32>* Pc;
	sc_uint<32>* ptr;
	sc_int<32>pcbyte;
	sc_uint<32>pcbranch ,jal;
	int pcsize = 8192;
	int i;

	SC_CTOR(pc) {
		Pc = new sc_uint<32>[1024];
		ptr = &Pc[0];
		i = 0;

		SC_THREAD(PC_INCR);
		sensitive << clk.pos();
	}
	void PC_INCR() {
		while (true) {

			wait(clk.posedge_event());
			AND = branchsig.read() & branchsel.read();
			if (jump.read() == 0b1) {
				pcbranch = pc_branch.read().to_uint();
				Pc[i] = Pc[i] + pcbranch;
			}

			else if (AND == 0b1) {
				pcbranch = pc_branch.read().to_uint();
				Pc[i] = Pc[i] + pcbranch;
			}
			else if (csr_pcsel.read() == 0b1) {
				Pc[i] = csr_in.read();
			}
			else {
				if (ptr == &Pc[0]) {
					Pc[i] = 0;

				}
				else if (ptr != &Pc[0]) {
					Pc[i] = Pc[i - 1] + 4;
				}
			}
			
			pcbyte = Pc[i].to_int();

			address.write(pcbyte);
			pcjal.write((Pc[i]).to_int() + 4);
				
			ptr++;
			i++;
		}


	}

};