#include <stdio.h>
#include <stdatomic.h>
#include <stdbool.h>

atomic_int counter = 0;
atomic_int flag = 0;

int main(void) {
    atomic_fetch_add_explicit(&counter, 5, memory_order_seq_cst);
    atomic_compare_exchange_strong_explicit(&flag, 0, 1, memory_order_seq_cst, memory_order_seq_cst);
    atomic_store_explicit(&counter, atomic_load_explicit(&counter, memory_order_acquire), memory_order_release);

    printf("counter=%d flag=%d\n", counter, flag);
}
