CLANG_VERSION = 11

#MUSL_INSTALL_PATH = ../musl_build/install
#COMPILER_RT_PATH  = ../compiler-rt_build/install/lib/riscv64/libclang_rt.builtins-riscv64.a

CFLAGS  = -target riscv64 -march=rv64i
CFLAGS += -I$(MUSL_INSTALL_PATH)/include
#  -Wall -Werror -O2 -g -nostdlib
all: syscat
	
syscat: syscat.o
	ld.lld-$(CLANG_VERSION) -o syscat \
		$(MUSL_INSTALL_PATH)/lib/crt1.o \
		$(MUSL_INSTALL_PATH)/lib/libc.a \
		$(COMPILER_RT_PATH) \
		*.o

syscat.o: syscat.c
	clang-$(CLANG_VERSION) $(CFLAGS) -c syscat.c

clean:
	rm -f syscat *.o

