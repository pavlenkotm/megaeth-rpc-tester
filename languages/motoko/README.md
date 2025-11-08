# Motoko - Internet Computer Smart Contracts

![Motoko](https://img.shields.io/badge/Motoko-Internet_Computer-blue)
![DFINITY](https://img.shields.io/badge/DFINITY-ICP-purple)

## Overview

Motoko is a programming language designed specifically for the Internet Computer blockchain, providing safe, secure, and efficient canister development.

## Features

- ✅ Token Canister (ICRC-1)
- ✅ Actor-based Architecture
- ✅ Async/Await Support
- ✅ Orthogonal Persistence

## Installation

```bash
# Install DFX (Internet Computer SDK)
sh -ci "$(curl -fsSL https://internetcomputer.org/install.sh)"

# Verify installation
dfx --version
```

## Usage

```bash
# Start local replica
dfx start --background

# Deploy canister
dfx deploy

# Call canister methods
dfx canister call token balance_of '(principal "xxxxx")'
```

## Canister Examples

### Token Canister (`token.mo`)

ICRC-1 compliant token:
- Transfer operations
- Balance queries
- Allowances

### Counter Canister (`counter.mo`)

Simple state management example:
- Increment/decrement
- Persistent storage

## Resources

- [Motoko Documentation](https://internetcomputer.org/docs/current/motoko/main/motoko)
- [Internet Computer SDK](https://internetcomputer.org/docs/current/developer-docs/setup/install)
- [Motoko Playground](https://m7sm4-2iaaa-aaaab-qabra-cai.raw.ic0.app/)

## License

MIT License
