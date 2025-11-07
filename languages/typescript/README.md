# 🔷 TypeScript Web3 Examples

Professional TypeScript examples for building modern Web3 DApps with React, Ethers.js, and Wagmi.

## 📋 Contents

- **WalletConnect.tsx** - React component for wallet connection
  - MetaMask integration
  - Balance display
  - Network detection
  - Account change handling

- **useContract.ts** - Custom React hook for smart contract interaction
  - Read contract functions
  - Write transactions
  - Event listening
  - Error handling

- **web3Utils.ts** - Utility functions for Web3 development
  - Address formatting
  - Network helpers
  - Gas calculation
  - Explorer links
  - Token management

## 🚀 Quick Start

### Prerequisites

```bash
node >= 18.0.0
npm >= 9.0.0
```

### Installation

```bash
cd languages/typescript
npm install
```

### Development

```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Linting & Formatting

```bash
# Lint code
npm run lint

# Format code
npm run format
```

## 🔧 Usage Examples

### Wallet Connection

```tsx
import { WalletConnect } from './WalletConnect';

function App() {
  const handleConnect = (address: string) => {
    console.log('Connected:', address);
  };

  return (
    <WalletConnect
      onConnect={handleConnect}
      onDisconnect={() => console.log('Disconnected')}
    />
  );
}
```

### Contract Interaction

```tsx
import { useContract } from './hooks/useContract';

const ERC20_ABI = [...];
const TOKEN_ADDRESS = '0x...';

function TokenBalance() {
  const { callFunction, sendTransaction, loading } = useContract(
    TOKEN_ADDRESS,
    ERC20_ABI
  );

  const getBalance = async (address: string) => {
    const balance = await callFunction('balanceOf', address);
    return balance;
  };

  const transfer = async (to: string, amount: bigint) => {
    const tx = await sendTransaction('transfer', to, amount);
    return tx;
  };

  return <div>...</div>;
}
```

### Using Web3 Utilities

```tsx
import web3Utils from './utils/web3Utils';

// Format address
const short = web3Utils.shortenAddress('0x1234...5678');

// Validate address
const isValid = web3Utils.isValidAddress(address);

// Get explorer link
const link = web3Utils.getExplorerUrl(address, 1, 'address');

// Format Ether
const formatted = web3Utils.formatEther(balance, 4);

// Switch network
await web3Utils.switchNetwork(137); // Polygon

// Add token to wallet
await web3Utils.addTokenToWallet(
  tokenAddress,
  'TOKEN',
  18,
  tokenImage
);
```

## 📚 Key Features

### WalletConnect Component

- Automatic connection detection
- Balance monitoring
- Network change handling
- Account switching support
- Clean disconnect flow

### useContract Hook

- Type-safe contract interaction
- Automatic transaction waiting
- Event subscription management
- Loading and error states
- Transaction receipt handling

### Web3 Utilities

- **Address Helpers**: Format, validate, shorten addresses
- **Network Helpers**: Get network names, switch chains
- **Gas Utilities**: Estimate with buffer, calculate costs
- **Explorer Links**: Generate etherscan/polygonscan URLs
- **Token Management**: Add tokens to MetaMask
- **Conversion**: Wei/Ether, Hex/Decimal conversions

## 🎯 Supported Networks

- Ethereum Mainnet & Testnets (Goerli, Sepolia)
- Polygon (Mainnet & Mumbai)
- Arbitrum (One & Goerli)
- Optimism (Mainnet & Goerli)
- BSC (Mainnet & Testnet)

## 🧪 Testing

```bash
npm test
```

## 📖 Learn More

- [Ethers.js Documentation](https://docs.ethers.org/)
- [Wagmi Documentation](https://wagmi.sh/)
- [Viem Documentation](https://viem.sh/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

## 🔐 Security Best Practices

- Never expose private keys
- Validate all user inputs
- Use proper error handling
- Implement transaction confirmations
- Add spending limits where appropriate
- Verify contract addresses

## 📄 License

MIT License - See LICENSE file for details
