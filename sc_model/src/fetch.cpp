#include<iostream>
#include <systemc.h>
#include <fstream>
#include <sstream>
#include<string>



using namespace std;


SC_MODULE(FETCH) {
    sc_in  <sc_int<32>> addresspc;
    sc_out<sc_int<32>> instruction;
    sc_int<32> readdata32_16;


    sc_in_clk clk;
    sc_int<32>* mem;

    int i, j = 0;
    int n;
    int memsize = 8192;


    SC_CTOR(FETCH) {

        mem = new sc_int<32>[memsize];

        memoryinitialize();

        SC_METHOD(checkins);
        sensitive << clk << addresspc;


    }

    void memoryinitialize() {
        cout << "enter number of instructions: " << endl;
        cin >> n;
        for (i = 0; i < n; i++) {
            cout << "enter instruction " << i + 1 << " : " << endl;
            cin >> readdata32_16;
            mem[i] = readdata32_16;
        }
    }


    void checkins() {
            instruction.write(mem[addresspc.read().range(31,2)]);
    }

    // Destructor to free memory
    ~FETCH() {
        delete[] mem; // Free the dynamically allocated memory
    }
};