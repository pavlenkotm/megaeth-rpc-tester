package main

import (
	"context"
	"crypto/ecdsa"
	"fmt"
	"log"
	"math/big"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/crypto"
	"github.com/ethereum/go-ethereum/ethclient"
)

// RPCClient is a Go client for interacting with Ethereum RPC endpoints.
// It provides methods for querying blockchain data, sending transactions,
// and verifying signatures with comprehensive error handling.
type RPCClient struct {
	client     *ethclient.Client
	privateKey *ecdsa.PrivateKey
	address    common.Address
	rpcURL     string
}

// NewRPCClient creates a new RPC client instance
func NewRPCClient(rpcURL string, privateKeyHex string) (*RPCClient, error) {
	// Connect to Ethereum node
	client, err := ethclient.Dial(rpcURL)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to RPC: %w", err)
	}

	// Load private key if provided
	var privateKey *ecdsa.PrivateKey
	var address common.Address

	if privateKeyHex != "" {
		privateKey, err = crypto.HexToECDSA(privateKeyHex)
		if err != nil {
			return nil, fmt.Errorf("invalid private key: %w", err)
		}

		publicKey := privateKey.Public()
		publicKeyECDSA, ok := publicKey.(*ecdsa.PublicKey)
		if !ok {
			return nil, fmt.Errorf("error casting public key to ECDSA")
		}

		address = crypto.PubkeyToAddress(*publicKeyECDSA)
	}

	return &RPCClient{
		client:     client,
		privateKey: privateKey,
		address:    address,
		rpcURL:     rpcURL,
	}, nil
}

// Close closes the RPC client connection
func (r *RPCClient) Close() {
	if r.client != nil {
		r.client.Close()
	}
}

// GetAddress returns the client's Ethereum address
func (r *RPCClient) GetAddress() common.Address {
	return r.address
}

// GetRPCURL returns the RPC URL being used
func (r *RPCClient) GetRPCURL() string {
	return r.rpcURL
}

// GetBlockNumber retrieves the latest block number
func (r *RPCClient) GetBlockNumber(ctx context.Context) (*big.Int, error) {
	blockNumber, err := r.client.BlockNumber(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get block number: %w", err)
	}

	return new(big.Int).SetUint64(blockNumber), nil
}

// GetBalance retrieves the balance of an address
func (r *RPCClient) GetBalance(ctx context.Context, address common.Address) (*big.Int, error) {
	balance, err := r.client.BalanceAt(ctx, address, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to get balance: %w", err)
	}

	return balance, nil
}

// GetChainID retrieves the chain ID
func (r *RPCClient) GetChainID(ctx context.Context) (*big.Int, error) {
	chainID, err := r.client.ChainID(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get chain ID: %w", err)
	}

	return chainID, nil
}

// GetGasPrice retrieves the current gas price
func (r *RPCClient) GetGasPrice(ctx context.Context) (*big.Int, error) {
	gasPrice, err := r.client.SuggestGasPrice(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get gas price: %w", err)
	}

	return gasPrice, nil
}

// SendTransaction sends a transaction to the network
func (r *RPCClient) SendTransaction(ctx context.Context, to common.Address, value *big.Int) (*types.Transaction, error) {
	if r.privateKey == nil {
		return nil, fmt.Errorf("private key not set")
	}

	// Get nonce
	nonce, err := r.client.PendingNonceAt(ctx, r.address)
	if err != nil {
		return nil, fmt.Errorf("failed to get nonce: %w", err)
	}

	// Get gas price
	gasPrice, err := r.client.SuggestGasPrice(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get gas price: %w", err)
	}

	// Get chain ID
	chainID, err := r.client.ChainID(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to get chain ID: %w", err)
	}

	// Create transaction
	tx := types.NewTransaction(
		nonce,
		to,
		value,
		21000, // gas limit for simple transfer
		gasPrice,
		nil,
	)

	// Sign transaction
	signedTx, err := types.SignTx(tx, types.NewEIP155Signer(chainID), r.privateKey)
	if err != nil {
		return nil, fmt.Errorf("failed to sign transaction: %w", err)
	}

	// Send transaction
	err = r.client.SendTransaction(ctx, signedTx)
	if err != nil {
		return nil, fmt.Errorf("failed to send transaction: %w", err)
	}

	return signedTx, nil
}

// WaitForTransaction waits for a transaction to be mined
func (r *RPCClient) WaitForTransaction(ctx context.Context, txHash common.Hash) (*types.Receipt, error) {
	receipt, err := r.client.TransactionReceipt(ctx, txHash)
	if err != nil {
		return nil, fmt.Errorf("failed to get transaction receipt: %w", err)
	}

	return receipt, nil
}

// VerifySignature verifies an Ethereum signature
func VerifySignature(message []byte, signature []byte, expectedAddress common.Address) (bool, error) {
	// Hash the message
	hash := crypto.Keccak256Hash(message)

	// Recover public key from signature
	sigPublicKey, err := crypto.SigToPub(hash.Bytes(), signature)
	if err != nil {
		return false, fmt.Errorf("failed to recover public key: %w", err)
	}

	// Get address from public key
	recoveredAddr := crypto.PubkeyToAddress(*sigPublicKey)

	// Compare addresses
	return recoveredAddr == expectedAddress, nil
}

// Example usage
func main() {
	ctx := context.Background()

	// Create client (read-only, no private key)
	client, err := NewRPCClient("https://eth.llamarpc.com", "")
	if err != nil {
		log.Fatalf("Failed to create RPC client: %v", err)
	}

	fmt.Println("🔗 Ethereum RPC Client Example\n")

	// Get block number
	blockNumber, err := client.GetBlockNumber(ctx)
	if err != nil {
		log.Printf("Error getting block number: %v", err)
	} else {
		fmt.Printf("Latest Block: %s\n", blockNumber.String())
	}

	// Get chain ID
	chainID, err := client.GetChainID(ctx)
	if err != nil {
		log.Printf("Error getting chain ID: %v", err)
	} else {
		fmt.Printf("Chain ID: %s\n", chainID.String())
	}

	// Get gas price
	gasPrice, err := client.GetGasPrice(ctx)
	if err != nil {
		log.Printf("Error getting gas price: %v", err)
	} else {
		fmt.Printf("Gas Price: %s wei\n", gasPrice.String())
	}

	// Check balance of an address
	address := common.HexToAddress("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
	balance, err := client.GetBalance(ctx, address)
	if err != nil {
		log.Printf("Error getting balance: %v", err)
	} else {
		fmt.Printf("Balance of %s: %s wei\n", address.Hex(), balance.String())
	}

	fmt.Println("\n✅ RPC client example completed successfully")
}
