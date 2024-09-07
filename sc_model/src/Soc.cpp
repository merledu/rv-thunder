#include <systemc.h>
#include <iostream>

#include "rv-thunder.cpp"
#include "mmio.cpp"


SC_MODULE(SOC) {
	sc_in_clk clk1;
	rvthunder thunder_inst;
	dmem dmem_inst1;
	MMIO mmio_inst;

	sc_signal<sc_int<32>> dmem_index, data, dataout, dec_addout, d_wrt;
	sc_signal<sc_uint<1>> d_wem, d_memreadsig;
	sc_signal<sc_uint<2>> d_memmask;
	sc_signal<sc_uint<1>> wrt_sel{ "wrt_sel" }, dmem_en, time_en, timecmp_en;
	sc_signal<sc_int<32>> data_time{ "data_time" }, dout{ "dout" };

	sc_int<64> mtime,mtimecmp;
	sc_signal<sc_uint<64>>time;
	

	SC_CTOR(SOC) :dmem_inst1("dmem_inst1"), thunder_inst("thunder_inst"), mmio_inst("mmio_inst") {
		SC_METHOD(operations);
		sensitive << d_wem<< d_memreadsig<<dout<<data<<data_time<<timecmp_en<<time_en;

		SC_THREAD(MTIME);
		sensitive << clk1.pos();
		

		thunder_inst.add(dmem_index);
			thunder_inst.doutdmem_mask(d_memmask);
			thunder_inst.d_memwrite(d_wem);
			thunder_inst.d_memread(d_memreadsig);
			thunder_inst.d_dmem_data(data);
			
			thunder_inst.d_dmem_out(dataout);
		thunder_inst.clk(clk1);

		dmem_inst1.index(dec_addout);
		dmem_inst1.mask(d_memmask);
		dmem_inst1.memwrite(d_wem);
		dmem_inst1.memread(d_memreadsig);
		dmem_inst1.rs2in(data);
		
		dmem_inst1.dataout(dout);
		dmem_inst1.clk(clk1);
		dmem_inst1.dmem_en(dmem_en);

		mmio_inst.address(dmem_index);
		mmio_inst.rd(d_memreadsig);
		mmio_inst.wrt(d_wem);
		mmio_inst.add_out(dec_addout);
		mmio_inst.dmem_en(dmem_en);
		mmio_inst.time_en(time_en);
		mmio_inst.timecmp_en(timecmp_en);

		
	}
    void MTIME() {
		while (true) {
			wait(clk1.posedge_event());
			if(clk1.posedge()||time_en.read())
			time.write((sc_time_stamp().to_seconds() / 10));
			mtime = time.read();
		}
	} 
	void operations() {
		if (d_wem.read() == 0b1) {
			
			
			 if (timecmp_en.read()==0b1) {
				mtimecmp = data.read();
				

			 }
		}
	    if (d_memreadsig.read() == 0b1) {
			if (time_en.read()==0b1) {
				wrt_sel = 0b0;
				data_time.write(mtime);
			}
			else if (timecmp_en.read() == 0b1) {
				wrt_sel = 0b0;
				data_time.write(mtimecmp);


			}
			else if(dmem_en.read()==0b1) { 
				wrt_sel.write(0b1);
			}


			if (wrt_sel.read() == 0b0) {
				dataout.write(data_time.read());
			}
			else if (wrt_sel.read() == 0b1) {
				dataout.write(dout.read());
			}
		}
		

		
	}

	



};
int sc_main(int argc, char* argv[]) {



	sc_set_time_resolution(1, SC_SEC);
	sc_clock clk("clk", 2, SC_SEC);

	SOC TOP("TOP");
	TOP.clk1(clk);



	sc_trace_file* tf = sc_create_vcd_trace_file("SOC");
	sc_trace(tf, TOP.dmem_inst1.clk, "clk");
	sc_trace(tf, TOP.thunder_inst.add, "address");
	sc_trace(tf, TOP.thunder_inst.add, "address");
	sc_trace(tf, TOP.thunder_inst.d_dmem_out, " d_dmem_out");
	sc_trace(tf, TOP.dmem_inst1.index, "index");
	sc_trace(tf, TOP.dmem_inst1.mask, "mask");
	sc_trace(tf, TOP.dmem_inst1.memwrite, "memwrite");
	sc_trace(tf, TOP.dmem_inst1.memread, "memread");
	sc_trace(tf, TOP.dmem_inst1.rs2in, "data");
	
	sc_trace(tf, TOP.dmem_inst1.dataout, "dmem_dataout"); 
	sc_trace(tf, TOP.thunder_inst.dmem_dout, "dataincore");
	sc_trace(tf, TOP.thunder_inst.csr_inst.mcycle_reg, "mcycle");
	sc_trace(tf, TOP.thunder_inst.reg_inst.writeData, "datainreg");
	sc_trace(tf, TOP.dout, "dout");
	sc_trace(tf, TOP.wrt_sel, "wrt_Sel");
	sc_trace(tf, TOP.d_wem, "write");
	sc_trace(tf, TOP.d_memreadsig, "read");
	sc_trace(tf, TOP.dmem_en, "dmem_en");
	sc_trace(tf, TOP.time_en, "time_en");
	sc_trace(tf, TOP.timecmp_en, "timeh_en");
	sc_trace(tf, TOP.data, "data");
	sc_trace(tf, TOP.mtime, "mtime");
	sc_trace(tf, TOP.mtimecmp, "mtimecmp");
	sc_trace(tf, TOP.data_time, "data_time");
	sc_trace(tf, TOP.dataout, "dataout");
	sc_trace(tf, TOP.time, "time");
	sc_trace(tf, TOP.thunder_inst.decode_inst.instruction, "instruction");

	sc_trace(tf, TOP.thunder_inst.reg_inst.readData2, "redport2reg");
	sc_trace(tf, TOP.thunder_inst.reg_inst.readData1, "readreg1");
	sc_trace(tf, TOP.thunder_inst.alu_inst.alu_out, "aluoutput");

	sc_trace(tf, TOP.thunder_inst.pc_inst.address, "pcvalue");
	sc_trace(tf, TOP.thunder_inst.pc_inst.branchsel, "branchsel");
	sc_trace(tf, TOP.thunder_inst.pc_inst.branchsig, "branchsig");
	sc_trace(tf, TOP.thunder_inst.pc_inst.jump, "jump");
	sc_trace(tf, TOP.thunder_inst.pc_inst.csr_pcsel, "csr_pcsel");
	sc_trace(tf, TOP.thunder_inst.pc_inst.csr_in, "csr_in");

	sc_trace(tf, TOP.thunder_inst.csr_inst.ill_instr, "ill_instr");
	sc_trace(tf, TOP.thunder_inst.csr_inst.mis_all_ins, "mis_allins");
	sc_trace(tf, TOP.thunder_inst.csr_inst.csr_value, "csr_value");
	sc_trace(tf, TOP.thunder_inst.reg_inst.regwrite, "wrt_en");
	sc_trace(tf, TOP.thunder_inst.reg_inst.oprd, "oprd");
	sc_trace(tf, TOP.thunder_inst.reg_inst.readData2, "readreg2");
	sc_trace(tf, TOP.thunder_inst.reg_inst.oprs2, "oprs2");

	

	sc_start(150, SC_SEC);

	sc_close_vcd_trace_file(tf);
	for (int i = 0; i < 32; i++) {
		cout << hex << "Register " << i << ": " << TOP.thunder_inst.reg_inst.regFile[i] << endl;
	}

	for (int i = 0; i < 8000; i++) {
		cout << "memory " << i << ": " << TOP.dmem_inst1.datamem[i] << endl;
	}

	return 0;
}