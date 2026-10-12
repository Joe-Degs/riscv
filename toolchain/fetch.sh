#!/usr/bin/env bash
set -euo pipefail

MUSL_VER=1.2.6
LLVM_VER=20.1.8
LLVM_URL=https://github.com/llvm/llvm-project/releases/download/llvmorg-$LLVM_VER

mkdir -p "$(dirname "$0")/src"
cd "$(dirname "$0")/src"

curl -LO https://musl.libc.org/releases/musl-$MUSL_VER.tar.gz
curl -LO $LLVM_URL/compiler-rt-$LLVM_VER.src.tar.xz
curl -LO $LLVM_URL/cmake-$LLVM_VER.src.tar.xz

tar xf musl-$MUSL_VER.tar.gz
tar xf compiler-rt-$LLVM_VER.src.tar.xz
tar xf cmake-$LLVM_VER.src.tar.xz
mv cmake-$LLVM_VER.src cmake
