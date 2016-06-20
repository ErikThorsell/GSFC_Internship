# Use gcc for C and gfortran for Fortran code.
CC=gcc
FC=gfortran

calc : calcf.o fclient.o
	$(FC) -o calc calcf.o fclient.o

fclient.o : fclient.c
	$(CC) -Wall -c fclient.c

calcf.o: calcf.f90
	$(FC) -c calcf.f90

