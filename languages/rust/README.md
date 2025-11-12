# 🦀 Rust Blockchain Development

Professional Rust examples for blockchain development on Solana and NEAR using the Anchor framework and NEAR SDK.

## 📋 Contents

- **src/lib.rs** - Anchor-based SPL token program (Solana)
  - Token minting with supply cap
  - Transfer functionality
  - Burn mechanism
  - Account state management
  - PDA (Program Derived Addresses)

- **examples/signature_verify.rs** - Cryptographic signature verification
  - Ed25519 signature creation
  - Transaction signing
  - Signature verification
  - Invalid signature detection

## 📦 Blockchain Support

This Rust implementation supports multiple blockchain platforms:

### Solana
- **Framework**: Anchor
- **Token Standard**: SPL (Solana Program Library)
- **Features**: High-performance, low-cost transactions
- **Use Cases**: DeFi, NFTs, payments

### NEAR Protocol
- **Framework**: NEAR SDK
- **Token Standard**: NEP-141 (Fungible Tokens)
- **Features**: Human-readable accounts, built-in scaling
- **Use Cases**: DeFi, NFTs, DAOs, social applications

## 🚀 Quick Start

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Add WASM target (for NEAR)
rustup target add wasm32-unknown-unknown
```

### Solana Setup

```bash
# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"

# Install Anchor
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install latest
avm use latest
```

### NEAR Setup

```bash
# Install NEAR CLI
npm install -g near-cli

# Install cargo-near for building
cargo install cargo-near
```

### Build

#### Solana (Anchor)

```bash
cd languages/rust

# Build the Anchor program
anchor build

# Build examples
cargo build --examples
```

#### NEAR

```bash
cd languages/rust

# Build NEAR contract
cargo near build

# Or standard build
cargo build --target wasm32-unknown-unknown --release
```

### Test

#### Solana

```bash
# Run Anchor tests
anchor test

# Run specific example
cargo run --example signature_verify
```

#### NEAR

```bash
# Run NEAR tests
cargo test

# Run with NEAR workspaces
cargo test --features near-sdk/unit-testing
```

### Deploy

#### Solana

```bash
# Deploy to devnet
anchor deploy --provider.cluster devnet

# Deploy to mainnet
anchor deploy --provider.cluster mainnet
```

#### NEAR

```bash
# Login to NEAR
near login

# Deploy to testnet
near deploy --accountId your-account.testnet --wasmFile target/wasm32-unknown-unknown/release/contract.wasm

# Deploy to mainnet
near deploy --accountId your-account.near --wasmFile target/wasm32-unknown-unknown/release/contract.wasm
```

## 🔧 Program Features

### Solana Token Program (Anchor)

A complete SPL token implementation with:

- **Initialization**: Set up token mint with configurable decimals and max supply
- **Minting**: Create new tokens up to the max supply limit
- **Transfers**: Move tokens between accounts
- **Burning**: Destroy tokens to reduce total supply
- **Account Management**: Track balances and ownership

### NEAR Smart Contracts

NEAR contracts can implement:

- **NEP-141**: Fungible token standard
- **NEP-171**: NFT standard
- **Cross-contract calls**: Interact with other contracts
- **State management**: Efficient storage patterns
- **Access control**: Role-based permissions

### Security Features

- Supply cap enforcement (Solana)
- Authority verification
- Balance checks
- PDA-based account derivation (Solana)
- State validation (NEAR)
- Comprehensive error handling

## 📚 Usage Examples

### Solana Examples

#### Initialize Token Mint

```rust
pub fn initialize_mint(
    ctx: Context<InitializeMint>,
    decimals: u8,
    max_supply: u64,
) -> Result<()>
```

### Mint Tokens

```rust
pub fn mint_tokens(
    ctx: Context<MintTokens>,
    amount: u64,
) -> Result<()>
```

### Transfer Tokens

```rust
pub fn transfer_tokens(
    ctx: Context<TransferTokens>,
    amount: u64,
) -> Result<()>
```

#### Burn Tokens

```rust
pub fn burn_tokens(
    ctx: Context<BurnTokens>,
    amount: u64,
) -> Result<()>
```

### NEAR Examples

NEAR smart contracts use a different syntax. Here's a basic example:

```rust
use near_sdk::borsh::{self, BorshDeserialize, BorshSerialize};
use near_sdk::{env, near_bindgen, AccountId, Balance};
use near_sdk::collections::LookupMap;

#[near_bindgen]
#[derive(BorshDeserialize, BorshSerialize)]
pub struct FungibleToken {
    owner_id: AccountId,
    total_supply: Balance,
    balances: LookupMap<AccountId, Balance>,
}

#[near_bindgen]
impl FungibleToken {
    #[init]
    pub fn new(owner_id: AccountId, total_supply: Balance) -> Self {
        let mut ft = Self {
            owner_id: owner_id.clone(),
            total_supply,
            balances: LookupMap::new(b"b"),
        };
        ft.balances.insert(&owner_id, &total_supply);
        ft
    }

    pub fn transfer(&mut self, receiver_id: AccountId, amount: Balance) {
        let sender_id = env::predecessor_account_id();
        let sender_balance = self.balances.get(&sender_id).unwrap_or(0);

        assert!(sender_balance >= amount, "Insufficient balance");

        let receiver_balance = self.balances.get(&receiver_id).unwrap_or(0);
        self.balances.insert(&sender_id, &(sender_balance - amount));
        self.balances.insert(&receiver_id, &(receiver_balance + amount));
    }
}
```

## 🧪 Testing

### Solana Testing

```bash
# All tests
anchor test

# With detailed output
anchor test -- --nocapture

# Specific test
anchor test -f "test_mint_tokens"
```

### NEAR Testing

```bash
# Unit tests
cargo test

# Integration tests with NEAR workspaces
cargo test --features integration-tests

# Simulation tests
near-workspaces test
```

## 📖 Project Structure

```
rust/
├── src/
│   └── lib.rs           # Main Anchor program
├── examples/
│   └── signature_verify.rs  # Signature verification demo
├── tests/
│   └── web3-token.ts    # TypeScript tests
├── Cargo.toml           # Rust dependencies
├── Anchor.toml          # Anchor configuration
└── README.md            # This file
```

## 🔐 Security Considerations

- All state changes are validated
- Authority checks on privileged operations
- Supply caps prevent inflation attacks
- Balance verification prevents overdrafts
- Uses Anchor's built-in security features

## 📖 Learn More

### Solana
- [Anchor Framework](https://www.anchor-lang.com/)
- [Solana Cookbook](https://solanacookbook.com/)
- [Solana Documentation](https://docs.solana.com/)
- [SPL Token Program](https://spl.solana.com/token)

### NEAR
- [NEAR SDK Documentation](https://docs.near.org/sdk/rust/introduction)
- [NEAR Examples](https://examples.near.org/)
- [NEAR Protocol](https://near.org/)
- [NEAR University](https://www.near.university/)

## 🎯 Use Cases

### Solana
- **DeFi Protocols**: High-speed DEXs, lending, AMMs
- **NFT Marketplaces**: Fast, low-cost NFT trading
- **Gaming**: Real-time blockchain gaming
- **Payments**: Micropayments and instant settlements

### NEAR
- **Social Applications**: Decentralized social networks
- **DeFi**: Cross-chain DeFi protocols
- **NFTs**: Creator-friendly NFT platforms
- **DAOs**: Governance and community management
- **Web3 Apps**: User-friendly dApps with human-readable accounts

## 📄 License

MIT License - See LICENSE file for details
