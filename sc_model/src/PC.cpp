#include<systemc.h>

SC_MODULE(PC) {
	sc_in < sc_uint<1>> branchsel,jump;
	sc_in < sc_uint<1>> branchsig;
	sc_in_clk clk;
	
	sc_in<sc_int<32>> pc_branch;
	sc_out <sc_int<32>> address,pcjal;
	sc_uint<1> AND;
	sc_uint<32>* pc;
	sc_uint<32>* ptr;
	sc_int<32>pcbyte;
	sc_uint<32>pcbranch ,jal;
	int pcsize = 8192;
	int i;

	SC_CTOR(PC) {
		pc = new sc_uint<32>[1024];
		ptr = &pc[0];
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
				pc[i] = pc[i] + pcbranch;
			}

			else if (AND == 0b1) {
				pcbranch = pc_branch.read().to_uint();
				pc[i] = pc[i] + pcbranch;
			}
			else {
				if (ptr == &pc[0]) {
					pc[i] = 0;

				}
				else if (ptr != &pc[0]) {
					pc[i] = pc[i - 1] + 4;
				}
			}
			
			pcbyte = pc[i].to_int();

			address.write(pcbyte);
			pcjal.write((pc[i]).to_int() + 4);
				
			ptr++;
			i++;
		}


	}

};