# Use gcc for C and gfortran for Fortran code.
CC=gcc
FC=gfortran

hello : hello_prb.o hello.o
	$(FC) -o hello hello_prb.o hello.o

hello.o : hello.c
	$(CC) -Wall -c hello.c

hello_prb.o: hello_prb.f90
	$(FC) -c hello_prb.f90

