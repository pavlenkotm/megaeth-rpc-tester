# 🔧 C++ Crypto Utilities

Professional C++ implementations of cryptographic algorithms used in Web3 and blockchain development.

## 📋 Contents

- **crypto_utils.cpp** - Cryptographic utility functions
  - SHA-256 hashing
  - Double SHA-256 (Bitcoin)
  - RIPEMD-160 hashing
  - Hash160 (SHA-256 + RIPEMD-160)
  - ECDSA key pair generation (secp256k1)
  - Public/private key handling
  - Hash verification

## 🚀 Quick Start

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get install build-essential cmake libssl-dev

# macOS
brew install cmake openssl

# Fedora/RHEL
sudo dnf install gcc-c++ cmake openssl-devel
```

### Build

```bash
cd languages/cpp

# Create build directory
mkdir build && cd build

# Configure
cmake ..

# Build
make

# Run
./crypto_utils
```

### Alternative: Direct Compilation

```bash
g++ -o crypto_utils crypto_utils.cpp -lssl -lcrypto -std=c++17
./crypto_utils
```

## 🔧 Features

### Hashing Functions

- **SHA-256**: Standard SHA-256 hashing
- **Double SHA-256**: Two rounds of SHA-256 (Bitcoin)
- **RIPEMD-160**: RIPEMD-160 hashing algorithm
- **Hash160**: SHA-256 followed by RIPEMD-160 (Bitcoin addresses)

### ECDSA Operations

- **Key Generation**: Create secp256k1 key pairs
- **Public Key Export**: Get uncompressed public key
- **Private Key Export**: Get private key in hex format
- **Curve**: secp256k1 (used in Bitcoin and Ethereum)

### Utility Functions

- **Hex Encoding**: Convert bytes to hexadecimal strings
- **Hash Verification**: Validate hash format
- **Error Handling**: Robust error checking

## 📚 Usage Examples

### SHA-256 Hash

```cpp
#include "crypto_utils.cpp"

std::string message = "Hello, Blockchain!";
std::string hash = Web3Crypto::sha256(message);
std::cout << "SHA-256: " << hash << std::endl;
```

### Double SHA-256 (Bitcoin)

```cpp
std::string double_hash = Web3Crypto::double_sha256(message);
std::cout << "Double SHA-256: " << double_hash << std::endl;
```

### Hash160 (Bitcoin Address Hash)

```cpp
std::string hash160 = Web3Crypto::hash160(publicKey);
std::cout << "Hash160: " << hash160 << std::endl;
```

### Generate ECDSA Key Pair

```cpp
Web3Crypto::ECDSAKeyPair keypair;
std::cout << "Private Key: " << keypair.get_private_key_hex() << std::endl;
std::cout << "Public Key: " << keypair.get_public_key_hex() << std::endl;
```

### Verify Hash Format

```cpp
bool isValid = Web3Crypto::verify_hash_format(hash);
std::cout << "Valid hash: " << isValid << std::endl;
```

## 🧪 Testing

```bash
# Build with tests
cmake -DBUILD_TESTING=ON ..
make
ctest
```

## 📖 Project Structure

```
cpp/
├── crypto_utils.cpp     # Main implementation
├── CMakeLists.txt       # CMake build configuration
└── README.md            # This file
```

## 🔐 Security Considerations

- Uses OpenSSL for production-grade cryptography
- Implements secp256k1 curve (Ethereum/Bitcoin standard)
- Proper memory management for keys
- Secure random number generation
- RAII pattern for resource management

## 📚 Learn More

- [OpenSSL Documentation](https://www.openssl.org/docs/)
- [secp256k1 Curve](https://en.bitcoin.it/wiki/Secp256k1)
- [Cryptographic Hash Functions](https://en.wikipedia.org/wiki/Cryptographic_hash_function)
- [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)

## 🎯 Use Cases

- **Wallet Development**: Generate and manage keys
- **Transaction Signing**: Create and verify signatures
- **Address Generation**: Bitcoin/Ethereum address creation
- **Hash Verification**: Validate transaction hashes
- **Custom Blockchains**: Build your own blockchain protocol

## ⚡ Performance

- Optimized with OpenSSL
- Zero-copy where possible
- Efficient memory management
- Suitable for high-throughput applications

## 📄 License

MIT License - See LICENSE file for details
