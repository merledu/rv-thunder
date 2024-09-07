#include <systemc.h>
#include <cstdio>

SC_MODULE(imem) {
    sc_in<sc_int<32>> addresspc;
    sc_out<sc_int<32>> instruction;
    sc_int<32> readdata32_16;
    
    sc_in_clk clk;
    sc_int<32>* mem;

    unsigned int memsize; // Change to unsigned int

    SC_CTOR(imem) : mem(nullptr), memsize(8192) {
        unsigned int mem_word;
        FILE* fp;
#ifdef _WIN32
        if (fopen_s(&fp, "imem.txt", "r") != 0) {
            perror("Error opening file");
        }
#else
        fp = fopen("imem.txt", "r");
        if (fp == nullptr) {
            perror("Error opening file");
        }
#endif

        int size = 0;

        mem = new sc_int<32>[memsize]; // Allocate memory

        while (fscanf_s(fp, "%x", &mem_word) != EOF) {
            mem[size] = mem_word;
            size++;
        }

        fclose(fp);

        SC_METHOD(checkins);
        sensitive << clk << addresspc;
    }

    void checkins() {
        if (mem[addresspc.read().range(15, 2)] != 0) {
            instruction.write(mem[addresspc.read().range(15, 2)]);
        }
    }

    ~imem() {
        delete[] mem;
    }
};
