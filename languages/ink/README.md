# 🦑 ink! Smart Contracts

Professional ink! smart contract examples for Polkadot and Substrate-based blockchains.

## 📋 Overview

ink! is an eDSL (embedded domain-specific language) for writing smart contracts in Rust for blockchains built on Substrate, including Polkadot parachains.

## 📦 Contents

- **lib.rs** - Complete ERC20 token implementation in ink!
  - Token minting and transfers
  - Allowance mechanism
  - Event emission
  - Comprehensive testing
  - Gas-optimized storage

## 🚀 Quick Start

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install ink! CLI (cargo-contract)
cargo install cargo-contract --force

# Add Rust target for WASM
rustup component add rust-src
rustup target add wasm32-unknown-unknown
```

### Build

```bash
cd languages/ink

# Build the contract
cargo contract build

# Build with release optimization
cargo contract build --release
```

### Test

```bash
# Run tests
cargo test

# Run tests with output
cargo test -- --nocapture
```

### Deploy

```bash
# Deploy to local Substrate node
cargo contract instantiate --constructor new \
  --args 1000000 "MyToken" "MTK" 18 \
  --suri //Alice \
  --skip-confirm

# Upload code only
cargo contract upload --suri //Alice
```

## 🔧 Contract Features

### ERC20 Token

A complete ERC20-compatible token implementation:

- **Metadata**: Name, symbol, decimals
- **Balances**: Account balance tracking
- **Transfers**: Direct token transfers
- **Allowances**: Approve and transferFrom pattern
- **Events**: Transfer and Approval events
- **Safety**: Overflow protection and balance checks

### ink! Advantages

- **Rust Safety**: Memory safety, type safety, thread safety
- **WASM**: Compiles to WebAssembly for fast execution
- **Storage Optimization**: Efficient on-chain storage
- **Testing**: Built-in test framework
- **Upgradeable**: Proxy pattern support
- **Low Gas Costs**: Optimized for Substrate

## 📚 Usage Examples

### Initialize Token

```rust
let contract = Erc20::new(
    1_000_000_000,           // Total supply
    "My Token".to_string(),  // Name
    "MTK".to_string(),       // Symbol
    18                       // Decimals
);
```

### Transfer Tokens

```rust
contract.transfer(recipient, 100)?;
```

### Approve Allowance

```rust
contract.approve(spender, 500)?;
```

### Transfer From

```rust
contract.transfer_from(owner, recipient, 100)?;
```

## 🧪 Testing

Run comprehensive tests:

```bash
# All tests
cargo test

# Specific test
cargo test transfer_works

# With code coverage
cargo tarpaulin
```

## 📖 Project Structure

```
ink/
├── lib.rs           # Smart contract implementation
├── Cargo.toml       # Dependencies and metadata
└── README.md        # This file
```

## 🌐 Supported Networks

- **Polkadot Parachains**: Astar, Phala, Moonbeam, etc.
- **Substrate Chains**: Any Substrate-based blockchain with contracts pallet
- **Local Development**: substrate-contracts-node

## 🔐 Security Best Practices

- Use ink!'s built-in overflow protection
- Validate all inputs in public functions
- Use events for transparency
- Test edge cases thoroughly
- Follow checks-effects-interactions pattern
- Audit before mainnet deployment

## 📖 Learn More

- [ink! Documentation](https://use.ink/)
- [ink! Examples](https://github.com/paritytech/ink-examples)
- [Substrate Documentation](https://docs.substrate.io/)
- [Polkadot Wiki](https://wiki.polkadot.network/)

## 🎯 Use Cases

- **DeFi**: DEXs, lending protocols, stablecoins
- **NFTs**: ERC721/ERC1155 implementations
- **DAOs**: Governance and treasury management
- **Gaming**: In-game assets and economies
- **Identity**: Decentralized identity solutions

## 🔗 Ecosystem

- **Polkadot**: Main relay chain
- **Kusama**: Canary network
- **Astar**: Smart contract hub
- **Phala**: Privacy-preserving contracts
- **Moonbeam**: Ethereum compatibility

## 📄 License

MIT License - See LICENSE file for details
