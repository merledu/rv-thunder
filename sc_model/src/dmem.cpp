#include<systemc.h>

SC_MODULE(dmem) {
	sc_in<sc_int<32>> rs2in;
	sc_in<sc_int<32>> index;
	sc_in_clk clk;
	sc_out<sc_int<32>> dataout;
	sc_in<bool> memwrite;
	

	sc_int<32>* datamem;
	int memsize = 8192;
	sc_int<32> Ind;
	

	SC_CTOR(dmem) {
		datamem = new sc_int<32>[memsize];

		SC_THREAD(writemem);
		sensitive << clk.pos();
		SC_METHOD(readmem);
		sensitive << index;
	}
	void writemem() {
		while (true) {
			wait(clk.posedge_event());
			if (memwrite == true) {
				Ind = index.read();
				datamem[Ind.range(15, 2)] = rs2in.read();
			}
		}
		
		
	}
	void readmem() {

		if (memwrite == false) {
			dataout.write(datamem[index.read().range(15, 2)]);
		}
	}

};