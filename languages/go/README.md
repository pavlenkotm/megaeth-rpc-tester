# 🐹 Go Web3 Examples

Professional Go examples for Ethereum RPC interaction and signature verification using go-ethereum.

## 📋 Contents

- **rpc_client.go** - Complete Ethereum RPC client
  - Connect to RPC endpoints
  - Query blockchain data (blocks, balances, gas price)
  - Send transactions
  - Signature verification
  - Transaction receipt monitoring

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

### Build

```bash
# Build the binary
go build -o rpc-client .

# Run directly
go run rpc_client.go
```

### Usage Examples

```bash
# Run the example
./rpc-client

# Or run with go run
go run rpc_client.go
```

## 🔧 Features

### RPC Client

- **Block Information**: Get latest block number and block details
- **Balance Queries**: Check ETH balance of any address
- **Gas Pricing**: Retrieve current network gas prices
- **Chain Info**: Get chain ID and network information
- **Transaction Sending**: Send ETH transactions (with private key)
- **Receipt Monitoring**: Wait for transaction confirmations

### Signature Verification

- **Sign Messages**: Create Ethereum signatures
- **Verify Signatures**: Validate message authenticity
- **Recover Addresses**: Extract signer address from signature

## 📚 Code Examples

### Create RPC Client

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

### Verify Signature

```go
message := []byte("Hello, Ethereum!")
signature := []byte{...}
expectedAddr := common.HexToAddress("0x...")

isValid, err := VerifySignature(message, signature, expectedAddr)
if isValid {
    fmt.Println("Signature is valid!")
}
```

## 🧪 Testing

```bash
# Run tests
go test ./...

# With coverage
go test -cover ./...

# Verbose output
go test -v ./...
```

## 📖 Project Structure

```
go/
├── rpc_client.go    # Main RPC client implementation
├── go.mod           # Go module definition
├── go.sum           # Dependency checksums
└── README.md        # This file
```

## 🔐 Security Best Practices

- Never commit private keys
- Use environment variables for sensitive data
- Validate all inputs
- Handle errors properly
- Use context timeouts for RPC calls
- Verify transaction receipts

## 📚 Learn More

- [go-ethereum Documentation](https://geth.ethereum.org/docs)
- [Go Ethereum Book](https://goethereumbook.org/)
- [Ethereum JSON-RPC Spec](https://ethereum.org/en/developers/docs/apis/json-rpc/)

## 🎯 Use Cases

- **RPC Testing Tools**: Monitor endpoint health and performance
- **Blockchain Explorers**: Build custom blockchain data viewers
- **Trading Bots**: Automated transaction sending
- **Wallet Backends**: Manage accounts and balances
- **DApp Backends**: Server-side Web3 integration

## 📄 License

MIT License - See LICENSE file for details
