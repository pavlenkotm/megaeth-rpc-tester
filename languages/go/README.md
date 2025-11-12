# 🐹 Go Blockchain Development

Professional Go examples for blockchain development, including Ethereum RPC interaction and Cosmos SDK module development.

## 📋 Contents

- **rpc_client.go** - Complete Ethereum RPC client
  - Connect to RPC endpoints
  - Query blockchain data (blocks, balances, gas price)
  - Send transactions
  - Signature verification
  - Transaction receipt monitoring

- **cosmos_module.go** - Cosmos SDK custom module
  - Custom token creation
  - Token minting functionality
  - State management with KVStore
  - Message handlers and validation
  - Integration with bank keeper

## 🚀 Quick Start

### Prerequisites

```bash
go >= 1.21
```

### Installation

```bash
cd languages/go

# Download dependencies
go mod download
```

### Ethereum RPC Client

```bash
# Build the RPC client
go build -o rpc-client rpc_client.go

# Run
./rpc-client

# Or run directly
go run rpc_client.go
```

### Cosmos SDK Module

```bash
# Install Cosmos SDK
go get github.com/cosmos/cosmos-sdk@latest

# Build your chain with the module
go build -o mychain .

# Initialize chain
./mychain init mynode --chain-id mychain-1

# Start the chain
./mychain start
```

## 🔧 Features

### Ethereum RPC Client

- **Block Information**: Get latest block number and block details
- **Balance Queries**: Check ETH balance of any address
- **Gas Pricing**: Retrieve current network gas prices
- **Chain Info**: Get chain ID and network information
- **Transaction Sending**: Send ETH transactions (with private key)
- **Receipt Monitoring**: Wait for transaction confirmations

### Ethereum Signature Verification

- **Sign Messages**: Create Ethereum signatures
- **Verify Signatures**: Validate message authenticity
- **Recover Addresses**: Extract signer address from signature

### Cosmos SDK Module

- **Custom Tokens**: Create native tokens on Cosmos chains
- **Token Minting**: Mint additional supply (if allowed)
- **State Management**: Efficient KVStore operations
- **Message Validation**: Type-safe message handling
- **Bank Integration**: Seamless token transfers
- **Queries**: Retrieve token metadata and balances

## 📚 Code Examples

### Ethereum Examples

#### Create RPC Client

```go
client, err := NewRPCClient("https://eth.llamarpc.com", "")
if err != nil {
    log.Fatal(err)
}
```

### Get Block Number

```go
blockNumber, err := client.GetBlockNumber(context.Background())
if err != nil {
    log.Fatal(err)
}
fmt.Printf("Block: %s\n", blockNumber.String())
```

### Check Balance

```go
address := common.HexToAddress("0x...")
balance, err := client.GetBalance(ctx, address)
if err != nil {
    log.Fatal(err)
}
fmt.Printf("Balance: %s wei\n", balance.String())
```

### Send Transaction (requires private key)

```go
// Create client with private key
client, err := NewRPCClient(rpcURL, privateKeyHex)

// Send transaction
to := common.HexToAddress("0x...")
value := big.NewInt(1000000000000000000) // 1 ETH
tx, err := client.SendTransaction(ctx, to, value)
```

#### Verify Signature

```go
message := []byte("Hello, Ethereum!")
signature := []byte{...}
expectedAddr := common.HexToAddress("0x...")

isValid, err := VerifySignature(message, signature, expectedAddr)
if isValid {
    fmt.Println("Signature is valid!")
}
```

### Cosmos SDK Examples

#### Create Custom Token

```go
msg := MsgCreateToken{
    Creator:     creatorAddr,
    Denom:       "mytoken",
    TotalSupply: sdk.NewInt(1000000),
    Mintable:    true,
}

err := keeper.CreateToken(ctx, msg)
```

#### Mint Tokens

```go
msg := MsgMintToken{
    Minter: ownerAddr,
    Denom:  "mytoken",
    Amount: sdk.NewInt(5000),
    To:     recipientAddr,
}

err := keeper.MintToken(ctx, msg)
```

#### Query Token Info

```go
token, err := keeper.GetToken(ctx, "mytoken")
if err == nil {
    fmt.Printf("Token: %s\n", token.Denom)
    fmt.Printf("Supply: %s\n", token.TotalSupply)
    fmt.Printf("Owner: %s\n", token.Owner)
}
```

## 🧪 Testing

### Ethereum Client Tests

```bash
# Run tests
go test ./...

# With coverage
go test -cover ./...

# Verbose output
go test -v ./...
```

### Cosmos SDK Module Tests

```bash
# Run module tests
go test -v ./x/customtoken/...

# Integration tests
go test -v ./app/...

# Simulation tests
go test -v -run TestFullAppSimulation
```

## 📖 Project Structure

```
go/
├── rpc_client.go      # Ethereum RPC client
├── cosmos_module.go   # Cosmos SDK module
├── go.mod             # Go module definition
├── go.sum             # Dependency checksums
└── README.md          # This file
```

## 🔐 Security Best Practices

- Never commit private keys
- Use environment variables for sensitive data
- Validate all inputs
- Handle errors properly
- Use context timeouts for RPC calls
- Verify transaction receipts

## 🌐 Blockchain Support

- **Ethereum**: EVM-compatible chains (Ethereum, Polygon, BSC, etc.)
- **Cosmos SDK**: Cosmos Hub, Osmosis, Terra, Juno, Akash, etc.

## 📚 Learn More

### Ethereum
- [go-ethereum Documentation](https://geth.ethereum.org/docs)
- [Go Ethereum Book](https://goethereumbook.org/)
- [Ethereum JSON-RPC Spec](https://ethereum.org/en/developers/docs/apis/json-rpc/)

### Cosmos SDK
- [Cosmos SDK Documentation](https://docs.cosmos.network/)
- [Cosmos Academy](https://academy.cosmos.network/)
- [Cosmos SDK Tutorials](https://tutorials.cosmos.network/)
- [IBC Protocol](https://ibcprotocol.org/)

## 🎯 Use Cases

### Ethereum
- **RPC Testing Tools**: Monitor endpoint health and performance
- **Blockchain Explorers**: Build custom blockchain data viewers
- **Trading Bots**: Automated transaction sending
- **Wallet Backends**: Manage accounts and balances
- **DApp Backends**: Server-side Web3 integration

### Cosmos SDK
- **Custom Blockchains**: Build application-specific chains
- **DeFi Protocols**: DEXs, lending, staking platforms
- **NFT Marketplaces**: Native NFT support
- **Gaming**: High-performance gaming chains
- **Interoperability**: IBC-enabled cross-chain applications
- **DAOs**: On-chain governance and voting

## 📄 License

MIT License - See LICENSE file for details
