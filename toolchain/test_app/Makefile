CLANG_VERSION = 20

S=../sysroot
MUSL_INSTALL_PATH = $(S)
COMPILER_RT_PATH  = $S/lib/libclang_rt.builtins-riscv64.a

CFLAGS  = -Wall -Werror -O2 -g -target riscv64 -march=rv64i -mabi=lp64
CFLAGS += -nostdlibinc -isystem $(MUSL_INSTALL_PATH)/include

all: run

run: test_app
	qemu-riscv64 ./test_app
	
test_app: test_app.o
	ld.lld-$(CLANG_VERSION) -o test_app \
		$(MUSL_INSTALL_PATH)/lib/crt1.o \
		$(MUSL_INSTALL_PATH)/lib/libc.a \
		$(COMPILER_RT_PATH) \
		*.o

test_app.o: test_app.c
	clang-$(CLANG_VERSION) $(CFLAGS) -c test_app.c

clean:
	rm -f test_app *.o

