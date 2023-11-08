CC = g++
CFLAGS = -I. -I/usr/local/systemc-2.3.3/include
LDFLAGS = -L. -L/usr/local/systemc-2.3.3/lib-linux64 -Wl,-rpath=/usr/local/systemc-2.3.3/lib-linux64
LIBS = -lsystemc -lm

SRC = ALU.cpp branch.cpp datamemory.cpp decodemodule.cpp fetch.cpp mux.cpp mux2bit.cpp PC.cpp registerfile.cpp Toplevel.cpp
OBJ = $(SRC:.cpp=.o)
TARGET = out

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LIBS)

%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)

