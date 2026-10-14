LIB    := ../lib
CPU    ?= generic_rv64
OPTS   := -fsingle-threaded -O ReleaseSmall -fno-strip
TARGET := -target riscv64-linux-musl -mcpu=$(CPU)

bin    ?= hello

all: run

run: $(bin)
	qemu-riscv64 ./$(bin)

$(bin): $(bin).zig $(LIB)/.patched
	zig build-exe $(bin).zig $(OPTS) --zig-lib-dir $(LIB) $(TARGET)

$(LIB)/.patched:
	$(MAKE) -C ..

dump: $(bin)
	llvm-objdump -d --no-show-raw-insn --disassemble-symbols=$(bin).main $(bin)

dump-all: $(bin)
	llvm-objdump -d --no-show-raw-insn $(bin) | less

clean:
	rm -f $(bin) $(bin).o

.PHONY: all run dump dump-all clean
