# Use gcc for C and gfortran for Fortran code.
CC=gcc
FC=gfortran

calc : calcf.o client.o
	$(FC) -o calc calcf.o client.o

client.o : client.c
	$(CC) -Wall -c client.c

calcf.o: calcf.f90
	$(FC) -c calcf.f90

