ZIG_LIB  := $(shell zig env | sed -n 's/.*\.lib_dir = "\(.*\)",/\1/p')
LIB      := $(CURDIR)/lib
STAMP    := $(LIB)/.patched
PATCHES  := patches/zig-soft.diff patches/musl-atomics.diff

all: $(STAMP)

$(STAMP): $(PATCHES)
	rm -rf $(LIB)
	cp -r $(ZIG_LIB) $(LIB)
	git apply -p1 --directory=lib patches/zig-soft.diff
	git apply -p0 --directory=lib/libc/musl patches/musl-atomics.diff
	touch $@

clean:
	rm -rf $(LIB)

.PHONY: all clean
