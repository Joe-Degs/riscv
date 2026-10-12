CLANG    := clang-20
TRIPLE   := riscv64-unknown-elf
ARCH     := -march=rv64i -mabi=lp64

MUSL_VER := 1.2.6
LLVM_VER := 20.1.8

SRC      := $(CURDIR)/src
BUILD    := $(CURDIR)/build
SYSROOT  := $(CURDIR)/sysroot

MUSL_SRC := $(SRC)/musl-$(MUSL_VER)
MUSL_PATCHED := $(MUSL_SRC)/.patched
RT_SRC   := $(SRC)/compiler-rt-$(LLVM_VER).src

LIBC     := $(SYSROOT)/lib/libc.a
BUILTINS := $(SYSROOT)/lib/libclang_rt.builtins-riscv64.a

all: $(LIBC) $(BUILTINS)

$(MUSL_PATCHED): $(CURDIR)/patches/musl-atomics.diff
	patch -d $(MUSL_SRC) -p0 < $<
	touch $@

$(LIBC): $(MUSL_PATCHED)
	mkdir -p $(BUILD)/musl
	cd $(BUILD)/musl && \
		CC=$(CLANG) AR=llvm-ar RANLIB=llvm-ranlib \
		CFLAGS="--target=$(TRIPLE) $(ARCH)" \
		$(MUSL_SRC)/configure --target=riscv64 --disable-shared --prefix=$(SYSROOT)
	$(MAKE) -C $(BUILD)/musl
	$(MAKE) -C $(BUILD)/musl install

$(BUILTINS): $(LIBC)
	cmake -S $(RT_SRC) -B $(BUILD)/compiler-rt \
		-DLLVM_CMAKE_DIR=$(shell llvm-config-20 --cmakedir) \
		-DCMAKE_SYSTEM_NAME=Generic \
		-DCMAKE_C_COMPILER=$(CLANG) -DCMAKE_ASM_COMPILER=$(CLANG) \
		-DCMAKE_AR=$(shell command -v llvm-ar) \
		-DCMAKE_NM=$(shell command -v llvm-nm) \
		-DCMAKE_RANLIB=$(shell command -v llvm-ranlib) \
		-DCMAKE_C_COMPILER_TARGET=$(TRIPLE) -DCMAKE_ASM_COMPILER_TARGET=$(TRIPLE) \
		-DCMAKE_C_FLAGS="$(ARCH) -nostdlibinc -isystem $(SYSROOT)/include" \
		-DCMAKE_ASM_FLAGS="$(ARCH)" \
		-DCMAKE_TRY_COMPILE_TARGET_TYPE=STATIC_LIBRARY \
		-DCOMPILER_RT_BAREMETAL_BUILD=ON \
		-DCOMPILER_RT_DEFAULT_TARGET_ONLY=ON \
		-DCOMPILER_RT_BUILD_BUILTINS=ON -DCOMPILER_RT_BUILD_CRT=OFF \
		-DCOMPILER_RT_BUILD_SANITIZERS=OFF -DCOMPILER_RT_BUILD_XRAY=OFF \
		-DCOMPILER_RT_BUILD_LIBFUZZER=OFF -DCOMPILER_RT_BUILD_PROFILE=OFF \
		-DCOMPILER_RT_BUILD_MEMPROF=OFF -DCOMPILER_RT_BUILD_ORC=OFF \
		-DCOMPILER_RT_BUILD_CTX_PROFILE=OFF \
		-DCOMPILER_RT_INSTALL_LIBRARY_DIR=$(SYSROOT)/lib \
		-DCMAKE_INSTALL_PREFIX=$(SYSROOT)
	$(MAKE) -C $(BUILD)/compiler-rt builtins
	$(MAKE) -C $(BUILD)/compiler-rt install-builtins

clean:
	rm -rf $(BUILD) $(SYSROOT)

.PHONY: all clean
