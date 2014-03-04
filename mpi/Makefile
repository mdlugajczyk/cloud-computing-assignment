CC=mpicc
CCFLAGS=-Wall -Wextra
DEPS = matrix.h

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $<

generate: generate.o matrix.o
	$(CC) $(CCFLAGS) -o generate generate.o matrix.o

multiply: multiply.o matrix.o
	$(CC) $(CCFLAGS) -o multiply multiply.o matrix.o

all: multiply generate
