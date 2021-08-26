# Intro
*Warning, this project is done by an absolute beginner to assembly and riscv in general.
The things in this directory will be learning projects. Use at your own discretion
I saw [gamozolab](https://github.com/gamozolabs) use this one of his streams and that is
how i got started learning about riscv*

This projects simplifies building binaries for `rv64i` from single source C projects or
risc-v assembly projects.

# Usage
Everything here assumes you have everything from the parent directory working and want
to do more with riscv. You must have the following things in your `environment` for things
to work.
```
RISCV_PATH="/home/joe/dev/riscv"
export CLANG_VERSION=11
export MUSL_INSTALL_PATH=$RISCV_PATH/musl_build/install
export COMPILER_RT_PATH=$RISCV_PATH/compiler-rt_build/install/lib/riscv64/libclang_rt.builtins-riscv64.a
```

I wrote a simple script to generate Makefiles for single source projects and it sort of 
works(atleast on my machine). The script is `build.py` in the this directory.
For help using the package

    $ ./build.py --help

It uses a file `Makefile.template` to generate Makefile for the single source binaries.

## Test Applications
There is a C source file `test_c/test_c.c` and a riscv assembly source file `test_asm/hello_world.s` in this directory. this is how to generate Makefiles for them using `gamozolab`'s Makefile as the template

```
joe@debian:~/dev/riscv/projects/test_asm || ../build.py -d . -s hello_world.s --build
clang-11 -g -target riscv64 -march=rv64i -I/home/joe/dev/riscv/musl_build/install/include -c hello_world.s
ld.lld-11 -o hello_world \
        /home/joe/dev/riscv/musl_build/install/lib/crt1.o \
        /home/joe/dev/riscv/musl_build/install/lib/libc.a \
        /home/joe/dev/riscv/compiler-rt_build/install/lib/riscv64/libclang_rt.builtins-riscv64.a \
        *.o
joe@debian:~/dev/riscv/projects/test_asm || qemu-riscv64 hello_world
Hello Mothersuckers!
```
Sick right!?

Compiling source files with same name as their parent directory is way simpler.

```
joe@debian:~/dev/riscv/projects/test_c || ../build.py -d . --build
clang-11 -g -target riscv64 -march=rv64i -I/home/joe/dev/riscv/musl_build/install/include -c test_c.c
ld.lld-11 -o test_c \
        /home/joe/dev/riscv/musl_build/install/lib/crt1.o \
        /home/joe/dev/riscv/musl_build/install/lib/libc.a \
        /home/joe/dev/riscv/compiler-rt_build/install/lib/riscv64/libclang_rt.builtins-riscv64.a \
        *.o
joe@debian:~/dev/riscv/projects/test_c || qemu-riscv64 test_c
Hello Mothersuckers!
joe@debian:~/dev/riscv/projects/test_c ||
```
Maaadddd!

# Resources
- This whole thing is built on top of this [repository](https://github.com/gamozolabs/riscv) by gamozolabs
- If you want to learn more about this kinda of stuff watch him hack live on [youtube](https://www.youtube.com/user/gamozolabs)
- This [pdf](https://shakti.org.in/docs/risc-v-asm-manual.pdf) I found on the internet is a good introduction to systems programming with risc-v
