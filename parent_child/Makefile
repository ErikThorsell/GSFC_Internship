# Pick compiler.
FC=ifort
#FC=gfortran

# Pick libs
LIBS=libf77zmq.a

# Pick flags
FLAGS=-xHost -qopenmp -free -lzmq -nowarn
#FLAGS=-g -O2 -Wall -Wno-unused -fopenmp -fno-align-commons -ffree-form

EXE=parent child

.PHONY: default

default: $(EXE)

%: %.f
	$(FC) $(FLAGS) $*.f -o $@ $(LIBS)

clean:
	$(RM) -f -- $(EXE) *.ipc
