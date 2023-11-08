#include<systemc.h>
SC_MODULE(Mux) {

    sc_in<bool> selsig;
    sc_in<sc_int<32>> i1, i2;
    sc_out<sc_int<32>> muxout;
    sc_int<32> in2;
      

    SC_CTOR(Mux) {
        SC_METHOD(mux);
        sensitive << selsig<<i1<<i2;
    }

    void mux() { 
            
            if (selsig.read()==0) {
                muxout.write(i1.read());
               
                
            }
            else {
                in2 = i2.read();
                muxout.write(i2.read());
            
              
            }
    }
};