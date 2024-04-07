#include <systemc.h>


SC_MODULE(control) {
	sc_in<sc_int<32>> instruction;
	sc_out<sc_uint<2>> opasel;
	sc_out<sc_uint<12>>csr_offset;
	sc_out<sc_uint<2>>dmem_sel;
	sc_out<sc_uint<3>> func3;
	sc_out<bool>  regwrite,csr_sig,trig;
	sc_out<sc_uint<1>> branchsel,jump,memwritesig, operandbsel,wrt,muxwrt,readsig,mux3sel,ill_ins;
	sc_out<sc_uint<5>> oprs1, oprs2, oprd;
	sc_out < sc_uint<4>>alufunc;
	sc_out <sc_int<32>>immediate32;
	bool itypesig, rtypesig, stypesig,extdbit,loadsig,utypesig,utypesigaui,branch,jal,jalr,csr,trigger;
	
	sc_uint<4> alufunc1;
	

	sc_int<32>immediate;
	sc_uint<4> mask;
	

	SC_CTOR(control) {
		jalr = 0;
		jal = 0;
		branch = 0;
		utypesigaui = 0;
		utypesig = 0;
		itypesig = 0;
		rtypesig = 0;
		stypesig = 0;
		extdbit = 0;
		loadsig = 0;
		csr = 0;
		
		SC_METHOD(dec);
		sensitive << instruction;
		

	}
	void dec() {	
		//================type decode========================================
			if (instruction.read().range(6, 0) == 0b0110011) {
				
				rtypesig=true;
			}
			else {	
				rtypesig=false;
			}
			if (instruction.read().range(6, 0) == 0b0010011) {
				
				itypesig=true;
				
			}
			else {
				itypesig=false;
			}
			if (instruction.read().range(6, 0) == 0b0100011) {
				
				stypesig=true;
			}
			else {
				stypesig=false;
			}
			if (instruction.read().range(6, 0) == 0b0000011) {
				
				loadsig =true;
			}
			else {
				loadsig = false;
			}
			if (instruction.read().range(6, 0) == 0b0110111) {
				utypesig= true;
			}
			else {
				utypesig = false;
			}
			if (instruction.read().range(6, 0) == 0b0010111) {
				utypesigaui = true;
				
			}
			else {
				utypesigaui = false;
				
			}
			if (instruction.read().range(6, 0) == 0b1100011) {
				branch = true;
				
				

			}
			else {
				branch = false;
				

			}
			if (instruction.read().range(6, 0) == 0b1101111) {
				jal = true;
			}
			else {
				jal = false;	
			}
			if (instruction.read().range(6, 0) == 0b1100111) {
				jalr = true;
			}
			else {
				jalr = false;
			}
			if (instruction.read().range(6, 0) == 0b1110011) {
				csr = true;
			}
			else {
				csr = false;
			}
			if (rtypesig==false && itypesig==false && stypesig==false && loadsig==false && utypesig==false && utypesigaui==false && branch==false && jal==false && jalr==false && csr==false) {
				ill_ins.write(0b1);
			}
			else {
				ill_ins.write(0b0);
			}
			
			trig.write(!trig.read());
		
			
			//============================================ control signals======================
			if (itypesig == true || rtypesig == true||loadsig==true||branch==true||jalr==true||csr==true||branch==false||jal==false||jalr==false) {
				oprs1.write(instruction.read().range(19, 15).to_uint());	
				
			}
			

			if (itypesig == true || rtypesig == true || loadsig == true || utypesig == true||utypesigaui==true||jal==true||jalr==true||csr==true) {
				oprd.write(instruction.read().range(11, 7).to_uint());
				regwrite.write(true);	
				
			}
			else {
				regwrite.write(false);
			}
			

			if (itypesig == true || stypesig == true || loadsig == true || utypesig == true || utypesigaui == true || branch == true || jal == true||jalr==true) {

				operandbsel = 0b1;
				extdbit = true;
					
			}
			else {
				
				operandbsel = 0b0;
				extdbit = false;
			}
			
			if (rtypesig == true || stypesig == true||branch==true) {
				oprs2.write(instruction.read().range(24, 20).to_uint());
			}
			else {
				oprs2.write(false);
			}
			
			if (itypesig == true) {
				alufunc1.range(2, 0) = instruction.read().range(14, 12);
				alufunc1(3, 3) = 0;
				alufunc.write(alufunc1);
				opasel.write(0b00);
				wrt.write(0b0);
				muxwrt.write(0b1);
				
				
				
			}
			
			
			if (stypesig == true) {
				memwritesig.write(0b1);

				alufunc.write(0);
				oprs1.write(instruction.read().range(19, 15).to_uint());
				opasel.write(0b0000);
				if (instruction.read().range(14, 12) == 0b000) { // sb
					dmem_sel.write(0b01);
				}
				else if (instruction.read().range(14, 12) == 0b001) { //sh
					dmem_sel.write(0b10);
				}
				else if (instruction.read().range(14, 12) == 0b010) { //sw
					dmem_sel.write(0b11); 
				} 

				
			}
			else {
				memwritesig.write(0b0);
			}
			if (rtypesig == true) {

				alufunc1.range(2, 0) = instruction.read().range(14, 12);
				alufunc1(3, 3) = instruction.read().range(30, 30);
				alufunc.write(alufunc1);
				opasel.write(0b00);
				wrt.write(0b0);
				muxwrt.write(0b1);
				


			}
			
		
				
			
			if (loadsig == true) {
				
				alufunc.write(0);
				opasel.write(0b00);
				muxwrt.write(0b0);
				readsig.write(0b1);
				
				if (instruction.read().range(14, 12) == 0b000) { // lb
					dmem_sel.write(0b01);
				}
				else if (instruction.read().range(14, 12) == 0b001) { //lh
					dmem_sel.write(0b10);
				}
				else if (instruction.read().range(14, 12) == 0b010) { //lw
					dmem_sel.write(0b11);
				}
				
				
				
			}
			else {
				readsig.write(0b0);
				
			}
			
			if (utypesig == true) {
				alufunc.write(0b1111);
				opasel.write(0b01);
				wrt.write(0b0);
				muxwrt.write(0b1);
				
			}
			
			
			
			if (utypesigaui == true||branch==true) {
				alufunc.write(0b0000);
				opasel.write(0b01);
				
			}
			if (branch == true||csr==true) {
				
				func3.write(instruction.read().range(14, 12).to_uint());				
				
			}
			else {
				func3.write(0);
			}
			if (jal == true) {

				muxwrt.write(0b1);
				opasel.write(0b01);
				alufunc.write(0b0000);
				
				if (instruction.read().range(11, 7) == 0) {
					oprd.write(0b00001);
				}
				else if(instruction.read().range(11, 7) !=0){
					oprd.write(instruction.read().range(11, 7).to_uint());
				}
				
			}
			if (jalr == true) {
				muxwrt.write(0b1);
				alufunc.write(0b0000);
				opasel.write(0b00);
			}
			if (branch == true) {
				branchsel.write(0b1);
				
			}
			else {
				branchsel.write(0b0);
				
			}

			 if (jal == true||jalr==true) {
				jump.write(0b1);
				
				
			 }
			else {
				 jump.write(0b0);
				
				
			}
			//================================
			 if (jal == true||jalr==true) {
				 wrt.write(0b1);
			 }
			 else {
				 wrt.write(0b0);
			 }
			 if (csr == true) {
				 csr_sig.write(true);
				 csr_offset.write(instruction.read().range(31, 20).to_uint());
				 
				 mux3sel.write(0b1);
				 if (instruction.read().range(11, 7) != 0) {  //checking rd
					 regwrite.write(true);
				 }
				 else {
					 regwrite.write(false);
				 }

			 }
			 else {
				 mux3sel.write(0b0);
				 csr_sig.write(false);
				 
			
			 }
			
		
			
			
//=======================================immediate generation=============================
			if (extdbit == true ) {
				if (itypesig == true||jalr==true||loadsig==true) {
					immediate = instruction.read().range(31, 20);
					if (instruction.read().range(31, 31) == 1) {
						immediate.range(31, 12) = ~0;
						
					}
					immediate32.write(immediate);
					
				}
				
				else if (stypesig == true) {
					immediate.range(4, 0) = instruction.read().range(11, 7);
					immediate.range(11, 5) = instruction.read().range(31, 25);
					if (instruction.read().range(31, 31) == 1) {
						immediate.range(31, 12) = ~0;
						
					}
					immediate32.write(immediate);
					
				}
				else if (utypesig== true||utypesigaui==true) {
					immediate(31, 12) = instruction.read().range(31, 12);
					immediate(11, 0) = 0;
					immediate32.write(immediate);
					
				}
				else if (branch == true) {
					immediate(0, 0) = 0;
				    immediate(11, 11) = instruction.read().range(7,7);
					immediate(4, 1) = instruction.read().range(11, 8);
					immediate(10, 5) = instruction.read().range(30, 25);
					immediate(12, 12) = instruction.read().range(31, 31);
					if (instruction.read().range(31, 31) == 1) {
						immediate.range(31, 13) = ~0;

					}
					
					immediate32.write(immediate);

				}
				else if (jal == true) {
					immediate(0, 0) = 0;
					immediate(10, 1) = instruction.read().range(30, 21);
					immediate(11, 11) = instruction.read().range(20, 20);
					immediate(19, 12) = instruction.read().range(19, 12);
					immediate(20, 20) = instruction.read().range(31, 31);
					if (instruction.read().range(31, 31) == 1) {
						immediate.range(31, 21) = ~0;

					}

					immediate32.write(immediate);

				}
				
				
			}
			
	}
};







