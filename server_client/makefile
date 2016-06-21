# Use gcc for C and gfortran for Fortran code.
CC=gcc
FC=gfortran

calcin : calcf.o client.o
	$(FC) -o calcin calcf.o client.o

client.o : client.c
	$(CC) -Wall -c client.c

calcf.o: calcf.f90
	$(FC) -c calcf.f90

