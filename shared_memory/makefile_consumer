# this must use GNU Make ("make" on Linux)

CC = gcc
FC = ifort

# compiler options
OPT_GCC = -std=c99 -Wall -Wextra

OPT = -D_XOPEN_SOURCE=700
LIB = -lrt

all: cons

# Producer	 part of make
prod: c_producer.o f_producer.o
	$(FC) -o cons c_producer.o f_producer.o $(LIB)

c_producer.o: c_producer.c
	$(CC) $(OPT_GCC) $(OPT) -c c_producer.c $(LIB)

f_producer.o: f_producer.f90
	$(FC) -c f_producer.f90

run: cons prod
	./prod
	./cons

clean:
	rm -f cons prod
	rm -f *.o

