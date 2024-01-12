#include <systemc.h>

#include "pc.cpp"
#include "imem.cpp"
#include"control.cpp"
#include "regfile.cpp"
#include "mux.cpp"
#include "alu.cpp"
#include "dmem.cpp"
#include "mux2bit.cpp"
#include "branch.cpp"
#include "csr.cpp"


SC_MODULE(rv_thunder) {
	pc pc_inst;
	imem fetch_inst;
	control decode_inst;
	regfile reg_inst;
	mux mux_inst,mux_inst1, mux_inst2,mux_inst3;
	alu alu_inst;
	dmem data_mem_inst;
	CSR csr_inst;
	
	mux2bit mux2bit_inst;
	branch branch_inst;


	sc_signal <sc_int<32>>pcbranch32, jalpc;
	sc_signal<sc_uint<2>> op_a_sel,dmem_mask;
	sc_signal<sc_int<32>>addr, in3, in4, op1;
	sc_signal<sc_int<32>> instr_dat,mux3in;
	sc_signal<bool> itypesignal, rtypesignal, stypesignal;
	sc_signal<bool>we, extd_bitsig, auipc, nextpcsel;
	sc_signal<sc_int<32>> imm;
	sc_signal<sc_uint<5>> rs1, rs2, rd;
	sc_signal<sc_uint<4>>aluop;
	sc_signal<sc_uint<3>>func_3;
	sc_signal<sc_uint<12>>csr_val;
	sc_in_clk clk;

	sc_signal<sc_int<32>> rf_out1, rf_out2, wb_data, aluout,write,csr_reg;
	sc_signal < sc_int<32>>op2;
	sc_signal<sc_int<32>> dmem_dout;
	sc_signal<bool> pcwrite,csr_en;
	sc_signal<sc_uint<1>>  branchsel,wem, operandbselsig,wrt,muxwrtsig,memreadsig,mux3sel;
	sc_signal<sc_uint<1>> branchsig,pc_up;
	sc_signal <sc_uint<1>> AND;

	sc_signal<sc_int<32>> branchopa, branchopb, jump,test;
	sc_int<32> JAL;


	SC_CTOR(rv_thunder) :pc_inst("pc_inst"), fetch_inst("fetch_inst"), decode_inst("DecodeRinstance"), reg_inst("reginst"), mux_inst("mux_inst"), alu_inst("alu_inst"), data_mem_inst("data_mem_inst"), mux_inst1("mux_inst1"), mux2bit_inst("mux2bit_inst"), branch_inst("branch_inst"), mux_inst2("mux_inst2"),csr_inst("csr_inst"),mux_inst3("mux_inst3") {

		
		pc_inst.clk(clk);
		pc_inst.address(addr);
		pc_inst.branchsel(branchsel);
		pc_inst.branchsig(branchsig);
		pc_inst.pcjal(jump);
		pc_inst.pc_branch(aluout);
		pc_inst.jump(pc_up);

		fetch_inst.addresspc(addr);
		fetch_inst.clk(clk);
		fetch_inst.instruction(instr_dat);

		
		
		decode_inst.instruction(instr_dat); //transfering fetched inst to decode
		decode_inst.regwrite(we); //write data sig in control decode
		decode_inst.operandbsel(operandbselsig);	//operandb sig in control decode
		
		decode_inst.memwritesig(wem);
		decode_inst.immediate32(imm);
		decode_inst.oprs1(rs1);
		decode_inst.oprs2(rs2);
		decode_inst.oprd(rd);
		decode_inst.alufunc(aluop);
		decode_inst.opasel(op_a_sel);
		decode_inst.branchsel(branchsig);
		decode_inst.func3(func_3);
		decode_inst.wrt(wrt);
		decode_inst.jump(pc_up);
		decode_inst.dmem_sel(dmem_mask);
		decode_inst.muxwrt(muxwrtsig);
		decode_inst.readsig(memreadsig);
		decode_inst.csr_sig(csr_en);
		decode_inst.csr_offset(csr_val);
		decode_inst.mux3sel(mux3sel);
		
		


		reg_inst.oprs1(rs1);
		reg_inst.oprs2(rs2);
		reg_inst.oprd(rd);
		reg_inst.readData1(rf_out1);
		reg_inst.readData2(rf_out2);
		reg_inst.writeData(wb_data);
		reg_inst.regwrite(we);
		reg_inst.clk(clk);


		mux2bit_inst.in1(rf_out1);  //opa sel
		mux2bit_inst.in2(addr);
		mux2bit_inst.in3(in3);
		mux2bit_inst.in4(in4);
		mux2bit_inst.out(op1);
		mux2bit_inst.insel(op_a_sel);


		
		mux_inst.i1(rf_out2); //opbsel
		mux_inst.i2(imm);
		mux_inst.selsig(operandbselsig);
		mux_inst.muxout(op2);

		alu_inst.aluop(aluop);
		alu_inst.aluop1(op1);
		alu_inst.aluop2(op2);
		alu_inst.alu_out(aluout);
		

		data_mem_inst.index(aluout);
		data_mem_inst.clk(clk);
		data_mem_inst.rs2in(rf_out2);
		data_mem_inst.dataout(dmem_dout);
		data_mem_inst.memwrite(wem);
		data_mem_inst.mask(dmem_mask);
		data_mem_inst.memread(memreadsig);
		

		mux_inst1.i1(dmem_dout); //writeback sel
		mux_inst1.i2(aluout);
		mux_inst1.selsig(muxwrtsig);
		mux_inst1.muxout(write);

		branch_inst.OPA(rf_out1);
		branch_inst.OPB(rf_out2);
		branch_inst.func3(func_3);
		branch_inst.branch_out(branchsel);

		mux_inst2.i1(write);
		mux_inst2.i2(jump);
		mux_inst2.selsig(wrt);
		mux_inst2.muxout(mux3in);

		csr_inst.csr_sig(csr_en);
		csr_inst.func3(func_3);
		csr_inst.rd_in(rd);
		csr_inst.rs1_data(rf_out1);
		csr_inst.csr_val(csr_val);
		csr_inst.csr_reg(csr_reg);
		csr_inst.rs1_in(rs1);
		

		mux_inst3.i1(mux3in);
		mux_inst3.i2(csr_reg);
		mux_inst3.selsig(mux3sel);
		mux_inst3.muxout(wb_data);

	}

	
};

