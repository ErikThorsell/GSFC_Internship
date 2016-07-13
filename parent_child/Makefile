# Pick compiler.
FC=ifort
#FC=gfortran

# Pick libs
LIBS=libf77zmq.a -L/home/simon/Programming/zeromq-4.1.5/.libs/  -lzmq 

# Pick flags
FLAGS=-xHost -qopenmp -free -nowarn
#FLAGS=-g -O2 -Wall -Wno-unused -fopenmp -fno-align-commons -ffree-form

EXE=parent child

.PHONY: default

default: $(EXE)

%: %.f f77_zmq.h libf77zmq.a
	$(FC) $(FLAGS) $*.f -o $@ $(LIBS)

clean:
	$(RM) -f -- $(EXE) *.ipc
