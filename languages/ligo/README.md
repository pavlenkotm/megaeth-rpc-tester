# LIGO - Tezos Smart Contracts

![LIGO](https://img.shields.io/badge/LIGO-Tezos-blue)
![Syntax](https://img.shields.io/badge/syntax-CameLIGO-green)

## Overview

LIGO is a friendly smart contract language for Tezos blockchain. It offers multiple syntaxes (CameLIGO, JsLIGO) and compiles to Michelson.

## Features

- ✅ FA2 Token Standard (NFTs & Fungible)
- ✅ Multi-syntax Support
- ✅ Strong Type System
- ✅ Formal Verification Ready

## Installation

```bash
# Using Docker (recommended)
docker pull ligolang/ligo:stable

# Or install locally
curl -L https://gitlab.com/ligolang/ligo/-/releases/permalink/latest/downloads/ligo-linux -o ligo
chmod +x ligo
sudo mv ligo /usr/local/bin/
```

## Usage

```bash
# Compile contract
ligo compile contract token.mligo

# Run tests
ligo run test test/token.test.mligo

# Simulate call
ligo run dry-run token.mligo 'Transfer({from: alice, to: bob, value: 100})'
```

## Contract Examples

### FA2 Token (`token.mligo`)

Tezos FA2 multi-asset standard:
- NFT support
- Fungible token support
- Batch operations
- Operator permissions

### Simple Storage (`storage.mligo`)

Basic storage contract example:
- Increment/decrement
- State management

## Resources

- [LIGO Documentation](https://ligolang.org/docs/intro/introduction)
- [LIGO Playground](https://ide.ligolang.org/)
- [Tezos FA2 Standard](https://gitlab.com/tezos/tzip/-/blob/master/proposals/tzip-12/tzip-12.md)

## License

MIT License
