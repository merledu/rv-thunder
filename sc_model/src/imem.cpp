
#include<systemc.h>
#include<fstream>
SC_MODULE(imem) {
    sc_in  <sc_int<32>> addresspc;
    sc_out<sc_int<32>> instruction;
    sc_int<32> readdata32_16;


    sc_in_clk clk;
    sc_int<32>* mem;

    
    int memsize = 8192;

    

    SC_CTOR(imem) {
        mem = new sc_int<32>[memsize];
        unsigned int mem_word;
        FILE* fp;
        errno_t err = fopen_s(&fp, "imem.txt", "r");

        if (err != 0) {
            cout << "error opening file" << endl;
        }
        int size = 0;

        while (fscanf_s(fp, "%x", &mem_word) != EOF) {
            mem[size] = mem_word;
            size++;
        }

        SC_METHOD(checkins);
        sensitive << clk << addresspc;

    }
    void checkins() {
        instruction.write(mem[addresspc.read().range(15, 2)]);
    }


    ~imem() {
        delete[] mem;
    }

};