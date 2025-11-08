# Cairo - StarkNet Smart Contracts

![Cairo](https://img.shields.io/badge/Cairo-StarkNet-orange)
![Version](https://img.shields.io/badge/version-2.0-blue)

## Overview

Cairo is the programming language for writing smart contracts on StarkNet, a Layer 2 scaling solution for Ethereum using ZK-rollups.

## Features

- ✅ ERC-20 Token Contract
- ✅ Account Abstraction
- ✅ ZK-Proof Integration
- ✅ Cairo 2.0 Syntax

## Installation

```bash
# Install Scarb (Cairo package manager)
curl --proto '=https' --tlsv1.2 -sSf https://docs.swmansion.com/scarb/install.sh | sh

# Verify installation
scarb --version
```

## Usage

```bash
# Compile contracts
scarb build

# Run tests
scarb test

# Format code
scarb fmt
```

## Contract Examples

### ERC-20 Token (`token.cairo`)

A standard ERC-20 implementation with Cairo 2.0:
- Mint, transfer, approve
- Balance queries
- Total supply tracking

### Account Contract (`account.cairo`)

Account abstraction implementation:
- Multi-call support
- Signature verification
- Nonce management

## Resources

- [Cairo Documentation](https://www.cairo-lang.org/docs/)
- [StarkNet Book](https://book.starknet.io/)
- [Cairo by Example](https://cairo-by-example.com/)

## License

MIT License - See LICENSE file for details