int sc_main(int argc, char* argv[]) {
	sc_set_time_resolution(1, SC_SEC);
	sc_clock clk("clk", 2, SC_SEC);

	rv_thunder TOP("TOP");
	TOP.clk(clk);

	sc_trace_file* tf = sc_create_vcd_trace_file("decode");
	sc_trace(tf, TOP.fetch_inst.clk, "clk");
	sc_trace(tf, TOP.pc_inst.address, "pcvalue");
	sc_trace(tf, TOP.pc_inst.pc_branch, "branchval_pc");
	sc_trace(tf, TOP.pc_inst.pcbyte, "pcval");

	sc_trace(tf, TOP.pc_inst.branchsel, "branchsel");
	sc_trace(tf, TOP.pc_inst.branchsig, "branchsig");

	sc_trace(tf, TOP.decode_inst.instruction, "instruction");
	sc_trace(tf, TOP.decode_inst.itypesig, "itypesignal");
	sc_trace(tf, TOP.decode_inst.rtypesig, "rtypesignal");
	sc_trace(tf, TOP.decode_inst.stypesig, "stypesignal");
	sc_trace(tf, TOP.decode_inst.operandbsel, "operandbselsig");
	sc_trace(tf, TOP.decode_inst.utypesig, "utypesignal");
	sc_trace(tf, TOP.decode_inst.regwrite, "wb_datatoregsig");
	sc_trace(tf, TOP.decode_inst.memwritesig, "memwrite");
	sc_trace(tf, TOP.decode_inst.opasel, "opasig");
	sc_trace(tf, TOP.decode_inst.branchsel, "branchseldec");

	sc_trace(tf, TOP.decode_inst.immediate32, "immfromimdgen");
	sc_trace(tf, TOP.decode_inst.loadsig, "loadsig");
	sc_trace(tf, TOP.decode_inst.alufunc, "alufunc");
	sc_trace(tf, TOP.reg_inst.oprs1, "oprs1");
	sc_trace(tf, TOP.reg_inst.oprs2, "oprs2");
	sc_trace(tf, TOP.reg_inst.oprd, "oprd");
	sc_trace(tf, TOP.mux_inst.muxout, "op2");
    sc_trace(tf, TOP.mux_inst.i1, "input1");
	sc_trace(tf, TOP.mux_inst.i2, "input2");
	sc_trace(tf, TOP.reg_inst.readData2, "redport2reg");
	sc_trace(tf, TOP.reg_inst.readData1, "readreg1");
	sc_trace(tf, TOP.alu_inst.aluop1, "aluinput1");
	sc_trace(tf, TOP.alu_inst.aluop2, "aluinput2");
	sc_trace(tf, TOP.alu_inst.alu_out, "aluoutput");
	sc_trace(tf, TOP.reg_inst.writeData, "datainreg");
	sc_trace(tf, TOP.reg_inst.regFile, "registerfile");
	sc_trace(tf, TOP.reg_inst.regwrite, "wrt_en");


	sc_trace(tf, TOP.data_mem_inst.rs2in, "datamem_rs2");
	sc_trace(tf, TOP.data_mem_inst.index, "datamem_index");
	sc_trace(tf, TOP.data_mem_inst.datamem, "datamemory");
    sc_trace(tf, TOP.data_mem_inst.dataout, "datamem_out");
	sc_trace(tf, TOP.data_mem_inst.memwrite, "memwritesig");
	sc_trace(tf, TOP.data_mem_inst.mask, "memmask");

	sc_trace(tf, TOP.mux_inst1.i1, " writebackmuxi1");
	sc_trace(tf, TOP.mux_inst1.i2, " writebackmuxi2");
	sc_trace(tf, TOP.mux_inst1.muxout, " writebackmux_out");
	


	sc_trace(tf, TOP.mux2bit_inst.in1, "2bitmuxin1");
	sc_trace(tf, TOP.mux2bit_inst.in2, "2bitmuxin2");
	sc_trace(tf, TOP.mux2bit_inst.in3, "2bitmuxin3");
	sc_trace(tf, TOP.mux2bit_inst.in4, "2bitmuxin4");
	sc_trace(tf, TOP.mux2bit_inst.insel, "2bitmuxinsel");
	sc_trace(tf, TOP.mux2bit_inst.out, "2bitop2");

	sc_trace(tf, TOP.branch_inst.OPA, "branchOPA");
	sc_trace(tf, TOP.branch_inst.OPB, "branchOPB");
	sc_trace(tf, TOP.branch_inst.func3, "branchfunc3");

	sc_trace(tf, TOP.branch_inst.branch_out, "branchout");
	sc_trace(tf, TOP.mux_inst2.i1, " mux2_in1");
	sc_trace(tf, TOP.mux_inst2.i2, " mux2_in2");
	sc_trace(tf, TOP.mux_inst2.muxout, " mux2_out");

	sc_trace(tf, TOP.mux_inst3.i1, " mux3_in1");
	sc_trace(tf, TOP.mux_inst3.i2, " mux3_in2");
	sc_trace(tf, TOP.mux_inst3.muxout, " mux3_out");
	sc_trace(tf, TOP.mux_inst3.selsig, " mux3_selsig");

	sc_trace(tf, TOP.csr_inst.csr_value, " csr_value");
	sc_trace(tf, TOP.csr_inst.csr_val, " csr_val");
	sc_trace(tf, TOP.csr_inst.csr_reg, " csr_reg");
	sc_trace(tf, TOP.csr_inst.rd_in, " csr_rd");
	sc_trace(tf, TOP.csr_inst.func3, " csr_func3");
	
	

	sc_start(150, SC_SEC);



	sc_close_vcd_trace_file(tf);
	
	for (int i = 0; i < 32; i++) {
		cout << hex << "Register " << i << ": " << TOP.reg_inst.regFile[i] << endl;
    }

		for (int i = 0; i < 8000; i++) {
			cout << "memory " << i << ": " << TOP.data_mem_inst.datamem[i] << endl;
		} 


	return 0;
}