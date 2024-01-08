#include<systemc.h>

SC_MODULE(dmem) {
    sc_in<sc_uint<2>> mask;
    sc_in<sc_int<32>> rs2in;
    sc_in<sc_int<32>> index;
    sc_in_clk clk;
    sc_out<sc_int<32>> dataout;
    sc_in<sc_uint<1>> memwrite,memread;

    sc_int<32>* datamem;
    int memsize = 8192;
    sc_uint<32> Ind;

    SC_CTOR(dmem) {
        datamem = new sc_int<32>[memsize];

        SC_METHOD(operations);
        sensitive << index<<memwrite;
        
    }

    void operations() {
        
            if (memwrite.read() == 0b1 && index.read()<memsize) {
                Ind = index.read().range(15,2).to_uint();
                if (mask.read() == 0b11) {
                    datamem[Ind] = rs2in.read();
                }
                else if (mask.read() == 0b01) {
                    datamem[Ind] = rs2in.read().range(7,0);
                }
                else if (mask.read() == 0b10) {
                    datamem[Ind] = rs2in.read().range(15, 0);
                }

                
            }
             if (memread.read() == 0b1 && index.read() < memsize) {
                cout << "value of memory index :" << index.read() << endl;
                Ind = index.read().range(15, 2).to_uint();
                if (mask.read() == 0b11) {
                    dataout.write(datamem[Ind]);
                }
                else if (mask.read() == 0b01) {
                    dataout.write(datamem[Ind].range(7, 0));
                }
                else if (mask.read() == 0b10) {
                    dataout.write(datamem[Ind].range(15, 0));
                }

            }
        
    }

    
};