# Clarity - Stacks Blockchain Smart Contracts

![Clarity](https://img.shields.io/badge/Clarity-Stacks-purple)
![Bitcoin](https://img.shields.io/badge/Powered_by-Bitcoin-orange)

## Overview

Clarity is a decidable smart contract language for the Stacks blockchain, enabling smart contracts on Bitcoin. It's designed to be safe, secure, and predictable.

## Features

- ✅ SIP-010 Fungible Token
- ✅ SIP-009 NFT
- ✅ Bitcoin Integration
- ✅ Decidable Language (No Infinite Loops)

## Installation

```bash
# Install Clarinet
curl -L https://github.com/hirosystems/clarinet/releases/download/v1.7.0/clarinet-linux-x64.tar.gz | tar xz
sudo mv clarinet /usr/local/bin/

# Verify installation
clarinet --version
```

## Usage

```bash
# Create new project
clarinet new my-project

# Check contract
clarinet check

# Run tests
clarinet test

# Deploy
clarinet deploy
```

## Contract Examples

### Fungible Token (`token.clar`)

SIP-010 compliant fungible token:
- Transfer functions
- Balance tracking
- Token metadata

### NFT Contract (`nft.clar`)

SIP-009 NFT implementation:
- Minting and burning
- Ownership tracking
- Metadata URIs

## Resources

- [Clarity Documentation](https://docs.stacks.co/clarity/)
- [Clarity Book](https://book.clarity-lang.org/)
- [Stacks Blockchain](https://www.stacks.co/)

## License

MIT License
