LIB    := ../lib
CPU    ?= generic_rv64
OPTS   := -fsingle-threaded -O ReleaseSmall -fno-strip
TARGET := -target riscv64-linux-musl -mcpu=$(CPU)

bin    ?= hello

all: run

run: $(bin)
	qemu-riscv64 ./$(bin)

$(bin): $(bin).c $(LIB)/.patched
	ZIG_LIB_DIR=$(LIB) zig cc $(TARGET) -O2 $(bin).c -o $@

$(LIB)/.patched:
	$(MAKE) -C ..

dump: $(bin)
	llvm-objdump -d --no-show-raw-insn --disassemble-symbols=main $(bin)

dump-all: $(bin)
	llvm-objdump -d --no-show-raw-insn $(bin) | less

clean:
	rm -f $(bin) $(bin).o

.PHONY: all run dump dump-all clean
