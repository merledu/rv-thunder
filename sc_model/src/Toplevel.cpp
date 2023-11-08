#include <systemc.h>

#include "PC.cpp"
#include "fetch.cpp"
#include"decode module.cpp"
#include "registerfile.cpp"
#include "mux.cpp"
#include "ALU.cpp"
#include "datamemory.cpp"
#include "mux2bit.cpp"
#include "branch.cpp"


SC_MODULE(TOP) {
	PC pc_inst;
	FETCH fetch_inst;
	DECODE decode_inst;
	RegisterFile reg_inst;
	Mux mux_inst;
	ALU alu_inst;
	DATA_MEMORY data_mem_inst;
	Mux mux_inst1, mux_inst2;
	mux2bit mux2bit_inst;
	BRANCH branch_inst;


	sc_signal <sc_int<32>>pcbranch32, jalpc;
	sc_signal<sc_uint<2>> op_a_sel;
	sc_signal<sc_int<32>>addr, in3, in4, op1;
	sc_signal<sc_int<32>> instr_dat;
	sc_signal<bool> itypesignal, rtypesignal, stypesignal;
	sc_signal<bool>we, operandbselsig, extd_bitsig, wem, memreadsig, auipc, nextpcsel,wrt;
	sc_signal<sc_int<32>> imm;
	sc_signal<sc_uint<5>> rs1, rs2, rd;
	sc_signal<sc_uint<4>>aluop;
	sc_signal<sc_uint<3>>func_3;
	sc_in_clk clk;

	sc_signal<sc_int<32>> rf_out1, rf_out2, wb_data, aluout,write;
	sc_signal < sc_int<32>>op2;
	sc_signal<sc_int<32>> dmem_dout;
	sc_signal<bool> pcwrite;
	sc_signal<sc_uint<1>>  branchsel;
	sc_signal<sc_uint<1>> branchsig,pc_up;
	sc_signal <sc_uint<1>> AND;

	sc_signal<sc_int<32>> branchopa, branchopb, jump,test;
	sc_int<32> JAL;


	SC_CTOR(TOP) :pc_inst("pc_inst"), fetch_inst("fetch_inst"), decode_inst("DecodeRinstance"), reg_inst("reginst"), mux_inst("mux_inst"), alu_inst("alu_inst"), data_mem_inst("data_mem_inst"), mux_inst1("mux_inst1"), mux2bit_inst("mux2bit_inst"), branch_inst("branch_inst"), mux_inst2("mux_inst2") {

		
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
		decode_inst.memread(memreadsig);
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

		alu_inst.func4(aluop);
		alu_inst.aluop1(op1);
		alu_inst.aluop2(op2);
		alu_inst.alu_out(aluout);
		

		data_mem_inst.index(aluout);
		data_mem_inst.clk(clk);
		data_mem_inst.rs2in(rf_out2);
		data_mem_inst.dataout(dmem_dout);
		data_mem_inst.memwrite(wem);
		

		mux_inst1.i1(aluout); //writeback sel
		mux_inst1.i2(dmem_dout);
		mux_inst1.selsig(memreadsig);
		mux_inst1.muxout(write);

		branch_inst.OPA(rf_out1);
		branch_inst.OPB(rf_out2);
		branch_inst.func3(func_3);
		branch_inst.branch_out(branchsel);

		mux_inst2.i1(write);
		mux_inst2.i2(jump);
		mux_inst2.selsig(wrt);
		mux_inst2.muxout(wb_data);

	}

	
};

int sc_main(int argc, char* argv[]) {
	sc_set_time_resolution(1, SC_SEC);
	sc_clock clk("clk", 2, SC_SEC);

	TOP TOP("TOP");
	TOP.clk(clk);

	


	return 0;
}