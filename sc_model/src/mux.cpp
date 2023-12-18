#include<systemc.h>
SC_MODULE(mux) {

    sc_in<sc_uint<1>> selsig;
    sc_in<sc_int<32>> i1, i2;
    sc_out<sc_int<32>> muxout;
    sc_int<32> in2;
      

    SC_CTOR(mux) {
        SC_METHOD(Mux);
        sensitive << selsig<<i1<<i2;
    }

    void Mux() { 
            
            if (selsig.read()==0b0) {
                muxout.write(i1.read());
               
                
            }
            else {
                in2 = i2.read();
                muxout.write(i2.read());
            
              
            }
    }
};