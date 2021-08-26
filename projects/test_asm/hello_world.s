.globl main

.data
helloworld: .string "Hello Mothersuckers!\n"

.text

main: addi a0, zero, 1        # write to stdout
        la   a1, helloworld     # get start address of string
        addi a2, zero, 21       # len of string
        addi a7, zero, 64       # linux write syscall number
        ecall

        addi a0, zero, 0        # clean exit
        addi a7, zero, 93       # linux exit syscall number
        ecall                   # do environment call
