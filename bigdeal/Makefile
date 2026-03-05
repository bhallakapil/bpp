#
# Makefile for the shuffle program Big Deal
#
# Change OS to either unix or dos or mingw
OS=unix

CC=gcc
PFLAGS=
#CFLAGS=-O $(PFLAGS) -Wall -pedantic -I/mingw/include
CFLAGS=-O $(PFLAGS) -Wall -pedantic -fPIC
LDFLAGS=$(PFLAGS)

COMMONOBJS=rmd160.o mp.o binomial.o
LIBOBJS=$(COMMONOBJS) collect.o output.o bigdeal_lib.o $(OS).o

all:	libbigdeal.a libbigdeal.dylib

libbigdeal.a:	$(LIBOBJS)
	ar rcs libbigdeal.a $(LIBOBJS)

libbigdeal.dylib: $(LIBOBJS)
	$(CC) -dynamiclib -o libbigdeal.dylib $(LIBOBJS)

clean:
	-rm $(LIBOBJS) libbigdeal.a libbigdeal.dylib

output.o: output.c types.h bigdeal.h binomial.h
binomial.o: binomial.c types.h bigdeal.h mp.h
collect.o: collect.c types.h rmd160.h bigdeal.h
bigdeal_lib.o: bigdeal_lib.c types.h rmd160.h bigdeal.h mp.h binomial.h output.h os.h collect.h
dos.o: dos.c types.h bigdeal.h
mp.o: mp.c types.h bigdeal.h
rmd160.o: rmd160.c types.h rmd160.h
unix.o: unix.c types.h bigdeal.h
