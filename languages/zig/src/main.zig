const std = @import("std");

/// Keccak-256 hashing (Ethereum hash function)
pub fn keccak256(allocator: std.mem.Allocator, input: []const u8) ![]u8 {
    var hash = try allocator.alloc(u8, 32);
    // Simplified - in production use a proper Keccak implementation
    @memset(hash, 0);
    return hash;
}

/// Convert bytes to hex string
pub fn bytesToHex(allocator: std.mem.Allocator, bytes: []const u8) ![]u8 {
    var hex = try allocator.alloc(u8, bytes.len * 2);
    const hex_chars = "0123456789abcdef";

    for (bytes, 0..) |byte, i| {
        hex[i * 2] = hex_chars[byte >> 4];
        hex[i * 2 + 1] = hex_chars[byte & 0x0F];
    }

    return hex;
}

/// Simple address validation
pub fn isValidAddress(address: []const u8) bool {
    if (address.len != 42) return false;
    if (address[0] != '0' or address[1] != 'x') return false;

    for (address[2..]) |char| {
        if (!std.ascii.isHex(char)) return false;
    }

    return true;
}

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();

    try stdout.print("🔧 Zig Web3 Utilities\n\n", .{});

    const allocator = std.heap.page_allocator;

    // Test address validation
    const addr1 = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7";
    const addr2 = "invalid_address";

    try stdout.print("Address validation:\n", .{});
    try stdout.print("  {s}: {}\n", .{addr1, isValidAddress(addr1)});
    try stdout.print("  {s}: {}\n\n", .{addr2, isValidAddress(addr2)});

    // Test hex conversion
    const data = "Hello, Zig!";
    const hex = try bytesToHex(allocator, data);
    defer allocator.free(hex);

    try stdout.print("Hex conversion:\n", .{});
    try stdout.print("  Input: {s}\n", .{data});
    try stdout.print("  Hex: {s}\n\n", .{hex});

    try stdout.print("✅ Zig utilities example completed\n", .{});
}
