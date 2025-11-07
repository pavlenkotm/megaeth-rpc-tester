# Quick Start Guide for All Languages

This guide helps you get started with any language in this repository.

## Choose Your Language

Click on your preferred language to jump to its quick start:

- [Solidity](#solidity---smart-contracts)
- [TypeScript](#typescript---dapp-frontend)
- [Rust](#rust---solana-programs)
- [Go](#go---rpc-client)
- [Python](#python---rpc-tester)
- [Java](#java---enterprise-backend)
- [C++](#c---cryptography)
- [Vyper](#vyper---secure-contracts)
- [Move](#move---aptos-contracts)
- [Bash](#bash---deployment-scripts)
- [Ruby](#ruby---scripting)
- [Zig](#zig---systems-programming)
- [Haskell](#haskell---functional-web3)
- [AssemblyScript](#assemblyscript---webassembly)
- [HTML/CSS](#htmlcss---landing-pages)

---

## Solidity - Smart Contracts

```bash
cd languages/solidity
npm install
npx hardhat compile
npx hardhat test
```

Deploy to testnet:
```bash
npx hardhat run scripts/deploy.js --network sepolia
```

## TypeScript - DApp Frontend

```bash
cd languages/typescript
npm install
npm run dev
```

## Rust - Solana Programs

```bash
cd languages/rust
anchor build
anchor test
```

Deploy to devnet:
```bash
anchor deploy --provider.cluster devnet
```

## Go - RPC Client

```bash
cd languages/go
go run rpc_client.go
```

## Python - RPC Tester

```bash
cd ../  # back to root
python -m rpc_tester https://eth.llamarpc.com
```

## Java - Enterprise Backend

```bash
cd languages/java
mvn compile
mvn exec:java
```

## C++ - Cryptography

```bash
cd languages/cpp
mkdir build && cd build
cmake ..
make
./crypto_utils
```

## Vyper - Secure Contracts

```bash
cd languages/vyper
vyper SimpleVault.vy
```

## Move - Aptos Contracts

```bash
cd languages/move
aptos move compile
aptos move test
```

## Bash - Deployment Scripts

```bash
cd languages/bash
./deploy.sh
```

## Ruby - Scripting

```bash
cd languages/ruby
ruby web3_client.rb
```

## Zig - Systems Programming

```bash
cd languages/zig
zig build run
```

## Haskell - Functional Web3

```bash
cd languages/haskell
ghc -o web3-client Web3Client.hs
./web3-client
```

## AssemblyScript - WebAssembly

```bash
cd languages/assemblyscript
npm install
npm run asbuild
```

## HTML/CSS - Landing Pages

```bash
cd languages/html-css
# Open index.html in browser or use:
python -m http.server 8000
```

---

## Common Issues

### Node.js not found
```bash
# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Rust/Anchor not found
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

### Go not found
```bash
# Download from https://go.dev/dl/
# Or use package manager:
sudo apt install golang-go  # Ubuntu/Debian
brew install go             # macOS
```

---

## Next Steps

1. **Explore the code**: Each folder has a README with detailed explanations
2. **Modify examples**: Try changing parameters and rerunning
3. **Add your own**: Create new functions or contracts
4. **Deploy**: Use testnets to deploy your changes
5. **Contribute**: Submit a PR with your improvements!

## Need Help?

- Check the individual README in each language folder
- Open an issue on GitHub
- Read the main [CONTRIBUTING.md](../CONTRIBUTING.md)
