#FC=ifort -O2 -xHost -openmp
#FC=gfortran -g -O2 -Wall -Wno-unused -fopenmp
FC=gfortran -g -O2 -Wno-unused -fopenmp
LIBS=libf77zmq.a -L/home/simon/Programming/zeromq-4.1.5/.libs/  -lzmq 

EXE=hwserver hwclient

.PHONY: default

default: $(EXE)

%: %.f f77_zmq.h libf77zmq.a
	$(FC) $*.f -o $@ $(LIBS) -ffree-form

#libf77zmq.a: libf77zmq.a
#	$(MAKE) -C ..
#	cp ../libf77zmq.a .

#f77_zmq.h: ../f77_zmq.h
	#cp ../f77_zmq.h .

clean:
	$(RM) -f -- $(EXE) *.ipc
