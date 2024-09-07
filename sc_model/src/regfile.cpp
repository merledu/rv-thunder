#include<systemc.h>
SC_MODULE(regfile) {
    sc_in_clk clk;
   
    sc_in<bool> regwrite,trigger;
    sc_in<sc_uint<5>>oprs1;
    sc_in<sc_uint<5>>oprs2;
    sc_in<sc_uint<5>> oprd;
    sc_in<sc_int<32>> writeData;
    sc_out<sc_int<32>> readData1;
    sc_out<sc_int<32>> readData2;

    sc_int<32> writedatainreg;
   

    sc_int<32> regFile[32];

    SC_CTOR(regfile) {
        SC_METHOD(register_update);
        sensitive <<regwrite<<oprd<<writeData;

        SC_METHOD(read_ports);
        sensitive << oprs1<<oprs2 << trigger;
       
    

    }
    void read_ports() {
            if (oprs1.read() >= 0 && oprs1.read() <= 31) {
                readData1.write(regFile[oprs1.read()]);

            }
            if (oprs2.read() >= 0 && oprs2.read() <= 31) {
                readData2.write(regFile[oprs2.read()]);
            }
            
        
        
    }

   
    void register_update() {
      
            if (regwrite == true) {
                writedatainreg = regFile[oprd.read()];

                if (oprd.read() >= 0 && oprd.read() <= 31) {
                    
                    regFile[oprd.read()] = writeData.read();
                    regFile[0] = 0;

                }
                
            }
       
    }

  

   
};
