CC=gcc
CCFLAGS=-Wall -Wextra
DEPS = matrix.h

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $<

multiply: multiply.o matrix.o
	$(CC) $(CCFLAGS) -o multiply multiply.o matrix.o
