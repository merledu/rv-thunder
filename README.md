# RISC-V Thunder Core (Using Amaranth HDL)

 RISC-V Thunder Core is a 32 bit CPU core that currently implements the [RISC-V](1) RV32I instruction set. Its microarchitecture is described in plain Python code using [Amaranth HDL](2). There is one main file [top_level.py](rv-amaranth/src/top_level.py)

 ## Features

 * Written in user friendly language python's framework (amaranth HDL)
 * Support instruction set architecture of RISC-V 32I
 * 8KB Instruction and data memory
 * 32 general purpose registers
 * Test bench (using Amaranth HDL)

 ## Block Diagram
 * TBA
 ## Testing

 A testbench for RISC-V Thunder Core is available [here](https://github.com/merledu/rv-amaranth/tree/main/test).

 ## About Amaranth HDL

 Amaranth HDL is a hardware description language (which is previously known as nMigen) used for designing digital circuits and systems. It allows hardware engineers to specify the behavior and structure of digital designs, which can be synthesized into actual hardware using tools like [Yosys](https://github.com/YosysHQ/yosys) or translated into Verilog code. It's used for FPGA and ASIC design.
 
 ## Prerequisites

 Before working with this project, ensure you have the following prerequisites:
 * Python's library [Amaranth HDL](https://amaranth-lang.org/docs/amaranth/latest/) 
 * [iVerilog](https://github.com/steveicarus/iverilog)
 * [GTKWave](https://gtkwave.sourceforge.net/) 

 ## Amaranth HDL docs

 Install Amaranth HDL and other platforms (GTKWave, etc) using installation method and also clone git given in [Language guide](https://amaranth-lang.org/docs/amaranth/latest/)
 
  For basic understanding of Amaranth HDL use [Robert Baruch's introduction](https://github.com/RobertBaruch/nmigen-tutorial)

 ## Acknowledgements
 We want to express our gratitude to the RISC-V community for their valuable contributions to the open-source hardware ecosystem. Additionally, thanks to the Amaranth HDL developers for providing a platform for hardware design.