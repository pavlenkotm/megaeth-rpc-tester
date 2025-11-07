/**
 * AssemblyScript Web3 Utilities
 * Compile to WebAssembly for browser/Node.js
 */

// Simple Keccak-256 placeholder (use actual implementation in production)
export function keccak256(data: Uint8Array): Uint8Array {
  const hash = new Uint8Array(32);
  // Placeholder - use actual Keccak implementation
  for (let i = 0; i < 32; i++) {
    hash[i] = 0;
  }
  return hash;
}

// Convert bytes to hex string
export function bytesToHex(bytes: Uint8Array): string {
  const hexChars = "0123456789abcdef";
  let hex = "";

  for (let i = 0; i < bytes.length; i++) {
    const byte = bytes[i];
    hex += hexChars.charAt(byte >> 4);
    hex += hexChars.charAt(byte & 0x0F);
  }

  return hex;
}

// Validate Ethereum address format
export function isValidAddress(address: string): boolean {
  if (address.length != 42) return false;
  if (address.charAt(0) != '0' || address.charAt(1) != 'x') return false;

  for (let i = 2; i < address.length; i++) {
    const char = address.charAt(i);
    if (!isHexChar(char)) return false;
  }

  return true;
}

// Check if character is hex
function isHexChar(char: string): boolean {
  const code = char.charCodeAt(0);
  return (code >= 48 && code <= 57) ||  // 0-9
         (code >= 65 && code <= 70) ||  // A-F
         (code >= 97 && code <= 102);   // a-f
}

// Simple hash function
export function simpleHash(input: string): u32 {
  let hash: u32 = 0;

  for (let i = 0; i < input.length; i++) {
    hash = ((hash << 5) - hash) + input.charCodeAt(i);
    hash = hash & hash; // Convert to 32bit integer
  }

  return hash;
}

// Convert Wei to Eth (simplified)
export function weiToEth(wei: u64): f64 {
  return f64(wei) / 1000000000000000000.0;
}

// Convert Eth to Wei (simplified)
export function ethToWei(eth: f64): u64 {
  return u64(eth * 1000000000000000000.0);
}
