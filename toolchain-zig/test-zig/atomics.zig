// atomics.zig
const std = @import("std");

var counter: u64 = 0;
var flag: u32 = 0;

pub fn main() void {
    _ = @atomicRmw(u64, &counter, .Add, 5, .seq_cst); // -> call __atomic_fetch_add_8
    const old = @cmpxchgStrong(u32, &flag, 0, 1, .seq_cst, .seq_cst); // -> call __atomic_compare_exchange_4
    @atomicStore(u64, &counter, @atomicLoad(u64, &counter, .acquire) * 3, .release);
    std.debug.print("counter={d} flag={d} old={?d}\n", .{ counter, flag, old });
}
