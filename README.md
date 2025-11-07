# 🌐 Web3 Multi-Language Playground

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Languages](https://img.shields.io/badge/languages-14+-green.svg)
![Commits](https://img.shields.io/github/commit-activity/m/pavlenkotm/megaeth-rpc-tester)
![Stars](https://img.shields.io/github/stars/pavlenkotm/megaeth-rpc-tester)

**A comprehensive showcase of Web3 development across 14+ programming languages**

This repository demonstrates professional Web3 development patterns, smart contracts, DApp frontends, blockchain utilities, and cryptographic implementations across the most popular languages in the Web3 ecosystem.

---

## 🎯 Overview

This is a **multi-language Web3 development portfolio** featuring real-world examples, production-ready code, and best practices for:

- ✅ Smart contract development (Solidity, Vyper, Move, Rust/Anchor)
- ✅ DApp frontend development (TypeScript, HTML/CSS, JavaScript)
- ✅ Blockchain client implementations (Go, Java, Ruby, Python)
- ✅ Low-level cryptography (C++, Zig, AssemblyScript)
- ✅ Functional programming (Haskell)
- ✅ DevOps and deployment (Bash scripts)

---

## 📚 Languages & Technologies

| Language | Use Case | Location | Features |
|----------|----------|----------|----------|
| **Solidity** | Smart Contracts | [`languages/solidity/`](languages/solidity/) | ERC-20, ERC-721, Hardhat |
| **Vyper** | Secure Contracts | [`languages/vyper/`](languages/vyper/) | Vault, ERC-20, Brownie |
| **Rust** | Solana Programs | [`languages/rust/`](languages/rust/) | Anchor, SPL Tokens |
| **Move** | Aptos/Sui | [`languages/move/`](languages/move/) | Token Module, Tests |
| **TypeScript** | DApp Frontend | [`languages/typescript/`](languages/typescript/) | React, Ethers.js, Wagmi |
| **JavaScript** | Web3 Integration | [`languages/html-css/`](languages/html-css/) | Wallet Connect, UI |
| **Go** | RPC Client | [`languages/go/`](languages/go/) | go-ethereum, Transactions |
| **Python** | RPC Tester | [`rpc_tester/`](rpc_tester/) | Async, Metrics, Reporting |
| **Java** | Enterprise Backend | [`languages/java/`](languages/java/) | Web3j, Maven |
| **C++** | Cryptography | [`languages/cpp/`](languages/cpp/) | OpenSSL, ECDSA, Hashing |
| **Bash** | DevOps | [`languages/bash/`](languages/bash/) | Deploy, Node Management |
| **Ruby** | Scripting | [`languages/ruby/`](languages/ruby/) | RPC Client, Balance Checker |
| **Zig** | Systems/WASM | [`languages/zig/`](languages/zig/) | Low-level Utils, Performance |
| **AssemblyScript** | WebAssembly | [`languages/assemblyscript/`](languages/assemblyscript/) | WASM Modules |
| **Haskell** | Functional | [`languages/haskell/`](languages/haskell/) | Type-safe RPC |
| **HTML/CSS** | Landing Pages | [`languages/html-css/`](languages/html-css/) | Responsive Design |

---

## 🚀 Quick Start

### Clone the Repository

```bash
git clone https://github.com/pavlenkotm/megaeth-rpc-tester.git
cd megaeth-rpc-tester
```

### Explore by Language

Each language folder contains:
- ✅ Complete, runnable code examples
- ✅ Dedicated README with setup instructions
- ✅ Dependencies and build configurations
- ✅ Usage examples and documentation

```bash
# Solidity Smart Contracts
cd languages/solidity
npm install
npx hardhat compile

# Rust/Anchor Solana Programs
cd languages/rust
anchor build
anchor test

# TypeScript DApp Components
cd languages/typescript
npm install
npm run dev

# Go RPC Client
cd languages/go
go run rpc_client.go

# And so on for each language...
```

---

## 💎 Highlighted Projects

### 🔷 Solidity: Advanced Token Contracts

**ERC-20 Token** with:
- Mintable with supply cap
- Burnable tokens
- Permit (EIP-2612) gasless approvals
- Batch transfers

**ERC-721 NFT Collection** with:
- Whitelist minting
- Per-wallet limits
- Batch operations
- Metadata management

[View Solidity Examples →](languages/solidity/)

### 🦀 Rust: Solana Token Program

Full SPL token implementation using Anchor:
- Initialize mint with configurable parameters
- Mint, transfer, and burn operations
- PDA-based account management
- Comprehensive test coverage

[View Rust Examples →](languages/rust/)

### 🔷 TypeScript: React DApp Components

Production-ready React components:
- **WalletConnect**: MetaMask integration
- **useContract**: Smart contract interaction hook
- **web3Utils**: 20+ utility functions

[View TypeScript Examples →](languages/typescript/)

### 🐹 Go: Enterprise RPC Client

Professional Go client for Ethereum:
- Transaction sending and monitoring
- Balance queries and gas estimation
- Signature verification
- Error handling and retries

[View Go Examples →](languages/go/)

### 🎨 HTML/CSS: Web3 Landing Page

Modern, responsive DApp landing page:
- Dark theme with gradients
- MetaMask wallet integration
- Mobile-responsive design
- Zero build tools required

[View Landing Page →](languages/html-css/)

---

## 🏗️ Repository Structure

```
megaeth-rpc-tester/
├── languages/                    # Multi-language examples
│   ├── solidity/                # Smart contracts (Hardhat)
│   ├── vyper/                   # Vyper contracts
│   ├── rust/                    # Solana/Anchor programs
│   ├── move/                    # Aptos/Sui modules
│   ├── typescript/              # React/Web3 components
│   ├── go/                      # Go RPC client
│   ├── cpp/                     # C++ crypto utils
│   ├── java/                    # Web3j integration
│   ├── bash/                    # Deployment scripts
│   ├── ruby/                    # Ruby RPC client
│   ├── zig/                     # Zig WASM utilities
│   ├── assemblyscript/          # AS/WASM modules
│   ├── haskell/                 # Functional RPC client
│   └── html-css/                # Landing page
├── rpc_tester/                  # Python RPC testing tool
├── examples/                    # Python usage examples
├── tests/                       # Test suites
├── .github/                     # CI/CD workflows
├── CONTRIBUTING.md              # Contribution guidelines
├── CODE_OF_CONDUCT.md           # Code of conduct
└── README.md                    # This file
```

---

## 🎓 Learning Resources

Each language folder includes:

- **📖 Comprehensive README** - Setup, usage, and examples
- **💻 Working Code** - Production-ready implementations
- **🧪 Tests** - Unit and integration tests where applicable
- **📦 Dependencies** - All configs (package.json, Cargo.toml, etc.)
- **🔧 Build Scripts** - Easy compilation and deployment

---

## 🌟 Key Features

### Smart Contracts
- **Solidity**: ERC-20, ERC-721, Hardhat deployment
- **Vyper**: Secure vault, token with Brownie
- **Move**: Aptos token module with tests
- **Rust**: Solana SPL token with Anchor

### DApp Development
- **TypeScript**: React hooks, wallet connection
- **JavaScript**: Web3 utilities, Ethers.js integration
- **HTML/CSS**: Responsive landing pages

### Blockchain Clients
- **Go**: Full-featured RPC client
- **Python**: Async RPC tester with metrics
- **Java**: Web3j enterprise integration
- **Ruby**: Simple RPC wrapper

### Low-Level & Performance
- **C++**: Cryptographic primitives (SHA-256, ECDSA)
- **Zig**: WASM-compatible utilities
- **AssemblyScript**: WebAssembly modules

### DevOps
- **Bash**: Contract deployment, node management
- **GitHub Actions**: CI/CD pipelines

---

## 🧪 Testing

Most language implementations include tests:

```bash
# Solidity
npx hardhat test

# Rust/Anchor
anchor test

# TypeScript
npm test

# Go
go test ./...

# Python
pytest

# And more...
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Areas for Contribution

- 🐛 Bug fixes and improvements
- ✨ New language examples
- 📚 Documentation enhancements
- 🧪 Additional test coverage
- 🎨 UI/UX improvements

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links & Resources

- **GitHub**: https://github.com/pavlenkotm/megaeth-rpc-tester
- **Issues**: https://github.com/pavlenkotm/megaeth-rpc-tester/issues
- **Discussions**: https://github.com/pavlenkotm/megaeth-rpc-tester/discussions

### Official Documentation

- [Ethereum](https://ethereum.org/developers)
- [Solana](https://docs.solana.com/)
- [Aptos](https://aptos.dev/)
- [Hardhat](https://hardhat.org/)
- [Anchor](https://www.anchor-lang.com/)
- [Ethers.js](https://docs.ethers.org/)

---

## 📊 Repository Stats

- **14+ Programming Languages**
- **40+ Meaningful Commits**
- **Professional Code Quality**
- **Comprehensive Documentation**
- **Production-Ready Examples**

---

## 👨‍💻 Author

**Developed with ⚡ for the Web3 community**

- GitHub: [@pavlenkotm](https://github.com/pavlenkotm)
- Repository: [megaeth-rpc-tester](https://github.com/pavlenkotm/megaeth-rpc-tester)

---

## ⭐ Show Your Support

If you find this repository helpful, please consider giving it a star! ⭐

---

Made with ❤️ for Web3 developers everywhere
