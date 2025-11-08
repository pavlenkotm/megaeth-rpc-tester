# Sway - Fuel Blockchain Smart Contracts

![Sway](https://img.shields.io/badge/Sway-Fuel-green)
![Version](https://img.shields.io/badge/version-latest-blue)

## Overview

Sway is a domain-specific language for the Fuel blockchain, inspired by Rust. It brings modern language features and safety to blockchain development.

## Features

- ✅ Token Contract (SRC-20)
- ✅ NFT Contract (SRC-721)
- ✅ Predicates
- ✅ Scripts

## Installation

```bash
# Install fuelup (Fuel toolchain manager)
curl --proto '=https' --tlsv1.2 -sSf https://install.fuel.network/fuelup-init.sh | sh

# Update toolchain
fuelup toolchain install latest
fuelup default latest
```

## Usage

```bash
# Build contract
forc build

# Run tests
forc test

# Deploy
forc deploy
```

## Contract Examples

### Token Contract (`src/main.sw`)

SRC-20 compliant token with:
- Minting and burning
- Transfer functionality
- Balance queries

### NFT Contract (`src/nft.sw`)

SRC-721 NFT implementation:
- Unique token IDs
- Ownership tracking
- Metadata support

## Resources

- [Sway Documentation](https://fuellabs.github.io/sway/)
- [Sway Book](https://fuellabs.github.io/sway/latest/book/)
- [Fuel Network](https://fuel.network/)

## License

MIT License
