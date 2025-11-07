# 🐚 Bash Deployment Scripts

Professional Bash scripts for Web3 development, deployment, and node management.

## 📋 Contents

- **deploy.sh** - Smart contract deployment script
  - Multi-framework support (Hardhat, Foundry)
  - Network connection checks
  - Gas price monitoring
  - Deployment backups
  - Error handling

- **node-manager.sh** - Ethereum node management
  - Start/stop node operations
  - Sync status monitoring
  - Log management
  - Multi-node support (Geth, Erigon, Nethermind)

## 🚀 Quick Start

### Prerequisites

```bash
# Basic tools
sudo apt-get install curl jq

# Node.js (for Hardhat)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Foundry (optional)
curl -L https://foundry.paradigm.xyz | bash
```

### Make Scripts Executable

```bash
cd languages/bash
chmod +x *.sh
```

## 🔧 Usage

### Contract Deployment

```bash
# Basic deployment
./deploy.sh

# With custom network
NETWORK=sepolia RPC_URL=https://eth-sepolia.g.alchemy.com/v2/your-key ./deploy.sh

# With all options
NETWORK=mainnet \
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/your-key \
PRIVATE_KEY=your_private_key \
./deploy.sh
```

### Node Management

```bash
# Start node
./node-manager.sh start

# Check sync status
./node-manager.sh status

# View logs
./node-manager.sh logs

# Stop node
./node-manager.sh stop

# Custom configuration
NODE_TYPE=geth \
NETWORK=mainnet \
DATA_DIR=./my-node-data \
HTTP_PORT=8545 \
./node-manager.sh start
```

## 📚 Features

### Deploy Script

- **Dependency Checks**: Verifies required tools are installed
- **Network Validation**: Tests RPC connectivity before deployment
- **Gas Monitoring**: Fetches current gas prices
- **Chain Detection**: Automatically detects chain ID
- **Backup System**: Saves deployment history
- **Multi-Framework**: Supports Hardhat and Foundry
- **Error Handling**: Comprehensive error checking

### Node Manager

- **Multiple Clients**: Supports Geth, Erigon, Nethermind
- **Process Management**: PID-based process tracking
- **Sync Monitoring**: Real-time sync status
- **Log Viewing**: Tail logs in real-time
- **Port Configuration**: Customizable HTTP/WS/metrics ports
- **Network Selection**: Mainnet, testnet, or custom networks

## 🎯 Common Tasks

### Deploy to Testnet

```bash
# Set environment variables
export NETWORK=sepolia
export RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_KEY
export PRIVATE_KEY=your_private_key

# Run deployment
./deploy.sh
```

### Run Local Node

```bash
# Start Geth in dev mode
NODE_TYPE=geth \
NETWORK=dev \
DATA_DIR=./devnet \
./node-manager.sh start

# Check it's running
./node-manager.sh status
```

### Monitor Gas Prices

```bash
# Extract gas price check into standalone
curl -s -X POST -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}' \
  https://eth.llamarpc.com | jq -r '.result'
```

## 🔐 Security Best Practices

- **Never commit private keys**: Use environment variables
- **Secure RPC endpoints**: Use authenticated endpoints for production
- **Validate inputs**: Scripts include input validation
- **Backup deployments**: Automatic backup before each deploy
- **Error handling**: Exit on errors with set -e

## 📖 Environment Variables

### Deploy Script

| Variable | Default | Description |
|----------|---------|-------------|
| `NETWORK` | localhost | Network to deploy to |
| `RPC_URL` | http://localhost:8545 | RPC endpoint URL |
| `PRIVATE_KEY` | - | Deployer private key |
| `GAS_PRICE` | auto | Gas price (auto or specific value) |
| `GAS_LIMIT` | 3000000 | Gas limit for transactions |

### Node Manager

| Variable | Default | Description |
|----------|---------|-------------|
| `NODE_TYPE` | geth | Node client (geth/erigon/nethermind) |
| `DATA_DIR` | ./ethereum-data | Data directory |
| `NETWORK` | mainnet | Network to connect to |
| `HTTP_PORT` | 8545 | HTTP RPC port |
| `WS_PORT` | 8546 | WebSocket port |
| `METRICS_PORT` | 6060 | Metrics port |

## 🧪 Testing Scripts

```bash
# Test deployment script
bash -x deploy.sh  # Debug mode

# Test node manager
./node-manager.sh start
./node-manager.sh status
./node-manager.sh stop
```

## 📄 License

MIT License - See LICENSE file for details
