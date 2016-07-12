FC=ifort
FLAGS= -xHost -qopenmp -free -nowarn
LIBS=libf77zmq.a -lzmq

EXE=hwserver hwclient

.PHONY: default

default: $(EXE)

%: %.f f77_zmq.h libf77zmq.a
	$(FC) $(FLAGS) $*.f -o $@ $(LIBS)

clean:
	$(RM) -f -- $(EXE) *.ipc
