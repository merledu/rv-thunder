#include <systemc.h>
#include <iostream>
#include <cstring>

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
#include"or.cpp"


SC_MODULE(rvthunder) {
	sc_out<sc_int<32>> add{ "add" };
	sc_out<sc_int<32>> d_dmem_data{ "d_dmem_data" };
sc_out<sc_uint<1>> d_memwrite{ "d_memwrite" }, d_memread{ "d_memread" };
	sc_out<sc_uint<2>> doutdmem_mask{ "doutdmem_mask" };
	
	sc_in<sc_int<32>> d_dmem_out{ "d_demem_out" };



	sc_in_clk clk{ "clk" };

	

	pc pc_inst;
	imem fetch_inst;
	control decode_inst;
	regfile reg_inst;
	mux mux_inst, mux_inst1, mux_inst2, mux_inst3;
	alu alu_inst;
	//dmem data_mem_inst;
	CSR csr_inst;
	

	

	mux2bit mux2bit_inst;
	branch branch_inst;


	sc_signal <sc_int<32>>pcbranch32, jalpc;
	sc_signal<sc_uint<2>> op_a_sel, dmem_mask;
	sc_signal<sc_int<32>>addr, in3, in4, op1;
	sc_signal<sc_int<32>> instr_dat, mux3in;
	sc_signal<bool> itypesignal, rtypesignal, stypesignal;
	sc_signal<bool>we, extd_bitsig, auipc, nextpcsel;
	sc_signal<sc_int<32>> imm;
	sc_signal<sc_uint<5>> rs1, rs2, rd;
	sc_signal<sc_uint<4>>aluop,sample2;
	sc_signal<sc_uint<3>>func_3;
	sc_signal<sc_uint<12>>csr_val;
	

	sc_signal<sc_int<32>> rf_out1, rf_out2, wb_data, write, csr_out,d_dmemout,aluout,sample1,sample3,sample4;
	
	sc_signal < sc_int<32>>op2;
	sc_signal<sc_int<32>> dmem_dout, pc_out, trap_add;
	sc_signal<bool> pcwrite, csr_en, inter_sig,trig;
	sc_signal<sc_uint<1>>  branchsel, wem, operandbselsig, wrt, muxwrtsig, memreadsig, mux3sel,ill_instr;
	sc_signal<sc_uint<1>> branchsig, pc_up,inval_add,inv_add,orout,csr_pcsel,dmem_inv_Add;
	sc_signal <sc_uint<1>> AND;

	sc_signal<sc_int<32>> branchopa, branchopb, jump, test;
	


	SC_CTOR(rvthunder) :pc_inst("pc_inst"), fetch_inst("fetch_inst"), decode_inst("DecodeRinstance"), reg_inst("reginst"), mux_inst("mux_inst"), alu_inst("alu_inst"), mux_inst1("mux_inst1"), mux2bit_inst("mux2bit_inst"), branch_inst("branch_inst"), mux_inst2("mux_inst2"), csr_inst("csr_inst"), mux_inst3("mux_inst3") {

		
		SC_METHOD(operations);
		sensitive << aluout<< wem<<memreadsig<< d_dmem_out;
		//add(alu_inst.alu_out);
	//	d_dmem_data(reg_inst.readData2);
	//	d_memwrite(decode_inst.memwritesig);
	//	d_memread(decode_inst.readsig);
	//    doutdmem_mask(decode_inst.dmem_sel);
		//clk(clk);
	// d_inv_add(dmem_inv_Add);
	  //  d_dmem_out(d_dmemout);
		
		


		pc_inst.clk(clk);
		pc_inst.address(addr);
		pc_inst.branchsel(branchsel);
		pc_inst.branchsig(branchsig);
		pc_inst.pcjal(jump);
		pc_inst.pc_branch(aluout);
		pc_inst.jump(pc_up);
		pc_inst.csr_pcsel(csr_pcsel);
		pc_inst.csr_in(pc_out);
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
		decode_inst.ill_ins(ill_instr);
		decode_inst.trig(trig);



		reg_inst.oprs1(rs1);
		reg_inst.oprs2(rs2);
		reg_inst.oprd(rd);
		reg_inst.readData1(rf_out1);
		reg_inst.readData2(rf_out2);
		reg_inst.writeData(wb_data);
		reg_inst.regwrite(we);
		reg_inst.clk(clk);
		reg_inst.trigger(trig);


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
		
		


	//	data_mem_inst.index(aluout);
	//	data_mem_inst.clk(clk);
	//	data_mem_inst.rs2in(rf_out2);
	//	data_mem_inst.dataout(dmem_dout);
	//	data_mem_inst.memwrite(wem);
	//	data_mem_inst.mask(dmem_mask);
	//	data_mem_inst.memread(memreadsig);
	//	data_mem_inst.inv_add(inv_add);
	

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
		csr_inst.csr_out(csr_out);
		csr_inst.rs1_in(rs1);
		//csr_inst.interrupt(inter_sig);
		csr_inst.trap_add(trap_add);
		csr_inst.pc_out(pc_out);
		csr_inst.pc(addr);
		csr_inst.ill_instr(ill_instr);
		csr_inst.instr(addr);
		csr_inst.pc_sel(csr_pcsel);
		csr_inst.clk(clk);
		csr_inst.mis_all_ins(orout);
		

		mux_inst3.i1(mux3in);
		mux_inst3.i2(csr_out);
		mux_inst3.selsig(mux3sel);
		mux_inst3.muxout(wb_data);

		

	}
	void operations() {
		
			add.write(aluout);
			d_dmem_data.write(rf_out2);
			d_memread.write(memreadsig);
			d_memwrite.write(wem);
			doutdmem_mask.write(dmem_mask);

			dmem_dout= d_dmem_out.read();
			
	
	}


};
