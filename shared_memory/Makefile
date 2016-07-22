# this must use GNU Make ("make" on Linux)

# compiler options -- C99 with warnings
OPT_GCC = -std=c99 -Wall -Wextra

OPT = -D_XOPEN_SOURCE=700
LIB = -lrt

all: cons prod

cons: posix_c.c
	gcc $(OPT_GCC) $(OPT) -o cons posix_c.c $(LIB)

prod: posix_p.c
	gcc $(OPT_GCC) $(OPT) -o prod posix_p.c $(LIB)

run: cons prod
	./prod
	./cons

clean:
	rm -f cons prod

