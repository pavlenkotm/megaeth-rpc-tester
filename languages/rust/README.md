# 🦀 Rust Web3 Examples

Professional Rust examples for Solana blockchain development using the Anchor framework and Solana SDK.

## 📋 Contents

- **src/lib.rs** - Anchor-based SPL token program
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

## 🚀 Quick Start

### Prerequisites

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install Solana CLI
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"

# Install Anchor
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install latest
avm use latest
```

### Build

```bash
cd languages/rust

# Build the Anchor program
anchor build

# Build examples
cargo build --examples
```

### Test

```bash
# Run Anchor tests
anchor test

# Run specific example
cargo run --example signature_verify
```

### Deploy

```bash
# Deploy to devnet
anchor deploy --provider.cluster devnet

# Deploy to mainnet
anchor deploy --provider.cluster mainnet
```

## 🔧 Program Features

### Web3 Token Program

A complete SPL token implementation with:

- **Initialization**: Set up token mint with configurable decimals and max supply
- **Minting**: Create new tokens up to the max supply limit
- **Transfers**: Move tokens between accounts
- **Burning**: Destroy tokens to reduce total supply
- **Account Management**: Track balances and ownership

### Security Features

- Supply cap enforcement
- Authority verification
- Balance checks
- PDA-based account derivation
- Comprehensive error handling

## 📚 Usage Examples

### Initialize Token Mint

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

### Burn Tokens

```rust
pub fn burn_tokens(
    ctx: Context<BurnTokens>,
    amount: u64,
) -> Result<()>
```

## 🧪 Testing

Run comprehensive tests:

```bash
# All tests
anchor test

# With detailed output
anchor test -- --nocapture

# Specific test
anchor test -f "test_mint_tokens"
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

- [Anchor Framework](https://www.anchor-lang.com/)
- [Solana Cookbook](https://solanacookbook.com/)
- [Solana Documentation](https://docs.solana.com/)
- [SPL Token Program](https://spl.solana.com/token)

## 🎯 Use Cases

- **DeFi Protocols**: Build lending, staking, or AMM platforms
- **NFT Projects**: Create token-gated communities
- **Gaming**: Implement in-game currencies
- **DAOs**: Governance tokens and treasury management

## 📄 License

MIT License - See LICENSE file for details
