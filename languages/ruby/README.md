# 💎 Ruby Web3 Client

Simple and elegant Ruby client for Ethereum RPC interaction.

## 📋 Contents

- **web3_client.rb** - Ruby Web3 RPC client
  - JSON-RPC calls
  - Block queries
  - Balance checks
  - Transaction monitoring
  - Gas price fetching

## 🚀 Quick Start

```bash
cd languages/ruby

# Make executable
chmod +x web3_client.rb

# Run
ruby web3_client.rb
```

## 📚 Usage

```ruby
require_relative 'web3_client'

client = Web3Client.new('https://eth.llamarpc.com')

# Get block number
puts client.block_number

# Get balance
balance = client.get_balance('0x...')
puts client.wei_to_eth(balance)
```

## 📄 License

MIT License
