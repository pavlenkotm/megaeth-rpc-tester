# 🔷 Solidity Smart Contracts

Professional Solidity examples demonstrating modern Web3 development patterns with OpenZeppelin contracts and Hardhat.

## 📋 Contents

- **Web3Token.sol** - ERC-20 token with advanced features
  - Mintable with supply cap
  - Burnable tokens
  - Permit (EIP-2612) for gasless approvals
  - Batch transfers
  - Owner controls

- **Web3NFT.sol** - ERC-721 NFT collection
  - Auto-incrementing token IDs
  - URI storage for metadata
  - Whitelist minting
  - Max supply and per-wallet limits
  - Royalty support
  - Batch minting

## 🚀 Quick Start

### Prerequisites

```bash
node >= 16.0.0
npm >= 8.0.0
```

### Installation

```bash
cd languages/solidity
npm install
```

### Compile Contracts

```bash
npm run compile
```

### Run Tests

```bash
npm run test
```

### Deploy Locally

```bash
# Terminal 1: Start local node
npm run node

# Terminal 2: Deploy contracts
npm run deploy
```

### Deploy to Testnet

1. Create `.env` file:

```env
PRIVATE_KEY=your_private_key_here
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/your-api-key
ETHERSCAN_API_KEY=your_etherscan_api_key
```

2. Deploy:

```bash
npx hardhat run scripts/deploy.js --network sepolia
```

## 🔧 Configuration

Edit `hardhat.config.js` to:
- Add more networks
- Adjust compiler settings
- Configure gas reporter
- Set up Etherscan verification

## 📚 Key Features

### Web3Token (ERC-20)

- **Supply Management**: 1 billion max supply with initial 100M
- **Batch Operations**: Transfer to multiple recipients in one transaction
- **Permit Support**: Gasless approvals using EIP-2612
- **Access Control**: Owner-only minting
- **Burn Mechanism**: Token holders can burn their tokens

### Web3NFT (ERC-721)

- **Limited Supply**: 10,000 NFT maximum
- **Whitelist System**: Controllable whitelist for minting
- **Pricing**: 0.05 ETH per mint
- **Per-Wallet Limit**: Maximum 5 NFTs per wallet
- **Metadata**: Updatable base URI and per-token URIs
- **Owner Tools**: Batch minting, whitelist management, withdrawals

## 🧪 Testing

Run comprehensive tests:

```bash
npx hardhat test
npx hardhat coverage  # With coverage report
```

## 📖 Learn More

- [Hardhat Documentation](https://hardhat.org/docs)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts)
- [Solidity Documentation](https://docs.soliditylang.org/)
- [Ethereum Development](https://ethereum.org/en/developers/)

## 🔐 Security

These contracts use:
- OpenZeppelin audited libraries
- Solidity 0.8.20+ (built-in overflow protection)
- Access control patterns
- Reentrancy guards where applicable

**Note**: These are educational examples. Always conduct professional audits before production use.

## 📄 License

MIT License - See LICENSE file for details
