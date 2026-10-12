LIB    := ../lib
CPU    ?= generic_rv64
TARGET := -target riscv64-linux-musl -mcpu=$(CPU)

all: run

run: hello
	qemu-riscv64 ./hello

hello: hello.zig $(LIB)/.patched
	zig build-exe hello.zig --zig-lib-dir $(LIB) $(TARGET)

$(LIB)/.patched:
	$(MAKE) -C ..

dump: hello
	llvm-objdump -d --no-show-raw-insn --disassemble-symbols=hello.main hello

dump-all: hello
	llvm-objdump -d --no-show-raw-insn hello | less

clean:
	rm -f hello hello.o

.PHONY: all run dump dump-all clean
