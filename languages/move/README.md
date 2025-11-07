# 🚀 Move Smart Contracts

Professional Move language examples for Aptos and Sui blockchain development.

## 📋 Contents

- **token.move** - Simple token implementation
  - Token initialization with metadata
  - Mint and burn functionality
  - Transfer capabilities
  - Supply cap enforcement
  - Event emission
  - Comprehensive tests

## 🚀 Quick Start

### Prerequisites

```bash
# Install Aptos CLI
curl -fsSL "https://aptos.dev/scripts/install_cli.py" | python3
```

### Build

```bash
cd languages/move

# Compile the Move module
aptos move compile

# Run tests
aptos move test
```

### Deploy

```bash
# Initialize account
aptos init

# Publish module
aptos move publish --named-addresses web3_examples=default

# Run initialization function
aptos move run \
  --function-id 'default::simple_token::initialize' \
  --args string:"MyToken" string:"MTK" u8:8 u64:1000000
```

## 🔧 Features

### Token Module

- **Initialization**: Set up token with name, symbol, decimals, and max supply
- **Minting**: Create new tokens (admin only, respects max supply)
- **Burning**: Destroy tokens to reduce supply
- **Transfers**: Send tokens between accounts
- **Balance Queries**: Check token balances
- **Supply Tracking**: Monitor total and remaining supply
- **Events**: Comprehensive event logging for all operations

### Security Features

- **Supply Cap**: Enforced maximum supply
- **Access Control**: Admin-only minting
- **Type Safety**: Move's resource model prevents double-spending
- **Balance Checks**: Automatic balance verification
- **Test Coverage**: Unit tests included

## 📚 Usage Examples

### Initialize Token

```bash
aptos move run \
  --function-id 'YOUR_ADDR::simple_token::initialize' \
  --args \
    string:"Web3 Token" \
    string:"W3T" \
    u8:8 \
    u64:1000000000
```

### Mint Tokens

```bash
aptos move run \
  --function-id 'YOUR_ADDR::simple_token::mint' \
  --args \
    address:RECIPIENT_ADDRESS \
    u64:1000000
```

### Transfer Tokens

```bash
aptos move run \
  --function-id 'YOUR_ADDR::simple_token::transfer' \
  --args \
    address:RECIPIENT_ADDRESS \
    u64:500000
```

### Burn Tokens

```bash
aptos move run \
  --function-id 'YOUR_ADDR::simple_token::burn' \
  --args u64:100000
```

### Query Balance

```bash
aptos move view \
  --function-id 'YOUR_ADDR::simple_token::balance_of' \
  --args address:ACCOUNT_ADDRESS
```

## 🧪 Testing

```bash
# Run all tests
aptos move test

# Run with coverage
aptos move test --coverage

# Run specific test
aptos move test --filter test_mint_and_transfer
```

## 📖 Project Structure

```
move/
├── sources/
│   └── token.move       # Token implementation
├── Move.toml            # Package configuration
└── README.md            # This file
```

## 🔐 Move Language Benefits

- **Resource Safety**: Linear type system prevents double-spending
- **Formal Verification**: Mathematical proofs of correctness
- **Gas Efficiency**: Optimized for blockchain execution
- **Type Safety**: Strong static typing catches errors at compile time
- **No Reentrancy**: Resource model eliminates reentrancy attacks

## 📚 Learn More

- [Move Book](https://move-language.github.io/move/)
- [Aptos Documentation](https://aptos.dev/)
- [Sui Documentation](https://docs.sui.io/)
- [Move Patterns](https://www.move-patterns.com/)

## 🎯 Use Cases

- **DeFi Protocols**: DEXs, lending platforms, staking
- **NFT Platforms**: Marketplaces, collections, gaming
- **DAOs**: Governance tokens and voting systems
- **GameFi**: In-game currencies and assets
- **Identity**: Decentralized identity and credentials

## 📄 License

MIT License - See LICENSE file for details
