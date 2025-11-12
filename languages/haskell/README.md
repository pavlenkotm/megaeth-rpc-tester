# 🎩 Haskell Blockchain Development

Professional Haskell examples for blockchain development, including Ethereum RPC client and Cardano Plutus smart contracts.

## 📋 Contents

- **Web3Client.hs** - Ethereum RPC client
  - JSON-RPC calls
  - Block queries
  - Type-safe operations
  - Functional patterns

- **PlutusValidator.hs** - Cardano Plutus smart contracts
  - Validator scripts for Cardano
  - Token minting policies
  - Datum and Redeemer patterns
  - On-chain validation logic
  - Type-safe smart contracts

## 🚀 Quick Start

### Ethereum RPC Client

```bash
cd languages/haskell

# Install dependencies
cabal update
cabal install aeson http-conduit bytestring

# Compile
ghc -o web3-client Web3Client.hs

# Run
./web3-client
```

### Cardano Plutus Contracts

```bash
cd languages/haskell

# Install Plutus dependencies (requires Nix)
curl -L https://nixos.org/nix/install | sh
nix-shell

# Compile Plutus contract
cabal build

# Run Plutus in playground
plutus-playground-server
```

## 📚 Features

### Ethereum Client

- Type-safe RPC calls
- Functional composition
- Maybe monad for errors
- JSON parsing with Aeson

### Cardano Plutus Contracts

- **Validators**: Lock and unlock funds with custom logic
- **Minting Policies**: Create native tokens
- **Datum/Redeemer**: Type-safe on-chain data
- **Script Contexts**: Access transaction information
- **Plutus Core**: Compile to on-chain code

## 🔧 Plutus Examples

### Simple Validator

Lock funds with a secret number:

```haskell
mkValidator :: SecretDatum -> SecretRedeemer -> ScriptContext -> Bool
mkValidator datum redeemer _ =
    traceIfFalse "Wrong secret!" $ guess redeemer == secretNumber datum
```

### Minting Policy

One-time minting policy:

```haskell
mkPolicy :: TxOutRef -> () -> ScriptContext -> Bool
mkPolicy oref () ctx = traceIfFalse "UTXO not consumed" hasUTxO
  where
    info = scriptContextTxInfo ctx
    hasUTxO = any (\i -> txInInfoOutRef i == oref) $ txInfoInputs info
```

## 🧪 Testing

### Ethereum Client

```bash
# Run with custom RPC endpoint
RPC_URL=https://eth.llamarpc.com ./web3-client
```

### Plutus Contracts

```bash
# Run Plutus tests
cabal test

# Use Plutus emulator
cabal repl
> import Wallet.Emulator
> runEmulatorTraceIO myTrace
```

## 📖 Project Structure

```
haskell/
├── Web3Client.hs        # Ethereum RPC client
├── PlutusValidator.hs   # Cardano Plutus contracts
├── cabal.project        # Cabal configuration
└── README.md            # This file
```

## 🌐 Blockchain Support

- **Ethereum**: EVM-compatible chains via RPC
- **Cardano**: Plutus smart contracts on Cardano mainnet/testnet

## 🔐 Cardano Smart Contract Features

- **Extended UTXO Model**: More powerful than Bitcoin's UTXO
- **Deterministic Validation**: Predictable fees and outcomes
- **Formal Verification**: Mathematical proof of correctness
- **Low Fees**: Cost-effective smart contract execution
- **Native Tokens**: First-class token support

## 📖 Learn More

### Ethereum
- [Web3 Haskell](https://hackage.haskell.org/package/web3)
- [Ethereum JSON-RPC](https://ethereum.org/en/developers/docs/apis/json-rpc/)

### Cardano Plutus
- [Plutus Documentation](https://plutus.readthedocs.io/)
- [Cardano Developer Portal](https://developers.cardano.org/)
- [Plutus Pioneer Program](https://plutus-pioneer-program.readthedocs.io/)
- [Plutus Playground](https://playground.plutus.iohkdev.io/)

## 🎯 Use Cases

### Ethereum
- RPC endpoint monitoring
- Blockchain data analysis
- Web3 backends

### Cardano
- **DeFi**: DEXs, lending, stablecoins
- **NFTs**: Unique digital assets
- **DAOs**: Decentralized governance
- **Gaming**: Play-to-earn games
- **Supply Chain**: Traceability and verification

## 📄 License

MIT License
