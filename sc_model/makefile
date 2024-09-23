# Makefile for 32-bit RISC-V Simulator

# Compiler
CXX = g++

# Directories
INCDIR = /usr/local/systemc-2.3.3/include
LIBDIR = /usr/local/systemc-2.3.3/lib-linux64

# Compiler Flags
CXXFLAGS = -I. -I$(INCDIR)

# Linker Flags
LDFLAGS = -L. -L$(LIBDIR) -Wl,-rpath=$(LIBDIR)

# Libraries
LIBS = -lsystemc -lm

# Source Files
SRCS = rv-thunder.cpp 

# Output Executable
TARGET = out

# Build the project
all: $(TARGET)

# Rule to link the object files and create the executable
$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET) $(LDFLAGS) $(LIBS)

# Clean up the build
clean:
	rm -f $(TARGET)

# Phony targets
.PHONY: all clean
